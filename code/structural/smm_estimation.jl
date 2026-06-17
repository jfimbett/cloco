# Minimum Distance Estimation of the Two-Type Vickrey Auction Model
# ==================================================================
#
#   - Julia compiled code eliminates per-call Python overhead in DE inner loop
#   - Differential evolution implemented natively (rand/1/bin scheme)
#   - Local polish via Optim.jl Fminbox(LBFGS()) — equivalent to scipy L-BFGS-B
#   - 7 moments per group (8 bins, young baseline) from 10_structural_moments.py
#   - Full 7×7 HC1 VCV as weighting matrix (optimal MD)
#   - moments_integrated() via bin-averaged log prices (no midpoint bias)
#   - J-test of overidentification (7 moments, fix_lambda has 5 free params → 2 df)
#   - Bootstrap SEs as primary inference (delta-method as secondary)
#
# Three specifications:
#   :unrestricted  — 6 free params, 7 moments (1 df over-identified)
#   :fix_lambda    — 5 free params, 7 moments (2 df over-identified)  ← PREFERRED
#   :fix_lambda_ak — 4 free params, 7 moments (3 df over-identified)
#
# Reference: quality_reports/structural_strategy_2026-03-29.md

include("model_solver.jl")

using JSON3
using LinearAlgebra
using Statistics
using Random
using Optim
using Distributions
using Printf

const ROOT = joinpath(@__DIR__, "..", "..")
const MOMENTS_FILE = joinpath(ROOT, "output", "structural_moments_fine.json")

const PARAM_NAMES_FULL = ["alpha_c", "v_bar_k", "alpha_k", "gamma", "delta", "lam_bar"]

# Bin edges — must match 10_structural_moments.py
const BIN_EDGES = Dict{String,Tuple{Float64,Float64}}(
    "young"    => (0.0,  0.4),
    "pre1"     => (0.4,  0.8),
    "pre2"     => (0.8,  1.0),
    "peak1"    => (1.0,  1.4),
    "peak2"    => (1.4,  1.6),
    "trough"   => (1.6,  2.0),
    "antique1" => (2.0,  2.5),
    "antique2" => (2.5,  3.1),
)

# lam_bar proxies: (1 − high-price share) = consumption-buyer fraction
const LAMBDA_PROXIES = Dict{String,Float64}(
    "Bordeaux Grand Cru (red)" => 1.0 - 0.390,
    "Burgundy Grand Cru"       => 1.0 - 0.515,
    "Burgundy Premier Cru"     => 1.0 - 0.112,
)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

struct CategoryData
    category    :: String
    moments     :: Vector{Float64}
    vcov        :: Matrix{Float64}
    bin_labels  :: Vector{String}
    bin_midpoints :: Vector{Float64}
    bins        :: Vector{Tuple{String,Float64,Float64}}
    N           :: Int
    N_eff       :: Float64
    n_moments   :: Int
end

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

function labels_to_bins(labels::Vector{String})::Vector{Tuple{String,Float64,Float64}}
    [(lab, BIN_EDGES[lab][1], BIN_EDGES[lab][2]) for lab in labels]
end

function load_empirical_data()::Dict{String,CategoryData}
    isfile(MOMENTS_FILE) || error(
        "Run 10_structural_moments.py first to generate $MOMENTS_FILE"
    )
    raw = JSON3.read(read(MOMENTS_FILE, String))
    data = Dict{String,CategoryData}()
    for (cat, d) in pairs(raw)
        cat_str = String(cat)
        labels  = [String(s) for s in d[:bin_labels]]
        moms    = Float64.(d[:moments])
        n_m     = length(moms)
        vcov    = Matrix{Float64}(undef, n_m, n_m)
        for (i, row) in enumerate(d[:vcov])
            for (j, val) in enumerate(row)
                vcov[i, j] = Float64(val)
            end
        end
        data[cat_str] = CategoryData(
            cat_str, moms, vcov, labels,
            Float64.(d[:bin_midpoints]),
            labels_to_bins(labels),
            Int(d[:N]), Float64(d[:N_eff]), n_m,
        )
    end
    data
end

const EMPIRICAL_DATA = load_empirical_data()

# ---------------------------------------------------------------------------
# Specification helpers
# ---------------------------------------------------------------------------

function expand_theta(phi::Vector{Float64}, spec::Symbol, lam_bar_fixed::Float64)::Vector{Float64}
    if spec == :unrestricted
        return phi
    elseif spec == :fix_lambda
        return [phi[1], phi[2], phi[3], phi[4], phi[5], lam_bar_fixed]
    elseif spec == :fix_lambda_ak
        return [phi[1], phi[2], 0.0, phi[3], phi[4], lam_bar_fixed]
    else
        error("Unknown spec: $spec")
    end
end

function get_bounds(spec::Symbol)::Vector{Tuple{Float64,Float64}}
    if spec == :unrestricted
        return [(0.01, 30.0), (0.01, 30.0), (0.00, 15.0),
                (0.1,  30.0), (0.01, 30.0), (0.01, 0.99)]
    elseif spec == :fix_lambda
        return [(0.01, 30.0), (0.01, 30.0), (0.00, 15.0),
                (0.1,  30.0), (0.01, 30.0)]
    elseif spec == :fix_lambda_ak
        return [(0.01, 30.0), (0.01, 30.0),
                (0.1,  30.0), (0.01, 30.0)]
    else
        error("Unknown spec: $spec")
    end
end

function get_param_names(spec::Symbol)::Vector{String}
    if spec == :unrestricted
        return copy(PARAM_NAMES_FULL)
    elseif spec == :fix_lambda
        return ["alpha_c", "v_bar_k", "alpha_k", "gamma", "delta"]
    elseif spec == :fix_lambda_ak
        return ["alpha_c", "v_bar_k", "gamma", "delta"]
    else
        error("Unknown spec: $spec")
    end
end

# ---------------------------------------------------------------------------
# Objective
# ---------------------------------------------------------------------------

function md_objective(theta::Vector{Float64}, m_data::Vector{Float64},
                      W::Matrix{Float64},
                      bins::Vector{Tuple{String,Float64,Float64}},
                      n::Int=5)::Float64
    m_model = moments_integrated(theta, bins, n)
    diff    = m_data - m_model
    dot(diff, W * diff)
end

# ---------------------------------------------------------------------------
# Differential Evolution (rand/1/bin, box-constrained)
# ---------------------------------------------------------------------------

"""
    de_optimize(obj, bounds; popsize_mult, maxiter, F, CR, seed) -> (best_x, best_f)

Differential evolution (DE/rand/1/bin) with box constraints.
Parameters match scipy.optimize.differential_evolution defaults:
  popsize_mult=25, maxiter=1000, F∈[0.5,1.5] dithered, CR=0.9.
"""
function de_optimize(obj::Function, bounds::Vector{Tuple{Float64,Float64}};
                     popsize_mult::Int=25, maxiter::Int=1000,
                     F_lo::Float64=0.5, F_hi::Float64=1.5,
                     CR::Float64=0.9, seed::Int=42)

    n  = length(bounds)
    NP = popsize_mult * n
    lo = [b[1] for b in bounds]
    hi = [b[2] for b in bounds]
    rng = MersenneTwister(seed)

    # Initialize population uniformly within bounds
    pop = [lo .+ rand(rng, n) .* (hi .- lo) for _ in 1:NP]
    fitness = [obj(x) for x in pop]

    best_idx = argmin(fitness)
    best_x   = copy(pop[best_idx])
    best_f   = fitness[best_idx]

    # Temporary buffer to avoid allocation in the loop
    mutant = Vector{Float64}(undef, n)
    trial  = Vector{Float64}(undef, n)

    for _ in 1:maxiter
        for i in 1:NP
            # Select three distinct indices r1, r2, r3 ≠ i
            r1 = i; while r1 == i;            r1 = rand(rng, 1:NP); end
            r2 = i; while r2 == i || r2 == r1; r2 = rand(rng, 1:NP); end
            r3 = i; while r3 == i || r3 == r1 || r3 == r2; r3 = rand(rng, 1:NP); end

            # Dithered F (sampled per vector)
            F = F_lo + rand(rng) * (F_hi - F_lo)

            # Mutation: mutant = pop[r1] + F*(pop[r2] - pop[r3])
            @inbounds for j in 1:n
                mutant[j] = clamp(pop[r1][j] + F * (pop[r2][j] - pop[r3][j]), lo[j], hi[j])
            end

            # Crossover (binomial)
            j_rand = rand(rng, 1:n)
            @inbounds for j in 1:n
                trial[j] = (j == j_rand || rand(rng) < CR) ? mutant[j] : pop[i][j]
            end

            # Selection
            f_trial = obj(trial)
            if f_trial < fitness[i]
                pop[i] = copy(trial)
                fitness[i] = f_trial
                if f_trial < best_f
                    best_f = f_trial
                    best_x = copy(trial)
                end
            end
        end
    end

    best_x, best_f
end

# ---------------------------------------------------------------------------
# Jacobian and delta-method SEs
# ---------------------------------------------------------------------------

function compute_jacobian(theta::Vector{Float64}, spec::Symbol,
                          lam_bar_fixed::Float64,
                          bins::Vector{Tuple{String,Float64,Float64}},
                          n::Int=5, eps::Float64=1e-6)::Matrix{Float64}
    free_names = get_param_names(spec)
    n_free    = length(free_names)
    n_moments = length(bins)

    phi = spec == :unrestricted ? theta[1:6] :
          spec == :fix_lambda   ? theta[1:5] :
          [theta[1], theta[2], theta[4], theta[5]]

    J = Matrix{Float64}(undef, n_moments, n_free)
    for j in 1:n_free
        step  = max(eps, abs(phi[j]) * eps)
        phi_p = copy(phi); phi_p[j] += step
        phi_m = copy(phi); phi_m[j] -= step
        m_p = moments_integrated(expand_theta(phi_p, spec, lam_bar_fixed), bins, n)
        m_m = moments_integrated(expand_theta(phi_m, spec, lam_bar_fixed), bins, n)
        J[:, j] = (m_p - m_m) / (2.0 * step)
    end
    J
end

function delta_method_se(theta::Vector{Float64}, W::Matrix{Float64},
                         vcov_data::Matrix{Float64}, spec::Symbol,
                         lam_bar_fixed::Float64,
                         bins::Vector{Tuple{String,Float64,Float64}},
                         n::Int=5)
    J = compute_jacobian(theta, spec, lam_bar_fixed, bins, n)
    JWJ = J' * W * J

    F = eigen(Symmetric(JWJ))
    eigvals_v = F.values
    threshold = 1e-10 * max(maximum(eigvals_v), 1e-15)
    jac_rank  = count(v -> v > threshold, eigvals_v)
    pos_eigs  = filter(v -> v > 0, eigvals_v)
    jac_cond  = isempty(pos_eigs) ? Inf : maximum(eigvals_v) / minimum(pos_eigs)

    null_idx   = findall(v -> v <= threshold, eigvals_v)
    null_space = [(eigvals_v[i], F.vectors[:, i]) for i in null_idx]

    n_free = size(J, 2)
    se_phi = try
        JWJ_inv = jac_rank < n_free ? pinv(JWJ) : inv(JWJ)
        V = JWJ_inv * (J' * W * vcov_data * W * J) * JWJ_inv
        sqrt.(max.(diag(V), 0.0))
    catch
        fill(NaN, n_free)
    end

    se_phi, J, jac_rank, jac_cond, null_space
end

# ---------------------------------------------------------------------------
# Estimation
# ---------------------------------------------------------------------------

"""
    estimate_category(category; n, n_starts, seed, verbose, spec) -> Dict

Hybrid DE + L-BFGS-B estimation for one wine category.
Phase 1: DE/rand/1/bin (popsize=25×n_free, maxiter=1000) — global search
Phase 2: Optim Fminbox(LBFGS()) polish from DE solution + n_starts random starts
"""
function estimate_category(category::String; n::Int=5, n_starts::Int=50,
                           seed::Int=42, verbose::Bool=true,
                           spec::Symbol=:fix_lambda)::Dict

    data   = EMPIRICAL_DATA[category]
    m_data = data.moments
    vcov   = data.vcov
    bins   = data.bins
    n_mom  = data.n_moments

    W = try inv(vcov) catch _ pinv(vcov) end

    lam_bar_fixed = get(LAMBDA_PROXIES, category, 0.5)
    bounds        = get_bounds(spec)
    free_names    = get_param_names(spec)
    n_free        = length(free_names)
    lower         = [b[1] for b in bounds]
    upper         = [b[2] for b in bounds]

    obj_phi = phi -> md_objective(expand_theta(phi, spec, lam_bar_fixed), m_data, W, bins, n)

    # Phase 1: Differential evolution (global search)
    best_phi, best_obj = de_optimize(
        obj_phi, bounds;
        popsize_mult=25, maxiter=1000,
        F_lo=0.5, F_hi=1.5, CR=0.9, seed=seed,
    )

    # Phase 2: L-BFGS-B polish
    rng    = MersenneTwister(seed)
    starts = Vector{Vector{Float64}}()
    push!(starts, copy(best_phi))
    for _ in 1:n_starts
        push!(starts, [rand(rng) * (upper[j] - lower[j]) + lower[j] for j in 1:n_free])
    end

    converged = 0
    for phi0 in starts
        try
            res = optimize(
                obj_phi, lower, upper, phi0,
                Fminbox(LBFGS()),
                Optim.Options(iterations=5000, f_reltol=1e-15, g_tol=1e-12, show_trace=false),
            )
            Optim.converged(res) && (converged += 1)
            if Optim.minimum(res) < best_obj
                best_obj = Optim.minimum(res)
                best_phi = Optim.minimizer(res)
            end
        catch
        end
    end

    best_theta = expand_theta(best_phi, spec, lam_bar_fixed)
    m_model    = moments_integrated(best_theta, bins, n)
    diff       = m_data - m_model

    df_jtest = n_mom - n_free
    j_stat   = df_jtest > 0 ? best_obj : NaN
    p_jtest  = df_jtest > 0 ? ccdf(Chisq(df_jtest), j_stat) : NaN
    avg_sq_t = best_obj / n_mom

    se_phi, J_mat, jac_rank, jac_cond, null_space_dirs = delta_method_se(
        best_theta, W, vcov, spec, lam_bar_fixed, bins, n
    )

    theta_dict = Dict(name => best_theta[i] for (i, name) in enumerate(PARAM_NAMES_FULL))
    se_dict = Dict{String,Any}()
    se_idx = 1
    for name in PARAM_NAMES_FULL
        if name in free_names
            se_dict[name] = se_phi[se_idx]
            se_idx += 1
        else
            se_dict[name] = nothing
        end
    end

    result = Dict(
        "category"          => category,
        "specification"     => String(spec),
        "n_bidders"         => n,
        "n_free_params"     => n_free,
        "n_moments"         => n_mom,
        "df_overid"         => df_jtest,
        "theta"             => theta_dict,
        "se_delta"          => se_dict,
        "objective"         => best_obj,
        "avg_sq_t_mismatch" => avg_sq_t,
        "j_stat"            => j_stat,
        "p_jtest"           => p_jtest,
        "moments_data"  => Dict(lab => m_data[i]  for (i, lab) in enumerate(data.bin_labels)),
        "moments_model" => Dict(lab => m_model[i] for (i, lab) in enumerate(data.bin_labels)),
        "jacobian_rank"     => jac_rank,
        "jacobian_cond"     => jac_cond,
        "se_reliable"       => jac_cond < 1e10,
        "null_space"        => [(ev, vec) for (ev, vec) in null_space_dirs],
        "converged_starts"  => converged,
        "total_starts"      => length(starts),
        "N_eff"             => data.N_eff,
    )

    verbose && print_result(result, free_names, data)
    result
end

# ---------------------------------------------------------------------------
# Pretty printer
# ---------------------------------------------------------------------------

function print_result(result::Dict, free_names::Vector{String}, data::CategoryData)
    spec = result["specification"]
    cat  = result["category"]
    n    = result["n_bidders"]
    nf   = result["n_free_params"]
    nm   = result["n_moments"]
    df   = result["df_overid"]

    println("\n" * "=" ^ 72)
    println("  $cat  (n=$n, spec=$spec)")
    println("=" ^ 72)
    @printf("  Objective: %.4f   Avg sq-t: %.4f\n", result["objective"], result["avg_sq_t_mismatch"])
    @printf("  Overid df=%d  J-stat=%.2f  p(J)=%.4f\n", df, result["j_stat"], result["p_jtest"])
    @printf("  Free params: %d, Moments: %d, df=%d\n", nf, nm, df)
    se_label = result["se_reliable"] ? "[SEs reliable]" : "[SEs unreliable — use bootstrap]"
    @printf("  Jacobian rank: %d/%d  cond=%.2e  %s\n",
            result["jacobian_rank"], nf, result["jacobian_cond"], se_label)

    ses_data = sqrt.(diag(data.vcov))
    println("\n  " * @sprintf("%-12s %10s %10s %8s", "Param", "Estimate", "Delta-SE", "t-stat"))
    println("  " * "-" ^ 44)
    for name in PARAM_NAMES_FULL
        est = result["theta"][name]
        se  = result["se_delta"][name]
        if isnothing(se)
            @printf("  %-12s %10.4f %10s %8s  [fixed]\n", name, est, "--", "--")
        else
            t   = (se > 0 && !isnan(se)) ? est / se : NaN
            tag = abs(t) > 1.96 ? "*" : ""
            if result["se_reliable"]
                @printf("  %-12s %10.4f %10.4f %8.2f %s\n", name, est, se, t, tag)
            else
                @printf("  %-12s %10.4f %10s %8s  [boot req]\n", name, est, "(n/a)", "--")
            end
        end
    end

    println("\n  " * @sprintf("%-12s %9s %9s %9s %9s", "Bin", "Data", "Model", "Diff", "Diff/SE"))
    println("  " * "-" ^ 52)
    for (i, lab) in enumerate(data.bin_labels)
        d_val  = result["moments_data"][lab]
        m_val  = result["moments_model"][lab]
        se_val = ses_data[i]
        flag   = abs(d_val - m_val) / se_val > 3 ? " <--" : ""
        @printf("  %-12s %9.4f %9.4f %9.4f %9.2f%s\n",
                lab, d_val, m_val, d_val - m_val, (d_val - m_val) / se_val, flag)
    end

    ac  = result["theta"]["alpha_c"]
    vbk = result["theta"]["v_bar_k"]
    rho = ac > 0 ? vbk / ac : NaN
    label = rho > 1 ? "> 1: Prop.2 satisfied — no trough expected" : "< 1: trough possible"
    @printf("\n  rho = v_bar_k / alpha_c = %.3f  (%s)\n", rho, label)
end

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

function main()
    Random.seed!(42)
    all_results = Dict{String,Any}()

    for spec in [:unrestricted, :fix_lambda, :fix_lambda_ak]
        println("\n\n" * "#" ^ 75)
        println("#  SPECIFICATION: $spec")
        println("#" ^ 75)

        spec_results = Dict{String,Any}()
        for category in keys(EMPIRICAL_DATA)
            spec_results[category] = estimate_category(
                category; n=5, n_starts=50, seed=42, verbose=true, spec=spec
            )
        end
        all_results[String(spec)] = spec_results
    end

    output_path = joinpath(ROOT, "output", "structural_estimates_julia.json")
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        JSON3.write(io, all_results)
    end
    println("\nResults saved to $output_path")

    # Summary table for preferred spec
    preferred = "fix_lambda"
    results   = all_results[preferred]
    cats      = collect(keys(EMPIRICAL_DATA))

    println("\n\n" * "=" ^ 90)
    println("  PREFERRED SPECIFICATION: fix_lambda  (5 free params, 7 moments, 2 df overidentified)")
    println("=" ^ 90)

    println("\n  " * @sprintf("%-34s %9s %9s %9s %8s %4s %6s",
                              "Category", "Obj", "Avg sq-t", "J-stat", "p(J)", "df", "Rank"))
    println("  " * "-" ^ 82)
    for cat in cats
        r = results[cat]
        @printf("  %-34s %9.3f %9.4f %9.2f %8.4f %4d %6d\n",
                cat, r["objective"], r["avg_sq_t_mismatch"],
                r["j_stat"], r["p_jtest"], r["df_overid"], r["jacobian_rank"])
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end

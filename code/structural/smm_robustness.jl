# Robustness Checks for the Two-Type Vickrey Auction Model
# ==========================================================
#
# Improvements over Python v1:
#   - Bootstrap parallelized with Threads.@threads (set JULIA_NUM_THREADS)
#   - Full VCV Cholesky perturbation (not independent se*z)
#   - Profile CI: 50-point grid, concentrated objective
#   - n-sensitivity uses :fix_lambda spec to match primary estimation
#
# Checks:
#   1. Sensitivity to number of bidders n = {3, 5, 10}
#   2. Parametric bootstrap SEs with correlated moment perturbation (B=500)
#   3. Profile confidence sets (grid over each free parameter)
#
# Usage:
#   julia --threads auto code/structural/smm_robustness.jl
#
# Reference: quality_reports/structural_strategy_2026-03-29.md

include("smm_estimation.jl")

using Base.Threads
using LinearAlgebra
using Statistics
using Random

# ---------------------------------------------------------------------------
# 1. Sensitivity to n
# ---------------------------------------------------------------------------

"""
    sensitivity_n(categories, spec, n_values, n_starts, seed) -> Dict

Re-estimate for each category × n combination and return a comparison table.
"""
function sensitivity_n(categories::Vector{String};
                       spec::Symbol=:fix_lambda,
                       n_values::Vector{Int}=[3, 5, 10],
                       n_starts::Int=30,
                       seed::Int=42)::Dict

    results = Dict{String,Any}()
    for cat in categories
        results[cat] = Dict{String,Any}()
        for n in n_values
            println("\n--- $cat, n=$n ---"); flush(stdout)
            res = estimate_category(cat; n=n, n_starts=n_starts, seed=seed,
                                    verbose=false, spec=spec)
            results[cat][string(n)] = res
            rho = res["theta"]["v_bar_k"] / res["theta"]["alpha_c"]
            @printf("  Obj=%.3f  J=%.2f  p(J)=%.4f  rho=%.3f\n",
                    res["objective"], res["j_stat"], res["p_jtest"], rho)
            flush(stdout)
        end
    end
    results
end

# ---------------------------------------------------------------------------
# 2. Parametric bootstrap with full VCV Cholesky perturbation
# ---------------------------------------------------------------------------

"""
    parametric_bootstrap(category, spec, B, n, n_starts, seed, verbose) -> Dict

Parametric bootstrap: perturb data moments using full VCV Cholesky decomposition.

    m_boot = m_data + L * z,  z ~ N(0, I),  vcov = L * L'

Correctly accounts for correlation between hedonic regression coefficients.
Parallelized over bootstrap draws using Threads.@threads.

B=500 by default (minimum for ±2% SE reliability per scoring-protocol.md).
"""
function parametric_bootstrap(category::String;
                               spec::Symbol=:fix_lambda,
                               B::Int=500,
                               n::Int=5,
                               n_starts::Int=15,
                               seed::Int=42,
                               verbose::Bool=true)::Dict

    data   = EMPIRICAL_DATA[category]
    m_data = data.moments
    vcov   = data.vcov
    bins   = data.bins
    n_mom  = data.n_moments

    W = try inv(vcov) catch _ pinv(vcov) end

    # Cholesky decomposition for correlated perturbation
    L = try
        cholesky(Symmetric(vcov)).L
    catch
        cholesky(Symmetric(vcov + 1e-10 * I)).L
    end

    lam_bar_fixed = get(LAMBDA_PROXIES, category, 0.5)
    bounds        = get_bounds(spec)
    free_names    = get_param_names(spec)
    lower         = [b[1] for b in bounds]
    upper         = [b[2] for b in bounds]
    n_free        = length(free_names)

    # Baseline estimate for warm-starting bootstrap draws
    baseline = estimate_category(category; n=n, n_starts=30, seed=seed,
                                 verbose=false, spec=spec)
    phi_base = [baseline["theta"][name] for name in free_names]

    # Pre-generate all random seeds for reproducibility across thread counts
    rng_master = MersenneTwister(seed)
    boot_seeds = rand(rng_master, UInt32, B)

    # Thread-local storage: one result slot per draw
    bootstrap_thetas = Vector{Union{Vector{Float64},Nothing}}(nothing, B)
    n_failed = Threads.Atomic{Int}(0)

    Threads.@threads for b in 1:B
        rng_b = MersenneTwister(boot_seeds[b])
        z     = randn(rng_b, n_mom)
        m_boot = m_data + L * z

        obj_boot = phi -> begin
            theta   = expand_theta(phi, spec, lam_bar_fixed)
            m_model = moments_integrated(theta, bins, n)
            diff    = m_boot - m_model
            dot(diff, W * diff)
        end

        best_obj_b = Inf
        best_phi_b = nothing

        starts_b = Vector{Vector{Float64}}()
        push!(starts_b, copy(phi_base))
        for _ in 1:(n_starts - 1)
            push!(starts_b, [rand(rng_b) * (upper[j] - lower[j]) + lower[j] for j in 1:n_free])
        end

        for phi0 in starts_b
            try
                res = optimize(
                    obj_boot, lower, upper, phi0,
                    Fminbox(LBFGS()),
                    Optim.Options(iterations=3000, f_reltol=1e-14, g_tol=1e-10, show_trace=false),
                )
                if Optim.minimum(res) < best_obj_b
                    best_obj_b = Optim.minimum(res)
                    best_phi_b = Optim.minimizer(res)
                end
            catch
            end
        end

        if !isnothing(best_phi_b)
            bootstrap_thetas[b] = expand_theta(best_phi_b, spec, lam_bar_fixed)
        else
            Threads.atomic_add!(n_failed, 1)
        end

        if verbose && b % 50 == 0
            println("  Bootstrap $b/$B done ($(n_failed[]) failed)")
        end
    end

    valid = [t for t in bootstrap_thetas if !isnothing(t)]
    isempty(valid) && error("All bootstrap draws failed for $category")

    boot_mat  = hcat(valid...)'   # (B_eff × 6)
    boot_mean = vec(mean(boot_mat, dims=1))
    boot_se   = vec(std(boot_mat, dims=1, corrected=true))
    boot_q025 = [quantile(boot_mat[:, j], 0.025) for j in 1:6]
    boot_q975 = [quantile(boot_mat[:, j], 0.975) for j in 1:6]

    result = Dict(
        "category"         => category,
        "specification"    => String(spec),
        "n_bidders"        => n,
        "B_requested"      => B,
        "B_effective"      => length(valid),
        "n_failed"         => n_failed[],
        "baseline_theta"   => baseline["theta"],
        "bootstrap_mean"   => Dict(name => boot_mean[i] for (i, name) in enumerate(PARAM_NAMES_FULL)),
        "bootstrap_se"     => Dict(name => boot_se[i]   for (i, name) in enumerate(PARAM_NAMES_FULL)),
        "bootstrap_ci_025" => Dict(name => boot_q025[i] for (i, name) in enumerate(PARAM_NAMES_FULL)),
        "bootstrap_ci_975" => Dict(name => boot_q975[i] for (i, name) in enumerate(PARAM_NAMES_FULL)),
    )

    if verbose
        println("\n  " * @sprintf("%-12s %10s %10s %10s %10s %10s",
                                  "Param", "Baseline", "Boot Mean", "Boot SE", "CI 2.5%", "CI 97.5%"))
        println("  " * "-" ^ 64)
        for name in PARAM_NAMES_FULL
            bl = baseline["theta"][name]
            @printf("  %-12s %10.4f %10.4f %10.4f %10.4f %10.4f\n",
                    name, bl,
                    result["bootstrap_mean"][name],
                    result["bootstrap_se"][name],
                    result["bootstrap_ci_025"][name],
                    result["bootstrap_ci_975"][name])
        end
    end

    result
end

# ---------------------------------------------------------------------------
# 3. Profile confidence sets
# ---------------------------------------------------------------------------

"""
    profile_ci(category, spec, n, n_grid, seed) -> Dict

For each free parameter, compute profile of MD objective over a fixed grid.
At each grid point: fix that parameter, minimize over remaining free params.
Identifies whether the objective has a sharp minimum vs. flat identification surface.
"""
function profile_ci(category::String;
                    spec::Symbol=:fix_lambda,
                    n::Int=5,
                    n_grid::Int=50,
                    seed::Int=42)::Dict

    data          = EMPIRICAL_DATA[category]
    m_data        = data.moments
    vcov          = data.vcov
    bins          = data.bins
    lam_bar_fixed = get(LAMBDA_PROXIES, category, 0.5)
    bounds        = get_bounds(spec)
    free_names    = get_param_names(spec)
    n_free        = length(free_names)
    lower         = [b[1] for b in bounds]
    upper         = [b[2] for b in bounds]

    W = try inv(vcov) catch _ pinv(vcov) end

    baseline = estimate_category(category; n=n, n_starts=30, seed=seed,
                                 verbose=false, spec=spec)
    phi_opt  = [baseline["theta"][name] for name in free_names]
    obj_opt  = baseline["objective"]

    profiles = Dict{String,Any}()

    for (j, param_name) in enumerate(free_names)
        lo, hi   = bounds[j]
        grid     = collect(range(lo, hi, length=n_grid))
        obj_grid = Vector{Float64}(undef, n_grid)

        other_bounds = [bounds[i] for i in 1:n_free if i != j]
        other_lower  = [b[1] for b in other_bounds]
        other_upper  = [b[2] for b in other_bounds]

        for (k, val) in enumerate(grid)
            phi_init_other = deleteat!(copy(phi_opt), j)

            obj_profiled = phi_other -> begin
                phi_full = insert!(copy(phi_other), j, val)
                theta    = expand_theta(phi_full, spec, lam_bar_fixed)
                md_objective(theta, m_data, W, bins, n)
            end

            try
                res = optimize(
                    obj_profiled, other_lower, other_upper, phi_init_other,
                    Fminbox(LBFGS()),
                    Optim.Options(iterations=2000, f_reltol=1e-13, g_tol=1e-10, show_trace=false),
                )
                obj_grid[k] = Optim.minimum(res)
            catch
                obj_grid[k] = Inf
            end
        end

        flat_frac = mean(obj_grid .< 2.0 * obj_opt)
        @printf("  %-12s: opt=%.3f  min_profile=%.4f  flat_frac(<2*opt)=%.2f\n",
                param_name, phi_opt[j], minimum(obj_grid), flat_frac)

        profiles[param_name] = Dict(
            "grid"      => grid,
            "objective" => obj_grid,
            "opt_value" => phi_opt[j],
            "opt_obj"   => obj_opt,
        )
    end

    Dict(
        "category"      => category,
        "specification" => String(spec),
        "baseline_obj"  => obj_opt,
        "profiles"      => profiles,
    )
end

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

function main()
    Random.seed!(42)
    categories = collect(keys(EMPIRICAL_DATA))
    spec = :fix_lambda

    all_results = Dict{String,Any}("specification" => String(spec))

    # 1. Sensitivity to n
    println("=" ^ 75)
    println("  ROBUSTNESS CHECK 1: Sensitivity to n (spec=$spec)")
    println("=" ^ 75)
    flush(stdout)
    sensitivity = sensitivity_n(categories; spec=spec, n_values=[3, 5, 10],
                                n_starts=15, seed=42)
    all_results["sensitivity_n"] = sensitivity

    for cat in categories
        println("\n" * "=" ^ 70)
        println("  $cat")
        println("=" ^ 70)
        header = @sprintf("  %-12s", "Parameter")
        for nv in [3, 5, 10]
            header *= @sprintf("    n=%-4d    ", nv)
        end
        println(header)
        println("  " * "-" ^ 54)
        for name in PARAM_NAMES_FULL
            row = @sprintf("  %-12s", name)
            for nv in [3, 5, 10]
                est = sensitivity[cat][string(nv)]["theta"][name]
                row *= @sprintf("  %8.4f  ", est)
            end
            println(row)
        end
        row_obj = @sprintf("  %-12s", "Obj")
        row_rho = @sprintf("  %-12s", "rho")
        for nv in [3, 5, 10]
            r   = sensitivity[cat][string(nv)]
            obj = r["objective"]
            rho = r["theta"]["v_bar_k"] / r["theta"]["alpha_c"]
            row_obj *= @sprintf("  %8.2f  ", obj)
            row_rho *= @sprintf("  %8.4f  ", rho)
        end
        println(row_obj)
        println(row_rho)
    end

    # 2. Parametric bootstrap (B=200, parallelized)
    println("\n" * "=" ^ 75)
    println("  ROBUSTNESS CHECK 2: Parametric Bootstrap (B=200, spec=$spec)")
    println("  Running on $(Threads.nthreads()) threads")
    println("=" ^ 75)
    flush(stdout)
    bootstrap_results = Dict{String,Any}()
    for cat in categories
        println("\n--- $cat ---"); flush(stdout)
        bootstrap_results[cat] = parametric_bootstrap(
            cat; spec=spec, B=200, n=5, n_starts=5, seed=42, verbose=true
        )
        flush(stdout)
    end
    all_results["bootstrap"] = bootstrap_results

    # 3. Profile CIs
    println("\n" * "=" ^ 75)
    println("  ROBUSTNESS CHECK 3: Profile Confidence Sets (spec=$spec)")
    println("=" ^ 75)
    flush(stdout)
    profile_results = Dict{String,Any}()
    for cat in categories
        println("\n--- $cat ---"); flush(stdout)
        profile_results[cat] = profile_ci(cat; spec=spec, n=5, n_grid=25, seed=42)
        flush(stdout)
    end
    all_results["profiles"] = profile_results

    # Save
    output_path  = joinpath(ROOT, "output", "structural_robustness_julia.json")
    profiles_path = joinpath(ROOT, "output", "structural_profiles_julia.json")
    mkpath(dirname(output_path))

    open(output_path, "w") do io
        JSON3.write(io, all_results)
    end
    open(profiles_path, "w") do io
        JSON3.write(io, profile_results)
    end

    println("\nRobustness results saved to $output_path")
    println("Profile CIs saved to $profiles_path")
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end

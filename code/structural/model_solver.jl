# Model Solver for the Two-Type Vickrey Auction Model
# =====================================================

using Printf
# Closed-form equilibrium price and model-predicted moments for the
# consumption-collector wine auction model.
#
# Reference: quality_reports/theory_model_2026-03-29.md
#
# Parameters (theta): (alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar)
#   alpha_c  — consumption-type valuation scale
#   v_bar_k  — collector-type baseline valuation
#   alpha_k  — collector-type age sensitivity
#   gamma    — shape of consumption quality function h(a*)
#   delta    — rate of consumption-type exit post-maturity
#   lam_bar  — fraction of consumption-type bidders at maturity

# ---------------------------------------------------------------------------
# Segment definitions (normalised age a* = auction_age / maturity_date)
# ---------------------------------------------------------------------------

const SEGMENT_MIDPOINTS = Dict{String,Float64}(
    "young"   => 0.30,
    "approach" => 0.80,
    "peak"    => 1.30,
    "trough"  => 1.80,
    "antique" => 2.50,
)

const SEGMENT_ORDER = ["approach", "peak", "trough", "antique"]
const YOUNG_BIN = (0.0, 0.4)  # baseline bin boundaries

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

"""
    h_fn(a_star, gamma) -> Float64

Consumption quality function: h(a*) = (a*)^γ · exp(γ·(1 − a*))
Properties: h(0)=0, h(1)=1, increasing on [0,1], decreasing on (1,∞).
"""
function h_fn(a_star::Float64, gamma::Float64)::Float64
    a_star <= 0.0 && return 0.0
    (a_star^gamma) * exp(gamma * (1.0 - a_star))
end

"""
    vc_fn(a_star, alpha_c, gamma) -> Float64
Consumption-type valuation: v_c(a*) = α_c · h(a*)
"""
function vc_fn(a_star::Float64, alpha_c::Float64, gamma::Float64)::Float64
    alpha_c * h_fn(a_star, gamma)
end

"""
    vk_fn(a_star, v_bar_k, alpha_k) -> Float64
Collector-type valuation: v_k(a*) = v̄_k + α_k · a*
"""
function vk_fn(a_star::Float64, v_bar_k::Float64, alpha_k::Float64)::Float64
    v_bar_k + alpha_k * a_star
end

"""
    lam_fn(a_star, lam_bar, delta) -> Float64
Fraction of consumption-type bidders:
  λ(a*) = λ̄                           if a* ≤ 1
  λ(a*) = λ̄ · exp(−δ·(a* − 1))       if a* > 1
"""
function lam_fn(a_star::Float64, lam_bar::Float64, delta::Float64)::Float64
    a_star <= 1.0 && return lam_bar
    lam_bar * exp(-delta * (a_star - 1.0))
end

# ---------------------------------------------------------------------------
# Equilibrium price (expected second-order statistic)
# ---------------------------------------------------------------------------

"""
    price(a_star, theta, n) -> Float64

Expected second-highest bid from n i.i.d. draws of the two-point valuation
distribution {v_high with prob p_high, v_low with prob 1−p_high}.

E[Y_{(n-1:n)}] = v_high · Pr(≥2 are v_high) + v_low · Pr(≤1 is v_high)
             = v_high · (1 − prob_leq1) + v_low · prob_leq1
where
  prob_leq1 = (1−p_high)^n + n·p_high·(1−p_high)^(n−1)
"""
function price(a_star::Float64, theta::Vector{Float64}, n::Int=5)::Float64
    alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar = theta

    vc = vc_fn(a_star, alpha_c, gamma)
    vk = vk_fn(a_star, v_bar_k, alpha_k)
    la = lam_fn(a_star, lam_bar, delta)

    if vc >= vk
        v_high, v_low, p_high = vc, vk, la
    else
        v_high, v_low, p_high = vk, vc, 1.0 - la
    end

    prob_leq1 = (1.0 - p_high)^n + n * p_high * (1.0 - p_high)^(n - 1)
    v_high * (1.0 - prob_leq1) + v_low * prob_leq1
end

# ---------------------------------------------------------------------------
# Bin-averaged log price (replaces midpoint approximation)
# ---------------------------------------------------------------------------

"""
    avg_log_price_bin(a_lo, a_hi, theta, n, n_points) -> Float64

Average of log P(a*) over a uniform grid on [a_lo, a_hi].
Returns 1e6 (penalty) if any price is non-positive.
Eliminates Jensen's-inequality bias from single-midpoint approximation.
"""
function avg_log_price_bin(a_lo::Float64, a_hi::Float64,
                           theta::Vector{Float64}, n::Int, n_points::Int=20)::Float64
    step = (a_hi - a_lo) / (n_points - 1)
    s = 0.0
    @inbounds for i in 0:(n_points - 1)
        a = a_lo + i * step
        p = price(a, theta, n)
        p <= 0.0 && return 1e6
        s += log(p)
    end
    s / n_points
end

# ---------------------------------------------------------------------------
# Model-predicted moments
# ---------------------------------------------------------------------------

"""
    moments_integrated(theta, bins, n, n_points) -> Vector{Float64}

Compute model-predicted log-price differences relative to the young baseline bin.

bins: Vector of (label, lo, hi) tuples for the non-baseline bins.

Returns log P̄(bin_i) − log P̄(young) for each bin.
Returns fill(1e6, ...) if the baseline price is non-positive (penalty region).
"""
function moments_integrated(theta::Vector{Float64},
                            bins::Vector{Tuple{String,Float64,Float64}},
                            n::Int=5,
                            n_points::Int=20)::Vector{Float64}
    log_p_young = avg_log_price_bin(YOUNG_BIN[1], YOUNG_BIN[2], theta, n, n_points)
    log_p_young >= 1e5 && return fill(1e6, length(bins))

    m = Vector{Float64}(undef, length(bins))
    @inbounds for (i, (_, a_lo, a_hi)) in enumerate(bins)
        avg = avg_log_price_bin(a_lo, a_hi, theta, n, n_points)
        m[i] = avg - log_p_young
    end
    m
end

# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

"""
    print_valuations(theta, n)
Print valuation decomposition at each segment midpoint.
"""
function print_valuations(theta::Vector{Float64}, n::Int=5)
    alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar = theta
    p0 = price(SEGMENT_MIDPOINTS["young"], theta, n)
    log_p0 = p0 > 0 ? log(p0) : NaN

    println(@sprintf("%-10s %5s %8s %8s %8s %8s %12s",
                     "Segment", "a*", "v_c", "v_k", "lambda", "Price", "log P-log P0"))
    println("-" ^ 65)
    for seg in vcat(["young"], SEGMENT_ORDER)
        a    = SEGMENT_MIDPOINTS[seg]
        vc   = vc_fn(a, alpha_c, gamma)
        vk   = vk_fn(a, v_bar_k, alpha_k)
        la   = lam_fn(a, lam_bar, delta)
        pval = price(a, theta, n)
        ld   = (pval > 0 && p0 > 0) ? log(pval) - log_p0 : NaN
        println(@sprintf("%-10s %5.2f %8.4f %8.4f %8.4f %8.4f %12.4f",
                         seg, a, vc, vk, la, pval, ld))
    end
end

"""
Model Solver for the Two-Type Vickrey Auction Model
====================================================

Closed-form equilibrium price and model-predicted moments for the
consumption-collector wine auction model.

Reference: quality_reports/theory_model_2026-03-29.md
"""

from pathlib import Path
import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Segment definitions (normalised age a*)
# ---------------------------------------------------------------------------
SEGMENT_MIDPOINTS = {
    "young": 0.30,
    "approach": 0.80,
    "peak": 1.30,
    "trough": 1.80,
    "antique": 2.50,
}

SEGMENT_ORDER = ["approach", "peak", "trough", "antique"]


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

def h(a_star: float, gamma: float) -> float:
    """Consumption quality function.

    h(a*) = (a*)^gamma * exp(gamma * (1 - a*))

    Properties: h(0)=0, h(1)=1, increasing on [0,1], decreasing on (1,inf).
    """
    if a_star <= 0.0:
        return 0.0
    return (a_star ** gamma) * np.exp(gamma * (1.0 - a_star))


def v_c(a_star: float, alpha_c: float, gamma: float) -> float:
    """Consumption-type valuation: v_c(a*) = alpha_c * h(a*)."""
    return alpha_c * h(a_star, gamma)


def v_k(a_star: float, v_bar_k: float, alpha_k: float) -> float:
    """Collector-type valuation: v_k(a*) = v_bar_k + alpha_k * a*."""
    return v_bar_k + alpha_k * a_star


def lam(a_star: float, lam_bar: float, delta: float) -> float:
    """Probability that a bidder is consumption type.

    lambda(a*) = lam_bar                           if a* <= 1
    lambda(a*) = lam_bar * exp(-delta*(a* - 1))    if a* > 1
    """
    if a_star <= 1.0:
        return lam_bar
    return lam_bar * np.exp(-delta * (a_star - 1.0))


# ---------------------------------------------------------------------------
# Equilibrium price (expected second-order statistic)
# ---------------------------------------------------------------------------

def price(a_star: float, theta: np.ndarray, n: int = 5) -> float:
    """Equilibrium price: expected second-order statistic of n i.i.d. draws
    from the two-point valuation distribution.

    Parameters
    ----------
    a_star : float
        Normalised age (age / maturity date).
    theta : array-like, shape (6,)
        (alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar)
    n : int
        Number of bidders (>= 2).

    Returns
    -------
    float
        Expected second-highest bid (= equilibrium price).
    """
    alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar = theta

    vc = v_c(a_star, alpha_c, gamma)
    vk = v_k(a_star, v_bar_k, alpha_k)
    la = lam(a_star, lam_bar, delta)

    # Probability weights for the second-order statistic of a two-point
    # distribution with values {v_high, v_low} and probabilities {p_high, p_low}.
    #
    # E[Y_{(n-1:n)}] = v_high * Pr(at least 2 draws are v_high)
    #                 + v_low  * Pr(at most 1 draw is v_high)
    #
    # Pr(at most 1 draw = v_high) = (1-p_high)^n + n * p_high * (1-p_high)^(n-1)

    if vc >= vk:
        # v_high = vc with probability la
        p_high = la
        prob_at_most_1_high = (1.0 - p_high) ** n + n * p_high * (1.0 - p_high) ** (n - 1)
        p_val = vc * (1.0 - prob_at_most_1_high) + vk * prob_at_most_1_high
    else:
        # v_high = vk with probability (1-la)
        p_high = 1.0 - la
        prob_at_most_1_high = (1.0 - p_high) ** n + n * p_high * (1.0 - p_high) ** (n - 1)
        p_val = vk * (1.0 - prob_at_most_1_high) + vc * prob_at_most_1_high

    return p_val


def price_vec(a_star_arr: np.ndarray, theta: np.ndarray, n: int = 5) -> np.ndarray:
    """Vectorised price over an array of normalised ages."""
    return np.array([price(a, theta, n) for a in a_star_arr])


# ---------------------------------------------------------------------------
# Model-predicted moments
# ---------------------------------------------------------------------------

def moments(theta: np.ndarray, n: int = 5) -> np.ndarray:
    """Compute model-predicted log-price differences relative to young baseline.

    Returns
    -------
    np.ndarray, shape (4,)
        [log P(0.80) - log P(0.30),
         log P(1.30) - log P(0.30),
         log P(1.80) - log P(0.30),
         log P(2.50) - log P(0.30)]
    """
    p_young = price(SEGMENT_MIDPOINTS["young"], theta, n)

    if p_young <= 0.0:
        return np.full(4, 1e6)  # penalty for non-positive prices

    log_p_young = np.log(p_young)

    m = np.empty(4)
    for i, seg in enumerate(SEGMENT_ORDER):
        p_seg = price(SEGMENT_MIDPOINTS[seg], theta, n)
        if p_seg <= 0.0:
            m[i] = 1e6  # penalty
        else:
            m[i] = np.log(p_seg) - log_p_young

    return m


# ---------------------------------------------------------------------------
# Integrated moments (Fix: replaces midpoint approximation)
# ---------------------------------------------------------------------------

# Young baseline bin boundaries for normalisation
YOUNG_BIN = (0.0, 0.4)


def _avg_log_price_bin(a_lo: float, a_hi: float, theta: np.ndarray,
                       n: int, n_points: int = 20) -> float:
    """Average log P(a*) over [a_lo, a_hi] using Simpson's rule (n_points points).

    Returns large penalty value if any price is non-positive within the bin
    (prevents optimization from exploring degenerate regions).
    """
    a_grid = np.linspace(a_lo, a_hi, n_points)
    log_p_vals = np.empty(n_points)
    for j, a in enumerate(a_grid):
        p = price(a, theta, n)
        if p <= 0.0:
            return 1e6  # penalty — this parameter region is infeasible
        log_p_vals[j] = np.log(p)
    return float(np.mean(log_p_vals))  # trapezoidal rule on uniform grid


def moments_integrated(theta: np.ndarray,
                       bins: list,
                       n: int = 5,
                       n_points: int = 20) -> np.ndarray:
    """Compute model-predicted moments using bin-averaged log prices.

    Replaces single-midpoint approximation with average log P over each bin,
    eliminating Jensen's inequality bias and approximation error in wide bins.

    Parameters
    ----------
    theta : array-like, shape (6,)
        (alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar)
    bins : list of (label, a_lo, a_hi) or (a_lo, a_hi)
        Non-baseline bins. Each element is (label, lo, hi) or just (lo, hi).
    n : int
        Number of bidders.
    n_points : int
        Grid points per bin for numerical integration (default 20).

    Returns
    -------
    np.ndarray, shape (len(bins),)
        Average log P(a*) in each bin minus average log P in the young baseline.
    """
    # Young baseline: [0.0, 0.4)
    log_p_young = _avg_log_price_bin(YOUNG_BIN[0], YOUNG_BIN[1], theta, n, n_points)
    if log_p_young >= 1e5:
        return np.full(len(bins), 1e6)

    m = np.empty(len(bins))
    for i, b in enumerate(bins):
        # Accept either (label, lo, hi) or (lo, hi)
        if len(b) == 3:
            _, a_lo, a_hi = b
        else:
            a_lo, a_hi = b
        avg = _avg_log_price_bin(a_lo, a_hi, theta, n, n_points)
        m[i] = avg - log_p_young

    return m


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

def print_valuations(theta: np.ndarray, n: int = 5):
    """Print valuation decomposition at each segment midpoint."""
    alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar = theta

    print(f"{'Segment':<10} {'a*':>5} {'v_c':>8} {'v_k':>8} {'lambda':>8} {'Price':>8} {'log P-log P0':>12}")
    print("-" * 65)

    p0 = price(SEGMENT_MIDPOINTS["young"], theta, n)
    log_p0 = np.log(p0) if p0 > 0 else np.nan

    for seg_name in ["young"] + SEGMENT_ORDER:
        a = SEGMENT_MIDPOINTS[seg_name]
        vc_val = v_c(a, alpha_c, gamma)
        vk_val = v_k(a, v_bar_k, alpha_k)
        la_val = lam(a, lam_bar, delta)
        p_val = price(a, theta, n)
        log_diff = np.log(p_val) - log_p0 if p_val > 0 and p0 > 0 else np.nan
        print(f"{seg_name:<10} {a:5.2f} {vc_val:8.4f} {vk_val:8.4f} {la_val:8.4f} {p_val:8.4f} {log_diff:12.4f}")


if __name__ == "__main__":
    # Quick sanity check with plausible parameters
    # theta = (alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar)
    theta_test = np.array([2.0, 0.5, 0.3, 3.0, 1.5, 0.5])

    print("=== Model Solver Sanity Check ===\n")
    print(f"Parameters: alpha_c={theta_test[0]}, v_bar_k={theta_test[1]}, "
          f"alpha_k={theta_test[2]}, gamma={theta_test[3]}, "
          f"delta={theta_test[4]}, lam_bar={theta_test[5]}")
    print(f"n = 5\n")

    print_valuations(theta_test, n=5)

    print(f"\nModel moments: {moments(theta_test, n=5)}")

"""
Minimum Distance Estimation of the Two-Type Vickrey Auction Model
=================================================================

Improvements over v1:
  - 7 moments per group (8 bins, young baseline) from 10_structural_moments.py
  - Full 7x7 HC1 VCV as weighting matrix (optimal MD, not diagonal approximation)
  - moments_integrated() via bin-averaged log prices (not single midpoint)
  - J-test of overidentification (7 moments, fix_lambda has 5 free params → 2 df)
  - Bootstrap SEs as primary inference (delta-method reported as secondary check)
  - lam_bar proxied as (1 - high_price_share): consumption-buyer fraction

Three specifications:
  A. unrestricted:   6 free params, 7 moments (1 df over-identified)
  B. fix_lambda:     5 free params, 7 moments (2 df over-identified)  ← PREFERRED
  C. fix_lambda_ak:  4 free params, 7 moments (3 df over-identified)

Reference: quality_reports/structural_strategy_2026-03-29.md
"""

from pathlib import Path
import json
import logging
import warnings
import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import chi2
import sys

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_solver import moments_integrated, SEGMENT_ORDER

# ---------------------------------------------------------------------------
# Load empirical moments from 10_structural_moments.py output
# ---------------------------------------------------------------------------

_MOMENTS_FILE = ROOT / "output" / "structural_moments_fine.json"


def _load_empirical_data() -> dict:
    if not _MOMENTS_FILE.exists():
        raise FileNotFoundError(
            f"Run 10_structural_moments.py first to generate {_MOMENTS_FILE}"
        )
    with open(_MOMENTS_FILE) as f:
        raw = json.load(f)

    data = {}
    for cat, d in raw.items():
        data[cat] = {
            "moments":       np.array(d["moments"]),
            "vcov":          np.array(d["vcov"]),
            "bin_labels":    d["bin_labels"],
            "bin_midpoints": d["bin_midpoints"],
            "N":             d["N"],
            "N_eff":         d["N_eff"],
            "n_moments":     d["n_moments"],
            # Build (label, lo, hi) tuples for moments_integrated()
            "bins": _labels_to_bins(d["bin_labels"]),
        }
    return data


_BIN_EDGES = {
    "young":    (0.0, 0.4),
    "pre1":     (0.4, 0.8),
    "pre2":     (0.8, 1.0),
    "peak1":    (1.0, 1.4),
    "peak2":    (1.4, 1.6),
    "trough":   (1.6, 2.0),
    "antique1": (2.0, 2.5),
    "antique2": (2.5, 3.1),
}


def _labels_to_bins(labels: list) -> list:
    """Convert bin label list to (label, lo, hi) tuples for moments_integrated()."""
    return [(lab, _BIN_EDGES[lab][0], _BIN_EDGES[lab][1]) for lab in labels]


EMPIRICAL_DATA = _load_empirical_data()

# lam_bar proxy: (1 - high_price_share) = consumption-buyer fraction.
# High $200+ share of young lots → collector-dominated market → lower lam_bar.
# Source: Table 1 / Section 5.3.
LAMBDA_PROXIES = {
    "Bordeaux Grand Cru (red)": 1.0 - 0.390,   # 0.610 — majority consumption buyers
    "Burgundy Grand Cru":       1.0 - 0.515,   # 0.485 — near-equal, lean collector
    "Burgundy Premier Cru":     1.0 - 0.112,   # 0.888 — strongly consumption-driven
}

PARAM_NAMES_FULL = ["alpha_c", "v_bar_k", "alpha_k", "gamma", "delta", "lam_bar"]


# ---------------------------------------------------------------------------
# Specification helpers
# ---------------------------------------------------------------------------

def _expand_theta(phi: np.ndarray, spec: str, lam_bar_fixed: float) -> np.ndarray:
    """Map free parameters phi to full theta = (alpha_c, v_bar_k, alpha_k, gamma, delta, lam_bar)."""
    if spec == "unrestricted":
        return phi
    elif spec == "fix_lambda":
        return np.array([phi[0], phi[1], phi[2], phi[3], phi[4], lam_bar_fixed])
    elif spec == "fix_lambda_ak":
        return np.array([phi[0], phi[1], 0.0, phi[2], phi[3], lam_bar_fixed])
    else:
        raise ValueError(f"Unknown spec: {spec}")


def _get_bounds(spec: str):
    if spec == "unrestricted":
        return [(0.01, 30.0), (0.01, 30.0), (0.00, 15.0),
                (0.1,  30.0), (0.01, 30.0), (0.01, 0.99)]
    elif spec == "fix_lambda":
        return [(0.01, 30.0), (0.01, 30.0), (0.00, 15.0),
                (0.1,  30.0), (0.01, 30.0)]
    elif spec == "fix_lambda_ak":
        return [(0.01, 30.0), (0.01, 30.0),
                (0.1,  30.0), (0.01, 30.0)]
    else:
        raise ValueError(f"Unknown spec: {spec}")


def _get_param_names(spec: str):
    if spec == "unrestricted":
        return ["alpha_c", "v_bar_k", "alpha_k", "gamma", "delta", "lam_bar"]
    elif spec == "fix_lambda":
        return ["alpha_c", "v_bar_k", "alpha_k", "gamma", "delta"]
    elif spec == "fix_lambda_ak":
        return ["alpha_c", "v_bar_k", "gamma", "delta"]
    else:
        raise ValueError(f"Unknown spec: {spec}")


# ---------------------------------------------------------------------------
# Objective and Jacobian
# ---------------------------------------------------------------------------

def md_objective(theta: np.ndarray, m_data: np.ndarray, W: np.ndarray,
                 bins: list, n: int = 5) -> float:
    """Minimum distance objective: (m_data - m_model)' W (m_data - m_model).

    Uses bin-averaged log prices (moments_integrated) to eliminate midpoint bias.
    """
    m_model = moments_integrated(theta, bins, n)
    diff = m_data - m_model
    return float(diff @ W @ diff)


def compute_jacobian(theta: np.ndarray, spec: str, lam_bar_fixed: float,
                     bins: list, n: int = 5, eps: float = 1e-6) -> np.ndarray:
    """Numerical Jacobian dm/dphi, shape (n_moments, n_free)."""
    if spec == "unrestricted":
        phi = theta.copy()
    elif spec == "fix_lambda":
        phi = theta[:5].copy()
    elif spec == "fix_lambda_ak":
        phi = np.array([theta[0], theta[1], theta[3], theta[4]])
    else:
        raise ValueError(f"Unknown spec: {spec}")

    n_moments = len(bins)
    n_free = len(phi)
    J = np.empty((n_moments, n_free))

    for j in range(n_free):
        phi_p, phi_m = phi.copy(), phi.copy()
        step = max(eps, abs(phi[j]) * eps)
        phi_p[j] += step
        phi_m[j] -= step
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            m_p = moments_integrated(_expand_theta(phi_p, spec, lam_bar_fixed), bins, n)
            m_m = moments_integrated(_expand_theta(phi_m, spec, lam_bar_fixed), bins, n)
        J[:, j] = (m_p - m_m) / (2.0 * step)

    return J


def delta_method_se(theta: np.ndarray, W: np.ndarray, vcov_data: np.ndarray,
                    spec: str, lam_bar_fixed: float,
                    bins: list, n: int = 5) -> tuple:
    """Delta-method SEs. Returns (se_phi, J_mat, rank, cond, null_space_directions).

    Warning: unreliable when Jacobian condition number > 1e10.
    Bootstrap SEs should be used as primary inference.

    null_space_directions: list of (eigenvalue, eigenvector) for directions with
    eigenvalue < 1e-10 * max_eigenvalue — these parameter combinations are locally
    unidentified. Reported for diagnostics when rank < n_free.
    """
    J_mat = compute_jacobian(theta, spec, lam_bar_fixed, bins, n)
    JWJ = J_mat.T @ W @ J_mat
    eigvals, eigvecs = np.linalg.eigh(JWJ)
    pos = eigvals[eigvals > 0]
    threshold = 1e-10 * max(eigvals.max(), 1e-15)
    rank = int(np.sum(eigvals > threshold))
    cond = eigvals.max() / pos.min() if len(pos) > 0 else np.inf

    # Identify null-space directions (locally unidentified parameter combinations)
    null_idx = eigvals <= threshold
    null_space = [(float(eigvals[i]), eigvecs[:, i].tolist())
                  for i in range(len(eigvals)) if null_idx[i]]

    n_free = J_mat.shape[1]
    try:
        JWJ_inv = np.linalg.pinv(JWJ) if rank < n_free else np.linalg.inv(JWJ)
        V = JWJ_inv @ (J_mat.T @ W @ vcov_data @ W @ J_mat) @ JWJ_inv
        se_phi = np.sqrt(np.maximum(np.diag(V), 0.0))
    except np.linalg.LinAlgError:
        se_phi = np.full(n_free, np.nan)

    return se_phi, J_mat, rank, cond, null_space


# ---------------------------------------------------------------------------
# Estimation
# ---------------------------------------------------------------------------

def estimate_category(category: str, n: int = 5, n_starts: int = 50,
                      seed: int = 42, verbose: bool = True,
                      spec: str = "fix_lambda") -> dict:
    """Estimate parameters for one wine category using hybrid global+local search."""
    data = EMPIRICAL_DATA[category]
    m_data  = data["moments"]
    vcov    = data["vcov"]
    bins    = data["bins"]
    N_eff   = data["N_eff"]
    n_mom   = data["n_moments"]

    # Full optimal weighting matrix: W = Sigma^{-1}
    try:
        W = np.linalg.inv(vcov)
    except np.linalg.LinAlgError:
        W = np.linalg.pinv(vcov)

    lam_bar_fixed = LAMBDA_PROXIES.get(category, 0.5)
    bounds        = _get_bounds(spec)
    free_names    = _get_param_names(spec)
    n_free        = len(free_names)

    def obj_phi(phi):
        theta = _expand_theta(phi, spec, lam_bar_fixed)
        return md_objective(theta, m_data, W, bins, n)

    # Phase 1: Differential evolution (global search)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        de_result = differential_evolution(
            obj_phi, bounds, seed=seed, maxiter=1000, tol=1e-14,
            popsize=25, mutation=(0.5, 1.5), recombination=0.9,
        )
    best_phi = de_result.x.copy()
    best_obj = de_result.fun

    # Phase 2: Polish with L-BFGS-B from DE solution + random starts
    rng = np.random.default_rng(seed)
    starts = [best_phi.copy()]
    for _ in range(n_starts):
        phi0 = np.array([rng.uniform(lo, hi) for lo, hi in bounds])
        starts.append(phi0)

    converged = 0
    for phi0 in starts:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                res = minimize(obj_phi, phi0, method="L-BFGS-B", bounds=bounds,
                               options={"maxiter": 5000, "ftol": 1e-15, "gtol": 1e-12})
            if res.success:
                converged += 1
            if res.fun < best_obj:
                best_obj = res.fun
                best_phi = res.x.copy()
        except Exception as e:
            logger.debug("L-BFGS-B start failed: %s", e)

    best_theta = _expand_theta(best_phi, spec, lam_bar_fixed)

    # Fit statistics
    m_model = moments_integrated(best_theta, bins, n)
    diff    = m_data - m_model

    # J-test: objective ~ chi2(n_moments - n_free) under correct specification.
    # W = vcov^{-1} = (Var[m_hat])^{-1} already incorporates N (it is N * Sigma^{-1}),
    # so diff' W diff = N * diff' Sigma^{-1} diff = J directly.
    # Do NOT multiply by N_eff again — that would double-count the sample size.
    df_jtest = n_mom - n_free
    j_stat   = float(best_obj) if df_jtest > 0 else float("nan")
    p_jtest  = float(chi2.sf(j_stat, df=df_jtest)) if df_jtest > 0 else float("nan")
    avg_sq_t = float(best_obj / n_mom)  # average squared t-stat of moment mismatch

    # Standard errors (delta method — secondary check only)
    se_phi, J, jac_rank, jac_cond, null_space = delta_method_se(
        best_theta, W, vcov, spec, lam_bar_fixed, bins, n
    )

    # Build result
    theta_dict = {name: float(val) for name, val in zip(PARAM_NAMES_FULL, best_theta)}
    se_dict = {}
    se_idx = 0
    for name in PARAM_NAMES_FULL:
        if name in free_names:
            se_dict[name] = float(se_phi[se_idx])
            se_idx += 1
        else:
            se_dict[name] = None

    result = {
        "category":            category,
        "specification":       spec,
        "n_bidders":           n,
        "n_free_params":       n_free,
        "n_moments":           n_mom,
        "df_overid":           df_jtest,
        "theta":               theta_dict,
        "se_delta":            se_dict,   # secondary — unreliable when cond > 1e10
        "objective":           float(best_obj),
        "avg_sq_t_mismatch":   avg_sq_t,
        "j_stat":              j_stat,
        "p_jtest":             p_jtest,
        "moments_data":        {lab: float(m_data[i])  for i, lab in enumerate(data["bin_labels"])},
        "moments_model":       {lab: float(m_model[i]) for i, lab in enumerate(data["bin_labels"])},
        "jacobian_rank":       int(jac_rank),
        "jacobian_cond":       float(jac_cond),
        "se_reliable":         bool(jac_cond < 1e10),
        "null_space":          null_space,   # locally unidentified directions (empty = full rank)
        "converged_starts":    converged,
        "total_starts":        len(starts),
        "N_eff":               float(N_eff),
    }

    if verbose:
        _print_result(result, free_names, data)

    return result


def _print_result(result: dict, free_names: list, data: dict):
    """Pretty-print estimation results."""
    spec = result["specification"]
    cat  = result["category"]
    n    = result["n_bidders"]
    nf   = result["n_free_params"]
    nm   = result["n_moments"]
    df   = result["df_overid"]

    print(f"\n{'=' * 72}")
    print(f"  {cat}  (n={n}, spec={spec})")
    print(f"{'=' * 72}")
    print(f"  Objective: {result['objective']:.4f}   Avg sq-t: {result['avg_sq_t_mismatch']:.4f}")
    print(f"  Overid df={df}  J-stat={result['j_stat']:.2f}  p(J)={result['p_jtest']:.4f}")
    print(f"  Free params: {nf}, Moments: {nm}, df={df}")
    print(f"  Jacobian rank: {result['jacobian_rank']}/{nf}  cond={result['jacobian_cond']:.2e}  "
          f"{'[SEs reliable]' if result['se_reliable'] else '[SEs unreliable — use bootstrap]'}")
    if result.get("null_space"):
        free_names_local = _get_param_names(spec)
        for eigval, evec in result["null_space"]:
            dominant = [(free_names_local[i], abs(v)) for i, v in enumerate(evec)]
            dominant.sort(key=lambda x: -x[1])
            top = ", ".join(f"{n}({v:.2f})" for n, v in dominant[:3])
            print(f"  [Null direction λ={eigval:.2e}]: {top}")
    print(f"  Converged L-BFGS-B: {result['converged_starts']}/{result['total_starts']}")

    vcov = np.array(data["vcov"])
    ses_data = np.sqrt(np.diag(vcov))

    print(f"\n  {'Param':<12} {'Estimate':>10} {'Delta-SE':>10} {'t-stat':>8} {'':>8}")
    print("  " + "-" * 52)
    for name in PARAM_NAMES_FULL:
        est = result["theta"][name]
        se  = result["se_delta"][name]
        if se is None:
            print(f"  {name:<12} {est:10.4f} {'--':>10} {'--':>8} {'[fixed]':>8}")
        else:
            t   = est / se if se > 0 and not np.isnan(se) else float("nan")
            tag = "*" if abs(t) > 1.96 else ""
            if result["se_reliable"]:
                print(f"  {name:<12} {est:10.4f} {se:10.4f} {t:8.2f} {tag:>8}")
            else:
                print(f"  {name:<12} {est:10.4f} {'(n/a)':>10} {'--':>8} {'[boot req]':>8}")

    print(f"\n  {'Bin':<12} {'Data':>9} {'Model':>9} {'Diff':>9} {'Diff/SE':>9}")
    print("  " + "-" * 52)
    for i, lab in enumerate(data["bin_labels"]):
        d_val  = result["moments_data"][lab]
        m_val  = result["moments_model"][lab]
        se_val = float(ses_data[i])
        flag   = " <--" if abs(d_val - m_val) / se_val > 3 else ""
        print(f"  {lab:<12} {d_val:9.4f} {m_val:9.4f} {d_val - m_val:9.4f} "
              f"{(d_val - m_val) / se_val:9.2f}{flag}")

    # rho = v_bar_k / alpha_c — key model quantity
    ac  = result["theta"]["alpha_c"]
    vbk = result["theta"]["v_bar_k"]
    rho = vbk / ac if ac > 0 else float("nan")
    print(f"\n  rho = v_bar_k / alpha_c = {rho:.3f}  "
          f"({'> 1: Prop.2 satisfied — no trough expected' if rho > 1 else '< 1: trough possible'})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    np.random.seed(42)

    all_results = {}

    for spec in ["unrestricted", "fix_lambda", "fix_lambda_ak"]:
        print(f"\n\n{'#' * 75}")
        print(f"#  SPECIFICATION: {spec}")
        print(f"{'#' * 75}")

        spec_results = {}
        for category in EMPIRICAL_DATA:
            spec_results[category] = estimate_category(
                category, n=5, n_starts=50, seed=42, verbose=True, spec=spec
            )
        all_results[spec] = spec_results

    # Save all results
    output_path = ROOT / "output" / "structural_estimates.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Summary for preferred spec
    preferred = "fix_lambda"
    results   = all_results[preferred]

    print(f"\n\n{'=' * 90}")
    print(f"  PREFERRED SPECIFICATION: {preferred}  (5 free params, 7 moments, 2 df overidentified)")
    print(f"{'=' * 90}")

    header = f"  {'Parameter':<12}"
    for cat in EMPIRICAL_DATA:
        short = cat.replace(" (red)", "")[:22]
        header += f"  {short:>25}"
    print(header)
    print("  " + "-" * 88)

    for name in PARAM_NAMES_FULL:
        row = f"  {name:<12}"
        for cat in EMPIRICAL_DATA:
            est = results[cat]["theta"][name]
            se  = results[cat]["se_delta"][name]
            if se is None:
                row += f"  {est:8.3f} [fixed]         "
            elif results[cat]["se_reliable"] and not np.isnan(se):
                row += f"  {est:8.3f} ({se:7.3f})     "
            else:
                row += f"  {est:8.3f} [boot req]      "
        print(row)

    print(f"\n  {'Category':<34} {'Obj':>9} {'Avg sq-t':>9} {'J-stat':>9} {'p(J)':>8} {'df':>4} {'Rank':>6}")
    print("  " + "-" * 82)
    for cat in EMPIRICAL_DATA:
        r = results[cat]
        print(f"  {cat:<34} {r['objective']:9.3f} {r['avg_sq_t_mismatch']:9.4f} "
              f"{r['j_stat']:9.2f} {r['p_jtest']:8.4f} {r['df_overid']:4d} {r['jacobian_rank']:6d}")


if __name__ == "__main__":
    main()

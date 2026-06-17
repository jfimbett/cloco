"""
Robustness Checks for the Two-Type Vickrey Auction Model
=========================================================

Improvements over v1:
  - Bootstrap uses full VCV Cholesky perturbation (not independent se*z)
  - Profile CI: for each free parameter, grid of 50 values, concentrated objective
  - n-sensitivity uses fix_lambda spec to match primary estimation

Checks:
  1. Sensitivity to number of bidders n = {3, 5, 10}
  2. Parametric bootstrap SEs with correlated moment perturbation (B=200)
  3. Profile confidence sets (grid over each free parameter)

Reference: quality_reports/structural_strategy_2026-03-29.md
"""

from pathlib import Path
import json
import logging
import warnings
import numpy as np
from scipy.optimize import minimize, differential_evolution
import sys

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_solver import moments_integrated
from smm_estimation import (
    EMPIRICAL_DATA, PARAM_NAMES_FULL, LAMBDA_PROXIES,
    md_objective, delta_method_se, estimate_category,
    _expand_theta, _get_bounds, _get_param_names,
)


# ---------------------------------------------------------------------------
# 1. Sensitivity to n
# ---------------------------------------------------------------------------

def sensitivity_n(categories: list, spec: str = "fix_lambda",
                  n_values: list = None, n_starts: int = 30,
                  seed: int = 42) -> dict:
    """Re-estimate for each category × n combination."""
    if n_values is None:
        n_values = [3, 5, 10]

    results = {}
    for cat in categories:
        results[cat] = {}
        for n in n_values:
            print(f"\n--- {cat}, n={n} ---")
            res = estimate_category(cat, n=n, n_starts=n_starts,
                                    seed=seed, verbose=False, spec=spec)
            results[cat][str(n)] = res
            rho = res["theta"]["v_bar_k"] / res["theta"]["alpha_c"]
            print(f"  Obj={res['objective']:.3f}  J={res['j_stat']:.2f}  p(J)={res['p_jtest']:.4f}  "
                  f"rho={rho:.3f}")
    return results


# ---------------------------------------------------------------------------
# 2. Parametric bootstrap with full VCV Cholesky perturbation
# ---------------------------------------------------------------------------

def parametric_bootstrap(category: str, spec: str = "fix_lambda",
                         B: int = 200, n: int = 5, n_starts: int = 15,
                         seed: int = 42, verbose: bool = True) -> dict:
    """Parametric bootstrap: perturb data moments using full VCV Cholesky.

    Correctly accounts for correlation between hedonic regression coefficients:
        m_boot = m_data + L @ z,  z ~ N(0, I),  vcov = L @ L'
    """
    data   = EMPIRICAL_DATA[category]
    m_data = data["moments"]
    vcov   = data["vcov"]
    bins   = data["bins"]
    n_mom  = data["n_moments"]

    try:
        W = np.linalg.inv(vcov)
    except np.linalg.LinAlgError:
        W = np.linalg.pinv(vcov)

    # Cholesky decomposition for correlated perturbation
    try:
        L = np.linalg.cholesky(vcov)
    except np.linalg.LinAlgError:
        # vcov not positive definite — regularise
        vcov_reg = vcov + 1e-10 * np.eye(n_mom)
        L = np.linalg.cholesky(vcov_reg)

    lam_bar_fixed = LAMBDA_PROXIES.get(category, 0.5)
    bounds        = _get_bounds(spec)
    free_names    = _get_param_names(spec)

    rng = np.random.default_rng(seed)

    # Baseline estimate for warm-starting
    baseline = estimate_category(category, n=n, n_starts=30, seed=seed,
                                 verbose=False, spec=spec)
    phi_base = np.array([baseline["theta"][name] for name in free_names])

    bootstrap_thetas = []
    n_failed = 0

    for b in range(B):
        # Correlated moment perturbation — respects HC1 covariance structure
        z      = rng.standard_normal(n_mom)
        m_boot = m_data + L @ z

        def obj_boot(phi):
            theta   = _expand_theta(phi, spec, lam_bar_fixed)
            m_model = moments_integrated(theta, bins, n)
            diff    = m_boot - m_model
            return float(diff @ W @ diff)

        best_obj_b = np.inf
        best_phi_b = None

        starts_b = [phi_base.copy()]
        for _ in range(n_starts - 1):
            starts_b.append(np.array([rng.uniform(lo, hi) for lo, hi in bounds]))

        for phi0 in starts_b:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    res = minimize(obj_boot, phi0, method="L-BFGS-B", bounds=bounds,
                                   options={"maxiter": 3000, "ftol": 1e-14, "gtol": 1e-10})
                if res.fun < best_obj_b:
                    best_obj_b = res.fun
                    best_phi_b = res.x.copy()
            except Exception as e:
                logger.debug("Bootstrap L-BFGS-B failed: %s", e)

        if best_phi_b is not None:
            full_theta = _expand_theta(best_phi_b, spec, lam_bar_fixed)
            bootstrap_thetas.append(full_theta)
        else:
            n_failed += 1

        if verbose and (b + 1) % 50 == 0:
            print(f"  Bootstrap {b + 1}/{B} done ({n_failed} failed)")

    if len(bootstrap_thetas) == 0:
        raise RuntimeError(f"All bootstrap draws failed for {category}")

    bootstrap_thetas = np.array(bootstrap_thetas)

    boot_mean  = np.mean(bootstrap_thetas, axis=0)
    boot_se    = np.std(bootstrap_thetas, axis=0, ddof=1)
    boot_q025  = np.percentile(bootstrap_thetas, 2.5, axis=0)
    boot_q975  = np.percentile(bootstrap_thetas, 97.5, axis=0)

    result = {
        "category":         category,
        "specification":    spec,
        "n_bidders":        n,
        "B_requested":      B,
        "B_effective":      len(bootstrap_thetas),
        "n_failed":         n_failed,
        "baseline_theta":   baseline["theta"],
        "bootstrap_mean":   {name: float(boot_mean[i]) for i, name in enumerate(PARAM_NAMES_FULL)},
        "bootstrap_se":     {name: float(boot_se[i])   for i, name in enumerate(PARAM_NAMES_FULL)},
        "bootstrap_ci_025": {name: float(boot_q025[i]) for i, name in enumerate(PARAM_NAMES_FULL)},
        "bootstrap_ci_975": {name: float(boot_q975[i]) for i, name in enumerate(PARAM_NAMES_FULL)},
    }

    if verbose:
        print(f"\n  {'Param':<12} {'Baseline':>10} {'Boot Mean':>10} "
              f"{'Boot SE':>10} {'CI 2.5%':>10} {'CI 97.5%':>10}")
        print("  " + "-" * 64)
        for name in PARAM_NAMES_FULL:
            bl = baseline["theta"][name]
            print(f"  {name:<12} {bl:10.4f} "
                  f"{result['bootstrap_mean'][name]:10.4f} "
                  f"{result['bootstrap_se'][name]:10.4f} "
                  f"{result['bootstrap_ci_025'][name]:10.4f} "
                  f"{result['bootstrap_ci_975'][name]:10.4f}")

    return result


# ---------------------------------------------------------------------------
# 3. Profile confidence sets
# ---------------------------------------------------------------------------

def profile_ci(category: str, spec: str = "fix_lambda",
               n: int = 5, n_grid: int = 50, seed: int = 42) -> dict:
    """For each free parameter, compute profile of MD objective.

    At each grid point, fix that parameter and minimise over remaining free params.
    Profile minimum identifies well-defined minimum vs. flat identification surface.
    """
    data          = EMPIRICAL_DATA[category]
    m_data        = data["moments"]
    vcov          = data["vcov"]
    bins          = data["bins"]
    lam_bar_fixed = LAMBDA_PROXIES.get(category, 0.5)
    bounds        = _get_bounds(spec)
    free_names    = _get_param_names(spec)
    n_free        = len(free_names)

    try:
        W = np.linalg.inv(vcov)
    except np.linalg.LinAlgError:
        W = np.linalg.pinv(vcov)

    # Baseline estimate
    baseline = estimate_category(category, n=n, n_starts=30, seed=seed,
                                 verbose=False, spec=spec)
    phi_opt  = np.array([baseline["theta"][name] for name in free_names])
    obj_opt  = baseline["objective"]

    rng = np.random.default_rng(seed)
    profiles = {}

    for j, param_name in enumerate(free_names):
        lo, hi   = bounds[j]
        grid     = np.linspace(lo, hi, n_grid)
        obj_grid = np.empty(n_grid)

        for k, val in enumerate(grid):
            # Fix parameter j at val, optimise over remaining params
            other_bounds = [b for i, b in enumerate(bounds) if i != j]
            phi_init     = np.delete(phi_opt.copy(), j)

            def obj_profiled(phi_other):
                phi_full = np.insert(phi_other, j, val)
                theta    = _expand_theta(phi_full, spec, lam_bar_fixed)
                return md_objective(theta, m_data, W, bins, n)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                res = minimize(obj_profiled, phi_init, method="L-BFGS-B",
                               bounds=other_bounds,
                               options={"maxiter": 2000, "ftol": 1e-13, "gtol": 1e-10})
            obj_grid[k] = res.fun

        profiles[param_name] = {
            "grid":      grid.tolist(),
            "objective": obj_grid.tolist(),
            "opt_value": float(phi_opt[j]),
            "opt_obj":   float(obj_opt),
            # 95% profile CI: region where obj < opt + chi2(0.95,1)/N_eff
            # (informal approximation)
        }

        flat_frac = float(np.mean(obj_grid < obj_opt * 2))
        print(f"  {param_name:<12}: opt={phi_opt[j]:.3f}  "
              f"min_profile={obj_grid.min():.4f}  flat_frac(<2*opt)={flat_frac:.2f}")

    return {
        "category":      category,
        "specification": spec,
        "baseline_obj":  float(obj_opt),
        "profiles":      profiles,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    np.random.seed(42)
    categories = list(EMPIRICAL_DATA.keys())
    # Use fix_lambda as primary spec (matches smm_estimation.py preferred spec)
    spec = "fix_lambda"

    all_results = {"specification": spec}

    # 1. Sensitivity to n
    print("=" * 75)
    print(f"  ROBUSTNESS CHECK 1: Sensitivity to n (spec={spec})")
    print("=" * 75)
    sensitivity = sensitivity_n(categories, spec=spec, n_values=[3, 5, 10],
                                n_starts=30, seed=42)
    all_results["sensitivity_n"] = sensitivity

    # Structured comparison table
    for cat in categories:
        print(f"\n{'=' * 70}")
        print(f"  {cat}")
        print(f"{'=' * 70}")
        header = f"  {'Parameter':<12}"
        for n_val in [3, 5, 10]:
            header += f"    n={n_val}    "
        print(header)
        print("  " + "-" * 54)
        for name in PARAM_NAMES_FULL:
            row = f"  {name:<12}"
            for n_val in [3, 5, 10]:
                est = sensitivity[cat][str(n_val)]["theta"][name]
                row += f"  {est:8.4f}  "
            print(row)
        row_obj = f"  {'Obj':<12}"
        row_rho = f"  {'rho':<12}"
        for n_val in [3, 5, 10]:
            r   = sensitivity[cat][str(n_val)]
            obj = r["objective"]
            rho = r["theta"]["v_bar_k"] / r["theta"]["alpha_c"]
            row_obj += f"  {obj:8.2f}  "
            row_rho += f"  {rho:8.4f}  "
        print(row_obj)
        print(row_rho)

    # 2. Parametric bootstrap
    print("\n" + "=" * 75)
    print(f"  ROBUSTNESS CHECK 2: Parametric Bootstrap (B=200, spec={spec})")
    print("=" * 75)
    bootstrap_results = {}
    for cat in categories:
        print(f"\n--- {cat} ---")
        bootstrap_results[cat] = parametric_bootstrap(
            cat, spec=spec, B=200, n=5, n_starts=15, seed=42, verbose=True
        )
    all_results["bootstrap"] = bootstrap_results

    # 3. Profile CIs
    print("\n" + "=" * 75)
    print(f"  ROBUSTNESS CHECK 3: Profile Confidence Sets (spec={spec})")
    print("=" * 75)
    profile_results = {}
    for cat in categories:
        print(f"\n--- {cat} ---")
        profile_results[cat] = profile_ci(
            cat, spec=spec, n=5, n_grid=50, seed=42
        )
    all_results["profiles"] = profile_results

    # Save
    output_path = ROOT / "output" / "structural_robustness.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    profiles_path = ROOT / "output" / "structural_profiles.json"
    with open(profiles_path, "w") as f:
        json.dump(profile_results, f, indent=2, default=str)

    print(f"\nRobustness results saved to {output_path}")
    print(f"Profile CIs saved to {profiles_path}")


if __name__ == "__main__":
    main()

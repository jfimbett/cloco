"""
Analytic SE for kappa via delta method from spread OLS regression.
Replicates 08_smm_estimation.py exactly, then adds HC3 SE.

kappa = 2 * E_nu_shifted * |beta_frac|
SE(kappa) = 2 * E_nu_shifted * SE(beta_frac) = 2 * E_nu_shifted * SE(beta_bps) / 10000
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.linalg import lstsq as sp_lstsq
from scipy import stats
import json
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS   = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ================================================================== #
# 1. Load leverage panel (no spread_bps yet — same as script 08)
# ================================================================== #
print("Loading leverage panel...")
lev = pd.read_parquet(PROC / "leverage_panel.parquet")
lev["datadate"] = pd.to_datetime(lev["datadate"])
print(f"  {len(lev):,} obs, {lev.gvkey.nunique():,} firms")

Q_mat    = lev[QUANTILE_COLS].values.astype(np.float64)
Q_nu_raw = np.nanmean(Q_mat, axis=0)
E_nu_raw = Q_nu_raw.mean()

shift    = max(0.0, -Q_nu_raw.min() + 1e-6)
Q_nu_s   = Q_nu_raw + shift
z_ppf    = stats.norm.ppf(QUANTILE_LEVELS)
logQ     = np.log(Q_nu_s)
A        = np.column_stack([np.ones(10), z_ppf])
coef, *_ = sp_lstsq(A, logQ, check_finite=False)
alpha_nu = float(coef[0])
sigma_nu = float(max(coef[1], 0.05))
E_nu_shifted = np.exp(alpha_nu + sigma_nu**2 / 2)

print(f"  alpha_nu = {alpha_nu:.4f}, sigma_nu = {sigma_nu:.4f}")
print(f"  E_nu_raw = {E_nu_raw:.4f},  E_nu_shifted = {E_nu_shifted:.4f}")

# Compute W1_shape (identical to script 08 step 3)
E_nu_dem   = Q_nu_raw - E_nu_raw
cf_mean_q  = Q_mat.mean(axis=1)
q_dem      = Q_mat - cf_mean_q[:, None]
lev["W1_shape"]  = np.mean(np.abs(q_dem - E_nu_dem[None, :]), axis=1)
lev["cf_mean_q"] = cf_mean_q
print(f"  W1_shape: mean={lev['W1_shape'].mean():.4f}, p50={lev['W1_shape'].median():.4f}")

# ================================================================== #
# 2. Merge TRACE spreads and build spread sample (identical to script 08)
# ================================================================== #
print("\nLoading TRACE spreads...")
spr = pd.read_parquet(PROC / "trace_spreads.parquet")
spr["datadate"] = pd.to_datetime(spr["datadate"])

panel_full = lev.merge(spr[["gvkey","datadate","spread_bps"]],
                       on=["gvkey","datadate"], how="left")

samp_spr = panel_full.dropna(subset=["spread_bps"]).copy()
samp_spr = samp_spr[samp_spr["datadate"] >= "2012-01-01"]
samp_spr = samp_spr[
    np.isfinite(samp_spr["spread_bps"]) &
    np.isfinite(samp_spr["W1_shape"]) &
    np.isfinite(samp_spr["cf_mean_q"]) &
    np.isfinite(samp_spr["cf_vol"]) &
    np.isfinite(samp_spr["log_assets"])
].copy()
print(f"  Spread sample: {len(samp_spr):,} obs, {samp_spr.gvkey.nunique():,} firms")

# ================================================================== #
# 3. OLS spread regression (identical to script 08)
# ================================================================== #
X_k = np.column_stack([np.ones(len(samp_spr)),
                       samp_spr["W1_shape"].values,
                       samp_spr["cf_mean_q"].values,
                       samp_spr["cf_vol"].values,
                       samp_spr["log_assets"].values])
y_k = samp_spr["spread_bps"].values

coef_k, *_ = sp_lstsq(X_k, y_k, check_finite=False)
beta_bps   = float(coef_k[1])
y_hat      = X_k @ coef_k
resid      = y_k - y_hat
n, k       = X_k.shape
r2_spr     = float(1 - np.sum(resid**2) / np.sum((y_k - y_k.mean())**2))

kappa_pt   = max(2 * E_nu_shifted * abs(beta_bps / 10000.0), 0.001)
print(f"  beta(spread_bps ~ W1_shape) = {beta_bps:.2f}   R2={r2_spr:.4f}")
print(f"  kappa (should = 0.4511): {kappa_pt:.4f}")

# HC3 SE (all numpy)
X_np    = np.asarray(X_k, dtype=np.float64)
resid_np = np.asarray(resid, dtype=np.float64)
XtX_inv = np.linalg.pinv(X_np.T @ X_np)
hat     = np.sum(X_np @ XtX_inv * X_np, axis=1)   # leverage (hat diag)
e_adj   = resid_np / (1.0 - hat)                   # HC3 adjusted residuals
meat    = X_np * (e_adj**2)[:, None]               # n×k: X_i * e_adj_i^2
B       = X_np.T @ meat                            # k×k sandwich filling
cov_hc3 = XtX_inv @ B @ XtX_inv
se_bps  = float(np.sqrt(cov_hc3[1, 1]))

se_kappa = 2 * E_nu_shifted * (se_bps / 10000.0)

print(f"\n--- HC3 SE ---")
print(f"  SE(beta_bps) = {se_bps:.2f}")
print(f"  SE(kappa)    = {se_kappa:.4f}")
print(f"  t(kappa)     = {kappa_pt / se_kappa:.2f}")
print(f"  95% CI       = ({kappa_pt - 1.96*se_kappa:.4f}, {kappa_pt + 1.96*se_kappa:.4f})")

result = {
    "kappa_point":  float(kappa_pt),
    "kappa_se":     float(se_kappa),
    "beta_bps":     float(beta_bps),
    "se_bps":       float(se_bps),
    "r2_spread":    float(r2_spr),
    "E_nu_shifted": float(E_nu_shifted),
    "n_spread":     int(n),
    "method":       "HC3 delta method",
}
with open(ROOT / "output" / "kappa_analytic_se.json", "w") as f:
    json.dump(result, f, indent=2)
print(f"\nSaved to output/kappa_analytic_se.json")

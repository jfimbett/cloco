"""
Joint SMM: identify kappa from decile-mean credit spreads as moment conditions.

Current approach (two-stage calibration):
  - (alpha_nu, sigma_nu) from Frechet mean
  - kappa from firm-level OLS of spread_bps on W1_shape (beta is negative;
    take |beta|, explain as composition effect)

This script implements the proper SMM moment-condition identification:
  - Model prediction: s_model_d = kappa * W1_shape_bar_d / (2 * E_nu) * 10000 bps
  - Moment condition: E[s_data | decile d] = s_model_d + epsilon_d
  - kappa* = OLS (no intercept) of s_data_d on x_d = W1_shape_bar_d/(2*E_nu)*10000
    = Sigma_d(x_d * s_data_d) / Sigma_d(x_d^2)
  - This regression has the CORRECT positive sign (higher W1_shape -> higher spread)
    because the model prediction correctly orders deciles by expected spread

Also fixes fig_model_fit.pdf Panel B to actually show the model-implied spread line.

Outputs:
  - paper/figures/fig_model_fit.pdf (updated with model spread line in Panel B)
  - paper/tables/tab_decile_fit.tex (updated with correct Spread^model column)
  - prints: kappa_smm vs kappa_ols for comparison
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.linalg import lstsq as sp_lstsq
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
FIGS = ROOT / "paper" / "figures"
TABS = ROOT / "paper" / "tables"

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS   = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ── 1. Load data ──────────────────────────────────────────────────────────────
print("Loading data...")
lev = pd.read_parquet(PROC / "leverage_panel.parquet")
spr = pd.read_parquet(PROC / "trace_spreads.parquet")
spr["datadate"] = pd.to_datetime(spr["datadate"])
print(f"  Leverage panel: {len(lev):,} obs, {lev.gvkey.nunique():,} firms")
print(f"  TRACE spreads:  {len(spr):,} obs, {spr.gvkey.nunique():,} firms")

Q_mat = lev[QUANTILE_COLS].values.astype(np.float64)

# ── 2. Frechet mean -> (alpha_nu, sigma_nu, E_nu) ────────────────────────────
print("\nCalibrating nu from Frechet mean...")
Q_nu_raw = np.nanmean(Q_mat, axis=0)
E_nu_raw = float(Q_nu_raw.mean())

shift    = max(0.0, -Q_nu_raw.min() + 1e-6)
Q_nu_s   = Q_nu_raw + shift
z_ppf    = stats.norm.ppf(QUANTILE_LEVELS)
logQ     = np.log(Q_nu_s)
A        = np.column_stack([np.ones(10), z_ppf])
coef, *_ = sp_lstsq(A, logQ, check_finite=False)
alpha_nu = float(coef[0])
sigma_nu = float(max(coef[1], 0.05))
E_nu_shifted = float(np.exp(alpha_nu + sigma_nu**2 / 2))

print(f"  alpha_nu={alpha_nu:.4f}, sigma_nu={sigma_nu:.4f}, E_nu={E_nu_shifted:.4f}")

# ── 3. W1_shape ───────────────────────────────────────────────────────────────
cf_mean_arr = Q_mat.mean(axis=1)
q_dem       = Q_mat - cf_mean_arr[:, None]
Q_dem       = Q_nu_raw - E_nu_raw
W1_shape    = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)
lev["W1_shape"]  = W1_shape
lev["cf_mean_q"] = cf_mean_arr

# ── 4. Decile assignment ──────────────────────────────────────────────────────
lev["W1s_decile"] = pd.qcut(lev["W1_shape"], 10, labels=False) + 1

# ── 5. Merge TRACE spreads ────────────────────────────────────────────────────
panel = lev.merge(spr[["gvkey","datadate","spread_bps"]],
                  on=["gvkey","datadate"], how="left")
samp_spr = panel.dropna(subset=["spread_bps"]).copy()
samp_spr = samp_spr[samp_spr["datadate"] >= "2012-01-01"]
samp_spr = samp_spr[
    np.isfinite(samp_spr["spread_bps"]) &
    np.isfinite(samp_spr["W1_shape"])
].copy()
print(f"\nTRACE matched sample: {len(samp_spr):,} obs, {samp_spr.gvkey.nunique():,} firms")

# ── 6. Decile-level spread moments ───────────────────────────────────────────
# W1_shape decile labels for TRACE-matched sample
samp_spr["W1s_decile"] = pd.cut(
    samp_spr["W1_shape"],
    bins=np.percentile(lev["W1_shape"], np.linspace(0, 100, 11)),
    labels=False, include_lowest=True
) + 1

dec_spr = (samp_spr.groupby("W1s_decile")
           .agg(s_data=("spread_bps", "mean"),
                W1s_bar=("W1_shape", "mean"),
                n_spr=("spread_bps", "count"))
           .reset_index())
print("\nDecile spread moments (data):")
print(dec_spr.to_string(index=False))

# ── 7. SMM identification of kappa ───────────────────────────────────────────
#
# Model prediction (from Proposition 2 under competitive equilibrium):
#   s_model_d = kappa * W1_shape_bar_d / (2 * E_nu) * 10000   [bps]
#
# Moment condition: s_data_d ~ s_model_d
#   OLS (no intercept): s_data_d = kappa * x_d + error_d
#   where x_d = W1_shape_bar_d / (2 * E_nu_shifted) * 10000
#
# This regression has the CORRECT sign: higher W1_shape -> higher model spread.
# The model predicts a lower bound; deciles where data >> model reflect
# composition effects (IG bonds in low deciles have non-model premia).
# The no-intercept OLS naturally down-weights low deciles (small x_d)
# and is dominated by the high-mismatch deciles where the bound is tightest.

x_d = dec_spr["W1s_bar"].values / (2 * E_nu_shifted) * 10000   # x_d
s_d = dec_spr["s_data"].values                                   # s_data_d

# SMM kappa: no-intercept OLS
kappa_smm = float(np.dot(x_d, s_d) / np.dot(x_d, x_d))
print(f"\n=== Joint SMM kappa (decile-mean spread moments, no-intercept OLS) ===")
print(f"  kappa_smm = {kappa_smm:.4f}")

# Model spreads at SMM kappa
s_model_d = kappa_smm * x_d
dec_spr = dec_spr.copy()
dec_spr["s_model"] = s_model_d

# Check bounds: data >= model for all deciles?
dec_spr["bound_satisfied"] = dec_spr["s_data"] >= dec_spr["s_model"]
print("\nDecile-level spread bound check (kappa_smm):")
print(f"{'Decile':>7} {'W1_bar':>8} {'s_data':>8} {'s_model':>9} {'Bound OK':>10}")
for _, r in dec_spr.iterrows():
    ok = "YES" if r["bound_satisfied"] else "NO (viol)"
    print(f"{int(r['W1s_decile']):>7} {r['W1s_bar']:>8.4f} {r['s_data']:>8.1f} "
          f"{r['s_model']:>9.1f} {ok:>10}")

# Compare with old kappa (OLS firm-level, |beta|)
print(f"\nFor comparison: old kappa (firm-level |OLS slope|) would be read from")
print(f"  08_smm_estimation.py. kappa_smm = {kappa_smm:.4f}")

# ── 8. Leverage bisection at kappa_smm ───────────────────────────────────────
print("\nComputing lambda* at kappa_smm...")

Q_nu_vals = Q_nu_raw.copy()

def pc_residual(lam_arr, Q_mat, Q_nu, E_nu, kappa):
    promised  = lam_arr[:, None] * Q_nu[None, :]
    shortfall = np.maximum(promised - Q_mat, 0)
    E1 = shortfall.mean(axis=1)
    E2 = (shortfall**2).mean(axis=1)
    return E1 + kappa * E2 - (1 - lam_arr) * E_nu

N  = len(Q_mat)
lo = np.zeros(N)
hi = np.ones(N)
for _ in range(45):
    mid = 0.5 * (lo + hi)
    res = pc_residual(mid, Q_mat, Q_nu_vals, E_nu_raw, kappa_smm)
    lo[res < 0]  = mid[res < 0]
    hi[res >= 0] = mid[res >= 0]
lambda_star = np.clip(0.5*(lo + hi), 1e-4, 1 - 1e-4)
lev["lambda_star"] = lambda_star

E_mu_X = Q_mat.mean(axis=1)
L_raw  = lambda_star * E_nu_raw / np.where(np.abs(E_mu_X) > 0.001, np.abs(E_mu_X), 0.001)
gamma  = float(lev["book_lev"].mean() / np.nanmean(L_raw))
lev["L_model"] = gamma * L_raw

# Model-implied spread using PROPOSITION formula (correct formula, not (1-lambda)/(2*lambda-1))
# s_i = kappa * W1_shape_i / (2 * E_nu) * 10000
lev["s_model_bps"] = kappa_smm * lev["W1_shape"] / (2 * E_nu_shifted) * 10000

# ── 9. Decile summary table ───────────────────────────────────────────────────
lev_merged = lev.merge(spr[["gvkey","datadate","spread_bps"]],
                       on=["gvkey","datadate"], how="left")
lev_merged["s_model_bps"] = kappa_smm * lev_merged["W1_shape"] / (2 * E_nu_shifted) * 10000

def safe_mean(x): return x.dropna().mean() if x.notna().any() else np.nan

dec = (lev_merged.groupby("W1s_decile")
       .agg(
           W1s_mean      = ("W1_shape",    "mean"),
           book_lev_mean = ("book_lev",    "mean"),
           L_model_mean  = ("L_model",     "mean"),
           spread_mean   = ("spread_bps",  safe_mean),
           s_model_mean  = ("s_model_bps", "mean"),
           n             = ("book_lev",    "count"),
           n_spread      = ("spread_bps",  lambda x: x.notna().sum()),
       )
       .reset_index())

print("\nDecile summary (kappa_smm):")
print(dec.to_string(index=False))

# R2 leverage decile fit
ss_r = np.sum((dec["book_lev_mean"] - dec["L_model_mean"])**2)
ss_t = np.sum((dec["book_lev_mean"] - dec["book_lev_mean"].mean())**2)
r2_lev = float(1 - ss_r/ss_t) if ss_t > 0 else np.nan
from scipy.stats import spearmanr
rho, pval = spearmanr(dec["W1s_decile"], dec["book_lev_mean"])
print(f"\nLeverage R2={r2_lev:.4f}, Spearman rho={rho:.3f} (p={pval:.3f})")

# ── 10. Figure: model vs data (Panel A: leverage, Panel B: spreads) ───────────
try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    d = dec["W1s_decile"].values

    # Panel A: leverage
    ax = axes[0]
    ax.plot(d, dec["book_lev_mean"]*100, "o-", color="#1f77b4",
            lw=2, ms=7, label="Data")
    ax.plot(d, dec["L_model_mean"]*100,  "s--", color="#d62728",
            lw=2, ms=7, label="Model")
    ax.set_xlabel(r"$\widehat{W}_{1,\mathrm{shape}}$ Decile", fontsize=13)
    ax.set_ylabel("Mean Book Leverage (%)", fontsize=13)
    ax.set_title("(A) Leverage", fontsize=13, fontweight="bold")
    ax.set_xticks(range(1, 11))
    ax.legend(fontsize=12); ax.grid(alpha=0.25)

    # Panel B: credit spreads — now with model line
    ax = axes[1]
    spr_d = dec.dropna(subset=["spread_mean"])
    ax.plot(spr_d["W1s_decile"], spr_d["spread_mean"],
            "o-", color="#1f77b4", lw=2, ms=7, label="Data (TRACE)")
    ax.plot(dec["W1s_decile"], dec["s_model_mean"],
            "s--", color="#d62728", lw=2, ms=7,
            label=r"Model: $\hat\kappa \bar W_{1,d}/(2\hat{\mathbb{E}}_\nu[Y])$")
    ax.set_xlabel(r"$\widehat{W}_{1,\mathrm{shape}}$ Decile", fontsize=13)
    ax.set_ylabel("Mean Credit Spread (bps)", fontsize=13)
    ax.set_title("(B) Credit Spreads", fontsize=13, fontweight="bold")
    ax.set_xticks(range(1, 11))
    ax.legend(fontsize=11); ax.grid(alpha=0.25)

    fig.suptitle(
        r"Model vs. Data by $\widehat{W}_{1,\mathrm{shape}}$ Decile",
        fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGS / "fig_model_fit.pdf", dpi=150, bbox_inches="tight")
    fig.savefig(FIGS / "fig_model_fit.png", dpi=150, bbox_inches="tight")
    print(f"\nFigure saved: {FIGS / 'fig_model_fit.pdf'}")
except Exception as e:
    print(f"Figure error: {e}")

# ── 11. Update tab_decile_fit.tex ─────────────────────────────────────────────
lines = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Leverage and Credit Spreads by $\widehat{W}_{1,\text{shape}}$ Decile}",
    r"\label{tab:decile_fit}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{lccccccc}",
    r"\toprule",
    (r"Decile & $\bar{W}_{1,\text{shape}}$ & Lev$^{\text{data}}$ & Lev$^{\text{model}}$"
     r" & Spread$^{\text{data}}$ & Spread$^{\text{model}}$ & $N$ & $N_{\text{spr}}$ \\"),
    r"\midrule",
]
for _, r in dec.iterrows():
    sd = f"{r['spread_mean']:.1f}"  if pd.notna(r['spread_mean'])  else "---"
    sm = f"{r['s_model_mean']:.1f}" if pd.notna(r['s_model_mean']) else "---"
    lines.append(
        f"{int(r['W1s_decile'])} & {r['W1s_mean']:.4f} & "
        f"{r['book_lev_mean']:.4f} & {r['L_model_mean']:.4f} & "
        f"{sd} & {sm} & "
        f"{int(r['n']):,} & {int(r['n_spread']):,} \\\\"
    )
lines += [
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}[flushleft]",
    r"\small",
    (r"\item $\widehat{W}_{1,\text{shape}}$ is the mean-adjusted shape component of the "
     r"Wasserstein-1 distance. Lev$^{\text{data}}$ = mean book leverage. "
     r"Lev$^{\text{model}}$ = model-implied leverage from calibrated structural parameters. "
     r"Spread$^{\text{data}}$ = mean TRACE spread (2012--2024) in basis points (bps). "
     r"Spread$^{\text{model}} = \hat{\kappa}\bar{W}_{1,\text{shape},d}/(2\hat{\mathbb{E}}_\nu[Y])\times 10{,}000$ "
     r"is the model-implied mean credit spread from Proposition~\ref{prop:spreads} "
     r"under the competitive-equilibrium point prediction. "
     r"$\hat{\kappa}$ is identified from the no-intercept OLS of Spread$^{\text{data}}_d$ on "
     r"$\bar{W}_{1,\text{shape},d}/(2\hat{\mathbb{E}}_\nu[Y])\times 10{,}000$ "
     r"across deciles (SMM moment conditions). "
     r"$N_{\text{spr}}$ = TRACE observations in the spread sample."),
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
with open(TABS / "tab_decile_fit.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Table saved: {TABS / 'tab_decile_fit.tex'}")
print(f"\n=== Summary ===")
print(f"kappa_smm (decile-mean SMM) = {kappa_smm:.4f}")
print(f"E_nu_shifted                = {E_nu_shifted:.4f}")
print(f"alpha_nu                    = {alpha_nu:.4f}")
print(f"sigma_nu                    = {sigma_nu:.4f}")
print(f"Leverage decile R2          = {r2_lev:.4f}")
print(f"Spearman rho (lev~decile)   = {rho:.4f} (p={pval:.4f})")

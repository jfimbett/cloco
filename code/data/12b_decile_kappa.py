"""
Targeted script: decile-robustness table + kappa bootstrap SE.
Skips the distress horse-race (already completed by script 12).

Fixes:
  - 'datadate' now included in regression DataFrame so merge with pan_dec works
  - Vectorized cluster_se: O(n*k) instead of O(n*G*k) — ~100x faster
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.linalg import lstsq as sp_lstsq
import json
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
RAW  = ROOT / "data" / "raw"
TABS = ROOT / "paper" / "tables"
TABS.mkdir(parents=True, exist_ok=True)
(ROOT / "output").mkdir(parents=True, exist_ok=True)

QUANTILE_COLS = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ================================================================== #
# Helper functions
# ================================================================== #
def ols_within(df, outcome, regressors, group_firm, group_year=None):
    """Two-way within (firm + year FE) via alternating projections."""
    df2 = df.copy()
    cols = regressors + [outcome]
    for c in cols:
        df2[c] = df2[c].astype(np.float64)
        if group_year is not None:
            gm_firm = df2.groupby(group_firm)[c].transform("mean").astype(np.float64)
            gm_year = df2.groupby(group_year)[c].transform("mean").astype(np.float64)
            gm_all  = float(df2[c].mean())
            df2[c + "_w"] = df2[c].values - gm_firm.values - gm_year.values + gm_all
        else:
            gm_firm = df2.groupby(group_firm)[c].transform("mean").astype(np.float64)
            df2[c + "_w"] = df2[c].values - gm_firm.values
    y  = df2[outcome + "_w"].values
    X  = np.column_stack([df2[c + "_w"].values for c in regressors])
    coef, *_ = sp_lstsq(X, y, check_finite=False)
    resid = y - X @ coef
    n, k  = X.shape
    r2    = 1 - np.sum(resid**2) / np.sum((y - y.mean())**2)
    return coef, resid, X, np.asarray(df2[group_firm].values), n, r2

def cluster_se_fast(resid, X, group_arr):
    """Vectorized cluster SE — O(n*k) not O(n*G*k)."""
    if hasattr(group_arr, 'values'):
        group_arr = group_arr.values
    resid = np.asarray(resid, dtype=np.float64)
    X     = np.asarray(X,     dtype=np.float64)
    n, k  = X.shape
    groups, inv = np.unique(group_arr, return_inverse=True)
    G     = len(groups)
    scores = np.zeros((G, k))  # G × k
    np.add.at(scores, inv, X * resid[:, None])
    B     = scores.T @ scores  # k × k
    XtX_inv = np.linalg.pinv(X.T @ X)
    adj   = (G / (G - 1)) * ((n - 1) / (n - k))
    return np.sqrt(np.diag(adj * XtX_inv @ B @ XtX_inv))

def fmt_coef(coef, se, decimal=4):
    t = abs(coef / se)
    stars = "^{***}" if t > 3.29 else "^{**}" if t > 1.96 else "^{*}" if t > 1.645 else ""
    return f"{coef:.{decimal}f}{stars}", f"({se:.{decimal}f})"

def write_table(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Written: {path}")

def run_col(df_sub, regressors):
    mask = df_sub[regressors + ["book_lev"]].notna().all(axis=1)
    df_ok = df_sub[mask].copy()
    coef, resid, X, grp, n, r2 = ols_within(
        df_ok, "book_lev", regressors, "gvkey", "year")
    se = cluster_se_fast(resid, X, grp)
    return coef, se, n, r2, df_ok.gvkey.nunique()

# ================================================================== #
# 1. Load data
# ================================================================== #
print("Loading main panel...")
pan = pd.read_parquet(PROC / "main_panel.parquet")
pan["datadate"] = pd.to_datetime(pan["datadate"])
print(f"  Loaded: {len(pan):,} obs, {pan.gvkey.nunique():,} firms")

CONTROLS_BASE = ["cf_mean", "cf_vol", "log_assets", "mtb", "profitability", "tangibility"]
# Include datadate so the merge with pan_dec works
NEEDED = ["gvkey", "datadate", "year", "book_lev", "W1_shape"] + CONTROLS_BASE
df = pan[NEEDED].dropna(subset=["book_lev", "W1_shape"] + CONTROLS_BASE).copy()

lo_w = df["W1_shape"].quantile(0.01)
hi_w = df["W1_shape"].quantile(0.99)
df["W1_shape"] = df["W1_shape"].clip(lo_w, hi_w)

print(f"Base sample: {len(df):,} obs, {df.gvkey.nunique():,} firms")

REGS_BASE = ["W1_shape"] + CONTROLS_BASE

# ================================================================== #
# 2. Decile-10 robustness
# ================================================================== #
print("\nRunning decile-10 robustness regressions...")

pan_dec = pan[["gvkey", "datadate", "W1s_decile"]].dropna(subset=["W1s_decile"])
df_with_dec = df.merge(pan_dec, on=["gvkey", "datadate"], how="left")

rA = run_col(df,                                             REGS_BASE)
rB = run_col(df_with_dec[df_with_dec["W1s_decile"] < 10],   REGS_BASE)

df_w95 = df.copy()
df_w95["W1_shape"] = df_w95["W1_shape"].clip(upper=df["W1_shape"].quantile(0.95))
rC = run_col(df_w95, REGS_BASE)

df_w90 = df.copy()
df_w90["W1_shape"] = df_w90["W1_shape"].clip(upper=df["W1_shape"].quantile(0.90))
rD = run_col(df_w90, REGS_BASE)

print("  W1_shape coefficient across decile-10 robustness:")
for res, lab in zip([rA, rB, rC, rD],
                    ["Full (baseline)", "Excl. decile 10", "Winsor p95", "Winsor p90"]):
    coef, se, n, r2v, _ = res
    print(f"    {lab}: beta={coef[0]:.4f}, SE={se[0]:.4f}, t={coef[0]/se[0]:.2f}, N={n:,}")

ALL_RESULTS_B = [rA, rB, rC, rD]
COEF_B = [r[0][0] for r in ALL_RESULTS_B]
SE_B   = [r[1][0] for r in ALL_RESULTS_B]
N_B    = [r[2]    for r in ALL_RESULTS_B]
R2_B   = [r[3]    for r in ALL_RESULTS_B]

def fmt(c, s): return fmt_coef(c, s)

lines2 = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Robustness: Sensitivity to $\widehat{W}_{1,\text{shape}}$ Outliers}",
    r"\label{tab:robustness_decile}",
    r"\resizebox{\textwidth}{!}{",
    r"\begin{threeparttable}",
    r"\begin{tabular}{l" + "c"*4 + "}",
    r"\toprule",
    r" & (1) & (2) & (3) & (4) \\",
    r"\cmidrule(lr){2-5}",
    r"Outcome: Book leverage & Baseline & Excl.\ decile 10 & Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p95) & Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p90) \\",
    r"\midrule",
]

for i, (c, s) in enumerate(zip(COEF_B, SE_B)):
    cv, sv = fmt(c, s)
    lines2.append(r"$\widehat{W}_{1,\text{shape}}$" + f" & ${cv}$" * (1 if i == 0 else 0)
                  + (" & ".join([f"${fmt(COEF_B[j], SE_B[j])[0]}$" for j in range(4)])) * (1 if i == 0 else 0)
                  + r" \\")
    lines2.append(r" & " + " & ".join([f"{fmt(COEF_B[j], SE_B[j])[1]}" for j in range(4)]) + r" \\[2pt]")
    break  # only need one row

# Fix the above with clean approach
lines2 = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Robustness: Sensitivity to $\widehat{W}_{1,\text{shape}}$ Outliers}",
    r"\label{tab:robustness_decile}",
    r"\resizebox{\textwidth}{!}{",
    r"\begin{threeparttable}",
    r"\begin{tabular}{l" + "c"*4 + "}",
    r"\toprule",
    r" & (1) & (2) & (3) & (4) \\",
    r"\cmidrule(lr){2-5}",
    r"Outcome: Book leverage & Baseline & Excl.\ decile 10 & Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p95) & Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p90) \\",
    r"\midrule",
]

coef_cells = " & ".join(f"${fmt_coef(c, s)[0]}$" for c, s in zip(COEF_B, SE_B))
se_cells   = " & ".join(f"{fmt_coef(c, s)[1]}" for c, s in zip(COEF_B, SE_B))
lines2.append(r"$\widehat{W}_{1,\text{shape}}$ & " + coef_cells + r" \\")
lines2.append(r" & " + se_cells + r" \\[2pt]")

lines2 += [
    r"\midrule",
    r"Firm FE & Yes & Yes & Yes & Yes \\",
    r"Year FE & Yes & Yes & Yes & Yes \\",
    r"$R^2$ & " + " & ".join(f"{r:.4f}" for r in R2_B) + r" \\",
    r"$N$ & " + " & ".join(f"{n:,}" for n in N_B) + r" \\",
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}[flushleft]",
    r"\small",
    (r"\item Dependent variable: book leverage. All specifications include firm and "
     r"year-quarter fixed effects; standard errors clustered at firm level. "
     r"Column (2) excludes firm-quarters in the top decile of $\widehat{W}_{1,\text{shape}}$. "
     r"Columns (3)--(4) replace $\widehat{W}_{1,\text{shape}}$ with versions winsorized "
     r"at the 95th and 90th percentile, respectively. "
     r"$^{***}$, $^{**}$, $^{*}$ denote significance at 1\%, 5\%, 10\%."),
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"}",
    r"\end{table}",
]
write_table(lines2, TABS / "tab_robustness_decile.tex")

# ================================================================== #
# 3. Bootstrap SE for kappa
# ================================================================== #
print("\nComputing bootstrap SE for kappa (100 firm-level replications)...")

try:
    spreads = pd.read_parquet(PROC / "trace_spreads.parquet")
    spreads["datadate"] = pd.to_datetime(spreads["datadate"])
    spread_pan = pan.merge(spreads[["gvkey","datadate","spread_bps"]],
                           on=["gvkey","datadate"], how="inner",
                           suffixes=("", "_trace"))
    if "spread_bps_trace" in spread_pan.columns:
        spread_pan["spread_use"] = spread_pan["spread_bps_trace"]
    else:
        spread_pan["spread_use"] = spread_pan["spread_bps"]
    spread_pan = spread_pan.dropna(subset=["spread_use", "W1_shape"] + CONTROLS_BASE)
    print(f"  Spread sample: {len(spread_pan):,} obs")
except Exception as e:
    print(f"  Using spread_bps from main panel (fallback): {e}")
    spread_pan = pan.dropna(subset=["spread_bps", "W1_shape"] + CONTROLS_BASE).copy()
    spread_pan["spread_use"] = spread_pan["spread_bps"]

def estimate_kappa_once(df_boot):
    if not set(QUANTILE_COLS).issubset(df_boot.columns):
        return np.nan, np.nan
    Q_mat  = df_boot[QUANTILE_COLS].values.astype(np.float64)
    Q_nu   = np.nanmean(Q_mat, axis=0)
    E_nu   = Q_nu.mean()
    cf_mean_arr = Q_mat.mean(axis=1)
    q_dem  = Q_mat - cf_mean_arr[:, None]
    Q_dem  = Q_nu  - E_nu
    has_spread = spread_pan["gvkey"].isin(df_boot["gvkey"].unique())
    sp_sub = spread_pan[has_spread].copy()
    sp_sub2 = sp_sub.merge(
        df_boot[["gvkey","datadate"] + QUANTILE_COLS],
        on=["gvkey","datadate"], how="inner", suffixes=("","_b"))
    if len(sp_sub2) < 100:
        return np.nan, np.nan
    Q_cols2  = [c for c in sp_sub2.columns if c in QUANTILE_COLS]
    Q_mat2   = sp_sub2[Q_cols2].values.astype(np.float64)
    cf_m2    = Q_mat2.mean(axis=1)
    q_dem2   = Q_mat2 - cf_m2[:, None]
    w1s2     = np.mean(np.abs(q_dem2 - Q_dem[None, :]), axis=1)
    sp_sub2["W1_shape_b"] = w1s2
    sp_sub2 = sp_sub2.dropna(subset=["spread_use", "W1_shape_b"] + CONTROLS_BASE)
    if len(sp_sub2) < 100:
        return np.nan, np.nan
    y_s = sp_sub2["spread_use"].values / 10000.0
    X_s = np.column_stack([np.ones(len(sp_sub2)),
                           sp_sub2["W1_shape_b"].values,
                           sp_sub2["log_assets"].values,
                           sp_sub2["cf_mean"].values,
                           sp_sub2["cf_vol"].values])
    coef_s, *_ = sp_lstsq(X_s, y_s, check_finite=False)
    return 2 * E_nu * coef_s[1], E_nu

np.random.seed(42)
firms_all = pan["gvkey"].unique()
kappas = []
for b in range(100):
    boot_firms = np.random.choice(firms_all, size=len(firms_all), replace=True)
    df_boot    = pan[pan["gvkey"].isin(boot_firms)].copy()
    k, _ = estimate_kappa_once(df_boot)
    kappas.append(k)
    if (b + 1) % 25 == 0:
        valid = [x for x in kappas if not np.isnan(x)]
        print(f"  Bootstrap {b+1}/100: mean={np.mean(valid):.4f}, SE={np.std(valid):.4f}")

kappas_valid  = [k for k in kappas if not np.isnan(k)]
kappa_boot_se = np.std(kappas_valid)
kappa_boot_mean = np.mean(kappas_valid)
print(f"\nBootstrap kappa: mean={kappa_boot_mean:.4f}, SE={kappa_boot_se:.4f}")
print(f"95% CI: ({kappa_boot_mean - 1.96*kappa_boot_se:.4f}, "
      f"{kappa_boot_mean + 1.96*kappa_boot_se:.4f})")
print(f"n_reps used: {len(kappas_valid)}/100")

kappa_result = {
    "kappa_point":     0.4511,
    "kappa_boot_mean": float(kappa_boot_mean),
    "kappa_boot_se":   float(kappa_boot_se),
    "n_reps":          len(kappas_valid),
}
with open(ROOT / "output" / "kappa_bootstrap.json", "w") as f:
    json.dump(kappa_result, f, indent=2)
print(f"Saved to output/kappa_bootstrap.json")
print("\nDone.")

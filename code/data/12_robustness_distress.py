"""
Robustness regressions for Distributional Debt Capacity paper.

This script produces:
1. Tab 3: Distress horse-race — W1_shape vs. financial distress proxies
   (Altman Z-score proxy, net income ratio, profitability, market-to-book)
2. Tab 3B: W1_shape coefficient with decile-10 excluded / W1_shape winsorized
3. Bootstrap SE for kappa from spread regression

Output:
    paper/tables/tab_robustness_distress.tex
    paper/tables/tab_robustness_decile.tex
    (also prints kappa bootstrap SE)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.linalg import lstsq as sp_lstsq
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
RAW  = ROOT / "data" / "raw"
TABS = ROOT / "paper" / "tables"
TABS.mkdir(parents=True, exist_ok=True)

QUANTILE_COLS = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ================================================================== #
# 0. Helper functions
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
    X = np.column_stack([df2[c + "_w"].values.astype(np.float64) for c in regressors])
    y = df2[outcome + "_w"].values.astype(np.float64)
    coef, *_ = sp_lstsq(X, y, check_finite=False)
    resid = y - X @ coef
    n, k  = X.shape
    r2    = 1 - np.sum(resid**2) / np.sum((y - y.mean())**2)
    return coef, resid, X, np.asarray(df2[group_firm].values), n, r2

def cluster_se(resid, X, group_arr):
    if hasattr(group_arr, 'values'):
        group_arr = group_arr.values
    if hasattr(resid, 'values'):
        resid = np.asarray(resid, dtype=np.float64)
    X = np.asarray(X, dtype=np.float64)
    XtX_inv = np.linalg.pinv(X.T @ X)
    groups  = np.unique(group_arr)
    B       = np.zeros((X.shape[1], X.shape[1]))
    for g in groups:
        mask = group_arr == g
        Xg   = X[mask]; eg = np.asarray(resid[mask], dtype=np.float64)
        B   += np.outer(Xg.T @ eg, eg @ Xg)
    G, n, k = len(groups), X.shape[0], X.shape[1]
    adj = (G / (G - 1)) * ((n - 1) / (n - k))
    return np.sqrt(np.diag(adj * XtX_inv @ B @ XtX_inv))

def fmt_coef(coef, se, decimal=4):
    t = abs(coef / se)
    stars = "^{***}" if t > 3.29 else "^{**}" if t > 1.96 else "^{*}" if t > 1.645 else ""
    return f"{coef:.{decimal}f}{stars}", f"({se:.{decimal}f})"

def write_table(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Written: {path}")

# ================================================================== #
# 1. Load main panel
# ================================================================== #
print("Loading main panel...")
pan = pd.read_parquet(PROC / "main_panel.parquet")
pan["datadate"] = pd.to_datetime(pan["datadate"])
print(f"  Loaded: {len(pan):,} obs, {pan.gvkey.nunique():,} firms")

# ================================================================== #
# 2. Merge additional Compustat variables for distress proxies
# ================================================================== #
print("Loading Compustat for distress proxies...")
fund = pd.read_parquet(RAW / "compustat" / "fundq.parquet",
                       columns=["gvkey", "datadate", "ibq", "dpq", "atq",
                                "dlttq", "oibdpq", "ppentq"])
fund["datadate"] = pd.to_datetime(fund["datadate"])
fund = fund.dropna(subset=["ibq", "atq"])
fund = fund[fund["atq"] > 0]

# Net income to assets (quarterly)
fund["ni_ratio"]  = fund["ibq"] / fund["atq"]

# Cash flow coverage: (ibq + dpq) / atq  (Fazzari-Hubbard-Petersen style)
fund["cf_fhp"] = (fund["ibq"].fillna(0) + fund["dpq"].fillna(0)) / fund["atq"]

# Long-term leverage for Whited-Wu: dlttq/atq
fund["tltd"] = fund["dlttq"].fillna(0) / fund["atq"]

# Simplified Whited-Wu index (Whited & Wu 2006, sans dividends and industry sales growth)
# WW = -0.091*CF - 0.044*LNTA + 0.021*TLTD  (partial index, available variables only)
fund["ww_partial"] = (-0.091 * fund["cf_fhp"]
                      - 0.044 * np.log(fund["atq"].clip(lower=0.001))
                      + 0.021 * fund["tltd"])

# Altman Z-score proxy (using available variables, without actq/lctq/req/saleq)
# Use X3 = EBIT/TA, X4 = MktEq/TotalDebt (from main panel's market data)
# Z-proxy = 3.3*X3 where X3 = oibdpq/atq (ebit proxy)
fund["z_ebit_comp"] = 3.3 * (fund["oibdpq"].fillna(0) / fund["atq"])

pan = pan.merge(
    fund[["gvkey", "datadate", "ni_ratio", "cf_fhp", "ww_partial", "z_ebit_comp"]],
    on=["gvkey", "datadate"],
    how="left"
)
print(f"  After merge: {pan.notna().sum()['ww_partial']:,} obs with distress proxies")

# ================================================================== #
# 3. Base sample (same as main regressions)
# ================================================================== #
CONTROLS_BASE = ["cf_mean", "cf_vol", "log_assets", "mtb", "profitability", "tangibility"]
NEEDED = ["gvkey", "year", "book_lev", "W1_shape"] + CONTROLS_BASE
df = pan[NEEDED + ["ni_ratio", "cf_fhp", "ww_partial", "z_ebit_comp"]].dropna(
    subset=["book_lev", "W1_shape"] + CONTROLS_BASE).copy()

# Winsorize W1_shape (same as main regressions)
lo_w = df["W1_shape"].quantile(0.01)
hi_w = df["W1_shape"].quantile(0.99)
df["W1_shape"] = df["W1_shape"].clip(lo_w, hi_w)

# Winsorize distress proxies at 1/99
for c in ["ni_ratio", "cf_fhp", "ww_partial", "z_ebit_comp"]:
    lo_c = df[c].quantile(0.01)
    hi_c = df[c].quantile(0.99)
    df[c] = df[c].clip(lo_c, hi_c)

print(f"Base sample: {len(df):,} obs, {df.gvkey.nunique():,} firms")

# ================================================================== #
# 4. Distress horse-race regressions (Table A: firm+year FE)
# ================================================================== #
# Column 1: baseline (replicate col 5 from main table)
# Column 2: + net income / assets
# Column 3: + net income / assets + WW partial index
# Column 4: + all distress controls jointly
# Column 5: + z_ebit_comp (EBIT-based Z-score component)

def run_col(df_sub, regressors):
    mask = df_sub[regressors + ["book_lev"]].notna().all(axis=1)
    df_ok = df_sub[mask].copy()
    coef, resid, X, grp, n, r2 = ols_within(
        df_ok, "book_lev", regressors, "gvkey", "year")
    se = cluster_se(resid, X, grp)
    return coef, se, n, r2, df_ok.gvkey.nunique()

REGS_BASE     = ["W1_shape"] + CONTROLS_BASE
REGS_PLUS_NI  = REGS_BASE + ["ni_ratio"]
REGS_PLUS_WW  = REGS_BASE + ["ni_ratio", "ww_partial"]
REGS_ALL      = REGS_BASE + ["ni_ratio", "ww_partial", "z_ebit_comp"]

print("\nRunning horse-race regressions...")
r1 = run_col(df, REGS_BASE)
r2 = run_col(df, REGS_PLUS_NI)
r3 = run_col(df, REGS_PLUS_WW)
r4 = run_col(df, REGS_ALL)

print("  Coefficient on W1_shape across distress specifications:")
for i, (res, lab) in enumerate(zip([r1,r2,r3,r4],
    ["Baseline", "+NI/A", "+WW partial", "+All distress"])):
    coef, se, n, r2v, nfirms = res
    print(f"    {lab}: beta={coef[0]:.4f}, SE={se[0]:.4f}, t={coef[0]/se[0]:.2f}, N={n:,}")

# Build LaTeX table
DIST_LABS = {
    "W1_shape":     r"$\widehat{W}_{1,\text{shape}}$",
    "cf_mean":      r"CF mean",
    "cf_vol":       r"CF volatility",
    "log_assets":   r"Log assets",
    "mtb":          r"Market-to-book",
    "profitability": r"Profitability",
    "tangibility":  r"Tangibility",
    "ni_ratio":     r"Net income / assets",
    "ww_partial":   r"WW index (partial)",
    "z_ebit_comp":  r"Z-score component (EBIT)",
}

ALL_VAR_NAMES = (["W1_shape"] + CONTROLS_BASE +
                 ["ni_ratio", "ww_partial", "z_ebit_comp"])
all_results   = [
    (r1, REGS_BASE),
    (r2, REGS_PLUS_NI),
    (r3, REGS_PLUS_WW),
    (r4, REGS_ALL),
]

lines = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Robustness: $\widehat{W}_{1,\text{shape}}$ vs.\ Financial Distress Proxies}",
    r"\label{tab:robustness_distress}",
    r"\begin{threeparttable}",
    r"\resizebox{\textwidth}{!}{",
    r"\begin{tabular}{l" + "c"*4 + "}",
    r"\toprule",
    r" & (1) & (2) & (3) & (4) \\",
    r"\cmidrule(lr){2-5}",
    r"Outcome: Book leverage & Baseline & +NI/A & +WW & +All distress \\",
    r"\midrule",
]

for var in ALL_VAR_NAMES:
    coef_row, se_row = [], []
    for (res, reg_list) in all_results:
        coef, se = res[0], res[1]
        if var in reg_list:
            idx = reg_list.index(var)
            c_s, s_s = fmt_coef(coef[idx], se[idx])
            coef_row.append(f"${c_s}$")
            se_row.append(s_s)
        else:
            coef_row.append("")
            se_row.append("")
    lines.append(DIST_LABS[var] + " & " + " & ".join(coef_row) + r" \\")
    lines.append(" & " + " & ".join(se_row) + r" \\[2pt]")

lines += [
    r"\midrule",
    r"Firm FE & Yes & Yes & Yes & Yes \\",
    r"Year FE & Yes & Yes & Yes & Yes \\",
    r"$R^2$ & " + " & ".join(f"{r[3]:.4f}" for r, _ in all_results) + r" \\",
    r"$N$ & " + " & ".join(f"{r[2]:,}" for r, _ in all_results) + r" \\",
    r"\bottomrule",
    r"\end{tabular}",
    r"}",
    r"\begin{tablenotes}[flushleft]",
    r"\small",
    (r"\item Dependent variable: book leverage (dlttq + dlcq) / atq. "
     r"All specifications include firm and year-quarter fixed effects. "
     r"Standard errors (in parentheses) clustered at firm level. "
     r"NI/A = net income / total assets. "
     r"WW index (partial) = $-0.091 \times ((\text{ibq}+\text{dpq})/\text{atq}) "
     r"- 0.044 \times \log(\text{atq}) + 0.021 \times (\text{dlttq}/\text{atq})$, "
     r"following \citet{WhitedWu2006financial}. "
     r"Z-score component = $3.3 \times (\text{oibdpq}/\text{atq})$, the EBIT-to-assets "
     r"term from \citet{Altman1968}. "
     r"All variables winsorized at 1st/99th percentile. "
     r"$^{***}$, $^{**}$, $^{*}$ denote significance at 1\%, 5\%, 10\%."),
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
write_table(lines, TABS / "tab_robustness_distress.tex")

# ================================================================== #
# 5. Decile-10 robustness (Table B)
# ================================================================== #
print("\nRunning decile-10 robustness regressions...")

# Need W1s_decile from main panel
pan_dec = pan[["gvkey", "datadate", "W1s_decile"]].dropna(subset=["W1s_decile"])
df_with_dec = df.merge(pan_dec, on=["gvkey", "datadate"], how="left")

# Col A: baseline (full sample)
rA = run_col(df, REGS_BASE)

# Col B: exclude decile 10
df_nodec10 = df_with_dec[df_with_dec["W1s_decile"] < 10].copy()
rB = run_col(df_nodec10, REGS_BASE)

# Col C: winsorize W1_shape at 95th percentile (more aggressive)
df_w95 = df.copy()
w95 = df_w95["W1_shape"].quantile(0.95)
df_w95["W1_shape"] = df_w95["W1_shape"].clip(upper=w95)
rC = run_col(df_w95, REGS_BASE)

# Col D: winsorize W1_shape at 90th percentile (very aggressive)
df_w90 = df.copy()
w90 = df_w90["W1_shape"].quantile(0.90)
df_w90["W1_shape"] = df_w90["W1_shape"].clip(upper=w90)
rD = run_col(df_w90, REGS_BASE)

print("  W1_shape coefficient across decile-10 robustness:")
for res, lab in zip([rA, rB, rC, rD],
                    ["Full sample (baseline)", "Excl. decile 10", "Winsor p95", "Winsor p90"]):
    coef, se, n, r2v, _ = res
    print(f"    {lab}: beta={coef[0]:.4f}, SE={se[0]:.4f}, t={coef[0]/se[0]:.2f}, N={n:,}")

# W1_shape stats in each sample
for df_sub, lab in zip([df, df_nodec10, df_w95, df_w90],
                       ["Full", "Excl-D10", "Winsor-95", "Winsor-90"]):
    print(f"    {lab}: W1_shape mean={df_sub['W1_shape'].mean():.4f}, "
          f"p99={df_sub['W1_shape'].quantile(0.99):.4f}")

lines2 = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Robustness: Sensitivity to $\widehat{W}_{1,\text{shape}}$ Outliers}",
    r"\label{tab:robustness_decile}",
    r"\begin{threeparttable}",
    r"\resizebox{\textwidth}{!}{",
    r"\begin{tabular}{l" + "c"*4 + "}",
    r"\toprule",
    r" & (1) & (2) & (3) & (4) \\",
    r"\cmidrule(lr){2-5}",
    (r"Outcome: Book leverage & Baseline & Excl.\ decile 10 "
     r"& Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p95) "
     r"& Winsor.\ $\widehat{W}_{1,\text{shape}}$ (p90) \\"),
    r"\midrule",
]

ALL_RESULTS_B = [rA, rB, rC, rD]
for var in ["W1_shape"] + CONTROLS_BASE:
    coef_row, se_row = [], []
    for res in ALL_RESULTS_B:
        coef, se = res[0], res[1]
        idx = REGS_BASE.index(var) if var in REGS_BASE else None
        if idx is not None and idx < len(coef):
            c_s, s_s = fmt_coef(coef[idx], se[idx])
            coef_row.append(f"${c_s}$")
            se_row.append(s_s)
        else:
            coef_row.append(""); se_row.append("")
    lines2.append(DIST_LABS[var] + " & " + " & ".join(coef_row) + r" \\")
    lines2.append(" & " + " & ".join(se_row) + r" \\[2pt]")

lines2 += [
    r"\midrule",
    r"Firm FE & Yes & Yes & Yes & Yes \\",
    r"Year FE & Yes & Yes & Yes & Yes \\",
    r"$R^2$ & " + " & ".join(f"{r[3]:.4f}" for r in ALL_RESULTS_B) + r" \\",
    r"$N$ & " + " & ".join(f"{r[2]:,}" for r in ALL_RESULTS_B) + r" \\",
    r"\bottomrule",
    r"\end{tabular}",
    r"}",
    r"\begin{tablenotes}[flushleft]",
    r"\small",
    (r"\item Dependent variable: book leverage. All specifications include firm and "
     r"year-quarter fixed effects; standard errors clustered at firm level. "
     r"Column (2) excludes firm-quarters in the top decile of $\widehat{W}_{1,\text{shape}}$ "
     r"(decile 10, $\bar{W}_{1,\text{shape}} = 0.270$). "
     r"Columns (3)--(4) replace $\widehat{W}_{1,\text{shape}}$ with versions winsorized "
     r"at the 95th and 90th percentile, respectively. "
     r"$^{***}$, $^{**}$, $^{*}$ denote significance at 1\%, 5\%, 10\%."),
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
write_table(lines2, TABS / "tab_robustness_decile.tex")

# ================================================================== #
# 6. Bootstrap SE for kappa
# ================================================================== #
print("\nComputing bootstrap SE for kappa (100 firm-level replications)...")

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])

# Load trace spreads for spread regression
try:
    spreads = pd.read_parquet(PROC / "trace_spreads.parquet")
    spreads["datadate"] = pd.to_datetime(spreads["datadate"])
    spread_pan = pan.merge(spreads[["gvkey","datadate","spread_bps"]],
                           on=["gvkey","datadate"], how="inner",
                           suffixes=("", "_trace"))
    # Use trace spread if available; fall back to existing spread_bps in panel
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
    """Two-stage calibration on a bootstrap sample."""
    Q_mat = df_boot[QUANTILE_COLS].values.astype(np.float64)
    # Stage 1: Frechet mean
    Q_nu = np.nanmean(Q_mat, axis=0)
    E_nu = Q_nu.mean()
    # W1_shape
    cf_mean_arr = Q_mat.mean(axis=1)
    q_dem = Q_mat - cf_mean_arr[:, None]
    Q_dem = Q_nu   - E_nu
    w1s   = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)
    # Stage 2: spread regression
    has_spread = spread_pan["gvkey"].isin(df_boot["gvkey"].unique())
    sp_sub = spread_pan[has_spread].copy()
    # Recompute W1_shape for these firms using the bootstrap Frechet mean
    sp_sub2 = sp_sub.merge(
        df_boot[["gvkey","datadate"] + QUANTILE_COLS],
        on=["gvkey","datadate"], how="inner", suffixes=("","_b"))
    if len(sp_sub2) < 100:
        return np.nan, np.nan
    qm2 = sp_sub2[[c for c in sp_sub2.columns if c.endswith("_b") or c in QUANTILE_COLS]
                   ]
    # Use bootstrap Frechet mean to compute W1_shape for spread firms
    Q_cols = [c for c in sp_sub2.columns if c in QUANTILE_COLS]
    Q_mat2 = sp_sub2[Q_cols].values.astype(np.float64)
    cf_m2  = Q_mat2.mean(axis=1)
    q_dem2 = Q_mat2 - cf_m2[:, None]
    w1s2   = np.mean(np.abs(q_dem2 - Q_dem[None, :]), axis=1)
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
    beta_s = coef_s[1]
    kappa  = 2 * E_nu * beta_s
    return kappa, E_nu

np.random.seed(42)
firms_all = pan["gvkey"].unique()
kappas = []
for b in range(100):
    boot_firms = np.random.choice(firms_all, size=len(firms_all), replace=True)
    df_boot = pan[pan["gvkey"].isin(boot_firms)].copy()
    k, _ = estimate_kappa_once(df_boot)
    kappas.append(k)
    if (b + 1) % 25 == 0:
        valid = [x for x in kappas if not np.isnan(x)]
        print(f"  Bootstrap {b+1}/100 complete. kappa so far: "
              f"mean={np.mean(valid):.4f}, SE={np.std(valid):.4f}")

kappas_valid = [k for k in kappas if not np.isnan(k)]
kappa_boot_se = np.std(kappas_valid)
kappa_boot_mean = np.mean(kappas_valid)
print(f"\nBootstrap kappa: mean={kappa_boot_mean:.4f}, SE={kappa_boot_se:.4f}")
print(f"Point estimate (from main estimation): 0.4511")
print(f"Bootstrap SE for kappa: {kappa_boot_se:.4f}")
print(f"95% CI: ({kappa_boot_mean - 1.96*kappa_boot_se:.4f}, "
      f"{kappa_boot_mean + 1.96*kappa_boot_se:.4f})")

# Save kappa SE result to a file for reference
kappa_result = {
    "kappa_point": 0.4511,
    "kappa_boot_mean": kappa_boot_mean,
    "kappa_boot_se":   kappa_boot_se,
    "n_reps":          len(kappas_valid),
}
import json
with open(ROOT / "output" / "kappa_bootstrap.json", "w") as f:
    json.dump(kappa_result, f, indent=2)
print(f"\nSaved to output/kappa_bootstrap.json")
print("\nAll robustness tables done.")

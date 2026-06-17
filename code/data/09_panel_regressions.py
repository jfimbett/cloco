"""
Panel regressions of leverage on W1_shape (distributional mismatch).

This script:
  1. Loads the main panel from 08_smm_estimation.py
     (if main_panel.parquet doesn't have W1/W1_shape, recomputes from leverage_panel)
  2. Runs six leverage regressions:
     (1) OLS: book_lev ~ W1_shape
     (2) OLS: book_lev ~ W1_shape + cf_mean + cf_vol
     (3) OLS: book_lev ~ W1_shape + cf_mean + cf_vol + log_assets + mtb + prof + tang
     (4) FE:  col 3 + firm FE
     (5) FE:  col 3 + firm FE + year FE
     (6) FE:  col 5 with market_lev as outcome
  3. Tests the "shape beyond mean+vol" result:
     W1_resid = residual of W1_shape ~ cf_mean + cf_vol (the pure shape effect)
     Column 7: book_lev ~ W1_resid + cf_mean + cf_vol + std controls + firm + year FE
  4. Outputs:
     paper/tables/tab_panel_regressions.tex
     paper/tables/tab_summary_stats.tex

Note: linearmodels.PanelOLS for FE regressions, standard errors clustered at firm level.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.linalg import lstsq as sp_lstsq
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
TABS = ROOT / "paper" / "tables"
TABS.mkdir(parents=True, exist_ok=True)

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS   = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ================================================================== #
# 1. Load panel and ensure W1_shape is available
# ================================================================== #
print("Loading main panel...")
try:
    pan = pd.read_parquet(PROC / "main_panel.parquet")
    if "W1_shape" not in pan.columns:
        raise ValueError("W1_shape missing")
    print(f"  Loaded main_panel: {len(pan):,} obs")
except Exception:
    print("  main_panel missing W1_shape — recomputing from leverage_panel...")
    pan = pd.read_parquet(PROC / "leverage_panel.parquet")
    Q_mat    = pan[QUANTILE_COLS].values.astype(np.float64)
    Q_nu_raw = np.nanmean(Q_mat, axis=0)
    E_nu_raw = Q_nu_raw.mean()
    cf_mean_arr = Q_mat.mean(axis=1)
    q_dem    = Q_mat    - cf_mean_arr[:, None]
    Q_dem    = Q_nu_raw - E_nu_raw
    pan["W1"]       = np.mean(np.abs(Q_mat - Q_nu_raw[None, :]), axis=1)
    pan["W1_shape"] = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)
    pan["cf_mean_q"] = cf_mean_arr

pan["datadate"] = pd.to_datetime(pan["datadate"])

# ================================================================== #
# 2. Prepare regression sample
# ================================================================== #
CONTROLS = ["cf_mean", "cf_vol", "log_assets", "mtb", "profitability", "tangibility"]
USE_COLS = ["gvkey", "datadate", "year", "book_lev", "market_lev",
            "W1_shape", "W1", "cf_mean_q"] + CONTROLS

df = pan[USE_COLS].dropna(subset=["book_lev", "W1_shape"] + CONTROLS).copy()
# Force numpy dtypes to avoid pandas masked-array issues
for c in ["book_lev", "market_lev", "W1_shape", "W1", "cf_mean_q"] + CONTROLS:
    if c in df.columns:
        df[c] = df[c].astype(np.float64)

# Winsorize W1_shape at 1st/99th
lo_w = df["W1_shape"].quantile(0.01)
hi_w = df["W1_shape"].quantile(0.99)
df["W1_shape"] = df["W1_shape"].clip(lo_w, hi_w)

print(f"  Regression sample: {len(df):,} obs, {df.gvkey.nunique():,} firms")
print(f"  W1_shape: mean={df['W1_shape'].mean():.4f}, std={df['W1_shape'].std():.4f}")

# ================================================================== #
# 3. OLS regressions (hand-coded for max control)
# ================================================================== #
def ols(y, X):
    """Return coefficients, std errors (HC3-robust), t-stats."""
    coef, *_ = sp_lstsq(X, y, check_finite=False)
    resid    = y - X @ coef
    n, k     = X.shape
    # HC3 robust variance
    h   = np.einsum('ij,jk,ki->i', X, np.linalg.pinv(X.T @ X), X.T)
    e2  = (resid / (1 - h))**2
    XtX_inv = np.linalg.pinv(X.T @ X)
    V   = XtX_inv @ (X.T * e2) @ X @ XtX_inv
    se  = np.sqrt(np.diag(V))
    t   = coef / se
    r2  = 1 - np.sum(resid**2) / np.sum((y - y.mean())**2)
    return coef, se, t, r2, n

y_b = df["book_lev"].values
y_m = df["market_lev"].values

# Column 1: bivariate
c1_X = np.column_stack([np.ones(len(df)), df["W1_shape"].values])
c1   = ols(y_b, c1_X)

# Column 2: + cf_mean + cf_vol
c2_X = np.column_stack([np.ones(len(df)),
                         df["W1_shape"].values,
                         df["cf_mean"].values,
                         df["cf_vol"].values])
c2   = ols(y_b, c2_X)

# Column 3: + full controls (no FE)
c3_X = np.column_stack([np.ones(len(df)),
                         df["W1_shape"].values,
                         df[CONTROLS].values])
c3   = ols(y_b, c3_X)

# ================================================================== #
# 4. Fixed-effects regressions via within-transformation (firm FE)
# ================================================================== #
def within_transform(df, outcome, regressors, group):
    """Demean by group (within-transformation for FE)."""
    df2 = df.copy()
    gm  = df2.groupby(group)[regressors + [outcome]].transform("mean")
    for c in regressors + [outcome]:
        df2[c + "_w"] = df2[c] - gm[c]
    return df2

# Column 4: firm FE only
df4 = within_transform(df, "book_lev", ["W1_shape"] + CONTROLS, "gvkey")
c4_X = np.column_stack([df4[c + "_w"].values for c in ["W1_shape"] + CONTROLS])
c4   = ols(df4["book_lev_w"].values, c4_X)

# Column 5: firm + year FE (two-way within)
df5 = df.copy()
for c in ["W1_shape"] + CONTROLS + ["book_lev"]:
    gm_firm = df5.groupby("gvkey")[c].transform("mean")
    gm_year = df5.groupby("year")[c].transform("mean")
    gm_all  = df5[c].mean()
    df5[c + "_w"] = df5[c] - gm_firm - gm_year + gm_all
c5_X = np.column_stack([df5[c + "_w"].values for c in ["W1_shape"] + CONTROLS])
c5   = ols(df5["book_lev_w"].values, c5_X)

# Column 6: firm + year FE, market leverage outcome
df6 = df.dropna(subset=["market_lev"]).copy()
for c in ["W1_shape"] + CONTROLS + ["market_lev"]:
    gm_firm = df6.groupby("gvkey")[c].transform("mean")
    gm_year = df6.groupby("year")[c].transform("mean")
    gm_all  = df6[c].mean()
    df6[c + "_w"] = df6[c] - gm_firm - gm_year + gm_all
c6_X = np.column_stack([df6[c + "_w"].values for c in ["W1_shape"] + CONTROLS])
c6   = ols(df6["market_lev_w"].values, c6_X)

# Column 7: Shape-only W1 (residualized on cf_mean + cf_vol)
df7 = df5.copy()
Xres = np.column_stack([np.ones(len(df7)), df7["cf_mean_w"].values, df7["cf_vol_w"].values])
Xres_ok = np.isfinite(Xres).all(axis=1) & np.isfinite(df7["W1_shape_w"].values)
cres, *_ = sp_lstsq(Xres[Xres_ok], df7["W1_shape_w"].values[Xres_ok], check_finite=False)
df7["W1_resid_w"] = df7["W1_shape_w"] - Xres @ cres
c7_X = np.column_stack([df7["W1_resid_w"].values] + [df7[c+"_w"].values for c in CONTROLS])
c7   = ols(df7["book_lev_w"].values, c7_X)

# ================================================================== #
# 5. Cluster SEs at firm level for FE regressions
# ================================================================== #
def cluster_se(resid, X, group_arr):
    """Cluster standard errors by group."""
    XtX_inv = np.linalg.pinv(X.T @ X)
    groups  = np.unique(group_arr)
    B       = np.zeros((X.shape[1], X.shape[1]))
    for g in groups:
        mask = group_arr == g
        Xg   = X[mask]
        eg   = resid[mask]
        B   += (Xg.T @ eg[:, None]) @ (eg[None, :] @ Xg)
    G    = len(groups)
    n, k = X.shape
    adj  = (G / (G - 1)) * ((n - 1) / (n - k))   # small-sample correction
    V    = adj * XtX_inv @ B @ XtX_inv
    return np.sqrt(np.diag(V))

# Re-compute cluster SEs for columns 4, 5, 6, 7
for col_data, (c_val, c_X_arr, outcome_col, group_col) in enumerate([
    (c4, c4_X, "book_lev_w", df["gvkey"].values),
    (c5, c5_X, "book_lev_w", df["gvkey"].values),
    (c6, c6_X, "market_lev_w", df6["gvkey"].values),
]):
    coef = c_val[0]
    if col_data == 0: y_r = df4["book_lev_w"].values
    elif col_data == 1: y_r = df5["book_lev_w"].values
    else: y_r = df6["market_lev_w"].values
    resid = y_r - c_X_arr @ coef
    se_cl = cluster_se(resid, c_X_arr, group_col)
    if col_data == 0: c4 = (coef, se_cl, coef/se_cl, c4[3], c4[4])
    elif col_data == 1: c5 = (coef, se_cl, coef/se_cl, c5[3], c5[4])
    else: c6 = (coef, se_cl, coef/se_cl, c6[3], c6[4])

# Column 7 cluster SEs
resid7 = df7["book_lev_w"].values - c7_X @ c7[0]
se7_cl = cluster_se(resid7, c7_X, df5["gvkey"].values)
c7 = (c7[0], se7_cl, c7[0]/se7_cl, c7[3], c7[4])

# ================================================================== #
# 6. Print key results
# ================================================================== #
results = [c1, c2, c3, c4, c5, c6]
labels  = ["(1)", "(2)", "(3)", "(4) Firm FE", "(5) Two-way FE",
           "(6) Market Lev", "(7) Shape-only"]

print("\n=== Key coefficient on W1_shape / W1_resid ===")
for i, (res, lab) in enumerate(zip(results + [c7], labels)):
    coef = res[0][1] if i > 0 else res[0][1]  # skip constant
    se   = res[1][1] if i > 0 else res[1][1]
    t    = coef / se
    n    = res[4]
    r2   = res[3]
    print(f"  {lab}: coef={coef:.4f}, SE={se:.4f}, t={t:.2f}, R²={r2:.4f}, N={n:,}")

# ================================================================== #
# 7. Summary statistics table
# ================================================================== #
STAT_COLS = ["book_lev", "market_lev", "W1_shape", "W1",
             "cf_mean", "cf_vol", "log_assets", "mtb", "profitability", "tangibility"]
STAT_LABS = ["Book leverage", "Market leverage", "$\\widehat{W}_{1,\\text{shape}}$",
             "$\\widehat{W}_1$ (full)", "CF mean", "CF volatility",
             "Log assets", "Market-to-book", "Profitability", "Tangibility"]

ss_rows = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Summary Statistics}",
    r"\label{tab:summary_stats}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{lcccccc}",
    r"\toprule",
    r"Variable & Mean & Std & p10 & p50 & p90 & N \\",
    r"\midrule",
]
for col, lab in zip(STAT_COLS, STAT_LABS):
    if col in df.columns:
        x = df[col].dropna()
    elif col in pan.columns:
        x = pan[col].dropna()
    else:
        continue
    ss_rows.append(
        f"{lab} & {x.mean():.4f} & {x.std():.4f} & "
        f"{x.quantile(0.10):.4f} & {x.quantile(0.50):.4f} & "
        f"{x.quantile(0.90):.4f} & {len(x):,} \\\\"
    )
ss_rows += [
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}",
    r"\small",
    r"\item Book leverage = (dlttq + dlcq) / atq. Market leverage = debt / (debt + mktcap).",
    r"$\widehat{W}_{1,\text{shape}}$ = mean-adjusted Wasserstein-1 distance between firm",
    r"cash-flow distribution and aggregate capital supply distribution.",
    r"CF mean (vol) = rolling 20-quarter mean (std) of oancfy/atq.",
    r"Sample: Compustat quarterly 1989--2024, non-financial, non-utility firms.",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
with open(TABS / "tab_summary_stats.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(ss_rows))

# ================================================================== #
# 8. Panel regression table
# ================================================================== #
# Row labels: coefficient rows
ROW_LABS = [
    ("W1_shape",    r"$\widehat{W}_{1,\text{shape}}$"),
    ("cf_mean",     r"CF mean"),
    ("cf_vol",      r"CF volatility"),
    ("log_assets",  r"Log assets"),
    ("mtb",         r"Market-to-book"),
    ("profitability", r"Profitability"),
    ("tangibility", r"Tangibility"),
]

col_headers = [
    "(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)"
]
outcome_row   = ["Book lev", "Book lev", "Book lev", "Book lev", "Book lev", "Mkt lev", "Book lev"]
firm_fe_row   = ["No", "No", "No", "Yes", "Yes", "Yes", "Yes"]
year_fe_row   = ["No", "No", "No", "No", "Yes", "Yes", "Yes"]

# Mapping from variable name to index in coefficient vector
def get_idx(col_num, varname):
    """Return (coef_index, is_first_coef) for column col_num, variable varname."""
    if col_num == 1:
        # c1: const, W1_shape
        return {"W1_shape": 1}.get(varname, None)
    elif col_num == 2:
        # c2: const, W1_shape, cf_mean, cf_vol
        return {"W1_shape": 1, "cf_mean": 2, "cf_vol": 3}.get(varname, None)
    elif col_num in [3, 4, 5, 6]:
        # CONTROLS = ["cf_mean", "cf_vol", "log_assets", "mtb", "profitability", "tangibility"]
        base = {"W1_shape": 0, "cf_mean": 1, "cf_vol": 2,
                "log_assets": 3, "mtb": 4, "profitability": 5, "tangibility": 6}
        # col3 has const, so add 1 for c3; no const for FE cols
        if col_num == 3:
            return base[varname] + 1 if varname in base else None
        else:
            return base.get(varname, None)
    elif col_num == 7:
        # c7: W1_resid, controls (within)
        if varname == "W1_shape":
            return 0   # W1_resid
        base = {"cf_mean": 1, "cf_vol": 2, "log_assets": 3, "mtb": 4,
                "profitability": 5, "tangibility": 6}
        return base.get(varname, None)
    return None

all_results = [c1, c2, c3, c4, c5, c6, c7]

def fmt_coef(coef, se):
    stars = ""
    t = abs(coef/se)
    if t > 3.29: stars = "^{***}"
    elif t > 1.96: stars = "^{**}"
    elif t > 1.645: stars = "^{*}"
    return f"{coef:.4f}{stars}", f"({se:.4f})"

tab_rows = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Leverage and Distributional Mismatch: Panel Regressions}",
    r"\label{tab:panel_regressions}",
    r"\begin{threeparttable}",
    r"\resizebox{\textwidth}{!}{",
    r"\begin{tabular}{l" + "c"*7 + "}",
    r"\toprule",
    " & " + " & ".join(col_headers) + r" \\",
    r"\cmidrule(lr){2-8}",
    r"Outcome & " + " & ".join(outcome_row) + r" \\",
    r"\midrule",
]

for varname, lab in ROW_LABS:
    coef_strs, se_strs = [], []
    for ci, res in enumerate(all_results):
        idx = get_idx(ci+1, varname)
        if idx is not None and idx < len(res[0]):
            cf, se = float(res[0][idx]), float(res[1][idx])
            cs, ss = fmt_coef(cf, se)
            coef_strs.append(f"${cs}$")
            se_strs.append(f"{ss}")
        else:
            coef_strs.append("")
            se_strs.append("")
    tab_rows.append(lab + " & " + " & ".join(coef_strs) + r" \\")
    tab_rows.append(" & " + " & ".join(se_strs) + r" \\[2pt]")

tab_rows += [
    r"\midrule",
    r"Firm FE & " + " & ".join(firm_fe_row) + r" \\",
    r"Year FE & " + " & ".join(year_fe_row) + r" \\",
    r"$R^2$ & " + " & ".join(f"{r[3]:.4f}" for r in all_results) + r" \\",
    r"$N$ & " + " & ".join(f"{r[4]:,}" for r in all_results) + r" \\",
    r"\bottomrule",
    r"\end{tabular}",
    r"}",
    r"\begin{tablenotes}",
    r"\small",
    r"\item $^{***}$, $^{**}$, $^{*}$ denote significance at 1\%, 5\%, 10\%.",
    r"Columns (1)--(3): OLS with heteroskedasticity-robust (HC3) standard errors.",
    r"Columns (4)--(7): within-firm estimator; standard errors clustered at firm level.",
    r"Column (7): $\widehat{W}_{1,\text{shape}}$ is residualized on CF mean and CF volatility,",
    r"isolating the pure distributional shape component beyond mean and variance.",
    r"Sample: Compustat quarterly 1989--2024.",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]

with open(TABS / "tab_panel_regressions.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(tab_rows))

print(f"\nTables written to {TABS}")
print("Done.")

# ================================================================== #
# 9. W1 decile sort corrected for mean (the right way to visualize H1)
# ================================================================== #
print("\nW1_shape deciles (CONDITIONAL on cf_mean tercile):")
df["cf_tercile"] = pd.qcut(df["cf_mean"], 3, labels=["Low CF", "Mid CF", "High CF"])
for t in ["Low CF", "Mid CF", "High CF"]:
    sub = df[df["cf_tercile"] == t].copy()
    sub["W1s_d"] = pd.qcut(sub["W1_shape"], 5, labels=False) + 1
    dmean = sub.groupby("W1s_d")["book_lev"].mean()
    print(f"  {t}: " + " ".join(f"Q{k}={v:.3f}" for k,v in dmean.items()))
    rho_s, p_s = stats.spearmanr(sub["W1s_d"], sub["book_lev"])
    print(f"    Spearman rho={rho_s:.3f} (p={p_s:.4f})")

"""
Build the main leverage panel from Compustat fundq.

Outputs:
    data/processed/leverage_panel.parquet
    Columns: gvkey, datadate, book_lev, market_lev, log_assets,
             mtb, profitability, tangibility, cf_vol (rolling std),
             cf_mean (rolling mean from quantiles)
    + merges with mu_quantiles (q05..q95, n_obs)

Sample:
    - Non-financial (SIC 6000-6999 excluded), non-utility (4900-4999)
    - Positive assets (atq > 0), non-negative book equity (ceqq >= 0)
    - 1988-01-01 onward (SFAS 95 for oancfy)
    - At least 8 quarters of cash flow history (from mu_quantiles join)
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW  = Path(__file__).parents[2] / "data" / "raw"
PROC = Path(__file__).parents[2] / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ #
# 1. Load Compustat fundq
# ------------------------------------------------------------------ #
print("Loading Compustat fundq...")
q = pd.read_parquet(
    RAW / "compustat" / "fundq.parquet",
    columns=["gvkey", "datadate", "sic",
             "atq", "dlttq", "dlcq", "ceqq",
             "cshoq", "prccq",
             "oancfy", "oibdpq", "ppentq"]
)
q["datadate"] = pd.to_datetime(q["datadate"])
q = q[q["datadate"] >= "1988-01-01"].copy()
print(f"  Raw rows: {len(q):,}")

# ------------------------------------------------------------------ #
# 2. Industry exclusions + basic filters
# ------------------------------------------------------------------ #
q["sic"] = pd.to_numeric(q["sic"], errors="coerce")
q = q[~q["sic"].between(6000, 6999)]
q = q[~q["sic"].between(4900, 4999)]
q = q.dropna(subset=["atq"])
q = q[q["atq"] > 0]
q = q[q["ceqq"].fillna(-1) >= 0]      # non-negative book equity
print(f"  After industry/basic filters: {len(q):,}")

# ------------------------------------------------------------------ #
# 3. Fill missing debt items with 0 (some firms report no long-term debt)
# ------------------------------------------------------------------ #
q["dlttq"] = q["dlttq"].fillna(0)
q["dlcq"]  = q["dlcq"].fillna(0)
q["total_debt"] = q["dlttq"] + q["dlcq"]

# ------------------------------------------------------------------ #
# 4. Book and market leverage
# ------------------------------------------------------------------ #
q["book_lev"] = q["total_debt"] / q["atq"]
# Market equity: cshoq (millions of shares) * prccq ($/share)
q["mktcap"] = q["cshoq"].abs() * q["prccq"].abs()
q["market_lev"] = q["total_debt"] / (q["total_debt"] + q["mktcap"])

# Winsorize leverage at [0, 1]
q["book_lev"]   = q["book_lev"].clip(0, 1)
q["market_lev"] = q["market_lev"].clip(0, 1)

# Drop obs where price/shares are missing (can't compute market lev)
q = q.dropna(subset=["book_lev"])

# ------------------------------------------------------------------ #
# 5. Control variables
# ------------------------------------------------------------------ #
q["log_assets"]    = np.log(q["atq"])
q["mtb"]           = q["mktcap"] / q["ceqq"].replace(0, np.nan)
q["profitability"] = q["oibdpq"] / q["atq"]
q["tangibility"]   = q["ppentq"] / q["atq"]

# Winsorize controls at 1st/99th percentile
for col in ["book_lev", "market_lev", "mtb", "profitability", "tangibility"]:
    lo = q[col].quantile(0.01)
    hi = q[col].quantile(0.99)
    q[col] = q[col].clip(lo, hi)

# ------------------------------------------------------------------ #
# 6. Rolling cash flow mean and volatility (for controls in regressions)
#    These come from the same 20-quarter rolling window used in mu_quantiles
# ------------------------------------------------------------------ #
print("Computing rolling CF moments for controls...")
q["cf_ratio"] = q["oancfy"] / q["atq"]

# Global winsorize cf_ratio (same as in 05_build_mu_quantiles)
lo = q["cf_ratio"].quantile(0.01)
hi = q["cf_ratio"].quantile(0.99)
q["cf_ratio_w"] = q["cf_ratio"].clip(lo, hi)

q = q.sort_values(["gvkey", "datadate"]).reset_index(drop=True)

cf_mean_list = []
cf_vol_list  = []
for gvkey, grp in q.groupby("gvkey", sort=False):
    cf = grp["cf_ratio_w"].values
    n  = len(cf)
    means = np.full(n, np.nan)
    vols  = np.full(n, np.nan)
    for i in range(n):
        start = max(0, i - 19)
        w = cf[start:i+1]
        w = w[~np.isnan(w)]
        if len(w) >= 4:
            means[i] = np.mean(w)
            vols[i]  = np.std(w, ddof=1) if len(w) > 1 else 0.0
    cf_mean_list.append(means)
    cf_vol_list.append(vols)

q["cf_mean"] = np.concatenate(cf_mean_list)
q["cf_vol"]  = np.concatenate(cf_vol_list)

# ------------------------------------------------------------------ #
# 7. Merge with mu_quantiles (inner join — keeps firm-quarters with
#    at least 8 obs in the rolling window)
# ------------------------------------------------------------------ #
print("Merging with mu_quantiles...")
mu = pd.read_parquet(PROC / "mu_quantiles.parquet")
mu["datadate"] = pd.to_datetime(mu["datadate"])

panel = q.merge(mu[["gvkey", "datadate", "n_obs",
                     "q05", "q15", "q25", "q35", "q45",
                     "q55", "q65", "q75", "q85", "q95"]],
                on=["gvkey", "datadate"], how="inner")

print(f"  Panel after mu_quantiles merge: {len(panel):,} firm-quarters")
print(f"  Firms: {panel.gvkey.nunique():,}")
print(f"  Date range: {panel.datadate.min().date()} — {panel.datadate.max().date()}")

# ------------------------------------------------------------------ #
# 8. Add fiscal year-quarter label for FE
# ------------------------------------------------------------------ #
panel["year"]    = panel["datadate"].dt.year
panel["quarter"] = panel["datadate"].dt.quarter
panel["yt"]      = panel["year"].astype(str) + "Q" + panel["quarter"].astype(str)

# ------------------------------------------------------------------ #
# 9. Final column selection and save
# ------------------------------------------------------------------ #
keep = ["gvkey", "datadate", "year", "quarter", "yt", "sic",
        "book_lev", "market_lev", "total_debt", "atq",
        "log_assets", "mtb", "profitability", "tangibility",
        "cf_mean", "cf_vol",
        "n_obs", "q05", "q15", "q25", "q35", "q45",
        "q55", "q65", "q75", "q85", "q95"]

panel = panel[keep].reset_index(drop=True)

out = PROC / "leverage_panel.parquet"
panel.to_parquet(out, index=False)
print(f"\nSaved: {out}")
print(f"Shape: {panel.shape}")

print("\nLeverage summary:")
print(panel[["book_lev", "market_lev"]].describe().round(4))

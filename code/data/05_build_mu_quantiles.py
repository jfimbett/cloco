"""
Build non-parametric firm cash flow distributions (mu_it).

For each eligible firm-quarter, compute ten empirical quantile values from
the trailing 20 quarters of operating income scaled by assets.  The
quantile levels are the decile midpoints u_k = (2k-1)/20 for k=1..10,
i.e. {0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95}.

These ten values represent the discrete approximation of mu_it used in the
W1 computation:
    W1_hat(mu_it, nu(theta)) = (1/10) * sum_k |q_it_k - F_nu^{-1}(u_k)|

CASH FLOW VARIABLE: oibdpq / atq  (quarterly EBITDA / total assets)

oibdpq is Compustat's quarter-specific operating income before depreciation
(not YTD), so it directly measures the cash available for debt service in
each quarter without de-cumulation.  This avoids the YTD contamination
present in oancfy (year-to-date operating cash flow).  oibdpq is the
standard measure of "pledgeable income" in the structural capital-structure
literature (cf. Hennessy and Whited 2005, Strebulaev 2007).

Robustness: de-cumulated oancfy/atq results are available in Appendix B.

Input:
    data/raw/compustat/fundq.parquet

Output:
    data/processed/mu_quantiles.parquet
    Columns: gvkey, datadate, n_obs, q05, q15, q25, q35, q45, q55, q65, q75, q85, q95
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW = Path(__file__).parents[2] / "data" / "raw"
PROC = Path(__file__).parents[2] / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

QUANTILE_LEVELS = [(2 * k - 1) / 20 for k in range(1, 11)]  # 0.05, 0.15, ..., 0.95
QUANTILE_COLS   = ["q05", "q15", "q25", "q35", "q45", "q55", "q65", "q75", "q85", "q95"]
WINDOW          = 20   # rolling window in quarters
MIN_OBS         = 8    # minimum observations required

# ------------------------------------------------------------------
# 1. Load and filter Compustat
# ------------------------------------------------------------------
print("Loading Compustat...")
q = pd.read_parquet(RAW / "compustat" / "fundq.parquet",
                    columns=["gvkey", "datadate", "sic", "oibdpq", "atq"])

q["datadate"] = pd.to_datetime(q["datadate"])
q = q[q["datadate"] >= "1988-01-01"].copy()

# Industry exclusions
q["sic"] = pd.to_numeric(q["sic"], errors="coerce")
q = q[~q["sic"].between(6000, 6999)]
q = q[~q["sic"].between(4900, 4999)]

# Require positive assets and non-null EBITDA
q = q.dropna(subset=["oibdpq", "atq"])
q = q[q["atq"] > 0]

# Cash flow = quarterly EBITDA scaled by assets (no de-cumulation needed)
q["cf_ratio"] = q["oibdpq"] / q["atq"]

# Sort for rolling window
q = q.sort_values(["gvkey", "datadate"]).reset_index(drop=True)

# ------------------------------------------------------------------
# 2. Winsorize at 1st / 99th percentile (global, before rolling)
# ------------------------------------------------------------------
lo = q["cf_ratio"].quantile(0.01)
hi = q["cf_ratio"].quantile(0.99)
q["cf_ratio"] = q["cf_ratio"].clip(lo, hi)
print(f"Winsorize bounds (oibdpq/atq, quarterly EBITDA/A): [{lo:.4f}, {hi:.4f}]")
print(f"  Fraction positive: {(q['cf_ratio'] > 0).mean():.3f}")

# ------------------------------------------------------------------
# 4. Rolling quantile computation
# ------------------------------------------------------------------
print("Computing rolling quantiles (this may take a few minutes)...")

def rolling_quantiles(series, window, min_obs, levels):
    """Return a DataFrame of empirical quantiles from a rolling window."""
    n = len(series)
    out = np.full((n, len(levels)), np.nan)
    n_obs_arr = np.zeros(n, dtype=int)
    for i in range(n):
        start = max(0, i - window + 1)
        vals = series.iloc[start : i + 1].dropna().values
        n_obs_arr[i] = len(vals)
        if len(vals) >= min_obs:
            out[i] = np.quantile(vals, levels)
    return out, n_obs_arr

results = []
for gvkey, grp in q.groupby("gvkey", sort=False):
    grp = grp.reset_index(drop=True)
    qmat, nobs = rolling_quantiles(grp["cf_ratio"], WINDOW, MIN_OBS, QUANTILE_LEVELS)
    df = pd.DataFrame(qmat, columns=QUANTILE_COLS)
    df["gvkey"]    = gvkey
    df["datadate"] = grp["datadate"].values
    df["n_obs"]    = nobs
    results.append(df)

out = pd.concat(results, ignore_index=True)

# Drop firm-quarters that did not meet minimum observation threshold
out = out.dropna(subset=QUANTILE_COLS)

# Final column order
out = out[["gvkey", "datadate", "n_obs"] + QUANTILE_COLS]

# ------------------------------------------------------------------
# 5. Save
# ------------------------------------------------------------------
out_path = PROC / "mu_quantiles.parquet"
out.to_parquet(out_path, index=False)

print(f"\nDone.")
print(f"  Firm-quarters: {len(out):,}")
print(f"  Firms:         {out['gvkey'].nunique():,}")
print(f"  Date range:    {out['datadate'].min().date()} — {out['datadate'].max().date()}")
print(f"  Output:        {out_path}")
print(f"\nQuantile summary (across all firm-quarters):")
print(out[QUANTILE_COLS].describe().round(4).to_string())

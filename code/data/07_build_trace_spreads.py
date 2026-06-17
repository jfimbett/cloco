"""
Build firm-quarter credit spreads from TRACE bond transaction data.

Strategy:
    spread_it = quarterly mean(close_yld - GS10_monthly)
    GS10 = 10-year constant-maturity Treasury from FRED (monthly, mapped to quarter)
    Match TRACE bonds to Compustat firms via issuer CUSIP6 → gvkey.

Identification note:
    Using GS10 as a fixed benchmark introduces a level shift relative to
    maturity-matched spreads, but does NOT affect cross-sectional ordering
    within W1 deciles — which is what identifies κ in the SMM.

Outputs:
    data/processed/trace_spreads.parquet
    Columns: gvkey, datadate (quarter-end), spread_bps, n_bonds, n_obs

Coverage: 2012-2026 (TRACE Enhanced starts ~2012 in this extract)
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW  = Path(__file__).parents[2] / "data" / "raw"
PROC = Path(__file__).parents[2] / "data" / "processed"

# ------------------------------------------------------------------ #
# 1. Load TRACE
# ------------------------------------------------------------------ #
print("Loading TRACE trade_summary_corp...")
trace = pd.read_parquet(RAW / "trace" / "trade_summary_corp.parquet",
                        columns=["issuer_cusip6", "trans_dt", "close_yld"])
trace["trans_dt"] = pd.to_datetime(trace["trans_dt"])
print(f"  Raw: {len(trace):,} bond-days")

# ------------------------------------------------------------------ #
# 2. Filter yields to plausible corporate bond range
# ------------------------------------------------------------------ #
# close_yld is in percent (e.g., 4.5 means 4.5%)
# Exclude: zero (no yield), negative (data error), >30% (distressed extreme)
trace = trace[(trace["close_yld"] > 0.01) & (trace["close_yld"] < 30.0)]
print(f"  After yield filter (0.01–30%): {len(trace):,} bond-days")

# ------------------------------------------------------------------ #
# 3. Match TRACE → gvkey via CUSIP6
# ------------------------------------------------------------------ #
print("Matching CUSIP6 → gvkey...")
cusip_map = pd.read_parquet(RAW / "trace" / "company_cusip.parquet",
                            columns=["gvkey", "cusip6", "year1", "year2"])

# Keep one gvkey per cusip6 (latest available link to handle re-listings)
# For time-varying links: match on year1 <= trade_year <= year2
# For simplicity: use the most recent record per cusip6
cusip_map["year2"] = cusip_map["year2"].fillna(9999)
cusip_map = (cusip_map
             .sort_values(["cusip6", "year2"], ascending=[True, False])
             .drop_duplicates("cusip6", keep="first")
             [["gvkey", "cusip6"]])

trace = trace.merge(cusip_map, left_on="issuer_cusip6", right_on="cusip6", how="inner")
print(f"  After CUSIP match: {len(trace):,} bond-days, {trace.gvkey.nunique():,} firms")

# ------------------------------------------------------------------ #
# 4. Load FRED GS10 and map to months
# ------------------------------------------------------------------ #
print("Loading FRED GS10...")
fred = pd.read_parquet(RAW / "fred" / "macro_controls.parquet")
fred = fred.reset_index()
# fred index is 'date' (monthly), column 'gs10' in percent
fred["ym"] = fred["date"].dt.to_period("M")
gs10 = fred[["ym", "gs10"]].dropna().set_index("ym")["gs10"]

# Map each TRACE observation to month → GS10
trace["ym"] = trace["trans_dt"].dt.to_period("M")
trace["gs10"] = trace["ym"].map(gs10)

# Drop obs where GS10 is missing (before 1985 or after latest FRED date)
trace = trace.dropna(subset=["gs10"])

# Spread in basis points (100 bps = 1 percentage point)
trace["spread_bps"] = (trace["close_yld"] - trace["gs10"]) * 100

# Keep only positive spreads (negative = pricing error or very short maturities)
trace = trace[trace["spread_bps"] > -200]   # allow slightly negative (short bonds)
trace = trace[trace["spread_bps"] < 3000]   # cap at 30 pp = 3000 bps (severe distress)

print(f"  After spread filter: {len(trace):,} bond-days")
print(f"  Spread range: {trace.spread_bps.min():.1f} — {trace.spread_bps.max():.1f} bps")

# ------------------------------------------------------------------ #
# 5. Aggregate to firm-quarter
# ------------------------------------------------------------------ #
print("Aggregating to firm-quarter...")
trace["datadate"] = trace["trans_dt"].dt.to_period("Q").dt.to_timestamp("Q")

firm_q = (trace
          .groupby(["gvkey", "datadate"])
          .agg(spread_bps=("spread_bps", "mean"),
               n_obs=("spread_bps", "count"))
          .reset_index())

# Require at least 5 daily observations per firm-quarter for reliability
firm_q = firm_q[firm_q["n_obs"] >= 5]

firm_q["datadate"] = pd.to_datetime(firm_q["datadate"])

print(f"  Firm-quarters: {len(firm_q):,}")
print(f"  Firms:         {firm_q.gvkey.nunique():,}")
print(f"  Date range:    {firm_q.datadate.min().date()} — {firm_q.datadate.max().date()}")
print(f"\nSpread summary (bps):")
print(firm_q["spread_bps"].describe().round(1))

# ------------------------------------------------------------------ #
# 6. Save
# ------------------------------------------------------------------ #
out = PROC / "trace_spreads.parquet"
firm_q.to_parquet(out, index=False)
print(f"\nSaved: {out}")

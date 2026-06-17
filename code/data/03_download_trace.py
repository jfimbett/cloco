"""
Download TRACE bond transaction data from WRDS (replaces FISD for spread moments).

Uses trace.trade_summary — pre-aggregated daily data, already Dick-Nielsen cleaned.
Corporate bonds only, 2002-2024.

Usage:
    python 03_download_trace.py

Output:
    data/raw/trace/trade_summary_corp.parquet   daily bond yields (CUSIP x date)
    data/raw/trace/company_cusip.parquet        gvkey -> 6-digit CUSIP map from Compustat

Spread construction (in cleaning step):
    spread = close_yld - gs10   (10-year Treasury from FRED, fixed maturity benchmark)
    Quarterly average spread per bond, then matched to firm-quarter via issuer CUSIP.
    Fixed benchmark introduces a systematic level shift but does not affect
    cross-sectional ordering within W1 deciles.

Coverage note:
    TRACE mandatory reporting began July 2002 for investment grade,
    expanding to all corporate bonds by January 2005. Sample effectively
    starts 2005 for full coverage.
"""

import wrds
import pandas as pd
from pathlib import Path

TRACE_OUT = Path(__file__).parents[2] / "data" / "raw" / "trace"
TRACE_OUT.mkdir(parents=True, exist_ok=True)

db = wrds.Connection(wrds_username="juanimbet")

# ------------------------------------------------------------------
# 1. TRACE daily trade summary — corporate bonds
#    cusip_id       : 9-digit CUSIP (first 6 = issuer CUSIP)
#    trans_dt       : trade date
#    close_yld      : closing yield for the day (percent)
#    close_pr       : closing price
#    company_symbol : 6-char company identifier
#    sub_prd_type   : product subtype — keep 'CORP' (corporate bonds)
# ------------------------------------------------------------------
TRACE_QUERY = """
    SELECT cusip_id, trans_dt, close_yld, close_pr, company_symbol
    FROM trace.trade_summary
    WHERE sub_prd_type = 'CORP'
      AND trans_dt     >= '2002-01-01'
      AND close_yld    IS NOT NULL
"""
if (TRACE_OUT / "trade_summary_corp.parquet").exists():
    print("TRACE file already exists — skipping download.")
else:
    print("Downloading TRACE trade_summary (corporate bonds)...")
    trace = db.raw_sql(TRACE_QUERY, date_cols=["trans_dt"])
    print(f"TRACE: {len(trace):,} bond-days, {trace.cusip_id.nunique():,} CUSIPs")
    trace["issuer_cusip6"] = trace["cusip_id"].str[:6]
    trace.to_parquet(TRACE_OUT / "trade_summary_corp.parquet", index=False)
    print(f"Saved to {TRACE_OUT / 'trade_summary_corp.parquet'}")

# ------------------------------------------------------------------
# 2. Compustat CUSIP map (gvkey -> CUSIP) from comp.names
#    comp.names has historical name/CUSIP records per firm with year ranges.
#    cusip is VARCHAR(21) — first 6 chars = issuer CUSIP matching TRACE.
#    year1/year2 allow time-aware matching if needed; here we take all records
#    and dedupe to unique gvkey-cusip6 pairs.
# ------------------------------------------------------------------
CUSIP_QUERY = """
    SELECT gvkey, cusip, sic, year1, year2
    FROM comp.names
    WHERE cusip IS NOT NULL
"""
print("\nDownloading Compustat company CUSIP map (comp.names)...")
cusip_map = db.raw_sql(CUSIP_QUERY)
cusip_map["cusip6"] = cusip_map["cusip"].str[:6]
print(f"Company CUSIP map: {len(cusip_map):,} records, {cusip_map.gvkey.nunique():,} firms")
cusip_map.to_parquet(TRACE_OUT / "company_cusip.parquet", index=False)
print(f"Saved to {TRACE_OUT / 'company_cusip.parquet'}")

db.close()
print("\nDone.")

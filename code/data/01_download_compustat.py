"""
Download Compustat Fundamentals Quarterly from WRDS.

Usage:
    python 01_download_compustat.py

Requires: wrds Python package  (pip install wrds)
          WRDS credentials set up via  wrds.Connection()  (prompts on first run)

Output:
    data/raw/compustat/fundq.parquet
"""

import wrds
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parents[2] / "data" / "raw" / "compustat"
OUT.mkdir(parents=True, exist_ok=True)

# Variables needed
# oancfy   : operating cash flows, year-to-date (SFAS 95, from 1988)
# atq      : total assets
# dlttq    : long-term debt, total
# dlcq     : debt in current liabilities (current portion of LT debt)
# ceqq     : common equity (to filter negative book equity)
# cshoq    : common shares outstanding
# prccq    : price per share, calendar-quarter close
# ibq      : income before extraordinary items (robustness CF measure)
# dpq      : depreciation & amortization quarterly (robustness CF measure)
# oibdpq   : operating income before D&P (profitability control)
# ppentq   : net PP&E (tangibility control)
# sic      : SIC code — lives in comp.company, joined in below
# fyearq   : fiscal year
# fqtr     : fiscal quarter

QUERY = """
    SELECT
        f.gvkey, f.datadate, f.fyearq, f.fqtr, c.sic,
        f.oancfy, f.atq, f.dlttq, f.dlcq, f.ceqq,
        f.cshoq, f.prccq, f.ibq, f.dpq, f.oibdpq, f.ppentq
    FROM comp.fundq f
    LEFT JOIN comp.company c ON f.gvkey = c.gvkey
    WHERE f.indfmt  = 'INDL'
      AND f.datafmt = 'STD'
      AND f.popsrc  = 'D'
      AND f.consol  = 'C'
      AND f.datadate >= '1985-01-01'
"""

db = wrds.Connection(wrds_username="juanimbet")
df = db.raw_sql(QUERY, date_cols=["datadate"])
db.close()

print(f"Downloaded {len(df):,} firm-quarters, {df.gvkey.nunique():,} firms")
df.to_parquet(OUT / "fundq.parquet", index=False)
print(f"Saved to {OUT / 'fundq.parquet'}")

"""
Download Treasury constant-maturity yields and macro controls from FRED.

Usage:
    python 04_download_fred.py

    Requires: pandas-datareader  (pip install pandas-datareader)
    No credentials needed — FRED is public.

Output:
    data/raw/fred/treasury_yields.parquet   monthly CMT yields
    data/raw/fred/macro_controls.parquet    macro controls for estimation

Treasury series used to compute bond spreads at issuance:
    GS1, GS2, GS3, GS5, GS7, GS10, GS20, GS30
    (Constant Maturity Treasury yields, percent per annum)

Macro controls used in structural estimation:
    TB3MS   : 3-month T-bill rate
    GS10    : 10-year Treasury yield (already in CMT set)
    BAA     : Moody's Baa corporate bond yield
    AAA     : Moody's Aaa corporate bond yield
    (BAA - AAA = credit spread proxy for aggregate capital supply conditions)
"""

import pandas_datareader.data as web
import pandas as pd
from pathlib import Path

FRED_OUT = Path(__file__).parents[2] / "data" / "raw" / "fred"
FRED_OUT.mkdir(parents=True, exist_ok=True)

START = "1985-01-01"
END   = "2024-12-31"

# ------------------------------------------------------------------
# 1. Treasury constant-maturity yields (for spread construction)
# ------------------------------------------------------------------
CMT_SERIES = ["GS1", "GS2", "GS3", "GS5", "GS7", "GS10", "GS20", "GS30"]
cmt = web.DataReader(CMT_SERIES, "fred", START, END)
cmt.index.name = "date"
cmt.columns = [c.lower() for c in cmt.columns]
print(f"Treasury yields: {cmt.shape}")
cmt.to_parquet(FRED_OUT / "treasury_yields.parquet")

# ------------------------------------------------------------------
# 2. Macro controls
# ------------------------------------------------------------------
MACRO_SERIES = ["TB3MS", "GS10", "BAA", "AAA"]
macro = web.DataReader(MACRO_SERIES, "fred", START, END)
macro.index.name = "date"
macro.columns = [c.lower() for c in macro.columns]
macro["baa_aaa_spread"] = macro["baa"] - macro["aaa"]
print(f"Macro controls: {macro.shape}")
macro.to_parquet(FRED_OUT / "macro_controls.parquet")

print("Done.")

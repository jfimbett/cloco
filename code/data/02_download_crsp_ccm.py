"""
Download CRSP monthly stock file and the CRSP/Compustat Merged link table from WRDS.

Usage:
    python 02_download_crsp_ccm.py

Output:
    data/raw/crsp/msf.parquet          CRSP monthly stock file (price, shares)
    data/raw/ccm/ccmxpf_lnkhist.parquet  CCM link table
"""

import wrds
import pandas as pd
from pathlib import Path

CRSP_OUT = Path(__file__).parents[2] / "data" / "raw" / "crsp"
CCM_OUT  = Path(__file__).parents[2] / "data" / "raw" / "ccm"
CRSP_OUT.mkdir(parents=True, exist_ok=True)
CCM_OUT.mkdir(parents=True, exist_ok=True)

db = wrds.Connection(wrds_username="juanimbet")

# ------------------------------------------------------------------
# 1. CRSP monthly stock file
#    permno  : permanent company number (CRSP identifier)
#    date    : month-end date
#    prc     : price (negative if from bid-ask midpoint — take abs)
#    shrout  : shares outstanding (thousands)
#    hexcd   : exchange code (1=NYSE, 2=AMEX, 3=NASDAQ) — "hexcd" in new WRDS
#    shrcd   : share code (10, 11 = ordinary common shares) — in crsp.stocknames
#
#    shrcd is NOT in crsp.msf; it lives in crsp.stocknames with date ranges.
#    Join on permno + date within [namedt, nameendt] to get it.
# ------------------------------------------------------------------
MSF_QUERY = """
    SELECT m.permno, m.date, m.prc, m.shrout, m.hexcd, s.shrcd
    FROM crsp.msf m
    INNER JOIN crsp.stocknames s
        ON m.permno = s.permno
       AND m.date BETWEEN s.namedt AND COALESCE(s.nameenddt, CURRENT_DATE)
    WHERE m.date >= '1985-01-01'
      AND s.shrcd IN (10, 11)
"""
msf = db.raw_sql(MSF_QUERY, date_cols=["date"])
msf["prc"] = msf["prc"].abs()                    # negative = bid-ask mid
msf = msf.rename(columns={"hexcd": "exchcd"})   # normalise to familiar name
msf["mktcap"] = msf["prc"] * msf["shrout"]      # in thousands of dollars
print(f"CRSP msf: {len(msf):,} obs, {msf.permno.nunique():,} permnos")
msf.to_parquet(CRSP_OUT / "msf.parquet", index=False)

# ------------------------------------------------------------------
# 2. CCM link table
#    gvkey       : Compustat firm identifier
#    lpermno     : CRSP permno
#    linktype    : keep LC (confirmed), LU (unconfirmed), LS (single)
#    linkprim    : keep P (primary), C (primary conditional)
#    linkdt      : link start date
#    linkenddt   : link end date (null = still active)
# ------------------------------------------------------------------
CCM_QUERY = """
    SELECT gvkey, lpermno AS permno, linktype, linkprim, linkdt, linkenddt
    FROM crsp.ccmxpf_lnkhist
    WHERE linktype IN ('LC', 'LU', 'LS')
      AND linkprim IN ('P', 'C')
"""
ccm = db.raw_sql(CCM_QUERY, date_cols=["linkdt", "linkenddt"])
# Replace NULL linkenddt with a far-future date so date comparisons work
ccm["linkenddt"] = ccm["linkenddt"].fillna(pd.Timestamp("2099-12-31"))
print(f"CCM links: {len(ccm):,} rows, {ccm.gvkey.nunique():,} gvkeys")
ccm.to_parquet(CCM_OUT / "ccmxpf_lnkhist.parquet", index=False)

db.close()
print("Done.")

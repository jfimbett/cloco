"""
Download Mergent FISD bond issuance data from WRDS.

Usage:
    python 03_download_fisd.py

Output:
    data/raw/fisd/fisd_mergedissue.parquet   bond-level issuance data
    data/raw/fisd/fisd_issuer.parquet        issuer-level data

Notes:
    - FISD coverage is reliable from ~1995; earlier data exists but is sparse
    - We keep US-domiciled corporate straight bonds with an offering yield
    - country_domicile lives in fisd_issuer (not fisd_mergedissue) — join required
    - callable does not exist in fisd_mergedissue; redeemable is the closest proxy
    - sic_code does not exist in either FISD table; use naics_code / industry_group
      Industry exclusions (financials, utilities) applied when merging with Compustat
    - Spread = offering_yield - Treasury yield at matching maturity (cleaning step)
"""

import wrds
from pathlib import Path

FISD_OUT = Path(__file__).parents[2] / "data" / "raw" / "fisd"
FISD_OUT.mkdir(parents=True, exist_ok=True)

db = wrds.Connection(wrds_username="juanimbet")

# ------------------------------------------------------------------
# 1. Bond issuance file (fisd.fisd_mergedissue)
#    country_domicile is in fisd_issuer, so we join to filter on it.
#    callable does not exist — redeemable is the closest available flag.
#    sic_code does not exist — industry filtered via Compustat merge later.
#
#    issue_id       : bond identifier
#    issuer_id      : issuer identifier (links to fisd_issuer)
#    complete_cusip : 9-digit CUSIP
#    issuer_cusip   : 6-digit issuer CUSIP (for Compustat match via cusip)
#    offering_date  : issuance date
#    maturity       : maturity date (needed for Treasury yield matching)
#    offering_yield : yield at issuance (percent, e.g. 5.25 = 5.25%)
#    offering_price : price at issuance (usually 100)
#    offering_amt   : deal size (USD thousands)
#    coupon_type    : FIXED, ZERO, VARIABLE
#    bond_type      : CDEB = corporate debenture, etc.
#    rule_144a      : 'Y'/'N' — 144A bonds have lower secondary liquidity
#    convertible    : 'Y'/'N' — exclude convertibles
#    redeemable     : 'Y'/'N' — closest proxy for callable in this table
#    putable        : 'Y'/'N'
#    security_level : SECRD, UNSECRD, etc.
#    currency       : keep 'USD'
# ------------------------------------------------------------------
ISSUE_QUERY = """
    SELECT
        f.issue_id, f.issuer_id, f.complete_cusip, f.issuer_cusip,
        f.offering_date, f.maturity, f.offering_yield, f.offering_price, f.offering_amt,
        f.coupon_type, f.bond_type, f.rule_144a,
        f.convertible, f.redeemable, f.putable, f.security_level,
        f.currency
    FROM fisd.fisd_mergedissue f
    INNER JOIN fisd.fisd_issuer i ON f.issuer_id = i.issuer_id
    WHERE i.country_domicile = 'USA'
      AND f.currency         = 'USD'
      AND f.convertible      = 'N'
      AND f.offering_yield   IS NOT NULL
      AND f.offering_date    >= '1993-01-01'
"""
issues = db.raw_sql(ISSUE_QUERY, date_cols=["offering_date", "maturity"])
print(f"FISD issues: {len(issues):,} bonds, {issues.issuer_cusip.nunique():,} unique issuer CUSIPs")
issues.to_parquet(FISD_OUT / "fisd_mergedissue.parquet", index=False)

# ------------------------------------------------------------------
# 2. Issuer file (fisd.fisd_issuer)
#    issuer_id        : issuer identifier
#    country_domicile : country of domicile
#    industry_group   : FISD industry classification (4-char)
#    industry_code    : FISD industry sub-code
#    naics_code       : NAICS code (no SIC in this table)
#
#    Note: issuer_cusip and sic_code do NOT exist in fisd_issuer.
#    The 6-digit issuer CUSIP for Compustat matching is in fisd_mergedissue.issuer_cusip.
# ------------------------------------------------------------------
ISSUER_QUERY = """
    SELECT issuer_id, country_domicile, industry_group, industry_code, naics_code
    FROM fisd.fisd_issuer
    WHERE country_domicile = 'USA'
"""
issuers = db.raw_sql(ISSUER_QUERY)
print(f"FISD issuers: {len(issuers):,} rows")
issuers.to_parquet(FISD_OUT / "fisd_issuer.parquet", index=False)

db.close()
print("Done.")

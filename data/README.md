# Data

Raw and processed data for *Distributional Debt Capacity*.

Data files are excluded from git. Run the download scripts in `code/data/` to populate the folders.

---

## What to Download and From Where

### 1. Compustat Fundamentals Quarterly — WRDS

**Source:** `comp.fundq` via WRDS  
**Script:** `code/data/01_download_compustat.py`  
**Output:** `data/raw/compustat/fundq.parquet`

Log in to WRDS and run the script, or use the WRDS web query tool:
- Library: `COMPUSTAT`
- Dataset: `Fundamentals Quarterly (FUNDQ)`
- Date range: 1985–2024 (we start 1985 to have enough history for rolling windows; sample starts 1988)
- `indfmt=INDL`, `datafmt=STD`, `popsrc=D`, `consol=C`

Variables to pull:

| Variable | Description |
|----------|-------------|
| `gvkey` | Firm identifier |
| `datadate` | Fiscal quarter end date |
| `fyearq`, `fqtr` | Fiscal year and quarter |
| `sic` | SIC code (for industry exclusions) |
| `oancfy` | Operating cash flows, YTD (SFAS 95) |
| `atq` | Total assets |
| `dlttq` | Long-term debt |
| `dlcq` | Debt in current liabilities |
| `ceqq` | Common equity |
| `cshoq` | Common shares outstanding |
| `prccq` | Price per share, quarter close |
| `ibq` | Income before extraordinary items |
| `dpq` | Depreciation & amortization |
| `oibdpq` | Operating income before D&P |
| `ppentq` | Net PP&E |

---

### 2. CRSP Monthly Stock File — WRDS

**Source:** `crsp.msf` via WRDS  
**Script:** `code/data/02_download_crsp_ccm.py`  
**Output:** `data/raw/crsp/msf.parquet`

- Share codes 10 and 11 (ordinary common shares) only
- Date range: 1985–2024

Variables: `permno`, `date`, `prc`, `shrout`, `exchcd`, `shrcd`

---

### 3. CRSP/Compustat Merged Link Table — WRDS

**Source:** `crsp.ccmxpf_lnkhist` via WRDS  
**Script:** `code/data/02_download_crsp_ccm.py`  
**Output:** `data/raw/ccm/ccmxpf_lnkhist.parquet`

Keep only: `linktype IN ('LC','LU','LS')` and `linkprim IN ('P','C')`

Variables: `gvkey`, `lpermno`, `linktype`, `linkprim`, `linkdt`, `linkenddt`

---

### 4. Mergent FISD — WRDS

**Source:** `fisd.fisd_mergedissue` and `fisd.fisd_issuer` via WRDS  
**Script:** `code/data/03_download_fisd.py`  
**Output:** `data/raw/fisd/fisd_mergedissue.parquet`, `data/raw/fisd/fisd_issuer.parquet`

- US-domiciled issuers (`country_domicile = 'USA'`), USD-denominated
- Exclude convertibles
- Keep only bonds with a non-null `offering_yield`
- Date range: 1993–2024 (FISD is reliable from ~1995; pull from 1993 to be safe)

Key variables: `issue_id`, `issuer_id`, `complete_cusip`, `issuer_cusip`, `offering_date`, `maturity`, `offering_yield`, `offering_amt`, `coupon_type`, `convertible`, `redeemable`, `rule_144a`, `security_level`

FISD schema notes: `country_domicile` is in `fisd_issuer` (not `fisd_mergedissue`), so the download joins the two tables. `callable` does not exist — `redeemable` is used instead. `sic_code` does not exist in either FISD table; industry exclusions (financials/utilities) are applied when merging with Compustat.

**Note:** You need a WRDS subscription that includes Mergent FISD. Check access at `wrds.wharton.upenn.edu` under the Mergent module. FISD has been available to most academic subscribers since ~2010.

---

### 5. FRED (Treasury Yields + Macro Controls) — Public

**Source:** FRED API (no credentials required)  
**Script:** `code/data/04_download_fred.py`  
**Output:** `data/raw/fred/treasury_yields.parquet`, `data/raw/fred/macro_controls.parquet`

Requires `pip install pandas-datareader`.

Treasury series for spread construction:

| Series | Description |
|--------|-------------|
| `GS1` | 1-year constant maturity Treasury |
| `GS2` | 2-year |
| `GS3` | 3-year |
| `GS5` | 5-year |
| `GS7` | 7-year |
| `GS10` | 10-year |
| `GS20` | 20-year |
| `GS30` | 30-year |

Macro controls:

| Series | Description |
|--------|-------------|
| `TB3MS` | 3-month T-bill rate |
| `BAA` | Moody's Baa yield |
| `AAA` | Moody's Aaa yield |

---

## How to Run

```bash
# Install dependencies once
pip install wrds pandas-datareader pyarrow

# Step 1: Download raw data (order matters — CCM links needed for merging)
cd code/data
python 01_download_compustat.py
python 02_download_crsp_ccm.py
python 03_download_fisd.py
python 04_download_fred.py

# Step 2: Build firm cash flow distributions (mu_it)
python 05_build_mu_quantiles.py
```

WRDS will prompt for your username and password on first connection; credentials are cached in `~/.pgpass` afterward.

### What `05_build_mu_quantiles.py` does

For each eligible firm-quarter (post-1988, non-financial, non-utility, at least 8 observations in the rolling window), computes ten empirical quantile values of the trailing 20-quarter cash flow ratio (`oancfy/atq`), winsorized at the 1st and 99th percentile.

Quantile levels: $u_k = (2k-1)/20$ for $k=1,\ldots,10$ — i.e., $\{0.05, 0.15, \ldots, 0.95\}$ (decile midpoints).

Output: `data/processed/mu_quantiles.parquet` — columns `gvkey`, `datadate`, `n_obs`, `q05`, `q15`, ..., `q95`.

These ten values are the non-parametric representation of $\hat\mu_{it}$ used in the SMM step. No distributional assumption is imposed.

---

## Folder Structure

```
data/
├── raw/
│   ├── compustat/    fundq.parquet
│   ├── crsp/         msf.parquet
│   ├── ccm/          ccmxpf_lnkhist.parquet
│   ├── fisd/         fisd_mergedissue.parquet, fisd_issuer.parquet
│   └── fred/         treasury_yields.parquet, macro_controls.parquet
└── processed/        (populated by cleaning scripts — code/data/05_*.py onward)
```

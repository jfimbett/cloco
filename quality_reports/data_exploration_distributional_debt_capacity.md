# Data Assessment: Distributional Debt Capacity Paper
**Date:** 2026-06-13
**Researcher:** Juan F. Imbet, Paris Dauphine University - PSL
**Research Question:** Does W1(μ_it, ν_t) explain cross-sectional leverage heterogeneity beyond mean and variance?
**Estimation Method:** SMM with θ = (α_ν, σ_ν, κ)

---

## Executive Summary

The core empirical infrastructure for this project is feasible with standard WRDS access: Compustat Quarterly (`comp.fundq`) provides reliable cash flow and balance sheet data from ~1988 onward (the SFAS 95 boundary for `oancfy`), and Mergent FISD (`fisd.fisd_mergedissue`) provides the cleanest source of credit spreads at issuance for identifying bankruptcy cost κ, though its coverage is most reliable from 1995 onward. The critical gap is Component C — there is no off-the-shelf cross-sectional distribution of capital supply ν_t; constructing it requires either (a) aggregating bank-level lending from Call Reports (`bank_all` schema on WRDS, available from 1976), (b) using bond issuance amounts from Mergent FISD as a proxy, or (c) using Z.1 aggregate credit flow data (FRED series `BCNSDODNS`) as a single moment rather than a distribution. This construction choice is the most consequential modeling decision in the project and will require explicit justification in the paper. The recommended sample period is 1988–2024 for cash flows, with credit spread identification starting in 1995.

---

## Component A: Firm Cash Flow Distributions (μ_it)

**Primary Dataset(s):** Compustat North America Fundamentals Quarterly
**Provider:** S&P Global via WRDS
**WRDS dataset path(s):** `comp.fundq` (VERIFIED from multiple academic sources and WRDS documentation)

**Key Variables:**

| Variable | Mnemonic | Description | Verified? |
|----------|----------|-------------|-----------|
| Net cash from operations (YTD) | `oancfy` | Year-to-date operating cash flow; subtract adjacent quarters to get quarterly flow | VERIFIED (SFAS 95, available from 1988) |
| Net income | `ibq` | Quarterly net income | VERIFIED |
| Depreciation & amortization | `dpq` | Quarterly D&A | VERIFIED |
| Total assets | `atq` | Quarterly total assets | VERIFIED |
| Property, plant & equipment (net) | `ppentq` | Quarterly net PP&E | VERIFIED |
| Operating income before D&A | `oibdpq` | EBITDA proxy | VERIFIED |
| GVKEY | `gvkey` | Compustat firm identifier | VERIFIED |
| Fiscal quarter end date | `datadate` | Quarter-end date | VERIFIED |
| Fiscal year | `fyearq` | Fiscal year | VERIFIED |
| Fiscal quarter | `fqtr` | Fiscal quarter (1–4) | VERIFIED |
| SIC code | `sic` | Industry classification | VERIFIED |

**Coverage:**
- Time period: 1961 (quarterly database inception) — present, but SFAS 95 cash flow items (`oancfy`) reliably available from **1988** onward (VERIFIED). Before 1988, Compustat used `fopty` (funds from operations), which is a different concept; switching to `oancfy` as the cash flow numerator limits the clean sample to 1988+.
- Geography: US and Canada (North America database)
- Frequency: Quarterly
- Approximate observations: Hundreds of thousands of firm-quarters; universe of US listed firms

**Feasibility Grade: A**
- Ready to use with standard WRDS access and well-documented construction steps.

**Strengths for this research design:**
- `comp.fundq` is the universal standard for US corporate finance panel data in structural estimation (Hennessy & Whited 2007, Glover 2016, Strebulaev & Whited 2012 all use Compustat quarterly).
- The year-to-date structure of `oancfy` requires a simple differencing step: Q1 = `oancfy_Q1`; Q2 = `oancfy_Q2` − `oancfy_Q1`; Q3 = `oancfy_Q3` − `oancfy_Q2`; Q4 = `oancfy_Q4` − `oancfy_Q3`. This is well-documented and standard.
- Scaling by `atq` gives a stationary, comparable ratio across firms and time.
- For rolling-window MLE of μ_it, the Compustat quarterly panel provides sufficient depth (8–16 quarters per rolling window) for the majority of firms in the post-1993 era.

**Weaknesses / Gaps:**
- **The ibq + dpq alternative:** The sum `ibq + dpq` ("accounting cash flow") is available from earlier in the Compustat quarterly history (pre-1988) and is continuous. However, it mixes accruals with cash flows in a way that `oancfy` does not. The literature is split: Hennessy & Whited (2005) "Debt Dynamics" use `oancfy`-based measures; Bolton, Chen & Wang (2011) and many structural models use earnings-based measures. For your distributional approach (moment estimation of μ_it), `oancfy` is preferred because it represents actual cash flows rather than accrual-adjusted earnings — but at the cost of losing the pre-1988 sample.
- **Sample attrition from rolling-window MLE:** Requiring 8 consecutive quarters of data reduces the sample materially — firms with gaps or short histories are excluded. No published paper reports an exact fraction, but structural estimation papers typically document ~30–50% attrition relative to the raw panel when imposing 8+ quarter minimums and non-financial / non-utility restrictions. UNVERIFIED — user should confirm from their own data pull.
- **Year-to-date reporting:** Q4 `oancfy` is sometimes reported as annual cumulative; verify against `oancfy` in `comp.funda` for annual reconciliation.
- **Survivorship:** Compustat is survivor-bias-free for listed firms (includes delistings back to the data's inception).

**Standard Winsorization Convention:** 1%–99% by fiscal year is the standard in corporate finance panel data (VERIFIED from multiple empirical papers). Apply this to cash flow / assets ratios (μ_it moments) before the rolling-window MLE step.

**Connection to SMM Estimation:**
This component feeds the pre-SMM step: for each firm i in each rolling window t, estimate the parameters of the cash flow distribution μ_it by MLE on 8–16 quarterly observations of cash flow / assets. The resulting firm-quarter estimates (mean, variance, skewness if a flexible distribution is used) become the empirical moments or distributional objects to which the Wasserstein distance W1(μ_it, ν_t) is applied. The quality of μ_it estimation depends critically on having enough consecutive observations per firm — this is the primary data risk in Component A.

**UNVERIFIED — User Must Confirm:**
- Whether `oancfy` is available on Paris Dauphine's specific WRDS subscription (confirm by running `select count(*) from comp.fundq where oancfy is not null and datadate >= '1988-01-01'`).
- The exact fraction of firms with 8+ consecutive non-missing quarterly `oancfy` observations (run a survival analysis on your specific sample).
- Whether `oancfy` is reported gross or net of working capital changes in Compustat quarterly (check a few known firms against 10-Q filings).

---

## Component B: Leverage Outcomes

**Primary Dataset(s):** Compustat Quarterly (`comp.fundq`) merged with CRSP Monthly Stock File (`crsp.msf`) via CRSP/Compustat Merged (CCM) link table
**Provider:** S&P Global + CRSP via WRDS
**WRDS dataset path(s):**
- `comp.fundq` — balance sheet items (VERIFIED)
- `crsp.msf` — monthly stock prices (VERIFIED)
- `crsp.ccmxpf_lnkhist` — CCM link history table (VERIFIED from multiple academic sources)

**Key Variables:**

| Variable | Mnemonic | Description | Verified? |
|----------|----------|-------------|-----------|
| Long-term debt | `dlttq` | Long-term debt, total | VERIFIED (available from ~1970s) |
| Current portion of long-term debt | `dlcq` | Debt in current liabilities | VERIFIED (available from ~1970s) |
| Total assets | `atq` | Total assets | VERIFIED |
| Shares outstanding | `cshoq` | Common shares outstanding | VERIFIED |
| Stock price | `prccq` | Price at fiscal quarter close | VERIFIED |
| Book equity | `ceqq` | Common equity (book) | VERIFIED |
| CRSP permno | `lpermno` | CRSP permanent security ID (via CCM link) | VERIFIED |
| CCM link type | `linktype` | LC, LU, LS — standard filter | VERIFIED |
| CCM link primary indicator | `linkprim` | P or C — primary link | VERIFIED |

**Standard Variable Construction (VERIFIED from empirical corporate finance literature):**
- **Book leverage:** `(dlttq + dlcq) / atq`
- **Market leverage:** `(dlttq + dlcq) / (dlttq + dlcq + cshoq × prccq)`
- Note: `prccq` can be substituted with CRSP end-of-quarter price (`prc`) for cleaner measurement; the latter is preferred because Compustat sometimes carries stale prices.

**Coverage:**
- Time period: `dlttq` and `dlcq` are available from the early 1970s onward in quarterly data; coverage thins materially before 1980 for the cross-section. Reliable panel from ~1980. Market leverage requires CRSP merge, which begins in 1926 but has good quarterly coverage for NYSE/AMEX from the 1960s and NASDAQ from the 1970s.
- Geography: US and Canada
- Frequency: Quarterly
- Approximate observations: ~1 million firm-quarters for the full post-1980 panel

**Feasibility Grade: A**
- Entirely standard WRDS infrastructure; this is the most commonly constructed quantity in corporate finance.

**CCM Merge Conventions (VERIFIED):**
Standard filter: `linktype in ('LC','LU','LS') and linkprim in ('P','C')` applied together with date validity checks `linkdt <= datadate <= coalesce(linkenddt, '2099-12-31')`. The `ccmxpf_lnkhist` table (SAS macro library `crsp`) is the canonical link table for quarterly panel merges. Known reliability issues: (1) some firms have multiple valid links in overlapping periods — the `linkprim = 'P'` filter resolves most duplicates; (2) fiscal quarter end dates (Compustat `datadate`) must be matched to the appropriate calendar date before joining to CRSP monthly returns.

**Fiscal-Quarter-to-Calendar-Quarter Alignment:** This is a known issue documented in the literature. Firms with non-December fiscal year ends report their Q1/Q2/Q3/Q4 dates in different calendar months. Standard practice is to use `datadate` directly (Compustat's fiscal period end) and match to the nearest CRSP month-end price. Do not assume calendar quarter alignment — always use `datadate`.

**Treatment of Negative Book Equity (VERIFIED convention):** The dominant convention in empirical corporate finance and structural estimation is to **exclude** observations with negative book equity (`ceqq < 0`). Fama and French (1992) and virtually all subsequent leverage regressions exclude them. In the structural model context, negative equity corresponds to technical insolvency; these observations are outside the parameter space of standard trade-off models. The structural estimation literature (Hennessy & Whited 2007, Glover 2016) also excludes them.

**Strengths for this research design:**
- Both book and market leverage can be constructed; your SMM moments should target both (they have different noise properties).
- The quarterly frequency aligns with the rolling-window cash flow distribution estimation window.
- Long history enables testing whether W1(μ_it, ν_t) has stronger explanatory power in high-dispersion periods (recessions, credit crunches).

**Weaknesses / Gaps:**
- **Pre-1980 `dlttq` / `dlcq` coverage:** Coverage of long-term debt items in Compustat quarterly thins substantially before 1980. Using annual data (`comp.funda`) and interpolating for pre-1980 periods is possible but introduces measurement error. The clean sample effectively starts around 1980 for leverage, and 1988 for cash flows — the intersection dictates the estimation sample.
- **`prccq` staleness:** For inactive or thinly traded firms, Compustat's `prccq` can carry forward a stale price. Replacing with CRSP end-of-quarter closing price is recommended.
- **Financial and utility firms:** Standard practice (and structural model validity) requires excluding SIC codes 6000–6999 (financials) and 4900–4999 (utilities). These sectors have regulated capital structure.

**Connection to SMM Estimation:**
Book leverage (and/or market leverage) is the primary outcome variable. The SMM targets moments of the cross-sectional leverage distribution — mean, variance, and ideally higher-order moments — conditional on the Wasserstein distance W1(μ_it, ν_t). The cross-sectional heterogeneity in leverage is the empirical fact the model must replicate.

**UNVERIFIED — User Must Confirm:**
- Whether `dlcq` is consistently reported as "current maturities of long-term debt" or also includes short-term borrowings in your specific firm-quarters (spot-check against 10-Q notes for a few firms).
- Whether the CCM merge produces duplicates in your quarterly panel (run `count(distinct gvkey, datadate)` after merge and compare to before merge).

---

## Component C: Capital Supply Distribution (ν_t)

**Primary Dataset(s):** No single off-the-shelf dataset provides a cross-sectional distribution of capital supply. Three candidate approaches are documented below, ordered by feasibility.

**Provider:** FRED (Federal Reserve) / WRDS Bank Regulatory / WRDS Mergent FISD
**WRDS dataset path(s):**
- `bank_all` schema — WRDS Bank Regulatory (Call Reports, FR Y-9C) (VERIFIED as schema name; specific table names UNVERIFIED — require direct WRDS query)
- `fisd.fisd_mergedissue` — bond issuance amounts as proxy (VERIFIED schema.table)
- FRED series `BCNSDODNS` — aggregate-level only (VERIFIED series exists, quarterly from Q4 1945)

**Feasibility Grade: C**
- The distributional shape of ν_t is not directly observable in any standard WRDS dataset. Construction requires nontrivial aggregation choices with significant modeling implications.

---

### Approach C-1: Bond Issuance Cross-Section from Mergent FISD (RECOMMENDED FIRST ATTEMPT)

**Logic:** Each quarter t, observe the cross-section of bond issuance deals: their sizes (`offering_amt`) form an empirical distribution. Fit LogNormal(α_ν(t), σ_ν²) to this cross-section. This directly gives the parameters the SMM needs to estimate.

**Key Variables:**

| Variable | Mnemonic | Description | Verified? |
|----------|----------|-------------|-----------|
| Issuance amount | `offering_amt` | Face value at issuance (USD thousands) | VERIFIED (fisd.fisd_mergedissue) |
| Offering date | `offering_date` | Date of bond issuance | VERIFIED |
| CUSIP | `complete_cusip` | 9-digit bond identifier | VERIFIED |
| Maturity | `maturity` | Maturity date | VERIFIED |
| Coupon | `coupon` | Coupon rate | VERIFIED |
| Issue type | `bond_type` | CDEB, CMTN, CZ, etc. | VERIFIED |
| Issuer domicile | `country_domicile` | Filter for US (via fisd_mergedissuer) | VERIFIED |

**Coverage:**
- Time period: Most reliable from **1995** onward for US corporate bonds (VERIFIED from multiple library guides and academic usage). Pre-1995 coverage exists but is incomplete and heavily back-filled.
- Geography: US corporate bonds (filter `country_domicile = 'USA'` in `fisd_mergedissuer`)
- Frequency: Transaction-level (issuance date); aggregate to quarterly cross-section
- Approximate observations: 140,000+ bond issues in the full database

**Strengths:**
- Directly measures the supply side of capital markets from the bond issuer's perspective.
- `offering_amt` is naturally log-normal in cross-section (bond deal sizes follow power-law / log-normal distributions in practice).
- Available on standard WRDS access; same database used for Component D (credit spreads).
- Covers both investment grade and high yield (VERIFIED).

**Weaknesses:**
- Only captures public bond market capital supply; excludes bank loans (which dominate for smaller firms), private placements (Rule 144A), and equity issuance.
- Pre-1995 coverage is thin — this is a hard constraint if you want a 1988 start date.
- The number of issues per quarter varies substantially (thin in recessions), which affects the precision of MLE estimation of α_ν(t) and σ_ν.
- Conflates supply and demand: a large issuance could reflect high supply or high demand.

---

### Approach C-2: Bank-Level Loan Supply from Call Reports

**Logic:** Each quarter t, observe the cross-section of bank lending (new loans or total loan book) across FDIC-insured institutions. Fit LogNormal to the deal-size or loan-volume distribution.

**WRDS dataset path(s):** Schema `bank_all` on WRDS (VERIFIED as schema name). Known variable codes: `bhck2170` (total loans and leases, net), `bhck3210` (total assets) for FR Y-9C filers. Coverage from 1976 (commercial banks via Call Reports, FFIEC). Bank Holding Company (FR Y-9C) data available from 2001 on WRDS; raw FFIEC Call Report data (individual commercial banks) from 1976.

**Coverage:**
- Time period: 1976 onward (commercial banks, Call Reports); 2001 onward (BHC, FR Y-9C via WRDS Bank Regulatory Premium). VERIFIED.
- Geography: US chartered depository institutions
- Frequency: Quarterly

**Strengths:**
- Bank-level data provides a genuine cross-sectional distribution of lender size/supply.
- Long history back to 1976 — predates the Mergent FISD bond data.
- Captures the dominant form of corporate financing for smaller and mid-sized firms.

**Weaknesses:**
- **The conceptual mapping is imprecise:** Total bank loan book ≠ new capital supply to nonfinancial corporations in a given quarter. You would need Call Report Schedule RC-C (loan categories) to isolate commercial & industrial lending.
- Constructing a deal-size distribution from bank balance sheets requires assuming that loan portfolio size proxies for lending capacity, which is a strong assumption.
- WRDS Bank Regulatory Premium subscription required for BHC data; confirm Paris Dauphine has access.
- Specific table names within `bank_all` schema are UNVERIFIED — user must query WRDS data dictionary.

---

### Approach C-3: Z.1 Aggregate Series (Fallback / Robustness)

**FRED Series:** `BCNSDODNS` — Nonfinancial Corporate Business; Debt Securities and Loans; Liability, Level (quarterly, from Q4 1945). VERIFIED.

**Logic:** Use aggregate credit availability as a single-moment proxy for ν_t. Parameterize α_ν(t) as a deterministic function of `log(BCNSDODNS_t)` and treat σ_ν as a free structural parameter estimated by SMM. This collapses the distribution identification to a much simpler problem but sacrifices the cross-sectional richness that motivates the paper.

**Feasibility Grade: B** (for this specific fallback use only)

**Weaknesses:** This approach does not provide the cross-sectional variance of ν_t (σ_ν) from data — σ_ν is estimated entirely through model moment-matching. This is defensible in a structural paper but must be clearly stated as a maintained assumption.

---

### Note on Literature Precedent for ν_t

A search of the academic literature found **no existing paper** that directly constructs and uses a cross-sectional distribution of capital supply (ν_t) the way this paper proposes. The concept of lender heterogeneity is studied (Jimenez et al., ECB Working Papers, Abad et al. 2025), but these papers focus on pass-through rates, not on fitting a parametric distributional shape to aggregate lending flows. This is a genuine methodological novelty and will require careful justification of the ν_t construction choice. This novelty is both a strength (contribution) and a risk (referee scrutiny).

**UNVERIFIED — User Must Confirm:**
- Whether Paris Dauphine's WRDS subscription includes the Bank Regulatory Premium tier (required for FR Y-9C BHC data).
- Specific table names within `bank_all` schema for quarterly loan data (query WRDS data dictionary at `/data-dictionary/bank_all/`).
- Whether Mergent FISD `offering_amt` has sufficient quarterly density (number of deals per quarter) for stable LogNormal MLE — especially pre-2000. Minimum ~20–30 deals per quarter recommended for stable two-parameter MLE.

---

## Component D: Credit Spreads at Issuance (for identification of κ)

**Primary Dataset(s):** Mergent FISD (primary) + DealScan (secondary for bank loan spreads)
**Provider:** LSEG Mergent via WRDS (FISD); LSEG/Thomson Reuters via WRDS (DealScan)
**WRDS dataset path(s):**
- `fisd.fisd_mergedissue` — bond-level issuance characteristics (VERIFIED)
- `fisd.fisd_mergedissuer` — issuer-level information (VERIFIED)
- `fisd.fisd_ratings` — credit ratings (VERIFIED)
- TRACE: `trace_standard` and `trace_enhanced` (VERIFIED schema names from WRDS FINRA page) — **secondary market only**
- DealScan: Schema `lpc` likely; exact table names UNVERIFIED — user must confirm via WRDS

**Key Variables (Mergent FISD):**

| Variable | Mnemonic | Description | Verified? |
|----------|----------|-------------|-----------|
| Yield at issuance | `offering_yield` | Yield to maturity at offering | UNVERIFIED (variable name inferred from documentation; confirm in WRDS data dictionary) |
| Yield spread at issuance | `offering_spread` OR derived | Spread over Treasury at issuance | UNVERIFIED (may require user to compute as `offering_yield` minus matched Treasury yield) |
| Issuance amount | `offering_amt` | Face amount issued (USD thousands) | VERIFIED |
| Offering date | `offering_date` | Date of public offering | VERIFIED |
| Maturity | `maturity` | Final maturity date | VERIFIED |
| Credit rating at issuance | See `fisd.fisd_ratings` | Moody's / S&P / Fitch ratings | VERIFIED (table exists) |
| Bond type | `bond_type` | CDEB (straight corporate), CMTN, CZ, USBN, etc. | VERIFIED |
| Convertible flag | (filter variable) | Exclude convertibles | UNVERIFIED (variable name) |
| Seniority | `security_level` | Senior, subordinated, etc. | UNVERIFIED (variable name) |
| CUSIP | `complete_cusip` | 9-digit identifier | VERIFIED |
| Issuer ID | `issuer_id` | Links to `fisd_mergedissuer` | VERIFIED |

**Coverage:**
- Time period: **Most reliable from 1995 onward** for US corporate bonds (VERIFIED from multiple sources). The WRDS vendor page shows database date range technically back to 1800 but this reflects government/agency bonds. Practical corporate bond coverage that is adequate for academic research starts ~1995.
- Geography: US (filter `country_domicile = 'USA'` in `fisd.fisd_mergedissuer`)
- Frequency: Transaction-level (offering date); aggregate to deal-level
- Approximate observations: 140,000+ bonds in the full database; roughly 60,000–80,000 US corporate bonds with sufficient data for spread calculation
- Covers both IG and HY: VERIFIED (the database covers "investment grade, high yield and convertible debt")

**Feasibility Grade: B**
- Accessible with moderate cleaning effort; the main challenge is constructing the spread variable (offering yield minus matched-maturity Treasury) and linking to Compustat via CUSIP-to-GVKEY crosswalk.

**TRACE — Secondary Market Only (VERIFIED):** TRACE captures OTC secondary market transactions for all publicly traded corporate bonds starting July 2002. It is NOT a primary market database — it does not contain offering yields at issuance. New issues appear in TRACE the day after they begin secondary market trading. TRACE is valuable for observing secondary spreads over the bond's life but cannot directly provide credit spreads at issuance for identification of κ. Do not use TRACE as a substitute for Mergent FISD for the issuance spread moment.

**Strengths for this research design:**
- Mergent FISD `offering_yield` (if confirmed) provides the credit spread at issuance — the cleanest empirical moment for identifying bankruptcy cost κ in a structural capital structure model.
- The cross-section of bond issuance spreads by rating, maturity, and time period directly maps to model-implied default risk pricing.
- Papers using structural models to identify bankruptcy costs (Glover 2016; Bhamra, Kuehn & Strebulaev 2010 RFS) match to credit spread data — Bhamra et al. (2010) use the Baa-Aaa spread (available from FRED as a long series); Glover (2016) targets leverage and default rates rather than credit spreads directly. For your SMM design, using issuance-level spreads from Mergent FISD is an improvement over aggregate indices.
- DealScan provides bank loan spreads (all-in drawn spread over LIBOR) for the loan market — important if you want to capture non-bond capital supply for κ identification.

**DealScan (Bank Loans):**
- Coverage: **1988 onward** (detailed), with selected data back to 1981. VERIFIED.
- WRDS schema: Likely `lpc` (Loan Pricing Corporation); exact table names (loan, facility, borrower) UNVERIFIED — user must confirm in WRDS.
- Key variable: **All-in drawn spread** (spread over LIBOR, including annual fees) — this is the standard variable used in the bank loan literature. VERIFIED as the standard measure.
- Compustat link: Use Chava & Roberts (2008, JF) link table between DealScan and Compustat (available separately; not built into WRDS CCM).
- Feasibility Grade: B — requires the Chava-Roberts link file and separate data pull.

**Known Data Quality Issues (Mergent FISD):**
- **Offering yield** may not always be populated for all issues; some bonds report only coupon, not offering yield. When offering yield is missing, researchers typically back out yield from offering price (when available) or use the coupon as a proxy — the latter introduces measurement error.
- Pre-1995 coverage is sparse and potentially back-filled; caution with pre-1995 spread data.
- Some MTN (medium-term note) programs report aggregate shelf amounts rather than individual deal sizes, which inflates `offering_amt` for individual tranches.
- **UNVERIFIED:** Whether `offering_yield` is the exact variable name in `fisd.fisd_mergedissue` or whether it is stored differently (e.g., derived from `offering_price` and coupon). User must check WRDS data dictionary at `/data-dictionary/fisd_fisd/`.

**Capital IQ via WRDS:** WRDS does offer Capital IQ Capital Structure data. It covers debt capital structure for 60,000+ global companies, including bond yield, offering price, offering date, maturity, ratings at issuance. The WRDS dataset name is UNVERIFIED — user should check under the "Capital IQ" section on the WRDS platform. This could serve as a cross-check against Mergent FISD for issuance yield coverage.

**Connection to SMM Estimation:**
The key SMM moment for identifying κ (bankruptcy cost) is the level and cross-sectional dispersion of credit spreads at issuance, conditional on firm leverage and risk characteristics. In the model, κ shifts the default boundary and affects the pricing of risky debt — higher κ → higher spreads for a given leverage ratio. Matching the empirical distribution of issuance spreads from Mergent FISD to model-implied spreads is the cleanest identification strategy. If offering yield is missing for too many bonds, a fallback is to use the ICE BofA OAS indices (Component E) as time-series aggregate moments instead.

**UNVERIFIED — User Must Confirm:**
- Exact variable name for offering yield in `fisd.fisd_mergedissue` — run `describe fisd.fisd_mergedissue` or check data dictionary.
- Fraction of US corporate bonds in Mergent FISD with non-missing `offering_yield` (or equivalent).
- Whether Paris Dauphine's WRDS subscription includes DealScan (LPC) — check under LSEG subscriptions.
- Exact DealScan schema.table names — likely `lpc.deal`, `lpc.facility`, `lpc.borrower` but UNVERIFIED.

---

## Component E: Controls and Macro Variables

**Primary Dataset(s):** FRED (Federal Reserve Bank of St. Louis) + Compustat Quarterly (firm-level controls)
**Provider:** FRED (free, no WRDS required); S&P Global via WRDS (Compustat)
**WRDS dataset path(s):** `comp.fundq` for firm controls; FRED API for macro series

**FRED Series (all VERIFIED as correct series codes):**

| Series | Code | Description | Start Date | Frequency |
|--------|------|-------------|------------|-----------|
| 3-Month T-Bill | `TB3MS` | Secondary market rate, discount basis | 1934-01-01 | Monthly |
| 10-Year Treasury | `GS10` | Constant maturity yield | 1953-04-01 | Monthly |
| IG Corporate OAS | `BAMLC0A0CM` | ICE BofA US Corporate Index OAS (all ratings) | 1996-12-31 | Daily |
| HY Corporate OAS | `BAMLH0A0HYM2` | ICE BofA US High Yield Index OAS | 1996-12-31 | Daily |
| VIX | `VIXCLS` | CBOE Volatility Index, daily close | 1990-01-02 | Daily |
| Real GDP | `GDPC1` | Real Gross Domestic Product, chained 2017 dollars | 1947-01-01 | Quarterly |
| Nonfinancial Corp. Debt | `BCNSDODNS` | Z.1 nonfinancial corporate debt securities and loans | Q4 1945 | Quarterly |

**Important caveat on BAMLC0A0CM and BAMLH0A0HYM2:** As of April 2026, FRED distributes only a rolling 3-year window of these daily series (approximately 2023–present via FRED). Pre-2023 history for these OAS series is now available directly from ICE Data Indices (which requires a separate data agreement). This is a material coverage gap for historical research. Workaround: Use the St. Louis FRED ALFRED (Archival Federal Reserve Economic Data) which may retain historical vintages, or access ICE directly. UNVERIFIED — user should confirm current availability through Paris Dauphine's data licenses.

**Firm-Level Controls (from `comp.fundq`):**

| Variable | Mnemonic | Description | Verified? |
|----------|----------|-------------|-----------|
| Property, plant & equipment | `ppentq` | Net PP&E (tangibility proxy) | VERIFIED |
| Operating income before D&A | `oibdpq` | EBITDA proxy (profitability) | VERIFIED |
| Common shares outstanding | `cshoq` | For market cap calculation | VERIFIED |
| Stock price (quarter close) | `prccq` | Quarter-end price | VERIFIED |
| Total assets | `atq` | Firm size | VERIFIED |
| R&D expenditure | `xrdq` | R&D (growth options proxy) | VERIFIED |

**Coverage of Firm-Level Controls:**
- `ppentq`, `oibdpq`, `atq`, `cshoq` are available from at least 1980 in the quarterly database. VERIFIED from documented usage in the capital structure literature.
- `xrdq` has substantial missing data (many firms do not report R&D); standard practice is to set to zero when missing (UNVERIFIED convention — confirm with your referee strategy).
- `prccq` staleness caveat applies — see Component B.

**Feasibility Grade: A** (FRED series, Compustat controls)
**Feasibility Grade: C** (ICE BofA OAS series for historical period — access now restricted)

**Strengths for this research design:**
- `GDPC1` (quarterly) and `TB3MS` (monthly, aggregate to quarterly) provide the standard macro cycle controls.
- `BAMLC0A0CM` and `BAMLH0A0HYM2` (when accessible) provide time-varying credit market conditions that are natural instruments or controls for the aggregate capital supply distribution ν_t.
- VIX from 1990 covers most of the SMM estimation window.

**Weaknesses / Gaps:**
- The ICE BofA OAS series access issue (post-2026 FRED rolling window) is a real constraint. For the 1997–2022 historical OAS data, the researcher will need to either (a) obtain historical data from ICE directly, (b) use Moody's Baa-Aaa spread (FRED series `BAA` minus `AAA`, available from 1919) as a long-history alternative, or (c) use Bloomberg (if available). The Baa-Aaa spread alternative: FRED `BAA` (Moody's Baa Corporate Bond Yield) and `AAA` (Moody's Aaa) are available from 1919 and 1949 respectively, and their difference is a widely used credit risk proxy.
- `VIXCLS` only starts in 1990 — this is fine given the recommended sample start of 1988, with VIX entering as a control from 1990.

**Connection to SMM Estimation:**
Macro variables serve as (a) controls in the reduced-form leverage regressions that establish the W1 result, (b) conditioning variables for the structural SMM moments (time-varying components of α_ν(t)), and (c) instruments or robustness checks for ν_t dynamics. `BCNSDODNS` is the most natural aggregate-level proxy for the scale of capital supply and can be used to parameterize α_ν(t) in Approach C-3.

**UNVERIFIED — User Must Confirm:**
- Current FRED availability of `BAMLC0A0CM` and `BAMLH0A0HYM2` for the 1997–2022 period — check whether Paris Dauphine has a Bloomberg or ICE data subscription.
- Whether `GDPC1` real GDP (quarterly) is appropriate or whether GDP deflator-adjusted nominal series is preferred for the model's time period normalization.

---

## Recommended Data Stack

**Primary sample period: 1988 Q1 — 2024 Q4** (constrained by SFAS 95 cash flow data availability)

**For leverage and cash flow distributions (Components A + B):**
1. Pull `comp.fundq` for all US firms, filter to non-financial (SIC not 6000–6999) and non-utility (SIC not 4900–4999) firms.
2. Merge with CCM link table (`crsp.ccmxpf_lnkhist`) using `linktype in ('LC','LU','LS')` and `linkprim in ('P','C')` to get CRSP `permno`.
3. Construct `oancfy` quarterly flows by differencing year-to-date values within fiscal year.
4. Scale cash flows by `atq`; winsorize at 1%–99% by fiscal year.
5. Require minimum 8 consecutive non-missing quarterly observations per firm-rolling-window for μ_it MLE.
6. Compute book leverage = `(dlttq + dlcq) / atq`; market leverage using CRSP prices.
7. Exclude observations with `atq <= 0` or `ceqq < 0` (negative equity).

**For capital supply distribution (Component C):**
1. **First attempt:** Pull `fisd.fisd_mergedissue` joined to `fisd.fisd_mergedissuer` where `country_domicile = 'USA'` and `bond_type in ('CDEB','CMTN','CMTZ','CZ','USBN')`. Aggregate `offering_amt` by `offering_date` quarter. Fit LogNormal(α_ν(t), σ_ν) by quarter. Require minimum 20 deals per quarter for stable fit.
2. **If quarterly bond counts are too sparse (especially pre-2000):** Use 4-quarter rolling windows to estimate quarterly ν_t parameters.
3. **Sensitivity check:** Re-estimate with bank-level loan data (`bank_all` on WRDS) using total C&I loans per bank per quarter.
4. **Aggregate fallback:** Parameterize α_ν(t) = f(log BCNSDODNS_t) and estimate σ_ν via SMM.

**For credit spreads (Component D):**
1. Pull `fisd.fisd_mergedissue` with `offering_date >= 1995-01-01`, filter to US corporate straight debt.
2. Compute issuance spread = `offering_yield` minus matched-maturity on-the-run Treasury yield (from `GS10`, `GS5`, `GS2` on FRED or H.15 release).
3. Link to Compustat via CUSIP-to-GVKEY crosswalk (WRDS provides this through the CCM bond linking table).
4. For loan spreads: Pull DealScan `lpc` schema, extract all-in drawn spread, link via Chava-Roberts crosswalk.

**For controls (Component E):**
1. Download `TB3MS`, `GS10`, `GDPC1`, `VIXCLS` from FRED API (free, no WRDS needed).
2. For ICE BofA OAS: Access historical series from ICE or use Moody's Baa-Aaa spread (`BAA` minus `AAA` from FRED) as a long-history proxy.
3. Merge Compustat firm-level controls (`ppentq`, `oibdpq`, `cshoq × prccq`) from `comp.fundq`.

---

## Critical Gaps

1. **Component C is the structural hole:** There is no standard dataset that directly provides the cross-sectional distribution of capital supply ν_t. Every candidate approach (Mergent FISD bond issuance, Call Reports, Z.1 aggregate) has serious measurement limitations. The paper must devote explicit section space (likely a Data Appendix) to justifying the choice and presenting sensitivity across approaches. This is not a showstopper — it is a methodological contribution — but it requires explicit defense.

2. **Sample period conflict:** Cash flows (Component A) start cleanly in 1988 due to SFAS 95. Credit spreads (Component D) start reliably in 1995 from Mergent FISD. Bond issuance distribution (Component C) is thin before 2000. The SMM estimation sample may effectively be **1995–2024** for the fully identified model, which gives approximately 29 years of quarterly data — sufficient for SMM but shorter than the full leverage panel.

3. **ICE BofA OAS historical access (Component E):** The rolling-window FRED restriction on `BAMLC0A0CM` and `BAMLH0A0HYM2` is a real constraint for historical analysis. If Paris Dauphine does not have Bloomberg or ICE direct access, use Moody's Baa-Aaa spread as the primary credit market control.

4. **ν_t identification within SMM:** The LogNormal parameters (α_ν, σ_ν) for ν_t are estimated jointly with bankruptcy cost κ inside the SMM. If ν_t is pre-estimated outside the SMM loop (from bond issuance data), identification of (α_ν, σ_ν) comes from the distribution of deal sizes — but the model's link between deal size distribution and the supply of capital available to a given firm is not tight. This is a potential referee objection: "Why is the bond deal size distribution the right measure of capital supply to firm i?" The paper needs a theoretical justification.

5. **TRACE limitation for κ identification:** TRACE is secondary market only (post-2002). For primary market credit spreads (the natural identification moment for κ), TRACE is not useful. Mergent FISD is the correct source. Do not conflate the two databases.

---

## Verification Checklist

Items the user must personally verify on WRDS before beginning data construction:

- [ ] **Confirm `oancfy` density:** Run `select count(*) from comp.fundq where oancfy is not null and datadate between '1988-01-01' and '2024-12-31'` on WRDS. Confirm the variable exists and has reasonable coverage.
- [ ] **Confirm `fisd.fisd_mergedissue` offering yield variable name:** Run `describe fisd.fisd_mergedissue` or equivalent in the WRDS query interface. Identify the correct variable name for yield at issuance (may be `offering_yield`, `offeringprice`, or derived). Check what fraction is non-missing.
- [ ] **Confirm quarterly deal counts in Mergent FISD:** For Component C, count the number of US corporate bond issuances per quarter from `fisd.fisd_mergedissue` with `offering_date` between 1995 and 2024. Minimum ~20 deals/quarter required for stable LogNormal fit.
- [ ] **Confirm `bank_all` schema tables:** On WRDS, run `show tables in bank_all` or access the data dictionary at `wrds-www.wharton.upenn.edu/data-dictionary/bank_all/`. Identify the quarterly Call Report tables for C&I loans.
- [ ] **Confirm DealScan subscription:** Check whether Paris Dauphine's WRDS subscription includes the `lpc` (DealScan) library. If so, identify the facility-level table with all-in drawn spread.
- [ ] **Confirm ICE BofA OAS access:** Check whether FRED `BAMLC0A0CM` and `BAMLH0A0HYM2` provide pre-2023 history or whether an alternative source (Bloomberg, ICE direct) is needed.
- [ ] **Confirm CCM merge completeness:** After merging `comp.fundq` with `crsp.ccmxpf_lnkhist`, check that the merge does not introduce substantial duplicates (>5% of firm-quarters). If duplicates exist, apply additional `linkprim` filtering.
- [ ] **Confirm negative equity sample size:** Run `select count(*) from comp.fundq where ceqq < 0 and datadate >= '1988-01-01'` to understand the fraction of firm-quarters excluded by the negative equity filter.
- [ ] **Confirm `dlttq` and `dlcq` coverage pre-1990:** For the pre-1990 sample, run coverage statistics on both variables to assess whether the leverage panel is thin before 1988.
- [ ] **Confirm Capital IQ coverage on WRDS:** Check whether Paris Dauphine's WRDS subscription includes Capital IQ Capital Structure data as a potential cross-check for bond issuance yields.

---

*Report prepared by: Data Quality Surveyor agent*
*Assessment scope: Distributional Debt Capacity — SMM estimation of W1(μ_it, ν_t) and leverage heterogeneity*
*Web searches conducted: 2026-06-13*

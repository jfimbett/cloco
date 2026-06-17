# Data Exploration Report — Liquid Assets

**Generated:** 2026-03-29  
**Dataset:** `clean_data_final.parquet` (or fallback `clean_data_mixed_lots.parquet`)

---

## 1. What the Dataset Contains

The master dataset has **1,068,703 rows and 78 columns**. It covers auction lots from three French wine regions (Bordeaux, Burgundy, Rhone) sold between **1996-01-01** and **2015-12-16** at the major international auction houses (Christie's, Sotheby's, Zachys, TCWC, Acker Merrall & Condit, Hart Davis Hart, Bonhams, Artcurial and others).

| Variable group | Coverage |
|----------------|----------|
| Region         | Bordeaux 58.9%, Burgundy 31.2%, Rhone 9.9% |
| Date           | 100% complete; range 1996–2015 |
| Vintage        | ~100% complete |
| Producer/Maker | 94.8% complete; NOT standardised |
| Price (P_$/Bt_Combi) | 100% complete |
| Age (years)    | 100% complete |
| Size           | 100% complete |
| Wine ratings   | 0.2%–0.6% complete per rater |

---

## 2. Canonical Price Variable

**Use `P_$/Bt_Combi` as the canonical per-bottle price.**

### All price-related columns

| Column | Level | Coverage | Notes |
|--------|-------|----------|-------|
| `P_$`              | Lot total (USD) | 100% | NOT per bottle; P_$ = P_$/Bt_Combi * Qty |
| `P_Loc`            | Lot total (local) | 100% | Same as P_$ but in local currency |
| `Hammer_$_Combi`   | Lot total (USD) | 75.3% | Combined Hammer_$ + Ham_$; missing ~25% |
| `Hammer_Loc_Combi` | Lot total (local) | 75.5% | Combined hammer in local currency |
| `HP_$/Bt_Combi`    | Per bottle (USD) | 90.9% | Hammer price; 9.1% missing |
| `P_$/Bt_Combi`     | **Per bottle (USD)** | **100%** | **USE THIS: always populated** |
| `Esti_$_Low_Combi` | Per lot, low estimate | 49.7% | Pre-auction estimate |
| `Esti_$_High_Combi`| Per lot, high estimate | 49.7% | Pre-auction estimate |
| `P_$/Standard_size`| Per standard 750ml | 31.2% | Normalises large-format bottles |
| `HP_$/Standard_BT` | Per standard 750ml | 9.9% | Limited coverage |

### Justification for `P_$/Bt_Combi`

- **100% non-null** across all 1,068,703 rows
- Median: USD 184.34, Max: USD 310,700.0  
- Lucie's f2_some_ml.py renames this column 'Price per Bottle' for all analysis
- `P_$` is the lot-level total (confirmed: P_$ = P_$/Bt_Combi × Qty in 100% of cases)
- `HP_$/Bt_Combi` is the hammer price per bottle (90.9% complete) and is the
  alternative if the hammer vs. total-price distinction matters

### P_Loc / P_$ conflict note

Lucie's `data_work.txt` (Q9a/9b) flags that `P_Loc` and `P_$` have values that
conflict with `Hammer_Loc_Combi` and `Hammer_$_Combi` on some rows.
`P_$` and `P_Loc` appear to be lot-level totals from one source of the auction data,
while `Hammer_$_Combi` and `Hammer_Loc_Combi` come from a second source.
The combined variable `P_$/Bt_Combi` (which divides P_$ by Qty) is 100% complete
and is the safest choice for per-bottle analysis.

---

## 3. Canonical Producer/Wine Name Variables

**Primary producer variable: `Producer/Maker` (94.8% complete, NOT standardised).**
**Primary wine-name variable: `For Matching` (41.1% complete; most consistent).**

### All identity columns

| Column | Coverage | Unique values | Notes |
|--------|----------|---------------|-------|
| `Producer/Maker` | 94.8% | ~varies | Primary; Lucie's pipeline left unstandardised |
| `Ori Producer Nm` | ~0% | — | Dropped in cleaning (no values) |
| `Producer Dummy`  | 8.0% | — | Lowercased producer name from one data source |
| `Producer`        | 2.2% | — | Sparse; partial third source |
| `WineNm`          | 2.1% | — | Very sparse |
| `Wine Nm`         | 5.6% | — | Second wine name field |
| `Wine_Nm`         | 0.7% | — | Very sparse |
| `Item_Nm`         | 9.9% | — | Full description from one source |
| `LotNm1`          | 31.2% | — | First token of lot name (often wine name) |
| `Lot Nm`          | 58.9% | — | Lot name; most complete alternative |
| `For Matching`    | 41.1% | — | Curated for Duc's URL matching; uppercase tokens |
| `Wine Vintage Pair` | 31.2% | — | Full canonical description (GPT-assisted) |

### Recommendation

- Use `Producer/Maker` for producer fixed effects (94.8% coverage).
- Use `Lot Nm` or `LotNm1` for wine-level analysis when producer names are needed.
- Standardisation of producer names is an **open task** (flagged in data_work.txt).
  This is a prerequisite for producer-level fixed effects in the final regressions.

---

## 4. Age Variable Recommendation

**Use recomputed Age in quarters for the main regression:**

```python
vintage_anchor = pd.to_datetime(df['Vintage'].astype(int).astype(str) + '-06-30')
df['Age_q'] = (4 * (df['Date'] - vintage_anchor).dt.days / 365.25).clip(lower=0).astype(int)
```

### Why not use the parquet's `Age` column?

- The parquet `Age` is `Date.year - Vintage` (integer years).
  This is coarse and does not account for the sale month.
- Lucie's `data_work.txt` explicitly notes: *'VARIABLE DATE NEEDS TO BE CHECKED
  AGAIN and variable age might need to be updated'*.
- `f2_some_ml.py` recomputes Age in quarters using June 30 as the vintage anchor
  (the wine is assumed bottled at the end of Q2 of the vintage year).
- The Stata specification uses `agequarters`, confirming that quarters is the
  convention used for all published regressions.

Age range (recomputed quarters): 0.0 to 917.2457221081451 quarters (0 to 229 years)

Age range in the parquet column (years): 0.0 to 229.0

Rows with Age > 100 years in parquet: 2,123

---

## 5. Data Quality Issues

| Issue | Count | Recommendation |
|-------|-------|----------------|
| Mixed-lot flagged rows | 12,668 (1.19%) | See `Excluded_Lots` |
| True mixed lots (exclude from price analysis) | 1,948 (0.18%) | Drop rows where Excluded_Lots = 1 |
| Age > 100 years in parquet | 2123 | Recompute Age_q; cap at reasonable max |
| Producer/Maker missing | 5.2% (~55,567 rows) | Cannot use for producer FE |
| Wine ratings present | 0.2%–0.6% | Ratings are too sparse for main analysis |
| P_Loc / P_$ vs Combi conflict | Unresolved (Lucie Q9) | Use P_$/Bt_Combi (100% complete) |
| Class column | NOT standardised | See proposed dict in data_work.txt Q3 |
| Date range | 1996–2015 | No post-2015 data; China shock period covered |

### Duc's two large CSVs (Wine_Maturity(Rep_1).csv and Wine_data(Rep2).csv)

These files (514 MB and 491 MB) contain the **same 78 columns** as the master parquet
plus extra columns: a `Link` column with tastingbook.com URLs (already matched via
`Matching.R`), and a `Year (corrected?)` column in Rep_1. Both are essentially CSV
exports of the auction data **after** Duc added URL matches — NOT a separate data source.

Key finding: the `Link` column in these CSVs appears to overlap with `matched_url`
in `output_with_matches.parquet`.

### Xin Ning's data.xlsx (extracted from Wine data_Xin Ning.zip)

Contains **15,902 rows** of tastingbook.com 'When to drink' data for **602 producers**
(Bordeaux producers only). Columns: `url`, `year`, `year_url`, `When to drink`,
`Country ranking`, `Producer ranking`, `Decanting time`, `Food Pairing`.
This is the maturity data needed for the structural model and DiD.
Coverage of ~602 Bordeaux producers is much broader than Duc's 6-producer scraping.

### URL matching coverage (output_with_matches.parquet)

Duc's R script matched **18,431 rows** out of 1,068,703 (1.7%) to tastingbook URLs.
Only 6 producers were included in the matching pool (Armand Rousseau, Romanee Conti,
Comtes Lafon, Pere & Fils, Georges de Vogue + Scraped_Links.xlsx).
Xin Ning's data provides much broader maturity data and should be merged via `year_url`.

---

## 6. The Bimodal Pattern

The core finding of the paper is a **bimodal age-price profile**:
wine prices first rise as the wine ages, reach a first peak early,
then dip (the 'trough') before rising again to a second, higher peak.

The trough and second peak are consistent with a market where
consumers (who want the wine at its maturity peak) exit the market,
leaving it to investors/collectors (who value aged wines for other reasons).

| Region | Trough (years) | Second peak (years) |
|--------|---------------|---------------------|
| Bordeaux | ~10.2 | ~100.0 |
| Burgundy | ~10.2 | ~94.0 |
| Rhone | ~10.2 | ~53.8 |

The Chow test at age=120 quarters (~30 years) in `f2_some_ml.py` confirms a
structural break in the price-age relationship at that point.

See `output/figures/price_age_profile.pdf` for the visual.

---

## 7. Files Needed for the Pipeline

| File | Status | Action |
|------|--------|--------|
| `old/RALucie/wine/parquet/clean_data_mixed_lots.parquet` | Present, 94 MB | This IS the master dataset |
| `old/RADuc/clean_data_mixed_lots.parquet` | Present, identical | Duplicate; use Lucie's version |
| `old/RADuc/output_with_matches.parquet` | Present, 62 MB | 1.7% coverage; use with Xin Ning data |
| `old/in vino veritas/Auction data/Bordeaux*.xlsx` | Present | Source for 00_xlsx_to_parquet.py |
| `Wine data_Xin Ning.zip` (data.xlsx) | Present | 15,902 maturity rows; extract and merge |

---

*Report generated by `code/analysis/03_data_exploration.py`*
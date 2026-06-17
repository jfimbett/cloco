# Project State: Liquid Assets
**Audit Date:** 2026-03-29
**Auditor:** Claude (onboard-ra skill)
**Project:** Bimodal price-age relationship in fine wine auctions; heterogeneous buyer types (consumption vs. collector/investor)
**Authors (alphabetical):** Imbet (Paris Dauphine-PSL), Kräussl (Bayes Business School), Piatti (QMUL), Steri (U. Luxembourg)

---

## 1. Executive Summary

The repository contains the accumulated work of three sequential RA generations (Lucie Bourdychova, Duc/unnamed, Xin Ning) plus the lead author's own exploratory analysis, all stored under `old/`. There is no `paper/`, `code/`, or `data/` directory at the project root — everything is in `old/`. The most important deliverable is a cleaned auction dataset (`clean_data_mixed_lots.parquet`, ~94 MB, present in three near-identical copies) that serves as the master input for all downstream analysis. The data pipeline is partially documented and partially reproducible: Lucie's cleaning scripts are the most complete, but several open questions from her `data_work.txt` were never resolved. Duc's contributions consist of a URL-matching R script and two large raw CSV files (~491 MB and ~514 MB); both contain critical quality issues documented below and must be independently verified before use. Xin Ning's contribution is a small producer-list extraction script. The most recent analytical code (`f2_some_ml.py`, `specification.do`, `petrus_analysis.py`) establishes the core empirical pattern (bimodal age-price profile) and runs a preliminary Callaway-Sant'Anna DiD on Petrus, but no results have been incorporated into a paper draft. A theory note (`case3.tex`/`case3.pdf`) for the structural model exists and is authored under "KPSV" (Kräussl, Piatti, Steri + one other). The project is at an early empirical exploration stage: data is cleaned, the bimodal pattern is documented, but there is no paper draft in this repository.

---

## 2. Directory Map

```
cloco-wine/
├── CLAUDE.md                          # Project instructions
├── README.md                          # Template readme (generic, not project-specific)
├── .gitignore
├── .env.example
│
├── memory/
│   ├── MEMORY.md                      # Generic workflow learnings
│   └── project_liquid_assets.md      # Key project facts (authors, RAs, core finding)
│
├── quality_reports/
│   ├── research_spec_liquid_assets.md # Full research specification (written 2026-03-29)
│   └── session_logs/                  # One session log entry
│
├── output/                            # JUST CREATED — was empty before this audit
│
├── .claude/                           # Agent/skill infrastructure (not project content)
│   ├── agents/                        # 15 agent definition files
│   ├── skills/                        # 30+ skill SKILL.md files
│   ├── hooks/                         # 8 hooks (Python)
│   ├── rules/                         # 20 rule files
│   └── lessons/LESSONS.md
│
└── old/                               # ALL PRIOR WORK LIVES HERE
    ├── Wine data_Xin Ning.zip         # 2 MB zip — content unknown (not extracted)
    │
    ├── RADuc/                         # ⚠️ VERIFY (Duc's work)
    │   ├── README.txt                 # Method doc: URL matching via Octoparse + R
    │   ├── Matching.R                 # R script: match wine rows to tastingbook URLs
    │   ├── test.py                    # Quick Bordeaux filter / vintage inspection
    │   ├── Code for Producer list.py  # Extract unique producers from parquet [Xin Ning]
    │   ├── clean_data_mixed_lots.parquet  # 94 MB — copy of master cleaned data
    │   ├── output_with_matches.parquet    # 62 MB — result of URL matching
    │   ├── Wine_Maturity(Rep_1).csv   # 514 MB — raw data (Replication 1) ⚠️
    │   ├── Wine_data(Rep2).csv        # 491 MB — raw data (Replication 2) ⚠️
    │   └── Links by producers/        # Excel files with scraped tastingbook URLs
    │       ├── Scraped_Links.xlsx
    │       ├── Armand_Rosseau.xlsx
    │       ├── Romanee_Conti.xlsx
    │       ├── Pere_Fils.xlsx
    │       ├── Comtes _Lafon.xlsx
    │       └── Georges_de_Vogue.xlsx
    │
    ├── RALucie/                       # Lucie Bourdychova's work (reliable)
    │   └── wine/
    │       ├── f00_settings.py        # ⚠️ EXPOSED API KEY — OpenAI key hardcoded
    │       ├── f1_data_cleaning.py    # Data cleaning pipeline v1 (uses OpenAI)
    │       ├── f1_data_cleaning_final.py  # Data cleaning pipeline FINAL (no OpenAI)
    │       ├── mixed_lots_finding.py  # Identify mixed lots via text mining
    │       ├── f2_some_ml.py          # Exploratory analysis + hedonic regression
    │       ├── petrus_analysis.py     # Petrus-only DiD: maturity as treatment
    │       ├── wordcloud.py           # Text exploration (Dec, Desc, Tasting Notes)
    │       ├── NLP_model.py           # BERT embedding on descriptions
    │       ├── scrape_wine_data.py    # Scrape tastingbook for Petrus vintage data
    │       ├── utils.py               # Bottle size converter (convert_to_liters)
    │       ├── specification.do       # Stata: reghdfe price on age + maturity
    │       ├── did_petrus.do          # Stata: csdid DiD for Petrus
    │       ├── temp.do                # Same as specification.do (duplicate)
    │       ├── Data Exploration.ipynb # Jupyter notebook
    │       ├── Data_Standardization.ipynb  # Jupyter notebook
    │       ├── data_work.txt          # IMPORTANT: detailed cleaning notes + open questions
    │       ├── comments_for_lucie.md  # Coding correction note from supervisor
    │       ├── descriptive_stats.tex  # Generated LaTeX descriptive stats table
    │       ├── verbose.log            # OpenAI API error log from NLP pipeline
    │       ├── parquet/               # Processed data (see Data Inventory)
    │       ├── data/
    │       │   └── clean_data_mixed_lots.csv   # 46 MB — CSV export of cleaned data
    │       ├── plots/                 # 113 PDF figures generated by f2_some_ml.py
    │       ├── obsolete/              # Old versions of cleaning and NLP scripts
    │       └── [many .geojson files]  # Bordeaux geographic boundaries
    │
    ├── in vino veritas/               # Early paper draft + analysis (author's own)
    │   ├── main.tex                   # Paper draft: "In Vino Veritas" (older title)
    │   ├── data_cleaning.tex          # Data section: cleaning methodology
    │   ├── analysis.tex               # Analysis section (word cloud appendix)
    │   ├── data.tex, data_exploration.tex, figures.tex, tables.tex  # Paper sections
    │   ├── related_literature.tex     # Literature review section
    │   ├── appendix.tex, internet_appendix.tex
    │   ├── Auction data/              # Raw Excel + parquet inputs
    │   │   ├── Bordeaux Auction Results (Complete).xlsx   # 116 MB
    │   │   ├── Burgundy Auction Results (Complete).xlsx   # 97 MB
    │   │   ├── Rhone Auction Results (Complete).xlsx      # 36 MB
    │   │   ├── [non-complete versions]
    │   │   └── parquet/               # Parquet versions of the above
    │   ├── Code/
    │   │   ├── analysis.py            # Almost empty (2-line stub)
    │   │   ├── utils.py               # Bottle size converter (identical to Lucie's)
    │   │   ├── Data Exploration.ipynb
    │   │   ├── Data_Standardization.ipynb
    │   │   └── parquet/               # Another copy of the raw parquet files
    │   ├── figures/                   # ~20 generated PDF figures
    │   ├── Results/
    │   │   ├── case3.tex              # Theory note: Cobb-Douglas model (KPSV, Feb 2021)
    │   │   └── vinoveritas.pdf        # Compiled paper PDF
    │   └── tables/
    │       └── descriptive_stats.tex
    │
    └── wine/                          # Intermediate paper materials
        ├── main.tex                   # Short doc: data cleaning + rating methodology
        └── appendix 1 - word cloud.tex # Word cloud figures with frequency tables
```

---

## 3. Data Inventory

### Master Data Files

| File | Location | Size | Format | Status | Notes |
|------|----------|------|--------|--------|-------|
| Bordeaux Auction Results (Complete).xlsx | `old/in vino veritas/Auction data/` | 116 MB | Excel | Raw input | Original; not readable w/o Excel |
| Burgundy Auction Results (Complete).xlsx | `old/in vino veritas/Auction data/` | 97 MB | Excel | Raw input | Original |
| Rhone Auction Results (Complete).xlsx | `old/in vino veritas/Auction data/` | 36 MB | Excel | Raw input | Original |
| Bordeaux Auction Results complete.parquet | `old/RALucie/wine/parquet/` | 25 MB | Parquet | Raw input | Parquet conversion of xlsx |
| Burgundy Auction Results complete.parquet | `old/RALucie/wine/parquet/` | 30 MB | Parquet | Raw input | Parquet conversion of xlsx |
| Rhone Auction Results complete.parquet | `old/RALucie/wine/parquet/` | 5.8 MB | Parquet | Raw input | Parquet conversion of xlsx |
| Bordeaux Auction filtered.parquet | `old/RALucie/wine/parquet/` | 6.5 MB | Parquet | Filtered | Subset of above |
| Burgundy Auction filtered.parquet | `old/RALucie/wine/parquet/` | 6.2 MB | Parquet | Filtered | Subset of above |
| Rhone Auction filtered.parquet | `old/RALucie/wine/parquet/` | 3.2 MB | Parquet | Filtered | Subset of above |
| clean_data.parquet | `old/RALucie/wine/parquet/` | 94 MB | Parquet | Cleaned (v1) | Output of f1_data_cleaning.py |
| clean_data_mixed_lots.parquet | `old/RALucie/wine/parquet/` | 94 MB | Parquet | **Master cleaned** | Output of mixed_lots_finding.py — primary analysis dataset |
| clean_data_mixed_lots.parquet | `old/RADuc/` | 94 MB | Parquet | **⚠️ VERIFY** | Duc's copy — may differ; verify checksums |
| clean_data_mixed_lots.csv | `old/RALucie/wine/data/` | 46 MB | CSV | Cleaned | Exported subset (numerical cols only) for Stata |
| output_with_matches.parquet | `old/RADuc/` | 62 MB | Parquet | **⚠️ VERIFY** | URL-matched file from Matching.R; exact coverage unknown |
| petrus_consumption_ideal_date.parquet | `old/RALucie/wine/parquet/` | 232 KB | Parquet | Scraped | Petrus-only with tastingbook maturity dates |
| petrus.csv / petrus_did.csv | `old/RALucie/wine/` | small | CSV | Intermediate | Petrus analysis intermediates |
| Wine_Maturity(Rep_1).csv | `old/RADuc/` | 514 MB | CSV | **⚠️ VERIFY** | Large raw data — Duc's replication 1; unknown provenance |
| Wine_data(Rep2).csv | `old/RADuc/` | 491 MB | CSV | **⚠️ VERIFY** | Large raw data — Duc's replication 2; unknown provenance |
| Wine data_Xin Ning.zip | `old/` | 2 MB | ZIP | Unextracted | Contents unknown; must be opened |

### Key Variables (from data_work.txt + code inspection)

The `clean_data_mixed_lots.parquet` contains the following variable groups:

| Group | Key Variables | Notes |
|-------|--------------|-------|
| Identity | `ID`, `Source`, `Sale#`, `Lot#`, `Auc#` | Not unique identifiers; Lucie notes these are non-informative |
| Auction | `AH` / `AucHouse` → `Auc_House_Combi`, `Date`, `Loc_City`, `Loc_Country` | Standardized; `Date` still flagged for re-checking |
| Wine | `Vintage`, `Age`, `Region`, `Country`, `Sub_Region_Combi`, `Area`, `Class`, `Type_Combi`, `Size` / `Size_liter` | `Age` computed as Date - Vintage; formula may need revision |
| Price | `P_$/Bt_Combi`, `HP_$/Bt_Combi`, `Hammer_$_Combi`, `Esti_$_Low_Combi`, `Esti_$_High_Combi` | Multiple overlapping price vars; `P_Loc` / `P_$` had conflicts with hammer price |
| Quantity | `Qty` | Flagged as potentially non-informative |
| Producer | `Producer/Maker`, `Ori Producer Nm`, `Producer`, `Producer Dummy` | NOT fully standardized — open question as of Lucie's notes |
| Wine name | `WineNm`, `Wine Nm`, `Wine_Nm`, `Item_Nm`, `name` | NOT fully standardized |
| Lot quality | `Mixed_Lots`, `Excluded_Lots`, `Lot_Mark_Combi` | Mixed lot identification completed by Lucie |
| Ratings | `WS_100_st`, `RP_100_st`, `WA_100_st`, `AM_100_st`, `JR_100_st`, `JR_20_st` | Standardized to 100-pt scale |
| Pairing | `For Matching`, `Wine Vintage Pair`, split into `Wine Pair Name/Producer/Region/Year` | GPT-assisted; OpenAI API errors visible in verbose.log |
| URL matching | `matched_url` | Added by Duc's Matching.R; in output_with_matches.parquet only |

### Data Pipeline

```
Raw Excel files (Bordeaux/Burgundy/Rhone)
        │
        ▼
[xlsx → parquet conversion — tool unclear, no script found]
        │
        ▼
Parquet files: "Bordeaux/Burgundy/Rhone Auction Results complete.parquet"
        │
        ▼
f1_data_cleaning_final.py  (Lucie — RELIABLE)
  - Standardizes missing values
  - Cleans location, auction house, wine attributes, ratings, size
  - Joins complementary column pairs (e.g., AucHouse + AH → Auc_House_Combi)
  - OpenAI API used in v1 (f1_data_cleaning.py) to parse Wine Vintage Pair
  - Final version (f1_data_cleaning_final.py) does NOT use OpenAI
  - Output: clean_data.parquet (94 MB)
        │
        ▼
mixed_lots_finding.py  (Lucie — RELIABLE)
  - Text-mines Description_Combi to flag mixed lots
  - Uses consecutive Lot# logic to distinguish true mixed lots from mislabels
  - Creates Mixed_Lots and Excluded_Lots columns
  - Output: clean_data_mixed_lots.parquet (94 MB) ← MASTER DATASET
        │
        ├──→ f2_some_ml.py  (Lucie — exploratory, RELIABLE)
        │     - Loads clean_data_mixed_lots.parquet
        │     - Hedonic OLS residuals on age: documents bimodal pattern
        │     - Outputs: clean_data_mixed_lots.csv, 113 PDF plots
        │     - Chow test at age=120 quarters (30 years): structural break confirmed
        │
        ├──→ specification.do / temp.do  (Lucie — RELIABLE)
        │     - reghdfe: price ~ age × post_maturity, FE by producer
        │     - Input: clean_data_mixed_lots.csv (reads from data/ subdir)
        │
        ├──→ petrus_analysis.py + scrape_wine_data.py  (Lucie — RELIABLE)
        │     - Scrapes tastingbook.com for Petrus maturity dates
        │     - Callaway-Sant'Anna DiD using maturity as staggered treatment
        │     - Output: petrus_consumption_ideal_date.parquet, petrus_did.csv
        │
        ├──→ did_petrus.do  (Lucie — RELIABLE)
        │     - Stata csdid on petrus_did.csv
        │
        └──→ Matching.R  (Duc — ⚠️ VERIFY)
              - Token-based matching of wine rows to tastingbook URLs
              - Reads: clean_data_mixed_lots.parquet (hardcoded: C:/Users/PC/...)
              - Reads: Excel link files (hardcoded: C:/Users/PC/...)
              - Output: output_with_matches.parquet
              [Only 6 producers scraped so far: Armand Rousseau, Romanee Conti,
               Comtes Lafon, Pere & Fils, Georges de Vogue + Scraped_Links.xlsx]
```

---

## 4. Code Inventory

| Script | Language | Purpose | Status | RA | Issues |
|--------|----------|---------|--------|----|--------|
| `f1_data_cleaning_final.py` | Python | Master data cleaning pipeline | Complete | Lucie | Reliable; no OpenAI dependency; correct version to use |
| `f1_data_cleaning.py` | Python | Earlier cleaning pipeline | Superseded | Lucie | Uses OpenAI API (deprecated approach) |
| `mixed_lots_finding.py` | Python | Identify and flag mixed lots | Complete | Lucie | Uses `parquet/clean_data.parquet` as input |
| `f2_some_ml.py` | Python | Exploratory: bimodal pattern + hedonic OLS | Complete/Exploratory | Lucie | Has a bug: `df.groupby('year').size().plot()` after renaming Age col; some cells may fail; uses relative paths |
| `petrus_analysis.py` | Python | Petrus DiD + tastingbook scraping | Complete/Exploratory | Lucie | Scrapes tastingbook; hardcoded to Petrus; outputs petrus_did.csv |
| `scrape_wine_data.py` | Python | Scrape tastingbook for wine data | Complete | Lucie | Works for Petrus; generalizable but not generalized |
| `NLP_model.py` | Python | BERT embeddings on wine descriptions | Partial/Broken | Lucie | API errors logged in verbose.log; loads data from Dropbox URL |
| `wordcloud.py` | Python | Text exploration | Exploratory | Lucie | Uses `parquet/clean_data.parquet` |
| `utils.py` | Python | Bottle size converter | Complete | Lucie/Original | Identical copies in two directories |
| `specification.do` | Stata | reghdfe: price ~ age × maturity | Exploratory | Lucie | Reads `data/clean_data_mixed_lots.csv`; relative path |
| `did_petrus.do` | Stata | csdid: Petrus staggered DiD | Exploratory | Lucie | Reads `petrus_did.csv`; relative path |
| `temp.do` | Stata | Identical to specification.do | Duplicate | Lucie | Delete or merge with specification.do |
| `Matching.R` | R | Token-match wine rows to tastingbook URLs | Complete | Duc | **HARDCODED PATHS**: `C:/Users/PC/Documents/R/RA Task/`; files do not exist at those paths; only 6 producers done |
| `Code for Producer list.py` | Python | Extract Bordeaux producer list | Complete | Xin Ning | **HARDCODED PATH**: `/Users/ningxin/Desktop/Wine Data/`; path does not exist on this machine |
| `test.py` (RADuc) | Python | Bordeaux filter + vintage inspection | Exploratory | Duc | Reads `clean_data_mixed_lots.parquet` relative; meant for Duc's machine |
| `analysis.py` (in vino veritas) | Python | Stub — effectively empty | Broken | Unknown | Only 2 lines; no content |
| `bibtex_to_csv.py` | Python | Convert bib files to CSV | Complete | Lucie | Unrelated to wine data pipeline |
| `articles_scrapping_selenium.py` | Python | Scrape article metadata | Complete | Lucie | Unrelated to wine data pipeline |

---

## 5. Items Requiring Verification

### Duc's Work

Every file touching Duc's name requires independent verification before use in the paper.

| File | What It Claims to Do | Why Verify |
|------|---------------------|------------|
| `old/RADuc/Matching.R` | Match wine rows to tastingbook URLs using token overlap | Algorithm is documented and logic appears sound, but: (1) only 6 producers scraped, (2) coverage of `Producer/Maker = NA` rows is explicitly acknowledged as incomplete, (3) output path hardcoded to Duc's machine |
| `old/RADuc/output_with_matches.parquet` | 62 MB — wine data with `matched_url` column added | Unknown what % of rows have a non-empty `matched_url`; unknown if matching was re-run on full Scraped_Links or only on 6 producers' files |
| `old/RADuc/clean_data_mixed_lots.parquet` | 94 MB — copy of master cleaned dataset | Verify file hash matches `old/RALucie/wine/parquet/clean_data_mixed_lots.parquet`; if different, determine which is authoritative |
| `old/RADuc/Wine_Maturity(Rep_1).csv` | 514 MB raw wine auction data (Replication 1) | Unclear provenance: is this the raw data before Lucie's cleaning? A separate data pull? A duplicate? Must check column names and row count against the parquet files |
| `old/RADuc/Wine_data(Rep2).csv` | 491 MB raw wine auction data (Replication 2) | Same concerns as above; "Rep2" suggests a second replication pull — are these the same data, or two different time periods/sources? |
| `old/RADuc/Links by producers/Scraped_Links.xlsx` | Full pool of scraped tastingbook URLs | Only 6 producers documented; Scraped_Links.xlsx may have more, but Duc's README says full scraping requires ~5 days of Octoparse work that may not have been completed |

### Exposed API Key

`old/RALucie/wine/f00_settings.py` line 1 contains a hardcoded OpenAI API key:
```
API_KEY = "[REDACTED - key removed from repository]"
```
This key was committed to the repo. It is likely already expired (this is Lucie's key from when she was working), but the key should be revoked immediately and this file should be added to `.gitignore`. The final cleaning script (`f1_data_cleaning_final.py`) does NOT use this key — only the superseded `f1_data_cleaning.py` imports it.

### Broken / Missing File References

| Script | Referenced Path | Exists? | Fix |
|--------|----------------|---------|-----|
| `Matching.R` | `C:/Users/PC/Documents/R/RA Task/clean_data_mixed_lots.parquet` | NO | Replace with `old/RADuc/clean_data_mixed_lots.parquet` (or relative path) |
| `Matching.R` | `C:/Users/PC/Documents/R/RA Task/Armand_Rosseau.xlsx` | NO | Replace with `old/RADuc/Links by producers/Armand_Rosseau.xlsx` |
| `Matching.R` | `C:/Users/PC/Documents/R/RA Task/output_with_matches.parquet` | NO | Replace output path |
| `Code for Producer list.py` | `/Users/ningxin/Desktop/Wine Data/RADuc/clean_data_mixed_lots.parquet` | NO | Replace with repo-relative path |
| `Code for Producer list.py` | `/Users/ningxin/Desktop/Wine Data/bordeaux_producers_list.csv` | NO | Replace output path |
| `Correlation_AEWReturns.py` | `/Users/lucieburdychova/Desktop/VSCode2/Industry-Firm/...` | NO | Unrelated project; not needed for wine paper |
| `f1_data_cleaning.py` | `parquet/` directory (relative) | YES, if run from `old/RALucie/wine/` | Script must be run from correct cwd |
| `mixed_lots_finding.py` | `parquet/clean_data.parquet` (relative) | YES, if run from `old/RALucie/wine/` | Same cwd requirement |
| `specification.do` | `data/clean_data_mixed_lots.csv` (relative) | YES, if run from `old/RALucie/wine/` | Same cwd requirement |
| `did_petrus.do` | `petrus_did.csv` (relative) | YES, if run from `old/RALucie/wine/` | Same cwd requirement |

### Hardcoded Absolute Paths

| Script | Path | Action Needed |
|--------|------|--------------|
| `Matching.R` (line 8) | `C:/Users/PC/Documents/R/RA Task/clean_data_mixed_lots.parquet` | Rewrite with relative/config path |
| `Matching.R` (line 10) | `C:/Users/PC/Documents/R/RA Task/Armand_Rosseau.xlsx` | Rewrite |
| `Matching.R` (line 99-101) | `C:/Users/PC/Documents/R/RA Task/output_with_matches.parquet` | Rewrite |
| `Code for Producer list.py` (line 4) | `/Users/ningxin/Desktop/Wine Data/RADuc/clean_data_mixed_lots.parquet` | Rewrite |
| `Code for Producer list.py` (line 13) | `/Users/ningxin/Desktop/Wine Data/bordeaux_producers_list.csv` | Rewrite |
| `NLP_model.py` (line 4) | Dropbox URL (public link) | URL may expire; better to read from local file |
| `f00_settings.py` (line 1) | OpenAI API key string | Revoke + move to `.env` |
| `Correlation_AEWReturns.py` | `/Users/lucieburdychova/Desktop/VSCode2/...` | Not relevant to this project |

---

## 6. Pipeline Gaps

### What Exists
- Raw auction data (Excel + Parquet) for Bordeaux, Burgundy, Rhone
- Complete data cleaning pipeline (Lucie) → `clean_data_mixed_lots.parquet`
- Exploratory bimodal pattern documentation (f2_some_ml.py plots)
- A preliminary hedonic OLS establishing the structural break at ~28-33 years of age
- Partial tastingbook scraping (Petrus only)
- Preliminary DiD on Petrus using maturity as treatment
- Early theory note (case3.tex, KPSV, 2021) modeling the consumption-collector tradeoff
- Related literature section (related_literature.tex) — coverage appears reasonable but needs updating

### What Is Missing (Priority Order)

1. **Maturity estimates for non-Petrus wines** — the tastingbook scraping only covers Petrus. The entire structural strategy requires `tau_i` (maturity date) for all wines or at least a representative sample. The Duc URL-matching exercise was intended to enable this, but: (a) only 6 producers have scraped links, (b) `output_with_matches.parquet` exists but its coverage is unknown.

2. **Verification of Duc's raw CSV files** — `Wine_Maturity(Rep_1).csv` (514 MB) and `Wine_data(Rep2).csv` (491 MB) are large and their relationship to the clean parquet files is unclear. If these contain maturity information not in the cleaned data, that is a critical gap.

3. **The xlsx → parquet conversion script** — no script is present that converts the original Excel files to parquet. This conversion clearly happened (both formats exist), but there is no reproducible code for it.

4. **Producer and wine name standardization** — Lucie's `data_work.txt` explicitly marks producer/wine name fields as "NOT YET STANDARDIZED." These are essential for producer-level fixed effects.

5. **`Age` variable validation** — Lucie's data_work.txt flags: "VARIABLE DATE NEEDS TO BE CHECKED AGAIN and variable age might need to be updated." The `f2_some_ml.py` script recalculates age from scratch using a June 30 vintage-quarter assumption, suggesting the original `Age` in the parquet may be unreliable.

6. **`P_Loc` / `P_$` conflict** — Lucie's notes flag that hammer price in local currency (`P_Loc`) and dollar (`P_$`) have conflicting values vs. the combined variables (`Hammer_Loc_Combi`, `Hammer_$_Combi`). This was not resolved and may affect price analysis.

7. **Paper draft** — there is no paper draft at the project root. The old draft (`old/in vino veritas/main.tex`) is a very early version (titled "In Vino Veritas") that likely does not reflect current thinking and has not been updated.

8. **`Wine data_Xin Ning.zip` contents** — this 2 MB zip in `old/` has never been extracted. Contents are unknown.

9. **Literature review** — `related_literature.tex` exists but needs to be updated with recent work on structural auction models, alternative assets, and especially the China demand shock literature.

10. **No `code/`, `data/`, or `paper/` structure** — the canonical CLAUDE.md folder structure does not exist. All files are in `old/` with no separation of raw vs. processed data, no centralized bibliography, and no single paper source file.

---

## 7. Recommended Next Steps

Priority order — each step blocks the next:

1. **[IMMEDIATE] Revoke and rotate the OpenAI API key** in `f00_settings.py`. Add this file to `.gitignore`. Move any needed keys to `.env`.

2. **[IMMEDIATE] Verify Duc's parquet files** — run a checksum or row-count comparison between `old/RADuc/clean_data_mixed_lots.parquet` and `old/RALucie/wine/parquet/clean_data_mixed_lots.parquet`. If they differ, determine which is the authoritative version and why.

3. **[HIGH] Inspect Duc's raw CSVs** — open `Wine_Maturity(Rep_1).csv` and `Wine_data(Rep2).csv` (at least check shape, columns, and row count). Determine: (a) are these the same underlying data as the clean parquet, just un-cleaned? (b) do they contain a maturity column that is absent from the cleaned data? This is the single most important unknown in the project.

4. **[HIGH] Extract and inspect `Wine data_Xin Ning.zip`** — unzip and document contents.

5. **[HIGH] Assess tastingbook URL coverage** — open `output_with_matches.parquet` and check: how many rows have a non-empty `matched_url`? How many unique wines have been matched? This determines how far Duc got on the maturity data collection.

6. **[MEDIUM] Establish folder structure** — create `data/raw/`, `data/processed/`, `code/`, `paper/` directories and migrate files from `old/`. The canonical structure in CLAUDE.md does not exist.

7. **[MEDIUM] Resolve open data questions** from Lucie's `data_work.txt` — particularly: (a) producer name standardization, (b) `Age` variable re-computation, (c) `P_Loc` / `P_$` conflict, (d) `Class` standardization.

8. **[MEDIUM] Generalize scraping to all wines** — `scrape_wine_data.py` works for Petrus. Generalize it to all wines using the URL pool from Duc's `output_with_matches.parquet`. This feeds directly into the structural model.

9. **[MEDIUM] Run `/lit-review`** — the existing literature section covers pre-2020 work. Update with structural auction models (Lovo & Spaenjers 2018 is cited; check for follow-ups) and recent work on China demand shocks.

10. **[LOWER] Fix all hardcoded paths** in `Matching.R` and `Code for Producer list.py` before those scripts can be re-run.

---

## 8. Open Questions for the Team

Questions that only the researchers can answer:

1. **What is in `Wine_Maturity(Rep_1).csv` (514 MB)?** Is the word "Maturity" in the filename significant — does this file contain maturity dates or expert assessments not available in the auction data? This is the most urgent empirical question.

2. **What is the relationship between the two large CSVs** (`Wine_Maturity(Rep_1)` and `Wine_data(Rep2)`)? Are these from different data vendors or different time periods? "Rep_1" and "Rep2" suggest replications of the same dataset — if so, which is more recent/reliable?

3. **Was the tastingbook scraping ever extended beyond Petrus?** Duc's README says full scraping requires ~5 days with Octoparse. Was this ever completed? Is there a more complete version of `Scraped_Links.xlsx` somewhere outside the repo?

4. **How should `Age` be computed?** The original parquet has an `Age` column computed as `Date - Vintage`. Lucie's `f2_some_ml.py` recomputes it as `4 × (Date - June 30 of Vintage year) / 365.25` (quarters). Which convention should be used? The Stata spec uses `agequarters`, implying quarters — is this from the parquet or recomputed?

5. **`P_Loc` / `P_$` vs `Hammer_Loc_Combi` / `Hammer_$_Combi`** — which price variable is authoritative for the main analysis? The `P_Loc` / `P_$` variables had conflicting values in Lucie's cleaning. Has this been resolved?

6. **What did the co-authors (Kräussl, Piatti, Steri) work on since the 2021 theory note (`case3.tex`)?** The structural model should be coordinated with their latest version before estimation begins.

7. **Acknowledgment policy confirmed?** `project_liquid_assets.md` says to thank Lucie and Xin Ning, explicitly DO NOT acknowledge Duc. The research spec confirms this. Has this been communicated to all co-authors?

8. **What does `Wine data_Xin Ning.zip` contain?** Was Xin Ning given a specific task? The only code attributed to Xin Ning is `Code for Producer list.py` (a 14-line script to extract Bordeaux producers). The zip may contain more work.

9. **Is `old/in vino veritas/Results/vinoveritas.pdf` the most recent compiled paper?** If so, should this be the starting point for `paper/main.tex` or should the paper be written fresh from the research spec?

10. **China demand shock dates** — the research spec mentions a Chinese market withdrawal "circa 2012-2013." Does the auction data span this period? Is there a buyer geography variable reliable enough to distinguish Chinese buyers?

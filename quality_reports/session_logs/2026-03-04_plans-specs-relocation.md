# Session Log — 2026-03-04: Move Plans/Specs to .claude/

**Goal:** Relocate agent plan and spec files from `quality_reports/plans/` and `quality_reports/specs/` to `.claude/plans/` and `.claude/specs/`, to keep `quality_reports/` exclusively for paper-quality artifacts.

**Status:** COMPLETED

---

## Key Context

- `quality_reports/` should hold only paper-quality outputs (scores, session logs, merge reports, research journal)
- Plans and specs are internal Claude agent orchestration artifacts — they belong inside `.claude/` alongside rules, hooks, skills, and agents
- This was a 6-file change with zero paper/code impact

---

## Changes Made

1. Created `.claude/plans/` and `.claude/specs/` directories (with `.gitkeep`)
2. **CLAUDE.md** — updated folder structure: `quality_reports/` comment clarified; `.claude/plans/` and `.claude/specs/` added under `.claude/`
3. **`.claude/rules/plan-first-workflow.md`** — 4 path references updated
4. **`.claude/rules/meta-governance.md`** — dogfooding section + quick reference table updated; Plans row marked ❌ No / gitignored
5. **`.claude/hooks/pre-compact.py`** — 3 references updated (`find_active_plan`, session log note, checklist item)
6. **`.claude/skills/context-status/SKILL.md`** — 2 references updated

## Verification

- Grep for `quality_reports/(plans|specs)` across all files → 0 hits
- `.claude/plans/` and `.claude/specs/` confirmed to exist

---

## 2026-03-29 — Maturity Data Merge

**Goal:** Execute plan `.claude/plans/2026-03-29_merge-maturity-data.md` — merge Tastingbook "When to drink" maturity data onto auction dataset.

**Status:** COMPLETED

### Steps completed

1. Extracted `old/Wine data_Xin Ning.zip` → `data/raw/tastingbook_xin_ning/` (data.xlsx, scraper, README, missing values)
2. Explored tastingbook structure: 15,902 rows, ~87% Bordeaux, 99.3% have maturity data; `year_url` cannot directly join auction `matched_url` (different producer coverage)
3. Identified correct normalization: `unicodedata.normalize('NFKD', ...).encode('ascii', errors='ignore')` handles `Ch\u00e2teau` → `chateau` for both auction and tastingbook
4. Wrote `code/cleaning/04_merge_maturity.py` — 3-stage merge (exact, producer+vintage, fuzzy pre-computed, producer avg)
5. Optimised fuzzy stage: pre-computed producer-level map once (O(n_producers²)) instead of per-row O(n²) — reduced runtime from >4 min timeout to ~2 min
6. Output: `data/processed/auction_with_maturity.parquet` (70.7 MB, 1,068,703 rows, 90 columns)
7. Verification plot: `output/figures/price_relative_to_maturity.{pdf,png}`
8. Report: `output/maturity_merge_report.md`

### Match rates
- exact: 25.3% | producer_vintage: 11.6% | fuzzy: 7.0% | producer_avg: 5.0% | unmatched: 51.1%
- Bordeaux match rate: 80.5% | Burgundy: 0.7% | Rhone: 13.3%

### Key finding (critical caveat)
Tastingbook "When to drink" is a **2026-anchored** current recommendation. For historical auction sales (1996–2020), old vintages all appear "pre-maturity" (100%). The `age_relative_to_maturity` variable is not valid for testing the bimodal hypothesis against historical data. It IS valid as a cross-sectional structural parameter (years-to-maturity per wine type). Flagged prominently in §5b of the report. Recommended fix: classify lots using `sale_year ∈ [drink_from, drink_until]` directly.

---

## 2026-03-29 — Tastingbook Re-scrape (sitemap approach)

**Goal:** Recover the ~51% unmatched lots by finding missing producers on Tastingbook.

**Status:** IN PROGRESS (merge re-running)

### Key discoveries
1. **No auth needed** — all Tastingbook wine pages are public
2. **Tastingbook has a sitemap** (`sitemap-index.xml` → 2 gzipped XMLs) with 61,990 wine URLs across 6,789 producers
3. **Slug patterns are unpredictable** — hyphens dropped inconsistently, owner initials prepended (`m_chapoutier`, `eguigal`), `de la` dropped (`domaine_de_la_romaneeconti`). No deterministic rule; sitemap is ground truth.
4. **Xin Ning's scraper had no auth** — it used feapder with a Chrome UA on direct URLs. The original 51% miss rate was entirely due to wrong slug guesses, not auth.

### Steps completed
1. Rewrote `code/scraping/05_scrape_tastingbook.py` — sitemap-based, no auth, parallel workers
   - Step 1: download + cache both sitemaps → `data/raw/tastingbook_rescrape/sitemap_urls.csv`
   - Step 2: match auction producers → TB slugs (exact → word-boundary → containment → fuzzy)
   - Step 3: parallel scrape with ThreadPoolExecutor
   - Step 4: combine with Xin Ning baseline → `data_combined.xlsx`
2. Matched 289 producers covering 439k lots (Burgundy 177, Bordeaux 72, Rhône 39)
3. Scraped 8,192 new rows (8,321 target, 129 no-data)
4. Combined: 17,701 rows (15,902 Xin Ning + 1,799 new net)
5. Updated `04_merge_maturity.py` to use `data_combined.xlsx` with fallback to Xin Ning

### Key producers recovered
- DRC (48,676 lots) → `domaine_de_la_romaneeconti` — 493 pages in sitemap
- Chapoutier (19,718) → `m_chapoutier`
- Guigal (15,543) → `eguigal`
- La Mission Haut-Brion (15,102) → `chateau_la_mission_hautbrion`
- Léoville Las Cases (15,761) → `chateau_leovillelas_cases`
- Lynch Bages (13,463) → `chateau_lynchbages`

### Final results
- Overall match rate: **76.0%** (up from 48.9%)
- fuzzy 41.9% | producer_vintage 26.2% | unmatched 24.0% | producer_avg 7.6% | exact 0.3%
- Burgundy: 51.6% unmatched (was ~99%); Bordeaux: 7.6% unmatched

---

## 2026-03-29 — Price-Age Analysis

**Goal:** Characterise how log price per bottle depends on wine age with heterogeneity by region, maturity stage, wine type, bottle size.

**Status:** COMPLETED

### Steps completed
1. Wrote and ran `code/analysis/04_price_age_analysis.py`
   - Fix needed: `P_$/Bt_Combi` stored as string → `pd.to_numeric(..., errors='coerce')`
2. Output: `output/price_age_report.md`
   - 3 OLS specs (pooled cubic, region×cubic, hedonic with producer demeaning)
   - Turning points: Bordeaux monotone, Burgundy peak ~80.8 yrs (Spec 3), Rhône peak ~66.9 yrs
   - R²=0.40 (Spec 3); magnum premium +70%; white premium +56%; post-maturity discount -22% (n=18, insignificant)

### Key finding
Monotone price-age profile — no bimodal or inverted-U visible in raw calendar age. Reason: see maturity imputation section below.

---

## 2026-03-29 — Maturity Imputation + Normalized Age Analysis

**Goal:** Impute years_to_maturity for unmatched lots; re-run price analysis on normalized age (age/years_to_maturity) to test inverted-U hypothesis.

**Status:** COMPLETED (open question pending)

### Steps completed
1. Wrote and ran `code/analysis/05_maturity_imputation.py`
   - Fix needed: NaN in target-encoded features after join → `.fillna(global_mean)`
   - GradientBoostingRegressor, 5-fold CV R²=0.991, RMSE=2.0 yrs
   - Feature importances: vintage 99.8% (dominates — YTM = maturity_peak − vintage, peak varies little)
   - Imputed 256,296 lots (24%); output: `data/processed/auction_with_maturity_imputed.parquet`
2. Wrote and ran `code/analysis/06_price_normalized_age_analysis.py`
   - Fix needed: column `Bt_Combi` doesn't exist → use `Size_liter`
   - Output: `output/price_normalized_age_report.md`

### Key findings
- **100% of lots have age_norm < 1.0** — the entire dataset is pre-maturity by TB estimates
- Median years_to_maturity = 32–39 yrs by region; median drink_until = 2035; 93% of wines won't expire until 2026+
- Strong monotone price appreciation as wine approaches maturity (age_norm 0→1)
- Cannot test bimodal — dataset structurally doesn't reach post-maturity in volume

### Open question
Tastingbook values unreliable for very old vintages (e.g., Yquem 1784: drink_until=2026, YTM=242 yrs). These are TB-matched but should be imputed instead. Rule to implement: flag TB matches where `years_to_maturity > threshold` (e.g., 80 or 100) and replace with model prediction. Threshold TBD with user.

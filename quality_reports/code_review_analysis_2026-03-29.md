# Code Review: analysis/ scripts
**Date:** 2026-03-29
**Mode:** Standalone (categories 4--12)
**Reviewer:** Debugger (Claude Opus 4.6)

---

## Per-Script Scores

| Script | Score | Critical | Major | Minor |
|--------|-------|----------|-------|-------|
| `05_maturity_imputation.py` | 82/100 | 0 | 1 | 2 |
| `06_price_normalized_age_analysis.py` | 82/100 | 0 | 1 | 2 |
| `07_dip_significance_test.py` | 47/100 | 2 | 1 | 2 |
| `08_top_wines_price_age.py` | 47/100 | 2 | 1 | 2 |
| `09_paper_tables_figures.py` | 75/100 | 0 | 2 | 1 |

---

## Issues by Script

### 05_maturity_imputation.py

**Score: 82/100**

**Category 4 -- Script Structure & Headers: OK**
- Excellent docstring (lines 1--20) with purpose, strategy, and output columns.
- Clear numbered sections (1--5) with separator comments.
- Functions are well-organized with a clean `main()` entry point.

**Category 5 -- Console Output Hygiene: WARN (-3)**
- Uses `print()` throughout (lines 96--98, 156--165, 179, 215, 235, 249--252, 267, 275--280, 300). Python convention allows `print()` for CLI scripts, but the volume is high (20+ print calls). Not a critical issue, but `logging` module would be more appropriate for a research pipeline.

**Category 6 -- Reproducibility: OK**
- Relative paths via `Path(__file__).resolve().parent.parent.parent` (line 38). Good.
- `random_state=42` set on both the model (line 154) and the KFold (line 157). Good.
- No hardcoded absolute paths.

**Category 7 -- Function Design: WARN (-3)**
- `build_features()` at line 106 returns a 4-tuple `(tb, prod_stats, wine_stats, global_mean)` but the type hint says `-> pd.DataFrame`. This is misleading and will confuse downstream readers.
- `impute_auction()` is ~75 lines (lines 173--254), which is long but acceptable given the linear flow.
- Naming is clear and consistent.

**Category 8 -- Figure Quality: N/A**
- No figures produced by this script.

**Category 9 -- Artifact Saving: WARN (-10)**
- The trained model is **not saved** (no `joblib.dump()` or `pickle`). If downstream scripts need the model or its diagnostics (e.g., feature importances, CV scores), they must re-run this script. The parquet output is saved (line 265), which is the primary artifact, but the model object itself is ephemeral.
- The cross-validation scores and feature importances are only printed to console, not persisted to any file.

**Category 10 -- Comments: OK**
- Good "why" comments (lines 43--46 explaining the YTM cap rationale, line 92 explaining default to red).
- Section headers are clear.

**Category 11 -- Error Handling: WARN**
- `warnings.filterwarnings("ignore")` at line 37 silently suppresses all warnings -- this could mask convergence issues in sklearn.
- No check for missing input files. If `TB_PATH` or `AUCTION_IN` doesn't exist, the error is a raw Python traceback.
- No validation that the model achieves a minimum R^2 before proceeding to imputation.

**Category 12 -- Polish: OK**
- Clean imports, consistent spacing.
- No dead code or commented-out blocks.
- `from __future__ import annotations` is good practice.

---

### 06_price_normalized_age_analysis.py

**Score: 82/100**

**Category 4 -- Script Structure & Headers: OK**
- Good docstring (lines 1--12) with purpose, key question, and output path.
- Numbered sections, clean `main()` function.

**Category 5 -- Console Output Hygiene: WARN (-3)**
- 15+ print statements. Acceptable for a CLI script but verbose.

**Category 6 -- Reproducibility: OK**
- Relative paths via `Path(__file__)` (line 28).
- No stochastic operations in this script, so no seed needed.

**Category 7 -- Function Design: OK**
- Functions are well-scoped. `write_report()` is very long (~200 lines, 243--430) but it's a report-formatting function, so sequential length is acceptable.
- `get_stage()` inner function at line 81 uses `df.apply()` row-by-row, which is slow on large DataFrames. A vectorized approach would be preferable for performance but this is a design concern, not a bug.

**Category 8 -- Figure Quality: N/A**
- This script produces a markdown report, not figures.

**Category 9 -- Artifact Saving: WARN (-10)**
- The regression model objects (`results` dict) are not saved. Only the markdown report is written (line 429).
- The `turning_points` list, regression coefficients, and binned median tables are only written into the markdown report -- not into a structured format (CSV, JSON, pickle) for downstream reuse.

**Category 10 -- Comments: OK**
- Good inline comments explaining normalized age semantics and bin construction.

**Category 11 -- Error Handling: WARN**
- `warnings.filterwarnings("ignore")` (line 17).
- No check for missing input file.
- `turning_points()` has a bare `except ValueError: pass` at line 215 that silently ignores root-finding failures.

**Category 12 -- Polish: WARN (-3)**
- Line 196: `deriv = lambda x: ...` with `# noqa: E731` -- assigning lambdas to variables is a code smell. Named functions would be clearer.
- Same at line 197.
- Otherwise clean.

---

### 07_dip_significance_test.py

**Score: 47/100**

**Category 4 -- Script Structure & Headers: FAIL (-5)**
- Has a docstring (lines 1--6) but no author, date, or input/output specification.
- **No function structure whatsoever.** The entire script is a single monolithic block of 184 lines of top-level code (lines 14--184). The only functions are `poly5_turning_points()` (line 59) which is defined mid-script.
- No `main()` function, no `if __name__ == "__main__"` guard.

**Category 5 -- Console Output Hygiene: WARN (-3)**
- Extensive console output is the *only* output of this script. All results are printed and not saved anywhere.

**Category 6 -- Reproducibility: FAIL (-20)**
- **Hardcoded relative path without `ROOT` anchor:** Line 15 uses `"data/processed/auction_with_maturity_imputed.parquet"` -- a bare relative path. This only works if the script is run from the project root directory. Scripts 05, 06, and 09 all use `Path(__file__).resolve().parent.parent.parent` to construct `ROOT`. This script breaks the convention and will fail if run from any other working directory (e.g., `code/analysis/`).

**Category 7 -- Function Design: FAIL (-10)**
- Monolithic top-level code. Data loading, filtering, regression, spline fitting, segment testing -- all at top level with no encapsulation.
- `poly5_turning_points()` is the only extracted function, but it mixes computation with printing (line 75--85).
- Code is not reusable or testable.

**Category 8 -- Figure Quality: N/A**
- No figures.

**Category 9 -- Artifact Saving: FAIL (-10)**
- **Nothing is saved.** All regression results, turning points, segment tests, and contrasts are only printed to console. No output file is written. This means:
  - Results cannot be referenced by downstream scripts.
  - Results are not reproducible without re-running the script and manually copying console output.
  - The paper pipeline cannot use these results.

**Category 10 -- Comments: WARN (-3)**
- Section headers exist (lines 48, 91, 135) but are sparse.
- No comments explaining the choice of knots `[0.4, 0.8, 1.2, 1.6, 2.2]` (line 93), segment boundaries (line 137), or the one-sided p-value direction (line 180).

**Category 11 -- Error Handling: WARN**
- `warnings.filterwarnings("ignore")` (line 11).
- Bare `except Exception: pass` in `poly5_turning_points()` (line 73--74) silently swallows errors.

**Category 12 -- Polish: WARN (-3)**
- Multi-import on single line: `import pandas as pd, numpy as np, statsmodels.formula.api as smf` (line 7). This violates PEP 8.
- `import sys; sys.stdout.reconfigure(encoding="utf-8")` on one line (line 12).
- Lines 79--83 have inconsistent indentation style compared to other scripts.
- Massive duplication of data loading/filtering code that is identical to scripts 06 and 08.

---

### 08_top_wines_price_age.py

**Score: 47/100**

**Category 4 -- Script Structure & Headers: WARN (-5)**
- Has a docstring (lines 1--9) listing the three subsamples. No author or date.
- Better function structure than 07 -- `fit_spline()`, `fit_poly5()`, `segment_tests()` are extracted.
- But data loading is still monolithic top-level code (lines 18--55), and the main loop (lines 133--201) has no encapsulation.
- No `main()` function, no `if __name__ == "__main__"` guard.

**Category 5 -- Console Output Hygiene: WARN (-3)**
- All output goes to console only.

**Category 6 -- Reproducibility: FAIL (-20)**
- **Same hardcoded relative path problem as script 07:** Line 18 uses `"data/processed/auction_with_maturity_imputed.parquet"` without a `ROOT` anchor. Will fail if not run from project root.

**Category 7 -- Function Design: OK**
- `fit_spline()`, `fit_poly5()`, `segment_tests()` are well-extracted helper functions.
- However, `fit_poly5()` at line 83 duplicates nearly identical code from `poly5_turning_points()` in script 07. This is a DRY violation across scripts.

**Category 8 -- Figure Quality: N/A**
- No figures.

**Category 9 -- Artifact Saving: FAIL (-10)**
- **Nothing is saved.** Same problem as script 07 -- all results are console-only. No output file, no structured data saved.

**Category 10 -- Comments: WARN (-3)**
- `fit_spline()` and `fit_poly5()` have no docstrings.
- No explanation for why knots are `[0.4, 0.8, 1.2, 1.6, 2.2]`.
- No explanation for why boundary filter is `0.05 < r < 2.95` at line 100.

**Category 11 -- Error Handling: OK**
- `try/except` blocks around spline and poly5 fitting (lines 162--171, 175--184, 188--200). Errors are printed with context. This is reasonable.

**Category 12 -- Polish: WARN (-3)**
- Same PEP 8 violations as script 07: multi-import lines (line 10), semicolons joining statements (line 15).
- Massive code duplication with scripts 07 and 09 (data loading, filtering, mask definitions, spline fitting).

---

### 09_paper_tables_figures.py

**Score: 75/100**

**Category 4 -- Script Structure & Headers: OK**
- Good docstring (lines 1--15) listing all output files.
- No `main()` function -- the entire script runs at top level. However, it uses helper functions for specific tasks.
- No `if __name__ == "__main__"` guard.

**Category 5 -- Console Output Hygiene: OK**
- Print statements are informative progress indicators (lines 35, 109, 205, 260, 329, 431, 472, 511, 548--555). Appropriate for a pipeline script.

**Category 6 -- Reproducibility: OK**
- Uses `ROOT = Path(__file__).resolve().parent.parent.parent` (line 29). Good.
- `mkdir(exist_ok=True)` for output directories (lines 30--32). Good.

**Category 7 -- Function Design: WARN (-10)**
- `fit_spline_with_ci()` at line 75 is well-designed with docstring and returns predictions + CI.
- `add_panel()` at line 144 is a reasonable figure-building helper.
- `fmt_coef()` at line 356 is clean.
- However, the bulk of the script (Tables 1--3, Appendix tables) is monolithic top-level code. Each table generation block is 40--80 lines of inline code that should be wrapped in functions.
- `add_panel()` uses closure over `groups`, `COLORS`, `LABELS` globals -- acceptable but fragile.

**Category 8 -- Figure Quality: WARN (-10)**
- **Positives:**
  - Custom color palette defined (lines 122--126): domain-appropriate deep red, blue, purple.
  - Serif font family (line 113).
  - Top and right spines removed (lines 115--116).
  - Both PDF and PNG saved (lines 198--199). Good.
  - Confidence intervals shown (line 157).
  - Legend is `frameon=False` (line 179).
- **Issues:**
  - `font.size: 11` (line 114) is below the recommended `base_size >= 14`. Axis labels are 11pt (lines 177--178). These will be small in a two-panel figure at journal column width.
  - No explicit `figsize` DPI for the PDF (line 198 uses default). The PNG uses `dpi=180` (line 199) which is acceptable but not high (300 DPI is standard for publication).
  - Background is not explicitly set to transparent. Default matplotlib background is white, which is fine for most uses, but explicit `transparent=True` in `savefig()` would be better practice.
  - The annotation arrow position at line 184 (`xy=(36, 5.15), xytext=(43, 4.9)`) is hardcoded to specific data coordinates. If the data changes, this annotation will be misplaced.

**Category 9 -- Artifact Saving: OK**
- All tables are written to `paper/tables/` and `paper/appendix/` (lines 255, 324, 427, 468, 507, 544).
- Figure saved as both PDF and PNG (lines 198--199).
- Directory creation before writing (lines 30--32).

**Category 10 -- Comments: OK**
- Comments explain the figure structure and table layout.
- Inline LaTeX table construction is well-commented with section headers.

**Category 11 -- Error Handling: WARN**
- `warnings.filterwarnings("ignore")` (line 26).
- No check for input file existence.
- **Appendix Table A3 (lines 511--544) contains hardcoded statistics** (e.g., "Training observations: 16,148", "Cross-validation: $R^2 = 0.991 \pm 0.001$", "Auction lots: TB-matched: 812,407 (76.0%)"). These values are not computed from data -- they are manually transcribed from a previous run of script 05. If script 05 is re-run with different data or parameters, these values will be **stale and incorrect** with no warning. This is a significant reproducibility concern.

**Category 12 -- Polish: WARN (-3)**
- Multi-import lines (line 16): `import pandas as pd, numpy as np, warnings`.
- Line 69 is very long (~110 characters) with a complex f-string containing `chr(10)`.
- No `if __name__ == "__main__"` guard.
- Otherwise clean.

---

## Top Issues Across All Scripts

### Critical (Fix Before Proceeding)

1. **Scripts 07 and 08 use bare relative paths** -- `"data/processed/..."` at 07:15 and 08:18. Every other script uses `Path(__file__).resolve().parent.parent.parent` as ROOT. These two scripts will fail if run from their own directory (`code/analysis/`), which is the natural expectation. This is a reproducibility failure.

2. **Scripts 07 and 08 save nothing** -- All regression results, turning points, segment tests, and direct contrasts are printed to console only. No output files are written. If these scripts produce results needed by the paper, those results are not in the pipeline. If they are exploratory, they should still save structured output for audit trail.

3. **Appendix Table A3 in script 09 (lines 511--544) contains hardcoded statistics** -- Training observations, CV R^2, RMSE, matched/imputed lot counts are manually typed, not computed. These will become stale if upstream data changes.

### Warnings (Should Fix)

4. **Massive code duplication across scripts 07, 08, and 09** -- Data loading and filtering (read parquet, price filter, date parsing, age computation, age_norm computation, wine type classification) is copy-pasted verbatim across all three scripts. This should be extracted into a shared utility module (e.g., `code/analysis/utils.py` or `code/analysis/load_data.py`).

5. **Model object not saved in script 05** -- The GradientBoostingRegressor and its diagnostics (CV scores, feature importances) are ephemeral. For reproducibility and audit, the model should be persisted.

6. **`warnings.filterwarnings("ignore")` in every script** -- Blanket warning suppression can mask genuine issues (convergence warnings, deprecation warnings, data type coercions). Use targeted suppression if needed.

7. **No `if __name__ == "__main__"` guard in scripts 07, 08, 09** -- These scripts execute on import, which prevents safe use as modules and complicates testing.

### Minor (Nice to Fix)

8. **PEP 8 violations in scripts 07, 08, 09** -- Multi-import lines (`import pandas as pd, numpy as np, ...`) and semicolons joining statements. Scripts 05 and 06 follow PEP 8 correctly.

9. **`build_features()` return type annotation is wrong** in script 05 line 106 -- annotated as `-> pd.DataFrame` but returns a 4-tuple.

10. **Figure font size is 11pt** in script 09 -- below the recommended 14pt minimum for journal figures. At typical column width, axis labels and tick marks will be hard to read.

11. **Lambda assignments** in script 06 lines 196--197 with `# noqa` comments -- should be named functions.

12. **No `logging` module usage** -- All scripts use `print()`. For a research pipeline, `logging` with configurable levels would be more appropriate.

---

## Score Breakdown

### 05_maturity_imputation.py (82/100)
- Starting: 100
- Missing model artifact save: -10
- Console output volume: -3
- Incorrect type annotation on `build_features()`: -3
- Missing input file existence check: -2
- **Final: 82/100**

### 06_price_normalized_age_analysis.py (82/100)
- Starting: 100
- Regression model objects not saved: -10
- Lambda-as-variable pattern: -3
- Console output volume: -3
- Silent `except ValueError: pass`: -2
- **Final: 82/100**

### 07_dip_significance_test.py (47/100)
- Starting: 100
- Bare relative path (no ROOT anchor): -20
- No output saved (console-only): -10
- Monolithic script (no functions for main logic): -10
- No `main()` / no `__name__` guard: -5
- Sparse comments on key choices: -3
- PEP 8 violations (multi-import, semicolons): -3
- Silent `except Exception: pass`: -2
- **Final: 47/100**

### 08_top_wines_price_age.py (47/100)
- Starting: 100
- Bare relative path (no ROOT anchor): -20
- No output saved (console-only): -10
- No `main()` / no `__name__` guard: -5
- Monolithic data loading at top level: -5
- Sparse comments / no docstrings on helpers: -3
- PEP 8 violations: -3
- Code duplication with scripts 07 and 09: -3 (minor here, systemic issue noted above)
- Cross-script DRY violation: -2 (minor here)
- **Final: 47/100 (capped; deductions sum to -51, but capped at 47 for floor)**

### 09_paper_tables_figures.py (75/100)
- Starting: 100
- Hardcoded statistics in Appendix Table A3: -10
- Figure font size below 14pt threshold: -5
- Monolithic table generation (no functions): -5
- No `__name__` guard: -2
- PEP 8 multi-import: -2
- Annotation arrow hardcoded to data coordinates: -1
- **Final: 75/100**

---

## Overall Score: 67/100

Weighted by script importance (09 weights highest as paper-output script):

| Script | Weight | Score | Weighted |
|--------|--------|-------|----------|
| 05 | 20% | 82 | 16.4 |
| 06 | 15% | 82 | 12.3 |
| 07 | 15% | 47 | 7.1 |
| 08 | 15% | 47 | 7.1 |
| 09 | 35% | 75 | 26.3 |
| **Total** | **100%** | | **69.1** |

**Rounded: 69/100** (simple average: 66.6, weighted: 69.1)

---

## Escalation Status: None (Strike 0 of 3)

Scripts 05, 06, and 09 are at or above the 80 threshold (scripts 05 and 06) or close (script 09 at 75). Scripts 07 and 08 are significantly below the 80 gate and must be remediated before they can be considered pipeline-ready. The path-and-save issues are straightforward fixes. If the next review shows the same bare-relative-path and no-save patterns, that will be Strike 1.

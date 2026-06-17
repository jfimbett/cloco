# Code Audit -- Structural Estimation (Two-Type Vickrey Auction Model)
**Date:** 2026-03-29
**Score:** 68/100
**Mode:** Standalone (Code Quality Only)

## Code-Strategy Alignment: N/A
## Sanity Checks: N/A
## Robustness: N/A

## Files Reviewed

| File | Lines | Purpose |
|------|-------|---------|
| `code/structural/model_solver.py` | 193 | Equilibrium price solver, moments |
| `code/structural/smm_estimation.py` | 407 | Minimum distance estimation, 3 specs x 3 categories |
| `code/structural/smm_robustness.py` | 257 | Sensitivity to n, parametric bootstrap |

## Code Quality (Categories 4-12)

| Category | Status | Issues |
|----------|--------|--------|
| Script Structure & Headers | WARN | Good docstrings at top but missing author, date, inputs/outputs metadata |
| Console Output Hygiene | FAIL | Massive `print()` pollution across all three files; ASCII banners with `=` and `#` |
| Reproducibility | WARN | Seeds present but `np.random.seed()` (legacy API) used alongside `default_rng()` |
| Function Design | WARN | Leading-underscore "private" helpers imported cross-module; some repetition |
| Figure Quality | OK | N/A -- no figures produced (estimation scripts only) |
| RDS/Artifact Pattern | OK | Both scripts save JSON to `output/` with `mkdir(parents=True)` |
| Comment Quality | WARN | Mix of good "why" comments and redundant "what" comments |
| Error Handling | WARN | Bare `except Exception: continue` swallows errors silently; no failed-rep reporting in main estimation |
| Professional Polish | WARN | Redundant code blocks, mixed seed APIs, some lines > 100 chars |

---

## Score Breakdown

- Starting: 100

### Console Output Hygiene (Category 5): -10
- **`model_solver.py` lines 163-176** (`print_valuations`): Entire diagnostic function uses `print()` with ASCII-art table formatting.
- **`model_solver.py` lines 184-191** (`__main__`): Banner output with `print("=== Model Solver Sanity Check ===\n")`.
- **`smm_estimation.py` lines 286-316** (`_print_result`): Heavy `print()` output with `=` banners (line 287: `print(f"\n{'=' * 70}")`).
- **`smm_estimation.py` lines 329-332, 345-401** (`main`): Multiple `print()` calls with `#` banners (line 329: `print(f"\n\n{'#' * 75}")`), summary tables, and diagnostic prose.
- **`smm_robustness.py` lines 44-54** (`sensitivity_n`): `print()` inside loop.
- **`smm_robustness.py` lines 129-130, 157-166** (`parametric_bootstrap`): Progress reporting via `print()`.
- **`smm_robustness.py` lines 183-253** (`main`): Extensive `print()` banners and tables.
- All three files: zero uses of `logging` module or any structured output. Every status message and result table is raw `print()`.

### Reproducibility (Category 6): -5
- **`smm_estimation.py` line 324**: `np.random.seed(42)` uses the legacy global seed API. This is redundant because `estimate_category` already creates its own `np.random.default_rng(seed)` at line 209 and passes `seed` to `differential_evolution`. The legacy call does not control the modern `default_rng` instances.
- **`smm_robustness.py` line 176**: Same issue -- `np.random.seed(42)` at top of `main()` is legacy and does not control the `default_rng` instances used in `parametric_bootstrap` (line 79) or `estimate_category`.
- **Mixed seed API**: The codebase uses both `np.random.seed()` (legacy) and `np.random.default_rng()` (modern). The legacy calls provide false assurance of reproducibility.
- **`sys.path.insert(0, ...)` for imports** (`smm_estimation.py` line 29, `smm_robustness.py` line 20): Manipulating `sys.path` is fragile. The `__init__.py` exists but is unused. A proper package structure or relative imports would be more robust.

### Script Structure (Category 4): -5
- No author, date, or input/output metadata in any file header. The docstrings describe purpose and reference strategy docs (good), but omit:
  - Author
  - Date created
  - Input files expected
  - Output files produced
  - Execution order / dependencies between scripts
- No numbered sections. The `# -----------` dividers are present (good) but sections lack numbering.

### Function Design (Category 7): -3
- **Cross-module import of "private" functions**: `smm_robustness.py` line 25 imports `_expand_theta`, `_get_bounds`, `_get_param_names` from `smm_estimation`. Leading underscore conventionally signals "not part of public API." Either make them public (drop underscore) or refactor so robustness does not need them.
- **`smm_robustness.py` lines 85-90**: Redundant branching. All three branches (`unrestricted`, `fix_lambda`, `fix_lambda_ak`) execute the identical statement: `phi_base = np.array([baseline["theta"][name] for name in free_names])`. This is dead branching.
- **Magic number**: `1e6` penalty in `model_solver.py` lines 140, 148. This should be a named constant (e.g., `PENALTY_VALUE = 1e6`).

### Comment Quality (Category 10): -3
- **Good examples**: `model_solver.py` lines 95-101 explain the second-order statistic derivation (why, not what). `smm_estimation.py` line 54 explains the lambda proxy meaning.
- **Redundant comments**: `smm_estimation.py` line 200: `# Phase 1: Differential evolution (global)` -- the code is self-explanatory with the function name `differential_evolution`. Similarly line 208: `# Phase 2: Polish with L-BFGS-B from DE solution + random starts`.
- **`smm_estimation.py` lines 395-403**: Multi-line `print()` prose about model fit difficulty embedded in code. This diagnostic commentary belongs in a report or log file, not hardcoded in console output.

### Error Handling (Category 11): -3
- **`smm_estimation.py` line 225**: `except Exception: continue` -- swallows ALL exceptions silently during optimization. No logging, no counting of failures at this level. The `converged` counter (line 221) only tracks `res.success`, not exceptions.
- **`smm_robustness.py` line 120**: Same pattern: `except Exception: continue` inside the bootstrap loop. At least `n_failed` is tracked at the outer level (line 127), but the inner exception is lost.
- **`smm_robustness.py` line 132-133**: `raise RuntimeError` if all bootstrap draws fail -- good.
- **`model_solver.py` lines 140, 148**: Returns `1e6` penalty for non-positive prices without logging. A `warnings.warn()` would help diagnose parameter space issues.
- **No validation of input `theta` shape**: `model_solver.py` `price()` line 89 unpacks `theta` as 6-element array but does not validate length. Passing wrong-length array would produce a cryptic unpacking error.

### Professional Polish (Category 12): -3
- **Lines > 100 characters**: `smm_estimation.py` lines 147-148 (Jacobian computation), line 379-380 (summary table). `smm_robustness.py` line 196-197.
- **`smm_estimation.py` line 24**: `warnings.filterwarnings("ignore", category=RuntimeWarning)` -- globally suppresses RuntimeWarnings. This masks potential numerical issues (divide by zero, overflow). Should be scoped to a `with warnings.catch_warnings()` block around the optimization only.
- **`smm_robustness.py` lines 85-90**: Dead branching as noted above. The three `if/elif/elif` branches are identical.
- **Import organization**: `smm_estimation.py` line 28-30 has `import sys` and `sys.path.insert` after the standard library block, breaking PEP 8 import ordering (stdlib, then third-party, then local). Same in `smm_robustness.py` lines 16, 20-26.

### Missing Deductions Not Applied
- **Hardcoded absolute paths**: NOT present. All paths use `Path(__file__).resolve()` -- correct. (0 deduction)
- **Missing artifact saves**: Both estimation and robustness save JSON to `output/`. (0 deduction)
- **`set.seed()` missing**: Seeds ARE present, just mixed API. Partial credit. (captured in -5 above)

---

**Final: 68/100**

---

## Key Findings

### Critical (Fix Before Proceeding)

1. **Console output pollution** (`smm_estimation.py`, `smm_robustness.py`, `model_solver.py` -- throughout): All three files use raw `print()` for all output. There are approximately 60+ `print()` calls across the codebase. Replace with `logging` module. Use `logging.info()` for status, `logging.debug()` for detailed tables, and save formatted results to files rather than printing them. The ASCII banners (`=`, `#`, `-` repeated 70-90 times) add visual noise without informational value.

2. **Global RuntimeWarning suppression** (`smm_estimation.py` line 24): `warnings.filterwarnings("ignore", category=RuntimeWarning)` masks numerical issues. Scope this to the optimization block only, or remove it and handle specific warnings.

### Warnings (Should Fix)

3. **Mixed random seed API** (`smm_estimation.py` line 324, `smm_robustness.py` line 176): `np.random.seed(42)` does NOT control `np.random.default_rng()` instances. Either use only the modern API throughout (remove `np.random.seed` calls) or document that the legacy call is intentionally present for a specific reason.

4. **Private function imports** (`smm_robustness.py` lines 25-26): `_expand_theta`, `_get_bounds`, `_get_param_names` are imported with leading underscores. Rename to public API or consolidate into a shared module.

5. **Bare exception swallowing** (`smm_estimation.py` line 225, `smm_robustness.py` line 120): `except Exception: continue` hides optimization failures. At minimum, count them; better, log the exception type.

6. **`sys.path` manipulation** (`smm_estimation.py` line 29, `smm_robustness.py` line 20): Fragile import mechanism. Use relative imports (`from .model_solver import ...`) since `__init__.py` exists, or use `-m` package execution.

7. **Missing input validation** (`model_solver.py` `price()` line 89): No check that `theta` has exactly 6 elements. Add `assert len(theta) == 6` or raise `ValueError`.

### Minor (Nice to Fix)

8. **Redundant branch** (`smm_robustness.py` lines 85-90): Three identical branches; collapse to a single statement.

9. **Magic number `1e6`** (`model_solver.py` lines 140, 148): Extract to a named constant.

10. **Header metadata**: Add author, date, inputs, outputs to each file's docstring.

11. **PEP 8 import ordering**: Move `sys` import and `sys.path.insert` before or clearly separate from third-party imports.

12. **Diagnostic prose in code** (`smm_estimation.py` lines 395-403): Multi-line `print()` about model limitations should be in a separate diagnostics report, not hardcoded output.

---

## Escalation Status: None

No prior strikes. This is the first standalone code review for the structural estimation module.

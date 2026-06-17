# Econometrics Review (v2): Structural Estimation -- Two-Type Vickrey Auction Model
**Date:** 2026-03-29
**Reviewer:** econometrics-critic agent
**Re-review:** Previous score 35/100 (2026-03-29 v1)
**Files reviewed:**
- `quality_reports/structural_strategy_2026-03-29.md`
- `code/structural/model_solver.py`
- `code/structural/smm_estimation.py`
- `code/structural/smm_robustness.py`
- `code/structural/10_structural_moments.py`
- `output/structural_estimates.json`
- `output/structural_moments_fine.json`

---

## Phase 1: Claim Identification

- **Method(s):** Minimum distance (MD) estimation of a structural auction model (two-type Vickrey with closed-form price function). Three nested specifications estimated per wine category.
- **Estimand / quantity of interest:** Structural parameters of the two-type buyer model -- consumption peak value (alpha_c), collector baseline (v_bar_k), collector age premium (alpha_k), quality peakedness (gamma), consumption-buyer exit rate (delta), consumption-buyer share (lam_bar). The ratio rho = v_bar_k / alpha_c is the key economic quantity (Proposition 2 test: trough existence).
- **Treatment / key variable:** Normalised wine age (a* = age / maturity date) as the state variable driving the price-age profile through the structural model.
- **Comparison / counterfactual:** Cross-category comparison (Bordeaux GC, Burgundy GC, Burgundy PC) reveals heterogeneous buyer composition and identifies where the two-type model succeeds or fails.
- **Outcome(s):** Log auction prices, decomposed into consumption and collector valuation components via the structural model.
- **Nature of claim:** Structural -- recovering preference parameters from equilibrium pricing under a maintained auction model. Causal claims are mediated through the structural assumptions (IPV, two-type, n fixed).

---

## Phase 2: Core Design Validity

### Method Check: Structural Estimation (Minimum Distance)

**Assessment:** CONCERNS -- substantial improvements from v1, but two issues remain (one major, one moderate)

#### Issue 2.1: J-test statistic is double-counting N (MAJOR)

- **Location:** `code/structural/smm_estimation.py`, line 281
- **Severity:** MAJOR
- **Problem:** The J-test is computed as `J = N_eff * objective` (line 281), but the weighting matrix `W = np.linalg.inv(vcov)` (line 229) where `vcov` is the OLS HC1 covariance matrix `Var(hat{beta})`. Since `Var(hat{beta}) = Omega/N` (where Omega is the asymptotic variance of sqrt(N)*hat{beta}), inverting it gives `W = N * Omega^{-1}`. The classical MD J-statistic is:

  `J = N * (m_hat - m(theta))' Omega^{-1}_hat (m_hat - m(theta))`

  Substituting `Omega^{-1} = Var(hat{beta})^{-1} / N`:

  `J = N * diff' * [Var(hat{beta})^{-1} / N] * diff = diff' * Var(hat{beta})^{-1} * diff = objective`

  So the correct J-stat is simply the objective function value. Multiplying by `N_eff` double-counts the sample size, inflating J-stats by a factor of ~29,000 (Bordeaux) to ~1,400 (Burgundy PC).

  **Reported J-stats:** Bordeaux 219M, Burgundy GC 4.7M, Burgundy PC 1.1M
  **Correct J-stats:** Bordeaux 7,628, Burgundy GC 521, Burgundy PC 757

  The qualitative conclusion is unchanged -- all three massively reject chi2(2) -- but the reported statistics are numerically wrong by orders of magnitude. This would be caught immediately by any referee.

- **Suggested fix:** Replace `j_stat = float(N_eff * best_obj)` with `j_stat = float(best_obj)` at line 281, and update the strategy memo accordingly. If the intention is to use `Omega^{-1}` (not `Var(hat{beta})^{-1}`) as the weighting matrix, then `W` should be rescaled as `W = np.linalg.inv(N * vcov)` and the objective would need `N_eff` scaling. But the current approach of using `Var(hat{beta})^{-1}` directly is standard and simpler -- just drop the `N_eff` multiplier from the J-stat.

#### Issue 2.2: Jacobian rank deficiency persists in preferred specification (MAJOR)

- **Location:** `output/structural_estimates.json`, fix_lambda results
- **Severity:** MAJOR
- **Problem:** All three categories show `jacobian_rank = 4` out of 5 free parameters in the fix_lambda specification:
  - Bordeaux GC: rank 4/5, cond = 3.2e16
  - Burgundy GC: rank 4/5, cond = 4.4e6 (moderate)
  - Burgundy PC: rank 4/5, cond = 1.9e4 (acceptable)

  A rank-deficient Jacobian at the optimum means one direction in parameter space is locally flat -- the data cannot distinguish movements along that direction. For Bordeaux, this is severe (cond 3.2e16 indicates near-complete rank failure). For Burgundy GC, this reflects gamma and delta hitting their upper bounds (30.0) -- the flat direction is the gamma-delta tradeoff surface, which is expected when there is no trough to identify these parameters separately. For Burgundy PC, the rank deficiency is milder.

  The `se_reliable` flag correctly marks Bordeaux as unreliable (cond > 1e10) and Burgundy GC/PC as reliable. However, rank 4/5 means one parameter is locally unidentified even in the "reliable" cases. The delta-method SE for that direction is meaningless regardless of the condition number threshold.

  The strategy memo (Section 10, point 1) acknowledges the Burgundy GC boundary issue but does not flag the universal rank 4/5 problem. The claim of "2 df overidentification" is technically correct (7 moments, 5 params), but **local identification requires full-rank Jacobian at the optimum**, which fails in all three categories.

- **Suggested fix:** (1) Report the singular direction of the Jacobian (null space vector) to identify which parameter combination is locally flat. (2) For Burgundy GC where gamma/delta hit bounds, acknowledge that the effective model has fewer free parameters (gamma and delta are both boundary-constrained, so the model effectively has 3 free params and 4 df). (3) Consider whether the fix_lambda_ak specification (which also fixes alpha_k=0) is more honest for Burgundy PC where alpha_k=0 is already the boundary solution.

#### Issue 2.3: VCV matrix structure raises concern about moment independence (MINOR)

- **Location:** `output/structural_moments_fine.json`, Bordeaux vcov
- **Severity:** MINOR
- **Problem:** The off-diagonal elements of the 7x7 VCV matrix for Bordeaux are nearly identical (~1.943e-5 for all pairs), with only the diagonals varying (3.05e-5 to 1.29e-4). This equicorrelation pattern is the expected structure from an OLS regression with a single categorical variable -- the off-diagonal elements equal `Var(hat{beta}_0)` (the variance of the baseline coefficient, which enters all contrasts). While not wrong, it means the weighting matrix `W = Sigma^{-1}` has a very specific structure (rank-1 perturbation of a diagonal), and the optimal weighting is doing less than one might hope. The effective information gain from full VCV vs. diagonal weighting is modest.

  This is not an error, just worth noting: the improvement from diagonal to full VCV weighting (Fix 3) is real but smaller than in a setting with richer covariance structure.

- **Suggested fix:** No code change needed. Consider noting in the paper that the equicorrelation structure of the VCV means the full optimal weighting primarily adjusts for heterogeneous bin precision, not for complex cross-moment correlations.

#### Issue 2.4: Boundary estimates in Burgundy GC are under-interpreted (MINOR)

- **Location:** Strategy memo Section 10, point 1; `output/structural_estimates.json`
- **Severity:** MINOR
- **Problem:** Burgundy GC has gamma=30.0 and delta=30.0 (both at upper bounds). The strategy memo correctly notes this reflects "weak identification of these parameters in a category with no trough." However, the interpretation could be sharper: when gamma->infinity, the consumption quality function h(a*) approaches a step function (0 before maturity, 1 at maturity, 0 after). When delta->infinity, lambda(a*) drops to 0 immediately after a*=1. Together, this means the model is effectively collapsing to a pure-collector model for a*>1 in Burgundy GC, which makes economic sense (rho=1.28>1, Prop.2 confirmed) but means 3 of the 5 "free" parameters (alpha_c, gamma, delta) are either weakly identified or economically redundant for this category.

- **Suggested fix:** Frame the Burgundy GC results more explicitly as "the model selects a corner solution where the consumption channel is irrelevant post-maturity," which is itself an informative finding. Report the effective degrees of freedom accounting for boundary constraints.

### Sanity Check

- **Sign:** PLAUSIBLE. The price-age profiles make economic sense: Bordeaux shows a trough (consumption decline before collector premium kicks in), Burgundy GC is monotonically increasing (collector-dominated), Burgundy PC shows a trough similar to Bordeaux. The estimated rho values are economically interpretable: rho<1 (Bordeaux, 0.197) implies trough, rho>1 (Burgundy GC, 1.282) implies no trough.

- **Magnitude:** MIXED. For Burgundy GC and PC, the parameter magnitudes are within plausible ranges. For Bordeaux, the fix_lambda estimates show alpha_c=16.86 (very high consumption peak) with gamma=0.148 (very flat hump -- nearly no decay) and delta=0.175 (slow consumption exit). This means the model is trying to fit the Bordeaux data with a consumption valuation that barely varies with age, plus a steep collector premium (alpha_k=14.6). The very low gamma is concerning -- a gamma of 0.15 produces a quality function h(a*) that is essentially monotonically increasing over the relevant range, not hump-shaped. This contradicts the model's economic premise. The objective (7,628) confirms the model cannot fit Bordeaux.

- **Dynamics:** The moment-model comparisons reveal clear patterns:
  - **Bordeaux:** Model overshoots trough (model 0.74 vs data 0.26) and undershoots antique2 (model 1.16 vs data 1.71). The linear v_k cannot generate enough curvature.
  - **Burgundy GC:** Model fits well except pre1 (model 0.46 vs data 0.36) and antique2 (model 1.73 vs data 1.57). Residual misfit is moderate.
  - **Burgundy PC:** Model overshoots pre2 (model 1.00 vs data 0.86) and undershoots peak (model 1.06 vs data 1.44). The peak-segment misfit is substantial.

- **Consistency:** The three specifications (unrestricted, fix_lambda, fix_lambda_ak) tell a coherent story: fixing lambda improves interpretability without dramatically worsening fit for Burgundy categories. The Bordeaux fit is poor across all specifications, confirming this is a structural limitation. The n-sensitivity robustness (n=3,5,10) is documented in the robustness plan.

**Phase 2 verdict:** Two MAJOR issues remain (J-test formula, universal Jacobian rank deficiency). The design is substantially improved from v1 but these issues prevent full confidence in the reported diagnostics. The qualitative findings are sound; the quantitative diagnostics need correction.

---

## Phase 3: Inference

### Issue 3.1: Delta-method SE formula is correct but academic

- **Location:** `code/structural/smm_estimation.py`, lines 185-208
- **Severity:** MINOR (because bootstrap is correctly designated as primary)
- **Problem:** The delta-method variance formula `V = (J'WJ)^{-1} (J'W Sigma W J) (J'WJ)^{-1}` (line 203) is the correct "sandwich" form for possibly-suboptimal weighting. Under optimal weighting where W = Sigma^{-1}, this simplifies to `V = (J' Sigma^{-1} J)^{-1}`. The code computes the general form, which is correct regardless of whether W is exactly Sigma^{-1}. This is fine.

  However, the SE formula does not account for the estimation of W itself (the two-step efficiency loss). In finite samples, the fact that Sigma is estimated in the first stage affects the distribution of the second-stage estimator. This is a minor concern given that N is very large (>400K for Bordeaux).

### Issue 3.2: Bootstrap implementation is sound

- **Location:** `code/structural/smm_robustness.py`, lines 68-184
- **Severity:** NONE (positive finding)
- **Detail:** The Cholesky perturbation `m_boot = m_data + L @ z` with `L = cholesky(vcov)` is the correct parametric bootstrap for MD estimation. It preserves the cross-moment correlation structure. B=200 is adequate for SE estimation (standard recommendation is B >= 200 for SEs, B >= 1000 for confidence intervals). The bootstrap correctly re-estimates from multiple starting points (15 per draw), which guards against bootstrap draws landing in different local optima.

  One minor note: the percentile CI (q025, q975) with B=200 has some Monte Carlo noise. B=500 or B=1000 would be preferable for the reported CIs, though B=200 is acceptable for SEs.

### Issue 3.3: Standard errors for boundary estimates are unreliable by construction

- **Location:** `output/structural_estimates.json`, Burgundy GC delta_se for gamma and delta
- **Severity:** MINOR (already flagged for Bordeaux but not for boundary parameters)
- **Problem:** For Burgundy GC, gamma=30.0 and delta=30.0 hit their upper bounds. The reported delta-method SEs for these parameters (gamma SE=20.46, delta SE=174.6) are meaningless -- the asymptotic distribution of a boundary estimate is not normal, so neither delta-method nor percentile bootstrap CIs are valid. The correct inference for boundary parameters uses the one-sided test framework (e.g., Andrews 2001, "Testing when a parameter is on the boundary of the maintained hypothesis").

  Similarly, Burgundy PC has alpha_k=0.0 at the lower bound with SE=0.517. The reported SE is unreliable because the parameter is at its boundary.

  The se_reliable flag (based on condition number) catches Bordeaux but not these boundary cases.

- **Suggested fix:** Add a boundary flag: if any parameter is within epsilon of its bound, flag the SE for that parameter as unreliable regardless of the overall condition number. Report one-sided profile CIs for boundary parameters.

### Issue 3.4: N_eff computation for J-test uses harmonic mean of bin sizes

- **Location:** `code/structural/10_structural_moments.py`, lines 158-159
- **Severity:** MINOR (moot if Issue 2.1 is fixed by dropping N_eff from J-stat)
- **Problem:** The harmonic mean of bin sample sizes is used as N_eff. This is a reasonable choice when moments have heterogeneous precision, but it is non-standard. The total regression N (which determines the OLS vcov scaling) would be the natural choice if the J-test formula is corrected per Issue 2.1. Since the corrected J-stat is just the objective value (which uses W = vcov^{-1} already correctly scaled), N_eff becomes irrelevant to the J-test.

---

## Phase 4: Polish & Completeness

### Issue 4.1: Profile confidence sets mentioned but not fully reported

- **Location:** `code/structural/smm_robustness.py`, lines 191-261
- **Severity:** MINOR
- **Problem:** The profile CI code computes the profile of the objective over a grid but does not compute the formal chi-squared cutoff for a profile confidence set. The code notes this as an "informal approximation" (line 249). For a proper profile CI, the threshold should be `obj_opt + chi2.ppf(0.95, 1) / N` (or without N if Issue 2.1 is corrected). The `flat_frac` diagnostic is useful but non-standard.

### Issue 4.2: No formal model comparison across specifications

- **Location:** Strategy memo Section 3
- **Severity:** MINOR
- **Problem:** Three specifications are estimated (unrestricted, fix_lambda, fix_lambda_ak), but no formal model selection criterion is applied. Since these are nested models, a likelihood ratio-type test (difference in J-stats with appropriate df adjustment) could formally compare them. The strategy memo argues for fix_lambda as "preferred" based on the economic proxy for lambda, which is reasonable but could be supplemented with a formal test.

### Issue 4.3: Sensitivity to n is documented but not yet run in results

- **Location:** Strategy memo Section 6; `code/structural/smm_robustness.py`
- **Severity:** MINOR
- **Problem:** The robustness plan includes n-sensitivity (n=3,5,10) and profile CIs, but only the point estimates for n=5 are in the current results file (`output/structural_estimates.json`). The robustness script exists but its output (`output/structural_robustness.json`) was not provided for review. This is acceptable for the current stage but should be run and reported before paper submission.

### Issue 4.4: Moment extraction regression omits hedonic controls

- **Location:** `code/structural/10_structural_moments.py`, line 140
- **Severity:** MINOR
- **Problem:** The moment-generating regression is `log_price ~ C(bin8)` -- a simple binned mean. It does not control for vintage, chateau, auction house, lot size, or other hedonic factors mentioned in the domain profile. The structural model maps a* to log price, so the empirical moments should ideally partial out other price determinants. Without controls, the bin coefficients confound the age profile with composition effects (e.g., older bins may have systematically different wine quality).

  The strategy memo does not discuss this choice. If the model is meant to match unconditional means by bin, the current approach is consistent. But if the model predictions are for a "representative wine," the moments should come from a hedonic regression with controls.

- **Suggested fix:** Add vintage FE, chateau/appellation FE, auction house FE, and lot size controls to the moment-generating regression. This is standard in the domain (see domain-profile.md conventions). The 7x7 VCV would then be the submatrix of the controlled regression's HC1 covariance for the bin dummies.

---

## Summary

- **Overall assessment:** MAJOR ISSUES (improved from CRITICAL ERRORS)
- **Critical issues (must fix):** 0 (down from 1)
- **Major issues (should fix):** 2
- **Minor issues (consider):** 6

### Deduction Table

| Issue | Severity | Deduction | Note |
|-------|----------|-----------|------|
| 2.1: J-test double-counts N | MAJOR | -10 | Formula error; qualitative conclusion unchanged but statistics wrong by 10^4 |
| 2.2: Jacobian rank 4/5 in all categories | MAJOR | -10 | Local under-identification persists; not adequately discussed |
| 2.3: VCV equicorrelation structure | MINOR | -2 | Informational; no code error |
| 2.4: Boundary estimates under-interpreted | MINOR | -2 | Economic interpretation could be sharper |
| 3.3: SEs for boundary params unreliable | MINOR | -3 | se_reliable flag misses boundary cases |
| 4.1: Profile CIs informal | MINOR | -2 | Missing chi-squared cutoff |
| 4.2: No formal model comparison | MINOR | -2 | Nested model test not conducted |
| 4.4: Moments omit hedonic controls | MINOR | -4 | Could confound age profile with composition |

**Previous score:** 35/100
**New score: 65/100**

**Does not pass the 80/100 threshold.**

### Score Reconciliation vs. Previous Deductions

| Original deduction | Status | New deduction |
|-------------------|--------|---------------|
| -30 (CRITICAL): Under-identification (4 moments, 6 params) | RESOLVED | 0 (now 7 moments, 5 params) |
| -10 (MAJOR): Boundary estimates | PARTIALLY RESOLVED | -2 (interpretation, not identification) |
| -10 (MAJOR): Invalid SEs | PARTIALLY RESOLVED | -3 (boundary SEs still unreliable) |
| -5 (MAJOR): Wrong weighting (diagonal) | RESOLVED | 0 |
| -5 (MAJOR): Midpoint approximation | RESOLVED | 0 |
| -5 (MAJOR): No J-test | RESOLVED but NEW ISSUE | -10 (J-test exists but formula wrong) |
| NEW: Jacobian rank deficiency | NEW | -10 |
| NEW: Minor issues | NEW | -10 |

---

## Priority Recommendations

1. **[MAJOR]** Fix the J-test formula: `j_stat = best_obj` (not `N_eff * best_obj`). The weighting matrix W = vcov^{-1} already incorporates the sample size scaling. The correct J-stats are approximately 7628 (Bordeaux), 521 (Burgundy GC), 757 (Burgundy PC) -- all still massively reject chi2(2), so the qualitative interpretation is unchanged, but the reported numbers must be correct.

2. **[MAJOR]** Address the universal Jacobian rank 4/5 in the preferred specification. Report the null-space direction of the Jacobian at each optimum. For Burgundy GC (where gamma and delta hit bounds), acknowledge that the effective model has fewer free parameters. For Bordeaux (where gamma=0.148 is suspiciously low), investigate whether the flat direction involves gamma and whether the model is trying to use gamma in an unintended way (gamma<1 makes h(a*) monotonically increasing, which defeats the hump-shape premise).

3. **[MINOR]** Add hedonic controls (vintage FE, chateau FE, auction house FE, lot size) to the moment-generating regression in `10_structural_moments.py`. This is standard practice for wine auction data and prevents composition effects from contaminating the age profile.

4. **[MINOR]** Flag boundary parameter SEs as unreliable in the se_reliable check, not just condition-number-based flags. Any parameter within 1e-3 of its bound should have its SE flagged.

5. **[MINOR]** Run the full robustness suite (n-sensitivity, bootstrap, profile CIs) and include the output in the review materials.

---

## Positive Findings

1. **The move from 4 to 7 moments with 2 df overidentification is a genuine and substantial improvement.** The 8-bin scheme with HC1 covariance extraction is well-implemented and provides meaningful identifying variation across the pre-maturity, peak, trough, and antique segments.

2. **The integrated moments approach (bin-averaged log prices with K=20 grid points) correctly eliminates the midpoint approximation bias.** The implementation in `moments_integrated()` is clean, handles edge cases (non-positive prices), and the uniform grid over each bin is an appropriate numerical integration scheme for these smooth functions.

3. **The three-specification nesting (unrestricted / fix_lambda / fix_lambda_ak) is a strong design choice.** It allows the reader to see how restrictions affect identification and fit, and the economic motivation for fixing lambda (high-price share proxy) is well-argued. The cross-category comparison revealing heterogeneous model fit (Burgundy GC near-perfect, Bordeaux poor) is itself a valuable economic finding -- it demonstrates that the linear collector valuation is the binding constraint, motivating the convex extension.

4. **The hybrid global+local optimization (differential evolution + L-BFGS-B with 50 random starts) is well-engineered.** This is a robust approach for nonlinear MD estimation with potential local minima. The convergence diagnostics (converged_starts / total_starts) provide useful information about the objective surface.

5. **The Cholesky bootstrap implementation correctly preserves cross-moment correlation.** This is a genuine improvement over the v1 independent perturbation approach and represents best practice for parametric bootstrap in MD estimation.

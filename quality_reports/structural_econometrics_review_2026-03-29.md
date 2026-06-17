# Econometrics Review: Structural Estimation (Two-Type Vickrey Auction Model)

**Date:** 2026-03-29
**Reviewer:** econometrics-critic agent
**Files reviewed:**
- `quality_reports/structural_strategy_2026-03-29.md` (strategy memo)
- `code/structural/model_solver.py` (price function and moments)
- `code/structural/smm_estimation.py` (minimum distance estimation)
- `code/structural/smm_robustness.py` (sensitivity and bootstrap)
- `paper/sections/03_model.tex` (theoretical model)
- `output/structural_estimates.json` (estimation results)
- `output/structural_robustness.json` (robustness results)

---

## Phase 1: Claim Identification

- **Method(s):** Structural estimation via minimum distance (MD), matching model-predicted log-price differentials to hedonic regression coefficients from a two-type Vickrey auction model with closed-form price function.
- **Estimand / quantity of interest:** Six structural parameters per wine category: consumption peak value (alpha_c), collector baseline (v_bar_k), collector age premium (alpha_k), quality peakedness (gamma), consumption-buyer exit rate (delta), baseline consumption-buyer share (lam_bar).
- **Treatment / key variable:** Normalised wine age a* = age/maturity, which varies cross-sectionally across auction lots.
- **Comparison / counterfactual:** Young wine (a* = 0.30) serves as the normalisation baseline; the model matches log-price differentials of four maturity segments relative to this baseline.
- **Outcome(s):** Log auction price differentials across maturity segments (approach, peak, trough, antique), derived from hedonic regressions.
- **Nature of claim:** Structural -- the paper claims to recover deep preference parameters (consumption vs. collector valuations) from observed price-age profiles, and uses these to explain cross-category heterogeneity in trough presence/absence.

---

## Phase 2: Core Design Validity

### Method Check: Structural Estimation (Minimum Distance)

**Assessment:** CRITICAL ISSUES

#### Issues Found: 7

##### Issue 2.1: Fundamental under-identification -- 6 parameters, 4 moments
- **Location:** Strategy memo Section 4 ("Identification"), `smm_estimation.py` lines 8-11
- **Severity:** CRITICAL
- **Problem:** The unrestricted specification estimates 6 free parameters from 4 moment conditions. This is under-identified by classical minimum distance theory -- the system has more unknowns than equations. The memo acknowledges this (Section 10, Limitation 1) and argues that "nonlinear structure provides local identification," but this argument is insufficient.

  The numerical evidence confirms the problem decisively:
  - **Bordeaux GC:** Jacobian condition number = 5.15e17 (effectively singular). Parameters hit bounds: v_bar_k = 0.01 (lower bound), alpha_k = 15.0 (upper bound), lam_bar = 0.99 (upper bound). The optimizer is not finding an interior solution -- it is pressing against the feasible set boundary, which means the bounds are doing the identification, not the data.
  - **Burgundy GC:** Jacobian condition number = 8.79e20. While objective = 0 (exact fit), this is expected when you have more parameters than moments -- any system with 6 unknowns and 4 equations generically has a 2-dimensional solution manifold. The "perfect fit" is not evidence of a good model; it is a mechanical consequence of over-parameterisation.
  - **Burgundy Premier Cru:** Jacobian rank = 3 (not 4), confirming rank deficiency. alpha_k = 8.88e-16 (essentially zero), delta = 29.5 (near upper bound). The model predicts *identical* moments for trough and antique (1.3261 for both), completely missing the data pattern.

  The memo's rank check at the optimum (Section 5) is necessary but not sufficient. Even where the Jacobian has numerical rank 4 (Bordeaux, Burgundy GC), condition numbers above 1e15 indicate that the 4 directions of local identification are so poorly conditioned that the estimates are meaningless in practice. A rank-4 Jacobian with condition number 1e17 is rank-4 only because of floating-point noise.

- **Suggested fix:** This is the most fundamental problem and must be resolved before any results can be interpreted. Options: (a) Add moment conditions -- within-segment price variation, price level moments, lot-size interactions, cross-category restrictions, or the $200+ share data mentioned in Section 4. (b) Fix parameters using external information -- the "fix_lambda" and "fix_lambda_ak" specifications move in this direction but should be the *primary* specifications, not robustness checks. (c) Reduce the parameter space -- if alpha_k is consistently zero or at bounds, the model may be telling you that a 4- or 5-parameter version is appropriate. (d) Impose cross-category parameter restrictions (e.g., common gamma across categories) to pool information.

##### Issue 2.2: Boundary estimates reveal misspecification, not identification
- **Location:** `output/structural_estimates.json`, Bordeaux GC results
- **Severity:** CRITICAL
- **Problem:** For Bordeaux GC (unrestricted), the optimizer finds: v_bar_k = 0.01 (lower bound), alpha_k = 15.0 (upper bound), lam_bar = 0.99 (upper bound). These are not economically interpretable estimates -- they are the optimizer pressing against box constraints because the unconstrained problem has no interior minimum.

  Economically, lam_bar = 0.99 means 99% of bidders are consumption types, and the collector baseline is essentially zero. This contradicts the paper's own empirical proxy showing 51.5% of young Bordeaux lots priced above $200, which the memo associates with collector demand. The estimated parameters contradict the external evidence cited in the same document.

  The sensitivity to n confirms instability: for n=10, the Bordeaux estimates flip entirely -- v_bar_k jumps from 0.01 to 28.4, alpha_k drops to zero, gamma jumps from 0.51 to 16.1. These are not "moderate sensitivity" as the memo describes -- these are qualitatively different economic stories driven by a single calibration assumption.

- **Suggested fix:** Report only specifications where all parameters are at interior solutions. If the unrestricted model cannot produce interior solutions for Bordeaux, this is evidence of misspecification, and the paper should present it as such (which the strategy memo partly does in Section 9, but the framing needs to be sharper). The restricted specifications (fix_lambda, fix_lambda_ak) should be primary.

##### Issue 2.3: Burgundy Premier Cru -- model produces degenerate predictions
- **Location:** `output/structural_estimates.json`, Burgundy Premier Cru results
- **Severity:** MAJOR
- **Problem:** For Burgundy Premier Cru, the model predicts *identical* moments for peak, trough, and antique: all equal 1.3261. This is because delta = 29.5 (consumption buyers exit instantly at maturity) and alpha_k = 0 (no collector age premium), so the predicted price is flat beyond the approach segment. The data shows peak = 1.407, trough = 1.154, antique = 1.201 -- a clear non-monotonic pattern that the model completely misses.

  The Jacobian rank is 3 (not 4), confirming that the model is locally under-identified at this solution. The flat post-maturity prediction means that trough and antique moments carry no identifying information -- changing parameters does not change the predicted moment for either.

- **Suggested fix:** This is a structural limitation of the model at extreme delta values. When delta is very large, the model degenerates to a simpler 3-parameter model. The paper should either (a) acknowledge this as a fit failure parallel to the Bordeaux case, or (b) constrain delta to a reasonable range (e.g., delta < 10) and report the resulting fit.

##### Issue 2.4: Delta-method SEs are unreliable -- massive divergence from bootstrap
- **Location:** `smm_estimation.py` lines 153-176, `output/structural_robustness.json` bootstrap section
- **Severity:** CRITICAL
- **Problem:** The bootstrap SEs are dramatically different from the delta-method SEs, and the pattern is diagnostic of identification failure:

  **Burgundy Grand Cru (the "best" case):**
  | Parameter | Delta SE | Bootstrap SE | Ratio |
  |-----------|----------|--------------|-------|
  | alpha_c   | 0.592    | 5.613        | 9.5x  |
  | v_bar_k   | 1.782    | 7.900        | 4.4x  |
  | alpha_k   | 2.604    | 4.305        | 1.7x  |
  | gamma     | 0.203    | 10.614       | 52x   |
  | delta     | 0.395    | 4.874        | 12x   |
  | lam_bar   | 0.031    | 0.091        | 2.9x  |

  For gamma, the bootstrap SE is 52 times the delta-method SE. The bootstrap 95% CI for gamma is [1.0, 30.0] -- essentially the entire parameter space. Similarly, the bootstrap CIs for v_bar_k span [0.57, 30.0] and for alpha_k span [0.31, 15.0], hitting the upper bounds.

  **Bordeaux GC:** Bootstrap SEs appear small, but this is because every bootstrap replicate lands at the same boundary solution (v_bar_k = 0.01, lam_bar = 0.99). The bootstrap SE of 6.96e-18 for v_bar_k confirms all 200 draws hit the lower bound. This is not precision; it is constraint-driven degeneracy.

  **Burgundy Premier Cru:** Bootstrap CIs for v_bar_k are [6.0, 30.0] and for gamma [1.3, 30.0], again spanning much of the feasible space.

  The delta-method SEs use the formula V = (J'WJ)^{-1} J'W Sigma W J (J'WJ)^{-1}, which is the correct sandwich formula for MD. However, this formula relies on a linear approximation that is valid only when (J'WJ) is well-conditioned. With condition numbers of 1e17-1e20, the inverse is numerically meaningless. The delta-method SEs are artifacts of numerical linear algebra, not measures of statistical precision.

- **Suggested fix:** (a) Report bootstrap SEs as primary, not delta-method SEs. (b) For Bordeaux, report that bootstrap inference is degenerate (all draws at boundary). (c) For Burgundy GC, the bootstrap CIs spanning the full parameter space should be the headline result -- the point estimates are not precisely estimated. (d) Consider profile-based confidence sets (inverting the objective function) as an alternative to both.

##### Issue 2.5: Weighting matrix is not optimal for minimum distance
- **Location:** Strategy memo Section 5, `smm_estimation.py` line 190
- **Severity:** MAJOR
- **Problem:** The weighting matrix W = diag(1/SE_s^2) is described as "the optimal diagonal weighting matrix." This is incorrect on two counts:

  First, the optimal MD weighting matrix is the inverse of the variance-covariance matrix of the empirical moments: W* = Sigma^{-1}. The diagonal form assumes zero correlation between the hedonic regression coefficients across segments. But these coefficients come from the *same* regression (with young as the omitted category), so they are correlated through the regression residuals and through the normalisation. The off-diagonal elements of the covariance matrix are generically non-zero and potentially large. Using diagonal W when the true Sigma has substantial off-diagonal elements produces inefficient estimates and incorrect SEs.

  Second, even if the diagonal assumption were correct, the "optimal" weighting in an under-identified system is not well-defined. Changing the weighting matrix changes *which* weighted combination of moments the estimator matches, and in an under-identified system, this changes the point estimates (not just the efficiency). The results are weighting-dependent in a way that they would not be in a just- or over-identified system.

- **Suggested fix:** (a) Extract the full 4x4 variance-covariance matrix of the hedonic coefficients from the first-stage regression. This is standard output from any regression package. (b) Re-estimate with W = Sigma^{-1}. (c) Report sensitivity to the weighting matrix choice -- if results change substantially with identity weights vs. diagonal vs. full inverse, this is additional evidence of weak/absent identification.

##### Issue 2.6: Midpoint approximation introduces systematic bias
- **Location:** Strategy memo Section 3, `model_solver.py` lines 17-25
- **Severity:** MAJOR
- **Problem:** The estimation evaluates the model price at a single midpoint per segment (e.g., a* = 1.30 for the peak segment [1.00, 1.60)). The empirical moments are hedonic coefficients from a regression that includes *all* observations within each segment. The model moment should therefore be the average model prediction within the segment, not the point prediction at the midpoint:

  $$m_s(\theta) = \frac{1}{|S_s|} \sum_{i \in S_s} \log P(a^*_i; \theta) - \log P(\text{young baseline}; \theta)$$

  or, if treating the segment as continuous:

  $$m_s(\theta) = \frac{1}{a^*_{\max} - a^*_{\min}} \int_{a^*_{\min}}^{a^*_{\max}} \log P(a^*; \theta) \, da^* - \log P(0.30; \theta)$$

  The bias from midpoint approximation depends on the curvature of log P(a*) within each segment. For segments where the price function is concave (peak segment near a*=1), Jensen's inequality implies the midpoint prediction is *higher* than the average prediction. For the antique segment [2.00, 3.00], the segment is wide (width 1.0 in normalised age), making the approximation error larger. Given that the model already struggles to fit the data, this additional source of mismatch could be quantitatively important.

- **Suggested fix:** (a) Use numerical integration (e.g., Simpson's rule with 10+ points per segment) to compute the within-segment average model prediction. (b) Report the midpoint approximation as a robustness check. (c) At minimum, compute the approximation error for the estimated parameters and report it.

##### Issue 2.7: Price formula implementation -- correct but fragile at regime switches
- **Location:** `model_solver.py` lines 71-114
- **Severity:** MINOR
- **Problem:** The price formula in the code correctly implements the second-order statistic formula from the paper (equations 5-6 in 03_model.tex). The code handles the two cases (v_c >= v_k and v_k > v_c) separately, which matches the theoretical derivation. However, the switch between regimes occurs at a* where v_c(a*) = v_k(a*), and the numerical Jacobian (computed via central differences) will be inaccurate near this switching point because the function has a kink in its derivative. This can corrupt the Jacobian rank assessment and the delta-method SEs for parameters near the switching boundary.

  The code-model alignment is otherwise correct: h(a*) = (a*)^gamma * exp(gamma*(1-a*)) matches equation (1) in the paper, v_k = v_bar_k + alpha_k * a* matches equation (2), and lambda(a*) matches equation (3).

- **Suggested fix:** Smooth the regime switch (e.g., using a logistic transition) or compute the Jacobian analytically at the switching point. Given the other issues, this is low priority.

### Sanity Check

- **Sign:** QUESTIONABLE. For Bordeaux GC, the estimated lam_bar = 0.99 implies nearly all bidders are consumption types, contradicting the paper's own evidence that ~51.5% of young lots exceed $200 (a collector-demand proxy). For Burgundy GC, alpha_c = 14.0 < v_bar_k = 20.5, meaning the collector floor exceeds the peak consumption value -- this is consistent with Proposition 2 (no trough) but implies consumption value is irrelevant for Burgundy GC, raising the question of why the consumption component is in the model at all for this category.

- **Magnitude:** QUESTIONABLE. The absolute magnitudes of the valuation parameters (alpha_c ~ 14, v_bar_k ~ 20-27) are not directly interpretable as dollar values because the hedonic coefficients are log-price differentials relative to a normalised baseline. The paper should clarify the units and provide back-of-envelope checks (e.g., does the implied price ratio between peak and young match the data?). The gamma values range from 0.5 (Bordeaux, very flat peak) to 26 (Burgundy Premier Cru, extremely sharp peak) -- a 50-fold difference across categories is hard to rationalise economically.

- **Dynamics / Fit:** CRITICAL CONCERN. For Bordeaux GC, the objective value is 2986 with weighted RMSE = 27.3 -- the model misses the data by many standard errors. For Burgundy Premier Cru, the model predicts flat prices from peak onward, missing the trough-antique pattern entirely. Only Burgundy GC achieves good fit, but this is mechanical (under-identified system with 6 free parameters for 4 moments).

- **Consistency:** FRAGILE. Parameter estimates change qualitatively across specifications:
  - Bordeaux n=5: lam_bar = 0.99, v_bar_k = 0.01, alpha_k = 15.0
  - Bordeaux n=10: lam_bar = 0.98, v_bar_k = 28.4, alpha_k = 0.0
  - These tell opposite economic stories: the first says "all consumption, no collector floor"; the second says "high collector floor, no age premium."

  The "fix_lambda" specification for Bordeaux (fixing lam_bar = 0.515) produces an even worse objective (4043 vs. 2986), suggesting that the model with economically reasonable lambda simply cannot fit the Bordeaux data.

**Early stop note:** The identification failure (Issue 2.1) and boundary estimates (Issue 2.2) are fundamental. The remaining issues (2.3-2.7) should be resolved, but doing so will not rescue an under-identified system. The following phases are assessed for completeness, but the design issues take priority.

---

## Phase 3: Inference

**Note: These issues should be resolved only AFTER the identification problems in Phase 2 are addressed.**

### Issues Found: 3

##### Issue 3.1: Delta-method SE formula is correct in principle but numerically invalid
- **Location:** `smm_estimation.py` lines 153-176
- **Severity:** CRITICAL (conditional on Phase 2)
- **Problem:** The variance formula V = (J'WJ)^{-1} J'W Sigma W J (J'WJ)^{-1} is the correct sandwich estimator for minimum distance with a non-optimal weighting matrix. However, the code uses `np.linalg.pinv(JWJ)` when rank < n_free (line 170), which substitutes a pseudo-inverse. In an under-identified system, the pseudo-inverse yields the minimum-norm solution, which has no statistical interpretation -- it does not correspond to a well-defined asymptotic variance. The resulting SEs are meaningless numbers.

  Even for Burgundy GC where numerical rank = 4, the condition number of 8.79e20 means that the inverse amplifies floating-point errors by a factor of 10^20. The delta-method SEs of 0.03-2.6 for this category are numerically unreliable.

- **Suggested fix:** (a) Do not report delta-method SEs for the unrestricted specification. (b) For restricted specifications where identification may hold, verify the condition number is below 10^6 before trusting the inverse. (c) Use profile-based confidence sets as the primary inference method.

##### Issue 3.2: Bootstrap implementation uses insufficient starting values
- **Location:** `smm_robustness.py` lines 62-168
- **Severity:** MAJOR
- **Problem:** Each bootstrap replicate uses n_starts = 15 random starting values plus the baseline estimate. For an under-identified problem with a complex objective surface, 15 starts is too few to ensure convergence to the global minimum. The strategy memo specifies 50 starts for the main estimation but the bootstrap uses only 15 -- presumably for computational reasons, but this introduces bootstrap noise that is not from sampling variation but from optimisation failure.

  Additionally, the bootstrap perturbs moments as m_boot = m_data + se_data * z with z ~ N(0, I). This assumes the moment estimates are independent across segments, which has the same problem as the diagonal weighting matrix (Issue 2.5) -- the hedonic coefficients from the same regression are correlated.

- **Suggested fix:** (a) Use the full covariance matrix for the bootstrap perturbation: m_boot = m_data + L * z where Sigma = L L'. (b) Increase n_starts or use differential evolution for each bootstrap replicate (computationally expensive but necessary for reliability). (c) Report the fraction of bootstrap draws where the optimiser converges to different local minima as a diagnostic.

##### Issue 3.3: No overidentification test for restricted specifications
- **Location:** `smm_estimation.py`
- **Severity:** MAJOR
- **Problem:** The "fix_lambda_ak" specification has 4 parameters and 4 moments (just-identified). The "fix_lambda" specification has 5 parameters and 4 moments (still under-identified). Neither the overidentified case exists in the current setup, so a Hansen J-test is not applicable. However, for the just-identified case, the model fit statistic (objective value) should be zero if the model is correctly specified. For Bordeaux fix_lambda_ak (not shown in the output I reviewed), this provides a test of the model's functional form assumptions.

  More importantly, the paper lacks any formal specification test. Given that the model fails dramatically for Bordeaux and partially for Burgundy Premier Cru, a Chi-squared test of the model fit (even for the under-identified case, where positive objective values indicate misspecification) should be reported.

- **Suggested fix:** Report the objective value as a goodness-of-fit measure with an informal calibration: objective / n_moments as "average squared t-statistic of moment mismatch." For Bordeaux, this is 2986/4 = 747 -- hundreds of standard errors off. Make this misfit a headline finding, not a footnote.

---

## Phase 4: Polish & Completeness

**Note: Given the critical issues in Phases 2-3, these are lower priority. They become relevant once the identification problem is resolved.**

### Issues Found: 4

##### Issue 4.1: Missing profile likelihood / identified sets
- **Location:** Strategy memo Section 6 mentions "profile likelihood" but no results are reported
- **Severity:** MAJOR (for paper quality, conditional on fixing identification)
- **Problem:** The strategy memo plans profile-based diagnostics but they are not implemented. Given the severe identification concerns, reporting the profile of the objective function over each parameter (fixing others at estimated values and varying one) would directly show whether the objective has a well-defined minimum or a flat valley. This is especially important for the parameters that hit bounds.

- **Suggested fix:** Implement the planned profile analysis. For each parameter, evaluate the objective on a grid of 100 points across its feasible range, fixing other parameters at the optimum. Plot the profiles. This will make the identification problem visually obvious for the paper.

##### Issue 4.2: Sensitivity to n not structured as a robustness table
- **Location:** `output/structural_robustness.json`, sensitivity_n section
- **Severity:** MINOR
- **Problem:** The sensitivity to n = {3, 5, 10} is computed but not presented in a way that highlights the instability. For Bordeaux, the results change qualitatively with n (see Issue 2.2). For Burgundy GC and Premier Cru, the qualitative pattern is more stable but magnitudes shift substantially. The paper should present this as a structured table showing how each parameter varies with n, and discuss which features of the results are robust to this assumption.

- **Suggested fix:** Create a formatted table with n in columns and parameters in rows, separately for each category. Highlight parameters that change sign or hit different bounds across n values.

##### Issue 4.3: Paper section 03_model.tex says "we leave this for future work"
- **Location:** `paper/sections/03_model.tex` line 369
- **Severity:** MINOR (coordination issue)
- **Problem:** The paper section concludes with "We leave this for future work and focus here on the qualitative predictions of the model." But the strategy memo and code implement structural estimation. This is likely a drafting issue -- the paper text has not yet been updated to reflect the estimation work -- but it should be flagged to avoid internal inconsistency.

- **Suggested fix:** Update the paper text once the estimation issues are resolved and the results are ready for presentation.

##### Issue 4.4: Convex collector valuation extension -- adds identification burden
- **Location:** Strategy memo Section 9 (proposed extension)
- **Severity:** MAJOR (for the proposed extension)
- **Problem:** The strategy memo proposes extending the model to v_k(a*) = v_bar_k + alpha_k * (a*)^eta to resolve the Bordeaux misfit. This adds a 7th parameter (eta) to a system with 4 moments, making identification strictly worse. The current model already cannot be identified with 6 parameters and 4 moments.

  More fundamentally, the Bordeaux misfit may not be a problem with the functional form of v_k but with the model's structure. The data pattern (approach > trough but antique >> peak) could also be explained by: (a) time-varying lambda that does not follow the exponential form, (b) within-type heterogeneity in valuations, (c) common-value components in the auction, or (d) supply-side selection (which wines come to auction at different ages). Adding a curvature parameter treats the symptom, not the cause.

  If the convex extension is pursued, it *must* be accompanied by additional moments to maintain identification. Possible sources: finer age bins within the antique segment, price dispersion within segments, or cross-category parameter restrictions.

- **Suggested fix:** Before pursuing the convex extension, exhaust the diagnostic possibilities with the current model: (a) Verify that the fix_lambda_ak specification (4 params, 4 moments) produces sensible results for Bordeaux. (b) Try alternative lambda specifications (e.g., piecewise linear). (c) Only then consider the convex v_k, and only if accompanied by at least 2 additional moment conditions.

---

## Summary

- **Overall assessment:** CRITICAL ERRORS
- **Critical issues (must fix):** 3 (Issues 2.1, 2.2, 3.1)
- **Major issues (should fix):** 5 (Issues 2.3, 2.5, 2.6, 3.2, 3.3)
- **Minor issues (consider):** 3 (Issues 2.7, 4.2, 4.3)

---

## Priority Recommendations

1. **[CRITICAL] Resolve the identification problem before interpreting any parameter estimates.** The unrestricted specification (6 parameters, 4 moments) is under-identified. All results from this specification -- point estimates, standard errors, bootstrap CIs -- are unreliable. The restricted specifications (fix_lambda with external proxy, fix_lambda_ak) should be the primary reported results. Alternatively, add moment conditions (within-segment variation, price levels, cross-category restrictions) to achieve over-identification.

2. **[CRITICAL] Report bootstrap SEs as primary; do not report delta-method SEs for ill-conditioned systems.** The delta-method SEs are numerically invalid when the Jacobian condition number exceeds 10^10. The bootstrap CIs, while also affected by the identification problem, at least honestly reveal the parameter uncertainty (spanning most of the feasible space for Burgundy GC and Premier Cru).

3. **[CRITICAL] Present the Bordeaux misfit as a headline finding, not a limitation.** The model's inability to fit the Bordeaux pattern with linear collector valuation is an important economic finding -- it tells us something about the structure of collector demand for Bordeaux vs. Burgundy. Frame it positively: "The linear model provides a sharp test. Its failure for Bordeaux suggests that collector value is convex in age for the most prestigious wine category, consistent with [economic interpretation]." But do not estimate the convex extension without additional identifying information.

4. **[MAJOR] Use the full variance-covariance matrix of hedonic coefficients for both the weighting matrix and the bootstrap.** The current diagonal assumption ignores correlation between segment coefficients from the same regression, biasing both estimation and inference.

5. **[MAJOR] Replace midpoint approximation with numerical integration over segments.** The segments are wide (especially antique: a* from 2.0 to 3.0), and the price function has substantial curvature. This is a straightforward computational fix that removes a source of systematic bias.

6. **[MAJOR] Implement the profile-based diagnostics planned in the strategy memo.** These will make the identification issues transparent and publishable. Showing that the objective is flat in certain parameter directions is more informative than reporting (unreliable) standard errors.

---

## Positive Findings

1. **The closed-form price function is a genuine structural advantage.** Unlike many structural auction models that require simulation, the two-point type distribution gives an analytical expected second-order statistic. This makes the estimation transparent and reproducible, and avoids simulation noise as a confound.

2. **The code-model alignment is excellent.** The price formula in `model_solver.py` correctly implements the theoretical model from `03_model.tex`. The handling of the two regimes (v_c >= v_k and v_k > v_c) matches the paper's equations (5) and (6). The normalisation of moments relative to the young baseline correctly mirrors the hedonic regression specification.

3. **The estimation infrastructure is well-designed.** The combination of differential evolution (global search) and L-BFGS-B (local polish) with 50+ starting values is appropriate for a non-convex objective. The three specifications (unrestricted, fix_lambda, fix_lambda_ak) represent a sensible progression from flexible to disciplined. The diagnostic outputs (Jacobian rank, condition number, moment fit decomposition) are exactly the right things to report. The problem is not that the diagnostics are missing -- it is that the diagnostics reveal fundamental issues that need to be addressed.

---

## Score: 35/100

**Deduction breakdown:**
- Under-identification (6 params, 4 moments): -30
- Boundary estimates / non-interior solutions: -10
- Delta-method SEs numerically invalid: -10
- Weighting matrix ignores covariance: -5
- Midpoint approximation bias: -5
- Missing overidentification / specification test: -5

**Note:** The score reflects the *current state* of the structural estimation. The theoretical model is sound, the code is well-written, and the diagnostic infrastructure is excellent. The core problem -- insufficient identifying information relative to the number of parameters -- is solvable. Addressing recommendations 1-2 (restricted specifications as primary, bootstrap SEs) would immediately raise the score to 60-70. Adding moment conditions or cross-category restrictions to achieve over-identification would bring it to 80+.

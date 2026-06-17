# Structural Estimation Strategy Memo

**Date:** 2026-03-29
**Agent:** structural-estimation-expert
**Phase:** Strategy — Structural Estimation Design
**Project:** Liquid Assets (Wine Auction Two-Type Model)
**Model reference:** `quality_reports/theory_model_2026-03-29.md`

---

## 1. Model Summary

A second-price (Vickrey) auction with $n$ i.i.d. bidders drawn from a two-point type distribution (consumption vs. collector). The equilibrium price is the expected second-order statistic of $n$ draws from the mixture. Because the type space is discrete (two points), the expected second-order statistic has a closed-form expression that depends on the mixture probability $\lambda(a^*)$ and the two valuations $v_c(a^*)$, $v_k(a^*)$.

**Key structural advantage:** The price function $P(a^*; \theta)$ is available in closed form -- no simulation or numerical integration is required. This makes the estimation a minimum-distance (MD) problem rather than simulated method of moments (SMM).

---

## 2. Parameters

| Parameter | Symbol | Role | Domain |
|-----------|--------|------|--------|
| Consumption peak value | $\alpha_c$ | Height of consumption valuation at maturity | $(0, \infty)$ |
| Collector baseline value | $\bar{v}_k$ | Price floor from collector demand | $(0, \infty)$ |
| Collector age premium | $\alpha_k$ | Slope of collector valuation in age | $[0, \infty)$ |
| Quality peakedness | $\gamma$ | Sharpness of the consumption quality hump | $(0, \infty)$ |
| Consumption-buyer exit rate | $\delta$ | Speed of consumption-buyer departure post-maturity | $(0, \infty)$ |
| Baseline consumption-buyer share | $\bar{\lambda}$ | Fraction of consumption buyers pre-maturity | $(0, 1)$ |

Six parameters per wine category. Three categories (Bordeaux Grand Cru, Burgundy Grand Cru, Burgundy Premier Cru) estimated independently: 18 parameters total.

---

## 3. Model-to-Moments Mapping

### Empirical Moments

The data provides hedonic regression coefficients for 7 non-baseline bins (relative to the young baseline), extracted from an 8-bin OLS with HC1 errors via `code/structural/10_structural_moments.py` and saved to `output/structural_moments_fine.json`:

| Bin | $a^*$ range | Label | Empirical moment |
|-----|-------------|-------|------------------|
| Young (baseline) | [0.0, 0.4) | young | 0 (normalised) |
| Pre-maturity 1 | [0.4, 0.8) | pre1 | $\hat{\beta}_{\text{pre1}}$ |
| Pre-maturity 2 | [0.8, 1.0) | pre2 | $\hat{\beta}_{\text{pre2}}$ |
| Peak 1 | [1.0, 1.4) | peak1 | $\hat{\beta}_{\text{peak1}}$ |
| Peak 2 | [1.4, 1.6) | peak2 | $\hat{\beta}_{\text{peak2}}$ |
| Trough | [1.6, 2.0) | trough | $\hat{\beta}_{\text{trough}}$ |
| Antique 1 | [2.0, 2.5) | antique1 | $\hat{\beta}_{\text{antique1}}$ |
| Antique 2 | [2.5, 3.1) | antique2 | $\hat{\beta}_{\text{antique2}}$ |

The full 7×7 HC1-robust covariance matrix of these coefficients is extracted from the same regression and used as the optimal weighting matrix.

### Model-Predicted Moments

For each non-baseline bin $b$ with boundaries $[a^*_{\text{lo}}, a^*_{\text{hi}})$, the model-predicted moment is the **bin-averaged log price** minus the young baseline average:

$$m_b(\theta) = \frac{1}{K}\sum_{k=1}^K \log P(a^*_k; \theta) - \frac{1}{K_0}\sum_{k=1}^{K_0} \log P(a^*_{0k}; \theta)$$

where $\{a^*_k\}$ is a uniform grid of $K=20$ points over the bin, and $\{a^*_{0k}\}$ is the corresponding grid over the young baseline $[0.0, 0.4)$. This bin-averaging replaces the single-midpoint approximation, eliminating Jensen's inequality bias in wide bins. Implemented as `moments_integrated()` in `code/structural/model_solver.py`.

### Moment vector

With 7 non-baseline bins:

$$\mathbf{m}(\theta) \in \mathbb{R}^7, \quad m_b(\theta) = \overline{\log P}_b - \overline{\log P}_{\text{young}}$$

---

## 4. Identification

### Identification Table

| Parameter | Primary identifying variation | Intuition |
|-----------|------------------------------|-----------|
| $\alpha_c$ | Approach and peak moments (height of the hump) | Higher $\alpha_c$ raises the consumption valuation at maturity, inflating pre-maturity and at-maturity prices relative to young |
| $\bar{v}_k$ | Level of antique prices | As $a^* \to \infty$, consumption value $\to 0$ and $\lambda \to 0$; the price converges to $\bar{v}_k + \alpha_k a^*$. The intercept is $\bar{v}_k$ |
| $\alpha_k$ | Slope of antique prices | The rate at which antique-segment prices rise with age identifies the collector age premium |
| $\gamma$ | Curvature around the peak | Higher $\gamma$ produces a sharper peak and faster post-maturity decay; identified by the ratio of peak to approach moments |
| $\delta$ | Trough depth relative to peak | Controls how fast consumption buyers exit post-maturity; a deeper trough (lower trough moment relative to peak) implies faster exit |
| $\bar{\lambda}$ | Overall contrast between peak and antique | Given other parameters, $\bar{\lambda}$ governs the relative weight of consumption vs. collector demand, shifting the balance between the hump and the floor |

### Identification Concerns

1. **$\bar{\lambda}$ and $\alpha_c$ interact.** Both affect the height of the peak. Resolution: $\alpha_c$ affects the peak height given $\bar{\lambda}$, while $\bar{\lambda}$ also affects the antique-segment prices (through the auction order-statistic formula). The two are separately identified if both the peak and antique moments are informative.

2. **$\bar{v}_k$ and $\alpha_k$ near-collinear at moderate ages.** At $a^* = 2.5$, we observe $\bar{v}_k + 2.5 \alpha_k$. With only one antique midpoint, these are weakly identified individually. Resolution: the trough moment at $a^* = 1.8$ provides a second equation involving both.

3. **Preferred specification: `fix_lambda`.** $\bar{\lambda}$ is fixed at the empirical proxy $1 - \text{(fraction of young lots >\$200/bottle)}$: Bordeaux Grand Cru: 0.610, Burgundy Grand Cru: 0.485, Burgundy Premier Cru: 0.888. This leaves 5 free parameters $(\alpha_c, \bar{v}_k, \alpha_k, \gamma, \delta)$ against 7 moments, yielding **2 degrees of freedom** for an overidentification test. The lambda proxy comes from the economic structure of the model: high-priced young bottles are dominated by collectors, so $1 - \hat{\lambda}_{\text{proxy}}$ estimates the pre-maturity collector share.

4. **Overidentification testing.** Under correct specification, $J \equiv N_{\text{eff}} \times \text{objective}(\hat{\theta}) \sim \chi^2(2)$ where $N_{\text{eff}}$ is the harmonic mean of bin sample sizes. A large $J$ indicates model misspecification, not identification failure.

---

## 5. Estimation Algorithm

### Objective Function

$$\hat{\theta} = \arg\min_\theta \left[\mathbf{m}_{\text{data}} - \mathbf{m}(\theta)\right]' \mathbf{W} \left[\mathbf{m}_{\text{data}} - \mathbf{m}(\theta)\right]$$

where $\mathbf{W} = \hat{\Sigma}^{-1}$ is the **full optimal weighting matrix** — the inverse of the 7×7 HC1 covariance matrix from the hedonic regression. This is efficient MD: unlike diagonal weighting, it accounts for correlation between bin coefficients estimated from the same regression.

### Optimizer

- **Primary:** L-BFGS-B (scipy) with box constraints matching parameter domains
- **Bounds:**
  - $\alpha_c \in [0.01, 20]$
  - $\bar{v}_k \in [0.01, 20]$
  - $\alpha_k \in [0.00, 10]$
  - $\gamma \in [0.1, 20]$
  - $\delta \in [0.01, 20]$
  - $\bar{\lambda} \in [0.01, 0.99]$

### Multiple Starting Values

To guard against local minima, run from 50 random starting points drawn uniformly within the bounds. Report the best (lowest objective) and flag if multiple distinct optima are found.

### Standard Errors

Delta method: $\text{Var}(\hat{\theta}) = (J' W J)^{-1}$ where $J = \partial \mathbf{m}/\partial \theta$ evaluated numerically via central differences. The condition number of $J'WJ$ is checked; when $\text{cond} > 10^{10}$, delta-method SEs are flagged as unreliable and bootstrap SEs are reported instead.

**Bootstrap SEs (primary for unreliable delta-method):** Parametric bootstrap with $B=200$ draws using full Cholesky perturbation: $\mathbf{m}_{\text{boot}} = \mathbf{m}_{\text{data}} + L z$ where $\hat{\Sigma} = L L'$ and $z \sim N(0, I)$. This correctly accounts for cross-moment correlation.

### J-Test of Overidentification

For the `fix_lambda` spec (5 free params, 7 moments, df=2):
$$J = N_{\text{eff}} \times \hat{Q}(\hat{\theta}) \sim \chi^2(2) \text{ under correct specification}$$
A significant $J$ indicates model misspecification (the linear $v_k$ or single-peaked $v_c$ cannot jointly match all 7 moments). This is interpreted as a diagnostic, not a failure: the trough-missing or misfit segments reveal which features the model cannot accommodate.

---

## 6. Robustness Plan

| Check | Purpose |
|-------|---------|
| Vary $n \in \{3, 5, 10\}$ | Sensitivity to assumed number of bidders |
| Parametric bootstrap (B=200) | Perturb data moments using full Cholesky of VCV: $\mathbf{m}_{\text{boot}} = \mathbf{m}_{\text{data}} + L z$; re-estimate; report bootstrap SEs and percentile confidence intervals |
| Jacobian rank check | Confirm local identification at the optimum |
| Profile likelihood | For weakly identified parameters, report the profile of the objective over a grid |
| Cross-category comparison | Check whether parameter ordering matches economic priors (e.g., $\bar{\lambda}$ highest for Bordeaux GC) |

---

## 7. Implementation Plan

| File | Contents |
|------|----------|
| `code/structural/model_solver.py` | `price(a_star, theta, n)` and `moments(theta, n)` functions |
| `code/structural/smm_estimation.py` | MD estimation loop, delta-method SEs, results table |
| `code/structural/smm_robustness.py` | Sensitivity to $n$, parametric bootstrap |
| `output/structural_estimates.json` | Point estimates and SEs per category |
| `output/structural_robustness.json` | Robustness results |

All scripts use relative paths via `ROOT = Path(__file__).resolve().parent.parent.parent`.

---

## 8. Expected Outcomes

### Cross-Category Predictions

Based on the empirical moments:

- **Bordeaux Grand Cru:** Strong trough (coef drops from 0.467 at peak to 0.163 at trough). Expect high $\gamma$ (sharp peak), moderate $\delta$ (moderate consumption-buyer exit), and a large collector premium at antique ages.

- **Burgundy Grand Cru:** No trough -- prices rise monotonically through trough and antique. Expect low $\delta$ or high $\bar{v}_k$ (collector floor high enough to prevent a dip), and possibly lower $\bar{\lambda}$ (fewer consumption-oriented buyers in this prestige segment).

- **Burgundy Premier Cru:** Strong trough (similar to Bordeaux). Expect similar qualitative pattern to Bordeaux but with different magnitudes reflecting the different market composition.

### Model Fit Concern

For Burgundy Grand Cru, the monotonically increasing pattern (no trough) may be difficult to fit with a model that has a consumption hump. The model can accommodate this if (a) $\bar{\lambda}$ is low (few consumption buyers) or (b) the collector valuation rises fast enough to offset the consumption decline. This will be a key diagnostic.

---

## 9. Key Empirical Finding: Model Fit Heterogeneity

Estimation reveals an important pattern of heterogeneous model fit across categories:

### Burgundy Grand Cru: Perfect fit (objective = 0.0)
- The monotonically increasing moment pattern (approach < peak < trough < antique) is naturally accommodated by the model.
- The model achieves exact fit because the monotonic collector valuation plus decaying consumption share generates a steadily increasing price-age profile.
- Estimated parameters: high gamma (23.0, very sharp peak), moderate delta (1.8), lambda_bar ~ 0.70.

### Burgundy Premier Cru: Good fit with some tension (objective = 50.9)
- The non-monotonic pattern (peak > trough, but trough close to approach) is mostly captured.
- Residual misfit at peak/trough/antique: the model predicts flat prices beyond peak because delta is very high (consumption buyers exit instantly) and alpha_k ~ 0.

### Bordeaux Grand Cru: Poor fit (objective = 2986)
- The model fundamentally struggles with Bordeaux's distinctive pattern: approach(0.18) < trough(0.16) < peak(0.47) << antique(1.08).
- **Core tension:** The trough coefficient (0.163) being *lower* than approach (0.179) requires that consumption-value decay outpaces collector-value growth at a* = 1.8. But the antique coefficient (1.077) being much *higher* than peak (0.467) requires very steep collector-value growth. These two requirements conflict when v_k is linear in a*.

### Implication for Model Development
This finding motivates a model extension: **nonlinear collector valuation** (e.g., convex in age) would allow the collector premium to accelerate past the trough, resolving the tension. This is economically plausible -- the scarcity/prestige premium may be convex rather than linear in age.

---

## 10. Limitations

1. **Boundary estimates and null-space identification for Burgundy GC.** In the `fix_lambda` spec, $\gamma$ and $\delta$ hit their upper bounds (30.0) for Burgundy Grand Cru. This reflects weak identification: the Jacobian $J'WJ$ has rank 4/5, with one null-space direction concentrated in $(\gamma, \delta)$. Economically, a monotonically increasing price profile (no trough) is consistent with a wide range of $(\gamma, \delta)$ combinations as long as the collector floor $\bar{v}_k$ dominates — these parameters govern the consumption hump which is absent in this category. The null-space direction and profile CI (computed in `smm_robustness.py`) are reported to document this identification limitation. The identified parameters $(\alpha_c, \bar{v}_k, \alpha_k)$ — which govern the cross-category pattern of collector dominance — remain well-identified.

2. **Model misspecification for Bordeaux.** The linear collector valuation is too restrictive to match the non-monotonic Bordeaux price pattern. The $J$-test formally rejects the model for all three categories. For Bordeaux, the antique premium (1.71 log-points) is difficult to jointly fit with the trough (0.26 log-points below approach). A convex specification $g(a^*) = (a^*)^\eta$ would add one parameter but potentially resolve the fit issue.

3. **Fixed $\bar{\lambda}$ in preferred spec.** By fixing $\bar{\lambda}$ to the proxy, we impose a moment condition rather than estimating it. If the proxy is mismeasured, this introduces specification error. The `unrestricted` spec estimates $\bar{\lambda}$ freely but adds one parameter and reduces overidentification df from 2 to 1.

4. **Fixed $n$.** The number of bidders is not estimated but calibrated. Results are moderately sensitive to this choice (see robustness).

5. **IPV assumption.** Independent private values rules out common-value components (e.g., resale value uncertainty).

6. **Static model.** No intertemporal considerations. Sellers' decisions about when to auction are not modeled.

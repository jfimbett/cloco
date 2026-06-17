---
name: distributional-debt-capacity
description: Recurring referee issues and scoring calibration for the "Distributional Debt Capacity" paper (Imbet; optimal transport / Wasserstein capital structure). Use when reviewing this paper or its revisions.
metadata:
  type: project
---

# Distributional Debt Capacity (Imbet) — Referee Notes

**Core claim:** Capital supply is a distribution nu, not a price. Debt capacity = W1(mu_i, nu)/2 (exact). Welfare = kappa*W2^2. Within-firm panel: 1 SD of W1_shape -> -1.22pp book leverage (t=-9.1).

## Load-bearing strengths (genuine)
- Exact result delta_i = W1(mu_i,nu)/2 is clean and correct (HLP rearrangement / comonotone coupling, not Brenier — they correctly note this).
- nu calibrated as Frechet mean of firm distributions => does NOT use leverage/spread moments => addresses mechanical-circularity at first order.
- Within-firm FE result is the right test given the model is a within-firm, equal-mean statement.

## Persistent weaknesses (likely to recur across revisions)
1. **STRUCTURAL MODEL DOES NOT FIT.** Cross-decile R^2 = -0.83 (worse than mean). Spearman rho=0.45, p=0.19 (insignificant). Model-predicted spreads have OPPOSITE sign to data across deciles 1-9 (model rises 38->126bps, data falls 462->170bps). Authors reframe structural model as "analytically tractable benchmark" and lean entirely on reduced-form within-firm regression. This is a major fit failure dressed as a composition-effect story. The "structural estimation" is really a 2-param OLS quantile fit + 1 OLS slope, NOT SMM.
2. **kappa identification = OLS slope of spreads on W1_shape.** Identifying assumption: W1_shape uncorrelated with omitted spread determinants conditional on size/CF mean/vol. With ratings/covenants known to dominate spreads and to correlate with distributional shape, this is a strong unaddressed assumption. R^2 of spread reg = 0.15.
3. **nu = Frechet mean is an equilibrium ASSERTION, not derived.** The "free entry / zero profit => barycenter" claim is hand-waved in Sec data + estimation; not proven in appendix. Frechet mean is the W2-barycenter (welfare-optimal nu), so calibrating nu to it and then testing welfare = W2^2 is partly self-referential.
4. **Sign instability across columns (2) vs (3):** raw -0.35, +0.08 with CF controls, -0.057 with full controls. The headline sign depends on the control set; flagged honestly but a skeptic will worry about which conditioning is "right."
5. **Decile-trimming makes coefficient 3-4x larger (-0.16 -> -0.61).** Authors call baseline a "conservative lower bound." Could equally be read as fragility / the effect concentrated in trimmed mass. Plausible but convenient narrative.
6. **W1/W2^2 approximation accurate only "within 14% for 80%."** Heavily caveated heuristic; rejected by structural F-test p=0.046. Fine since they don't use it for estimation, but it weakens the W2 welfare bridge.
7. nu is time-INVARIANT in baseline (single Frechet mean over whole panel) yet Sec results_aggregate discusses nu_t shifts. Tension between static estimation and aggregate-dynamics claims (latter admitted as suggestive/future work).

## Data notes
- Compustat 625,105 fq (1989-2024). TRACE spreads only 23,814 fq matched (1,035 firms), heavily IG-selected.
- N inconsistency: distress robustness table uses 626,752 (vs 625,105) — authors flag a "less strict filter"; minor but a real internal inconsistency.
- TRACE-N inconsistency (recurring): ABSTRACT claims "56,837 firm-quarters" used in the two-stage procedure; but estimation Sec + Table tab_structural calibrate kappa on 23,814 fq / 1,035 firms; appendix app:fisd says 56,837 is the RAW TRACE sample (2,019 firms) BEFORE Compustat match. Decile-fit N_spr sums to ~23,818, confirming the estimation sample is 23,814 not 56,837. Abstract overstates the spread sample size by conflating raw with matched. Flag every revision.
- Aggregate-dynamics figure (fig_aggregate_w1) uses N=621,705 vs 625,105 baseline — another small unexplained N drift.
- Stage-2 kappa text in app:estimation_details says spread reg has "firm fixed effects"; main estimation.tex Sec describes it as cross-sectional OLS slope with size/CFmean/vol controls (no FE mentioned). Mild spec ambiguity in what regression actually identifies kappa.

## Scoring calibration (this paper, second-round revised draft)
- Theory is the strongest part: contribution is genuinely novel (distribution-as-primitive + exact W1 debt capacity). Worth a high contribution score (~80) but NOT top-5 slam-dunk because the empirical payoff is thin.
- Identification: reduced-form within-firm is decent; "structural estimation" largely fails to fit and kappa rests on an OLS exclusion restriction. ~66-70.
- Data: appropriate, well-described, but spread sample selection + composition effects limit what can be concluded. ~72.
- This is a Major Revisions paper for a top-5 (JF/RFS/JFE). The gap between an elegant theory and a structural model that produces R^2=-0.83 is the central problem. Don't let theoretical elegance pull the overall above ~73.
- Target journal per domain profile: JF/RFS/JFE. Honest fit is Review of Finance / JFI tier unless the structural side is fixed or dropped in favor of a cleaner reduced-form supply-side identification.

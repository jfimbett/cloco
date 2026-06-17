# Referee Report
**Date:** 2026-05-14
**Paper:** Incentives and Risk-Taking in Delegated Portfolio Management: A Contracting Approach
**Target Journal:** Not specified — inferred as *Journal of Finance* or *Review of Financial Studies* (top finance field)
**Recommendation:** Major Revisions
**Overall Score:** 70.6/100

## Summary
The paper develops a closed-form two-period principal-agent model in which convex flow-performance generates an option-like incentive for fund managers to over-load on volatility, and derives an incentive-compatible (IC) management fee `phi(sigma_d)` that implements an investor-chosen volatility target `sigma_d`. The contribution is framed as a "pay for risk, not luck" affine contract that is easy to communicate to practitioners. The model is technically clean and the affine approximation is genuinely useful, but the paper has (i) a material *internal inconsistency* between the calibration text and every figure note regarding the manager risk-aversion parameter `eta`, (ii) a *directional claim about welfare that contradicts the underlying CSV output*, (iii) unresolved conceptual issues about commitment, the relation between the management-fee mechanism and a hypothetical performance-fee mechanism, and the operational meaning of "implementing sigma_d" when sigma is unobservable in real time. The novelty relative to Basak-Pavlova (2007), Carpenter (2000), and Cuoco-Kaniel (2011) is real but narrow; the welfare exercise must be re-stated in economically meaningful units. I recommend Major Revisions.

## Dimension Scores
| Dimension | Weight | Raw Score | Weighted | Notes |
|-----------|--------|-----------|----------|-------|
| Contribution & Novelty | 25% | 70 | 17.5 | Closed-form IC fee in a tractable two-period setting is useful, but the marginal step beyond Basak-Pavlova (2007) and Carpenter (2000) is incremental and a comparison with a *performance-fee-only* benchmark is missing. |
| Identification / Model | 30% | 68 | 20.4 | Mechanics correct, but timing, commitment, equilibrium concept, and observability of sigma are insufficiently formalized; CARA-Gaussian approximation under `f_2 > 0` is asserted to be "accurate" with no quantitative bound. |
| Data / Calibration | 20% | 60 | 12.0 | Material inconsistency on `eta` (text says 15, every figure note and Appendix G.3 say 3); welfare claim's *direction* in `f_2` contradicts `welfare_comparison_vs_f2.csv`; welfare units not translated to certainty-equivalent return. |
| Writing & Presentation | 15% | 78 | 11.7 | Generally clear and well-organized. Notation is consistent. Several places hedge or paraphrase the same point and could be tightened. |
| Journal Fit | 10% | 70 | 7.0 | The closed-form contracting result fits RFS-style methodological notes; the empirical anchoring and welfare numbers are not yet at JF/RFS quality bar. *Review of Finance*, *JFE* (short paper), or *Management Science (Finance)* are more honest targets at the current quality. |
| **Weighted Total** | 100% | — | **70.6** | |

## Major Comments

1. **Critical internal inconsistency in the manager risk-aversion parameter (Section 4 vs. Section 5 vs. every figure note vs. Appendix G.3).**
   Section 4 (Calibration) states `eta = 15` with sensitivity over `[3, 30]`. Section 5 (Numerical illustration) repeats `eta = 15`. **All eleven figure notes in `sections/figures.tex`** (Figures `flow-performance`, `ic-fee-curve`, `opt-sigma-vs-f2`, `comp-f2`, `comp-scale`, `comp-sharpe`, `comp-risk`, `welfare`, `incentive-alignment`, `global-ic`, `affine-approx`) list baseline `eta = 3`. **Appendix G.3** also states *"baseline parameter values for the numerical exercise are S=0.35, r_f=0.037, gamma=5, eta=3, ..."* and sweeps `eta in [1, 8]` — *not* `[3, 30]` as in Section 4. Cross-checking with `output/figure_data/equilibrium_baseline.csv` (`sigma_d_star = 0.128`, `phi_star = 0.039`) and `code/solve_model.py` line 64 (`eta = 15.0`), the figures were generated with `eta = 15`, so it is the figure notes and Appendix G.3 that are wrong. This is a critical defect: the paper cannot ship to a top journal with such an obvious self-contradiction. All eleven figure notes and Appendix G.3 must be updated, and the `eta`-sweep range in G.3 must be made consistent with the `[3, 30]` claim in Section 4.

2. **Welfare claim's direction in `f_2` contradicts the paper's own output (Section 5, Figure `fig:welfare`, right panel).**
   Section 5, penultimate sentence: *"The right panel shows this welfare gain is increasing in `f_2`, confirming that IC enforcement is most valuable when flow convexity is high."* The supporting file `output/figure_data/welfare_comparison_vs_f2.csv` shows the *opposite*: `DeltaU_I = 0.131` at `f_2 = 5`, falls monotonically to `0.0070` at `f_2 = 25` (baseline), and becomes *negative* at `f_2 >= 40`. So the welfare gain from the IC contract relative to the 2% flat-fee benchmark is *decreasing* in `f_2`, not increasing. The intuition is that as `f_2` rises, the IC fee `phi(sigma_d)` falls, so the *gap* between the (mis-aligned) 2% flat fee and the IC fee widens — the comparison-fee benchmark becomes mechanically more punitive. This is a fee-level artifact, not a measure of "IC enforcement value". The paper must (a) correct the directional sentence and the right panel of `fig:welfare`, and (b) reconsider whether the welfare comparison against an exogenously fixed 2% management fee is the right counterfactual at all — see Comment 4.

3. **The "pay for risk, not luck" framing rests on commitment and observability assumptions that are not explicit.**
   Section 2 ("Level versus schedule interpretation") concedes that in the *theoretical model* the equilibrium is a single fee level `phi^*`, not a schedule. The "pay for risk, not luck" label only carries practical content if the contract is contingent on a (noisy) estimate `hat sigma`. The paper does not state:
   - whether the investor can *commit* to the fee `phi^*` before the manager chooses `sigma` (a Stackelberg structure with full commitment is essential for the IC condition to bind);
   - whether renegotiation can occur *after* `sigma` is observed (or estimated) and `r` is realized;
   - whether the schedule `phi(hat sigma)` is itself incentive-compatible once `hat sigma` is noisy (the paper merely says this is "an important direction for future work" in Section 5).

   A top-finance audience will read this as conceding that the headline contract is not actually implementable as advertised. At minimum, the paper should (a) state the equilibrium concept formally (Stackelberg with commitment, single fee level, common knowledge of `S, f_1, f_2, gamma, eta, A_0`), and (b) be more candid in the abstract and introduction that the "pay for risk, not luck" framing is conditional on the investor's ability to observe (or precisely estimate) realized volatility — which is the empirically hard part.

4. **Marginal contribution of the flow-mechanism is unclear; the relevant counterfactual is not a flat fee — it is a performance-fee contract.**
   The paper's core economic claim is that *convex flows* — distinct from explicit performance fees — generate risk-shifting. The mechanism is real, but the welfare exercise in Section 5 compares the IC management fee to a *flat 2% management fee*. This is the wrong counterfactual: the only thing the flat-fee benchmark establishes is that a *misaligned* contract is worse than an *aligned* one, which is mechanical. The interesting and JF/RFS-level question is whether the optimal IC management fee in the presence of convex flows dominates (a) an explicit performance fee `psi (r - r_f)^+`, (b) an HWM-style performance fee, or (c) a combined `(phi, psi)` schedule. Section 2 sketches a performance-fee extension but only in words. Without a quantitative comparison against a performance-fee benchmark, a reader cannot tell whether the convex-flow channel adds anything once standard performance-fee instruments are available. This is the comment a JF/RFS referee will press on hardest.

5. **CARA-Gaussian approximation under `f_2 > 0` is asserted as "accurate" without quantitative support (Section 2, footnote on manager utility, p. ~6 of model.tex).**
   The footnote concedes that when `f_2 > 0`, `phi A` is not Gaussian (AUM has a non-Gaussian `f_2 sigma^2 X^2 I` component), and the mean-variance form is then "a tractable first-order approximation to CARA certainty equivalence". The paper offers *no* quantitative bound on this approximation error. Given that the IC fee `phi(sigma_d) = 2(K S + 2 f_2 sigma_d C_1) / (eta (2 K^2 sigma_d + Delta_quad))` depends on third- and fourth-moment terms of `X` through `Delta_quad`, dropping non-Gaussian information from the CE is potentially a first-order, not second-order, distortion near the operating point. The authors should either (a) report the numerical CE error at the baseline (simulate CARA-CE directly under `f_2 > 0` and compare `sigma_d^*` and `phi^*` against the mean-variance solution), or (b) drop the CARA-CE rhetoric and present the manager objective as a *primitive* mean-variance preference over fee revenue. The current footnote-only treatment leaves the reader unable to assess whether the headline contract is right at the calibration.

6. **Two-period horizon — robustness to dynamics.**
   The two-period setup precludes the most interesting margins of the literature: (i) dynamic moral hazard with continuous reporting (Biais, Mariotti, Plantin, Rochet 2010); (ii) high-water-mark dynamics (Goetzmann-Ingersoll-Ross 2003; Panageas-Westerfield 2009); (iii) the well-known result that in dynamic settings the manager's volatility *response* to incentives is non-monotone and can reverse signs (Hodder-Jackwerth 2007; Buraschi-Kosowski-Sritrakul 2014; Lan-Wang-Yang 2013). The paper claims to provide "a tractable framework with the aim to study this type of agency frictions" but the two-period setting cannot speak to any of those margins. A more honest framing would be: *this is a one-shot model that delivers a closed-form contracting benchmark; dynamics are deferred*. The paper currently overclaims its scope; Section 6 acknowledges run-like dynamics as future work but the introduction and abstract do not.

7. **Literature gaps in dynamic moral hazard and structural performance-fee design.**
   The paper cites Starks (1987), Carpenter (2000), Basak-Pavlova (2007), Cuoco-Kaniel (2011), Ou-Yang (2003), Huang-Sialm-Zhang (2011), Berk-Green (2004), and Vayanos-Woolley (2013). Notably missing for a JF/RFS submission:
   - **Biais, Mariotti, Plantin, Rochet (2010)** — directly relevant dynamic version of this friction.
   - **Goetzmann, Ingersoll, Ross (2003)** — Appendix F sketches HWM but does not cite this canonical paper.
   - **Panageas-Westerfield (2009)** — risk-taking under HWM.
   - **Lan, Wang, Yang (2013)** — structural performance-fee + risk-shifting model.
   - **Drechsler (2014)** — risk choice under HWM.
   - **Hodder-Jackwerth (2007)** — incentive contracts and hedge-fund management.
   - **Buffa, Vayanos, Woolley (2022)** — asset management contracts and equilibrium prices.
   - **Dybvig, Farnsworth, Carpenter (2010)** — portfolio performance and agency.

   These are not optional for a top-finance submission on this topic.

8. **Investor's outside option and the "viability of delegation" claim (Section 5).**
   Section 5 says the investor's participation `U_I >= 0` is violated under the flat 2% fee but satisfied under the IC contract — therefore "the IC contract is necessary for delegation to be viable". This conflates two different statements: (a) under the *specific* exogenous flat fee of 2%, the investor prefers no-delegation; (b) under *some* feasible contract (IC), the investor prefers delegation. Statement (a) does not imply that delegation is non-viable absent IC — only that 2% is too high a fee. A more careful statement would compare investor utility under IC against (i) direct investment in the risk-free asset, and (ii) an *optimally chosen* flat fee `phi_flat^*` set by the investor (which will not equal 2%). The current framing borders on a strawman counterfactual.

9. **Fee-base equivalence — the approximation error is non-trivial at the calibration (Appendix F).**
   Appendix F shows `tilde phi approx phi (1 + r_f + S sigma)`. With `r_f = 3.7%`, `S sigma ~ 4.5%`, the multiplier is `~1.08` — i.e., the discrepancy between beginning- and end-of-period AUM conventions is roughly 8% of the fee, or ~32 bp on a 4% fee. Calling this "second-order and negligible" is misleading when the headline result is `phi^* approx 3.95%`. The paper should either (a) report results in the beginning-of-period AUM convention (the empirically standard one for mutual funds), or (b) explicitly quantify the 8% bias and explain why it does not affect comparative statics or welfare conclusions.

10. **Global IC verification is local-on-grid, not analytic (Appendix C.2).**
    Appendix C.2 ("Global incentive compatibility") asserts that "the manager's utility profile is everywhere single-peaked with a unique maximum at `sigma_d`" based on a "dense grid" of sigma values across the parameter sweep, and Figure `fig:global-ic` shows this at baseline. This is empirical, not analytical. A proper global-IC argument requires either (a) showing `U_M(sigma; phi(sigma_d))` is strictly quasi-concave in sigma for all admissible parameters, or (b) explicitly bounding the gap `U_M(sigma_d) - max_sigma U_M(sigma; phi(sigma_d))` numerically with confidence intervals. The current treatment leaves open the possibility of corner solutions or non-uniqueness inside the sweep but outside the grid. State global-IC as a *numerical* property and weaken the claim accordingly.

## Minor Comments

1. Section 2, paragraph after eq. (1): "Within a standard asset pricing interpretation, `sigma` can be viewed as scaling exposure to a strategy with constant Sharpe ratio, for example through leverage." This is the *only* role for `sigma`; the paper should be explicit that this rules out portfolio choice over multiple risky assets and the standard mean-variance frontier intuition. A reader familiar with Sharpe optimization will wonder why `S` is exogenous and constant.

2. Section 2, eq. (2) for `F(r)`: the kink at `r = r_f` is sharp; the derivative jumps from `f_1` (below) to `f_1 + 2 f_2 (r - r_f)` (above). Empirical estimates (Sirri-Tufano 1998; Chevalier-Ellison 1997) show a *smoother* convexity that kicks in not at `r_f` but somewhere in the upper performance quartile or relative to peer benchmarks. The sharpness of the kink at `r_f` is a strong functional-form choice — defend why the kink is at `r_f` rather than at a peer benchmark.

3. Section 2: "in the absence of contractual discipline, the manager's privately optimal volatility generally exceeds the level preferred by investors." "Generally" is vague — state the analytic condition under which `sigma^*_M(phi) > sigma^*_I` for `phi = phi_mkt` or for `phi = 0`.

4. Section 3, last paragraph: the affine approximation is said to have "average absolute errors below 0.1 percentage points of the fee level." `equilibrium_baseline.csv` reports `affine_mae_pct = 0.083` (i.e., 0.083 percentage points). Good — but clarify "below 0.1 pp" is the *MAE*, not the worst-case error. The maximum error over the +/-5pp window is presumably larger.

5. Section 4: the claim that `eta = 15 = 3 gamma` is the *only* justification for the eta calibration. This is a normalization claim, not an empirical one. Career-concern models (Chevalier-Ellison 1999; Hong-Kubik-Solomon 2000) give numerical anchors that could be cited.

6. Section 5: "The IC fee formula `phi = 2 partial_sigma E[A] / (eta partial_sigma V[A])` inherits the sign of `partial_sigma E[A]`, which is strictly positive whenever `S > 0` or `f_2 > 0`." Correct, but `phi(sigma_d^*)` could exceed 1 if `eta` is small enough — Appendix G.3 sweeps `eta in [1, 8]`. Report whether `phi(sigma_d^*) in [0, 1]` holds across the whole sweep. (At `eta = 1` with `f_2 = 25`, `A_0 = 1`, `f_1 = 1.5`, `S = 0.35`, the IC fee could plausibly exceed 100%.)

7. Section 5: the suggestion to use "high-frequency range-based estimators" of realized volatility is a one-line gesture. For a contracting application, the relevant estimator is one whose noise is *unbiased and independent* of the manager's actions, which range-based estimators are not in general. Either remove the gesture or expand it with a citation to Andersen-Bollerslev-Diebold-Labys (2001) or Barndorff-Nielsen-Shephard (2002).

8. Conclusion: the "next step" of incorporating run-like dynamics and risk of ruin is intriguing but should be substantiated: Liu-Mello (2011) on hedge-fund runs is the closest existing antecedent — cite it.

9. Notation: the `Remark` block in Section 3 ("Characterization of the Optimal Volatility Target") is not a theorem, lemma, or proposition. Top finance journals usually do not number Remarks. Consider downgrading to a paragraph header or upgrading to a Proposition with a proof in the appendix.

10. Bibliography style: `chicago` is non-standard for a JF/RFS submission; both journals use author-year inline citations with their own house style. Confirm style at the target journal.

11. Several captions in `sections/figures.tex` repeat the same parameter list four to five times verbatim. Replace with one explanatory paragraph and short cross-references.

12. The paper contains *no* tables. The quantitative summary in Section 5 (`sigma_d^* ~ 12.8%`, `phi^* ~ 3.95%`, `U_M(IC) ~ 0.050`, `U_I(IC) ~ 0.001`, `U_I(flat) ~ -0.006`, `sigma^free ~ 19.1%`, `DeltaU_I ~ 0.007`) would be much easier to follow as a table summarizing baseline equilibrium and the welfare comparison.

## Questions for the Authors

1. **Performance fees as the counterfactual.** Have you computed equilibrium volatility, IC fee, and investor utility under an *optimally chosen* performance fee `psi (r - r_f)^+` (with `phi = 0`) and under an *optimally chosen* combination `(phi, psi)`? Without that comparison, the paper has not established that the management-fee instrument is necessary — only that *some* contracting beats 2% flat.

2. **Why is the welfare gain decreasing in `f_2` in your CSV but described as increasing in the paper?** Please clarify which is correct (the CSV or the prose) and re-do the right panel of `fig:welfare` and the Section 5 prose accordingly. If decreasing is correct, the economic intuition needs to be re-stated.

3. **CARA-Gaussian approximation error.** Can you numerically simulate the true CARA certainty equivalent of `phi A` under `f_2 > 0` and report the percentage error in `sigma_d^*` and `phi^*` relative to the mean-variance solution at the calibrated baseline? If the error is below ~5%, say so; if above, the approximation is not innocuous.

4. **Equilibrium concept.** Is the equilibrium Stackelberg with full investor commitment to `phi^*`? Can the manager renegotiate after observing `r`? Is there an outside option for the investor that pins down `bar U_I`? Without these, the IC fee is a fixed point, not an equilibrium.

5. **`eta` calibration mismatch.** Which is the intended baseline: `eta = 15` (Section 4 and Section 5) or `eta = 3` (every figure note and Appendix G.3)? Please regenerate either text or figures so the paper is internally consistent. Also: is the sensitivity range `[3, 30]` (Section 4) or `[1, 8]` (Appendix G.3)?

6. **Welfare units.** Please translate `DeltaU_I = 0.007` from mean-variance utils into either (a) the certainty-equivalent net return in basis points, or (b) the equivalent permanent flow of fees the investor would pay to switch from flat to IC. As stated, `DeltaU_I = 0.007` is dimensionally opaque.

7. **Observability of sigma.** What is the *minimum* sample horizon (in months of returns) over which realized volatility must be estimated to keep the affine schedule `phi = alpha + beta hat sigma` within 0.5 pp of the IC fee with, say, 95% probability? This determines whether the contract is operationally feasible at quarterly vs. annual horizons.

8. **Non-Gaussian returns.** All closed-form results use Gaussian `epsilon`. Mutual fund returns exhibit fat tails. How sensitive is the IC fee schedule to a Student-t innovation with realistic degrees of freedom (e.g., `nu = 5`)?

9. **Global IC.** Is there an analytic condition on `(S, f_1, f_2, eta, A_0)` under which `U_M(sigma; phi(sigma_d))` is globally quasi-concave in sigma? Or is global IC verifiable only on a grid?

10. **Practical implementation.** In the U.S. mutual fund context, Form N-1A requires disclosure of management fees as a fixed percentage of NAV. Is the "pay for risk" schedule legally implementable as a *management* fee, or would it require restructuring as a *performance* fee — in which case the paper has not really shown that management fees alone can solve the friction?

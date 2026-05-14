# Referee Report
**Date:** 2026-05-14
**Paper:** Incentives and Risk-Taking in Delegated Portfolio Management: A Contracting Approach
**Target Journal:** Not specified — inferred as Journal of Financial Economics / Review of Asset Pricing Studies (per instructions)
**Recommendation:** Reject (encourage major revision and resubmission elsewhere or to a more specialized outlet)
**Overall Score:** 47.8/100

## Summary
The paper develops a two-period principal–agent model of delegated portfolio management in which the manager controls portfolio volatility, investors exhibit convex flow-performance, and the manager is compensated by a proportional management fee. The central claim is the derivation of a closed-form "incentive-compatible" (IC) fee schedule $\phi(\sigma_d)$ that implements an investor-chosen volatility target, plus an affine approximation amenable to practitioner communication ("pay for risk, not luck"). The paper is well-organized and well-motivated, and the literature positioning relative to Basak-Pavlova-Shapiro (2007) is clearly articulated. However, I identify (i) a load-bearing algebraic error in the manager's first-order condition that propagates into the IC fee formula and (ii) a severe internal inconsistency between the calibrated parameter values, the derived IC formula, and the reported equilibrium fees in the numerical section. Together these problems vitiate the paper's central quantitative claims and require substantial reworking of the model derivations, calibration, and numerical figures.

## Dimension Scores
| Dimension | Weight | Raw Score | Weighted | Notes |
|-----------|--------|-----------|----------|-------|
| Contribution & Novelty | 25% | 55 | 13.8 | Question is important and a tractable closed-form IC fee schedule has practical appeal, but the marginal contribution over Basak-Pavlova-Shapiro (2007) is modest and overstated; "pay for risk, not luck" framing is intuitive but not theoretically novel. |
| Model & Theory | 30% | 35 | 10.5 | Algebra error in the manager FOC (Eq. \ref{eq:manager-FOC}) corrupts the IC fee derivation; SOC, uniqueness, and global-maximum arguments in Appendix C.2 are incomplete; equilibrium existence proposition is essentially asserted, not proved. |
| Calibration & Numerics | 20% | 30 | 6.0 | Reported equilibrium $\phi^*\approx 1.4\%$ at $\sigma_d^*\approx 12\%$ is inconsistent with the stated IC formula and calibrated parameters by roughly an order of magnitude; comparative-statics figures use a "simplified" baseline whose IC fees would exceed 100% under the same formula. |
| Writing & Exposition | 15% | 70 | 10.5 | Writing is generally clear and well-organized, but "comparative statistics" is used throughout where "comparative statics" is meant; some equations are stated without sufficient setup; notation is mostly consistent. |
| Journal Fit | 10% | 70 | 7.0 | The question and structure are appropriate for JFE/RAPS in principle, but in current form the paper would not survive technical refereeing at either outlet. |
| **Weighted Total** | 100% | — | **47.8** | |

## Major Comments

1. **Algebra error in the manager's first-order condition (Eq. \ref{eq:manager-FOC} on p. ~7 of model.tex; Eq. \ref{eq:manager-FOC-app} in Appendix C.1).** The manager's mean–variance utility is defined as
$$U_M(\sigma,\phi)\;=\;\phi\,\E[A] - \frac{\eta\phi^2}{2}\,\V[A],$$
so the correct first derivative with respect to $\sigma$ is
$$\frac{\partial U_M}{\partial \sigma} = \phi\,\partial_\sigma\E[A] - \frac{\eta\phi^2}{2}\,\partial_\sigma\V[A].$$
However, the paper drops the factor of $1/2$ on the variance term in Eq. (\ref{eq:manager-FOC}) and in the appendix derivation immediately following Eq. (\ref{eq:manager-FOC-app}), writing
$$\phi\Big(\Kcal S + 2 f_2\sigma C_1\Big) - \eta\phi^2\Big(2\Kcal^2\sigma + \Delta_{\text{quad}}\Big) = 0.$$
I verified this numerically by computing $\partial U_M/\partial\sigma$ via finite differences at $\sigma_d=0.12$ under the calibrated parameters: the numerical derivative is $0.326$ while the paper's FOC evaluates to $\approx 0$. The corrected IC fee is exactly twice the value implied by Eq. (\ref{eq:phi-IC}):
$$\phi(\sigma_d) = \frac{2\big(\Kcal S + 2 f_2 \sigma_d C_1\big)}{\eta\big(2 \Kcal^2 \sigma_d + \Delta_{\text{quad}}(S,f_2;\sigma_d)\big)}.$$
This error propagates through Eq. (\ref{eq:phi-IC}), Eq. (\ref{eq:phi-IC-app}), the equilibrium FOC Eq. (\ref{eq:investor-FOC}), the affine approximation, and every numerical result. **This must be fixed before any other revision is meaningful.**

2. **Severe inconsistency between the calibrated parameters, the IC formula, and the reported equilibrium values (Sec. 4 vs. Sec. 5, paragraph "Equilibrium outcomes").** Section 4 specifies $\Sharpe=0.35$, $r_f=3.70\%$, $\gamma=5$, $\eta=3$, $A_0=1$, $f_1=1.5$, $f_2=25$. Section 5 then reports equilibrium $\sigma_d^*\approx 12\%$ and IC fee $\phi^*\approx 1.4\%$. Plugging these parameters into Eq. (\ref{eq:phi-IC}) as written gives $\phi(\sigma_d=0.12)\approx 11.0\%$ (and into the corrected version of the IC fee derived in Comment 1, gives $\phi(\sigma_d=0.12)\approx 21.9\%$). Neither value is close to 1.4%. To recover $\phi^*\approx 1.4\%$ from Eq. (\ref{eq:phi-IC}) one would need $\eta\approx 23.5$, far outside the paper's stated sensitivity range $\eta\in[1,8]$. Until the source of this gap is identified — whether it is the FOC error in Comment 1, a different definition of $\phi$ (e.g., not a pure proportional fee), an error in the IC algebra beyond Comment 1, or a numerical implementation that does not match the stated formula — the paper's central quantitative claim is unsupported.

3. **Comparative-statics figures use a "simplified" baseline that produces economically nonsensical fees (footnote in Sec. 5; figure notes in figures.tex).** The footnote in Sec. 5 states that Figures \ref{fig:comp-f2}–\ref{fig:comp-risk} use $\Sharpe=0.5$, $r_f=2\%$, $\gamma=3$, $\eta=2$, $A_0=1$, $f_1=0.2$, $f_2=0.5$ "for visual clarity." Under those parameters and the paper's Eq. (\ref{eq:phi-IC}), $\phi(\sigma_d=0.12)\approx 85\%$ (and $\approx 171\%$ with the corrected formula in Comment 1). Fees exceeding 100% of AUM are economically impossible — the manager cannot extract more than the assets themselves. This implies that whatever the figures plot, it is not the IC fee as defined in the paper. The paper must (a) reconcile the simplified parameters with the calibration baseline, (b) explain what the figures actually depict, and (c) re-draw the figures using parameter ranges where the IC fee is well-defined and economically sensible.

4. **Existence, uniqueness, and global maximization arguments are incomplete (Appendix C.2, "Existence, Uniqueness, and Second-Order Condition").** The appendix asserts that the condition $\eta\phi\cdot 2\Kcal^2 > 2 f_2 C_1$ guarantees uniqueness "by the intermediate value theorem" and that this condition is "verified numerically across the calibrated parameter ranges in Appendix~\ref{app:numerical}." Three problems: (i) the manager's FOC factors as $\phi\,[\,\text{bracket}\,]=0$, so $\sigma=0$ is always a solution (yielding $U_M=\phi A_0(1+r_f)$); the paper must verify that the interior IC solution dominates this corner. (ii) The bracket itself is a polynomial in $\sigma$ whose degree grows with $\Delta_{\text{quad}}$; uniqueness of the positive root is not guaranteed by a sign argument at $\sigma=0$ and $\sigma\to\infty$ alone. (iii) The "sufficiency" paragraph and the SOC paragraph in C.2 are not self-contained: substituting the IC fee back into the inequality $\eta\phi\cdot 2\Kcal^2 > 2 f_2 C_1$ produces a condition that depends on $\sigma_d$ in a non-trivial way and is not analytically established. Either provide a rigorous proof or qualify the claim of "unique interior solution" with explicit conditions and explicit numerical verification across the parameter space.

5. **The IC fee in Eq. (\ref{eq:phi-IC}) is a first-order condition only — global incentive compatibility is not addressed (Sec. 2.3, Appendix C).** Even if the SOC holds locally, IC in a moral-hazard setting requires the principal to verify that the agent's chosen action is the *global* maximizer of his expected utility under the proposed contract, not just a stationary point. Because the manager's utility is non-concave in $\sigma$ (the mean is convex through the $f_2\sigma^2 C_1$ term, and the variance is quartic in $\sigma$), local concavity does not imply global concavity. The paper must verify, at least numerically across the calibration grid, that the IC fee implements $\sigma_d$ as the *global* maximizer of $U_M$.

6. **The "pay for risk, not luck" framing is overstated (Sec. 2.3, final paragraph; Sec. 6 Conclusion).** The decomposition $A = \E[A] + (A-\E[A])$ is mathematically trivial, and $\phi A$ inherits both components. Calling $\phi\,\E[A]$ the "risk component" and $\phi(A-\E[A])$ the "luck component" is semantic — the manager's *realized* compensation $\phi A$ still depends entirely on realized AUM and therefore on luck. The IC fee schedule sets the *level* of $\phi$ as a function of the *target* $\sigma_d$, but the actual fee revenue $\phi A$ remains fully exposed to realized outcomes. The "pay for risk, not luck" label is therefore at best a description of how the *fee rate* is set; it is not a property of the manager's payoff. The paper should either provide a contract that genuinely insulates the manager from realized luck (e.g., a fixed fee on initial AUM, or a state-contingent fee schedule that delivers a deterministic payoff) or scale back this framing substantially.

7. **The manager's mean-variance preferences over fee revenue have undesirable properties under proportional fees (Eq. for $U_M$ in Sec. 2.1).** With $U_M = \phi\,\E[A] - \frac{\eta\phi^2}{2}\V[A]$, the manager's effective risk aversion over fee revenue scales with $\phi$: as $\phi\to 0$, the risk penalty vanishes faster than the mean term. This generates a degenerate-looking optimum in which lowering the fee toward zero appears to make the manager arbitrarily risk-loving on a per-dollar-of-fee basis. The paper should clarify whether $\eta$ is intended as risk aversion over fee revenue (in which case the formulation is internally consistent but $\eta=3$ has no straightforward calibration target) or risk aversion in CARA units (in which case the dependence on $\phi$ in the penalty term is unusual). Justification of the calibration $\eta=3$ via "career concerns" (Sec. 4) does not pin down the magnitude.

8. **The treatment of performance fees and high-water marks is essentially hand-waved (Sec. 2.1, final paragraph; Appendix F).** The paper mentions that performance fees and HWMs "can be incorporated" and that "in the extension with performance fees, the economic mechanism is unchanged, but closed-form expressions become less transparent, so we rely on numerical solutions." Appendix F provides only a sketch, not a derivation. Given that performance fees are the dominant contractual feature in hedge funds — the very setting where flow convexity is strongest — this omission undercuts the paper's policy relevance. At minimum the numerical illustration should be extended to a representative hedge-fund contract.

9. **Implementation discussion is too informal for the central practical claim (Sec. 5, paragraph "Implementation and observability").** The paper concedes that realized volatility $\hat\sigma$ is estimated with noise, can be manipulated via return smoothing, and depends on horizon — and then defers the full treatment to "future work." But the entire selling point of the IC contract is its practical implementability ("easy to communicate"). A serious analysis would: (i) derive the bias introduced by sample-volatility estimation, (ii) characterize the manager's incentive to manipulate reported volatility under the affine rule, and (iii) compare the welfare consequences of the affine rule to standard alternatives (high-water-mark contracts, asymmetric fees, lockups). Without this, the "pay for risk, not luck" rule is a theoretical artifact, not an implementable contract.

10. **Contribution is overstated relative to Basak-Pavlova-Shapiro (BPS 2007).** The introduction (paragraph 6) claims three distinguishing contributions: (a) closed-form IC fee schedule, (b) affine approximation, (c) explicit welfare comparison. (a) is genuine but only after correcting the algebra error in Comment 1; (b) is a Taylor approximation around the optimal target, which is a mathematical observation rather than an economic insight; (c) is asserted but I do not see the welfare comparison explicitly computed in Sec. 5 — the paper reports only $\sigma_d^*$ and $\phi^*$, not investor utility relative to the unconstrained equilibrium. A proper welfare comparison would require solving for the manager's unconstrained choice of $\sigma$ and comparing $U_I$ at the two equilibria; this is missing.

## Minor Comments

1. The paper uses "comparative statistics" repeatedly (Sec. 3, paragraph 4; Sec. 5, paragraph "Comparative statics"; figure captions; Appendix G.3). The correct term is **comparative statics**. This is a theoretic term of art and should be corrected throughout.

2. Equation (\ref{eq:dVarA}) in model.tex states $\partial_\sigma \V[A] = 2\Kcal^2\sigma + \Delta_{\text{quad}}$. This is internally consistent with Appendix B.3, but the reader is asked to accept it without seeing the derivation; placing the derivation in the main text or signposting Appendix B.3 more aggressively would help.

3. The flow function in Eq. (\ref{eq:flow}) is continuous and continuously differentiable at $r=r_f$ (both one-sided first derivatives equal $f_1$), but the second derivative jumps from $0$ to $2f_2$. The paper should note this and briefly comment on whether the kink in $F''$ is consequential for the moment computations in Appendix B.

4. The calibration claim "a fund with +5% excess return experiences flows of approximately +13.8% of AUM, while a fund with +10% excess return sees flows around +40%" (Sec. 4) is verified numerically (I compute 13.75% and 40.00% respectively). Good. However, at a +1 standard-deviation positive realization ($\sigma_d=12\%$, so excess return $\approx 0.042+0.12=0.162$), the implied flow is $\approx 90\%$ of AUM. The paper should note this tail magnitude and discuss whether such flows are empirically defensible.

5. The footnote in Sec. 5 (line 8) describing "simplified baseline" parameters for figures is buried; it should be elevated to a sentence in the main text. As discussed in Major Comment 3, the very fact that two different baselines are used (Sec. 4 vs. Sec. 5 figures) needs explicit justification beyond "visual clarity."

6. The conclusion (Sec. 6) is short and gestures vaguely at future extensions ("run-like dynamics and risk of ruin"). For a paper whose contribution is a tractable framework, the conclusion should more explicitly summarize the testable implications and the gap between the theoretical contract and feasible real-world implementation.

7. Appendix Section A.1 is labeled "Derivation sketch" — for a paper resting heavily on Gaussian tail identities, a proper derivation rather than a sketch would be appropriate.

8. References: Holmstrom (1979) and Holmstrom & Milgrom (1987) are cited in the intro but not heavily used; the foundational moral-hazard literature could be engaged more explicitly given the framing of the paper as a principal-agent problem.

9. The notation $\Kcal := A_0 + f_1$ is introduced in Sec. 2.2 (model.tex line 83). Note that $f_1$ is the coefficient on $(r-r_f)$, so the units of $f_1$ are (AUM)/(return), making $\Kcal = A_0 + f_1$ well-defined only after specifying that $A_0$ and $f_1\cdot 1$ are both interpreted in AUM units. A short clarifying sentence on units would help readers.

10. The participation constraint normalization $\bar U=0$ (Sec. 3, footnote) is fine but the paper should verify the constraint is slack everywhere in the comparative-statics ranges, not just at the calibrated equilibrium.

11. Figure files in `paper/figures/` (e.g., `compstats_f2.png`) appear current, but the captions reference "comparative statistics" — should be updated together with the in-text usage.

12. Sec. 5 paragraph "Equilibrium outcomes" reports $\alpha\approx 0.6\%$ and $\beta\approx 6.5\%$ per unit of volatility for the affine approximation. With $\sigma_d^*\approx 12\%$, this gives $\alpha + \beta\sigma_d^* \approx 0.6\% + 6.5\%\cdot 0.12 = 1.38\%$, consistent with the claimed $\phi^*\approx 1.4\%$ — but the underlying IC value is not consistent with the formula (see Major Comment 2). This *internal* consistency within the numerical section makes me suspect the numerical code may have been written with a different (possibly correct) formula than what is in the paper, and the paper's formula was transcribed with the algebra error in Major Comment 1.

## Questions for the Authors

1. **On the FOC algebra (Major Comment 1).** Please verify the derivation of Eq. (\ref{eq:manager-FOC}) by hand. With $U_M = \phi\E[A] - \frac{\eta\phi^2}{2}\V[A]$, why does Eq. (\ref{eq:manager-FOC}) write $\eta\phi^2 \partial_\sigma\V[A]$ rather than $\frac{\eta\phi^2}{2}\partial_\sigma\V[A]$? Either the FOC is wrong or the utility definition was meant to omit the factor of $1/2$ — please reconcile.

2. **On the numerical equilibrium (Major Comment 2).** What code was used to compute the reported $\phi^*\approx 1.4\%$ in Sec. 5? Did the numerical implementation use Eq. (\ref{eq:phi-IC}) as written in the paper, or a different (perhaps corrected) version? Please provide replication code and re-state the equilibrium values consistent with whatever formula is ultimately deemed correct.

3. **On the comparative-statics baseline (Major Comment 3).** Why does the comparative-statics analysis use different parameters from the calibration ($f_2=0.5$ vs. $f_2=25$, $f_1=0.2$ vs. $f_1=1.5$, $\Sharpe=0.5$ vs. $0.35$, $\eta=2$ vs. $3$)? Can the figures be reproduced at the Section 4 baseline? If not, please explain the obstruction.

4. **On the global IC condition (Major Comment 5).** Have you verified that the IC fee implements $\sigma_d$ as the *global* maximizer of $U_M$, not just a local stationary point? Please report the result of this check across the parameter ranges in Appendix G.3.

5. **On the welfare claim (Major Comment 10).** The intro claims "explicit welfare comparison between the IC contract and the unconstrained equilibrium." Where is this comparison reported? Please add a panel showing $U_I$ at the unconstrained manager's choice and at the IC equilibrium, with the welfare gain explicitly tabulated.

6. **On manager preferences (Major Comment 7).** Can you provide an alternative parameterization (e.g., CARA over fee revenue with a fixed risk-aversion coefficient that does not scale with $\phi$) and check whether the qualitative results survive?

7. **On performance fees (Major Comment 8).** Can the IC fee schedule be derived analytically (or at least numerically tabulated) in the presence of a performance fee $\psi$ with a high-water mark? The current Appendix F is too sketchy to assess robustness.

8. **On implementation (Major Comment 9).** Can you quantify the welfare cost of using $\hat\sigma$ instead of $\sigma$ in the affine rule, under a standard return-window assumption? Even a back-of-the-envelope calculation would strengthen the practical-contract claim.

9. **On the kink at $r=r_f$ (Minor Comment 3).** Is the kink in the second derivative of $F$ quantitatively important? Does the conclusion change if you replace the piecewise quadratic flow with a smooth approximation?

10. **On "pay for risk, not luck" (Major Comment 6).** Do you intend "pay for risk, not luck" to apply to (a) the fee *rate* $\phi$, (b) the manager's *realized* compensation, or (c) the manager's *expected* compensation? The current framing conflates these. Please clarify.

---

**Quality self-check:**
- [x] Read all main sections, appendix, and bibliography
- [x] Major comments tied to specific equations and sections
- [x] Weighted score (47.8) matches the recommendation tier (< 65 → Reject), but a strong revision could push this into Major Revision territory
- [x] Distinguished between fatal flaws (algebra error in FOC; numerical inconsistency) and addressable weaknesses (writing, additional robustness)
- [x] Acknowledged that the paper has potential — the framing and tractability are appealing — but central derivations and numerical claims require substantial reworking
- [x] Did not reference any other referee's report

# Referee Report (Referee 2)
**Date:** 2026-05-14
**Paper:** Incentives and Risk-Taking in Delegated Portfolio Management: A Contracting Approach
**Target Journal:** Not specified explicitly in the manuscript; inferred from scope, JEL codes (G11, G23, D82), and template styling to be *Journal of Financial Economics* or *Review of Asset Pricing Studies*.
**Recommendation:** Major Revisions
**Overall Score:** 62.8/100

## Summary
The paper develops a two-period principal-agent model of delegated portfolio management in which a piecewise-quadratic flow-performance function generates a convex managerial payoff, leading to risk-shifting. The authors derive a closed-form incentive-compatible (IC) management fee schedule $\phi(\sigma_d)$ that implements an investor's desired volatility target $\sigma_d$, propose an affine approximation $\phi \approx \alpha + \beta \sigma_d$ marketed as a "pay for risk, not luck" rule, and provide a numerical calibration with $\sigma_d^* \approx 12\%$ and $\phi^* \approx 1.4\%$. The economic idea is intuitive and the algebra is largely correct, but in its current form the paper falls short of the rigor, novelty, and depth expected at JFE/RAPS: the IC fee schedule is essentially the ratio of two FOC derivatives the authors define themselves rather than an equilibrium solution to a contracting game with proper participation/IR/observability constraints; the single "Proposition" is a tautology (it just restates the FOC) and proves neither existence/uniqueness of $\sigma_d^*$ nor the signed comparative statics it claims; and the calibration section uses one parameter set for headline numbers and a *different* parameter set for every comparative-statics figure (Figs. 3–7), undermining internal consistency. Substantive revision of the contracting setup, formal results, and consistency between calibration and figures is required.

## Dimension Scores
| Dimension | Weight | Raw Score | Weighted | Notes |
|-----------|--------|-----------|----------|-------|
| Contribution & Novelty | 25% | 60 | 15.0 | Useful tractable benchmark, but incremental relative to Basak–Pavlova–Shapiro (2007), Carpenter (2000), and Cuoco–Kaniel (2011); novelty claim ("closed-form IC fee" and "pay for risk, not luck") is overstated given the structure of the result. |
| Model & Theory | 30% | 60 | 18.0 | Algebra is internally consistent, but the contracting environment is informal (no IR, no LL, no observability primitives, no IC against deviations off the equilibrium path), and the single "Proposition" is not a theorem in the usual sense. |
| Calibration & Numerics | 20% | 65 | 13.0 | Headline calibration is reasonable, but Section 5 silently switches parameters for every comparative-statics figure ($\Sharpe=0.5$, $\gamma=3$, $\eta=2$, $f_1=0.2$, $f_2=0.5$), which breaks the logic of a "calibrated" exercise. |
| Writing & Exposition | 15% | 72 | 10.8 | Generally readable and well-organized; notation is mostly consistent; some inconsistency between $\Sharpe$ and $S$ symbols; equation (D.1) has two slightly different forms in main text vs. appendix. |
| Journal Fit | 10% | 60 | 6.0 | Conceptually relevant for JFE/RAPS, but the contribution as written reads closer to a *Journal of Banking and Finance* or *Annals of Finance* short methodological note than a JFE paper. |
| **Weighted Total** | 100% | — | **62.8** | Recommendation: Major Revisions. |

## Major Comments

### M1. The "Proposition" is essentially a restatement of the FOC, not a theorem.
Section 3.1 (contract.tex lines 22–24) presents Proposition 1 ("Optimal Volatility Target"): *"an interior equilibrium volatility target $\sigma_d^*>0$ is characterized by the first-order condition \eqref{eq:investor-FOC} equal to zero ... In general, the resulting equation is nonlinear in $\sigma_d^*$ and is solved numerically; the comparative statics below are established by total differentiation of the first-order condition."* This is a definition, not a result. The proposition proves nothing:

- **Existence** is not shown — the FOC could fail to admit a zero on $(0, \overline{\sigma}]$.
- **Uniqueness** is not shown — the FOC is nonlinear through $\phi(\sigma_d)$, $\phi'(\sigma_d)$, and $\Delta_{\text{quad}}(\sigma_d)$, and could have multiple roots.
- **Comparative statics are not "established by total differentiation"** anywhere in the paper. Appendix D.2 only defines $G(\sigma)$ and observes $G(\sigma_d^*)=0$, with no sign analysis of $\partial G/\partial f_2$, $\partial G/\partial S$, $\partial G/\partial \gamma$. The qualitative claims in Section 3.1 (lines 30–32) about how $\sigma_d^*$ responds to $f_2$, $A_0$, $f_1$, $S$, $\gamma$, $\eta$ are asserted from figures, not proved.

For a paper whose stated contribution is "closed-form tractability" (introduction line 16), the absence of any actual theorem is the central weakness. The Proposition should either (a) prove existence/uniqueness under explicit, *verifiable* sufficient conditions on $(S, f_2, \eta, A_0, f_1)$, or (b) be downgraded to a remark and the paper's contribution reframed.

### M2. Sufficiency condition for the SOC is hand-waved.
Appendix C.2 (appendix.tex lines 116–118) states: *"Under the condition $\eta\phi \cdot 2\mathcal{K}^2 > 2 f_2 C_1$, the marginal cost grows faster than the marginal benefit for large values of $\sigma$"*, and then in the sufficiency paragraph: *"this condition is verified numerically across the calibrated parameter ranges in Appendix~G; it holds whenever $\Kcal\,S > 0$, which is ensured by $S>0$ and $A_0, f_1 > 0$."*

The last claim is incorrect. The condition $\eta\phi \cdot 2\mathcal{K}^2 > 2 f_2 C_1$ involves $\eta, \phi, f_2$ — none of which appear on the right-hand side of the implication $\mathcal{K}S>0$. Moreover, in the IC contract, $\phi$ itself is *endogenous* (a function of $\sigma_d$), so verifying the SOC requires substituting eq. (C.4) into the condition, which the authors decline to do. The SOC must dominate not just the linear $\sigma$ terms but also the cubic terms in $\Delta_{\text{quad}}(S, f_2; \sigma) = 6\mathcal{K} f_2 \sigma^2 \mathrm{Cov}(X, X^2 I) + 4 f_2^2 \sigma^3 \V(X^2 I)$ (eq. B.10).

The authors should either derive a clean analytical sufficient condition on the *primitives* $(S, f_2, \eta, A_0, f_1)$, or honestly state that the SOC is only verified numerically and provide a table showing $\partial^2 U_M/\partial \sigma^2$ at the IC fee across the calibrated parameter grid in Appendix G.3.

### M3. The "contract" lacks the formal apparatus of a contracting model.
For a paper titled "A Contracting Approach" submitted to JFE/RAPS, the contracting environment is surprisingly thin:

**(a) No participation/IR constraint is verified analytically.** The footnote on contract.tex line 8 normalizes the manager's reservation utility to $\bar{U}=0$ and asserts it is "verified to be slack at the calibrated equilibrium." But "verified numerically at one calibration point" is not a substitute for a result about when the IR constraint binds. The comparative statics in Figures 3–7 sweep $\Sharpe, f_2, \gamma, \eta, A_0, f_1$ over wide ranges — does the IR constraint remain slack throughout these sweeps? Section 4 paragraph "Participation constraint" (numerical.tex line 10) asserts so, but offers no figure or table of $U_M(\sigma_d^*, \phi^*)$ across the parameter space.

**(b) No limited-liability or no-negative-fees constraint.** The IC fee in eq. (C.4) can in principle be very small or even sign-flip if the denominator's $\Delta_{\text{quad}}$ overwhelms the numerator for large $\sigma$ or large $f_2$. The numerical section reports $\phi^* \approx 1.4\%$ at baseline, but no discussion is provided of whether $\phi(\sigma_d)>0$ over the comparative-statics ranges in Appendix G.3.

**(c) No observability discussion before Section 4.** The observability paragraph in Section 4 (numerical.tex line 12) is the first time the manuscript acknowledges that $\sigma$ is *not directly contractible*: *"the realized volatility $\hat{\sigma}$ must be estimated from a time series of fund returns, introducing estimation error."* If $\sigma$ is unobservable, the entire IC argument collapses — the manager chooses $\sigma$ unilaterally and the investor cannot verify the choice ex post except through noisy estimation. The paper handles this by deferring it to future work (*"a full extension of the model to estimated volatility is beyond the scope"*). This is the central frictions problem in the literature (Basak–Pavlova–Shapiro 2007 §3, Ou-Yang 2003 §2) and cannot be relegated to a one-paragraph caveat. Either (i) make $\sigma$ contractible by assumption and discuss when this is realistic (e.g., institutional mandates with explicit volatility targets), or (ii) extend the model to the unobservable case using realized-volatility estimates as a contract signal.

**(d) No off-equilibrium check.** The manager's FOC at $\sigma=\sigma_d$ is necessary for $\sigma_d$ to be a *local* optimum, but the paper never verifies it is a *global* optimum of the manager's problem. With a piecewise-quadratic flow function and CARA-type mean-variance utility, the manager's objective is non-concave in $\sigma$ over its full domain; one must check $U_M(\sigma_d, \phi(\sigma_d)) \ge U_M(\sigma, \phi(\sigma_d))$ for all $\sigma > 0$, not just locally.

### M4. The flow function specification is ad hoc and lacks defense.
Equation (eq:flow) in model.tex (line 26) — $F(r) = f_1 (r-r_f) + f_2 (r-r_f)^2$ for $r \ge r_f$ and $F(r)=f_1(r-r_f)$ for $r<r_f$ — has several unjustified features:

**(a) Kinked at $r_f$, not at the benchmark.** Empirically (Sirri–Tufano 1998, Chevalier–Ellison 1997), flow convexity exists *throughout* the upper part of the distribution but the threshold is the *relative ranking* against peers, not the risk-free rate. The authors should defend $r_f$ as the kink point or, more honestly, parameterize the kink with a benchmark $b$ and check sensitivity. As written, the kink is doing analytic work (it activates the indicator $I$ in eq. B.1) without an empirical or theoretical justification.

**(b) Unbounded flows.** The quadratic kicker $f_2 (r-r_f)^2$ is unbounded above. At calibration values $f_1=1.5, f_2=25$, a 30% excess return implies flows of $0.45 + 2.25 = 270\%$ of AUM — implausible. Real flow data is bounded (funds cannot scale arbitrarily). The authors note this is "right-tail" behavior but the unboundedness is not acknowledged as a limitation when the equilibrium $\sigma_d^*$ depends on right-tail moments $C_1, \E[X^3 I], \E[X^4 I]$ that diverge with $f_2$.

**(c) Sign restrictions.** The flow function should presumably satisfy $A_0(1+r) + F(r) \ge 0$ (no negative AUM), but with $f_1=1.5$, a return of $r-r_f = -2/3 \approx -67\%$ gives $F(r) = -1.0$, i.e., $A_0(1+r) + F(r) = 0.33 - 1.0 = -0.67$. This is impossible in practice (investors cannot withdraw more than AUM). The probability of such an event is small under Gaussian returns with $\sigma=12\%$, but the model's variance formulas integrate over all of $\mathbb{R}$, so the tail is being integrated where AUM is mathematically negative.

**(d) Why piecewise-polynomial?** The empirical flow-performance literature typically uses ranks (Sirri–Tufano) or piecewise-linear in performance bins (Chevalier–Ellison). The choice of $f_1(r-r_f) + f_2(r-r_f)^2$ is presented without empirical fit or robustness to alternative functional forms (e.g., $f_1(r-r_f) + f_2[(r-r_f)^+]^2$, logistic, or piecewise-linear in three bins). The authors should either calibrate $f_1, f_2$ from microdata (mutual fund flow regressions) or provide robustness to alternative parametric flow functions.

### M5. Inconsistent parameter sets between the calibration and the comparative-statics figures.
Section 4, numerical.tex line 8, footnote: *"For visual clarity, these comparative-statics figures use a simplified baseline: $\Sharpe=0.5$, $r_f=2\%$, $\gamma=3$, $\eta=2$, $A_0=1$, $f_1=0.2$, with $f_2=0.5$ for scale-sensitivity and risk-aversion figures."* But the calibrated baseline in Section 4 line 4 is $\Sharpe=0.35, r_f=3.70\%, \gamma=5, \eta=3, f_1=1.5, f_2=25$. **Six of the seven parameters change** between the headline calibration and the comparative-statics figures, and $f_2$ in particular drops from 25 to 0.5 — a 50× difference. This is not a "simplified baseline"; it is effectively a *different model* for the figures.

This is a significant problem because:
- The paper's contribution (per the introduction) is that the model produces empirically plausible numbers under realistic flow convexity. If $f_2=0.5$ is needed for "visual clarity," then the comparative statics shown in Figures 3–7 may not apply at the empirically calibrated $f_2=25$.
- Appendix G.3 reassures the reader that "all qualitative comparative statics ... are unchanged at the Section 4 baseline," but provides no figures or numbers to back this up. The reader cannot verify this claim.
- The flow function at $f_2=0.5$ is essentially *linear* over normal return ranges (at $r-r_f=10\%$, the quadratic term contributes $0.5 \times 0.01 = 0.005$ versus $0.2 \times 0.10 = 0.02$ from the linear term). So Figures 3–7 are effectively showing the comparative statics of an *almost-linear-flow* model, which is exactly the limit where the paper's main mechanism (convex flows → risk-shifting) disappears.

**Required:** Replot all comparative-statics figures at the Section 4 baseline, or provide a separate appendix figure suite confirming identical qualitative patterns hold at the calibrated $f_2=25$.

### M6. Novelty vis-à-vis Basak–Pavlova–Shapiro (2007) is not adequately differentiated.
Introduction line 16 acknowledges Basak–Pavlova–Shapiro (BPS) as the "closest predecessor" and claims three distinguishing contributions: (1) closed-form IC fee in a two-period setting, (2) affine approximation, (3) explicit welfare comparison. Examining each:

- **(1) Closed-form IC fee.** BPS already derive an explicit closed-form portfolio policy that highlights the risk-shifting distortion. The "IC fee" in eq. (C.4) is the ratio of two derivatives the authors construct themselves and is "closed-form" only in the same sense that an integral of a normal density is "closed-form." It contains $\Phi(S), \varphi(S), \Delta_{\text{quad}}$ — non-elementary functions.

- **(2) Affine approximation.** The affine approximation eq. (eq:phi-linear-approx) is a first-order Taylor expansion of the IC fee around $\sigma_d^*$. The paper presents this as the key practical innovation ("pay for risk, not luck"), but it is mechanical: any sufficiently smooth function admits a local linearization, and Figure 8 confirms it works *within $\pm 5\%$ of $\sigma_d^*$* — a narrow neighborhood. The claim that this provides a "practical contracting benchmark directly communicable to practitioners" (intro line 16) is hard to assess without a real-world test or comparison to existing mutual-fund fee structures.

- **(3) Explicit welfare comparison.** The paper does **not** in fact contain a welfare comparison. There is no comparison of $U_I$ under the IC contract versus $U_I$ under the unconstrained equilibrium (where the manager picks her preferred $\sigma$ given a fixed flat $\phi$). The introduction makes this claim (line 16) but the paper body does not deliver. This is a fixable omission and should be added (a single figure or table comparing $U_I^{\text{IC}}(\sigma_d^*)$ to $U_I^{\text{free}}(\sigma^*(\phi_0))$ at a few calibration points would suffice).

The "pay for risk, not luck" framing (Section 2.3) is rhetorically appealing but, on inspection, is just the statement that $\phi$ depends on the volatility *target* $\sigma_d$ not the *realization* — which is true of any deterministic ex ante fee schedule. The economic content (that the IC fee is an explicit function of $\sigma_d$ and admits an affine approximation) is real but modest.

### M7. The manager's mean-variance preference assumption is questionable.
The manager has mean-variance preferences over *fee revenue* $\phi A$ with risk aversion $\eta$ (model.tex line 56). This is unconventional in the delegated-portfolio-management literature, where managers are typically modeled with CRRA over consumption (BPS 2007, Carpenter 2000) or with monetary CARA over wealth (Holmstrom-Milgrom 1987). Several oddities:

**(a) The $\phi^2$ scaling.** $U_M = \phi \E[A] - (\eta \phi^2/2)\V[A]$. The risk term scales with $\phi^2$, which means a manager facing a 1% fee is *not* simply more concerned about AUM risk than a manager facing 2% — she is 4× as concerned. This is a quirk of the specification and the authors should either (i) defend it (e.g., the manager has CARA-$\eta$ utility over fee income, which yields $-\exp(-\eta \phi A)$ and the certainty equivalent is $\phi \E[A] - (\eta \phi^2/2) \V[A]$ under Gaussianity — fine, but then state it explicitly), or (ii) acknowledge the unusual specification.

**(b) Manager wealth and outside consumption.** The manager has no outside wealth in this setup, only fee revenue. Career concerns (cited at calibration.tex line 8) are mentioned but not modeled. If career concerns matter, they should enter $U_M$ explicitly.

**(c) Comparison with Carpenter (2000).** Carpenter shows that option-like compensation may *decrease* risk-taking when the manager is sufficiently risk-averse over personal wealth. The authors' result is the opposite (convex flows always increase risk-taking) because their manager has linear utility in expected fee revenue. This contrast should be discussed.

### M8. Linear approximation accuracy is only validated over a narrow window.
Numerical.tex line 6: *"The approximation error between the affine rule $\alpha+\beta\sigma_d$ and the exact IC fee $\phi(\sigma_d)$ is approximately 0.1% on average in absolute terms, evaluated within $\pm 5\%$ of $\sigma_d^*$."* And Figure 8 caption (figures.tex line 75): *"evaluated within $\pm 5\%$ of that target."*

A 5% window around $\sigma_d^* \approx 12\%$ is roughly $[11.4\%, 12.6\%]$ — extremely narrow. For an *implementable* contract, the affine rule must remain accurate over the *plausible* range of $\sigma_d$ choices, e.g., $[6\%, 20\%]$ as discussed in calibration.tex line 18. Show approximation error over the full empirically plausible range $\sigma_d \in [6\%, 20\%]$, not just $\pm 5\%$ of the optimum.

### M9. The investor's outside option is dropped without justification.
Contract.tex line 8 footnote: *"On the investor side, we similarly abstract from an outside option, though one can add the constraint $U_I(\sigma_d, \phi(\sigma_d)) \ge \bar{U}_I$ in the presence of competing managers."* In a paper about contracting in delegated portfolio management — a competitive market with thousands of funds — abstracting from the investor's outside option is a strong assumption. It means the investor has *all* bargaining power and extracts all surplus subject to the manager's IR constraint. This contradicts the empirical evidence (Gil-Bazo 2008, cited line 4) that fees are *higher* than competitive levels. At minimum, the authors should acknowledge that their IC fee $\phi(\sigma_d)$ is the *lowest* fee consistent with implementing $\sigma_d$, not the equilibrium fee in a competitive market.

### M10. Two slightly different presentations of the investor FOC.
The main-text version, eq. (eq:investor-FOC) in contract.tex line 18, reads:
$$
\frac{dU_I}{d\sigma_d} = [(1-\phi)S - \gamma(1-\phi)^2 \sigma_d] + [-(1 + r_f + S\sigma_d) + \gamma(1-\phi)\sigma_d^2] \frac{d\phi}{d\sigma_d}
$$
The appendix version, eq. (D.1) (appendix.tex line 160), reads:
$$
\frac{dU_I}{d\sigma_d} = [(1-\phi)S - \gamma(1-\phi)^2 \sigma_d] + [-(r_f + S\sigma_d) - 1 + \gamma(1-\phi)\sigma_d^2] \frac{d\phi}{d\sigma_d}
$$
These are algebraically equivalent ($-(1+r_f+S\sigma_d) = -(r_f+S\sigma_d) - 1$). Working through $\partial U_I/\partial \phi$ directly from eq. (eq:UI-expanded) confirms both forms are correct. Recommend rewriting to one canonical form for clarity.

## Minor Comments

1. **Symbol $\Sharpe$ vs $S$.** The macro `\Sharpe` is defined as `S` in main.tex line 70, but the appendix (e.g., eq. C.4) uses bare $S$ while the main text mostly uses $\Sharpe$. Pick one and apply uniformly.

2. **Unused macros.** `\posreal` and `\nnegreal` defined but never used (main.tex lines 41-42). Either delete or use them.

3. **Title page date.** "April 8, 2026" appears on the title page (main.tex line 83) but the system context indicates the paper is being reviewed in May 2026. Update to the current submission date.

4. **JEL code D82.** "Asymmetric information" seems misplaced — the model is moral hazard / hidden action, not asymmetric information about types. D86 ("Economics of Contract: Theory") would be more appropriate.

5. **Equation labeling.** The flow equation (model.tex line 26) is labeled `eq:flow` but rendered as eq. (2). Reference it consistently in the text instead of by number where possible.

6. **Citation in calibration of $\Sharpe=0.35$.** Calibration.tex line 10 cites Carhart (1997) for a Sharpe ratio of 0.35 "consistent with the performance range documented for skilled managers net of transaction costs." But Carhart's central message is that there is *little persistence* in mutual fund alpha, and the post-cost Sharpe ratio of skilled funds in his sample is closer to zero. Kosowski et al. (2006) (already in the bib file) would be a better citation.

7. **Conclusion is too short** (conclusion.tex, 8 lines). For a JFE/RAPS submission, the conclusion should summarize the contribution, place it in context, and discuss limitations more substantively. The current conclusion gestures at "run-like dynamics and risk of ruin" as future work but does not engage with the limitations identified in the paper itself (observability, IR slackness, flow function form).

8. **Figure 1 (flow performance)** caption says it uses $\sigma=0.15$ "for visual clarity" (figures.tex line 6). Since the flow function $F(r)$ does not depend on $\sigma$ (it only depends on $r$), $\sigma=0.15$ should not appear in the caption.

9. **Wording: "comparative statistics" should be "comparative statics".** This typo recurs in contract.tex line 30, model.tex line 109, and elsewhere. Standard econ usage is "comparative statics."

10. **Appendix section labeling.** Appendix sections are introduced with `\section{}` (appendix.tex line 12, etc.) but cross-referenced in the main text as "Appendix B," "Appendix C," etc. Verify in the compiled PDF that section numbering is letter-based (A, B, C, ...). The `\renewcommand{\theequation}{\Alph{section}.\arabic{equation}}` (appendix.tex line 6) only restyles equation numbers, not section numbers.

11. **Appendix F (perf-fee sketch)** is genuinely only a sketch — incorporating performance fees is sufficiently important for the paper's framing (Section 2.1 lines 48–52 discuss performance fees) that the sketch should be either expanded into a full subsection or explicitly defended as out of scope.

12. **Bibliography entry `Gil-Bazo2008`** contains a raw URN field and a long abstract (references.bib lines 30–31). Clean up.

13. **`hyperref` colored links** (main.tex line 23) — for journal submission, most economics journals require black-text hyperlinks in the final version.

14. **AUM units.** The calibration sets $A_0=1$ as a normalization but the flow function uses excess returns in decimal units (calibration.tex line 14). For a flow of "+13.8% of AUM" the formula gives $F = 0.1375$ which under $A_0=1$ is 13.75% of AUM — consistent. Worth stating once explicitly that all monetary quantities are normalized by $A_0$.

## Questions for the Authors

1. **Existence and uniqueness.** Can you provide a clean analytical sufficient condition on the *primitives* $(S, f_2, \eta, A_0, f_1)$ — not on $\phi$ — under which the manager's SOC holds and the investor's FOC has a unique zero on a stated interval?

2. **Welfare comparison.** Could you add a numerical exercise comparing $U_I^{\text{IC}}(\sigma_d^*)$ to $U_I^{\text{free}}(\sigma^*(\phi_0))$ under a fixed-fee benchmark $\phi_0$, to quantify how much the IC contract improves investor welfare? This would substantiate the third novelty claim in the introduction.

3. **Robustness to flow specification.** Have you tried alternative flow functions (piecewise-linear in performance ranks, logistic, capped quadratic) and verified that the affine approximation of the IC fee remains accurate? The piecewise-quadratic specification is doing a lot of analytic work; demonstrating robustness would strengthen the contribution.

4. **Observability.** How would the IC contract change if $\sigma$ is unobservable and the contract must use realized volatility $\hat{\sigma}$ estimated over a window of returns? Section 4 acknowledges this but defers it. Can you provide even a stylized treatment — e.g., the contract $\phi(\hat{\sigma}) = \alpha + \beta \hat{\sigma}$ with estimation error $\hat{\sigma} = \sigma + \nu$ — to show whether the affine approximation is robust to noise?

5. **IR constraint.** Across the comparative-statics ranges in Appendix G.3 ($f_2 \in [5, 60]$, $\Sharpe \in [0.1, 1.0]$, etc.), does the manager's IR constraint $U_M(\sigma_d^*, \phi(\sigma_d^*)) \ge 0$ remain slack? A figure or table would clarify this.

6. **Parameter consistency.** Why do Figures 3–7 use $f_2 = 0.5$ rather than the calibrated $f_2 = 25$? The 50× discrepancy is substantial and unexplained except as "visual clarity." Could you provide the comparative-statics figures at the Section 4 baseline as a supplement?

7. **Boundedness of flows.** With $f_1=1.5, f_2=25$, a +30% excess return implies +270% flows. How frequently does the model touch these implausible regions, and what fraction of the variance moments $\E[X^4 I]$ comes from realizations with $r - r_f > 30\%$? A robustness check capping flows at some plausible upper bound (e.g., 100% of AUM) would address this concern.

8. **Comparison with Carpenter (2000).** Carpenter shows that for sufficiently risk-averse managers, option-like compensation may *decrease* risk-taking. Your manager has linear utility in expected fee revenue and gets the opposite result. Can you reconcile?

9. **Global optimum of the manager's problem.** Have you verified that $\sigma_d$ is a *global* maximum (not just local) of $U_M(\sigma, \phi(\sigma_d))$ given the IC fee? With non-concave flows, multiple local maxima are possible.

10. **Empirical anchor for $\beta$.** The affine slope $\beta \approx 6.5\%$ per unit of volatility (Section 4 line 6) implies that increasing the volatility target from 10% to 15% raises the management fee from $0.6\%+6.5\%\times 0.10 = 1.25\%$ to $0.6\%+6.5\%\times 0.15 = 1.575\%$ — a 33% increase. Is there any empirical evidence (e.g., cross-sectional fee variation across funds with different volatility levels) that fees actually scale with volatility in this way?

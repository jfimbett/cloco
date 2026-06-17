<!--
EDITING GUIDE FOR FRANK
========================
This is the full paper text in a format that's easy to edit.

SAFE TO EDIT:
  - Regular prose paragraphs — edit freely
  - Text inside ^[...] markers — these are footnotes; edit the words freely
  - Text around $...$ inline math — edit the words; keep the dollar signs and content

DO NOT CHANGE:
  - \citep{...} or \citet{...} — these are citations; keep the key name inside unchanged
  - \ref{...}, \eqref{...}, \label{...} — cross-reference codes; keep exactly as-is
  - Anything between \begin{...} and \end{...} — these are math environments; leave them alone

TO COMPILE TO PDF after editing:
  python compile_md.py
-->

# Introduction {#sec:introduction}

Global assets under management have reached unprecedented levels, exceeding USD 128 trillion in 2024, with a substantial share allocated to delegated investment vehicles such as mutual funds, hedge funds, and institutional mandates.^[\url{https://web-assets.bcg.com/cc/0a/25876ea740168e908a8652e147d7/2025-gam-report-april-2025.pdf}; \url{https://www.pwc.com/ng/en/press-room/global-assets-under-management-set-to-rise.html}] In these settings, investors delegate portfolio decisions to professional managers while retaining only limited control over the underlying investment process. Unlike direct ownership of firms, where investors may exercise governance rights, delegated portfolio management typically involves contracts that specify outcomes rather than actions. As a result, investors have little influence over how risk is chosen or implemented, and managerial decisions are only imperfectly observable \citep{BebchukCohenHirst2017}.

This institutional structure creates scope for agency frictions. Managers are compensated primarily through fees linked to assets under management, while investors care about risk-adjusted returns as well. Empirical evidence further indicates that fees are not necessarily aligned with performance, as poorly performing funds may charge higher fees than better-performing peers \citep{Gil-Bazo2008}. At the same time, investor capital flows respond asymmetrically to performance. A large literature documents that inflows increase strongly with good performance, particularly in the upper tail of the return distribution, while outflows following poor performance are more gradual \citep{Ippolito1992ConsumerReaction, chevalier1997risk, sirri1998costly}. This convex flow--performance relationship implies that the mapping from performance to assets under management is nonlinear.

The interaction between fee structures and convex flows has important implications for managerial incentives. Because fees are proportional to assets under management, and assets respond disproportionately to strong performance, the manager's payoff becomes convex in returns. This convexity resembles the payoff of a financial option. As in standard option pricing, higher volatility increases the probability of extreme positive outcomes, which are disproportionately rewarded through inflows. Consequently, even when expected returns per unit of risk are unchanged, a manager can increase expected compensation by raising portfolio volatility \citep{BrownHarlowStarks1996}. This creates a divergence between the manager's privately optimal choice of risk and the level of risk preferred by investors.

The central objective of this paper is to characterize how compensation contracts can be designed to mitigate this risk-shifting incentive. We develop a tractable principal--agent model of delegated portfolio management in which the manager chooses portfolio volatility and investors allocate capital based on realized performance. The model incorporates a convex flow--performance relationship and a fee structure tied to assets under management. Within this framework, we derive the incentive-compatible contract that implements a target level of portfolio volatility chosen by the investor.

Our main result is that, under mild conditions, there exists a unique fee schedule that aligns the manager's incentives with the investor's desired risk target. This incentive-compatible fee can be expressed as a function of the target volatility. Furthermore, we show that over empirically relevant ranges, this relationship can be well approximated by a simple affine function. This yields a contract that can be interpreted as compensating the manager for the level of risk undertaken rather than for realized outcomes. We refer to this structure as a ``pay for risk, not luck'' framework. A numerical calibration based on empirical parameter values demonstrates that the linear approximation closely tracks the optimal contract and provides a practical representation of the underlying incentive structure.

This paper contributes to the literature on agency problems in delegated portfolio management. In classic principal--agent models, investors contract on observable outcomes because effort and information acquisition are not directly observable \citep{Holmstrom1979, AdmatiPfleiderer1997}. This gives rise to well-known distortions, including underinvestment in costly effort, short-horizon behavior around evaluation dates, and actions that increase private benefits at the expense of investor welfare \citep{JensenMeckling1976, Musto1999, CarhartKanielMustoReed2002}. Our contribution is to highlight a distinct channel through which agency frictions arise. Specifically, we show that the interaction between convex investor flows and standard fee structures creates an endogenous incentive to increase portfolio volatility, even in the absence of explicit performance fees. Relative to existing work on incentive contracts in asset management \citep{Starks1987, AdmatiPfleiderer1997, HolmstromMilgrom1987}, our framework provides a tractable characterization of how contracts can be designed to control risk-taking directly. Rather than focusing solely on performance-based compensation, we derive a contract that implements a desired risk level as an equilibrium outcome. This approach shifts the emphasis from ex post evaluation of performance to ex ante alignment of incentives.

The closest predecessor to this framework is \citet{basak2007optimal}, who derive optimal portfolio policies for managers facing AUM-linked compensation under convex investor flows in a continuous-time setting with CRRA preferences and benchmark-relative returns. Their analysis fully characterizes the equilibrium volatility distortion: flow convexity generates an option-like payoff that induces managers to tilt toward higher risk. Our contribution is complementary and distinct in three respects. First, we work within a tractable two-period setting that yields a closed-form incentive-compatible fee schedule mapping any investor volatility target to an explicit, implementable compensation level. Continuous-time formulations typically characterize the equilibrium distortion but do not deliver closed-form contract rules directly communicable to practitioners. Second, the tractability of our framework allows us to derive an affine approximation to the exact incentive compatible (IC) fee schedule and verify numerically that approximation errors are small over empirically relevant ranges, yielding a practical contracting benchmark. Third, our framework allows explicit welfare comparison between the IC contract and a flat-fee benchmark, quantifying the gains from incentive alignment as a function of flow convexity.

Additional related work includes \citet{Starks1987}, who shows that performance incentive fees generate risk-shifting through option-like payoffs; \citet{Carpenter2000}, who demonstrates that option-like compensation more broadly raises managerial risk appetite under nonlinear incentive structures similar to those studied here; \citet{CuocoKaniel2011}, who study equilibrium asset prices in the presence of delegated portfolio management with AUM-linked compensation and document price distortions arising from managerial incentives; and \citet{HuangSialmZhang2011}, who provide empirical evidence that risk shifting in mutual funds is economically significant. Continuous-time principal--agent models for delegated asset management are developed by \citet{OuYang2003}, who characterize optimal contracts under moral hazard; our two-period framework obtains a comparable characterization analytically, trading dynamic completeness for closed-form tractability. \citet{berk2004mutual} predict that positive alpha is competed away by investor flows; our model treats fund skill as given and focuses on the contractual problem conditional on that skill, an approach consistent with the evidence in \citet{carhart1997persistence} that performance persistence is limited but nonzero. \citet{VayanosWoolley2013} study slow-moving capital and flow-induced momentum in a delegated management context; the flow dynamics in our model share the same empirical motivation, though we focus on the contracting problem rather than equilibrium asset prices.

The remainder of the paper is organized as follows. Section \ref{sec:environment} presents the model and characterizes the incentive-compatible fee schedule. Section \ref{sec:contract} analyzes the investor's optimal contract design problem. Section \ref{sec:calibration} provides a calibration of the model. Section \ref{sec:numerical} presents the numerical illustration. Section \ref{sec:conclusion} concludes.


# The Model {#sec:environment}

We now introduce a tractable model of delegated portfolio management that captures the interaction between portfolio risk, investor flows, and fee-based compensation. The framework is designed to isolate the mechanism through which convex flow--performance relationships affect managerial incentives and to provide a setting in which incentive-compatible contracts can be characterized analytically.

## Setup

Consider a two-period economy $t\in\{0,1\}$ populated by a representative fund and a continuum of investors. The fund generates excess returns over a risk--free rate with a constant Sharpe ratio as follows:
\begin{equation}
    r-\rf \;=\; \Sharpe\,\sigma \;+\; \sigma\,\epsilon,
    \qquad \epsilon \sim \Normal(0,1),\ \sigma>0,
\end{equation}
where $\Sharpe$ is the Sharpe Ratio of the fund, assumed to be common knowledge between manager and investors. The volatility $\sigma$ is a decision variable of the asset manager. Within a standard asset pricing interpretation, $\sigma$ can be viewed as scaling exposure to a strategy with constant Sharpe ratio, for example through leverage.
Intuitively, $\sigma$ is the risk knob: raising it increases expected excess return, but it also increases the dispersion of outcomes around that mean. The model treats $\sigma$ as the contracting variable: the investor specifies a target $\sigma_d$ and the IC contract implements it. In practice, $\sigma$ must be estimated from a time series of realized returns, and estimation noise introduces measurement error into the implemented contract; Section \ref{sec:numerical} discusses this practical limitation and implementation strategies.

With this setup, expected excess returns increase linearly with volatility:

$$
\E[r-\rf]=\Sharpe \sigma,\qquad \V[r-\rf]=\sigma^2,
$$

Thus, taking more risk by increasing $\sigma$ raises average performance but also increases uncertainty, and returns can be written as $r=\rf+\sigma(\Sharpe+\epsilon)$.

Both current and potential investors exhibit a convex response to the fund's positive performance. They invest disproportionately more during periods of good performance and redeem during bad times.

We assume a reduced form relation between past performance and fund flows. Let flows to the fund after current and potential investors observe $r$ be
\begin{align}
    \label{eq:flow}
    F(r) = \begin{cases}
      f_1 (r-\rf) + f_2 (r-\rf)^2 & \text{if } r \ge \rf,\\[3pt]
      f_1 (r-\rf) & \text{if } r< \rf,
   \end{cases}
\end{align}
with $f_1,f_2\ge 0$. This flow function captures the asymmetric response of investors to performance: when returns fall below the risk--free rate, investors withdraw capital at a constant linear rate, whereas once returns exceed $\rf$, inflows become convex in performance. The quadratic term amplifies flows after good outcomes, reflecting performance chasing in the right tail (see Figure \ref{fig:flow-performance}).

Assets under management (AUM) at the end of the period evolve based on the return of the fund and the new net flows.
\begin{equation}
    A \;=\; A_0(1+r)\;+\;F(r),
\end{equation}
so AUM is the sum of a pure performance component (initial assets grown by the return) and a scale component coming from investor reallocations after observing performance.

We model the management fee at rate $\phi$ as applied to end-of-period AUM. In practice, mutual funds typically charge based on the beginning-of-period or average AUM. In this single--period setting, charging on end--of--period or average AUM is equivalent up to first order in $\phi$; Appendix \ref{app:fee-base} shows the equivalence and how to translate between conventions. The investor's *net* return per unit of initial wealth is then
\begin{equation}
\label{eq:net-return}
r^{\text{net}} \;=\; r \;-\; \phi\,(1+r) \;=\; (1-\phi)\,r - \phi.
\end{equation}
This relation shows that management fees reduce the investor's payoff in two ways: they scale down the gross return and subtract the fee rate.

For small $\phi$, it is common to use an approximation: $r^{\text{net}}\approx r-\phi$. Equation \eqref{eq:net-return} is exact and we will use it across the paper. Although fee structures vary across the asset management industry, the linear specification adopted here provides a tractable benchmark and can be extended to alternative compensation schemes.

If a performance fee $\psi$ is charged on positive excess performance, a reduced--form net return is

$$
r^{\text{net}} \;=\; r - \phi(1+r) - \psi\,(r-\rf)^+.
$$

In this specification, the performance fee applies only when the fund beats the risk--free rate. Relative to a pure management fee, this shifts more compensation into upside states. Since the manager's incentives already tilt toward the right tail when flows are convex, performance fees can materially affect the equilibrium. In the extension with performance fees, the economic mechanism is unchanged, but closed-form expressions become less transparent, so we rely on numerical solutions and the corresponding fee--volatility relationships.

This specification ignores high--water marks (HWM) that are common in alternative investment funds. Omitting HWM slightly overstates the right--tail convexity in manager pay. Appendix \ref{app:perf-fee} sketches how to incorporate HWM in our normal--returns setting.

The manager has mean variance preferences with a constant absolute risk aversion $\eta>0$ over fee revenue $\phi A$:
\begin{equation}
    U_M \;=\; \phi\E[ A] \;-\; \frac{\eta}{2}\phi^2\,\V[A],
\end{equation}
so the manager values higher expected fee income but dislikes fluctuations in AUM because they make fee income risky. We take this mean-variance functional as a primitive specification for the manager's preferences over fee revenue. It corresponds to the certainty equivalent of a CARA agent with coefficient $\eta$ facing a Gaussian distribution of $\phi A$: under Gaussian returns and linear flows ($f_2=0$), $\phi A$ is exactly Gaussian and the functional is exact. With $f_2>0$, AUM inherits non-Gaussian components from the convex kicker $f_2\sigma^2 X^2 I$; the specification is then best understood as a tractable first-order approximation to CARA certainty equivalence that preserves the key economic forces --- the marginal cost of risk-taking scales with $\phi^2$ --- while maintaining analytical tractability.^[The $\phi^2 V[A]$ scaling is consistent with a CARA-Gaussian certainty equivalent if one approximates $\phi A$ by its first two moments. The approximation is exact when $f_2=0$ (linear flows, Gaussian fee revenue) and remains accurate for the parameter values considered in Section \ref{sec:numerical}.]

Investors have mean-variance preferences over net returns with a risk aversion captured by $\gamma>0$:
\begin{equation}
\label{eq:UI}
    U_I(\sigma,\phi)\;=\;\E[r^{\text{net}}] \;-\; \frac{\gamma}{2}\,\V[r^{\text{net}}].
\end{equation}
Using \eqref{eq:net-return}, a convenient representation is
\begin{equation}
\label{eq:UI-expanded}
U_I(\sigma,\phi) \;=\; (1-\phi)\,(\rf+\Sharpe\sigma) - \phi \;-\; \frac{\gamma}{2}\,(1-\phi)^2\,\sigma^2.
\end{equation}
This makes the investor's trade-off transparent: higher volatility $\sigma$ raises expected return when the fund has skill ($\Sharpe>0$), but it raises risk quadratically; fees lower the investor's mean payoff and rescale effective exposure.


## Manager's problem and incentives {#sec:manager}

The manager controls volatility $\sigma$, and, through $\sigma$, affects both the fund's return distribution and investor flows. This creates a central incentive mechanism in the model: when flows are convex in good states, taking more risk increases the likelihood and magnitude of extreme positive outcomes, and such outcomes attract disproportionately large inflows. Since fees are proportional to AUM, the manager benefits from this right-tail scaling.

To isolate the mechanism, it is helpful to think of end-of-period AUM as having a deterministic base plus a component that increases with realized performance and flows. With skill ($\Sharpe>0$), raising $\sigma$ increases expected performance, and thus expected AUM. With convex flows ($f_2>0$), raising $\sigma$ does more than that: it increases the weight on upside states where inflows accelerate, so expected fee revenue becomes especially sensitive to volatility. At the same time, AUM becomes riskier when $\sigma$ increases. The exact mean and variance expressions (and their derivatives with respect to $\sigma$) are summarized below, with full derivations provided in Appendix \ref{app:variance}.

Let $\Kcal:=A_0+f_1$, $X=\Sharpe+\epsilon$, $I:=\mathbf{1}_{\{X\ge 0\}}$. Using $r=\rf+\sigma X$, end-of-period AUM can be written as
\begin{equation}
A \;=\; A_0(1+\rf) \;+\; \Kcal\,\sigma X \;+\; f_2\,\sigma^2 X^2 I.
\end{equation}
Expected AUM is given by
\begin{align}
\E[A] &= A_0(1+\rf) + \Kcal\,\Sharpe\,\sigma + f_2\,\sigma^2\,C_1, \label{eq:EA}\\
C_1 &:= (\Sharpe^2+1)\,\PhiStd(\Sharpe) + \Sharpe\,\phiStd(\Sharpe). \label{eq:C1}
\end{align}
The variance of AUM is
\begin{align}
\V[A] &= \Kcal^2\,\sigma^2 + 2\,\Kcal f_2\,\sigma^3\,\Cov(X, X^2 I) + f_2^2\,\sigma^4\,\V(X^2 I), \label{eq:VarA}
\end{align}
where $\Cov(X, X^2 I)$ and $\V(X^2 I)$ have closed-form expressions provided in Appendix \ref{app:variance}.

Differentiating with respect to $\sigma$,
\begin{align}
\partial_\sigma \E[A] &= \Kcal\,\Sharpe + 2 f_2\,\sigma\,C_1, \label{eq:dEA}\\
\partial_\sigma \V[A] &= 2\Kcal^2\sigma + \Delta_{\text{quad}}(\Sharpe,f_2;\sigma), \label{eq:dVarA}
\end{align}
where $\Delta_{\text{quad}}$ collects higher-order terms defined in Appendix \ref{app:variance}.

The manager chooses $\sigma$ to maximize

$$
U_M(\sigma,\phi)\;=\;\phi\,\E[A] - \frac{\eta}{2}\phi^2\,\V[A].
$$

The resulting best response $\sigma^*(\phi)$ is characterized in Appendix \ref{app:manager-solution}. The comparative statics are intuitive: higher risk aversion $\eta$ reduces risk-taking because the manager dislikes fee revenue volatility; higher convexity $f_2$ increases risk-taking because convex flows make upside states more valuable. This characterization highlights the core agency friction in the model: in the absence of contractual discipline, the manager's privately optimal volatility generally exceeds the level preferred by investors.

For implementation, a simple and accurate approximation to the incentive--compatible schedule is to set the management fee approximately linear in the desired volatility target $\sigma_d$:
\begin{equation}
\label{eq:phi-linear-approx}
\phi(\sigma_d) \,\approx\, \alpha \, + \, \beta\,\sigma_d.
\end{equation}
This affine approximation provides a tractable representation of the incentive-compatible contract derived below. It implies that, over the relevant range of risk targets, one can treat the incentive-compatible fee as a linear function of the desired volatility. In practice, $\alpha$ plays the role of a base fee level, while $\beta$ governs how strongly fees adjust when the investor raises or lowers the volatility target. In the model, $\alpha$ and $\beta$ can be obtained by locally linearizing the exact incentive--compatible fee around a reference volatility (Appendix \ref{app:investor}).


## Incentive compatibility: Implementing a target $\sigma_d$ {#subsec:IC}

Our goal is to align the interests of the manager and the investor by designing a contract that implements a desired level of risk. Let $\sigma_d$ be the investor's desired volatility target. An incentive-compatible (IC) fee $\phi(\sigma_d)$ must make the manager willing to choose exactly $\sigma_d$.

The IC condition has a simple economic form: at the target, the manager's marginal benefit of raising volatility (through higher expected assets under management and associated flows) must be exactly offset by the marginal cost (through higher AUM risk). This pins down a unique fee level as a function of the target, under mild regularity conditions. The exact expression and existence and uniqueness conditions are summarized below, with full derivations provided in Appendix \ref{app:manager-solution}, and Figure \ref{fig:ic-fee-curve} visualizes the mapping $\sigma_d\mapsto \phi(\sigma_d)$.

The manager solves

$$
\max_\sigma \; \phi\,\E[A] - \frac{\eta}{2}\phi^2\,\V[A],
$$

which yields the first-order condition
\begin{equation}
\phi\Big(\Kcal \Sharpe + 2 f_2\,\sigma\,C_1\Big) - \frac{\eta}{2}\phi^2\Big(2 \Kcal^2 \sigma + \Delta_{\text{quad}}\Big) \;=\; 0.
\label{eq:manager-FOC}
\end{equation}
For any target volatility $\sigma_d$, the incentive-compatible fee that induces the manager to choose $\sigma_d$ is given by imposing the FOC at $\sigma=\sigma_d$:
\begin{equation}
\label{eq:phi-IC}
\phi(\sigma_d)
\;=\;
\frac{2\Big(\Kcal\,\Sharpe + 2 f_2 \,\sigma_d\,C_1\Big)}
{\eta\Big(2 \Kcal^2 \,\sigma_d + \Delta_{\text{quad}}(\Sharpe,f_2;\sigma_d)\Big)}.
\end{equation}
This mapping is central to the analysis, as it translates a desired risk policy into an implementable compensation scheme. The implications of this mapping for equilibrium contract design are analyzed in the next section.

The incentive-compatible fee schedule $\phi(\sigma_d)$ embodies a specific principle: the manager is compensated for the level of risk undertaken, not for realized outcomes. To formalize this, decompose end-of-period AUM as

$$
A \;=\; \underbrace{\E[A]}_{\text{risk component}} \;+\; \underbrace{(A - \E[A])}_{\text{luck component}},
$$

where $\E[A] = A_0(1+\rf) + \Kcal\,\Sharpe\,\sigma + f_2\,\sigma^2\,C_1$ depends on the manager's volatility choice $\sigma$ but not on the realized shock $\epsilon$, while $A - \E[A]$ depends on $\epsilon$ but has mean zero. Manager fee revenue $\phi A$ inherits this decomposition: the risk component $\phi\E[A]$ is determined entirely by $\sigma$ (the manager's action), while the luck component $\phi(A-\E[A])$ reflects pure realized variation. The IC contract sets the fee *rate* $\phi = \phi(\sigma_d)$ as a function solely of the volatility target $\sigma_d$; realized compensation $\phi A$ still varies with the return shock $\epsilon$ through the luck component $\phi(A-\E[A])$. What the IC contract achieves is that the *rate* at which the manager is compensated depends only on the chosen risk level, not on realized outcomes --- the manager cannot increase the fee by selecting a different volatility. The affine approximation $\phi \approx \alpha + \beta\sigma_d$ makes this structure transparent: the base fee $\alpha$ covers fixed compensation and the marginal charge $\beta\sigma_d$ rises with the risk target.

It is important to clarify the interpretation of $\phi(\sigma_d)$ in the model versus its implementation. In the theoretical model, the equilibrium is a single fee *level* $\phi^* = \phi(\sigma_d^*)$: the investor announces this fee rate ex ante, and the IC condition ensures that the manager's privately optimal response is exactly $\sigma_d^*$. The manager does not face a fee that adjusts with realized volatility; the fee is fixed at $\phi^*$ regardless of the manager's action. What aligns incentives is that, at the fee level $\phi^*$, the manager's FOC is satisfied at $\sigma_d^*$. In practice, one natural implementation maps estimated realized volatility $\hat\sigma$ to a fee via the affine rule $\phi \approx \alpha + \beta\hat\sigma$; this is a *contingent schedule* on $\hat\sigma$, and its IC properties in the presence of estimation noise are an important direction for future work (discussed further in Section \ref{sec:numerical}).


# Contract Design: Investor's Problem {#sec:contract}

## Investor's Problem and Equilibrium {#sec:investor}

Building on the incentive-compatible mapping derived in Section \ref{sec:environment}, the main comparative statics follow directly from the mechanism. Stronger flow convexity $f_2$ makes volatility more privately valuable to the manager because it increases upside scaling; therefore, keeping the manager at the desired risk target requires a more restrictive contract, which in the model is reflected in a lower incentive-compatible management fee. Conversely, a more risk-averse manager (higher $\eta$) requires a lower IC fee to implement any given target: the manager's natural aversion to AUM volatility already restrains excessive risk-taking, reducing the contractual cost of incentive alignment.

We now characterize the investor's contract design problem, taking into account incentive compatibility and participation constraints. The investor chooses $\sigma_d$ (hence $\phi(\sigma_d)$) to maximize its utility subject to IC and the manager's participation constraint:^[We normalize the manager's reservation utility $\bar{U} = 0$ as a convenient benchmark: the manager's participation constraint is $U_M(\sigma_d, \phi(\sigma_d)) \ge 0$, which is verified to be slack at the calibrated equilibrium in Section \ref{sec:numerical}. On the investor side, we similarly abstract from an outside option, though one can add the constraint $U_I\big(\sigma_d,\phi(\sigma_d)\big) \geq \bar{U}_I$ in the presence of competing managers.]
\begin{align}
\max_{\sigma_d>0}\quad & U_I\big(\sigma_d,\phi(\sigma_d)\big) \\
\text{s.t.}\quad & U_M\big(\sigma_d,\phi(\sigma_d)\big)\ge \bar U. \nonumber
\end{align}
Investor utility is given by
\begin{equation}
U_I(\sigma_d,\phi) \;=\; (1-\phi)\,(\rf+\Sharpe\sigma_d) - \phi \;-\; \frac{\gamma}{2}\,(1-\phi)^2\,\sigma_d^2.
\end{equation}
Differentiating the investor's objective with respect to $\sigma_d$ using the chain rule yields
\begin{align}
\frac{d U_I}{d \sigma_d} &= \Big[(1-\phi)\Sharpe - \gamma(1-\phi)^2\sigma_d\Big] + \Big[-(1+\rf+\Sharpe\sigma_d) + \gamma(1-\phi)\sigma_d^2\Big]\frac{d\phi}{d\sigma_d}. \label{eq:investor-FOC}
\end{align}

\begin{remark}[Characterization of the Optimal Volatility Target]
Under $S > 0$, $f_2 > 0$, and $\eta, \gamma > 0$, an interior equilibrium volatility target $\sigma_d^* > 0$ is characterized by the first-order condition \eqref{eq:investor-FOC} equal to zero, i.e., $G(\sigma_d^*)=0$ in the notation of Appendix \ref{app:investor}. The condition reflects both the direct effect of volatility on expected returns and risk (the first bracketed term) and the indirect effect through the incentive-compatible fee adjustment $d\phi/d\sigma_d$ (the second bracketed term). The equilibrium fee is $\phi^* = \phi(\sigma_d^*)$ from \eqref{eq:phi-IC}. Existence of an interior solution follows from the intermediate-value theorem applied to $G(\cdot)$ under the condition in Appendix \ref{app:manager-solution}; uniqueness is verified numerically across the full parameter grid in Appendix \ref{app:numerical}. The resulting nonlinear equation is solved numerically; the comparative statics below are established by total differentiation of the first-order condition.
\end{remark}

The first term in the first-order condition captures the standard trade-off between expected return and risk: increasing volatility raises expected returns when the Sharpe ratio is positive but also increases variance. The second term reflects the contract adjustment required to sustain incentive compatibility. Because higher target volatility requires adjusting fees to discipline the manager, changes in $\sigma_d$ affect investor utility not only through portfolio risk but also through the share of returns retained after fees.

This program summarizes the investor's contract design problem: choose a volatility target $\sigma_d$ that maximizes investor utility while guaranteeing that the manager is willing to participate and implement the target. The conflict of interests is immediate in the model. The investor values higher $\sigma_d$ only to the extent that the fund's skill (Sharpe ratio) compensates for additional risk, net of fees. The manager, in contrast, values higher $\sigma$ not only because it increases expected performance when $\Sharpe>0$, but also because it increases the probability and magnitude of inflows triggered by extreme positive outcomes. Incentive compatibility provides the key mechanism for alignment: for each target $\sigma_d$ there is a fee level that makes the manager choose exactly that risk, turning the investor's policy choice into an implementable contract. The equilibrium target and the associated fee can be computed numerically; the first-order condition and the derivative of the fee schedule are given in Appendix \ref{app:investor}.

The structure of the optimal contract can be characterized through comparative statics without solving the model numerically. First, an increase in flow convexity $f_2$ increases the option value of volatility for the manager, hence the IC fee $\phi(\sigma_d)$ must fall to keep incentives aligned (see Figure \ref{fig:comp-f2}). For the investor, the contract becomes more ``expensive'' to adjust (large $|d\phi/d\sigma_d|$), pushing optimal $\sigma_d$ down. Second, an increase in the scale of the agency problem (higher initial AUM $A_0$ or the linear term $f_1$) amplifies AUM sensitivity to performance; as shown in Figure \ref{fig:comp-scale}, both desired volatility $\sigma_d$ and the IC fee $\phi(\sigma_d)$ tend to decrease. Third, managerial skill (an increase in the Sharpe Ratio of the fund) improves the direct mean gain from risk taking; this tends to raise the optimal target, but the IC adjustment offsets part of the effect (see Figure \ref{fig:comp-sharpe}). Finally, as illustrated in Figure \ref{fig:comp-risk}, an increase in the investor's risk aversion ($\gamma$) reduces $\sigma_d$; while a higher manager $\eta$ lowers the IC fee required to implement any given $\sigma_d$, since the manager's natural risk aversion provides internal discipline that reduces the fee burden on the investor (see Figure \ref{fig:comp-risk}).

For implementation, the linear approximation \eqref{eq:phi-linear-approx} introduced in Section \ref{sec:manager} provides a simple way to communicate the contract as a base fee plus a marginal charge for volatility. Evaluated within $\pm 5\%$ of the optimal target $\sigma_d^*$ (i.e.\ roughly $[12\%, 14\%]$ at the baseline calibration), this affine rule achieves average absolute errors below $0.1$ percentage points of the fee level (Appendix \ref{app:investor} and Figure \ref{fig:affine-approx}).


# Calibration {#sec:calibration}

We calibrate the model to empirically grounded parameter values from the mutual fund and portfolio choice literature, ensuring that the implied equilibrium outcomes fall within empirically plausible ranges for delegated portfolio management.

We set $\gamma=5$ as the baseline investor risk aversion, with sensitivity analysis spanning $\gamma\in[2,10]$. These values are consistent with standard portfolio-choice calibrations \citep[][]{campbell2002strategic} and reflect the observed heterogeneity in risk preferences across investors \citep[][]{guiso2018time}.

We set $\eta=15$ as the baseline manager risk aversion over fee revenue, with sensitivity spanning $\eta\in[3,30]$. The key economic rationale is that fee income is the manager's primary and largely undiversifiable source of compensation. A portfolio manager whose livelihood depends on AUM-linked revenue cannot hedge fee-income risk across multiple positions the way a diversified investor can. Career concerns further amplify effective risk aversion: a manager who underperforms relative to peers faces redemptions, reputational damage, and possible termination, all of which are convex in downside outcomes \citep[][]{chevalier1997risk, BrownHarlowStarks1996}. Setting $\eta=15$ --- three times the investor's risk aversion $\gamma=5$ --- reflects this concentration premium over fee-revenue risk. The sensitivity analysis in Section \ref{sec:numerical} confirms that the model's qualitative predictions are robust across the full sweep of $\eta\in[3,30]$.

We set $\Sharpe=0.35$ (annualized) for an active mutual fund baseline, consistent with the performance range documented for skilled managers net of transaction costs \citep[][]{carhart1997persistence}. We explore $\Sharpe\in[0.10,1.00]$ in sensitivity analysis, with higher values (e.g., $\Sharpe=0.60$) representing particularly skilled managers or hedge fund strategies \citep[][]{fung2004hedge}.

We use $r_f=3.70\%$ (annual), based on the 3-month U.S. Treasury constant maturity rate as of January 2026.^[Source: FRED series DGS3MO, 2026-01-23: 3.70\%. For euro-denominated settings, the ECB €STR (euro short-term rate) was approximately 1.93\% as of the same date.] The qualitative results are robust to alternative risk-free rate values across plausible ranges, as $r_f$ enters the model only through the flow threshold and the net return level, and its effects on equilibrium $\sigma_d^*$ and $\phi^*$ are second-order relative to the convexity and risk-aversion parameters.

Empirical studies document strong convexity in the flow-performance relationship, whereby top-performing funds attract disproportionately large inflows \citep[][]{sirri1998costly, ferreira2012flow}. To match realistic annual flow responses, we set $f_1=1.5$ and $f_2=25$, where excess returns are measured in decimal units (e.g., a 5\% excess return corresponds to 0.05). This parameterization implies that a fund with $+5\%$ excess return experiences flows of approximately $+13.8\%$ of AUM, while a fund with $+10\%$ excess return sees flows around $+40\%$, capturing the strong convexity observed in empirical flow--performance relationships. We explore $f_1\in[0.5,3]$ and $f_2\in[5,60]$ to assess sensitivity to flow convexity.

We normalize $A_0=1$ since the problem is scale-invariant with proportional fees and homogeneous preferences. If one were to incorporate decreasing returns to scale or capacity constraints, AUM scale would interact with fund performance \citep[][]{berk2004mutual}, but we abstract from such effects in our baseline specification.

With these parameters, the model produces optimal volatility targets $\sigma_d^*\in[8\%,20\%]$ (annualized), which are consistent with observed volatility levels for actively managed equity mutual funds. For reference, \citet[][]{barras2010false} use a monthly market-return standard deviation of approximately 4.6\%, corresponding to roughly 16\% annualized. Individual fund volatilities can be higher or lower depending on style and leverage, but our target range aligns with typical volatilities of delegated equity portfolios.


# Numerical Illustration {#sec:numerical}

We now illustrate the quantitative implications of the model using the calibrated parameters described in Section \ref{sec:calibration}. The baseline parameters are $\Sharpe=0.35$, $r_f=3.70\%$, $\gamma=5$, $\eta=15$, $A_0=1$, $f_1=1.5$, and $f_2=25$.

At the baseline calibration, the model delivers an equilibrium volatility target $\sigma_d^* \approx 12.8\%$ (annualized), consistent with the volatility range for actively managed equity funds noted in Section \ref{sec:calibration}. The incentive-compatible fee is $\phi^* \approx 3.95\%$, computed from the IC fee schedule \eqref{eq:phi-IC} and the investor's first-order condition \eqref{eq:investor-FOC}. The manager's equilibrium utility $U_M(\sigma_d^*, \phi^*) \approx 0.050 > 0$, confirming that the participation constraint $U_M \ge 0$ is slack at the calibrated optimum. The affine approximation error between the rule $\alpha + \beta\sigma_d$ and the exact IC fee $\phi(\sigma_d)$ is approximately 0.08 percentage points on average in absolute terms, evaluated within $\pm 5\%$ of $\sigma_d^*$ (see Figure \ref{fig:affine-approx}). Figure \ref{fig:incentive-alignment} confirms incentive alignment: the investor's utility is maximized at $\sigma_d^*$ along the IC curve, and the manager's utility under the fixed IC fee $\phi^*$ is itself maximized at exactly $\sigma_d^*$. Figure \ref{fig:welfare} provides the welfare comparison against a flat-fee benchmark of $\phi_{\rm mkt}=2\%$ (an empirically typical management fee). At the flat fee, the manager freely chooses $\sigma^{\rm free}\approx 19.1\%>\sigma_d^*$, exploiting convex flows. Under the flat fee the investor's utility $U_I(\sigma^{\rm free},\phi_{\rm mkt})\approx -0.006$, while the IC contract achieves $U_I(\sigma_d^*,\phi^*)\approx 0.001$, a welfare gain of $\Delta U_I\approx 0.007$. Notably, the investor's participation constraint ($U_I\ge 0$) is satisfied under the IC contract but violated under the flat-fee benchmark, because the manager's over-risking at $\sigma^{\rm free}\approx 19.1\%$ generates variance large enough to make the investor's mean-variance utility negative despite the high expected return. The right panel shows this welfare gain is decreasing in $f_2$: IC enforcement delivers the largest improvement over the flat-fee benchmark at moderate convexity, and the gain diminishes as $f_2$ increases because the IC fee must fall sharply to maintain incentive alignment. At sufficiently high convexity ($f_2\gtrsim 40$), the IC contract no longer improves on the flat-fee benchmark.

Beyond the baseline, Figures \ref{fig:comp-f2}--\ref{fig:comp-risk} illustrate how the equilibrium target $\sigma_d^*$ and the IC fee $\phi(\sigma_d^*)$ vary with the key parameters, computed at the Section \ref{sec:calibration} calibration baseline while sweeping each parameter over empirically plausible ranges (documented in Appendix \ref{app:numerical}). Figure \ref{fig:flow-performance} shows the flow-performance relationship. Figure \ref{fig:ic-fee-curve} shows the IC mapping: for each target volatility $\sigma_d$, there is a fee level that makes the manager willing to implement it; higher convexity shifts the schedule downward, reflecting the stronger incentive to over-risk when performance chasing is more pronounced. Figure \ref{fig:opt-sigma-vs-f2} shows that stronger convexity lowers the investor's optimal target, consistent with the comparative statics: sustaining a high target becomes more contractually costly when flows are more convex. Figures \ref{fig:comp-sharpe} and \ref{fig:comp-risk} illustrate that higher fund skill raises the optimal target while higher investor risk aversion lowers it, and that a more risk-averse manager requires a lower IC fee to implement any given target, since greater natural risk aversion reduces the need for contractual discipline.

Throughout these exercises, the manager's participation constraint $U_M(\sigma_d^*,\phi(\sigma_d^*)) \ge 0$ and the investor's participation constraint $U_I(\sigma_d^*,\phi^*) \ge 0$ (normalized to zero reservation utility) are both satisfied throughout the calibrated parameter ranges. Notably, the investor's constraint is violated under the flat-fee benchmark --- the manager's over-risking at $\sigma^{\rm free}\approx 19.1\%$ generates a variance penalty that makes the investor's mean-variance utility negative --- whereas the IC contract restores a non-negative utility. The limited-liability constraint $\phi^* \ge 0$ holds across all parameter sweeps in Appendix \ref{app:numerical}: the IC fee formula $\phi(\sigma_d) = 2\,\partial_\sigma \E[A] / (\eta\,\partial_\sigma \V[A])$ inherits the sign of $\partial_\sigma \E[A]$, which is strictly positive whenever $S > 0$ or $f_2 > 0$. This confirms that, under the calibration, the relevant binding constraint is incentive compatibility rather than participation.

A practical question concerns how the contract $\phi(\sigma_d)$ is implemented: the investor must specify a target volatility $\sigma_d$ and the manager must implement it. In practice, the realized volatility $\hat{\sigma}$ must be estimated from a time series of fund returns, introducing estimation error. Over a standard evaluation horizon (e.g., quarterly or annual), estimation noise is non-negligible. A natural implementation maps a window of realized returns to an estimated $\hat{\sigma}$, then sets the fee according to the affine rule $\phi \approx \alpha + \beta\hat{\sigma}$. Two complications arise. First, estimation error in $\hat{\sigma}$ may cause the contract to inadvertently reward or penalize the manager for luck in realized returns rather than the risk level chosen. Second, managers have an incentive to manage reported volatility through return smoothing or infrequent pricing of illiquid assets, as documented in \citet{GetmanskyLoMakarov2004} and \citet{BollenPool2009} for hedge funds. In equity mutual fund contexts, mark-to-market pricing and regulatory reporting requirements reduce but do not eliminate this concern. The practical solution is to evaluate the contract over sufficiently long horizons and to use realized volatility measures that are robust to smoothing, such as high-frequency range-based estimators. A full extension of the model to estimated volatility is beyond the scope of the present analysis but constitutes a natural direction for future work.

Taken together, these results highlight how the model translates observable features of investor behavior into implications for contract design. For both investors and managers, the incentive-compatible fee schedule and its affine approximation provide a transparent mapping from a volatility target to a corresponding fee level, sustaining incentive alignment under realistic market conditions.


# Conclusion {#sec:conclusion}

This paper develops a tractable principal--agent framework to study agency conflicts in delegated portfolio management. In the model, performance chasing generates an option-like payoff for managers, which tilts their incentives toward higher volatility relative to what investors would choose. The central contribution of the paper is to characterize how compensation contracts can be designed to implement a desired level of portfolio risk.

The main practical output is a fee schedule that implements a target volatility: for each risk target, there exists a management fee level such that the manager's first-order condition is satisfied at that target, making it a locally incentive-compatible equilibrium under the stated conditions (global uniqueness is verified numerically across the calibrated parameter grid). Rather than increasing volatility to benefit from convex flow dynamics, the manager chooses the investor's preferred target. We also show that a simple linear approximation to the exact incentive-compatible schedule is accurate over empirically relevant ranges, making the contract easy to communicate and implement as ``pay for risk, not luck.'' Finally, the numerical exercise illustrates how flow convexity, fund scale, managerial skill, and risk aversion shape the equilibrium risk target and the fee level required to align incentives.

A natural next step in this research is to incorporate run-like dynamics and risk of ruin: when redemptions become strategic and non-linear in bad states, the same incentive problem remains, but the manager's costs of excessive risk can become impossible to disregard as AUM falls in a concave fashion when losses are large.

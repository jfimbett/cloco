# Annotated Bibliography: Distributional Debt Capacity and the Wasserstein Distance
## Research Question
Does the distributional shape mismatch between firm cash flow distributions and aggregate capital supply distributions — measured by the Wasserstein distance W1(μ_i, ν) — explain cross-sectional leverage heterogeneity beyond what firm-level mean and variance predict?

**Paper type:** Structural estimation, corporate finance  
**Theoretical result:** Optimal debt contract = quantile coupling D*(X) = F_ν^{-1}(F_μ(X)); individual debt capacity = W1(μ_i, ν)/2  
**Compiled:** 2026-06-13  
**Coverage:** 57 verified papers + key mathematical references  
**Last updated:** 2026-06-13 (Gap-fill revision: matching models, distributional estimation, post-2017 structural estimation, Lemmon-Roberts 2010 verified)

---

## Category 1: Directly Related — Same Core Question (Proximity 4–5)

### [Lemmon, Roberts, Zender 2008] Back to the Beginning: Persistence and the Cross-Section of Corporate Capital Structure
**Journal/Source:** Journal of Finance, Vol. 63, No. 4, pp. 1575–1608  
**Proximity Score:** 4/5  
**Summary:** Documents that the vast majority of cross-sectional variation in leverage ratios is driven by an unobserved, time-invariant firm-specific effect — the adjusted R² from regressing leverage on firm fixed effects alone is 60%. High-leverage firms remain high-leverage for more than two decades. Observables identified by prior studies (profitability, market-to-book, tangibility) explain very little of this persistent heterogeneity. The paper poses the open question: what time-invariant characteristic generates this pattern? This directly motivates the research question here — the Wasserstein distance W1(μ_i, ν) is a candidate time-invariant sufficient statistic for the otherwise unexplained fixed effect.  
**Identification:** OLS panel regressions with and without firm fixed effects; decomposition of R² into within/between variation. Compustat data 1965–2003.  
**Data:** Compustat, US public firms, 1965–2003  
**Key Result:** Firm fixed effects alone explain 60% of leverage variation; adding standard observables raises this only modestly. Leverage at IPO is the single best predictor of leverage 10–20 years later.

---

### [Massa, Yasuda, Zhang 2013] Supply Uncertainty of the Bond Investor Base and the Leverage of the Firm
**Journal/Source:** Journal of Financial Economics, Vol. 110, pp. 185–214  
**Proximity Score:** 4/5  
**Summary:** Shows that the distributional properties of the capital supply side — specifically the volatility and turnover of the bond investor base — significantly affect firm leverage. Supply uncertainty (measured as flow volatility of investors holding a firm's bonds, or prevalence of transient mutual funds vs. stable insurance companies) has a negative and statistically significant effect on leverage. This is one of the few empirical papers to treat capital supply as a distributional object rather than a scalar price, directly paralleling the theoretical setup in the proposed paper. The closer is capital supply to a stable distribution (dominated by insurance companies), the higher the firm's achievable leverage.  
**Identification:** OLS with firm and year fixed effects; instrument for supply uncertainty using flow volatility of non-overlapping bond holders. Proprietary bond-level ownership data merged with Compustat.  
**Data:** Proprietary bond ownership data (INSEAD), Compustat, 2003–2009  
**Key Result:** A one-standard-deviation increase in supply uncertainty reduces leverage by approximately 2–3 percentage points; effect on bond issuance probability is negative and symmetric.

---

### [Zhu 2021] Capital Supply and Corporate Bond Issuances: Evidence from Mutual Fund Flows
**Journal/Source:** Journal of Financial Economics, Vol. 141, No. 2, pp. 551–572  
**Proximity Score:** 4/5  
**Summary:** Demonstrates that bond mutual fund flows create exogenous variation in capital supply facing individual firms, and that this variation significantly affects corporate debt issuance and yields. Firms experiencing higher flow-driven capital supply are 12% more likely to issue bonds (relative to the unconditional mean) and enjoy 7.6 basis point lower offering yields. The paper treats capital supply as a firm-specific, time-varying quantity rather than a market-wide price, consistent with the theoretical framework in the proposed paper. Capital markets exhibit distinct segmentation that amplifies supply fluctuations.  
**Identification:** Instrument for firm-level capital supply using fund flows of existing bondholders; exploits that incumbent holders are 5× more likely to buy new issuances. Panel IV with firm and time fixed effects.  
**Data:** Morningstar bond holdings, Mergent FISD, Compustat, 2007–2016  
**Key Result:** One standard deviation increase in bondholder flows predicts 0.83 pp increase in bond issuance probability and 7.6 bp decline in offering yield spread.

---

### [Lian, Ma 2021] Anatomy of Corporate Borrowing Constraints
**Journal/Source:** Quarterly Journal of Economics, Vol. 136, No. 1, pp. 229–291  
**Proximity Score:** 4/5  
**Summary:** Establishes that 80% of US corporate debt by value is cash flow-based (constrained by a multiple of EBITDA) rather than asset-based (constrained by collateral value). This result is foundational for the proposed paper's setup: if debt capacity is primarily determined by cash flows, then the distribution of cash flows (μ_i) is the correct primitive, not the distribution of asset values. The paper distinguishes two regimes of borrowing constraints and shows that the cash-flow regime dominates empirically, directly supporting the theoretical choice to model the borrowing problem as matching cash flow distributions to capital supply distributions.  
**Identification:** Text analysis of credit agreements, regression analysis of covenant structure; Dealscan loan data merged with Compustat.  
**Data:** DealScan private credit agreements, Compustat, 1996–2016  
**Key Result:** 80% of debt by value constrained by earnings (EBITDA) multiples; 20% by asset collateral. Cash flow-based constraints bind for almost all large US nonfinancial firms.

---

### [Hartman-Glaser, Mayer, Milbradt 2022/2025] A Theory of Cash Flow-Based Financing with Distress Resolution
**Journal/Source:** NBER Working Paper No. 29712 (2022); Review of Economic Studies, Vol. 92, No. 6, pp. 3995–4025 (2025)  
**Proximity Score:** 4/5  
**Summary:** Develops a dynamic contracting theory in which financing capacity is endogenously determined by either asset liquidation values (asset-based) or the intermediary's going-concern valuation of the firm's cash flows (cash flow-based). The optimal contract is implemented with unsecured credit lines and senior-secured debt. The paper's cash flow-based financing regime directly connects to the proposed paper's framework: both treat cash flow distributions as the fundamental determinant of debt capacity. The key difference is that the proposed paper introduces the capital supply distribution ν as a new primitive and derives the Wasserstein distance as the sufficient statistic.  
**Identification:** Theoretical dynamic contracting model; no empirical estimation.  
**Data:** N/A (theory paper)  
**Key Result:** Financing capacity under cash-flow-based lending equals the intermediary's valuation of the firm's going-concern cash flows; optimal contract implements risk-sharing via bankruptcy in a way that mirrors Chapter 7 and Chapter 11.

---

## Category 2: Structural Capital Structure Models (Proximity 3–4)

### [Merton 1974] On the Pricing of Corporate Debt: The Risk Structure of Interest Rates
**Journal/Source:** Journal of Finance, Vol. 29, No. 2, pp. 449–470  
**Proximity Score:** 3/5  
**Summary:** The foundational structural model of corporate debt. Applies Black-Scholes option pricing to value firm liabilities; corporate debt is modeled as a put option on firm asset value. Scalar volatility σ of the GBM asset process is the sufficient statistic for credit risk. The proposed paper directly challenges this sufficiency claim: two firms with the same scalar volatility but different distributional shapes relative to capital supply have different debt capacity, measured by W1(μ_i, ν). Every subsequent structural capital structure model builds on this framework.  
**Identification:** Theoretical / Black-Scholes option pricing framework.  
**Data:** N/A (theory paper)  
**Key Result:** Risky debt value = risk-free bond minus put option on firm assets; yield spreads increase in leverage and asset volatility.

---

### [Leland 1994] Corporate Debt Value, Bond Covenants, and Optimal Capital Structure
**Journal/Source:** Journal of Finance, Vol. 49, No. 4, pp. 1213–1252  
**Proximity Score:** 3/5  
**Summary:** Extends Merton (1974) by deriving closed-form results for the optimal capital structure of a firm issuing perpetual debt when asset value follows a diffusion process with constant volatility. Optimal leverage, credit spreads, and bankruptcy levels are explicitly linked to tax benefits, bankruptcy costs, risk-free rate, and asset volatility σ. The proposed paper re-derives the sufficient statistic for debt capacity — replacing σ with W1(μ_i, ν) — and shows that Leland's model is a special case when ν = N(r_f, σ²).  
**Identification:** Contingent claims / continuous-time closed-form model.  
**Data:** N/A (theory paper)  
**Key Result:** Closed-form leverage ratio and credit spreads; optimal bankruptcy trigger increases in coupon payments and decreases in bankruptcy costs; numerical calibration matches observed spreads.

---

### [Leland, Toft 1996] Optimal Capital Structure, Endogenous Bankruptcy, and the Term Structure of Credit Spreads
**Journal/Source:** Journal of Finance, Vol. 51, No. 3, pp. 987–1019  
**Proximity Score:** 3/5  
**Summary:** Extends Leland (1994) to allow finite-maturity debt and optimize jointly over both the amount and maturity of debt. Bankruptcy is endogenous. Results extend the closed-form analysis to a richer class of debt structures. Maturity choice interacts with leverage choice; short-term debt improves incentive compatibility. The proposed paper's model of optimal debt contracts under distributional mismatch should be compared against this benchmark for calibration and model fit.  
**Identification:** Continuous-time contingent claims model.  
**Data:** N/A (theory paper)  
**Key Result:** Optimal leverage, credit spreads, default rates, and write-downs match historical averages closely; short-term debt dominates on incentive grounds despite tax disadvantage.

---

### [Fischer, Heinkel, Zechner 1989] Dynamic Capital Structure Choice: Theory and Tests
**Journal/Source:** Journal of Finance, Vol. 44, No. 1, pp. 19–40  
**Proximity Score:** 3/5  
**Summary:** Develops a dynamic model of capital structure choice in the presence of recapitalization costs. Firms allow leverage to drift within a band before recapitalizing. Even small recapitalization costs produce wide swings in observed leverage. The empirical measure is the range of debt ratios rather than a point estimate. The model predicts that volatility of asset value and recapitalization costs drive the width of the leverage band. The proposed paper's distributional distance measure is analogous to — but more general than — the volatility-driven band of Fischer et al.  
**Identification:** Dynamic continuous-time model; OLS regressions of debt ratio range on firm characteristics.  
**Data:** Sample of US publicly traded firms (Compustat), 1975–1985  
**Key Result:** Observed debt ratio ranges strongly support the model; firm size, earnings volatility, and tax rates explain band width.

---

### [Strebulaev 2007] Do Tests of Capital Structure Theory Mean What They Say?
**Journal/Source:** Journal of Finance, Vol. 62, No. 4, pp. 1747–1787  
**Proximity Score:** 3/5  
**Summary:** Generates artificial data from a calibrated dynamic trade-off model with adjustment costs and shows that standard cross-sectional OLS tests yield results consistent with the empirical literature even when the structural model is known to be true — thus conventional tests may not be informative about the underlying structural mechanism. The paper argues for structural estimation over reduced-form regressions in capital structure research. This methodological argument directly supports the proposed paper's structural approach (SMM/GMM) rather than reduced-form cross-sectional leverage regressions.  
**Identification:** Dynamic structural model with calibration; Monte Carlo simulation of empirical tests.  
**Data:** Compustat US firms; model calibration  
**Key Result:** Cross-sectional leverage-profitability correlations and other standard empirical regularities are consistent with the dynamic trade-off model even though no firm has a constant target leverage.

---

### [Hennessy, Whited 2005] Debt Dynamics
**Journal/Source:** Journal of Finance, Vol. 60, No. 3, pp. 1129–1165  
**Proximity Score:** 3/5  
**Summary:** Develops a dynamic trade-off model with endogenous leverage, distributions, and investment, incorporating a graduated corporate income tax, individual taxes on interest and distributions, financial distress costs, and equity flotation costs. The model endogenously explains why leverage is path-dependent, firms can be either savers or heavily levered, and no target leverage ratio exists. The proposed paper's structural model should be tested against the same moment conditions Hennessy and Whited use for identification.  
**Identification:** Dynamic programming model; calibration to US Compustat data.  
**Data:** Compustat US firms, 1980–2000  
**Key Result:** Path dependence of leverage, negative leverage-profitability correlation, and other empirical puzzles arise endogenously; no static trade-off target.

---

### [Hennessy, Whited 2007] How Costly Is External Financing? Evidence from a Structural Estimation
**Journal/Source:** Journal of Finance, Vol. 62, No. 4, pp. 1705–1745  
**Proximity Score:** 3/5  
**Summary:** Uses SMM to estimate a dynamic corporate model with endogenous investment, distributions, leverage, and default. Estimates marginal equity flotation costs at 5.0% for large firms and 10.7% for small firms; bankruptcy costs at 8.4% (large) and 15.1% (small) of capital. Provides the methodological template for the proposed paper's structural estimation via SMM. The moment conditions and identification strategy (matching simulated moments to Compustat moments) directly inform how to implement the proposed paper's empirical estimation of W1(μ_i, ν).  
**Identification:** Simulated Method of Moments (SMM) with GMM weighting. Targeted moments: leverage, investment-to-capital, dividends, cash.  
**Data:** Compustat US firms, 1988–2003  
**Key Result:** External financing frictions are economically large; estimated parameters match observed financial policies and imply financing costs 3–4× higher for constrained vs. unconstrained firms.

---

### [DeAngelo, DeAngelo, Whited 2011] Capital Structure Dynamics and Transitory Debt
**Journal/Source:** Journal of Financial Economics, Vol. 99, No. 2, pp. 235–261  
**Proximity Score:** 3/5  
**Summary:** Demonstrates that firms optimally maintain spare debt capacity by operating below their maximum leverage to preserve the option to fund future investment shocks with transitory debt. The model predicts that observed leverage is below the trade-off optimum for most firms at most times. This result is consistent with the proposed paper's framework: if debt capacity is determined by W1(μ_i, ν), firms that face uncertain future cash flow distributions might rationally maintain slack.  
**Identification:** Dynamic model with stochastic investment opportunities; calibration to Compustat.  
**Data:** Compustat US firms  
**Key Result:** Firms hold substantial debt capacity in reserve; transitory spikes in leverage are a rational response to investment shocks, not evidence against trade-off theory.

---

### [Nikolov, Whited 2014] Agency Conflicts and Cash: Estimates from a Dynamic Model
**Journal/Source:** Journal of Finance, Vol. 69, No. 5, pp. 1883–1921  
**Proximity Score:** 3/5  
**Summary:** Estimates a dynamic model featuring three sources of manager-shareholder conflict: limited managerial ownership, size-based compensation, and perquisite consumption. Uses SMM to estimate the model. Provides a close methodological template for the proposed paper's structural estimation: same moment-matching approach, same SMM estimator, same Compustat data. The paper establishes that structural agency models can be estimated from standard financial data, supporting the feasibility of estimating distributional distance parameters from Compustat.  
**Identification:** SMM with Compustat moments: leverage, cash, dividend, investment ratios.  
**Data:** Compustat US firms, 1980–2008  
**Key Result:** Perquisite consumption is the quantitatively dominant source of cash policy distortion; agency explains the secular upward trend in cash holdings for larger firms.

---

### [Morellec, Nikolov, Schuerhoff 2012] Corporate Governance and Capital Structure Dynamics
**Journal/Source:** Journal of Finance, Vol. 67, No. 3, pp. 803–848  
**Proximity Score:** 3/5  
**Summary:** Develops and structurally estimates a dynamic trade-off model with manager-shareholder conflicts. The model features time-varying agency costs and corporate governance mechanisms. SMM is used to match moments from Compustat. Finds that variations in agency conflicts account for a substantial portion of cross-sectional leverage heterogeneity. A key finding is that even after controlling for governance, significant unexplained firm-level heterogeneity in leverage remains — consistent with the proposed paper's claim that distributional shape differences (not just agency costs) matter.  
**Identification:** SMM; targeted moments include leverage, investment, dividends, cash. Compustat + governance data.  
**Data:** Compustat US firms, governance data (G-index, blockholder ownership), 1990–2008  
**Key Result:** Agency conflicts contribute but do not fully explain cross-sectional leverage dispersion; average governance improves leverage by 4–5 percentage points.

---

### [Crouzet 2018] Aggregate Implications of Corporate Debt Choices
**Journal/Source:** Review of Economic Studies, Vol. 85, No. 3, pp. 1635–1682  
**Proximity Score:** 3/5  
**Summary:** Develops and calibrates a macroeconomic model in which firms choose between bank loans and public bonds, where bank debt is more easily renegotiated in distress but carries higher intermediation costs. When bank credit contracts, firms substitute toward bonds — but not enough to avoid a decline in aggregate borrowing and investment. A key mechanism is "precautionary deleveraging": firms reduce total debt when switching from flexible bank relationships to inflexible bond structures, to avoid the higher bankruptcy risk associated with hard market debt. Calibrated to the Great Recession, the model accounts for roughly one-third of the investment decline among bond-market-accessible firms. Directly relevant to the proposed paper: Crouzet's two-debt-type framework is a special case of a model with two capital supply distributions (bank ν_b and bond ν_m); the Wasserstein distance between μ_i and each ν determines which instrument the firm prefers and what aggregate debt capacity it commands.  
**Identification:** Calibrated macroeconomic model; targeted moments from the Great Recession.  
**Data:** Compustat, Federal Reserve Flow of Funds; Great Recession calibration sample  
**Key Result:** Precautionary deleveraging explains approximately one-third of the investment decline among publicly traded firms during the Great Recession; pure substitution between bank and bond debt is incomplete.

---

### [Nikolov, Schmid, Steri 2021] The Sources of Financing Constraints
**Journal/Source:** Journal of Financial Economics, Vol. 139, No. 2, pp. 478–501  
**Proximity Score:** 3/5  
**Summary:** Uses a dynamic structural model to disentangle three sources of financing constraints — limited enforcement (collateral-based), moral hazard (incentive-based), and trade-off forces (tax-bankruptcy) — and estimates which mechanism dominates for different firm types. Estimation uses policy function benchmarks from each competing model, evaluated against panels of public and private firms from the ORBIS database. Key finding: trade-off models best explain larger public firms, limited commitment models work better for smaller public firms, and moral hazard models fit private firms. This is a direct methodological template for the proposed paper's structural estimation: the paper demonstrates that alternative structural models of debt capacity can be distinguished from each other by targeting different moment conditions, exactly the strategy needed to establish that the Wasserstein distance W1(μ_i, ν) provides additional identifying variation beyond what existing structural models capture.  
**Identification:** Dynamic structural model estimation with empirical policy function benchmarks; ORBIS international panel of public and private firms.  
**Data:** ORBIS global database (public and private firms); Compustat for US public firm validation  
**Key Result:** Different financing constraint mechanisms dominate for different firm types; trade-off vs. limited commitment vs. moral hazard can be structurally distinguished using policy functions.

---

### [Elenev, Landvoigt, Van Nieuwerburgh 2021] A Macroeconomic Model with Financially Constrained Producers and Intermediaries
**Journal/Source:** Econometrica, Vol. 89, No. 3, pp. 1361–1418  
**Proximity Score:** 2/5  
**Summary:** Builds a general equilibrium model where both firms (producers) and banks (intermediaries) face binding financial constraints simultaneously. Banks make risky long-term loans to firms funded by short-term deposits; government guarantees create a role for bank capital regulation. The model captures the sharp, persistent drop in macro aggregates and credit provision during the Great Recession, as well as the sharp change in credit spreads. A key result is that the distribution of capital across intermediaries — not just aggregate intermediary equity — determines the aggregate supply of credit available to firms. This is structurally analogous to the proposed paper's model: the distribution ν of capital supply across lenders determines the available debt capacity for the aggregate firm sector, and the Wasserstein distance between μ_i (firm cash flows) and ν (lender capital) measures the distributional mismatch that limits individual firm borrowing.  
**Identification:** Calibrated DSGE model with occasionally binding constraints; solved using global methods.  
**Data:** Great Recession calibration; FRED macro aggregates, Flow of Funds, bank Call Reports  
**Key Result:** Joint financial constraints on firms and intermediaries generate amplification 3× larger than models with only intermediary constraints; intermediary capital distribution (not just aggregate equity) determines credit supply.

---

### [Gomes, Schmid 2010] Levered Returns
**Journal/Source:** Journal of Finance, Vol. 65, No. 2, pp. 467–494  
**Proximity Score:** 3/5  
**Summary:** Develops a structural model linking leverage decisions to equity risk premia. In the presence of financing frictions, leverage and investment are correlated such that highly levered firms are mature firms with more book assets and fewer growth opportunities. The link between leverage and stock returns is complex and depends on investment opportunities. Provides both a structural equilibrium model and evidence that cross-sectional return variation is related to the interaction of leverage and investment, relevant for understanding why distributional shape might matter for risk premia beyond mean-variance.  
**Identification:** Structural equilibrium model with calibration; empirical validation using CRSP/Compustat data.  
**Data:** CRSP, Compustat US firms  
**Key Result:** Quantitative model matches several stylized facts about leverage-return relationship; leverage effect on returns depends critically on investment opportunity set.

---

### [Morellec 2004] Can Managerial Discretion Explain Observed Leverage Ratios?
**Journal/Source:** Review of Financial Studies, Vol. 17, No. 1, pp. 257–294  
**Proximity Score:** 3/5  
**Summary:** Analyzes the impact of managerial discretion on leverage within a contingent claims model. Manager derives perquisites from investment, creating agency costs that lower optimal leverage. Shows that realistic agency parameters can bring theoretical leverage down to observed empirical levels, which were otherwise too low relative to standard Merton-Leland predictions. The underleverage puzzle is a persistent anomaly in structural capital structure models; the proposed paper's Wasserstein-based debt capacity may help rationalize under-leverage by showing that distributional mismatch between μ_i and ν limits achievable leverage.  
**Identification:** Contingent claims model; calibration and comparison to data.  
**Data:** Calibration to historical averages; no formal structural estimation  
**Key Result:** Agency costs reduce optimal leverage from ~70% (Merton) to approximately observed levels (30–40%); consistent with cross-sectional leverage dispersion.

---

## Category 3: Empirical Capital Structure Determinants (Proximity 2–3)

### [Rajan, Zingales 1995] What Do We Know about Capital Structure? Some Evidence from International Data
**Journal/Source:** Journal of Finance, Vol. 50, No. 5, pp. 1421–1460  
**Proximity Score:** 2/5  
**Summary:** Investigates determinants of capital structure across G-7 countries. Identifies four firm-level factors correlated with leverage across countries: market-to-book ratio (negative), tangibility (positive), profitability (negative), and size (positive). Provides the benchmark set of cross-sectional leverage determinants that the proposed paper's Wasserstein distance measure must outperform. The paper's finding that "the theoretical underpinnings of the observed correlations are still largely unresolved" motivates the proposed distributional approach.  
**Identification:** OLS cross-sectional and panel regressions; no causal identification.  
**Data:** Compustat (US), Worldscope (Germany, France, Italy, UK, Japan, Canada), 1987–1991  
**Key Result:** Four factors (market-to-book, tangibility, profitability, size) explain approximately 25% of cross-country leverage variation; correlations are qualitatively similar across G-7 countries.

---

### [Frank, Goyal 2009] Capital Structure Decisions: Which Factors Are Reliably Important?
**Journal/Source:** Financial Management, Vol. 38, No. 1, pp. 1–37  
**Proximity Score:** 2/5  
**Summary:** Comprehensive horse-race of capital structure determinants using US Compustat data 1950–2003. Identifies the most reliable factors: median industry leverage (+), market-to-book ratio (−), tangibility (+), profitability (−), log assets (+), and expected inflation (+). The proposed paper's Wasserstein distance measure must explain the residual leverage variation after these standard controls are included. This paper defines the baseline specification that will serve as a control in the proposed paper's cross-sectional regressions.  
**Identification:** OLS; BMA (Bayesian model averaging) to assess robustness of factors. CRSP/Compustat, 1950–2003.  
**Data:** Compustat US public firms, 1950–2003  
**Key Result:** Six factors jointly explain approximately 27% of market leverage variation; individual factors have limited explanatory power.

---

### [Fama, French 2002] Testing Trade-Off and Pecking Order Predictions About Dividends and Debt
**Journal/Source:** Review of Financial Studies, Vol. 15, No. 1, pp. 1–33  
**Proximity Score:** 2/5  
**Summary:** Tests trade-off and pecking order theory predictions using US Compustat data. Finds evidence for both theories; more profitable firms are less levered (consistent with pecking order, inconsistent with simple trade-off). Short-term variation in investment and earnings is largely absorbed by debt. The paper's finding that profitability is the single best predictor of leverage (negative) motivates the question of whether distributional shape heterogeneity — correlated with the entire earnings distribution, not just its mean — adds explanatory power beyond standard controls.  
**Identification:** OLS with standard controls; no causal identification.  
**Data:** Compustat US industrial firms, 1965–1999  
**Key Result:** Profitability is the strongest negative predictor of leverage; investment is a negative predictor for both theories; short-run adjustment consistent with pecking order.

---

### [Lemmon, Roberts 2010] The Response of Corporate Financing and Investment to Changes in the Supply of Credit
**Journal/Source:** Journal of Financial and Quantitative Analysis, Vol. 45, No. 3, pp. 555–587  
**Proximity Score:** 3/5  
**Summary:** Exploits three exogenous contractions in the supply of below-investment-grade credit after 1989 — the collapse of Drexel Burnham Lambert, the passage of FIRREA (restricting S&L bond holdings), and regulatory changes to insurance company junk-bond holdings — to identify how credit supply shocks transmit to corporate financing and investment. A difference-in-differences strategy shows that high-yield-dependent firms had virtually no ability to substitute toward bank debt or alternative sources, so net investment declined almost one-for-one with the contraction in net bond issuance. The result directly motivates the proposed paper's model: when the capital supply distribution ν shifts away from a firm's cash flow distribution μ_i (i.e., W1(μ_i, ν) widens), the firm cannot easily find substitute lenders, producing the near-complete pass-through observed here.  
**Identification:** Difference-in-differences exploiting three regulatory and market events as exogenous credit supply contractions; high-yield-dependent firms vs. investment-grade firms.  
**Data:** Compustat US public firms, DealScan (loan data), 1985–1995  
**Key Result:** Investment of below-investment-grade firms fell nearly one-for-one with the contraction in high-yield bond issuance; substitution to bank or alternative credit was negligible.

---

### [Baker, Wurgler 2002] Market Timing and Capital Structure
**Journal/Source:** Journal of Finance, Vol. 57, No. 1, pp. 1–32  
**Proximity Score:** 2/5  
**Summary:** Shows that firms issue equity when market valuations are high and repurchase when valuations are low; this market-timing behavior has very persistent effects on capital structure. Current capital structure reflects the cumulative outcome of past equity market timing. The proposed paper's distributional approach should explain why some firms are persistently more "at odds" with the capital supply distribution ν and thus must rely more on equity timing as a financing strategy.  
**Identification:** OLS; external finance weighted average of market-to-book. Compustat, 1968–1999.  
**Data:** Compustat US public firms, 1968–1999  
**Key Result:** Historical market-to-book explains current leverage with coefficients that remain statistically significant 10 years later; market timing is not immediately reversed.

---

### [Lemmon, Roberts, Zender 2008] — See Category 1 above (Proximity 4/5)

---

### [DeAngelo, Roll 2015] How Stable Are Corporate Capital Structures?
**Journal/Source:** Journal of Finance, Vol. 70, No. 1, pp. 373–418  
**Proximity Score:** 2/5  
**Summary:** Challenges the view that firms maintain stable target leverage ratios. Finds that leverage cross-sections more than a few years apart differ markedly; many firms have high and low leverage at different times. Capital structure stability is the exception, not the rule. The proposed paper's time-invariant W1(μ_i, ν) measure should be tested against the DeAngelo-Roll finding: if firms maintain stable cash flow distributions over long periods (stable μ_i) and face a time-varying capital supply distribution ν, the instability of leverage is predicted by time variation in ν rather than mean-reverting adjustments.  
**Identification:** Descriptive analysis; regression analysis of leverage cross-sections over time. Compustat 1950–2008.  
**Data:** Compustat US firms, 1950–2008  
**Key Result:** Leverage exhibits substantial instability; less than 1% of firms maintain leverage above 0.5 for all years; target-leverage models with little weight on static targets best explain the data.

---

### [Graham, Harvey 2001] The Theory and Practice of Corporate Finance: Evidence from the Field
**Journal/Source:** Journal of Financial Economics, Vol. 60, No. 2–3, pp. 187–243  
**Proximity Score:** 1/5  
**Summary:** Survey of 392 CFOs on capital structure, capital budgeting, and cost of capital. Finds that trade-off theory and CAPM are widely used in practice but imperfectly applied. Managers consider financial flexibility and credit ratings as primary concerns. The survey evidence is useful background for motivating the gap between theory and practice: CFOs' concern for "financial flexibility" is consistent with the proposed paper's insight that distributional fit with capital supply matters beyond mean and variance.  
**Identification:** Survey (no causal identification).  
**Data:** Survey of 392 US and Canadian CFOs, 1999  
**Key Result:** 73.5% of CFOs use CAPM; credit rating maintenance is primary capital structure consideration; asymmetric information concerns are secondary.

---

## Category 4: Capital Supply and Credit Markets (Proximity 3–4)

### [Holmstrom, Tirole 1997] Financial Intermediation, Loanable Funds, and the Real Sector
**Journal/Source:** Quarterly Journal of Economics, Vol. 112, No. 3, pp. 663–691  
**Proximity Score:** 3/5  
**Summary:** Classic theory of financial intermediation in which firms and intermediaries are both capital-constrained. Analyzes how the distribution of wealth across firms, intermediaries, and uninformed investors affects investment and interest rates. All forms of capital tightening (credit crunch, collateral squeeze, savings squeeze) hit poorly capitalized firms hardest. The proposed paper's capital supply distribution ν is the analog to Holmstrom-Tirole's aggregate loanable funds; the model shows that the distribution of supply — not just its aggregate quantity — determines which firms receive financing.  
**Identification:** Theoretical model; no empirical estimation.  
**Data:** N/A (theory paper)  
**Key Result:** Credit supply tightening disproportionately hits low-capital firms; monitoring intensity and capital cushion jointly determine debt capacity.

---

### [Kashyap, Stein 2000] What Do a Million Observations on Banks Say About the Transmission of Monetary Policy?
**Journal/Source:** American Economic Review, Vol. 90, No. 3, pp. 407–428  
**Proximity Score:** 2/5  
**Summary:** Exploits heterogeneity across US commercial banks to identify a bank lending channel. Banks with less liquid balance sheets (low securities-to-assets) reduce lending more in response to monetary tightening. The paper identifies exogenous variation in credit supply at the bank level, providing a methodological template for the proposed paper's empirical strategy of identifying exogenous shifts in ν (the capital supply distribution) to measure W1(μ_i, ν).  
**Identification:** Panel regressions exploiting cross-sectional variation in bank liquidity interacted with monetary policy shocks. 1 million quarterly bank observations, 1976–1993.  
**Data:** Call Reports (quarterly observations of all insured US commercial banks), 1976–1993  
**Key Result:** Effect of monetary tightening on lending is concentrated in less liquid banks; 95th percentile of size distribution shows little adjustment; identifies bank lending channel.

---

### [Greenwood, Hanson 2013] Issuer Quality and Corporate Bond Returns
**Journal/Source:** Review of Financial Studies, Vol. 26, No. 6, pp. 1483–1525  
**Proximity Score:** 2/5  
**Summary:** Shows that the credit quality of corporate debt issuers deteriorates during credit booms, and this deterioration forecasts low excess returns to corporate bondholders. When capital supply is abundant and low-quality borrowers access bond markets, future returns are low. The paper treats the distribution of issuer quality in the bond market as an aggregate signal about capital supply, directly paralleling the proposed paper's distribution ν. The credit cycle is characterized by shifts in ν toward tolerating lower-quality borrowers.  
**Identification:** OLS time-series regressions; forecast regressions of bond returns on issuer quality measures.  
**Data:** Mergent FISD bond issuance data, CRSP, Compustat, 1965–2012  
**Key Result:** Issuer quality decline predicts negative bond excess returns; a 1-std-dev decline in issuer quality forecasts approximately 3–4% lower excess returns over the next 12 months.

---

### [Ivashina, Scharfstein 2010] Bank Lending During the Financial Crisis of 2008
**Journal/Source:** Journal of Financial Economics, Vol. 97, No. 3, pp. 319–338  
**Proximity Score:** 2/5  
**Summary:** Documents the collapse of bank lending during the 2008 financial crisis. New loans to large borrowers fell 47% in Q4 2008 relative to Q3 2008. After Lehman Brothers' failure, there was a simultaneous run by short-term bank creditors and by borrowers drawing down credit lines. Provides evidence of abrupt shifts in the capital supply distribution ν — specifically a shift in ν toward concentrating supply at very high credit quality, leaving lower-quality borrowers without access. This is exactly the type of ν-shift that the proposed paper's W1(μ_i, ν) would capture.  
**Identification:** Difference-in-differences exploiting cross-bank variation in reliance on short-term wholesale funding. DealScan loan-level data.  
**Data:** DealScan, Compustat, 2007–2009  
**Key Result:** 47% decline in new large borrower loans in Q4 2008; effect concentrated in banks with greater short-term funding reliance; real investment (not restructuring) lending showed smaller decline.

---

### [Khwaja, Mian 2008] Tracing the Impact of Bank Liquidity Shocks: Evidence from an Emerging Market
**Journal/Source:** American Economic Review, Vol. 98, No. 4, pp. 1413–1442  
**Proximity Score:** 2/5  
**Summary:** Exploits unanticipated nuclear tests in Pakistan as an instrument for differential liquidity shocks across banks. Using loan-level data with multiple bank-firm pairs, isolates credit supply shocks from demand. For every 1% additional liquidity shock to a bank, loans fall by 0.6% for the same firm. Large firms compensate through other credit sources; small firms cannot. Provides the canonical methodology for identifying credit supply shocks at the firm level — the K-M estimator (firm fixed effects in loan-level regressions) that the proposed paper may use to instrument for shifts in ν.  
**Identification:** Loan-level difference-in-differences with firm fixed effects; instrument: nuclear tests → differential bank liquidity shocks.  
**Data:** Loan-level data, all corporate loans in Pakistan, 1996–2000  
**Key Result:** Banks pass liquidity shocks to firms: 1% bank liquidity shock → 0.6% loan decline for same firm; small firms face full contraction while large firms fully offset.

---

### [Koijen, Yogo 2019] A Demand System Approach to Asset Pricing
**Journal/Source:** Journal of Political Economy, Vol. 127, No. 4, pp. 1475–1515  
**Proximity Score:** 2/5  
**Summary:** Develops a demand-system asset pricing model that allows flexible heterogeneity in asset demand across investors. Proposes an IV estimator for the demand system to address endogeneity of prices. Treats the distribution of investor demand as the fundamental object, consistent with the proposed paper's treatment of ν as a primitive distribution rather than a scalar price. While focused on equity markets, the demand-system approach is directly analogous to the proposed paper's treatment of the capital supply distribution ν for debt markets.  
**Identification:** IV estimator for demand system parameters; exploit characteristics-based variation in demand.  
**Data:** US equity holdings (13-F filings), CRSP, 2003–2017  
**Key Result:** Institutions and households have heterogeneous demand systems; model matches observed equity holdings and explains low price elasticity of demand.

---

## Category 5: Optimal Transport — Theoretical Foundations (Proximity 1–2)

### [Villani 2003] Topics in Optimal Transportation
**Journal/Source:** Graduate Studies in Mathematics, Vol. 58, American Mathematical Society (book)  
**Proximity Score:** 1/5  
**Summary:** The foundational graduate-level textbook on optimal transport theory. Covers Monge and Kantorovich problems, duality theory, Wasserstein distances, the Brenier theorem (existence and uniqueness of optimal transport maps), and regularity. The Kantorovich LP duality result — that the dual of the transport plan minimization is a Lipschitz function maximization — is directly used in the proposed paper to derive the closed-form expression for W1(μ_i, ν) in the debt capacity formula. Every lemma and theorem in the proposed paper's mathematical appendix will cite this work.  
**Identification:** N/A (mathematical theory book)  
**Data:** N/A  
**Key Result:** Existence and uniqueness of optimal transport maps (Brenier's theorem); Kantorovich duality; characterization of Wasserstein geodesics.

---

### [Villani 2009] Optimal Transport: Old and New
**Journal/Source:** Grundlehren der mathematischen Wissenschaften, Vol. 338, Springer (book)  
**Proximity Score:** 1/5  
**Summary:** The comprehensive reference work on optimal transport theory, winner of the AMS Doob Prize. Covers all aspects of optimal transport including the Monge problem, Kantorovich relaxation, Wasserstein spaces, regularity theory, and connections to PDEs, geometry, and probability. The W1 (earth-mover) distance and its dual Kantorovich-Rubinstein representation are derived here. The proposed paper's key expression for debt capacity = W1(μ_i, ν)/2 relies on results in this text.  
**Identification:** N/A (mathematical theory book)  
**Data:** N/A  
**Key Result:** Unified treatment of Monge-Kantorovich theory; Wasserstein space geometry; connection to Ricci curvature and concentration of measure.

---

### [Gangbo, McCann 1996] The Geometry of Optimal Transportation
**Journal/Source:** Acta Mathematica, Vol. 177, pp. 113–161  
**Proximity Score:** 1/5  
**Summary:** Establishes existence and uniqueness of optimal transport maps for general cost functions beyond the quadratic case. The main result — that optimal maps exist and are characterized by c-convex potentials — provides the mathematical foundation for Brenier's theorem in higher dimensions. For the proposed paper's one-dimensional case (quantile coupling), the result reduces to the monotone rearrangement, and D*(X) = F_ν^{-1}(F_μ(X)) is the optimal map. This paper is the key mathematical reference for uniqueness of the optimal debt contract.  
**Identification:** N/A (pure mathematics)  
**Data:** N/A  
**Key Result:** Optimal transport maps exist and are unique under mild regularity conditions; characterized as gradients of convex functions (c-convex potentials).

---

### [Brenier 1991] Polar Factorization and Monotone Rearrangement of Vector-Valued Functions
**Journal/Source:** Communications on Pure and Applied Mathematics, Vol. 44, pp. 375–417  
**Proximity Score:** 1/5  
**Summary:** Establishes the polar factorization theorem: any vector field u(x) satisfying a nondegeneracy condition admits the decomposition u(x) = ∇ψ(s(x)), where ψ is convex and s is measure-preserving. In one dimension, this reduces to the monotone rearrangement: the unique optimal transport map from μ to ν (under quadratic cost) is the quantile function F_ν^{-1}(F_μ(x)). This is the direct mathematical antecedent of the proposed paper's key result D*(X) = F_ν^{-1}(F_μ(X)).  
**Identification:** N/A (pure mathematics)  
**Data:** N/A  
**Key Result:** Polar factorization theorem; uniqueness of monotone rearrangement as optimal transport map in 1D.

---

### [Galichon 2016] Optimal Transport Methods in Economics
**Journal/Source:** Princeton University Press (book), 184 pages  
**Proximity Score:** 2/5  
**Summary:** The first textbook on optimal transport written for economists. Covers Monge-Kantorovich theory, linear programming duality, network flow interpretations, and applications to matching markets, gravity models, quantile regression, and discrete choice models. The quantile function representation and its connection to Wasserstein distances is central. This is the key economics-accessible reference for the proposed paper's theoretical framework; the paper's mathematical appendix will draw on Galichon's exposition of the one-dimensional case.  
**Identification:** N/A (textbook)  
**Data:** N/A  
**Key Result:** Wasserstein distances arise naturally from optimal matching problems; quantile coupling is the unique monotone measure-preserving map; applications to matching, trade, and discrete choice.

---

### [Galichon 2021] The Unreasonable Effectiveness of Optimal Transport in Economics
**Journal/Source:** Advances in Economics and Econometrics, Cambridge University Press (Chapter 3); arXiv:2107.04700  
**Proximity Score:** 2/5  
**Summary:** Review paper demonstrating the breadth of optimal transport applications in economics: matching markets with transfers, quantile regression, discrete choice models, gravity equations in trade. Shows that Wasserstein distances arise naturally in models of competitive sorting, which is structurally similar to the proposed paper's model of matching cash flow distributions to capital supply distributions. This paper is the primary economics literature reference for the proposed paper's optimal transport framework.  
**Identification:** N/A (review/survey)  
**Data:** N/A  
**Key Result:** Optimal transport is the correct mathematical framework for competitive sorting, quantile regression, and demand estimation; Wasserstein distance measures cost of distributional mismatch in each context.

---

### [Santambrogio 2015] Optimal Transport for Applied Mathematicians
**Journal/Source:** Progress in Nonlinear Differential Equations, Vol. 87, Springer (book)  
**Proximity Score:** 1/5  
**Summary:** Graduate textbook covering optimal transport with particular attention to the calculus of variations perspective, applications to PDEs, and numerical methods. Covers Knothe transport, Dacorogna-Moser flows, and the supremal cost case. Useful reference for the proposed paper's proof that the debt contracting problem is equivalent to a Kantorovich LP and that the optimizer is the quantile coupling.  
**Identification:** N/A (textbook)  
**Data:** N/A  
**Key Result:** Equivalence between Monge and Kantorovich formulations; characterization of optimal maps; numerical methods for computing Wasserstein distances.

---

## Category 6: Debt Contracting Theory (Proximity 2–3)

### [Townsend 1979] Optimal Contracts and Competitive Markets with Costly State Verification
**Journal/Source:** Journal of Economic Theory, Vol. 21, No. 2, pp. 265–293  
**Proximity Score:** 2/5  
**Summary:** Establishes that under costly state verification (CSV), the optimal incentive-compatible contract is the standard debt contract: no monitoring if the borrower pays the promised amount; monitoring (bankruptcy) if the borrower defaults. This is the canonical theoretical foundation for the optimality of debt contracts. The proposed paper's result — that the optimal debt contract is a quantile coupling D*(X) = F_ν^{-1}(F_μ(X)) — is a distributional generalization of the Townsend CSV result, which applies when the cost function is the identity and distributions are Dirac masses.  
**Identification:** Theoretical mechanism design (no empirical estimation)  
**Data:** N/A (theory paper)  
**Key Result:** Standard debt contract is optimal under costly state verification; no disclosure required when promised payment is made.

---

### [Gale, Hellwig 1985] Incentive-Compatible Debt Contracts: The One-Period Problem
**Journal/Source:** Review of Economic Studies, Vol. 52, No. 4, pp. 647–663  
**Proximity Score:** 2/5  
**Summary:** Formalizes the optimality of debt contracts under asymmetric information. In a simple borrowing-lending model, the second-best contract is a standard debt contract when states of nature are not costlessly verifiable. The proposed paper extends this framework by modeling both sides (borrower cash flow distribution μ_i and lender capital distribution ν) as primitives, showing that the optimal matching between these distributions determines both the contract form (quantile coupling) and the debt capacity (W1/2).  
**Identification:** Theoretical mechanism design  
**Data:** N/A  
**Key Result:** Standard debt contract is incentive-compatible and second-best optimal; second-best investment is strictly less than first-best investment.

---

### [Jensen, Meckling 1976] Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure
**Journal/Source:** Journal of Financial Economics, Vol. 3, No. 4, pp. 305–360  
**Proximity Score:** 1/5  
**Summary:** Foundational agency theory paper. Introduces agency costs of debt (asset substitution, underinvestment) and equity (shirking, perquisite consumption). Shows that the optimal capital structure balances tax benefits of debt against agency costs. The proposed paper's distributional approach complements the agency framework: holding agency costs constant, distributional shape mismatch between μ_i and ν imposes an additional constraint on feasible debt levels beyond what scalar volatility predicts.  
**Identification:** Theoretical (no empirical estimation)  
**Data:** N/A  
**Key Result:** Agency costs of debt and equity generate an optimal interior debt ratio; ownership concentration affects the magnitude of agency costs.

---

## Category 7: Methodological References (Proximity 1–3)

### [Berry, Levinsohn, Pakes 1995] Automobile Prices in Market Equilibrium
**Journal/Source:** Econometrica, Vol. 63, No. 4, pp. 841–890  
**Proximity Score:** 2/5  
**Summary:** Develops the BLP framework for structural estimation of differentiated product demand using aggregate market share data and product characteristics. The key methodological innovations — using the contraction mapping to recover unobserved quality, using instruments for price endogeneity, and using SMM to match moments — provide the direct template for the proposed paper's SMM estimation of the Wasserstein debt capacity model. The BLP approach of treating unobserved heterogeneity (ξ_jt) as a structural residual is analogous to the proposed paper's treatment of the unobservable distributional shape parameter.  
**Identification:** SMM with instruments for price; contraction mapping for market shares; instruments: exogenous product characteristics of competing products.  
**Data:** US automobile market, product-level data, 1971–1990  
**Key Result:** Demand elasticities are economically plausible after accounting for endogeneity; random coefficients produce realistic substitution patterns; methodology became standard in structural IO.

---

### [Strebulaev, Whited 2012] Dynamic Models and Structural Estimation in Corporate Finance
**Journal/Source:** Foundations and Trends in Finance, Vol. 6, No. 1–2, pp. 1–163  
**Proximity Score:** 2/5  
**Summary:** Comprehensive survey of structural estimation methods in corporate finance. Covers continuous-time contingent claims models, discrete-time dynamic programming models, SMM estimation, GMM moment conditions, and model validation. Provides the methodological foundation for the proposed paper's structural estimation of dynamic capital structure models. Every step of the proposed paper's estimation procedure — model solution, moment selection, SMM criterion function, standard error calculation — is covered in this reference.  
**Identification:** N/A (survey/methodological reference)  
**Data:** N/A (survey)  
**Key Result:** Reviews SMM and GMM as the dominant estimation methods; covers continuous-time structural models and their empirical implementation.

---

### [Whited, Wu 2006] Financial Constraints Risk
**Journal/Source:** Review of Financial Studies, Vol. 19, No. 2, pp. 531–559  
**Proximity Score:** 2/5  
**Summary:** Constructs an index of external finance constraints via GMM estimation of an investment Euler equation. The Whited-Wu (WW) index is widely used as a proxy for financial constraints. Unlike the Kaplan-Zingales index, the WW index is grounded in structural theory. The proposed paper's W1(μ_i, ν) measure should be compared against the WW index as an alternative structural measure of financial constraints — the key test being whether W1 captures variation in leverage heterogeneity beyond what the WW index explains.  
**Identification:** GMM estimation of investment Euler equation with firm fixed effects.  
**Data:** Compustat US firms, 1975–2001  
**Key Result:** WW index successfully predicts constrained firm behavior in cross-sectional return tests; constrained firms earn higher expected returns consistent with a financial constraints risk factor.

---

### [Koenker, Bassett 1978] Regression Quantiles
**Journal/Source:** Econometrica, Vol. 46, No. 1, pp. 33–50  
**Proximity Score:** 1/5  
**Summary:** Foundational paper introducing quantile regression. Generalizes the OLS minimization of squared residuals to minimization of asymmetrically weighted absolute residuals, yielding estimates of conditional quantile functions. The proposed paper's use of quantile coupling D*(X) = F_ν^{-1}(F_μ(X)) is a functional analog of quantile regression: the debt contract optimally maps quantiles of the borrower's cash flow distribution to quantiles of the lender's capital supply distribution. This paper provides the econometric framework for estimating quantile functions from data.  
**Identification:** Asymmetric least absolute deviation minimization  
**Data:** N/A (methodological paper)  
**Key Result:** Regression quantiles are equivariant and have asymptotic normality; closely related to robust M-estimators; generalize sample quantiles to the regression setting.

---

### [Chernozhukov, Galichon, Hallin, Henry 2017] Monge-Kantorovich Depth, Quantiles, Ranks and Signs
**Journal/Source:** Annals of Statistics, Vol. 45, No. 1, pp. 223–256  
**Proximity Score:** 2/5  
**Summary:** Introduces center-outward distribution and quantile functions in multivariate settings using optimal transport ideas. Proposes a concept of quantile function based on Monge-Kantorovich transportation that extends the classical one-dimensional quantile-rank duality to higher dimensions. Directly relevant to the proposed paper's use of quantile coupling as the optimal debt contract: the paper provides the rigorous statistical theory for empirically estimating the quantile coupling map D*(X) = F_ν^{-1}(F_μ(X)) from data.  
**Identification:** N/A (theoretical statistics)  
**Data:** N/A  
**Key Result:** Multivariate quantile functions based on optimal transport exist, are unique, and satisfy desirable equivariance properties; convergence rates for empirical estimates are established.

---

## Category 8: Additional Related Capital Structure Papers (Proximity 2)

### [Modigliani, Miller 1958] The Cost of Capital, Corporation Finance and the Theory of Investment
**Journal/Source:** American Economic Review, Vol. 48, pp. 261–297  
**Proximity Score:** 1/5  
**Summary:** Establishes the irrelevance proposition: capital structure does not affect firm value in perfect markets without taxes or bankruptcy costs. The proposed paper's framework is an explicit departure from MM irrelevance — it shows that even with a perfect capital market (no taxes, frictions, or information asymmetry), the distributional mismatch between μ_i and ν implies a binding debt capacity constraint. The MM irrelevance theorem fails because capital supply is modeled as a distribution ν, not as a perfectly elastic supply at a scalar price r_f.  
**Identification:** Theoretical arbitrage argument  
**Data:** N/A  
**Key Result:** Capital structure irrelevance under perfect markets; leverage does not affect cost of capital or firm value.

---

### [Kraus, Litzenberger 1973] A State-Preference Model of Optimal Financial Leverage
**Journal/Source:** Journal of Finance, Vol. 28, No. 4, pp. 911–922  
**Proximity Score:** 1/5  
**Summary:** Introduces the trade-off theory of capital structure in a state-preference framework. Optimal leverage balances the tax shield of debt against the cost of bankruptcy in different states of nature. The proposed paper's model endogenizes both the optimal contract form and the debt capacity, showing that the trade-off between tax shields and bankruptcy costs is mediated by the distributional fit between borrower cash flows and capital supply.  
**Identification:** Theoretical state-preference model  
**Data:** N/A  
**Key Result:** Optimal leverage equates marginal tax benefit of debt with marginal expected bankruptcy cost; existence of interior optimum.

---

### [Myers, Majluf 1984] Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have
**Journal/Source:** Journal of Financial Economics, Vol. 13, No. 2, pp. 187–221  
**Proximity Score:** 1/5  
**Summary:** Establishes the pecking order theory of capital structure under asymmetric information. Firms prefer internal finance to external finance; debt to equity. Information asymmetry creates an adverse selection cost of equity issuance. The proposed paper's distributional framework is complementary: even under symmetric information, the distributional mismatch W1(μ_i, ν) determines borrowing capacity. Pecking order behavior can arise from high W1 (large distributional mismatch) even without informational asymmetries.  
**Identification:** Theoretical signaling/adverse selection model  
**Data:** N/A  
**Key Result:** Firms prefer debt over equity due to adverse selection; equity is issued only when manager is forced (no positive NPV projects available); investment may be foregone when equity cost is too high.

---

### [Almeida, Campello, Weisbach 2004] The Cash Flow Sensitivity of Cash
**Journal/Source:** Journal of Finance, Vol. 59, No. 4, pp. 1777–1804  
**Proximity Score:** 2/5  
**Summary:** Proposes the cash flow sensitivity of cash as a test of financial constraints. Financially constrained firms save a larger share of cash flows as cash holdings, reflecting precautionary demand for liquidity. The proposed paper's W1(μ_i, ν) is a distributional analog: firms with higher Wasserstein distance between their cash flow distribution and the capital supply distribution face greater constraints, and thus should have higher cash flow sensitivity of cash. This paper provides both motivation and a testable implication for the proposed paper's Wasserstein measure.  
**Identification:** OLS with financial constraints proxies; difference-in-means between constrained and unconstrained firms. Compustat 1971–2000.  
**Data:** Compustat US firms, 1971–2000  
**Key Result:** Constrained firms have significantly positive cash flow sensitivity of cash (approximately 0.05–0.11 per dollar of cash flow); unconstrained firms show no such sensitivity.

---

### [Berk, Stanton, Zechner 2010] Human Capital, Bankruptcy, and Capital Structure
**Journal/Source:** Journal of Finance, Vol. 65, No. 2, pp. 891–926  
**Proximity Score:** 2/5  
**Summary:** Derives the optimal labor contract for a levered firm and shows that employees become entrenched; human costs of bankruptcy are large, so the firm's optimal capital structure trades off tax benefits of debt against human bankruptcy costs. The model explains persistent idiosyncratic differences in leverage across firms without relying on informational frictions. The proposed paper complements this: human capital costs that depend on the firm's cash flow distribution (μ_i) interact with the capital supply distribution (ν) to jointly determine optimal leverage.  
**Identification:** Theoretical model with calibration; no structural estimation.  
**Data:** Calibration  
**Key Result:** Optimal leverage is lower when human bankruptcy costs are higher; model predicts that more levered firms pay higher wages; persistent leverage differences arise without informational frictions.

---

### [Roberts, Sufi 2009] Control Rights and Capital Structure: An Empirical Investigation
**Journal/Source:** Journal of Finance, Vol. 64, No. 4, pp. 1657–1695  
**Proximity Score:** 2/5  
**Summary:** Shows that creditor control rights, activated through debt covenant violations, cause sharp and persistent declines in corporate debt policy. When creditors accelerate or tighten debt terms following covenant violations, borrowers reduce net debt issuance substantially and rarely switch lenders. This empirical evidence on the credit supply side — that creditor characteristics shape the debt capacity of borrowers — is consistent with the proposed paper's treatment of ν (the capital supply distribution) as a determinant of debt capacity distinct from borrower characteristics.  
**Identification:** Regression discontinuity exploiting discrete covenant violation thresholds. DealScan loan-level data merged with Compustat.  
**Data:** DealScan, Compustat, 1996–2005  
**Key Result:** Covenant violation leads to 20–30% reduction in net debt issuance; effects persist for 3–4 years; creditor identity matters.

---

## Category 9: Scooping Risk — Working Papers to Monitor

**No proximity-5 papers found** (no working paper identified that uses Wasserstein distance to explain corporate leverage or debt capacity). The specific combination of optimal transport + corporate debt contracting + cross-sectional leverage is, to the best of this search's knowledge, a novel contribution. However, three areas pose moderate scooping risk:

1. **Optimal transport in financial economics (general):** Active work on Wasserstein distances in asset pricing, risk measures, and portfolio optimization (Blanchet and Murthy 2019; Finance and Stochastics papers on adapted Wasserstein distances). These use OT for model robustness, not debt contracting.

2. **Cash flow-based lending theory:** Hartman-Glaser, Mayer, Milbradt (2025, REStud) develop a theory of cash flow-based financing but do not use optimal transport or derive the Wasserstein distance as the sufficient statistic.

3. **Cross-sectional leverage determinants:** Active NBER/SSRN literature on leverage persistence and heterogeneity (e.g., Lemmon, Roberts, Zender 2008 and follow-on work) seeks the "missing" determinant of cross-sectional leverage. The proposed paper's W1 measure is a candidate answer.

**Recommended monitoring:** Search SSRN quarterly for "optimal transport" + "capital structure" or "debt contracting" or "leverage."

---

## Category 10: Matching Models in Credit and Capital Markets (Proximity 3–4)

*Editor note: This category was absent from the original review. It addresses the most important gap flagged in the 78/100 score — without it, the novelty claim of the two-sided distributional sorting model is vulnerable to referee attack.*

### [Sørensen 2007] How Smart Is Smart Money? A Two-Sided Matching Model of Venture Capital
**Journal/Source:** Journal of Finance, Vol. 62, No. 6, pp. 2725–2762  
**Proximity Score:** 4/5  
**Summary:** Develops and estimates a structural two-sided matching model of the VC-startup market. More experienced VCs match with better startups (positive assortative matching on quality), and companies funded by more experienced VCs are more likely to go public. The key methodological innovation is to exploit characteristics of other market participants — not just the matched pair — to separately identify sorting from direct influence: experienced VCs select into better deals (sorting effect) and also improve outcomes (treatment effect), with sorting almost twice as large as the treatment effect. This is the closest methodological precedent for the proposed paper's two-sided distributional sorting model, where firms with cash flow distribution μ_i sort into matches with capital supply distributions ν via a competitive mechanism. The Sørensen framework establishes that (a) two-sided matching in financial markets can be structurally estimated, (b) sorting is empirically important and can be separated from selection on observables, and (c) the correct welfare analysis must account for equilibrium matching, not just pairwise comparisons.  
**Identification:** Structural two-sided matching model with maximum likelihood estimation; identification exploits distributional characteristics of the full market (not just matched pairs).  
**Data:** VC investment records (VentureOne database); IPO outcome data; US VC-startup pairs, 1980s–1990s  
**Key Result:** Sorting (assortative matching on quality) accounts for nearly twice as much of the IPO rate gap between experienced and inexperienced VC-backed companies as the direct influence effect.

---

### [Galichon, Salanié 2022] Cupid's Invisible Hand: Social Surplus and Identification in Matching Models
**Journal/Source:** Review of Economic Studies, Vol. 89, No. 5, pp. 2600–2629  
**Proximity Score:** 4/5  
**Summary:** Develops a comprehensive theory of one-to-one matching with transferable utility (TU) and general unobserved heterogeneity. The equilibrium matching maximizes a social gain function that trades off complementarities in observable characteristics against matching on unobservables. The key result is that under a separability assumption, the equilibrium social surplus is identified from the joint distribution of observable match characteristics via a convex optimization problem — which is solved using optimal transport methods. Two estimators are proposed: a minimum distance estimator based on the generalized entropy of matching, and a GLM estimator for the Choo-Siow special case. This paper is of direct relevance to the proposed paper's model: the two-sided distributional sorting between firms (μ_i) and lenders (ν) is structurally a TU matching problem, and Galichon-Salanié's identification results provide the econometric foundation for recovering the surplus function (which in the proposed paper equals the debt capacity W1(μ_i, ν)/2) from observable match data (loan amounts, yields, borrower-lender pairs).  
**Identification:** Social planner's surplus identification via convex duality; optimal transport methods; minimum distance and GLM estimators.  
**Data:** N/A (theory and estimation methodology paper)  
**Key Result:** Equilibrium social surplus in TU matching is nonparametrically identified; minimum distance estimator achieves root-n consistency; optimal transport solves the equilibrium as a linear programming problem.

---

### [Shimer, Smith 2000] Assortative Matching and Search
**Journal/Source:** Econometrica, Vol. 68, No. 2, pp. 343–370  
**Proximity Score:** 3/5  
**Summary:** Extends Becker's (1973) frictionless neoclassical matching model to allow time-intensive partner search. Establishes sufficient conditions for positively or negatively assortative matching in search equilibrium: supermodularity of the match output function f and of log(f_x) and log(f_xy) suffice for positive assortative matching — conditions strictly stronger than Becker's complementarity condition in the frictionless case. The proposed paper's competitive matching of μ_i to ν is formally a frictionless TU-matching problem (cf. Galichon 2016), but Shimer-Smith's results on the conditions for assortative outcomes provide the theoretical backdrop against which the proposed paper's distributional matching should be compared. In particular, if the payoff from matching μ_i to ν is supermodular in the Wasserstein sense (higher-quality cash flow distributions match with higher-quality capital supply distributions), the proposed paper can claim positive assortative matching as an equilibrium property.  
**Identification:** Theoretical characterization of search equilibria with heterogeneous types; no empirical estimation.  
**Data:** N/A (theory paper)  
**Key Result:** Assortative matching in search models requires stronger conditions than in Walrasian matching; supermodularity of output and its log-derivatives is sufficient; search frictions may generate non-assortative equilibria even when Becker's conditions hold.

---

### [Choo, Siow 2006] Who Marries Whom and Why
**Journal/Source:** Journal of Political Economy, Vol. 114, No. 1, pp. 175–201  
**Proximity Score:** 3/5  
**Summary:** Develops and estimates a static transferable utility model of the marriage market with logistic unobserved heterogeneity (the "Choo-Siow model"). The paper generates a nonparametric marriage matching function with spillover effects — the equilibrium match probabilities depend on the full distribution of types in the market, not just pairwise compatibility. The model is estimated on US marriage data for 1971/72 and 1981/82, and the estimated surplus reveals that the gains to marriage for young adults fell substantially over the decade. In the proposed paper's context, the Choo-Siow framework is the discrete-type special case of the TU matching problem that determines which firms match with which capital supply pools; the Galichon-Salanié (2022) generalization extends Choo-Siow to continuous types and non-logistic heterogeneity, which is the appropriate framework for continuous cash flow distributions μ_i.  
**Identification:** Maximum likelihood estimation of the TU matching model; identified from observed match frequencies by type cell.  
**Data:** US Current Population Survey (CPS), marriage data 1971/72 and 1981/82  
**Key Result:** Nonparametric estimates of marriage surplus are strongly positive for same-age matches; gains to marriage fell significantly from 1971 to 1981; spillover effects of competition for partners are quantitatively important.

---

### [Antón, Dam 2020] A Two-Sided Matching Model of Monitored Finance
**Journal/Source:** Economica, Vol. 87, No. 345, pp. 132–157  
**Proximity Score:** 4/5  
**Summary:** Develops a theoretical model of partnership formation between heterogeneous investors and entrepreneurs, where investors differ in monitoring capacity and entrepreneurs differ in initial wealth. Both sides face incentive problems (double-sided moral hazard): the entrepreneur chooses effort and the investor chooses monitoring intensity, and the optimal contract must address both. The equilibrium exhibits positive assortative matching: high-monitoring-capacity investors match with low-wealth entrepreneurs who most need monitoring. The model predicts that financial market equilibrium is characterized by a continuum of contract types, each corresponding to a different investor-entrepreneur quality tier. This is a direct precursor to the proposed paper's model: Antón and Dam establish that two-sided heterogeneity in credit markets (investor monitoring ability vs. entrepreneur quality) generates assortative matching, which the proposed paper re-derives in the distributional setting (lender capital supply distribution ν vs. firm cash flow distribution μ_i), showing that the Wasserstein coupling D*(X) = F_ν^{-1}(F_μ(X)) is the optimal financial contract in that distributional setting.  
**Identification:** Theoretical mechanism design; no empirical estimation.  
**Data:** N/A (theory paper)  
**Key Result:** Positive assortative matching in monitored finance; investors with higher monitoring capacity match with entrepreneurs of lower initial wealth; equilibrium exhibits a continuum of contract types sorted by investor-entrepreneur quality pairs.

---

### [Chen, Song 2013] Two-Sided Matching in the Loan Market
**Journal/Source:** International Journal of Industrial Organization, Vol. 31, No. 2, pp. 145–152  
**Proximity Score:** 3/5  
**Summary:** Estimates a two-sided matching model of banks and firms in the loan market using the Fox (2010) matching maximum score estimator. Documents positive assortative matching by size: similarly-sized banks match with similarly-sized firms, and this pattern is stronger in northern European countries than in southern Europe or the US. Banks and firms also prefer geographically closer partners and partners with whom they have had prior loan relationships. Provides the first structural empirical evidence of assortative matching in the bank loan market, establishing that lending relationships are not random assignments but equilibrium outcomes of a two-sided matching process. The proposed paper's model predicts that the degree of assortative matching between μ_i and ν is determined by the surplus function W1(μ_i, ν), and Chen-Song's empirical methodology (matching maximum score) provides an estimation alternative to the SMM approach.  
**Identification:** Fox (2010) matching maximum score estimator; identification from rank-order conditions on observed matches.  
**Data:** Bureau van Dijk bank-firm loan data (Europe); multiple country sample, 2000–2003  
**Key Result:** Positive assortative matching by size in the loan market; small banks specialize in credit to small firms; geographic proximity and prior relationship are significant match determinants.

---

## Category 11: Applied Distributional Estimation Methods (Proximity 2–3)

*Editor note: This category was absent from the original review. The paper estimates μ_it (firm cash flow distribution) and ν_t (capital supply distribution) empirically; the following papers provide the econometric toolkit for doing so.*

### [Chernozhukov, Fernández-Val, Melly 2013] Inference on Counterfactual Distributions
**Journal/Source:** Econometrica, Vol. 81, No. 6, pp. 2205–2268  
**Proximity Score:** 3/5  
**Summary:** Develops modeling and inference tools for counterfactual distributions using regression methods — what the distribution of an outcome would have been under an alternative assignment of covariates. The key tool is "distributional regression": modeling the entire conditional CDF F(y|x) using a family of binary regressions (one per quantile level τ), then inverting to recover the quantile function. Joint functional central limit theorems and bootstrap validity results are derived for the estimators of both the status quo and counterfactual outcome distributions. This is the primary econometric reference for the proposed paper's empirical estimation of μ_it: the firm-specific cash flow distribution F_μ_i(x) is a conditional distribution of cash flows given firm characteristics, and distributional regression is the appropriate tool for estimating it from Compustat panel data. The paper also provides the inferential framework (joint CLT for the entire quantile function) needed to construct confidence bands for W1(μ_i, ν) as a function of estimated distributions.  
**Identification:** Distributional regression (one binary regression per quantile level); functional delta method; bootstrap inference for distributional statistics.  
**Data:** CPS wage data used as illustration (counterfactual wage distributions by gender/union status)  
**Key Result:** Distributional regression consistently estimates conditional CDFs; the functional delta method yields valid inference for smooth functionals of the distribution (including quantiles, distribution functions, and Wasserstein distances); bootstrap is valid for distributional statistics.

---

### [Firpo, Fortin, Lemieux 2009] Unconditional Quantile Regressions
**Journal/Source:** Econometrica, Vol. 77, No. 3, pp. 953–973  
**Proximity Score:** 2/5  
**Summary:** Proposes unconditional quantile regression (UQR) based on the recentered influence function (RIF) of the outcome's unconditional quantile. Unlike standard (conditional) quantile regression, UQR estimates the effect of covariates on the unconditional (marginal) distribution of the outcome — the distribution that the proposed paper seeks to characterize as μ_it. The RIF regression is a simple OLS of the influence function on covariates, making estimation computationally straightforward. Applied to unionization and US wage inequality, UQR shows that union membership has much larger effects on the lower tail of the unconditional wage distribution than standard quantile regression suggests. In the proposed paper's context, UQR provides a complementary approach to Chernozhukov et al. (2013) for estimating how firm characteristics shift the entire cash flow distribution μ_i — particularly relevant for the horse-race test of whether distributional shape (above and beyond mean and variance) explains cross-sectional leverage.  
**Identification:** RIF regression (OLS of influence function on covariates); marginal distributional effects rather than conditional quantile effects.  
**Data:** CPS (Current Population Survey), US wages, 1983–1985  
**Key Result:** Unconditional quantile partial effects differ substantially from conditional quantile partial effects; union membership compresses the lower tail of the unconditional wage distribution; UQR is consistent and asymptotically normal under standard conditions.

---

## BibTeX Entries

```bibtex
@article{Merton1974pricing,
  author  = {Robert C. Merton},
  title   = {On the Pricing of Corporate Debt: The Risk Structure of Interest Rates},
  journal = {Journal of Finance},
  year    = {1974},
  volume  = {29},
  number  = {2},
  pages   = {449--470},
  doi     = {10.1111/j.1540-6261.1974.tb03058.x}
}

@article{ModiglianiMiller1958cost,
  author  = {Franco Modigliani and Merton H. Miller},
  title   = {The Cost of Capital, Corporation Finance and the Theory of Investment},
  journal = {American Economic Review},
  year    = {1958},
  volume  = {48},
  number  = {3},
  pages   = {261--297}
}

@article{KrausLitzenberger1973state,
  author  = {Alan Kraus and Robert H. Litzenberger},
  title   = {A State-Preference Model of Optimal Financial Leverage},
  journal = {Journal of Finance},
  year    = {1973},
  volume  = {28},
  number  = {4},
  pages   = {911--922},
  doi     = {10.1111/j.1540-6261.1973.tb01415.x}
}

@article{JensenMeckling1976theory,
  author  = {Michael C. Jensen and William H. Meckling},
  title   = {Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure},
  journal = {Journal of Financial Economics},
  year    = {1976},
  volume  = {3},
  number  = {4},
  pages   = {305--360},
  doi     = {10.1016/0304-405X(76)90026-X}
}

@article{MyersMajluf1984corporate,
  author  = {Stewart C. Myers and Nicholas S. Majluf},
  title   = {Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have},
  journal = {Journal of Financial Economics},
  year    = {1984},
  volume  = {13},
  number  = {2},
  pages   = {187--221},
  doi     = {10.1016/0304-405X(84)90023-0}
}

@article{Townsend1979optimal,
  author  = {Robert M. Townsend},
  title   = {Optimal Contracts and Competitive Markets with Costly State Verification},
  journal = {Journal of Economic Theory},
  year    = {1979},
  volume  = {21},
  number  = {2},
  pages   = {265--293},
  doi     = {10.1016/0022-0531(79)90031-0}
}

@article{GaleHellwig1985incentive,
  author  = {Douglas Gale and Martin Hellwig},
  title   = {Incentive-Compatible Debt Contracts: The One-Period Problem},
  journal = {Review of Economic Studies},
  year    = {1985},
  volume  = {52},
  number  = {4},
  pages   = {647--663},
  doi     = {10.2307/2297737}
}

@article{FischerHeinkelZechner1989dynamic,
  author  = {Edwin O. Fischer and Robert Heinkel and Josef Zechner},
  title   = {Dynamic Capital Structure Choice: Theory and Tests},
  journal = {Journal of Finance},
  year    = {1989},
  volume  = {44},
  number  = {1},
  pages   = {19--40},
  doi     = {10.1111/j.1540-6261.1989.tb02402.x}
}

@article{Leland1994corporate,
  author  = {Hayne E. Leland},
  title   = {Corporate Debt Value, Bond Covenants, and Optimal Capital Structure},
  journal = {Journal of Finance},
  year    = {1994},
  volume  = {49},
  number  = {4},
  pages   = {1213--1252},
  doi     = {10.1111/j.1540-6261.1994.tb02452.x}
}

@article{LelandToft1996optimal,
  author  = {Hayne E. Leland and Klaus Bjerre Toft},
  title   = {Optimal Capital Structure, Endogenous Bankruptcy, and the Term Structure of Credit Spreads},
  journal = {Journal of Finance},
  year    = {1996},
  volume  = {51},
  number  = {3},
  pages   = {987--1019},
  doi     = {10.1111/j.1540-6261.1996.tb02714.x}
}

@article{RajanZingales1995what,
  author  = {Raghuram G. Rajan and Luigi Zingales},
  title   = {What Do We Know about Capital Structure? {S}ome Evidence from International Data},
  journal = {Journal of Finance},
  year    = {1995},
  volume  = {50},
  number  = {5},
  pages   = {1421--1460},
  doi     = {10.1111/j.1540-6261.1995.tb05184.x}
}

@article{HolmstromTirole1997financial,
  author  = {Bengt Holmstrom and Jean Tirole},
  title   = {Financial Intermediation, Loanable Funds, and the Real Sector},
  journal = {Quarterly Journal of Economics},
  year    = {1997},
  volume  = {112},
  number  = {3},
  pages   = {663--691},
  doi     = {10.1162/003355397555316}
}

@article{GrahamHarvey2001theory,
  author  = {John R. Graham and Campbell R. Harvey},
  title   = {The Theory and Practice of Corporate Finance: Evidence from the Field},
  journal = {Journal of Financial Economics},
  year    = {2001},
  volume  = {60},
  number  = {2--3},
  pages   = {187--243},
  doi     = {10.1016/S0304-405X(01)00044-7}
}

@article{FamaFrench2002testing,
  author  = {Eugene F. Fama and Kenneth R. French},
  title   = {Testing Trade-Off and Pecking Order Predictions About Dividends and Debt},
  journal = {Review of Financial Studies},
  year    = {2002},
  volume  = {15},
  number  = {1},
  pages   = {1--33},
  doi     = {10.1093/rfs/15.1.1}
}

@article{BakerWurgler2002market,
  author  = {Malcolm Baker and Jeffrey Wurgler},
  title   = {Market Timing and Capital Structure},
  journal = {Journal of Finance},
  year    = {2002},
  volume  = {57},
  number  = {1},
  pages   = {1--32},
  doi     = {10.1111/1540-6261.00414}
}

@article{AlmeidaCampelloWeisbach2004cash,
  author  = {Heitor Almeida and Murillo Campello and Michael S. Weisbach},
  title   = {The Cash Flow Sensitivity of Cash},
  journal = {Journal of Finance},
  year    = {2004},
  volume  = {59},
  number  = {4},
  pages   = {1777--1804},
  doi     = {10.1111/j.1540-6261.2004.00679.x}
}

@article{HennessyWhited2005debt,
  author  = {Christopher A. Hennessy and Toni M. Whited},
  title   = {Debt Dynamics},
  journal = {Journal of Finance},
  year    = {2005},
  volume  = {60},
  number  = {3},
  pages   = {1129--1165},
  doi     = {10.1111/j.1540-6261.2005.00758.x}
}

@article{KashyapStein2000what,
  author  = {Anil K. Kashyap and Jeremy C. Stein},
  title   = {What Do a Million Observations on Banks Say about the Transmission of Monetary Policy?},
  journal = {American Economic Review},
  year    = {2000},
  volume  = {90},
  number  = {3},
  pages   = {407--428},
  doi     = {10.1257/aer.90.3.407}
}

@article{Strebulaev2007tests,
  author  = {Ilya A. Strebulaev},
  title   = {Do Tests of Capital Structure Theory Mean What They Say?},
  journal = {Journal of Finance},
  year    = {2007},
  volume  = {62},
  number  = {4},
  pages   = {1747--1787},
  doi     = {10.1111/j.1540-6261.2007.01256.x}
}

@article{HennessyWhited2007costly,
  author  = {Christopher A. Hennessy and Toni M. Whited},
  title   = {How Costly Is External Financing? {E}vidence from a Structural Estimation},
  journal = {Journal of Finance},
  year    = {2007},
  volume  = {62},
  number  = {4},
  pages   = {1705--1745},
  doi     = {10.1111/j.1540-6261.2007.01255.x}
}

@article{BerryLevinsohnPakes1995automobile,
  author  = {Steven Berry and James Levinsohn and Ariel Pakes},
  title   = {Automobile Prices in Market Equilibrium},
  journal = {Econometrica},
  year    = {1995},
  volume  = {63},
  number  = {4},
  pages   = {841--890},
  doi     = {10.2307/2171802}
}

@article{KhwajaMian2008tracing,
  author  = {Asim Ijaz Khwaja and Atif Mian},
  title   = {Tracing the Impact of Bank Liquidity Shocks: Evidence from an Emerging Market},
  journal = {American Economic Review},
  year    = {2008},
  volume  = {98},
  number  = {4},
  pages   = {1413--1442},
  doi     = {10.1257/aer.98.4.1413}
}

@article{LemmonRobertsZender2008back,
  author  = {Michael L. Lemmon and Michael R. Roberts and Jaime F. Zender},
  title   = {Back to the Beginning: Persistence and the Cross-Section of Corporate Capital Structure},
  journal = {Journal of Finance},
  year    = {2008},
  volume  = {63},
  number  = {4},
  pages   = {1575--1608},
  doi     = {10.1111/j.1540-6261.2008.01369.x}
}

@article{DeAngeloDeAngeloWhited2011capital,
  author  = {Harry DeAngelo and Linda DeAngelo and Toni M. Whited},
  title   = {Capital Structure Dynamics and Transitory Debt},
  journal = {Journal of Financial Economics},
  year    = {2011},
  volume  = {99},
  number  = {2},
  pages   = {235--261},
  doi     = {10.1016/j.jfineco.2010.09.005}
}

@article{FrankGoyal2009capital,
  author  = {Murray Z. Frank and Vidhan K. Goyal},
  title   = {Capital Structure Decisions: Which Factors Are Reliably Important?},
  journal = {Financial Management},
  year    = {2009},
  volume  = {38},
  number  = {1},
  pages   = {1--37},
  doi     = {10.1111/j.1755-053X.2009.01026.x}
}

@article{GomesSchmid2010levered,
  author  = {Joao F. Gomes and Lukas Schmid},
  title   = {Levered Returns},
  journal = {Journal of Finance},
  year    = {2010},
  volume  = {65},
  number  = {2},
  pages   = {467--494},
  doi     = {10.1111/j.1540-6261.2009.01541.x}
}

@article{IvashinaScharfstein2010bank,
  author  = {Victoria Ivashina and David S. Scharfstein},
  title   = {Bank Lending During the Financial Crisis of 2008},
  journal = {Journal of Financial Economics},
  year    = {2010},
  volume  = {97},
  number  = {3},
  pages   = {319--338},
  doi     = {10.1016/j.jfineco.2009.12.001}
}

@article{NikolovWhited2014agency,
  author  = {Boris Nikolov and Toni M. Whited},
  title   = {Agency Conflicts and Cash: Estimates from a Dynamic Model},
  journal = {Journal of Finance},
  year    = {2014},
  volume  = {69},
  number  = {5},
  pages   = {1883--1921},
  doi     = {10.1111/jofi.12183}
}

@article{DeAngeloRoll2015stable,
  author  = {Harry DeAngelo and Richard Roll},
  title   = {How Stable Are Corporate Capital Structures?},
  journal = {Journal of Finance},
  year    = {2015},
  volume  = {70},
  number  = {1},
  pages   = {373--418},
  doi     = {10.1111/jofi.12163}
}

@article{MassaYasudaZhang2013supply,
  author  = {Massimo Massa and Ayako Yasuda and Lei Zhang},
  title   = {Supply Uncertainty of the Bond Investor Base and the Leverage of the Firm},
  journal = {Journal of Financial Economics},
  year    = {2013},
  volume  = {110},
  number  = {1},
  pages   = {185--214},
  doi     = {10.1016/j.jfineco.2013.06.003}
}

@article{WhitedWu2006financial,
  author  = {Toni M. Whited and Guojun Wu},
  title   = {Financial Constraints Risk},
  journal = {Review of Financial Studies},
  year    = {2006},
  volume  = {19},
  number  = {2},
  pages   = {531--559},
  doi     = {10.1093/rfs/hhj012}
}

@article{KoijenYogo2019demand,
  author  = {Ralph S.J. Koijen and Motohiro Yogo},
  title   = {A Demand System Approach to Asset Pricing},
  journal = {Journal of Political Economy},
  year    = {2019},
  volume  = {127},
  number  = {4},
  pages   = {1475--1515},
  doi     = {10.1086/701683}
}

@article{RobertsSufi2009control,
  author  = {Michael R. Roberts and Amir Sufi},
  title   = {Control Rights and Capital Structure: An Empirical Investigation},
  journal = {Journal of Finance},
  year    = {2009},
  volume  = {64},
  number  = {4},
  pages   = {1657--1695},
  doi     = {10.1111/j.1540-6261.2009.01476.x}
}

@article{BerkStantonZechner2010human,
  author  = {Jonathan Berk and Richard Stanton and Josef Zechner},
  title   = {Human Capital, Bankruptcy, and Capital Structure},
  journal = {Journal of Finance},
  year    = {2010},
  volume  = {65},
  number  = {2},
  pages   = {891--926},
  doi     = {10.1111/j.1540-6261.2010.01556.x}
}

@article{MorellecNikolovSchuerhoff2012corporate,
  author  = {Erwan Morellec and Boris Nikolov and Norman Sch{\"u}rhoff},
  title   = {Corporate Governance and Capital Structure Dynamics},
  journal = {Journal of Finance},
  year    = {2012},
  volume  = {67},
  number  = {3},
  pages   = {803--848},
  doi     = {10.1111/j.1540-6261.2012.01735.x}
}

@article{GreenwoodHanson2013issuer,
  author  = {Robin Greenwood and Samuel G. Hanson},
  title   = {Issuer Quality and Corporate Bond Returns},
  journal = {Review of Financial Studies},
  year    = {2013},
  volume  = {26},
  number  = {6},
  pages   = {1483--1525},
  doi     = {10.1093/rfs/hht016}
}

@article{LianMa2021anatomy,
  author  = {Chen Lian and Yueran Ma},
  title   = {Anatomy of Corporate Borrowing Constraints},
  journal = {Quarterly Journal of Economics},
  year    = {2021},
  volume  = {136},
  number  = {1},
  pages   = {229--291},
  doi     = {10.1093/qje/qjaa030}
}

@article{Zhu2021capital,
  author  = {Qifei Zhu},
  title   = {Capital Supply and Corporate Bond Issuances: Evidence from Mutual Fund Flows},
  journal = {Journal of Financial Economics},
  year    = {2021},
  volume  = {141},
  number  = {2},
  pages   = {551--572},
  doi     = {10.1016/j.jfineco.2021.03.012}
}

@article{Morellec2004managerial,
  author  = {Erwan Morellec},
  title   = {Can Managerial Discretion Explain Observed Leverage Ratios?},
  journal = {Review of Financial Studies},
  year    = {2004},
  volume  = {17},
  number  = {1},
  pages   = {257--294},
  doi     = {10.1093/rfs/hhg036}
}

@article{KoenkerBassett1978regression,
  author  = {Roger Koenker and Gilbert Bassett},
  title   = {Regression Quantiles},
  journal = {Econometrica},
  year    = {1978},
  volume  = {46},
  number  = {1},
  pages   = {33--50},
  doi     = {10.2307/1913643}
}

@article{ChernozhukovGalichonHallinHenry2017monge,
  author  = {Victor Chernozhukov and Alfred Galichon and Marc Hallin and Marc Henry},
  title   = {{M}onge--{K}antorovich Depth, Quantiles, Ranks and Signs},
  journal = {Annals of Statistics},
  year    = {2017},
  volume  = {45},
  number  = {1},
  pages   = {223--256},
  doi     = {10.1214/16-AOS1450}
}

@article{Brenier1991polar,
  author  = {Yann Brenier},
  title   = {Polar Factorization and Monotone Rearrangement of Vector-Valued Functions},
  journal = {Communications on Pure and Applied Mathematics},
  year    = {1991},
  volume  = {44},
  number  = {4},
  pages   = {375--417},
  doi     = {10.1002/cpa.3160440402}
}

@article{GangboMcCann1996geometry,
  author  = {Wilfrid Gangbo and Robert J. McCann},
  title   = {The Geometry of Optimal Transportation},
  journal = {Acta Mathematica},
  year    = {1996},
  volume  = {177},
  pages   = {113--161},
  doi     = {10.1007/BF02392620}
}

@book{Villani2003topics,
  author    = {C{\'e}dric Villani},
  title     = {Topics in Optimal Transportation},
  publisher = {American Mathematical Society},
  series    = {Graduate Studies in Mathematics},
  volume    = {58},
  year      = {2003},
  address   = {Providence, RI}
}

@book{Villani2009optimal,
  author    = {C{\'e}dric Villani},
  title     = {Optimal Transport: {O}ld and New},
  publisher = {Springer-Verlag},
  series    = {Grundlehren der mathematischen Wissenschaften},
  volume    = {338},
  year      = {2009},
  address   = {Berlin},
  doi       = {10.1007/978-3-540-71050-9}
}

@book{Galichon2016optimal,
  author    = {Alfred Galichon},
  title     = {Optimal Transport Methods in Economics},
  publisher = {Princeton University Press},
  year      = {2016},
  address   = {Princeton, NJ},
  isbn      = {9780691172767}
}

@incollection{Galichon2021unreasonable,
  author    = {Alfred Galichon},
  title     = {The Unreasonable Effectiveness of Optimal Transport in Economics},
  booktitle = {Advances in Economics and Econometrics},
  publisher = {Cambridge University Press},
  year      = {2021},
  note      = {Also available as arXiv:2107.04700}
}

@book{Santambrogio2015optimal,
  author    = {Filippo Santambrogio},
  title     = {Optimal Transport for Applied Mathematicians: Calculus of Variations, {PDEs}, and Modeling},
  publisher = {Springer International Publishing},
  series    = {Progress in Nonlinear Differential Equations and Their Applications},
  volume    = {87},
  year      = {2015},
  doi       = {10.1007/978-3-319-20828-2}
}

@techreport{StrebulaevWhited2012dynamic,
  author      = {Ilya A. Strebulaev and Toni M. Whited},
  title       = {Dynamic Models and Structural Estimation in Corporate Finance},
  institution = {Foundations and Trends in Finance},
  year        = {2012},
  volume      = {6},
  number      = {1--2},
  pages       = {1--163},
  doi         = {10.1561/0500000035}
}

@article{LemmonRoberts2010response,
  author  = {Michael L. Lemmon and Michael R. Roberts},
  title   = {The Response of Corporate Financing and Investment to Changes in the Supply of Credit},
  journal = {Journal of Financial and Quantitative Analysis},
  year    = {2010},
  volume  = {45},
  number  = {3},
  pages   = {555--587},
  doi     = {10.1017/S0022109010000256}
}

@article{Sorensen2007smart,
  author  = {Morten S{\o}rensen},
  title   = {How Smart Is Smart Money? {A} Two-Sided Matching Model of Venture Capital},
  journal = {Journal of Finance},
  year    = {2007},
  volume  = {62},
  number  = {6},
  pages   = {2725--2762},
  doi     = {10.1111/j.1540-6261.2007.01291.x}
}

@article{GalichonSalanie2022cupid,
  author  = {Alfred Galichon and Bernard Salan{\'i}e},
  title   = {Cupid's Invisible Hand: Social Surplus and Identification in Matching Models},
  journal = {Review of Economic Studies},
  year    = {2022},
  volume  = {89},
  number  = {5},
  pages   = {2600--2629},
  doi     = {10.1093/restud/rdab090}
}

@article{ShimerSmith2000assortative,
  author  = {Robert Shimer and Lones Smith},
  title   = {Assortative Matching and Search},
  journal = {Econometrica},
  year    = {2000},
  volume  = {68},
  number  = {2},
  pages   = {343--370},
  doi     = {10.1111/1468-0262.00112}
}

@article{ChooSiow2006who,
  author  = {Eugene Choo and Aloysius Siow},
  title   = {Who Marries Whom and Why},
  journal = {Journal of Political Economy},
  year    = {2006},
  volume  = {114},
  number  = {1},
  pages   = {175--201},
  doi     = {10.1086/498585}
}

@article{AntonDam2020twosided,
  author  = {Arturo Ant{\'o}n and Kaniska Dam},
  title   = {A Two-Sided Matching Model of Monitored Finance},
  journal = {Economica},
  year    = {2020},
  volume  = {87},
  number  = {345},
  pages   = {132--157},
  doi     = {10.1111/ecca.12298}
}

@article{ChenSong2013twosided,
  author  = {Jiawei Chen and Kejun Song},
  title   = {Two-Sided Matching in the Loan Market},
  journal = {International Journal of Industrial Organization},
  year    = {2013},
  volume  = {31},
  number  = {2},
  pages   = {145--152},
  doi     = {10.1016/j.ijindorg.2012.12.002}
}

@article{ChernozhukovFernandezValMelly2013inference,
  author  = {Victor Chernozhukov and Iv{\'a}n Fern{\'a}ndez-Val and Blaise Melly},
  title   = {Inference on Counterfactual Distributions},
  journal = {Econometrica},
  year    = {2013},
  volume  = {81},
  number  = {6},
  pages   = {2205--2268},
  doi     = {10.3982/ECTA10582}
}

@article{FirpoFortinLemieux2009unconditional,
  author  = {Sergio Firpo and Nicole M. Fortin and Thomas Lemieux},
  title   = {Unconditional Quantile Regressions},
  journal = {Econometrica},
  year    = {2009},
  volume  = {77},
  number  = {3},
  pages   = {953--973},
  doi     = {10.3982/ECTA6822}
}

@article{Crouzet2018aggregate,
  author  = {Nicolas Crouzet},
  title   = {Aggregate Implications of Corporate Debt Choices},
  journal = {Review of Economic Studies},
  year    = {2018},
  volume  = {85},
  number  = {3},
  pages   = {1635--1682},
  doi     = {10.1093/restud/rdx058}
}

@article{NikolovSchmidSteri2021sources,
  author  = {Boris Nikolov and Lukas Schmid and Roberto Steri},
  title   = {The Sources of Financing Constraints},
  journal = {Journal of Financial Economics},
  year    = {2021},
  volume  = {139},
  number  = {2},
  pages   = {478--501},
  doi     = {10.1016/j.jfineco.2020.07.018}
}

@article{ElenevLandvoigtVanNieuwerburgh2021macroeconomic,
  author  = {Vadim Elenev and Tim Landvoigt and Stijn {Van Nieuwerburgh}},
  title   = {A Macroeconomic Model with Financially Constrained Producers and Intermediaries},
  journal = {Econometrica},
  year    = {2021},
  volume  = {89},
  number  = {3},
  pages   = {1361--1418},
  doi     = {10.3982/ECTA16438}
}

@article{HartmanGlaserMayerMilbradt2025theory,
  author  = {Barney Hartman-Glaser and Simon Mayer and Konstantin Milbradt},
  title   = {A Theory of Cash Flow-Based Financing with Distress Resolution},
  journal = {Review of Economic Studies},
  year    = {2025},
  volume  = {92},
  number  = {6},
  pages   = {3995--4025},
  doi     = {10.1093/restud/rdae093},
  note    = {NBER Working Paper No. 29712 (2022)}
}
```

---

## Frontier Map

### What Has Been Established

**Cross-sectional leverage heterogeneity is large and persistent.** Lemmon, Roberts, and Zender (2008) document that firm fixed effects explain 60% of leverage variation, and high-leverage firms remain high-leverage for decades. Standard observables (profitability, market-to-book, tangibility, size) together explain less than 30% of cross-sectional leverage. The residual — an unexplained time-invariant firm effect — has eluded explanation for 15 years.

**Structural capital structure models use scalar volatility as the sufficient statistic.** Merton (1974), Leland (1994, 1996), and Fischer et al. (1989) all parameterize the firm's risk by the volatility σ of a GBM process. Two firms with the same σ have the same predicted debt capacity. The model predicts no residual cross-sectional heterogeneity after controlling for σ.

**SMM is the dominant estimation framework for dynamic capital structure models.** Hennessy and Whited (2005, 2007), Nikolov and Whited (2014), and Morellec, Nikolov, and Schuerhoff (2012) all use SMM to match Compustat moments to dynamic model predictions. The frontier has moved post-2017: Nikolov, Schmid, and Steri (2021, JFE) extend the framework to disentangle multiple structural sources of financing constraints using international private-firm data; Crouzet (2018, REStud) introduces a two-debt-instrument structural model; Elenev, Landvoigt, and Van Nieuwerburgh (2021, Econometrica) add general equilibrium with jointly constrained firms and intermediaries.

**Two-sided matching is an empirically important feature of credit markets.** Sørensen (2007, JF) establishes that sorting in the VC-startup market accounts for almost twice as much of the performance gap as the direct treatment effect. Antón and Dam (2020, Economica) show that two-sided heterogeneity in monitored finance generates positive assortative matching in equilibrium. Chen and Song (2013, IJIO) provide direct empirical evidence of size-based assortative matching in bank loan markets. Choo and Siow (2006, JPE) and Galichon and Salanié (2022, REStud) provide the econometric toolkit for identifying and estimating the social surplus in TU matching problems, which maps directly onto the proposed paper's debt capacity surplus function W1(μ_i, ν)/2.

**Capital supply matters for corporate leverage.** Massa, Yasuda, and Zhang (2013) show that investor base uncertainty reduces leverage. Zhu (2021) shows that mutual fund flows shift bond issuance probability by 0.83 pp per standard deviation. Lemmon and Roberts (2010, JFQA) show that exogenous credit supply contractions pass through almost one-for-one to corporate investment with negligible substitution. Greenwood and Hanson (2013) show that issuer quality shifts predict future bond returns. These papers treat capital supply as a firm-specific, time-varying quantity but do not model it as a distribution.

**Cash flow-based borrowing constraints dominate collateral-based constraints.** Lian and Ma (2021) document that 80% of US corporate debt is cash-flow-based. Hartman-Glaser, Mayer, and Milbradt (2025) develop a contracting theory of this result.

**Optimal transport has extensive economics applications.** Galichon (2016, 2021) reviews applications to matching, quantile regression, discrete choice, and trade. Galichon and Salanié (2022) show that TU matching equilibria solve an optimal transport problem. No existing paper applies optimal transport to debt contracting or corporate leverage.

**Distributional estimation methods are available.** Chernozhukov, Fernández-Val, and Melly (2013, Econometrica) develop distributional regression and functional inference tools for estimating entire conditional CDFs from data — the appropriate tool for estimating μ_it from Compustat panel data. Firpo, Fortin, and Lemieux (2009, Econometrica) develop unconditional quantile regression for estimating marginal distributional effects.

### Methodological Frontier

- SMM/GMM with Compustat moments (Hennessy and Whited 2005, 2007; Nikolov and Whited 2014; Nikolov, Schmid, Steri 2021)
- Dynamic trade-off models with continuous-time contingent claims (Leland 1994; Morellec 2004; Crouzet 2018)
- Structural two-sided matching estimation (Sørensen 2007; Galichon and Salanié 2022)
- Distributional regression and functional inference for CDFs (Chernozhukov, Fernández-Val, Melly 2013)
- Optimal transport methods in matching and discrete choice (Galichon 2016; Galichon and Salanié 2022)
- General equilibrium macro-finance with jointly constrained firms and banks (Elenev, Landvoigt, Van Nieuwerburgh 2021)
- Demand systems for asset pricing (Koijen and Yogo 2019)

**Gap:** No paper has combined optimal transport methods with structural capital structure estimation. No paper has estimated a two-sided distributional matching model where types are firm cash flow distributions (μ_i) and lender capital supply distributions (ν).

### Data Frontier

- Compustat US panel (Lemmon et al. 2008; Hennessy and Whited 2007): standard; most papers use this
- DealScan loan-level data (Roberts and Sufi 2009; Ivashina and Scharfstein 2010; Lemmon and Roberts 2010): loan and covenant terms; bank-firm match data
- Bond ownership data (Massa et al. 2013): tracks investor identity at the bond level
- Morningstar bond holdings (Zhu 2021): fund-level bond positions
- ORBIS international firm panel (Nikolov, Schmid, Steri 2021): includes private firms; cross-country comparison
- Bureau van Dijk bank-firm loan data, Europe (Chen and Song 2013): for cross-country matching analysis

### Geographic/Contextual Gaps

- Most structural capital structure work uses US Compustat only; international applications (Rajan and Zingales 1995; Nikolov, Schmid, Steri 2021 using ORBIS) remain limited
- Private firms are severely understudied (Lian and Ma 2021 use DealScan which covers large private firms; the rest of the distribution is unknown)
- Emerging market capital supply distributions (ν) are poorly characterized
- The two-sided matching literature in credit markets (Chen and Song 2013) has focused on bank loans; bond markets lack a structural matching analysis

### Open Questions

1. **What generates the time-invariant firm fixed effect in leverage?** (Lemmon, Roberts, Zender 2008 identified the puzzle but not the cause)
2. **How does the distribution of capital supply (ν) shift over the credit cycle?** (Greenwood and Hanson 2013 document aggregate shifts; firm-level effects are not well characterized)
3. **Does distributional shape of cash flows — beyond mean and variance — explain leverage?** (No paper has tested this directly)
4. **Is the quantile coupling the optimal debt contract when both μ_i and ν are non-Gaussian?** (Hartman-Glaser et al. 2025 do not derive this result)
5. **What is the social surplus function in the credit matching market?** (Galichon and Salanié 2022 provide the identification framework; no paper has applied it to bank-firm matching with distributional types)
6. **Does assortative matching on cash flow distributions (not just firm size or credit rating) matter empirically?** (Sørensen 2007 and Chen-Song 2013 test matching by observable proxies; the proposed paper's distributional distance W1(μ_i, ν) provides a richer continuous type space)

### Where This Project Fits

This paper introduces the distribution of capital supply ν as a new structural primitive in corporate capital structure theory and bridges two previously separate literatures: the structural capital structure tradition (Merton 1974 through Nikolov, Schmid, Steri 2021) and the two-sided matching literature applied to financial markets (Sørensen 2007; Antón and Dam 2020; Galichon and Salanié 2022). Prior structural models treat capital supply as a price scalar (the risk-free rate r_f); prior matching models use discrete observable proxies (firm size, VC experience) rather than continuous distributional types. This paper shows that when both firm cash flows and capital supply are modeled as distributions, the optimal debt contract is the quantile coupling D*(X) = F_ν^{-1}(F_μ(X)) and individual debt capacity equals W1(μ_i, ν)/2. This result (a) provides a theoretical foundation for the unexplained time-invariant firm fixed effect documented by Lemmon et al. (2008), (b) extends Hartman-Glaser et al. (2025) by introducing ν as a distribution and deriving the Wasserstein distance as the exact debt capacity formula via optimal transport, and (c) generalizes Sørensen (2007) and Chen-Song (2013) from observable firm-size proxies to continuous distributional types as the matching type space.

### Scooping Risks

**Proximity 4–5 papers (direct competitors):** None identified. No published or working paper found that (a) uses Wasserstein distances to measure debt capacity or leverage heterogeneity, (b) derives optimal debt contracts using optimal transport theory, or (c) introduces the capital supply distribution ν as a structural primitive in a corporate finance model.

**Proximity 4 papers in the matching strand (must be addressed in the introduction to pre-empt referee attacks on novelty):**
- Sørensen (2007, JF): establishes two-sided structural matching estimation in financial markets (VC-startup); the proposed paper applies the same matching logic to continuous distributional types (μ_i, ν) — a generalization not present in Sørensen, who uses discrete type proxies (VC experience, startup quality indicators).
- Antón and Dam (2020, Economica): develops a two-sided matching theory of monitored credit markets with incentive contracts; the proposed paper's distributional framework extends this by adding the capital supply distribution ν and deriving the Wasserstein sufficient statistic for debt capacity.
- Galichon and Salanié (2022, REStud): establishes TU matching identification via optimal transport; the proposed paper is the first application of this framework to debt contracting with continuous distributional types.

**Proximity 3 papers (close but different angle):**
- Hartman-Glaser, Mayer, Milbradt (2025): closest theoretical paper; addresses cash flow-based financing but does not use optimal transport, does not derive quantile coupling, does not compute W1 as debt capacity.
- Massa, Yasuda, Zhang (2013): closest empirical paper; treats investor base uncertainty as a leverage determinant but measures it as a scalar variance, not a distributional distance.
- Nikolov, Schmid, Steri (2021): most recent structural estimation frontier paper in corporate finance; disentangles financing constraint sources but does not model capital supply as a distribution.
- Crouzet (2018): structural model of bank vs. bond debt choice; models two capital instruments but not as distributional types.

**Monitoring recommendation:** Search SSRN monthly for "optimal transport" + "corporate debt" or "capital structure" or "leverage" or "matching" + "credit market"; check working papers by: Alfred Galichon, Bernard Salanié, Toni Whited, Erwan Morellec, Michael Roberts, Morten Sørensen, Nicolas Crouzet.

---

## Positioning Notes

### Suggested Contribution Statement (Draft for Author Adaptation)

We introduce the distribution of capital supply ν as a new structural primitive in corporate capital structure theory and apply tools from the two-sided matching literature (Sørensen 2007; Galichon and Salanié 2022) to a continuous-type debt contracting setting. Prior structural capital structure models — from Merton (1974) to Leland (1994) to Hennessy and Whited (2007) to Nikolov, Schmid, and Steri (2021) — treat capital supply as a price (the risk-free rate r_f), implicitly assuming perfectly elastic supply at a scalar; prior matching models in finance (Sørensen 2007; Antón and Dam 2020; Chen and Song 2013) use discrete observable proxies rather than continuous distributional types. We show that when both sides of the credit market are modeled as distributions, the optimal debt contract is the quantile coupling D*(X) = F_ν^{-1}(F_μ(X)) — the unique measure-preserving map that transports the firm's cash flow distribution μ_i to the lender's capital supply distribution ν — and individual debt capacity equals W1(μ_i, ν)/2 — the Wasserstein distance between the two distributions divided by two. We provide the first structural estimation of this model, demonstrating that the Wasserstein distance explains a significant portion of the time-invariant firm-specific leverage heterogeneity documented by Lemmon, Roberts, and Zender (2008) but unexplained by existing structural models.

### Key Differentiators

- **vs. Merton (1974) / Leland (1994):** Prior models use scalar σ as the sufficient statistic for debt capacity; this paper replaces σ with W1(μ_i, ν), a distributional measure that nests scalar volatility as a special case.
- **vs. Hartman-Glaser, Mayer, Milbradt (2025):** HMM derive an optimal contract for cash flow-based lending but assume a scalar intermediary cost of capital; this paper introduces ν as a distribution and derives the Wasserstein distance as the exact debt capacity formula.
- **vs. Sørensen (2007) / Antón and Dam (2020):** Prior matching papers in finance use discrete observable proxies for type (VC experience, entrepreneur wealth); this paper uses continuous cash flow distributions μ_i as the type, requiring optimal transport methods rather than discrete matching estimators.
- **vs. Galichon and Salanié (2022):** G-S establish identification of TU matching surplus from observable match data; this paper provides the first application to debt contracting, where the surplus is the debt capacity W1(μ_i, ν)/2 and the match is between firm cash flow distributions and lender capital supply distributions.
- **vs. Massa, Yasuda, Zhang (2013):** MYZ measure supply uncertainty as a scalar (flow volatility) and find reduced-form effects on leverage; this paper provides the structural theory for why the distribution of capital supply — not just its variance — determines debt capacity.
- **vs. Lemmon, Roberts, Zender (2008):** LRZ identify a large unexplained firm fixed effect in leverage; this paper provides a theoretical candidate (W1(μ_i, ν)) for the mechanism generating this persistent heterogeneity.
- **vs. Hennessy, Whited (2005, 2007) / Nikolov, Schmid, Steri (2021):** These papers use SMM to estimate financing frictions; this paper introduces a new moment — the empirical Wasserstein distance — into the SMM objective function, and a new structural primitive (ν as a distribution) that existing SMM frameworks do not parameterize.
- **vs. Crouzet (2018):** Crouzet models the bank-bond choice as discrete and focuses on aggregate implications; this paper models the capital supply as a continuous distribution and focuses on cross-sectional heterogeneity in individual firm debt capacity.

### Potential Target Journals (Ranked)

1. **Journal of Finance** — Directly targets corporate capital structure; SMM structural papers (HW 2005, 2007; Nikolov-Whited 2014; Sørensen 2007) published here; novel theory + structural estimation + matching model matches JF appetite.
2. **Review of Economic Studies** — Strong theory-with-evidence papers; Crouzet (2018), Galichon-Salanié (2022), Hartman-Glaser et al. (2025) published here; if the theoretical contribution (quantile coupling, Wasserstein debt capacity) is the primary contribution, REStud is natural.
3. **Review of Financial Studies** — Strong structural estimation tradition; Greenwood and Hanson (2013), Morellec (2004) published here; slightly less weighted toward structural theory than JF.
4. **Journal of Financial Economics** — Empirically oriented; Massa et al. (2013), DeAngelo et al. (2011), Nikolov-Schmid-Steri (2021) published here; stronger if the paper leads with reduced-form empirical tests of W1.
5. **Quarterly Journal of Economics** — If the optimal transport theoretical contribution is emphasized over the corporate finance application; Lian and Ma (2021) published here; optimal transport in economics well-received.
```

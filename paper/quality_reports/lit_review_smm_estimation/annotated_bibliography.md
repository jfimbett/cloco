# Annotated Bibliography: GMM, SMM, and Structural Estimation in Corporate Finance

**Project**: Distributional Debt Capacity / Constrained GMM with Spread Moments
**Prepared**: 2026-06-14
**Scope**: Foundational GMM/SMM methodology, indirect inference, structural estimation in corporate finance, constrained/moment-inequality methods, related corporate finance structural papers

---

## A. Directly Related — Structural Estimation Methodology with Finance Applications (Proximity 4–5)

---

### [Duffie Singleton 1993] Simulated Moments Estimation of Markov Models of Asset Prices
**Journal/Source**: Econometrica, Vol. 61, No. 4, pp. 929–952
**Proximity Score**: 5/5
**Summary**: Duffie and Singleton develop the simulated moments estimator (SME) for dynamic Markov models of asset prices. The paper provides conditions for weak and strong consistency and asymptotic normality when the model's moments cannot be evaluated analytically but can be simulated. The framework covers continuous-time diffusion models for asset returns and interest rates. The paper is the canonical reference for applying SMM to financial economics models where simulation is the only feasible route to compute theoretical moments.
**Identification**: Simulated Method of Moments (SMM) — match simulated versus empirical moments via GMM objective
**Data**: Illustrative applications to asset pricing models; theoretical framework paper
**Key Result**: Asymptotic normality and consistency established under standard regularity conditions; finite-sample improvement over direct GMM when analytical moments unavailable

---

### [Lee Ingram 1991] Simulation Estimation of Time-Series Models
**Journal/Source**: Journal of Econometrics, Vol. 47, No. 2–3, pp. 197–205
**Proximity Score**: 5/5
**Summary**: Lee and Ingram pioneer the formal econometric theory for SMM applied to time-series models. Their paper demonstrates that replacing analytical moment conditions with simulated counterparts yields consistent and asymptotically normal estimators under conditions analogous to standard GMM. They apply the method to estimating asset pricing models. This is the co-foundational reference alongside Duffie-Singleton (1993) for justifying the use of SMM as an estimation procedure in structural finance models.
**Identification**: Method of Simulated Moments (SMM); conditions for consistency and asymptotic normality derived
**Data**: Applied to asset pricing time-series; theoretical econometrics paper
**Key Result**: Asymptotic normality and consistency of SMM estimator established; SMM standard errors depend on number of simulation draws relative to sample size

---

### [Gourieroux Monfort Renault 1993] Indirect Inference
**Journal/Source**: Journal of Applied Econometrics, Vol. 8, Supplement, pp. S85–S118
**Proximity Score**: 5/5
**Summary**: This foundational paper introduces indirect inference as a simulation-based alternative to direct maximum likelihood or GMM when the structural model's likelihood or moments are analytically intractable. The method matches an auxiliary "binding function" estimated from simulated data against its empirical counterpart. It requires only the ability to simulate the structural model. The method generalizes GMM and SMM and is widely used in structural macro-finance estimation. Any paper using SMM or simulation-based GMM should cite Gourieroux-Monfort-Renault as background.
**Identification**: Indirect inference via auxiliary binding function; consistent and asymptotically normal under standard regularity conditions
**Data**: Illustrative applications; primarily theoretical
**Key Result**: Indirect inference estimator is consistent and asymptotically normal; optimal auxiliary model choice discussed

---

### [Gourieroux Monfort 1996] Simulation-Based Econometric Methods (Book)
**Journal/Source**: Oxford University Press / CORE Lectures, 196 pp.
**Proximity Score**: 4/5
**Summary**: This textbook provides a unified treatment of simulation-based estimation methods including MSM (Method of Simulated Moments), Simulated Maximum Likelihood, Simulated Pseudo-Maximum Likelihood, Simulated Nonlinear Least Squares, and Indirect Inference. It covers both theory and application to limited dependent variable models, financial series, and switching regime models. Essential reference for any paper using SMM or indirect inference.
**Identification**: Textbook treatment of MSM, indirect inference, and related simulation-based methods
**Data**: N/A (textbook)
**Key Result**: N/A (textbook); provides asymptotic theory for all major simulation-based estimators

---

### [Strebulaev Whited 2012] Dynamic Models and Structural Estimation in Corporate Finance
**Journal/Source**: Foundations and Trends in Finance, Vol. 6, No. 1–2, pp. 1–163
**Proximity Score**: 5/5
**Summary**: This survey reviews how dynamic structural models are estimated using GMM, SMM, and simulated maximum likelihood in corporate finance. Covers Hennessy-Whited (2005, 2007), DeAngelo-DeAngelo-Whited (2011), Nikolov-Whited (2014), and related papers. Describes the moment selection problem, weighting matrix construction, overidentification tests, and bootstrap inference. The definitive methodological reference for structural estimation in corporate finance — must cite alongside the specific methodology papers.
**Identification**: Survey of GMM, SMM, and simulated MLE applied to dynamic corporate finance models
**Data**: Survey paper; reviews Compustat-based applications
**Key Result**: SMM with simulation draws ≥ 10× sample size is standard practice; bootstrap of full estimation procedure required for valid standard errors when first-stage moments are estimated

---

### [Whited Wu 2006] Financial Constraints Risk
**Journal/Source**: Review of Financial Studies, Vol. 19, No. 2, pp. 531–559
**Proximity Score**: 4/5
**Summary**: Whited and Wu construct an index of financial constraints by estimating an investment Euler equation via GMM. The paper applies GMM directly to moment conditions derived from the firm's optimality conditions. It is a direct application of Euler-equation GMM to corporate finance, yielding the Whited-Wu (WW) index as a side product. The methodology closely parallels constrained GMM applications: moment conditions are derived from a structural model (Euler equations), and the weighting matrix is estimated.
**Identification**: GMM estimation of investment Euler equation; optimal weighting matrix computed from heteroskedasticity-robust variance
**Data**: Compustat firm-level panel, US manufacturing, 1975–2000
**Key Result**: Constrained firms earn higher returns; WW index strongly predicts external financing difficulties; GMM J-test of Euler equation overidentification p > 0.10

---

### [Erickson Whited 2000] Measurement Error and the Relationship between Investment and Q
**Journal/Source**: Journal of Political Economy, Vol. 108, No. 5, pp. 1027–1057
**Proximity Score**: 4/5
**Summary**: Erickson and Whited address the classic measurement error problem in the investment-Q relationship using higher-order GMM moments. They introduce a third-order moment estimator that identifies the true Q coefficient even when Q is measured with error — an early example of using nonstandard moment conditions (beyond the standard second-order) for structural identification. This paper motivates the use of higher-order moments in GMM as identifying restrictions, directly paralleling the use of spread moments as overidentifying conditions.
**Identification**: Higher-order GMM moment estimator; instruments derived from third-order moments of error-contaminated variables
**Data**: Compustat, US manufacturing, 1992–1995
**Key Result**: OLS coefficient on Q severely attenuated by measurement error; higher-order moment estimator recovers substantial investment-Q sensitivity

---

### [Bloom 2009] The Impact of Uncertainty Shocks
**Journal/Source**: Econometrica, Vol. 77, No. 3, pp. 623–685
**Proximity Score**: 4/5
**Summary**: Bloom estimates a structural model of firm investment with both convex and nonconvex capital adjustment costs using SMM calibrated to match Compustat and labor market moments. The paper jointly estimates labor and capital adjustment costs simultaneously via simulation. A model-implied aggregate is then compared to time-series impulse responses from a VAR, providing cross-equation overidentification. Demonstrates the state-of-the-art approach to multi-moment structural estimation in a macro-finance context.
**Identification**: SMM — matches simulated moments from the model against data moments; model fit validated against VAR impulse responses
**Data**: Compustat firm-level data; aggregate US macro data
**Key Result**: Uncertainty shocks generate sharp, rapid drops and rebounds in output and employment; ignoring capital adjustment costs produces substantial bias in labor cost estimates

---

### [Ottonello Winberry 2020] Financial Heterogeneity and the Investment Channel of Monetary Policy
**Journal/Source**: Econometrica, Vol. 88, No. 6, pp. 2473–2502
**Proximity Score**: 4/5
**Summary**: Ottonello and Winberry study the role of financial heterogeneity in determining the investment channel of monetary policy. They build a heterogeneous-firm New Keynesian model with default risk and estimate it by matching empirical responses to monetary shocks. The paper demonstrates how structural estimation with moment conditions derived from heterogeneous firms can be used to disentangle mechanisms. Directly relevant as a methodological precedent for cross-sectional structural estimation with spread/default moments.
**Identification**: Structural estimation matching model responses to monetary policy shocks; empirical reduced-form panel evidence supports structural interpretation
**Data**: Compustat, 1980–2014
**Key Result**: Low default-risk firms are most responsive to monetary shocks due to flatter marginal cost of finance curve; aggregate monetary policy effect depends on cross-sectional distribution of risk

---

### [Gomes Schmid 2021] Equilibrium Asset Pricing with Leverage and Default
**Journal/Source**: Journal of Finance, Vol. 76, No. 2, pp. 977–1018
**Proximity Score**: 4/5
**Summary**: Gomes and Schmid develop a general equilibrium model linking stock and corporate bond pricing to endogenous leverage and aggregate volatility. The model features heterogeneous firms making optimal investment and financing decisions. Structural estimation by SMM matches model-implied moments for leverage, returns, and credit spreads simultaneously. The paper demonstrates how cross-sectional spread moments are used as identifying conditions alongside leverage moments — directly analogous to the 10-spread-moment GMM design.
**Identification**: SMM — simultaneous matching of leverage, equity return, and credit spread moments
**Data**: Compustat, CRSP, corporate bond data
**Key Result**: Countercyclical leverage drives predictable variation in risk premia; endogenous default produces countercyclical credit spreads propagated through investment

---

### [Gomes Schmid 2010] Levered Returns
**Journal/Source**: Journal of Finance, Vol. 65, No. 2, pp. 467–494
**Proximity Score**: 3/5
**Summary**: Gomes and Schmid revisit the theoretical relation between financial leverage and stock returns in a dynamic model where investment and financing are endogenous. A quantitative structural model is calibrated to match leverage and return moments. In the model, high-leverage firms tend to be mature with safe book assets and fewer growth opportunities. Relevant as an example of quantitative structural capital structure estimation using matched moments.
**Identification**: Structural model calibration to leverage and return moments; structural simulation
**Data**: Compustat, CRSP
**Key Result**: Leverage-return relationship is more complex than static theory; conditional on investment opportunities, leverage and returns can be negatively correlated

---

## B. Seminal GMM Methodology (Proximity 4–5)

---

### [Hansen 1982] Large Sample Properties of Generalized Method of Moments Estimators
**Journal/Source**: Econometrica, Vol. 50, No. 4, pp. 1029–1054
**Proximity Score**: 5/5
**Summary**: Hansen's foundational paper introduces and formally establishes the GMM estimator. The paper derives consistency and asymptotic normality for any GMM estimator defined by a set of moment conditions, establishes the optimal weighting matrix (inverse of the long-run variance of the moments), and derives the asymptotic distribution of the J-test statistic for overidentifying restrictions. This paper is the primary methodological reference for any GMM-based estimation procedure — must cite in any paper using GMM or constrained GMM.
**Identification**: GMM; optimal weighting matrix = inverse of long-run variance of moment conditions
**Data**: Theoretical econometrics paper; examples from asset pricing
**Key Result**: GMM estimator consistent and asymptotically normal; J-statistic asymptotically chi-squared with degrees of freedom = number of overidentifying restrictions

---

### [Hansen Singleton 1982] Generalized Instrumental Variables Estimation of Nonlinear Rational Expectations Models
**Journal/Source**: Econometrica, Vol. 50, No. 5, pp. 1269–1286
**Proximity Score**: 5/5
**Summary**: Hansen and Singleton apply GMM to estimate the parameters of a representative-agent asset pricing model via Euler equation moment conditions. This paper bridges Hansen (1982)'s econometric theory with empirical asset pricing and is the most commonly cited applied reference for GMM in finance. The paper demonstrates how instruments (lagged variables) interact with moment conditions to produce overidentified systems — directly analogous to the 10-spread-moment GMM design.
**Identification**: GMM applied to Euler equation moment conditions; instrument set = lagged asset returns and consumption growth
**Data**: US aggregate consumption and asset returns, 1959–1978 (monthly)
**Key Result**: Power utility parameters estimated; utility curvature parameter estimated at 0.97; overidentification restrictions not rejected

---

### [Sargan 1958] The Estimation of Economic Relationships Using Instrumental Variables
**Journal/Source**: Econometrica, Vol. 26, No. 3, pp. 393–415
**Proximity Score**: 4/5
**Summary**: Sargan derives the asymptotic error variance matrix for IV estimators and introduces the overidentification test for the validity of excess instruments — the Sargan test, the precursor to Hansen's J-test. For a constrained GMM paper with 10 moment conditions and fewer structural parameters, the overidentification test is a key model validity check. Cite as the historical foundation of the J-test.
**Identification**: Instrumental variables; overidentification test (Sargan test)
**Data**: Economic time series; theoretical paper
**Key Result**: Sargan test statistic asymptotically chi-squared under null of valid instruments; power properties discussed

---

### [Newey West 1987] A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix
**Journal/Source**: Econometrica, Vol. 55, No. 3, pp. 703–708
**Proximity Score**: 5/5
**Summary**: Newey and West propose the standard HAC (Heteroskedasticity and Autocorrelation Consistent) covariance matrix estimator using a truncated kernel weighting scheme. This estimator is positive semi-definite by construction and is consistent under general conditions. It is the standard choice for the GMM weighting matrix and for long-run variance estimation when computing efficient GMM or testing overidentifying restrictions with time-series data. The Newey-West estimator is the default standard error procedure for constrained GMM with spread moments subject to serial correlation.
**Identification**: HAC covariance matrix estimator; Bartlett kernel with lag truncation
**Data**: Theoretical econometrics paper
**Key Result**: Estimator is positive semi-definite, consistent under heteroskedasticity and autocorrelation; lag truncation grows as O(T^{1/4}) for consistency

---

### [Andrews 1991] Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation
**Journal/Source**: Econometrica, Vol. 59, No. 3, pp. 817–858
**Proximity Score**: 5/5
**Summary**: Andrews derives the asymptotically optimal kernel and bandwidth for HAC covariance matrix estimation, introducing automatic data-dependent bandwidth selection. The paper shows that the commonly used Bartlett kernel is suboptimal and derives the Parzen and QS kernels as efficient alternatives. For optimal weighting matrix construction in constrained GMM, Andrews (1991) is the primary reference for bandwidth selection procedures.
**Identification**: HAC covariance estimation; automatic optimal bandwidth via data-dependent procedures
**Data**: Theoretical econometrics paper
**Key Result**: Quadratic spectral (QS) kernel with MSE-optimal bandwidth is asymptotically efficient; data-dependent bandwidth selection introduced

---

### [Andrews Monahan 1992] An Improved Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimator
**Journal/Source**: Econometrica, Vol. 60, No. 4, pp. 953–966
**Proximity Score**: 4/5
**Summary**: Andrews and Monahan introduce prewhitened HAC estimators, using VAR prewhitening before kernel smoothing to reduce bias in finite samples. The prewhitening step substantially improves confidence interval coverage and reduces over-rejection of t-statistics in practice. Cite when discussing finite-sample behavior of the GMM weighting matrix, particularly if the moment conditions display serial correlation.
**Identification**: Prewhitened kernel HAC estimator; VAR prewhitening + kernel smoothing
**Data**: Monte Carlo simulations; theoretical econometrics paper
**Key Result**: Prewhitening reduces bias substantially; Monte Carlo shows large improvement in confidence interval coverage over standard Newey-West

---

### [Newey McFadden 1994] Large Sample Estimation and Hypothesis Testing
**Journal/Source**: Handbook of Econometrics, Vol. 4, Ch. 36, pp. 2111–2245 (eds. Engle and McFadden)
**Proximity Score**: 4/5
**Summary**: This comprehensive handbook chapter provides the definitive treatment of asymptotic theory for GMM, MLE, and related M-estimators. It covers the asymptotic distribution theory for constrained GMM (delta method for functions of moments), specification tests, and hypothesis testing. Essential reference for establishing the asymptotic theory of constrained GMM estimates — particularly for nonlinear moment conditions and the delta method for functions of structural parameters.
**Identification**: Asymptotic theory for GMM and related M-estimators; delta method for nonlinear moment functions
**Data**: Theoretical econometrics handbook chapter
**Key Result**: Delta method for nonlinear functions of GMM estimates; GMM efficient under optimal weighting; specification tests derived

---

### [Burnside Eichenbaum 1996] Small-Sample Properties of GMM-Based Wald Tests
**Journal/Source**: Journal of Business and Economic Statistics, Vol. 14, No. 3, pp. 294–308
**Proximity Score**: 4/5
**Summary**: Burnside and Eichenbaum assess the finite-sample size properties of GMM-based Wald tests via Monte Carlo simulation. They show that with many moment conditions relative to sample size, GMM Wald tests are severely over-sized, and that the root cause is difficulty in estimating the long-run spectral density matrix. This paper motivates conservative moment selection (not too many moments relative to sample size) and bootstrap inference for GMM in small samples. Directly relevant for justifying the choice of 10 spread moments versus a larger set.
**Identification**: Monte Carlo evaluation of GMM Wald statistics; size distortion analysis
**Data**: Simulated data; US business cycle model
**Key Result**: GMM Wald test rejection rates substantially exceed nominal size with many moments; size distortion worsens with moment count; bootstrap preferred over asymptotic critical values in finite samples

---

## C. Same Method, Different Context — GMM/SMM Methodology in Other Settings (Proximity 3)

---

### [Christiano Eichenbaum Evans 2005] Nominal Rigidities and the Dynamic Effects of a Shock to Monetary Policy
**Journal/Source**: Journal of Political Economy, Vol. 113, No. 1, pp. 1–45
**Proximity Score**: 3/5
**Summary**: Christiano, Eichenbaum, and Evans estimate a New Keynesian DSGE model by matching impulse response functions derived from a VAR — a form of SMM where moments are IRFs. The paper demonstrates how to estimate a structural macro model with many moment conditions (the full IRF vector) using a diagonal weighting matrix. The approach of using 10 spread moments in constrained GMM is methodologically analogous to using 10 IRF values as target moments.
**Identification**: IRF-matching SMM (indirect inference variant); VAR-based moments as targets; diagonal weighting matrix
**Data**: US macro time series, 1959–2001
**Key Result**: Model with moderate nominal rigidities matches observed persistence in output and inflation following monetary shocks; IRF-matching approach widely adopted in macro-finance

---

### [Krusell Smith 1998] Income and Wealth Heterogeneity in the Macroeconomy
**Journal/Source**: Journal of Political Economy, Vol. 106, No. 5, pp. 867–896
**Proximity Score**: 3/5
**Summary**: Krusell and Smith solve and calibrate a heterogeneous-agent macroeconomic model with idiosyncratic income risk. They demonstrate that aggregate dynamics can be approximated using only a few moments of the wealth distribution. The calibration methodology — matching simulated moments of the wealth distribution to their empirical counterparts — is a direct methodological precursor to calibrating a capital supply distribution ν_t using aggregate moment conditions. The "bounded rationality" equilibrium approximation using moment conditions is also relevant.
**Identification**: Calibration/SMM — matches cross-sectional moments of wealth distribution; approximate aggregation via moment truncation
**Data**: PSID household panel; NIPA macro aggregates
**Key Result**: Mean wealth is sufficient to approximate aggregate dynamics; higher moments of wealth distribution matter little for aggregates

---

### [Cagetti De Nardi 2006] Entrepreneurship, Frictions, and Wealth
**Journal/Source**: Journal of Political Economy, Vol. 114, No. 5, pp. 835–870
**Proximity Score**: 3/5
**Summary**: Cagetti and De Nardi estimate a structural model of occupational choice and borrowing constraints by calibrating the model to match the observed wealth distribution for entrepreneurs and workers. The calibration uses a targeted set of distributional moments — quantiles and moments of the firm size and wealth distributions. This paper is a direct methodological precedent for using distributional moments (e.g., distributional features of leverage or spreads) as GMM/SMM targets.
**Identification**: Structural calibration / SMM — match cross-sectional distributional moments of wealth and firm size
**Data**: Survey of Consumer Finances (SCF); NIPA data
**Key Result**: Borrowing constraints critically affect entrepreneurial entry, capital accumulation, and wealth concentration; accidental vs. voluntary bequests matter for aggregate capital

---

### [Nevo 2000] A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand
**Journal/Source**: Journal of Economics and Management Strategy, Vol. 9, No. 4, pp. 513–548
**Proximity Score**: 3/5
**Summary**: Nevo provides a step-by-step guide to implementing BLP-style random coefficients logit demand estimation using GMM. The paper discusses instrument construction, the optimal weighting matrix, contraction mapping convergence, and standard error computation — closely paralleling the implementation choices for constrained GMM with a structural objective function. Useful reference for the numerical implementation aspects of structural GMM.
**Identification**: GMM / BLP nested fixed-point algorithm; instruments = product characteristics of other goods; optimal weighting matrix estimated from moment residuals
**Data**: Ready-to-eat cereal market data; scanner data
**Key Result**: Full implementation walkthrough; random coefficients reduce substitution pattern bias relative to logit

---

### [Koijen Yogo 2019] A Demand System Approach to Asset Pricing
**Journal/Source**: Journal of Political Economy, Vol. 127, No. 4, pp. 1475–1515
**Proximity Score**: 3/5
**Summary**: Koijen and Yogo develop a structural demand system for the US stock market estimated by IV/GMM, using portfolio holdings data as moments. The methodology treats investors as structural agents with demand systems, and estimates demand elasticities via cross-sectional GMM. The paper demonstrates how large cross-sectional GMM systems (many moment conditions from the demand system) can be estimated and tested for overidentification.
**Identification**: IV/GMM structural demand system; cross-sectional moment conditions from portfolio holdings
**Data**: 13F portfolio holdings, CRSP stock market data, 1980–2017
**Key Result**: Demand elasticities are low (near-inelastic) for individual stocks; investor heterogeneity and demand shifts explain substantial stock market volatility

---

### [Albuquerque Hopenhayn 2004] Optimal Lending Contracts and Firm Dynamics
**Journal/Source**: Review of Economic Studies, Vol. 71, No. 2, pp. 285–315
**Proximity Score**: 3/5
**Summary**: Albuquerque and Hopenhayn develop a general equilibrium model of lending under limited liability and imperfect debt enforcement, characterizing optimal dynamic lending contracts. The model generates rich firm size and leverage dynamics consistent with Compustat data. While primarily theoretical, the paper informs the structural model design for optimal debt contracts under distributional assumptions about firm cash flows — a precursor to cash-flow distribution-based models of debt capacity.
**Identification**: Theoretical dynamic programming with limited enforcement; structural characterization of optimal contract as function of firm state
**Data**: Qualitative calibration to firm dynamics facts
**Key Result**: Optimal contract entails history-dependent borrowing constraints; firm growth rate is decreasing in firm age due to binding borrowing constraints

---

## D. Same Context, Different Method — Structural and Empirical Capital Structure and Credit Spreads (Proximity 3)

---

### [Leland 1994] Corporate Debt Value, Bond Covenants, and Optimal Capital Structure
**Journal/Source**: Journal of Finance, Vol. 49, No. 4, pp. 1213–1252
**Proximity Score**: 4/5
**Summary**: Leland derives closed-form formulas for corporate debt value, credit spreads, and optimal leverage when asset value follows a geometric Brownian motion and bankruptcy is endogenous. The model yields explicit expressions for optimal leverage, debt value, and credit spreads as functions of firm risk, taxes, and bankruptcy costs. This is the gold-standard structural model for corporate debt — any GMM estimation targeting credit spreads (as in the 10-spread-moment design) is implicitly tested against Leland's theoretical framework.
**Identification**: Analytical structural model (closed-form); optimal leverage from first-order conditions
**Data**: Calibrated to historical average leverage and credit spreads
**Key Result**: Higher asset volatility, lower taxes, higher bankruptcy costs → lower optimal leverage; model matches average investment-grade credit spreads

---

### [Leland Toft 1996] Optimal Capital Structure, Endogenous Bankruptcy, and the Term Structure of Credit Spreads
**Journal/Source**: Journal of Finance, Vol. 51, No. 3, pp. 987–1019
**Proximity Score**: 4/5
**Summary**: Leland and Toft extend Leland (1994) to allow firms to choose both the amount and maturity of debt, with endogenous bankruptcy. The model produces a full term structure of credit spreads. Importantly, the model simultaneously matches leverage ratios, default rates, recovery rates, and credit spreads — a direct antecedent to using spread moments as GMM overidentifying conditions. Must cite as the theoretical foundation for the spread-moment-matching approach.
**Identification**: Closed-form structural model with endogenous maturity choice; bankruptcy trigger optimized
**Data**: Calibrated to historical default and spread data
**Key Result**: Model closely matches historical average default rates, credit spreads, and recovery values; optimal debt maturity depends on volatility and tax rates

---

### [Merton 1974] On the Pricing of Corporate Debt: The Risk Structure of Interest Rates
**Journal/Source**: Journal of Finance, Vol. 29, No. 2, pp. 449–470
**Proximity Score**: 4/5
**Summary**: Merton applies contingent claims analysis to corporate debt, modeling equity as a call option on firm assets and deriving the credit spread as a function of firm leverage and asset volatility. This is the foundational structural model linking firm fundamentals to debt prices — any model that matches credit spreads to cash flow distributions is nested within or extends the Merton framework. Essential citation in any paper involving structural credit spread estimation.
**Identification**: Closed-form option pricing model; Black-Scholes applied to corporate liabilities
**Data**: Theoretical paper; calibrated to illustrative examples
**Key Result**: Credit spread is an increasing function of leverage and asset volatility; model implies near-zero spreads for short-maturity investment-grade debt (the "credit spread puzzle")

---

### [Collin-Dufresne Goldstein 2001] Do Credit Spreads Reflect Stationary Leverage Ratios?
**Journal/Source**: Journal of Finance, Vol. 56, No. 5, pp. 1929–1957
**Proximity Score**: 3/5
**Summary**: Collin-Dufresne and Goldstein propose a structural credit model where firms adjust debt levels in response to asset value changes, generating mean-reverting leverage. This produces credit spreads larger for low-leverage firms and a term structure consistent with empirical evidence. The mean-reversion in leverage implies a stationary distribution for leverage ratios — precisely the cross-sectional distributional setting relevant to estimating ν_t. Relevant as a structural benchmark for the cross-sectional distribution of leverage and spreads.
**Identification**: Structural model with mean-reverting leverage policy; closed-form credit spread formula
**Data**: Calibrated to investment-grade corporate bond spreads
**Key Result**: Stationary leverage policy model generates larger spreads for low-leverage firms; term structure of credit spreads can be upward-sloping for speculative-grade debt

---

### [Collin-Dufresne Goldstein Martin 2001] The Determinants of Credit Spread Changes
**Journal/Source**: Journal of Finance, Vol. 56, No. 6, pp. 2177–2207
**Proximity Score**: 3/5
**Summary**: Collin-Dufresne, Goldstein, and Martin investigate what drives monthly credit spread changes using panel regression on dealer quotes for industrial bonds. Structural model variables (leverage, volatility, interest rate level) explain only 25% of variation; residuals are highly cross-correlated and driven by a single common factor. This paper motivates using spread levels (not changes) as GMM moments to avoid the "credit spread puzzle," and highlights the supply-side capital factors driving spreads orthogonal to structural firm variables.
**Identification**: Panel OLS regression of credit spread changes on Merton-model variables plus controls; PCA of residuals
**Data**: Dealer quotes on industrial corporate bonds, 1988–1997
**Key Result**: Structural model variables explain only 25% of monthly spread changes; large unexplained common factor suggests supply/demand or liquidity effects

---

### [Whited Zhao 2021] The Misallocation of Finance
**Journal/Source**: Journal of Finance, Vol. 76, No. 5, pp. 2359–2407
**Proximity Score**: 3/5
**Summary**: Whited and Zhao extend production-based misallocation measurement to the liabilities side of the balance sheet, estimating real losses from cross-sectional misallocation of debt and equity in the US and China. The paper uses structural estimation to quantify misallocation in capital markets — a direct application of matching distributional moments of financing variables. Methodologically related to matching distributional features of capital supply and firm leverage.
**Identification**: Structural production-based framework; GMM/calibration to match distributional moments of financing variables
**Data**: US and Chinese manufacturing firm data (Compustat equivalent)
**Key Result**: Substantial misallocation of debt and equity in China; US misallocation smaller; misallocation causes real output losses

---

## E. Partial Identification and Constrained GMM — Methods Papers (Proximity 3–4)

---

### [Chernozhukov Lee Rosen 2013] Intersection Bounds: Estimation and Inference
**Journal/Source**: Econometrica, Vol. 81, No. 2, pp. 667–737
**Proximity Score**: 4/5
**Summary**: Chernozhukov, Lee, and Rosen develop methods for inference on identified sets defined as infima or suprema of parametric functions — i.e., intersection bounds. They provide median-bias-corrected estimators and valid confidence sets for partially identified parameters defined by moment inequality conditions. Relevant for any GMM design with more moments than parameters (overidentification): if the model is misspecified, some moments may be violated and the identified "set" for θ becomes an intersection of moment-inequality-defined regions.
**Identification**: Intersection bounds; median-bias-corrected estimation; bootstrap confidence sets for identified sets
**Data**: Theoretical econometrics paper; applied illustration
**Key Result**: Standard analog estimators of intersection bounds are severely biased downward (underestimate identified set); bias-corrected estimator and confidence procedure provided

---

### [Andrews Shi 2013] Inference Based on Conditional Moment Inequalities
**Journal/Source**: Econometrica, Vol. 81, No. 2, pp. 609–666
**Proximity Score**: 4/5
**Summary**: Andrews and Shi propose a Cramer-von Mises / Kolmogorov-Smirnov-based confidence set construction for models defined by conditional moment inequalities. They transform conditional moment inequalities into unconditional ones via instrument functions without losing identification power. Critical values obtained by generalized moment selection (GMS). This paper provides the formal econometric basis for inference when some GMM moment conditions are inequalities rather than equalities — relevant if the structural model only restricts moments from one side.
**Identification**: Conditional moment inequality inference; GMS critical values; IV-function transformation
**Data**: Theoretical econometrics paper; applied to partial identification in binary choice
**Key Result**: Confidence sets control coverage uniformly over large classes of DGPs; GMS outperforms less sophisticated approaches in simulations

---

### [Kaido Molinari Stoye 2019] Confidence Intervals for Projections of Partially Identified Parameters
**Journal/Source**: Econometrica, Vol. 87, No. 4, pp. 1397–1432
**Proximity Score**: 3/5
**Summary**: Kaido, Molinari, and Stoye develop bootstrap-based calibrated projection procedures to build confidence intervals for single components of a partially identified parameter vector in moment inequality models. They show that standard procedures for full parameter confidence sets are overly conservative for projections (individual components). Relevant for any GMM paper discussing the identified region for structural parameters under overidentification.
**Identification**: Bootstrap calibrated projection for moment inequality models; controls coverage uniformly
**Data**: Theoretical econometrics paper
**Key Result**: Calibrated projection confidence intervals are tighter than standard CS projections while controlling coverage uniformly; substantial power gains

---

### [Andrews Guggenberger 2019] Identification- and Singularity-Robust Inference for Moment Condition Models
**Journal/Source**: Quantitative Economics, Vol. 10, No. 4, pp. 1703–1746
**Proximity Score**: 3/5
**Summary**: Andrews and Guggenberger develop identification-robust and singularity-robust tests for moment condition models (GMM) under potential weak identification. They introduce SR-CQLR and SR-AR tests that maintain correct size under weak, partial, or failure of identification. Relevant for a constrained GMM with 10 moments: if some structural parameters are weakly identified from the spread moments, standard GMM Wald inference is unreliable and identification-robust procedures are needed.
**Identification**: Identification- and singularity-robust conditional quasi-likelihood ratio and Anderson-Rubin tests
**Data**: Theoretical econometrics paper
**Key Result**: SR-CQLR test has correct asymptotic size under weak identification; nearly as powerful as standard Wald test under strong identification

---

### [Andrews 1999] Consistent Moment Selection Procedures for GMM Estimation
**Journal/Source**: Econometrica, Vol. 67, No. 3, pp. 543–564
**Proximity Score**: 3/5
**Summary**: Andrews develops information-criterion-based moment selection procedures for GMM, analogous to AIC/BIC for model selection. The procedure selects the moment set that minimizes a modified J-statistic criterion, trading off model fit (J-statistic) against parsimony (number of moments). For a constrained GMM with 10 candidate spread moments, this framework formalizes the tradeoff between adding more moments (efficiency gain) versus finite-sample size distortion (as shown by Burnside-Eichenbaum).
**Identification**: Moment selection via information criterion applied to GMM J-statistic
**Data**: Theoretical econometrics paper; Monte Carlo simulations
**Key Result**: Consistent model and moment selection via modified J-statistic; procedure selects correct moment set with probability approaching 1

---

## F. Theoretical Foundations — Capital Structure Theory (Proximity 1–2)

---

### [DeMarzo Fishman 2007] Optimal Long-Term Financial Contracting
**Journal/Source**: Review of Financial Studies, Vol. 20, No. 6, pp. 2079–2128
**Proximity Score**: 2/5
**Summary**: DeMarzo and Fishman derive long-term debt, a line of credit, and equity as optimal securities in a dynamic agency model with cash diversion. The paper shows that optimal debt-equity ratios are history-dependent while debt and credit line terms are independent of financing amount. Relevant as a theoretical foundation for structural models of optimal debt contracts where the firm-lender matching is the fundamental primitive.
**Identification**: Dynamic mechanism design; optimal contracting under hidden action
**Data**: Theoretical model
**Key Result**: Optimal contract implemented by combination of long-term debt, credit line, and equity; history-dependence of capital structure arises endogenously

---

### [Brunnermeier Sannikov 2014] A Macroeconomic Model with a Financial Sector
**Journal/Source**: American Economic Review, Vol. 104, No. 2, pp. 379–421
**Proximity Score**: 2/5
**Summary**: Brunnermeier and Sannikov develop a continuous-time macro model with financial intermediaries where amplification arises through endogenous leverage. The model produces the "volatility paradox" — endogenous risk persists at crisis even for very low exogenous risk. Relevant as a theoretical motivation for why the capital supply distribution ν_t has time-varying moments linked to financial sector conditions rather than just firm fundamentals.
**Identification**: Continuous-time macro-finance model; analytical characterization of equilibrium dynamics
**Data**: Calibrated to qualitative properties of financial crises
**Key Result**: Financial intermediary leverage cycles generate nonlinear amplification; volatility paradox: endogenous systemic risk does not vanish with low exogenous risk

---

### [Gomes 2001] Financing Investment
**Journal/Source**: American Economic Review, Vol. 91, No. 5, pp. 1263–1285
**Proximity Score**: 2/5
**Summary**: Gomes develops a structural model of investment with financing frictions and shows that cash flow sensitivity of investment can arise even without financial constraints, due to measurement error in Q. The paper demonstrates how structural modeling disciplines the interpretation of reduced-form investment regressions. Relevant as background for Euler-equation-based GMM approaches to capital structure.
**Identification**: Structural dynamic investment model with financing costs; analytical characterization of Euler equations
**Data**: Compustat manufacturing firms; simulation experiments
**Key Result**: Cash flow sensitivity of investment can appear even in frictionless model due to Q measurement error; structural model necessary to separate financial friction effects

---

### [Strebulaev 2007] Do Tests of Capital Structure Theory Mean What They Say?
**Journal/Source**: Journal of Finance, Vol. 62, No. 4, pp. 1747–1787
**Proximity Score**: 3/5
**Summary**: Strebulaev simulates a calibrated dynamic trade-off model where firms adjust leverage infrequently, and shows that standard cross-sectional OLS regressions of leverage on firm characteristics would find the wrong signs even in a world where trade-off theory holds exactly. The paper demonstrates why structural estimation with simulation is necessary — reduced-form regressions on dynamic models can be systematically misleading. Key motivation for SMM-based structural estimation over OLS.
**Identification**: Structural model simulation; comparison of model-implied cross-sectional patterns to reduced-form regression estimates
**Data**: Simulated from calibrated structural model; compared to Compustat patterns
**Key Result**: Dynamic adjustment frictions cause leverage-profitability relationship to flip sign in cross-section even when trade-off theory is correctly specified; simulation necessary to interpret data

---

### [Almeida Campello Weisbach 2004] The Cash Flow Sensitivity of Cash
**Journal/Source**: Journal of Finance, Vol. 59, No. 4, pp. 1777–1804
**Proximity Score**: 2/5
**Summary**: Almeida, Campello, and Weisbach use GMM to test whether constrained firms show positive cash flow sensitivity of cash (propensity to save cash out of cash flows). This is one of the most prominent applied uses of GMM in corporate finance to test a structural hypothesis derived from a liquidity demand model. Relevant as a methodological precedent for testing structural predictions via GMM moment conditions in a corporate finance panel.
**Identification**: GMM panel estimation with lagged instruments; test of cash flow sensitivity of cash
**Data**: Compustat manufacturing panel, 1971–2000
**Key Result**: Constrained firms show positive and significant cash flow sensitivity of cash; unconstrained firms do not; constraint classification using Kaplan-Zingales and similar indices

---

## G. Data and Measurement (Proximity 2–3)

---

### [Griliches Hausman 1986] Errors in Variables in Panel Data
**Journal/Source**: Journal of Econometrics, Vol. 31, No. 1, pp. 93–118
**Proximity Score**: 2/5
**Summary**: Griliches and Hausman show that in panel data settings, errors-in-variables models are identifiable and estimable without external instruments, using within-group and between-group variation. This foreshadows the use of higher-order GMM moments (Erickson-Whited) and motivates attention to measurement error in structural estimation when firm-level cash flows or spreads are measured with noise.
**Identification**: Within/between estimator comparison under errors-in-variables; moment conditions from panel structure
**Data**: Panel data; empirical applications to returns to education
**Key Result**: Within estimator more biased by measurement error than between estimator; can bound and estimate measurement error variance without external instruments

---

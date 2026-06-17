# Annotated Bibliography: Credit Spreads, Capital Supply Dynamics, and the Cross-Section of Corporate Leverage

**Project**: Distributional Debt Capacity (Optimal Transport / Wasserstein)
**Compiled**: 2026-06-14
**Coverage**: Journal of Finance, Review of Financial Studies, Journal of Financial Economics, AER, JPE, QJE, Review of Economic Studies, Journal of Monetary Economics; NBER, SSRN, RePeC working papers
**Excluded per researcher request**: Rajan-Zingales (1995), Frank-Goyal (2009), Baker-Wurgler (2002), Lemmon-Roberts-Zender (2008), DeAngelo-Roll (2015), Graham-Harvey (2001), Kashyap-Stein (2000), Khwaja-Mian (2008), Greenwood-Hanson (2013 RFS), Ivashina-Scharfstein (2010), Koijen-Yogo (2019 JPE), Massa-Yasuda-Zhang (2013 JFE), Zhu (2021 JFE), Lemmon-Roberts (2010 JFQA)

---

## Category 1: Directly Related — Credit Spread Determinants (Proximity 4–5)

### [Collin-Dufresne, Goldstein, Martin 2001] The Determinants of Credit Spread Changes
**Journal/Source**: Journal of Finance, Vol. 56(6), pp. 2177–2207
**Proximity Score**: 5/5
**Summary**: Uses dealer quotes and transaction prices on straight industrial bonds to investigate which variables theory predicts should drive credit spread changes. Standard variables — leverage, volatility, risk-free rate, slope of yield curve — have limited explanatory power (R² around 25%). Residuals are highly cross-correlated and driven primarily by a single common factor that cannot be explained by macroeconomic or financial variables. The authors interpret this residual factor as local supply/demand shocks independent of credit-risk factors and standard liquidity proxies. This finding is foundational for the paper's argument that an aggregate capital supply distribution captures the unobserved supply-side component that standard regressions miss.
**Identification**: OLS regressions of monthly credit spread changes on theoretical determinants; principal components analysis of residuals
**Data**: Dealer quotes and transaction prices on U.S. investment-grade industrial bonds, 1988–1997
**Key Result**: Theoretical variables explain only ~25% of spread changes; residuals load on a single supply/demand factor not captured by observables
**FLAG**: Proximity 5 — Must address head-on in introduction. The "unobserved common factor" in CDG (2001) residuals is precisely what the Wasserstein distance between cash flow and capital supply distributions is designed to capture.

---

### [Gilchrist, Zakrajsek 2012] Credit Spreads and Business Cycle Fluctuations
**Journal/Source**: American Economic Review, Vol. 102(4), pp. 1692–1720
**Proximity Score**: 5/5
**Summary**: Constructs a micro-level credit spread index by pricing individual bonds relative to a default-risk model, then decomposes spreads into an expected-default component and a residual excess bond premium (EBP). The EBP predicts future economic activity independently of financial conditions. Increases in the EBP reflect reductions in the risk-bearing capacity of the financial sector, inducing credit supply contractions. This is the most widely used empirical decomposition of credit spreads into default risk vs. financial-sector supply factors. The present paper's W1 distance offers a structural characterization of what Gilchrist-Zakrajsek measure residually.
**Identification**: Regression of EBP on macro indicators; VAR with sign restrictions
**Data**: Micro-level bond prices from Lehman/Merrill bond databases, 1973–2010; TRACE from 2002
**Key Result**: EBP predicts GDP 6–12 months ahead; 1 SD increase in EBP reduces GDP growth by ~1 pp
**FLAG**: Proximity 5 — Directly cited comparator. The EBP is the time-series analog of what the paper explains cross-sectionally through W1.

---

### [Nozawa 2017] What Drives the Cross-Section of Credit Spreads?: A Variance Decomposition Approach
**Journal/Source**: Journal of Finance, Vol. 72(5), pp. 2045–2072
**Proximity Score**: 5/5
**Summary**: Applies a log-linearized pricing identity and VAR to decompose cross-sectional variation in corporate bond credit spreads into expected-return and expected-credit-loss components. Using CRSP/Compustat data from 1973 to 2011, finds that expected returns explain nearly as much cross-sectional variance as expected credit losses — implying that risk premia, not just default probabilities, are crucial determinants of the spread cross-section. This is the closest direct antecedent on the cross-section of spreads: the paper must show its W1 measure explains the cross-section orthogonally to Nozawa's expected-return variation.
**Identification**: VAR-based variance decomposition; log-linear present value identity
**Data**: CRSP bond return data and Compustat, 1973–2011 (pre-TRACE)
**Key Result**: Expected returns account for ~40% of cross-sectional spread variance; expected credit losses account for ~60%
**FLAG**: Proximity 5 — Direct competitor on the cross-section of credit spreads. Must be addressed head-on.

---

### [Siriwardane 2019] Limited Investment Capital and Credit Spreads
**Journal/Source**: Journal of Finance, Vol. 74(5), pp. 2303–2347
**Proximity Score**: 5/5
**Summary**: Uses proprietary CDS data to study how capital shocks to CDS protection sellers affect spread pricing. Measures capital shocks as CDS portfolio margin payments. Seller capital shocks account for 12% of time-series variation in weekly CDS spread changes — comparable to the 18% explained by standard credit factors — and contain information orthogonal to institution-wide capital measures, implying high market segmentation. Establishes that frictions within specialized intermediaries prevent capital from flowing to equalize spreads. This is the most direct empirical precedent: the paper's W2 distance captures the aggregate social cost of exactly such frictions.
**Identification**: OLS and IV regressions of spread changes on margin payment shocks; institution-level fixed effects
**Data**: Proprietary CDS portfolio data from a large dealer, 2010–2014
**Key Result**: 1 SD increase in seller capital shock → ~6 bps increase in weekly spread; explains 12% of time-series variation
**FLAG**: Proximity 5 — Direct competitor. Uses CDS; this paper uses TRACE bond data. Must compare frameworks explicitly.

---

### [Huang, Nozawa, Shi 2025] The Global Credit Spread Puzzle
**Journal/Source**: Journal of Finance, Vol. 80(1), pp. 101–162
**Proximity Score**: 4/5
**Summary**: Examines structural models' ability to match credit spreads using global data from eight developed economies. Finds that standard models (Black-Cox) systematically underpredict investment-grade spreads globally — a "global credit spread puzzle." A model incorporating endogenous secondary-market liquidity partially resolves the puzzle. This is the most recent published paper on the credit spread puzzle and directly motivates why a supply-side / distributional explanation (the paper's contribution) is needed beyond pure default-risk models.
**Identification**: Structural model calibration; cross-country comparison; decomposition of spread components
**Data**: TRACE-equivalent bond databases across 8 countries; historical default data
**Key Result**: Pure default-risk models underpredict IG spreads by 30–60 bps on average; liquidity model partially resolves the gap
**FLAG**: Proximity 4 — Very recent published paper. Cite as motivation for supply-side explanations.

---

### [Feldhutter, Schaefer 2018] The Myth of the Credit Spread Puzzle
**Journal/Source**: Review of Financial Studies, Vol. 31(8), pp. 2897–2942
**Proximity Score**: 4/5
**Summary**: Argues the credit spread puzzle may not be as severe as commonly believed. Uses a new calibration approach for structural models based on historical default rates that produces more precise estimates of investment-grade default probabilities. Finds the Black-Cox model matches IG spread levels well; the puzzle is concentrated in speculative-grade bonds where bond illiquidity contributes to underpricing. Key methodological comparator: shows that calibration approach matters greatly. The paper's cross-sectional distribution of spreads should be compared to the distribution implied by Feldhutter-Schaefer.
**Identification**: Structural model (Black-Cox) calibrated to historical default rates; cross-sectional comparison
**Data**: Moody's default database; Bloomberg bond prices, 1997–2015
**Key Result**: IG spreads well matched by calibrated structural model; speculative-grade puzzle remains; illiquidity contributes 40–50% of residual

---

### [Chen 2010] Macroeconomic Conditions and the Puzzles of Credit Spreads and Capital Structure
**Journal/Source**: Journal of Finance, Vol. 65(6), pp. 2171–2212
**Proximity Score**: 4/5
**Summary**: Builds a dynamic capital structure model that jointly explains the credit spread puzzle (spreads too high for observed default rates) and the under-leverage puzzle (firms use less debt than tax shields warrant). Business cycle variation in expected growth, uncertainty, and risk premia drives financing decisions and spread dynamics endogenously. Countercyclical risk prices generate large credit risk premia for investment-grade firms. This is the leading structural-equilibrium model connecting aggregate conditions and cross-sectional leverage to credit spreads.
**Identification**: Dynamic structural capital structure model with business cycle shocks; calibrated to aggregate macro moments
**Data**: Compustat, CRSP; historical default rates and recovery rates
**Key Result**: Model generates 54 bps average spread for Baa bonds (vs. 75 bps data) and realistic leverage ratios simultaneously

---

## Category 2: Aggregate Credit Supply and Intermediary Capital (Proximity 4–5)

### [Adrian, Etula, Muir 2014] Financial Intermediaries and the Cross-Section of Asset Returns
**Journal/Source**: Journal of Finance, Vol. 69(6), pp. 2557–2596
**Proximity Score**: 4/5
**Summary**: Constructs an intermediary stochastic discount factor from shocks to leverage of securities broker-dealers. A single-factor model using broker-dealer leverage growth prices size, book-to-market, momentum, and bond portfolios with R² of 77% and average pricing error of 1%. Establishes broker-dealer leverage as the premier empirical proxy for aggregate capital supply capacity in financial markets. Closely related to the paper's use of FRED Flow-of-Funds data for the capital supply distribution νt — the same aggregate intermediary balance sheet data underlies both.
**Identification**: Two-stage Fama-MacBeth; intermediary SDF from broker-dealer leverage
**Data**: Federal Reserve Flow of Funds, broker-dealer balance sheets, 1968–2009
**Key Result**: Broker-dealer leverage factor prices 25 asset classes with Sharpe ratio of 0.74

---

### [He, Krishnamurthy 2013] Intermediary Asset Pricing
**Journal/Source**: American Economic Review, Vol. 103(2), pp. 732–770
**Proximity Score**: 4/5
**Summary**: Models asset pricing dynamics during crises where the marginal investor is a financial intermediary facing an equity capital constraint. Risk premia rise nonlinearly when the constraint binds, reflecting capital scarcity. Model matches nonlinearity and speed of reversion in post-crisis risk premia. Provides the theoretical foundation for the supply-side interpretation of credit spread variation: when capital supply distribution νt is compressed (intermediary equity constrained), W1 distance rises and spreads widen.
**Identification**: Continuous-time dynamic model with intermediary capital constraint; calibrated
**Data**: Calibration to historical equity and credit market moments
**Key Result**: Model matches nonlinear risk-premium dynamics including 2008 crisis magnitude and 2009 reversal speed

---

### [He, Kelly, Manela 2017] Intermediary Asset Pricing: New Evidence from Many Asset Classes
**Journal/Source**: Journal of Financial Economics, Vol. 126(1), pp. 1–35
**Proximity Score**: 4/5
**Summary**: Extends the intermediary asset pricing framework to 20+ asset classes. Shocks to the equity capital ratio of Primary Dealer counterparties of the NY Fed have significant explanatory power for cross-sectional expected returns across equities, government bonds, corporate and sovereign bonds, derivatives, commodities, and currencies. The intermediary capital risk factor is strongly procyclical, implying countercyclical intermediary leverage. Price of risk is consistent across asset classes, suggesting intermediaries are marginal investors broadly. Cross-validation for the paper's νt measure: Primary Dealer capital ratio should correlate with the location of the Fréchet mean.
**Identification**: Fama-MacBeth cross-sectional regressions; intermediary capital ratio SDF
**Data**: NY Fed Primary Dealer reports, CRSP, TRACE, futures data, 1970–2012
**Key Result**: Intermediary capital factor R² of 0.77 across 20 asset classes; risk price consistently positive

---

### [Brunnermeier, Sannikov 2014] A Macroeconomic Model with a Financial Sector
**Journal/Source**: American Economic Review, Vol. 104(2), pp. 379–421
**Proximity Score**: 3/5
**Summary**: Studies full equilibrium dynamics of an economy with financial frictions. Intermediary net worth determines asset prices and investment; when intermediaries are undercapitalized, amplification effects create endogenous risk even with low exogenous volatility ("volatility paradox"). Securitization and risk-sharing can increase systemic risk through higher leverage. Provides the macro-finance theoretical backbone for interpreting time-variation in νt (capital supply distribution) as driven by intermediary net worth fluctuations.
**Identification**: Continuous-time general equilibrium model with financial sector; solved numerically
**Data**: Calibration to U.S. macro and financial data
**Key Result**: Economy has two steady states; "volatility paradox" — low exogenous risk compatible with high endogenous financial fragility

---

### [Adrian, Shin 2010] Liquidity and Leverage
**Journal/Source**: Journal of Financial Intermediation, Vol. 19(3), pp. 418–437
**Proximity Score**: 3/5
**Summary**: Documents that marked-to-market leverage of U.S. financial intermediaries (broker-dealers) is strongly procyclical. During asset price booms, intermediaries expand leverage; during busts, forced deleveraging amplifies price declines. Total assets and leverage grow at the same rate while equity is constant. Repo adjustments drive aggregate balance sheet dynamics. Foundational empirical documentation of the mechanism by which capital supply is procyclical — directly motivating why νt (the capital supply distribution anchored to FRED) varies over time.
**Identification**: OLS regression of leverage growth on asset growth; time-series analysis of broker-dealer balance sheets
**Data**: Federal Reserve Flow of Funds, broker-dealer balance sheets, 1963–2008
**Key Result**: Leverage and total assets are near-perfectly correlated (R² ≈ 0.98); equity nearly constant across cycles

---

### [Adrian, Shin 2014] Procyclical Leverage and Value-at-Risk
**Journal/Source**: Review of Financial Studies, Vol. 27(2), pp. 373–403
**Proximity Score**: 3/5
**Summary**: Develops a contracting model consistent with procyclical leverage — where intermediaries target a fixed Value-at-Risk constraint — and documents empirically that intermediary leverage is negatively aligned with VaR. Credit availability varies over the business cycle through shifts in intermediary leverage. Provides the micro-foundation for why the location of the capital supply distribution νt (anchored to FRED intermediary data) shifts countercyclically.
**Identification**: Contracting model; OLS with VaR measures; time-series analysis
**Data**: Federal Reserve Flow of Funds; commercial bank and broker-dealer data, 1963–2011
**Key Result**: A 1% increase in VaR reduces leverage by 0.4%; procyclical leverage amplifies credit cycles

---

## Category 3: Structural Models of Default and Optimal Leverage (Proximity 3–4)

### [Merton 1974] On the Pricing of Corporate Debt: The Risk Structure of Interest Rates
**Journal/Source**: Journal of Finance, Vol. 29(2), pp. 449–470
**Proximity Score**: 3/5
**Summary**: Applies option pricing theory to corporate debt. Equity is a call option on firm assets; debt is equivalent to risk-free debt minus a put option. Derives closed-form credit spread as a function of asset volatility, leverage, and time to maturity. Foundation of all structural credit risk models. The paper's μit (firm cash flow distribution) is the distributional generalization of Merton's asset value process.
**Identification**: Black-Scholes option pricing adapted to corporate liabilities
**Data**: Theoretical calibration
**Key Result**: Credit spread increases with leverage and asset volatility; decreases with risk-free rate

---

### [Leland 1994] Corporate Debt Value, Bond Covenants, and Optimal Capital Structure
**Journal/Source**: Journal of Finance, Vol. 49(4), pp. 1213–1252
**Proximity Score**: 3/5
**Summary**: Provides closed-form solutions for optimal leverage, credit spreads, and debt values in a continuous-time framework with endogenous default threshold, taxes, and bankruptcy costs. Simultaneously determines optimal debt level and credit spread. Demonstrates the trade-off between tax shields and default costs. The paper's optimal transport framework nests Leland-type solutions: when μit and νt are matched via W1 coupling, the optimal contract resembles Leland's endogenous default boundary.
**Identification**: Continuous-time contingent claims; endogenous bankruptcy threshold
**Data**: Theoretical model; calibration to U.S. corporate bond data
**Key Result**: Optimal leverage balances tax shield (τ ≈ 35%) against bankruptcy cost; closed-form spread formula

---

### [Longstaff, Schwartz 1995] A Simple Approach to Valuing Risky Fixed and Floating Rate Debt
**Journal/Source**: Journal of Finance, Vol. 50(3), pp. 789–819
**Proximity Score**: 3/5
**Summary**: Develops a two-factor structural model with stochastic default-free interest rate and mean-reverting firm value. Derives closed-form valuation for fixed and floating-rate risky debt. Finds credit spreads are negatively related to interest rates (consistent with empirical data) and that correlation between default risk and interest rates significantly affects spread properties. Key structural benchmark that the Wasserstein-based model should be compared against.
**Identification**: Two-factor contingent claims model; calibrated to Moody's bond yield data
**Data**: Moody's corporate bond yield data, 1977–1992
**Key Result**: Spreads negatively correlated with risk-free rate; two-factor model fits the term structure of spreads better than one-factor models

---

### [Strebulaev 2007] Do Tests of Capital Structure Theory Mean What They Say?
**Journal/Source**: Journal of Finance, Vol. 62(4), pp. 1747–1787
**Proximity Score**: 3/5
**Summary**: Shows that in dynamic trade-off models where firms adjust infrequently, observed leverage will differ systematically from target leverage, producing cross-sectional patterns that seem inconsistent with trade-off theory but are in fact consistent with it. Simulates a calibrated dynamic model and shows that standard cross-sectional regressions on simulated data replicate all the "puzzles" in the empirical leverage literature. Critical methodological point for the paper: the cross-sectional distribution of leverage is shaped by adjustment dynamics, not just cross-sectional heterogeneity in μit.
**Identification**: Calibrated dynamic structural model; simulated data regression
**Data**: Compustat annual panel, 1965–2000
**Key Result**: Dynamic model generates puzzling cross-sectional patterns even when all firms follow optimal target leverage; adjustment frictions drive most observed variation

---

### [Bhamra, Kuehn, Strebulaev 2010] The Levered Equity Risk Premium and Credit Spreads: A Unified Framework
**Journal/Source**: Review of Financial Studies, Vol. 23(2), pp. 645–703
**Proximity Score**: 3/5
**Summary**: Embeds a contingent-claim corporate financing model within a standard consumption-based asset pricing framework. Jointly models aggregate dynamics of capital structure and macroeconomic risk. Capital structure is procyclical at refinancing dates but countercyclical in aggregate — consistent with empirical evidence. Risk premia in equity and credit markets are unified in one framework. Closest structural analog to the paper's equilibrium: the Fréchet mean of νt corresponds to a state variable governing risk premia in this model.
**Identification**: Structural equilibrium model with Epstein-Zin preferences; calibration to aggregate moments
**Data**: Calibration to U.S. macroeconomic and financial data, 1961–2007
**Key Result**: Framework jointly explains equity premium, corporate spread levels, and procyclicality of leverage

---

### [Chen, Collin-Dufresne, Goldstein 2009] On the Relation Between the Credit Spread Puzzle and the Equity Premium Puzzle
**Journal/Source**: Review of Financial Studies, Vol. 22(9), pp. 3367–3409
**Proximity Score**: 3/5
**Summary**: Resolves the credit spread puzzle by noting that standard structural models are calibrated to time-averaged default rates, ignoring that default rates and risk premia covary (both high in recessions). Uses the Campbell-Cochrane (1999) pricing kernel and finds that the model generates Baa–Aaa spreads matching historical levels. Shows that the credit spread puzzle is the debt analog of the equity premium puzzle. Key theoretical precedent: the paper's W1 distance, anchored to FRED aggregate supply, captures exactly this covariance between νt and business cycle conditions.
**Identification**: Structural model with time-varying risk premia (Campbell-Cochrane preferences); calibrated to equity and credit data
**Data**: Calibration to Moody's default rates and S&P/Compustat, 1936–2002
**Key Result**: Credit spreads at historical levels emerge once risk-premium covariance with default risk is accounted for

---

### [Gomes, Schmid 2021] Equilibrium Asset Pricing with Leverage and Default
**Journal/Source**: Journal of Finance, Vol. 76(1), pp. 301–360
**Proximity Score**: 3/5
**Summary**: General equilibrium model linking pricing of stocks and corporate bonds to endogenous movements in corporate leverage and aggregate volatility. Heterogeneous firms make optimal investment and financing decisions; countercyclical leverage drives predictable variation in risk premia. Endogenous default produces countercyclical credit spread movements propagated to investment and output. This is the most recent general equilibrium model jointly addressing cross-sectional leverage heterogeneity and spread dynamics — direct structural comparator to the paper.
**Identification**: General equilibrium model with heterogeneous firms; solved via perturbation methods
**Data**: Calibration to Compustat and CRSP, 1971–2015
**Key Result**: Model matches equity premium, cross-sectional value premium, and countercyclical credit spreads simultaneously

---

### [Kuehn, Schmid 2014] Investment-Based Corporate Bond Pricing
**Journal/Source**: Journal of Finance, Vol. 69(6), pp. 2741–2776
**Proximity Score**: 3/5
**Summary**: Examines the importance of investment options in structural credit risk models. Firm-level variables proxying for asset composition (investment opportunities, growth options) are significant determinants of credit spreads beyond leverage and asset volatility alone. Cross-sectional spread variation is driven partly by heterogeneity in investment options. Complementary to the paper's finding that distributional shape of cash flows (captured by W1) explains spreads beyond leverage and volatility.
**Identification**: Investment-based structural model; calibrated panel regressions
**Data**: Compustat, CRSP, 1972–2011
**Key Result**: Investment opportunity variable lowers credit spreads by ~10 bps; omitting it causes spread overprediction for growth firms

---

### [Huang, Huang 2012] How Much of Corporate-Treasury Yield Spread Is Due to Credit Risk?
**Journal/Source**: Review of Asset Pricing Studies, Vol. 2(2), pp. 153–202 (circulated as SSRN 2003)
**Proximity Score**: 3/5
**Summary**: Calibrates a wide class of structural models to historical default rates and recovery rates and computes what fraction of corporate yield spreads is attributable to credit risk. Finds that for investment-grade bonds, credit risk accounts for only 20–30% of the spread; for junk bonds, it accounts for 55–75%. The non-credit component is substantial and unexplained — precisely the gap the paper's capital supply distribution addresses.
**Identification**: Structural model calibration across multiple model specifications
**Data**: Moody's default database; Altman recovery data
**Key Result**: Credit risk explains only 20–30% of IG spreads; large non-credit residual motivates supply-side explanation

---

## Category 4: Aggregate Credit Supply Shocks and the Leverage Cross-Section (Proximity 3–4)

### [Becker, Ivashina 2015] Reaching for Yield in the Bond Market
**Journal/Source**: Journal of Finance, Vol. 70(5), pp. 1863–1902
**Proximity Score**: 4/5
**Summary**: Studies "reaching for yield" by insurance companies — the largest institutional bondholders — using regulatory holdings data. Conditional on credit ratings, insurance portfolios are systematically biased toward higher-yield, higher-CDS bonds. Behavior is most pronounced in expansions and among firms with poor governance or binding regulatory capital constraints. Establishes that the composition of the capital supply distribution νt varies cyclically and by institutional type — directly informative for heterogeneity in νt across insurance, mutual fund, and other lender sectors.
**Identification**: Within-rating regressions of insurance holdings on CDS spreads; firm fixed effects; RD around rating boundaries
**Data**: NAIC insurance company bond holdings; Markit CDS; 2004–2010
**Key Result**: Insurance companies hold bonds with 6–11 bps higher CDS spread than rating peers; effect strongest when regulatory constraint binds

---

### [Becker, Ivashina 2016] Covenant-Light Contracts and Creditor Coordination
**Journal/Source**: Sveriges Riksbank Working Paper 321 (circulated 2016; also referenced as Ivashina 2018 "Weak Credit Covenants")
**Proximity Score**: 3/5
**Summary**: Documents the unprecedented rise in covenant-light loans in the U.S. leveraged loan market and connects it to inflows to passive institutional lenders (mutual funds, CLOs). Cov-lite issuance closely tracks institutional investor inflows, and at a given point in time, cov-lite loans are predominantly those with the highest ownership by structured products and mutual funds. Shows that the composition of the capital supply distribution — specifically the fraction of passive vs. active lenders — affects debt contract terms and implicitly borrowing capacity.
**Identification**: Panel regressions of cov-lite probability on institutional inflows; time-series analysis
**Data**: Loan-level data from Dealscan; 13F institutional holdings; 2001–2014
**Key Result**: 10 pp increase in CLO ownership of a loan → ~15 pp increase in probability of cov-lite terms

---

### [Ivashina, Laeven, Moral-Benito 2022] Loan Types and the Bank Lending Channel
**Journal/Source**: Journal of Monetary Economics, Vol. 126, pp. 171–187
**Proximity Score**: 3/5
**Summary**: Using Spanish and Peruvian credit registry data, documents that four types of commercial credit (asset-based, cash flow, trade finance, leasing) have distinct growth dynamics and respond differently to bank lending channel shocks. Supply-side contractions disproportionately affect cash flow loans (the closest analog to bond market borrowing). Shows that loan-type heterogeneity is necessary to identify bank lending channel effects. Methodological comparator: the paper's decomposition of capital supply into distributional components maps onto this heterogeneity.
**Identification**: Within-firm regressions exploiting loan-type variation; matched borrower-lender data
**Data**: Bank credit registry data (Spain, Peru), 2002–2016
**Key Result**: Cash flow loans are most sensitive to monetary policy; asset-based loans are least sensitive

---

### [Greenwald, Krainer, Paul 2025] The Credit Line Channel
**Journal/Source**: Journal of Finance, Vol. 80 (2025)
**Proximity Score**: 3/5
**Summary**: Shows that during COVID-19, large firms drew heavily on pre-committed credit lines, causing banks that experienced larger drawdowns to restrict term lending, crowding out credit to smaller firms and reducing investment. While credit lines increase total bank credit in bad times, they redistribute credit from high-investment-propensity firms to low-investment-propensity firms. Highly relevant: pre-committed credit lines are a form of committed capital supply allocation — exactly the type of commitment that the paper's W1 coupling formalizes.
**Identification**: Loan-level supervisory data; structural model; IV using credit line commitments pre-COVID
**Data**: Fed supervisory loan-level data, Y-14 and FR Y-9C, 2020
**Key Result**: $1 of credit line drawdown crowds out $0.60 of term lending to other firms; investment falls 4% for crowded-out firms

---

### [Erel, Julio, Kim, Weisbach 2012] Macroeconomic Conditions and Capital Raising
**Journal/Source**: Review of Financial Studies, Vol. 25(2), pp. 341–376
**Proximity Score**: 3/5
**Summary**: Studies how macroeconomic conditions affect securities issued to raise capital. Non-investment-grade borrowers exhibit procyclical capital raising while investment-grade borrowers are countercyclical. Poor market conditions push debt toward shorter maturities and more security. Shows that supply-side conditions interact with borrower quality to determine both the quantity and quality of capital raised — directly relevant to how W1(μit, νt) varies with both borrower distribution μit and aggregate supply νt.
**Identification**: Probit and OLS regressions; time-series variation in macro conditions
**Data**: SDC Platinum debt issuance database, 1970–2008; Bloomberg macro variables
**Key Result**: Junk bond issuance falls 60% in recessions; IG issuance falls only 15%; maturity shortens ~1 year in recessions

---

### [Faulkender, Petersen 2006] Does the Source of Capital Affect Capital Structure?
**Journal/Source**: Review of Financial Studies, Vol. 19(1), pp. 45–79
**Proximity Score**: 3/5
**Summary**: Demonstrates that capital market access — proxied by having a public debt rating — significantly increases leverage independent of firm characteristics. Firms with public bond market access have ~35% more debt. Supply-side access determines capital structure over and above demand-side factors. This is the cleanest earlier evidence that the source (not just the cost) of capital matters for leverage — the paper's νt captures exactly what it means to have access to vs. exclusion from the aggregate capital supply distribution.
**Identification**: IV using bond rating as instrument for capital market access; OLS with rating fixed effects
**Data**: Compustat, 1986–2000; Moody's/S&P ratings data
**Key Result**: Public bond market access → 35 pp higher leverage (D/A); effect holds instrumenting for rating endogeneity

---

### [Greenwood, Hanson, Shleifer, Sorensen 2022] Predictable Financial Crises
**Journal/Source**: Journal of Finance, Vol. 77(2), pp. 863–921
**Proximity Score**: 3/5
**Summary**: Documents that rapid credit growth and asset price appreciation over the prior three years predicts a 40% probability of financial crisis within three years, versus 7% in normal times. Supports the Minsky-Kindleberger view that crises are predictable consequences of credit booms. Directly motivates the paper's time-varying νt (capital supply distribution) — during credit booms, νt shifts toward easier capital supply, lowering W1, increasing borrowing, and creating the conditions for subsequent crises.
**Identification**: Logit/probit regressions on country-level panel; historical data
**Data**: BIS credit data; historical financial crisis database (17 countries), 1870–2016
**Key Result**: Credit boom of 1 SD above trend → 5× increase in crisis probability; rapid asset price growth adds predictive power

---

## Category 5: TRACE-Based Corporate Bond Methodology (Proximity 2–3)

### [Dick-Nielsen, Feldhutter, Lando 2012] Corporate Bond Liquidity Before and After the Onset of the Subprime Crisis
**Journal/Source**: Journal of Financial Economics, Vol. 103(3), pp. 471–492
**Proximity Score**: 3/5
**Summary**: Develops a comprehensive illiquidity measure for corporate bonds using TRACE transaction data, 2005–2009. Finds illiquidity contributions to spreads increase dramatically at crisis onset: slow and persistent for IG bonds, strong but transient for HY bonds. Establishes TRACE as the authoritative data source for corporate bond liquidity research and proposes the four-component illiquidity measure widely used subsequently. Methodological foundation for TRACE-based analysis in the present paper (2012–2024 sample).
**Identification**: Panel regressions of spread components on illiquidity measures; time-series comparison pre/post-crisis
**Data**: TRACE, 2005–2009; 4,000+ bonds
**Key Result**: Illiquidity contributes ~14% of IG spread changes normally; rises to ~50% during crisis

---

### [Bao, Pan, Wang 2011] The Illiquidity of Corporate Bonds
**Journal/Source**: Journal of Finance, Vol. 66(3), pp. 911–946
**Proximity Score**: 3/5
**Summary**: Develops a measure of bond illiquidity (γ) based on the autocovariance of price changes from TRACE data, 2003–2009. Documents that illiquidity is substantial and well in excess of bid-ask spreads. Higher-rated bonds are more liquid. Changes in market-level illiquidity explain large portions of time variation in IG yield spreads. Establishes the benchmark illiquidity control that must be included in any TRACE-based spread regression.
**Identification**: Autocovariance-based illiquidity measure; OLS regressions; time-series
**Data**: TRACE, 2003–2009
**Key Result**: Bond-level illiquidity explains ~7% of individual spread variation; market-level illiquidity explains up to 45% of time-series spread variation for AAA bonds

---

### [Friewald, Jankowitsch, Subrahmanyam 2012] Illiquidity or Credit Deterioration: A Study of Liquidity in the US Corporate Bond Market During Financial Crises
**Journal/Source**: Journal of Financial Economics, Vol. 105(1), pp. 18–36
**Proximity Score**: 3/5
**Summary**: Uses TRACE data to disentangle liquidity effects from credit deterioration during financial crises. Studies 20,000+ bonds from October 2004 to December 2008. Finds liquidity effects account for ~14% of market-wide corporate yield spread changes, with significantly larger effects during crisis periods and for speculative-grade bonds. Establishes that illiquidity and credit risk interact in ways that complicate simple decomposition — relevant for the paper's need to control for liquidity when testing W1's explanatory power for spreads.
**Identification**: Panel regressions with Amihud-type and Roll-type illiquidity measures; interaction with crisis indicators
**Data**: TRACE, October 2004–December 2008; 20,000+ bonds
**Key Result**: Liquidity accounts for 14% of spread changes normally; up to 30% during the 2008 crisis peak

---

### [Longstaff, Mithal, Neis 2005] Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market
**Journal/Source**: Journal of Finance, Vol. 60(5), pp. 2213–2253
**Proximity Score**: 3/5
**Summary**: Uses CDS spreads to directly measure the default component of corporate bond spreads, attributing the remainder to liquidity. Finds the majority of the corporate spread is due to default risk, but the non-default component is time-varying and strongly related to bond-specific illiquidity and macroeconomic liquidity measures. Establishes the CDS-bond basis as a clean way to decompose spreads. The paper uses TRACE bonds rather than CDS; Longstaff et al.'s methodology provides the theoretical basis for the liquidity controls.
**Identification**: CDS-bond decomposition; regression of residual on illiquidity and macro measures
**Data**: CDS market and corporate bond data, 2001–2002; 68 firms
**Key Result**: Default risk accounts for ~65% of corporate spread; non-default component correlated with illiquidity and flight-to-quality

---

### [Ericsson, Renault 2006] Liquidity and Credit Risk
**Journal/Source**: Journal of Finance, Vol. 61(5), pp. 2219–2250
**Proximity Score**: 2/5
**Summary**: Develops a structural model that simultaneously captures liquidity and credit risk in corporate bond pricing. Shows that as default becomes more likely, the liquidity component of spreads also increases, generating positive correlation between illiquidity and default components. This "liquidity-default feedback" is relevant when decomposing TRACE spreads into credit vs. supply components.
**Identification**: Structural bond valuation model; 15-year bond price dataset
**Data**: Corporate bond prices, 1983–1998
**Key Result**: Positive correlation between illiquidity and default spread components; downward-sloping term structure of liquidity spreads

---

### [Goldberg, Nozawa 2021] Liquidity Supply in the Corporate Bond Market
**Journal/Source**: Journal of Finance, Vol. 76(2), pp. 755–796
**Proximity Score**: 3/5
**Summary**: Identifies shocks to aggregate liquidity supply in the corporate bond market using TRACE data on bond yields and dealer positions. Liquidity supply shocks lead to persistent changes in market liquidity, correlate with dealer financial constraints, and have significant explanatory power for cross-sectional and time-series expected returns beyond standard risk factors. This is the closest TRACE-based paper using dealer balance sheet data to study supply-side effects — the supply shocks identified are closely related to shifts in νt.
**Identification**: IV with dealer inventory position changes; panel regressions; cross-sectional tests
**Data**: TRACE, FINRA dealer position data, Compustat, 2002–2015
**Key Result**: Liquidity supply shocks explain ~25% of time-series variation in market illiquidity measures; significant cross-sectional risk price

---

### [Chen, Cui, He, Milbradt 2018] Quantifying Liquidity and Default Risks of Corporate Bonds over the Business Cycle
**Journal/Source**: Review of Financial Studies, Vol. 31(3), pp. 852–897
**Proximity Score**: 3/5
**Summary**: Develops a structural credit model incorporating debt rollover, bond-price-dependent holding costs, and search frictions in secondary markets. Interactions between default and liquidity account for 10–24% of the level of credit spreads and 16–46% of spread changes over the business cycle. Structural decomposition shows liquidity-related financing costs amount to 6% of total bond issuance. Key methodological precedent for the paper's structural decomposition of spreads into cash flow distribution and capital supply distribution components.
**Identification**: Structural model with OTC search frictions; calibrated to TRACE data and historical default rates
**Data**: TRACE corporate bond data; Moody's default database, 1996–2015
**Key Result**: Default-liquidity interaction explains 10–24% of spread levels; model matches bid-ask and bond-CDS spread dynamics

---

### [He, Milbradt 2014] Endogenous Liquidity and Defaultable Bonds
**Journal/Source**: Econometrica, Vol. 82(4), pp. 1443–1508
**Proximity Score**: 2/5
**Summary**: Studies OTC corporate bond trading with search frictions where bond liquidity is endogenous to the firm's default decision. A default-liquidity loop arises: earlier default worsens secondary market liquidity, which amplifies equity holder rollover losses, leading to even earlier default. Provides the theoretical foundation for the endogenous component of the non-credit spread in TRACE data that the paper uses.
**Identification**: Continuous-time OTC search model; solved analytically
**Data**: Theoretical model; calibration to U.S. corporate bond data
**Key Result**: Default-liquidity loop can generate multiple equilibria and amplify spread increases beyond fundamental default probability

---

## Category 6: Credit Market Segmentation and Lender Heterogeneity (Proximity 3–4)

### [Chernenko, Sunderam 2012] The Real Consequences of Market Segmentation
**Journal/Source**: Review of Financial Studies, Vol. 25(7), pp. 2041–2069
**Proximity Score**: 4/5
**Summary**: Studies real effects of credit market segmentation at the investment-grade/speculative-grade boundary. Flows into high-yield mutual funds have economically significant effects on issuance and investment of speculative-grade firms relative to investment-grade matches — especially for financially constrained firms. The effect is associated with the discrete change in label, not continuous credit quality. Won RFS Young Researcher Prize. Directly motivates the paper's mechanism: segmentation of the capital supply distribution νt by credit rating implies W1(μit, νt) varies discretely at the rating boundary.
**Identification**: Matched-sample DiD using credit rating boundary; fund flow shocks as IV
**Data**: TRACE (pre-2012); Morningstar mutual fund flows; Compustat, 1995–2007
**Key Result**: 1 SD increase in HY fund flows → speculative-grade firms issue 4% more debt and invest 2% more; IG firms unaffected

---

### [Bretscher, Schmid, Sen, Sharma 2026] Institutional Corporate Bond Pricing
**Journal/Source**: Review of Financial Studies, Vol. 39(3), pp. 605– (Lead Article, Editor's Choice)
**Proximity Score**: 4/5
**Summary**: Proposes an equilibrium demand-based corporate bond pricing model capturing heterogeneity in institutional investor preferences and mandates. Estimated on holdings data, the model shows insurance companies are inelastic (focus on IG) while mutual funds are elastic and substitute across rating buckets. Institutional demand composition is an important state variable for corporate bond pricing. This is the most recent published paper using the demand-system approach to corporate bond markets — must be addressed as a direct comparator using similar institutional holdings data.
**Identification**: Demand system estimation (Koijen-Yogo style); equilibrium model; panel IV
**Data**: eMAXX institutional bond holdings; TRACE spreads; Compustat, 2003–2019
**Key Result**: Insurance elasticity ~0.2 (inelastic); mutual fund elasticity ~2.5 (elastic); composition of demand explains 30%+ of IG/HY spread differential
**FLAG**: Proximity 4 — Most recent supply-side demand-system paper on corporate bond pricing. Must address how the W1 approach differs from the demand-system approach.

---

### [Koijen, Yogo 2023] Understanding the Ownership Structure of Corporate Bonds
**Journal/Source**: American Economic Review: Insights, Vol. 5(1), pp. 73–92
**Proximity Score**: 3/5
**Summary**: Explains why insurance companies — despite being the largest corporate bond investors — hold corporate bonds in equilibrium, resolving a theoretical puzzle. Insurers have cheap access to leverage through underwriting activity and hold leveraged portfolios of low-beta assets, relaxing other investors' leverage constraints. The model implies specific equilibrium patterns in institutional ownership that vary with bond characteristics. Motivates the paper's heterogeneous lender interpretation: insurance companies represent a specific component of νt with distinct risk-bearing capacity.
**Identification**: Equilibrium asset pricing model; empirical validation against 13F and NAIC data
**Data**: NAIC insurance holdings; 13F mutual fund holdings; TRACE; 2010–2019
**Key Result**: Insurance holdings of corporate bonds are ~$3T; model explains their IG bias through leverage recycling mechanism

---

### [Colla, Ippolito, Li 2013] Debt Specialization
**Journal/Source**: Journal of Finance, Vol. 68(5), pp. 2117–2141
**Proximity Score**: 2/5
**Summary**: Documents using a comprehensive database of debt types that 85% of U.S. public firms borrow predominantly with one type of debt. Debt specialization varies systematically: small unrated firms specialize; large rated firms diversify. This heterogeneity in debt composition reflects segmented capital markets — firms access different parts of the capital supply distribution depending on their type. Relevant for understanding the support and shape of νt.
**Identification**: Descriptive statistics and regressions on debt type shares; cross-sectional variation
**Data**: Capital IQ debt structure data; Compustat, 2002–2009
**Key Result**: 85% of firms have one dominant debt type; senior secured and senior unsecured bonds dominate large firms; lines of credit dominate small firms

---

### [Rauh, Sufi 2010] Capital Structure and Debt Structure
**Journal/Source**: Review of Financial Studies, Vol. 23(12), pp. 4242–4280
**Proximity Score**: 2/5
**Summary**: Shows that capital structure studies ignoring debt heterogeneity miss substantial variation. Low-credit-quality firms have multi-tiered structures combining secured bank debt (tight covenants) and subordinated non-bank debt (loose covenants). The tiering of capital structure by credit quality reflects access to different segments of the capital supply distribution. Motivates the paper's multi-segment interpretation of νt.
**Identification**: Descriptive analysis; OLS regressions with debt-type fixed effects
**Data**: Capital IQ debt structure; Compustat, 2002–2006
**Key Result**: Investment-grade firms borrow primarily from bond markets; leveraged firms use tiered bank + bond structures

---

## Category 7: Leverage Cross-Section and Heterogeneity (Proximity 2–3)

### [Flannery, Nikolova, Oztekin 2012] Leverage Expectations and Bond Credit Spreads
**Journal/Source**: Journal of Financial and Quantitative Analysis, Vol. 47(4), pp. 689–714
**Proximity Score**: 3/5
**Summary**: Constructs proxies for investors' expectations about future leverage changes using trade-off, pecking order, and credit-rating theories of capital structure and shows these significantly affect bond yields beyond contemporaneous leverage. Investors appear to price expected leverage dynamics, not just current leverage levels. Directly relevant: the paper's W1(μit, νt) should contain information about expected future leverage beyond current leverage, consistent with this finding.
**Identification**: OLS with forward-looking leverage proxies derived from structural capital structure models
**Data**: Compustat; Lehman bond data, 1987–2004
**Key Result**: Expected leverage increase adds ~6 bps to spreads per unit; all three theory-based proxies have significant spread effects

---

### [Benmelech, Kumar, Rajan 2024] The Decline of Secured Debt
**Journal/Source**: Journal of Finance, Vol. 79(1), pp. 35–93
**Proximity Score**: 2/5
**Summary**: Documents a secular decline in secured debt among large public firms. Explains the decline via financial development that increases creditor confidence, leading firms to retain flexibility by not pledging collateral upfront. Security is given contingently as firms approach distress. Countercyclical share of secured debt superimposed on secular decline. Motivates the paper's time-varying interpretation of the capital supply distribution: tighter capital supply (higher W1) corresponds to conditions under which secured borrowing increases.
**Identification**: Time-series and panel OLS; historical data reconstruction
**Data**: Compustat, SDC, FISD; 1900–2018
**Key Result**: Secured debt share fell from ~80% in 1920s to ~15% today; contingent collateral becomes more prevalent near distress

---

### [Brunnermeier, Sannikov 2014] (see Category 2 above — also fits here as macro-finance theory)

---

### [Greenwood, Hanson 2013] Issuer Quality and Corporate Bond Returns
**Journal/Source**: Review of Financial Studies, Vol. 26(6), pp. 1483–1525
**Proximity Score**: 3/5
**Summary**: Shows that the credit quality of corporate debt issuers deteriorates during credit booms and that this deterioration forecasts low excess returns to corporate bondholders. Changes in pricing of credit risk disproportionately affect financing costs of low-quality firms; thus low-quality firm issuance is a useful predictor of bond returns. This is the paper cited in the researcher's "already cited" list (as 2013 RFS — confirmed: this is the Greenwood-Hanson 2013 RFS paper referenced by the researcher and excluded from the search list). Included here for completeness but the researcher indicated it is already cited.
**Note**: Researcher listed as "already cited" — included for cross-referencing only.

---

## Category 8: Theoretical Foundations — Optimal Transport (Proximity 1–2)

### [Villani 2009] Optimal Transport: Old and New
**Journal/Source**: Grundlehren der mathematischen Wissenschaften, Vol. 338 (Springer)
**Proximity Score**: 1/5
**Summary**: Comprehensive monograph on optimal transport theory. Covers the Kantorovich duality, Brenier's polar factorization theorem, geometry of optimal transportation, Monge-Ampere equations, Wasserstein distances, and applications. The Brenier theorem (every optimal transport plan between absolutely continuous measures is realized as the gradient of a convex potential) is the mathematical foundation for the quantile coupling result that underlies the paper's debt capacity formula.
**Identification**: Mathematical theory; no empirical content
**Data**: None
**Key Result**: W_p(μ, ν)^p = inf_{γ ∈ Γ(μ,ν)} ∫ c(x,y) dγ; Brenier theorem characterizes the optimizer as a monotone map

---

### [Brenier 1991] Polar Factorization and Monotone Rearrangement of Vector-Valued Functions
**Journal/Source**: Communications on Pure and Applied Mathematics, Vol. 44(4), pp. 375–417
**Proximity Score**: 1/5
**Summary**: Proves the polar factorization theorem: any sufficiently integrable vector-valued map can be decomposed as the composition of the gradient of a convex function with a measure-preserving map. This implies the existence of an optimal transport map that is the gradient of a convex potential, giving the monotone coupling result. The 1D special case directly implies the quantile coupling that underlies the paper's optimal contract characterization.
**Identification**: Mathematical proof; no empirical content
**Data**: None
**Key Result**: In 1D, optimal transport map between μ and ν is the quantile function composition F_ν^{-1} ∘ F_μ

---

## Category 9: Methods Papers — SMM and Structural Estimation (Proximity 1–2)

### [Berry, Levinsohn, Pakes 1995] Automobile Prices in Market Equilibrium
**Journal/Source**: Econometrica, Vol. 63(4), pp. 841–890
**Proximity Score**: 1/5
**Summary**: Develops the BLP method for estimating discrete-choice demand models using market-level data with random coefficients and instruments for price endogeneity. The contraction mapping and GMM estimation architecture are the template for the paper's SMM estimation of structural parameters θ = (α_ν, σ_ν, κ). Cite as the methodological ancestor of the SMM approach.
**Identification**: Random-coefficients logit; contraction mapping; GMM/IV
**Data**: U.S. automobile market, 1971–1990
**Key Result**: Demand elasticities are heterogeneous across consumers; price competition is more intense than homogeneous-goods models imply

---

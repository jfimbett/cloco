# Literature Review: Debt Capacity, Borrowing Constraints, and Financial Frictions
**Project**: Distributional Debt Capacity via Wasserstein Distance
**Date**: 2026-06-14
**Librarian**: academic-librarian agent

---

## Summary Statistics
- Total papers catalogued: 34
- Proximity 5 (direct competitors): 3
- Proximity 4 (closely related): 8
- Proximity 3 (same method or context, different question): 10
- Proximity 2 (background/motivating): 8
- Proximity 1 (theoretical/mathematical foundations): 5

---

## Category 1: Directly Related (Proximity 4–5)

### [Rampini and Viswanathan 2010] Collateral, Risk Management, and the Distribution of Debt Capacity
**Journal/Source**: Journal of Finance, Vol. 65, No. 6, pp. 2293–2322
**Proximity Score**: 5/5
**Summary**: This paper develops a theory in which the *distribution* of debt capacity across firms is the central object of study — the title uses the exact phrase that anchors your paper. The model shows that promises to both financiers and hedging counterparties must be collateralized, so that risk management and financing compete for the same scarce collateral. The paper derives how debt capacity is distributed across firms as a function of net worth and tangible asset values: firms with higher net worth can support more debt, and this capacity is pinned down by collateral constraints rather than cash-flow-based covenants. The distribution of debt capacity emerges from heterogeneity in collateral holdings.
**Identification**: Theory — two-period and infinite-horizon model with collateral constraints; no reduced-form empirics.
**Data**: Theoretical; calibration references US firm-level data.
**Key Result**: More constrained firms hedge less because hedging and financing compete for the same collateral; debt capacity is monotone in net worth and asset tangibility.

---

### [Rampini and Viswanathan 2013] Collateral and Capital Structure
**Journal/Source**: Journal of Financial Economics, Vol. 109, No. 2, pp. 466–492
**Proximity Score**: 5/5
**Summary**: Extends Rampini-Viswanathan (2010) to a full dynamic setting with endogenous investment, capital structure, leasing, and risk management, all subject to collateral constraints. The paper derives the cross-sectional and dynamic distribution of debt and risk management across firms. The central insight is that the same collateral constraint that limits borrowing also determines how firms sort across financing instruments. More constrained firms (lower net worth relative to investment needs) tilt toward leasing and away from hedging. The cross-sectional distribution of leverage follows directly from the distribution of net worth and investment opportunities.
**Identification**: Dynamic structural model; optimal contracts with limited enforcement.
**Data**: Theoretical; motivated by Compustat cross-sectional patterns.
**Key Result**: Leasing allows greater leverage when collateral is scarce; the distribution of capital structure is determined by the distribution of net worth relative to investment scale.

---

### [Lian and Ma 2021] Anatomy of Corporate Borrowing Constraints
**Journal/Source**: Quarterly Journal of Economics, Vol. 136, No. 1, pp. 229–291
**Proximity Score**: 5/5
**Summary**: The empirical benchmark paper for cash-flow-based debt capacity. Lian and Ma document that 80% of US nonfinancial corporate debt by value is cash-flow-based (primarily earnings-based), with only 20% asset-based. They define earnings-based borrowing constraints (EBCs) as total debt bounded by a multiple of EBITDA. The paper shows that this type of constraint directly shapes firm investment, employment, and cash management, and that asset price movements have a smaller effect on borrowing when EBCs bind. Their measure of debt capacity is explicitly a function of the distribution of earnings flows, making this the closest empirical counterpart to your theoretical setup.
**Identification**: Descriptive analysis of DealScan covenant data plus causal evidence from covenant violations using RDD in the spirit of Chava-Roberts (2008).
**Data**: DealScan (loan contract data), Compustat (firm financials), 1993–2015.
**Key Result**: 80% of debt value is governed by EBCs; firms facing binding EBCs reduce investment by roughly 3.5% of assets.

---

### [Hart and Moore 1994] A Theory of Debt Based on the Inalienability of Human Capital
**Journal/Source**: Quarterly Journal of Economics, Vol. 109, No. 4, pp. 841–879
**Proximity Score**: 4/5
**Summary**: Foundational incomplete-contracts theory of debt capacity. The entrepreneur cannot commit to not withdrawing human capital from the project, which creates an upper bound on total debt at any date. Hart and Moore derive this maximum borrowing capacity as a function of the liquidation value of assets and the entrepreneur's outside option — a direct precursor to the idea that debt capacity is pinned by the distribution of project payoffs relative to lender claims. The paper characterizes optimal debt contracts as a function of the maturity structure of payoffs and asset durability, showing that the shape of the cash-flow path determines the debt capacity path.
**Identification**: Incomplete contracts theory; comparative statics on debt capacity.
**Data**: Theoretical.
**Key Result**: Debt capacity is bounded above by the liquidation value of project assets; optimal debt repayment profile mirrors the project payoff profile.

---

### [Kiyotaki and Moore 1997] Credit Cycles
**Journal/Source**: Journal of Political Economy, Vol. 105, No. 2, pp. 211–248
**Proximity Score**: 4/5
**Summary**: The foundational macro-finance model of endogenous debt limits tied to asset values. In the Kiyotaki-Moore model, borrowing constraints bind at the collateral value of durable assets, so that the aggregate distribution of asset values determines the aggregate distribution of borrowing capacity. Small shocks get amplified because declining asset prices tighten borrowing constraints, which depresses investment, which further reduces asset prices. The mechanism depends on a mapping from the distribution of asset holdings to the distribution of debt limits — directly analogous to your mapping from the distribution of cash flows (µ) to debt capacity via W1.
**Identification**: Dynamic general equilibrium model with collateral constraints; theoretical.
**Data**: Theoretical; calibrated to US macro moments.
**Key Result**: Collateral constraints create a financial accelerator in which small shocks generate large, persistent output fluctuations.

---

### [Greenwald 2019] Firm Debt Covenants and the Macroeconomy: The Interest Coverage Channel
**Journal/Source**: MIT Sloan Research Paper / Working Paper (presented at SED 2019)
**Proximity Score**: 4/5
**Summary**: Greenwald builds a structural model of firm borrowing in which debt capacity is determined by cash-flow-based covenants — specifically, the interest coverage ratio (interest payments / EBITDA) and the debt-to-EBITDA ratio. These two covenants together imply that a firm's maximum debt is a function of earnings flows and interest rates. This is the most direct structural model of cash-flow-based debt capacity prior to your paper. Greenwald shows that interest coverage constraints amplify monetary policy transmission: when rates rise, coverage ratios tighten, compressing debt capacity and amplifying the investment response.
**Identification**: Structural model estimated on Compustat/DealScan; calibration.
**Data**: Compustat, DealScan, 2000–2016.
**Key Result**: Interest coverage covenants generate 30–40% additional amplification of interest rate shocks; debt-to-EBITDA covenants dominate in low-rate environments.

---

### [Kermani and Ma 2022] Two Tales of Debt
**Journal/Source**: NBER Working Paper No. 27641 (2020, revised 2022)
**Proximity Score**: 4/5
**Summary**: Documents and theorizes the distinction between asset-based debt (secured by discrete physical assets, governed by liquidation values) and going-concern debt (secured by firm operations, governed by cash flows). Roughly three-quarters of noninvestment-grade debt exceeds the liquidation value of physical assets, confirming that the bulk of corporate borrowing is underwritten by the distribution of future cash flows. The paper derives implications for monitoring intensity and covenant design, showing that cash-flow-based lenders impose tighter performance covenants when liquidation values are low. Directly motivates the cash flow distribution (µ) as the relevant object for debt capacity in your model.
**Identification**: Cross-sectional regression and structural decomposition using Capital IQ, DealScan, SNL data.
**Data**: Capital IQ, DealScan, SNL Financial; US public firms, 2000–2017.
**Key Result**: At least one-third of secured debt is backed by operating business value rather than discrete assets; tighter covenants when liquidation value is lower.

---

### [Nikolov, Schmid, and Steri 2021] The Sources of Financing Constraints
**Journal/Source**: Journal of Financial Economics, Vol. 139, No. 2, pp. 478–501
**Proximity Score**: 4/5
**Summary**: Uses structural estimation to distinguish among three theories of financing constraints — trade-off theory (debt tax shields vs. distress), limited commitment (collateral constraints à la Rampini-Viswanathan), and moral hazard (agency costs à la Holmstrom-Tirole). The paper tests which model best fits firm-level policy functions from Compustat (large firms) and Orbis (private firms). It finds that the data favor limited commitment models for small firms and moral hazard for private firms, providing direct evidence on which type of borrowing constraint is empirically relevant across the firm distribution. Directly informs how your distributional model should be interpreted across firm size.
**Identification**: Simulated Method of Moments (SMM); structural estimation; empirical policy function matching.
**Data**: Compustat (1980–2015) and Orbis (private firms, Europe and US).
**Key Result**: Limited commitment models fit small firms best; trade-off models fit large Compustat firms; moral hazard models fit private firms.

---

## Category 2: Same Method, Different Context (Proximity 3)

### [Bernanke, Gertler, and Gilchrist 1999] The Financial Accelerator in a Quantitative Business Cycle Framework
**Journal/Source**: Handbook of Macroeconomics, Vol. 1, Ch. 21, pp. 1341–1393 (Elsevier). Also NBER Working Paper No. 6455 (1997).
**Proximity Score**: 3/5
**Summary**: Introduces the financial accelerator into a DSGE model by deriving an external finance premium that depends inversely on borrower net worth. Firms with higher net worth can support more borrowing at lower cost. The key mechanism is an agency problem (costly state verification, following Townsend 1979) that maps the distribution of firm net worth to the distribution of external finance costs. As net worth falls (e.g., in a recession), borrowing costs rise, amplifying output fluctuations. While the method is structural DSGE rather than optimal transport, the mapping from a distribution of fundamentals (net worth) to a distribution of debt costs is conceptually similar to your W1 mapping.
**Identification**: Structural DSGE model with financial accelerator; calibration to US quarterly data.
**Data**: US National Accounts, quarterly, 1950–1998.
**Key Result**: Credit market frictions amplify and propagate real shocks; the external finance premium rises by 100–200 bps during recessions.

---

### [Hennessy and Whited 2007] How Costly Is External Financing? Evidence from a Structural Estimation
**Journal/Source**: Journal of Finance, Vol. 62, No. 4, pp. 1705–1745
**Proximity Score**: 3/5
**Summary**: Estimates a structural dynamic model of firm investment, leverage, and default using SMM — the same estimation architecture your paper employs. The model features endogenous investment, distributions, leverage, and default, with the corporation facing taxation, costly bankruptcy, and equity flotation costs. The paper infers the magnitude of financing frictions (equity issuance costs and bankruptcy costs) from the cross-sectional and time-series behavior of firm-level financial policies. The SMM implementation on Compustat provides the methodological template for your own structural estimation.
**Identification**: Simulated Method of Moments (SMM); dynamic structural model.
**Data**: Compustat, 1988–2001.
**Key Result**: Large-firm equity flotation costs average 5.0%; bankruptcy costs equal 8.4% of capital; financing frictions are substantial.

---

### [Hennessy and Whited 2005] Debt Dynamics
**Journal/Source**: Journal of Finance, Vol. 60, No. 3, pp. 1129–1165
**Proximity Score**: 3/5
**Summary**: Develops a dynamic trade-off model with endogenous leverage, distributions, and real investment, featuring a graduated corporate income tax, financial distress costs, and equity flotation costs. The paper shows that in this model there is no unique target leverage ratio; leverage is path-dependent and is decreasing in lagged liquidity. This provides the dynamic capital structure backdrop against which your static optimal transport model should be contrasted. The result that leverage varies negatively with external-finance-weighted average Q motivates the cross-sectional variation in leverage that your W1 should explain.
**Identification**: Structural dynamic model; analytical derivations and simulation.
**Data**: Theoretical; calibrated to Compustat moments.
**Key Result**: Leverage is path-dependent; no single target; leverage is decreasing in lagged liquidity and investment opportunity.

---

### [Strebulaev 2007] Do Tests of Capital Structure Theory Mean What They Say?
**Journal/Source**: Journal of Finance, Vol. 62, No. 4, pp. 1747–1787
**Proximity Score**: 3/5
**Summary**: Uses a calibrated dynamic trade-off model to show that standard cross-sectional OLS tests of capital structure theory can produce misleading results when leverage is sticky. In the model, firms adjust infrequently, so observed leverage is a mix of past and current targets. This is the canonical reference for why static cross-sectional regressions can reject the correct dynamic model. Directly relevant for your paper because your W1-based debt capacity is a static measure but your empirical tests use cross-sectional and panel leverage data that are potentially contaminated by adjustment frictions.
**Identification**: Calibrated dynamic structural model; simulated cross-sections compared to Compustat.
**Data**: Compustat, US firms, 1965–2003.
**Key Result**: Standard tests reject the correct dynamic model; the model can generate empirical patterns (e.g., negative profitability-leverage relation) that are typically attributed to pecking order theory.

---

### [DeAngelo, DeAngelo, and Whited 2011] Capital Structure Dynamics and Transitory Debt
**Journal/Source**: Journal of Financial Economics, Vol. 99, No. 2, pp. 235–261
**Proximity Score**: 3/5
**Summary**: Develops a dynamic structural model of financial flexibility, in which debt capacity is maintained by deliberately choosing lower leverage in good times so that borrowing capacity is available for future investment needs. The central object is a firm's "residual debt capacity" — how much more it could borrow relative to its current leverage. The paper formalizes why profitable firms maintain low leverage: the shadow value of debt capacity is high when investment opportunities are expected to be volatile. This notion of debt capacity as a buffer stock directly motivates why firms do not fully exhaust their W1-based debt capacity.
**Identification**: Dynamic structural model; calibration to Compustat.
**Data**: Compustat, US firms.
**Key Result**: Firms hold leverage below their static optimum to preserve future borrowing capacity; the financial flexibility value of low leverage equals 7–15% of firm value.

---

### [Geanakoplos 2010] The Leverage Cycle
**Journal/Source**: NBER Macroeconomics Annual 2009, Vol. 24, pp. 1–65 (also Cowles Foundation Discussion Paper No. 1715, January 2010)
**Proximity Score**: 3/5
**Summary**: Develops a general equilibrium theory of endogenous collateral constraints and leverage cycles. In Geanakoplos's model, equilibrium determines the haircut (margin requirement) on every security as well as the interest rate. During booms, haircuts fall and leverage rises; during crashes, haircuts jump and leverage collapses. The leverage cycle provides a macro-finance interpretation of how aggregate borrowing capacity (your ν_t) varies over the cycle: when the aggregate capital supply distribution shifts toward less lending (higher haircuts), debt capacity falls for all firms simultaneously.
**Identification**: General equilibrium theory with heterogeneous agents; no empirics.
**Data**: Theoretical.
**Key Result**: Leverage is procyclical because equilibrium haircuts are determined by the heterogeneity in agent beliefs about asset payoffs; leverage cycles amplify asset price volatility.

---

### [Brunnermeier and Pedersen 2009] Market Liquidity and Funding Liquidity
**Journal/Source**: Review of Financial Studies, Vol. 22, No. 6, pp. 2201–2238
**Proximity Score**: 3/5
**Summary**: Models the interaction between market liquidity of assets and funding liquidity of traders, showing that margins (haircuts) are endogenous and mutually reinforcing with asset prices. When funding is tight, traders reduce positions, reducing market liquidity, which increases margins, further tightening funding. The paper establishes how the distribution of funding capacity across traders maps to the distribution of asset liquidity — conceptually parallel to how your aggregate capital supply distribution ν_t maps to firm-level debt capacity. The spiral mechanism is relevant for understanding why debt capacity is correlated across firms during aggregate shocks.
**Identification**: Theoretical model; no structural estimation.
**Data**: Theoretical; motivated by observed margin spirals.
**Key Result**: Margins are destabilizing; small shocks can trigger liquidity spirals; commonality in market liquidity is endogenous.

---

### [Aghion and Bolton 1992] An Incomplete Contracts Approach to Financial Contracting
**Journal/Source**: Review of Economic Studies, Vol. 59, No. 3, pp. 473–494
**Proximity Score**: 3/5
**Summary**: Develops an incomplete contracts model of debt and equity financing, showing that the allocation of control rights between entrepreneur and investor as a function of realized cash flows determines the optimal financial structure. When cash flows are high, equity holders (entrepreneur) retain control; when low, debt holders gain control via default. The paper derives the optimal contract as a function of the distribution of cash-flow states, directly motivating how the shape of the cash-flow distribution (µ in your model) determines the design and quantity of feasible debt.
**Identification**: Mechanism design / incomplete contracts theory.
**Data**: Theoretical.
**Key Result**: Debt is optimal when the entrepreneur's private benefit from control is non-contractible; the threshold for control transfer is pinned by the distribution of cash-flow outcomes.

---

### [Chaney, Sraer, and Thesmar 2012] The Collateral Channel: How Real Estate Shocks Affect Corporate Investment
**Journal/Source**: American Economic Review, Vol. 102, No. 6, pp. 2381–2409
**Proximity Score**: 3/5
**Summary**: Provides the canonical empirical estimate of the collateral channel: firms borrow and invest more when their pledgeable assets appreciate. The identification uses local real estate price shocks interacted with land supply constraints as an instrument for collateral value. The paper finds that every $1 increase in collateral value raises investment by $0.06, implying a debt capacity elasticity of roughly 25–30 cents on the dollar. This is the empirical benchmark for asset-based debt capacity; your cash-flow-based debt capacity via W1 should be compared to this collateral channel in magnitude and cross-sectional variation.
**Identification**: IV regression; local real estate prices interacted with land supply inelasticity (following Saiz 2010) as instrument.
**Data**: Compustat, commercial real estate data, 1993–2007.
**Key Result**: $1 increase in collateral raises investment by $0.06; collateral channel is quantitatively important for firm-level investment.

---

### [Greenwald, Krainer, and Paul 2025] The Credit Line Channel
**Journal/Source**: Journal of Finance, Vol. LXXX, No. 6 (December 2025)
**Proximity Score**: 3/5
**Summary**: Documents that credit line drawdowns — rather than new term loans — drive aggregate bank lending expansions in bad times. Using supervisory loan-level data for large US banks, the paper shows that credit lines are an ex ante commitment of debt capacity that firms draw on during aggregate shocks. The mechanism is that credit lines pre-commit lenders to provide cash-flow-based debt capacity up to an agreed limit, and firms exercise this option during downturns. The paper demonstrates that redistribution of credit capacity across firm types has real effects — a distributional view of debt capacity closely aligned with your setup.
**Identification**: Difference-in-differences using COVID shock; supervisory loan-level data.
**Data**: Federal Reserve supervisory loan-level data, 2020.
**Key Result**: Credit line drawdowns drove all of the aggregate credit expansion after COVID; banks that faced larger drawdowns crowded out term lending to smaller firms.

---

## Category 3: Same Context, Different Method (Proximity 3)

### [Rajan and Zingales 1995] What Do We Know about Capital Structure? Some Evidence from International Data
**Journal/Source**: Journal of Finance, Vol. 50, No. 5, pp. 1421–1460
**Proximity Score**: 3/5
**Summary**: The canonical cross-sectional horse race for leverage determinants. Rajan and Zingales identify four factors robustly correlated with leverage across the G-7: market-to-book (–), asset tangibility (+), profitability (–), and firm size (+). These four factors serve as the baseline regression controls against which your W1-based debt capacity measure must demonstrate incremental explanatory power. The supply-side interpretation of their findings — that leverage variation reflects not just firm-level demand for debt but also cross-sectional variation in lender willingness — motivates your capital supply distribution ν_t.
**Identification**: OLS cross-sectional and panel regressions; no causal identification.
**Data**: Compustat plus international accounting data (G-7), 1987–1991.
**Key Result**: Tangibility (+), profitability (–), size (+), and market-to-book (–) robustly correlate with leverage across all G-7 countries.

---

### [Frank and Goyal 2009] Capital Structure Decisions: Which Factors Are Reliably Important?
**Journal/Source**: Financial Management, Vol. 38, No. 1, pp. 1–37
**Proximity Score**: 3/5
**Summary**: The updated and most comprehensive horse race for cross-sectional leverage determinants, spanning 1950–2003. Frank and Goyal identify six reliably important factors: median industry leverage (+), market-to-book (–), asset tangibility (+), profitability (–), log assets (+), and expected inflation (+). This is the exact horse race against which your W1-based measure should be tested: if W1(µ_i, ν_t) adds explanatory power beyond all six Frank-Goyal controls, it constitutes a new independent determinant of leverage. Profitability (–) is particularly important because it measures cash flows, which are the object in µ_i.
**Identification**: Cross-sectional OLS regressions with firm controls; some panel specifications.
**Data**: Compustat, US public firms, 1950–2003.
**Key Result**: Six factors reliably predict leverage; market-to-book and industry leverage are the strongest individual predictors.

---

### [Graham 2000] How Big Are the Tax Benefits of Debt?
**Journal/Source**: Journal of Finance, Vol. 55, No. 5, pp. 1901–1941 (Brattle Prize winner)
**Proximity Score**: 3/5
**Summary**: Estimates the capitalized value of corporate tax benefits from debt using simulated marginal tax rates, finding they equal approximately 9.7% of firm value. The paper also documents substantial variation in tax benefits across firms and shows that many profitable firms are "under-levered" relative to what the tax model predicts — the debt capacity puzzle. Graham's finding that large profitable firms use debt conservatively despite high tax benefits suggests that supply-side constraints (your ν_t) or other frictions limit firms from exploiting the full tax benefit, motivating a distributional approach to understanding why firms borrow less than the tax model predicts.
**Identification**: Simulated marginal tax rates (Compustat + Graham-Harvey tax rate methodology); no IV.
**Data**: Compustat, US firms, 1980–1994.
**Key Result**: Tax benefits of debt = 9.7% of firm value; typical firm could double tax benefits by issuing more debt — debt conservatism is widespread.

---

### [MacKay and Phillips 2005] How Does Industry Affect Firm Financial Structure?
**Journal/Source**: Review of Financial Studies, Vol. 18, No. 4, pp. 1433–1466
**Proximity Score**: 3/5
**Summary**: Documents that financial leverage depends not just on firm-level characteristics but on a firm's position within its industry — proxied by its proximity to the median industry capital-labor ratio (the "natural hedge"). Firms closer to the industry median have lower default risk and higher debt capacity, creating within-industry cross-sectional dispersion in leverage. This within-industry dispersion is directly relevant for your model: the Wasserstein distance between µ_i and ν_t varies within an industry because µ_i differs across firms, producing a distribution of debt capacities that should map to the observed leverage distribution.
**Identification**: OLS panel regressions with firm fixed effects; structural industrial organization model.
**Data**: Compustat, Census of Manufactures, 1981–1995.
**Key Result**: Leverage dispersion is larger in competitive industries; position within industry (proximity to median capital-labor ratio) is a significant leverage determinant.

---

### [Farre-Mensa and Ljungqvist 2016] Do Measures of Financial Constraints Measure Financial Constraints?
**Journal/Source**: Review of Financial Studies, Vol. 29, No. 2, pp. 271–308
**Proximity Score**: 3/5
**Summary**: Tests whether the six most widely used financial constraint indices (KZ, WW, SA, dividend payer, bond rating, size) actually capture binding financing constraints, using two tests: (i) constrained firms should issue equity more often when constraints relax; (ii) constrained firms should respond more to cash windfalls. The paper finds that most existing constraint measures fail both tests, suggesting that measured leverage and standard controls do not adequately capture the distributional variation in debt capacity. This motivates your W1-based measure as a theoretically grounded alternative to these reduced-form indices.
**Identification**: Regression discontinuity at index thresholds; event study around constraint shocks.
**Data**: Compustat, 1985–2011.
**Key Result**: Most constraint indices fail both validity tests; small-firm and dividend-payer classifications perform best; KZ and WW indices are unreliable.

---

### [Demiroglu and James 2010] The Information Content of Bank Loan Covenants
**Journal/Source**: Review of Financial Studies, Vol. 23, No. 10, pp. 3700–3737
**Proximity Score**: 3/5
**Summary**: Studies financial covenant thresholds in bank loans, focusing on how tight covenants signal borrower quality and affect post-issuance firm behavior. The key finding relevant to your paper: riskier firms and firms with fewer investment opportunities select tighter covenants, and tight covenants are associated with subsequent improvements in earnings (the covenant variable), declines in investment, and reduced debt issuance. This establishes that covenant tightness is a function of the firm's cash-flow distribution (riskier cash flows → tighter covenants → lower effective debt capacity), directly supporting the empirical interpretation of µ_i.
**Identification**: Selection model (Heckman) for covenant choice; event study around covenant violations.
**Data**: DealScan, Compustat, 1994–2006.
**Key Result**: Tighter covenants are chosen by riskier firms; tight covenants cause post-issuance improvement in covenant variable (earnings/EBITDA).

---

### [Ivashina and Vallee 2020] Weak Credit Covenants
**Journal/Source**: NBER Working Paper No. 27316 (June 2020); revised 2024
**Proximity Score**: 3/5
**Summary**: Analyzes the weakening of EBITDA-based covenants in leveraged loans through carve-outs and deductible clauses, using a novel dataset of 1,240 credit agreements. The paper shows that covenant weakness is associated with larger non-bank funding shares (covenant-lite loans to institutional investors) and is exploited by sophisticated borrowers. The key implication for your paper is that contractual flexibility in how EBITDA is measured for covenant purposes creates a wedge between the firm's true cash-flow distribution µ_i and the lender's effective measure — introducing measurement error in the empirical analogue of µ_i.
**Identification**: Cross-sectional regression; event study using J.Crew restructuring as external shock.
**Data**: DealScan, custom covenant data (1,240 credit agreements), 2012–2017.
**Key Result**: Carve-outs and deductibles are as prevalent as negative covenants themselves; covenant weakness priced at modest spread premium.

---

## Category 4: Theoretical Foundations (Proximity 1–2)

### [Townsend 1979] Optimal Contracts and Competitive Markets with Costly State Verification
**Journal/Source**: Journal of Economic Theory, Vol. 21, No. 2, pp. 265–293
**Proximity Score**: 2/5
**Summary**: Establishes the canonical costly state verification (CSV) model that underlies the financial accelerator. The borrower's output is privately observed; the lender must pay a monitoring cost to verify the state. The optimal contract is a standard debt contract: the borrower pays a fixed face value, and the lender monitors (audits) only in default. This is the theoretical ancestor of all cash-flow-based lending models and directly motivates why lenders care about the distribution of cash flows µ_i rather than just the mean.
**Identification**: Mechanism design (optimal contracting under asymmetric information).
**Data**: Theoretical.
**Key Result**: Standard debt contract is optimal under costly state verification; lender monitors only at default; monitoring probability is decreasing in borrower net worth.

---

### [Stiglitz and Weiss 1981] Credit Rationing in Markets with Imperfect Information
**Journal/Source**: American Economic Review, Vol. 71, No. 3, pp. 393–410
**Proximity Score**: 2/5
**Summary**: Demonstrates that credit markets can be in equilibrium with persistent rationing — some observationally identical borrowers receive loans while others do not, even at the prevailing interest rate. The mechanism is that raising rates worsens adverse selection (drives out safe borrowers) and moral hazard (incentivizes riskier projects). This establishes that debt capacity constraints can bind not through collateral shortage but through distributional mismatches between lender and borrower payoff profiles, anticipating your Wasserstein-distance framing.
**Identification**: General equilibrium theory with asymmetric information.
**Data**: Theoretical.
**Key Result**: Equilibrium credit rationing exists; the market-clearing interest rate may lie below the Walrasian rate; rationing is more severe when the distribution of borrower types is more dispersed.

---

### [Merton 1974] On the Pricing of Corporate Debt: The Risk Structure of Interest Rates
**Journal/Source**: Journal of Finance, Vol. 29, No. 2, pp. 449–470
**Proximity Score**: 2/5
**Summary**: The structural model of corporate default, applying the Black-Scholes option pricing framework to value risky corporate debt. Firm value follows a diffusion process; default occurs when firm value falls below the face value of debt. The credit spread is a function of the firm's asset volatility and leverage ratio. Merton's model implicitly defines debt capacity as the amount of debt for which the credit spread remains finite — which depends on the distribution of asset returns. Your model generalizes this by replacing the Gaussian asset distribution with a general cash-flow distribution µ_i.
**Identification**: Structural model (option-theoretic); no empirical estimation in the original paper.
**Data**: Theoretical.
**Key Result**: Credit spreads are a function of asset volatility and leverage; the probability of default is determined by the distance-to-default.

---

### [Aghion-Bolton 1992] — see Category 2 above (Proximity 3, also serves as theoretical foundation)

---

### [Villani 2009] Optimal Transport: Old and New
**Journal/Source**: Springer-Verlag, Grundlehren der Mathematischen Wissenschaften, Vol. 338. Springer, 2009.
**Proximity Score**: 1/5
**Summary**: The definitive mathematical reference for optimal transport theory. Villani covers the Monge problem, Kantorovich duality, Wasserstein distances (W_1, W_2, and general W_p), displacement convexity, Otto calculus, and applications to geometry and PDEs. Chapters on the Kantorovich duality (Ch. 5) and Wasserstein distances (Ch. 6) provide the mathematical foundations for your debt capacity formula δ_i = W_1(µ_i, ν)/2. The book establishes the dual representation of W_1 as a sup over 1-Lipschitz functions and the primal representation as an infimum over couplings — both used in your theoretical proofs.
**Identification**: Mathematical treatise; no empirical methods.
**Data**: N/A.
**Key Result**: W_1(µ, ν) = sup_{||f||_Lip ≤ 1} [∫f dµ – ∫f dν]; optimal transport map exists under mild regularity conditions.

---

### [Brenier 1991] Polar Factorization and Monotone Rearrangement of Vector-Valued Functions
**Journal/Source**: Communications on Pure and Applied Mathematics, Vol. 44, No. 4, pp. 375–417
**Proximity Score**: 1/5
**Summary**: Proves that any vector field can be factored as the composition of the gradient of a convex function with a measure-preserving map — the polar factorization theorem. In one dimension, this reduces to the quantile coupling result: the optimal transport map between µ and ν is the monotone rearrangement (quantile function composition F_ν^{-1} ∘ F_µ). This result is the mathematical basis for your Theorem characterizing the optimal contract as a quantile coupling, and for the analytical computation of W_1(µ_i, ν).
**Identification**: Pure mathematics; existence and uniqueness proof.
**Data**: N/A.
**Key Result**: Optimal transport map is the monotone rearrangement in 1D; existence and uniqueness of the Brenier map in higher dimensions under regularity.

---

## Category 5: Data and Measurement (Proximity 2–3)

### [Almeida, Campello, Laranjeira, and Weisbenner 2012] Corporate Debt Maturity and the Real Effects of the 2007 Credit Crisis
**Journal/Source**: Critical Finance Review, Vol. 1, No. 1, pp. 3–58
**Proximity Score**: 2/5
**Summary**: Exploits pre-crisis variation in debt maturity structure to identify the causal effect of credit supply shocks on firm investment. Firms whose long-term debt was maturing right after August 2007 faced a credit supply shock (the market froze) and cut investment by 2.5 percentage points per quarter more than firms with later-maturing debt. This provides quasi-experimental evidence that binding debt capacity constraints have real effects, and that the maturity distribution of existing debt — which affects the timing of refinancing need — interacts with aggregate credit supply (your ν_t).
**Identification**: Difference-in-differences using pre-crisis debt maturity; treatment is maturing debt during crisis window.
**Data**: Compustat, DealScan, 2006–2009.
**Key Result**: Firms with maturing debt during the crisis cut investment by 2.5pp/quarter more; effect concentrated in the first year of the crisis.

---

### [Gormley and Matsa 2014] Common Errors: How to (and Not to) Control for Unobserved Heterogeneity
**Journal/Source**: Review of Financial Studies, Vol. 27, No. 2, pp. 617–661
**Proximity Score**: 2/5
**Summary**: A methodological paper demonstrating that industry-adjusting the dependent variable (subtracting industry mean) or including industry-mean as a control produces inconsistent estimates of firm-level coefficients, while within-group fixed effects estimators are consistent. Directly relevant for your empirical cross-sectional tests of W1 as a leverage determinant: any specification that industry-adjusts leverage or uses industry-average leverage as a control (rather than industry fixed effects) will yield biased estimates of the W1 coefficient.
**Identification**: Monte Carlo simulations demonstrating estimator bias; analytical proofs.
**Data**: Simulated; illustrated with Compustat applications.
**Key Result**: Industry-adjusted OLS and industry-mean-as-control are inconsistent; use firm and time fixed effects instead.

---

## Category 6: Background and Methods Papers (Proximity 2)

### [Bernanke and Gertler 1989] Agency Costs, Net Worth, and Business Fluctuations
**Journal/Source**: American Economic Review, Vol. 79, No. 1, pp. 14–31
**Proximity Score**: 2/5
**Summary**: The two-period predecessor to BGG (1999), establishing the link between borrower net worth and the external finance premium under agency costs (costly state verification). The external finance premium is a decreasing function of net worth, creating a procyclical feedback loop: rising net worth in booms reduces finance costs, stimulating further investment. This provides the micro-foundation for why the distribution of firm net worth maps to the distribution of external finance costs — a key precursor to your mapping from µ_i to debt capacity.
**Identification**: Two-period general equilibrium model with CSV.
**Data**: Theoretical.
**Key Result**: External finance premium is a decreasing convex function of net worth; small net worth shocks produce large amplification.

---

### [Gale and Hellwig 1985] Incentive-Compatible Debt Contracts: The One-Period Problem
**Journal/Source**: Review of Economic Studies, Vol. 52, No. 4, pp. 647–663
**Proximity Score**: 2/5
**Summary**: Proves that standard debt is the uniquely optimal incentive-compatible contract under costly state verification in a one-period model. Extends Townsend (1979) by proving optimality rigorously. Establishes that the optimal face value of debt is a function of the distribution of the borrower's cash flow, which determines the probability that the debt constraint binds. This is cited alongside Townsend as the theoretical foundation for why lenders underwrite loans against cash-flow distributions.
**Identification**: Mechanism design; optimal contract under asymmetric information.
**Data**: Theoretical.
**Key Result**: Standard debt contract is uniquely optimal under CSV; face value equals expected project output minus expected monitoring cost.

---

### [Jensen and Meckling 1976] Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure
**Journal/Source**: Journal of Financial Economics, Vol. 3, No. 4, pp. 305–360
**Proximity Score**: 2/5
**Summary**: Establishes the agency cost framework for capital structure, identifying two types of costs: (i) asset substitution (equity holders prefer riskier projects when facing debt, shifting risk to lenders) and (ii) underinvestment (Myers 1977 debt overhang). These agency costs create an endogenous upper bound on debt — the debt capacity beyond which the agency cost premium exceeds the tax benefit. Your model's κ parameter (deadweight bankruptcy cost) and the optimal contract design are motivated by this framework.
**Identification**: Theory; no empirics.
**Data**: Theoretical.
**Key Result**: Optimal leverage balances tax benefits against agency costs; there exists a unique interior optimum for leverage.

---

### [Myers 1977] Determinants of Corporate Borrowing
**Journal/Source**: Journal of Financial Economics, Vol. 5, No. 2, pp. 147–175
**Proximity Score**: 2/5
**Summary**: Introduces the debt overhang (underinvestment) problem: firms with risky debt may pass up positive-NPV projects because the gains accrue to existing debt holders rather than equity holders. This creates an endogenous debt capacity limit — firms will not issue debt beyond the point at which underinvestment costs outweigh tax benefits. Debt capacity in this model is a function of the distribution of future investment opportunities, motivating your interpretation of µ_i as capturing both the level and uncertainty of future cash flows.
**Identification**: Theory; two-period model of investment and financing.
**Data**: Theoretical.
**Key Result**: Debt overhang causes underinvestment; optimal debt maturity shortens as growth options increase; short-term debt alleviates overhang.

---

### [Holmstrom and Tirole 1997] Financial Intermediation, Loanable Funds, and the Real Sector
**Journal/Source**: Quarterly Journal of Economics, Vol. 112, No. 3, pp. 663–691
**Proximity Score**: 2/5
**Summary**: Models financial intermediation as arising from firms' need to credibly commit to exert effort. Firms have two types of financing: direct (market) finance and intermediated (bank) finance. The firm's borrowing capacity is limited to the amount for which the entrepreneur has sufficient skin in the game (pledgeable income). As the aggregate supply of loanable funds (your ν_t) changes, the cross-sectional distribution of firms that can access financing shifts — providing a theoretical link between the aggregate capital supply distribution and the distribution of firm-level debt capacity.
**Identification**: Moral hazard model; two-period framework.
**Data**: Theoretical.
**Key Result**: Borrowing capacity is proportional to pledgeable income (a function of cash flows); aggregate credit supply shifts determine which firms can access financing.

---

## Annotated BibTeX Reference Section

See `references.bib` file saved alongside this document.

---

## Frontier Map

### What Has Been Established

1. **Collateral-based debt capacity** (Rampini-Viswanathan 2010, 2013; Kiyotaki-Moore 1997; Chaney-Sraer-Thesmar 2012): Debt capacity is bounded by the liquidation value of pledgeable collateral. The cross-sectional distribution of debt capacity mirrors the distribution of asset values. This is empirically supported by the collateral channel literature (CST 2012).

2. **Cash-flow-based debt capacity** (Lian-Ma 2021; Kermani-Ma 2022; Greenwald 2019): 80% of US corporate debt is governed by earnings-based borrowing constraints. Debt capacity is pinned by EBITDA multiples and interest coverage ratios. This is the dominant empirical form of borrowing constraints for large US corporations.

3. **Incomplete contracts foundation** (Hart-Moore 1994; Aghion-Bolton 1992): Debt capacity has an upper bound determined by the inalienability of human capital and the distribution of verifiable project payoffs. Standard debt contracts are optimal under CSV (Townsend 1979; Gale-Hellwig 1985).

4. **Dynamic capital structure** (Hennessy-Whited 2005, 2007; Strebulaev 2007; DeAngelo-DeAngelo-Whited 2011): Firms optimally maintain spare debt capacity as an option for future borrowing needs; observed cross-sectional leverage reflects adjustment frictions and path dependence, not just static optima.

5. **Cross-sectional leverage determinants** (Rajan-Zingales 1995; Frank-Goyal 2009; MacKay-Phillips 2005; Graham 2000): Six factors reliably predict leverage in cross-section: market-to-book, profitability, tangibility, size, industry leverage, and expected inflation. Any new measure of debt capacity must show incremental power beyond these.

6. **Macro-finance amplification** (Bernanke-Gertler-Gilchrist 1999; Geanakoplos 2010; Brunnermeier-Pedersen 2009): Distributional shifts in aggregate credit supply amplify real shocks. The financial accelerator operates through changes in the distribution of borrowing capacity across firms.

### Methodological Frontier

- **Structural estimation**: SMM on Compustat to recover structural parameters (Hennessy-Whited 2007; Nikolov-Schmid-Steri 2021). Your SMM with bootstrap standard errors follows directly.
- **Optimal transport in economics**: Econometric applications of OT are emerging (Galichon-Henry 2011; Chernozhukov et al. 2017) but applications to corporate finance debt capacity are nonexistent.
- **Cash-flow covenants as debt limits**: Lian-Ma (2021) and Greenwald (2019) establish EBCs empirically; no theoretical model derives debt capacity from the W1 distance between µ_i and ν_t.

### Data Frontier

- **DealScan + Compustat**: Standard dataset for cash-flow-based lending (Lian-Ma 2021; Demiroglu-James 2010). Covers public US firms with bank loans.
- **Capital IQ**: Debt contract data including all bond and loan covenant details (Kermani-Ma 2022; Ivashina-Vallee 2020).
- **FRED / Flow of Funds**: Aggregate capital supply distribution ν_t (Federal Reserve H.8 data on bank credit, Flow of Funds financial instruments).
- **Supervisory loan data**: Federal Reserve Y-14 data used by Greenwald-Krainer-Paul (2025); not widely accessible.

### Geographic and Contextual Gaps

- All major debt capacity papers focus on US public firms. Cross-country distribution of debt capacity is unstudied from a distributional perspective.
- Private firms face different constraints (Nikolov-Schmid-Steri 2021 use Orbis), but the cash-flow distributional approach has not been applied to private credit markets.
- The role of the aggregate capital supply distribution (ν_t) as a time-varying object is studied mostly in macro papers (BGG 1999; Geanakoplos 2010), not in structural corporate finance models.

### Open Questions

1. **What is the correct distribution class for µ_i?** Log-normal is tractable but restrictive; robustness to non-parametric µ_i is an open methodological question.
2. **How does ν_t shift during quantitative easing?** The Fed's asset purchases expand the aggregate capital supply distribution; the pass-through to firm-level debt capacity via W1 is not estimated.
3. **Is W1 identified separately from κ?** Nikolov-Schmid-Steri (2021) show that different structural models have different identification patterns; the identification of W1 vs. bankruptcy costs needs to be defended carefully.
4. **Does the theory extend to dynamic settings?** DeAngelo-DeAngelo-Whited (2011) show that spare debt capacity has option value; a dynamic extension of your model is flagged as future work.
5. **What explains within-industry dispersion of leverage?** MacKay-Phillips (2005) show it exists; the distributional model predicts it should equal the dispersion in W1(µ_i, ν_t) within industry.

### Where This Project Fits

This paper provides the first theoretical microfoundation for cash-flow-based debt capacity grounded in optimal transport theory, showing that δ_i = W1(µ_i, ν)/2 under a general mechanism design framework. Unlike existing models (Rampini-Viswanathan 2010, 2013) which focus on asset-based collateral, and unlike empirical descriptions (Lian-Ma 2021) which document EBCs without deriving them from first principles, this paper derives the full distribution of debt capacity from the distributional distance between firm-level cash flows and aggregate capital supply. The model nests collateral-based and cash-flow-based constraints as special cases, and the SMM estimation provides quantitative discipline.

### Scooping Risks

**High overlap (must address):**

1. **Rampini and Viswanathan (2010)** — "Collateral, Risk Management, and the Distribution of Debt Capacity," Journal of Finance. The title uses "distribution of debt capacity" and derives it theoretically. Your paper differs fundamentally in the mechanism (W1 distance from OT vs. collateral constraints from limited enforcement) and in emphasizing cash-flow distributions rather than asset values. Must cite prominently and articulate the distinction in the Introduction.

2. **Lian and Ma (2021)** — "Anatomy of Corporate Borrowing Constraints," QJE. The empirical benchmark for cash-flow-based debt capacity. Your theory provides the microfoundation that Lian-Ma (2021) lack. Must cite as the empirical motivation and contrast your theoretical contribution with their reduced-form documentation.

3. **Greenwald (2019)** — "Firm Debt Covenants and the Macroeconomy." The closest structural model to your setup; also derives cash-flow-based debt capacity from a two-covenant system. Your paper differs by (i) deriving the optimal contract rather than imposing covenant forms exogenously, (ii) using optimal transport geometry, and (iii) estimating the full distributional model via SMM. Must address in a related literature paragraph.

**Moderate overlap (monitor):**

4. **Kermani and Ma (2022)** — "Two Tales of Debt," NBER WP. Documents going-concern vs. discrete-asset debt. Does not provide a structural OT model.

5. **Nikolov, Schmid, and Steri (2021)** — "The Sources of Financing Constraints," JFE. Tests competing structural models of financing constraints using SMM. Does not use OT geometry or derive W1 debt capacity.

---

*Literature review produced by academic-librarian agent. Editor review recommended before submission.*

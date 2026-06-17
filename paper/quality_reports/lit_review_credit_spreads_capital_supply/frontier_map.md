# Frontier Map: Credit Spreads, Capital Supply Dynamics, and the Cross-Section of Corporate Leverage

**Project**: Distributional Debt Capacity (Optimal Transport / Wasserstein)
**Compiled**: 2026-06-14

---

## What Has Been Established

### On Credit Spread Levels and the Credit Spread Puzzle

The canonical observation (Huang-Huang 2012; Collin-Dufresne et al. 2001) is that standard structural models calibrated to historical default rates systematically underprice observed corporate bond spreads, especially for investment-grade firms. The "credit spread puzzle" has generated a large literature. Chen et al. (2009) resolve it by incorporating countercyclical risk premia (default rates and risk premia covary); Feldhutter-Schaefer (2018) argue the puzzle is less severe with proper calibration methods; Huang-Nozawa-Shi (2025) document it is a global phenomenon that liquidity models only partially address. The consensus is that credit spreads contain both a default component and a substantial non-default component (risk premia + liquidity + supply constraints).

### On Credit Spread Changes (Time-Series)

Collin-Dufresne et al. (2001) establish that a single common factor drives ~75% of spread variation that is unexplained by standard credit risk variables. Gilchrist-Zakrajsek (2012) operationalize this residual as the "excess bond premium" (EBP), which reflects the risk-bearing capacity of the financial sector and predicts GDP growth. He-Krishnamurthy (2013), Adrian-Etula-Muir (2014), and He-Kelly-Manela (2017) provide the intermediary asset pricing framework: when intermediary capital is scarce, risk premia in credit markets rise. This literature establishes that aggregate capital supply conditions — not just borrower fundamentals — drive time-series variation in spreads.

### On the Cross-Section of Credit Spreads

Nozawa (2017) is the definitive decomposition: expected returns account for roughly as much cross-sectional spread variance as expected credit losses. Flannery-Nikolova-Oztekin (2012) show that leverage expectations matter beyond contemporaneous leverage. Kuehn-Schmid (2014) show investment options matter beyond leverage and volatility. However, no existing paper explains the cross-section of spreads through the distributional distance between borrower cash flows and aggregate capital supply — this is the gap the project fills.

### On Aggregate Capital Supply Dynamics

The intermediary finance literature (He-Krishnamurthy 2013; Brunnermeier-Sannikov 2014; Adrian-Shin 2010, 2014) documents that financial intermediary balance sheets are the key transmission mechanism for capital supply conditions. Procyclical leverage creates amplification: capital supply expands in booms, contracts in busts. This literature, however, characterizes aggregate capital supply with a scalar (leverage ratio, capital ratio) rather than a distribution.

### On Capital Supply Heterogeneity and Lender Composition

Becker-Ivashina (2015) establishes that insurance companies systematically reach for yield within rating categories, showing lender preferences are heterogeneous. Chernenko-Sunderam (2012) shows that flows into high-yield mutual funds have real effects on speculative-grade firms — demonstrating credit market segmentation. Bretscher et al. (2026) is the most comprehensive recent treatment: using a demand-system equilibrium model with TRACE data, they show institutional demand composition is a state variable for corporate bond pricing. Koijen-Yogo (2023) explains why insurers hold corporate bonds in equilibrium through a leverage-recycling mechanism.

### On TRACE Methodology

Dick-Nielsen et al. (2012), Bao-Pan-Wang (2011), and Friewald et al. (2012) establish TRACE as the authoritative dataset for corporate bond liquidity research and provide the benchmark illiquidity measures. Goldberg-Nozawa (2021) identify dealer capacity shocks as drivers of corporate bond liquidity supply using TRACE. Chen-Cui-He-Milbradt (2018) provide the structural framework for decomposing TRACE spreads into default and liquidity components. The literature has converged on controlling for illiquidity (γ measure, price impact, bid-ask) when estimating credit spread regressions.

---

## Methodological Frontier

### Most Advanced Identification Strategies Used To Date

1. **Demand-system estimation (Bretscher et al. 2026; Koijen-Yogo 2019, 2023)**: Equilibrium pricing model with heterogeneous institutional demand, estimated on holdings data with IV. Current frontier for supply-side corporate bond pricing.

2. **Structural equilibrium models with intermediary frictions (He-Krishnamurthy 2013; Brunnermeier-Sannikov 2014; Gomes-Schmid 2021)**: Continuous-time or heterogeneous-agent models calibrated to macro moments. Frontier for jointly explaining spreads and leverage dynamics.

3. **Intermediary SDF pricing (Adrian-Etula-Muir 2014; He-Kelly-Manela 2017)**: Broker-dealer or Primary Dealer leverage/capital as a stochastic discount factor. Best empirical proxy for aggregate capital supply conditions to date.

4. **EBP decomposition (Gilchrist-Zakrajsek 2012)**: Decomposes bond-level spreads into default and non-default components using micro pricing. Gold standard for identifying the supply-side component of spread variation.

5. **SMM/BLP structural estimation (Berry-Levinsohn-Pakes 1995)**: Simulated Method of Moments for structural models. The methodological template for the paper's estimation of θ = (α_ν, σ_ν, κ).

### What Does Not Yet Exist

- No paper characterizes the capital supply side as a **distribution** (νt) rather than a scalar.
- No paper formalizes the matching between borrower cash flow distributions and capital supply distributions using optimal transport.
- No paper derives the Wasserstein distance as the sufficient statistic for individual debt capacity and firm leverage.
- No paper uses the Fréchet mean of firm cash flow distributions as an estimator for the aggregate capital supply distribution.

---

## Data Frontier

**Most comprehensive datasets used to date:**
- **TRACE** (2002–present): Complete OTC corporate bond transaction data; used by Goldberg-Nozawa (2021), Bretscher et al. (2026), Chen-Cui-He-Milbradt (2018). The paper's 2012–2024 sample is fully within TRACE coverage.
- **NAIC insurance holdings** (quarterly): Used by Becker-Ivashina (2015), Bretscher et al. (2026). Most granular lender-level data.
- **eMAXX institutional holdings**: Used by Bretscher et al. (2026). Comprehensive across institutions.
- **Federal Reserve Flow of Funds / Z.1**: Used by Adrian-Shin (2010, 2014), Adrian-Etula-Muir (2014). Standard source for aggregate intermediary balance sheets. The paper uses this to anchor νt.
- **Compustat Quarterly**: Standard panel source for μit (firm cash flow distribution). The paper's 5-year rolling window is comparable to the 10-year samples in Nozawa (2017) and Gomes-Schmid (2021).
- **Lehman/Merrill bond databases (pre-TRACE)**: Used by Gilchrist-Zakrajsek (2012) and Nozawa (2017) for long historical samples. The paper's TRACE-only focus limits pre-2012 comparisons.

---

## Geographic and Contextual Gaps

- **U.S.-centric**: Nearly all papers focus on U.S. corporate bond markets. Huang-Nozawa-Shi (2025) is the first to document a global credit spread puzzle across 8 countries, but does not study supply-side distributions.
- **Post-financial crisis period**: The paper's 2012–2024 TRACE sample is the most recent long window in this literature; most structural models are calibrated to pre-2010 data.
- **Non-financial firms**: Standard exclusion of SIC 6000–6999 (financials) and 4900–4999 (utilities) leaves manufacturing and services sectors as the universe. No paper studies distributional matching across sectors.
- **Small and unrated firms**: Most bond-market papers use rated, publicly traded firms. The paper's TRACE scope similarly excludes private borrowers.

---

## Open Questions and Debates

1. **The credit spread puzzle**: Is it genuine (models too simple) or calibration artefact (Feldhutter-Schaefer 2018)? The emerging consensus is that both liquidity and time-varying risk premia are necessary. The paper adds a third element: distributional mismatch between borrower and lender.

2. **What drives the common factor in CDG (2001)?** The single factor explains ~75% of residual spread variation. Gilchrist-Zakrajsek call it the EBP; Adrian et al. call it intermediary leverage; this paper argues it is the Fréchet mean of νt.

3. **Composition vs. level of capital supply**: Bretscher et al. (2026) show demand composition matters; this paper argues the distributional distance W1(μit, νt) is the sufficient statistic. These are complementary, not competing, claims — but the paper must demonstrate the W1 measure contains information orthogonal to Bretscher et al.'s demand composition variables.

4. **Cross-sectional vs. time-series identification**: Most papers study time-series variation in spreads; Nozawa (2017) and the present paper study the cross-section. Reconciling both dimensions is an ongoing challenge.

5. **Dynamic vs. static framework**: The credit spread literature is dominated by dynamic models (Leland 1994; Gomes-Schmid 2021). The paper's static optimal transport gives exact analytical results unavailable in dynamic models; this trade-off requires explicit defense.

---

## Where This Project Fits

The project occupies a gap at the intersection of three active lines of research: (1) the credit spread decomposition literature, which has identified an unexplained supply-side common factor in spread variation but has not characterized it distributionally; (2) the intermediary asset pricing literature, which has shown that capital supply conditions drive risk premia but treats supply as a scalar; and (3) the demand-system corporate bond pricing literature (Bretscher et al. 2026), which captures lender heterogeneity but does not formalize the matching between borrower distributions and lender distributions. The paper introduces the Wasserstein distance between firm cash flow distributions and aggregate capital supply distribution as the object that simultaneously determines individual debt capacity (via W1) and aggregate deadweight cost (via W2), providing both an equilibrium theory and an SMM estimator validated against TRACE and FRED.

---

## Scooping Risks

### Proximity 5 — Direct Competitors

**None identified** with exactly the same framework (Wasserstein distance between cash flow and capital supply distributions). However, the following working papers represent elevated scooping risk:

1. **Bretscher, Schmid, Sen, Sharma (RFS 2026 — already published)**: "Institutional Corporate Bond Pricing." Uses a demand-system equilibrium model of institutional bond pricing with heterogeneous lender preferences. Now published in RFS as Lead Article. This is not a working paper but a published competitor that must be directly addressed. The key differentiator is that they use a demand-system approach with observed heterogeneity; this paper uses an optimal transport approach with the Fréchet mean and distributional distance. These are complementary frameworks; the paper should cite Bretscher et al. as providing reduced-form evidence consistent with the W1 channel.

2. **Goldberg, Nozawa (JF 2021)**: "Liquidity Supply in the Corporate Bond Market." Uses dealer inventory data from TRACE to study supply-side shocks. Published and cites the same data infrastructure. Key differentiator: Goldberg-Nozawa study liquidity supply (dealer capacity); this paper studies credit capacity (the capital supply distribution). Not directly competing but addresses adjacent question.

### Proximity 4 — Closely Related Working Papers to Monitor

3. **Koijen-Yogo (AEI 2023)**: Already published. Models insurance ownership in equilibrium. Must be cited as microfoundation for νt composition.

4. Any NBER/SSRN working papers in 2024–2026 combining "Wasserstein", "optimal transport", and "corporate debt" or "credit spreads" — no such paper was found as of the search date (2026-06-14), but the researcher should check SSRN directly for very recent uploads.

### Elevated Monitoring Recommended

- **RFS pipeline**: Bretscher et al. accepted 2025, published 2026 — suggests RFS is actively publishing institutional demand-side papers. Monitor for any follow-on work by the same authors.
- **JF pipeline**: Huang-Nozawa-Shi (2025) and Greenwald-Krainer-Paul (2025) are recent JF publications in adjacent space — suggests JF is receptive to TRACE-based supply-side papers.

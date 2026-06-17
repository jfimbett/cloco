# Frontier Map: Liquid Assets Literature
**Date:** 2026-03-30
**Project:** Liquid Assets (Imbet, Kräussl, Piatti, Steri)
**Compiled by:** Academic Librarian (cloco research system)

---

## What Has Been Established

### Wine as an Investment: Returns and Portfolio Diversification
The literature since Burton & Jacobsen (2001) and Sanning et al. (2008) has consistently found that investment-grade Bordeaux and Burgundy wines generate nominal returns of 5–9% per annum — broadly comparable to bonds but below equities — with low CAPM beta, significant positive alpha, and diversification benefits due to low equity correlation. Dimson, Rousseau & Spaenjers (2015, JFE) establish the most reliable long-run estimate: a net real return of 4.1% using arithmetic repeat-sales regression over 1900–2012. Masset & Henderson (2010) confirm similar returns for the U.S. auction market (Chicago Wine Company) over 1996–2007.

### Price-Age Profile: Non-Monotone Pattern Documented
Dimson, Rousseau & Spaenjers (2015) note that young maturing high-quality vintages generate the highest returns, while post-maturity wines deliver growing non-pecuniary benefits. Breeden & Liang (2017) formally document the non-monotone cubic age-price profile using APC decomposition: prices rise pre-maturity, plateau, then rise again at antique ages. Masset (2024) refines this by showing that the aggregate non-linearity is the composition of five distinct market segments (investment, collectible, drinking wines). The **empirical pattern is established**; the **structural explanation is not**.

### Heterogeneous Buyer Types: Motivating Evidence
Cardebat et al. (2017) establish that heterogeneous buyer preferences (not just transaction costs) explain why fine wine prices violate the law of one price across auction houses and geographies. Masset et al. (2016) show that Hong Kong premiums (proxy for collector/conspicuous buyers) reach 60% at peak and collapse to 15% post-2012 — directly tracing the China demand shock's differential impact on collector-type demand. Ginsburgh (1998) documents that institutional features of French wine auctions (absentee bidding, sequential lots) generate anomalous price dynamics consistent with heterogeneous bidder strategies.

### Art Market Structural Analogy
The art market literature provides the closest structural and theoretical antecedents:
- Lovo & Spaenjers (2018, AER) is the canonical two-type heterogeneous buyer model for collectibles markets.
- Mandel (2009, AER) provides a theoretical model where art prices reflect both investment and conspicuous consumption dividends, yielding low financial returns as an equilibrium outcome.
- Goetzmann et al. (2011) and Renneboog & Spaenjers (2013) document that art prices are driven by wealth-induced collector demand, not broad market conditions.
- Pénasse & Renneboog (2022) document that speculative extrapolation drives boom-bust cycles in art.

### China Demand Shock: Established Exogenous Variation
Qian & Wen (2015) establish that the 2012 Xi Jinping anti-corruption campaign reduced luxury imports — including wine and spirits — by approximately 55% (or ~47% for wine specifically). Masset et al. (2016) document the corresponding collapse in Hong Kong wine premiums. Bian et al. (2025) confirm price effects on Chinese art markets at the regional prosecution level. The shock is accepted in the literature as plausibly exogenous.

### Theoretical Foundations
Bagwell & Bernheim (1996) provide the theoretical condition under which Veblen effects (luxury pricing above marginal cost) arise as equilibrium. Scheinkman & Xiong (2003) show that speculative resale options generate price premiums that compound with belief heterogeneity. Tirole (1982) establishes the theoretical bound — speculative bubbles require heterogeneous priors. Together, these papers bound the theoretical space within which the Liquid Assets collector premium can operate.

---

## Methodological Frontier

### Identification Strategies in Wine Returns
1. **Repeat-sales regression** (Goetzmann 1993; Korteweg, Kräussl & Verwijmeren 2016): Standard for returns estimation but suffers from selection bias — bottles that trade twice are non-random. Korteweg et al. (2016) apply the Heckman correction: selection-corrected returns fall from 8.7% to 6.3%.
2. **APC decomposition** (Breeden & Liang 2017): State of the art for separating age, vintage quality, and time trends in wine prices; requires normalization constraint that imposes one restriction on the three collinear components.
3. **Hedonic regression with fixed effects** (Combris et al. 1997; Hadj Ali et al. 2008; Jones & Storchmann 2001): Standard for cross-sectional price determinants; vintage × château FE are the prevailing specification.
4. **Natural experiments for expert scores** (Hadj Ali et al. 2008): The 2003 Parker natural experiment is the cleanest causal identification in the wine pricing literature.
5. **DiD for demand shocks** (Masset et al. 2016; Cardebat & Jiao 2018): Used to study the China shock but not yet combined with structural demand model or maturity analysis.

### Structural Estimation of Auction Demand
The frontier in structural auction economics is nonparametric identification and estimation of private-value distributions from bid data (Guerre, Perrigne & Vuong 2000 in QJE; Paarsch & Hong 2006). Asker (2010) applies structural estimation to stamp dealer auctions — the closest published analogy for wine. Berry, Levinsohn & Pakes (1995) and Nevo (2001) provide the BLP demand estimation template for differentiated product markets. The Liquid Assets paper would be the first to apply structural demand estimation to wine auction data with explicit buyer-type separation.

### Structural Models of Collectibles
Lovo & Spaenjers (2018) is the frontier: an infinite-horizon IPV model where agents differ in private use value and sell upon liquidity shocks. Their model generates selection biases in observed prices and auction volume. Mandel (2009) is the theoretical antecedent with a simpler two-type framework. Neither paper estimates structural parameters empirically using auction data — the Liquid Assets paper would advance this frontier.

---

## Data Frontier

### Wine Auction Databases
- The largest published wine dataset is Breeden & Liang (2017) with 1.5 million auction results across multiple producers and regions.
- Dimson, Rousseau & Spaenjers (2015) use historical Christie's records back to 1900.
- Masset et al. (2016) use five global auction houses 2007–2014 but only for 14 iconic Bordeaux wines.
- The Liquid Assets dataset — 1,068,703 French fine-wine auction transactions (1996–2015), Bordeaux Crus Classés and Burgundy Premier/Grand Cru — is the largest single-market, single-country dataset in the literature, with substantially more coverage of vintage-château combinations than prior work.

### Maturity Ratings
No prior academic work has formally incorporated Tastingbook (wine maturity/drinking window estimates) into the analysis of price-age profiles. This is a novel data source in the literature. The closest analogy is the use of Parker scores as quality controls, but maturity windows are physically distinct from quality scores.

### Buyer Geography
Cardebat et al. (2017) and Masset et al. (2016) exploit geography as a proxy for buyer type (Hong Kong auctions = collector buyers; Western = consumption buyers). The Liquid Assets paper has buyer geography data within a single national market — a finer-grained identification approach that has not been exploited in prior published work.

---

## Geographic and Contextual Gaps

1. **French domestic auction market**: All major published work on wine investment uses data from London (Christie's, Sotheby's), Chicago, or multi-house global samples. There is no published paper with a comprehensive French domestic auction market dataset — a genuine geographic gap.

2. **Burgundy vs. Bordeaux structural comparison**: Prior hedonic work covers Burgundy (Combris et al. 2000) and Bordeaux separately, but no published structural model compares the two with a unified buyer-type framework. The paper's prediction that Burgundy Grand Cru exhibits a muted dip (high-entry-price screen) is untested in the literature.

3. **Maturity threshold as identification variable**: No published paper has used the maturity threshold as a structural feature to identify buyer types. This is a gap the Liquid Assets paper explicitly fills.

4. **Antique wines**: The post-maturity price recovery ("antique premium") is documented but unexplained in the literature. No paper identifies whether the antique premium is driven by scarcity, prestige, or collector-type dominance after consumption buyers exit.

---

## Open Questions in the Literature

1. **What drives the antique premium?** Is it scarcity (fewer bottles surviving), collector prestige compounding with age, or exit of consumption buyers? The literature notes it exists (Breeden & Liang 2017; Dimson et al. 2015) but does not decompose it.

2. **Who are the collector buyers, and how sensitive are they to demand shocks?** Masset et al. (2016) show the Hong Kong premium collapsed post-2012, but cannot distinguish which auction-market price segment (pre- vs. post-maturity) was most affected.

3. **Is the collector premium in wine driven by the same mechanism as in art?** The art literature documents that wealth inequality (Goetzmann et al. 2011), sentiment (Pénasse et al. 2014), and speculative extrapolation (Pénasse & Renneboog 2022) all contribute. Wine may have a different mechanism (biological scarcity, physical irreplaceability).

4. **Does the Veblen mechanism generate a structural break at entry price?** Bagwell & Bernheim (1996) predict that goods can serve both consumption and signaling functions, but the exact price threshold above which signaling dominates is not identified in the wine literature.

5. **Can structural demand estimation recover buyer-type shares?** The literature has not yet applied BLP-style or mixture-model structural demand estimation to wine auction data. The identification challenge is that wine lots are differentiated products with unobserved demand shocks.

6. **How persistent is the China demand shock effect?** Cardebat & Jiao (2018) show cointegration; Bian et al. (2025) find the effect fades over time in Chinese art markets. For wine, the question of whether the structural change is permanent or cyclical remains open.

---

## Where This Project Fits

The Liquid Assets paper occupies a novel position at the intersection of the wine investment literature (empirical documentation of price-age profiles) and the structural demand estimation literature (heterogeneous buyer models). No published paper has combined: (1) the non-monotone price-age regularity as the central empirical fact; (2) a structural model separating consumption vs. collector valuations; and (3) identification via an exogenous demand shock and cross-sectional variation in maturity thresholds. The paper advances beyond Breeden & Liang (2017) by providing a structural explanation, and beyond Lovo & Spaenjers (2018) by bringing the model to wine auction data with a novel identification strategy.

---

## Scooping Risks

The following working papers have overlapping questions and should be monitored:

| Paper | Authors | Date | Venue | Nature of Overlap |
|---|---|---|---|---|
| Verdickt (2025) | Gertjan Verdickt | August 2025 | SSRN #5386662 | Uses 68,000+ Bordeaux Premier Cru auction prices; studies investor climate attention effects on wine prices. Same wine types (Bordeaux Premier Cru), different question (climate vs. maturity/buyer-type). Not a scooping risk but uses closely related data. |

No proximity-5 scooping risk has been identified. The combination of French domestic auction data + structural demand model + maturity threshold identification + China shock is not in any published or circulating working paper as of 2026-03-30.

---

*Frontier map completed: 2026-03-30*

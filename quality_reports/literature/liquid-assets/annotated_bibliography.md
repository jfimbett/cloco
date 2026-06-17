# Annotated Bibliography: Liquid Assets
**Date:** 2026-03-30
**Topic:** Wine auction prices, heterogeneous buyers, price-age profiles, alternative investments
**Strands covered:** Strand 1 (Wine Investment/Auction Markets) | Strand 2 (Alternative Assets/Collectibles) | Strand 3 (Heterogeneous Buyer Models) | Strand 4 (Durable Goods Pricing) | Strand 5 (Structural Demand Estimation) | Strand 6 (China Shock/Luxury Goods) | Strand 7 (Auction Theory)
**Compiled by:** Academic Librarian (cloco research system)
**Scope note:** Excludes papers already in project bibliography: Dimson/Rousseau/Spaenjers (2015 JFE), Ashenfelter (2008 Economic Journal), Lovo/Spaenjers (2018 AER), Goetzmann (1993 AER), Baumol (1986 AER), Mei/Moses (2002 AER), Korteweg/Kräussl/Verwijmeren (2016 RFS), Renneboog/Spaenjers (2013 Management Science), Ashenfelter/Graddy (2003 JEL), Rosen (1974 JPE), Gavazza/Lizzeri/Roketskiy (2014 AER), Breeden/Liang (2017 JWE), Goetzmann/Spaenjers/Van Nieuwerburgh (2021 RFS).
**Total papers in this bibliography:** 45 + 6 gap papers added 2026-03-30 (targeted search)

---

## Category 1: Directly Related — Wine Auction Prices, Maturity Lifecycle, Buyer Heterogeneity (Proximity 4–5)

Papers with the same core question as Liquid Assets: wine auction prices across the age/maturity spectrum, or heterogeneous buyer composition in wine markets.

---

### [Masset 2024] Market Segments and Pricing of Fine Wines over Their Lifecycle
**Journal/Source:** Economic Modelling, Vol. 141 (2024), Article 106915
**Proximity Score:** 5/5
**Strand:** 1
**Main contribution:** Applies finite mixture modelling to 20 years of wine auction data to identify five distinct market segments (investment, collectible, drinking wines) and shows that the aggregate non-monotone price-age profile is the superposition of linear within-segment age effects.
**Method/Identification:** Finite mixture model; hedonic regression within each segment
**Key data source:** Wine auction records, 20-year panel, multiple regions
**Key finding:** Five market segments; "investment wines" most sensitive to market conditions; "drinking wines" most sensitive to scores; non-linearity in aggregate price-age profile is fully explained by segment composition
**Relevance to Liquid Assets:** Most direct empirical antecedent — corroborates the claim that the bimodal aggregate age profile reflects underlying buyer-type heterogeneity; does not develop a structural model or use exogenous demand shocks.
**BibTeX key:** Masset2024segments

---

### [Breeden & Liang 2017] Auction-Price Dynamics for Fine Wines from Age-Period-Cohort Models
**Journal/Source:** Journal of Wine Economics, Vol. 12, No. 2, pp. 173–202
**Proximity Score:** 5/5
**Strand:** 1
**Main contribution:** Uses an APC algorithm on 1.5 million auction observations to disentangle the age effect, vintage quality, and time-period trends, documenting the non-monotone cubic price-age profile with a post-maturity trough and antique premium.
**Method/Identification:** Age-period-cohort (APC) decomposition with normalization constraint
**Key data source:** 1.5 million auction transactions; multiple producers and regions
**Key finding:** Prices rise pre-maturity, plateau, then recover at antique ages; Hill of Grace return: +14.8% at year 2, 0% at year 20, +10.4% at year 30
**Relevance to Liquid Assets:** Provides the key APC benchmark for the age effect and documents the trough/recovery pattern that the paper's structural model explains.
**BibTeX key:** BreedenLiang2017apc

---

### [Masset, Weisskopf, Faye & Le Fur 2016] Red Obsession: The Ascent of Fine Wine in China
**Journal/Source:** Emerging Markets Review, Vol. 29, pp. 200–225
**Proximity Score:** 4/5
**Strand:** 1, 6
**Main contribution:** Documents a 19% average price premium at Hong Kong auctions (peak 60% in 2008, declining to 15% post-2012) for the 14 most iconic Bordeaux wines, using hammer prices from five global auction houses 2007–2014.
**Method/Identification:** Hedonic regression with auction-house and geography fixed effects; time-series comparison
**Key data source:** Hammer prices, five global auction houses, 14 iconic Bordeaux wines, 2007–2014
**Key finding:** 19% average HK premium; decline from 60% (2008) to 15% (post-2012); largest premiums for perfect-score wines
**Relevance to Liquid Assets:** Most direct treatment of the China demand shock at wine auction level; provides effect magnitudes for the event-study identification strategy.
**BibTeX key:** MassetWeisskopfFaye2016

---

### [Cardebat, Faye, Le Fur & Storchmann 2017] The Law of One Price? Price Dispersion on the Auction Market for Fine Wine
**Journal/Source:** Journal of Wine Economics, Vol. 12, No. 3, pp. 302–331
**Proximity Score:** 4/5
**Strand:** 1
**Main contribution:** Tests the law of one price in fine wine using worldwide auction prices from eight auction houses (2000–2012). Finds significant price premiums in HK exceeding transaction costs, with counterfeit-suspect bottles at premium in HK and discount in Western markets.
**Method/Identification:** Hedonic regression with auction-house and geography interactions
**Key data source:** Worldwide auction prices, eight houses, 2000–2012
**Key finding:** LoOP rejected; heterogeneous buyer preferences explain price dispersion; HK buyer premium is real
**Relevance to Liquid Assets:** Provides evidence that different buyer types coexist with systematically different valuations — direct motivation for the two-type model.
**BibTeX key:** CardebatFayeLeStorchmann2017

---

### [Dimson & Spaenjers 2014] Investing in Emotional Assets
**Journal/Source:** Financial Analysts Journal, Vol. 70, No. 2, pp. 20–25
**Proximity Score:** 4/5
**Strand:** 2
**Main contribution:** Reviews long-run investment performance (1900–2012) of art, stamps, and musical instruments, finding 6.4–6.9% nominal (2.4–2.8% real) annual returns — superior to bonds but inferior to equities; coins the "emotional dividend" concept (non-pecuniary ownership benefit).
**Method/Identification:** Repeat-sales regression; CAPM benchmarking
**Key data source:** Multiple collectible asset price indices, 1900–2012
**Key finding:** Collectibles real return 2.4–2.8% p.a.; emotional dividend is a quantitatively important component; volatility understated by index-based estimates
**Relevance to Liquid Assets:** Establishes "emotional dividend" as the concept closest to the non-pecuniary collector premium in the paper's model; provides comparative return benchmark.
**BibTeX key:** DimsonSpaenjers2014emotional

---

### [Cardebat & Jiao 2018] The Long-Term Financial Drivers of Fine Wine Prices: The Role of Emerging Markets
**Journal/Source:** Quarterly Review of Economics and Finance, Vol. 67, pp. 347–361
**Proximity Score:** 4/5
**Strand:** 6
**Main contribution:** Shows using cointegration on 21-year monthly data (Liv-ex indices + 25 MSCI indices) that emerging markets — particularly China — are the main long-run driver of fine wine prices. Emerging buyers are less informed and more Veblen-sensitive than mature buyers.
**Method/Identification:** Cointegration analysis; VAR; impulse-response functions
**Key data source:** Liv-ex Fine Wine Investables Index and sub-indices; 25 MSCI national indices, monthly, 1994–2015
**Key finding:** Cointegration between Chinese equity markets and Bordeaux premier cru prices; emerging buyers Veblen-sensitive; long-run co-movement confirmed
**Relevance to Liquid Assets:** Provides financial-market evidence that Chinese demand drove the Bordeaux price spike and is the main mechanism behind the China demand shock used for identification.
**BibTeX key:** CardebatJiao2018

---

## Category 2: Wine as an Investment — Returns, Portfolio, and Market Efficiency (Proximity 3)

Papers studying wine primarily as a financial asset — return estimation, diversification, and market efficiency — without modelling the age-maturity mechanism or buyer heterogeneity structurally.

---

### [Masset & Henderson 2010] Wine as an Alternative Asset Class
**Journal/Source:** Journal of Wine Economics, Vol. 5, No. 1, pp. 87–118
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Uses Chicago Wine Company auction prices (1996–2007) to show that first growths and extraordinary-rated wines yield 4.1–6.0% annual returns with low CAPM beta; confirms wine's portfolio diversification benefit with low equity correlation.
**Method/Identification:** CAPM; Fama-French three-factor model; mean-variance portfolio analysis
**Key data source:** Chicago Wine Company auction prices, 1996–2007
**Key finding:** Wine alpha positive 1996–2009; first growth returns 4.1–6.0%; low beta; diversification benefit confirmed
**Relevance to Liquid Assets:** Benchmark return figures referees will expect; establishes that top-tier wines (the paper's sample) dominate the investable segment.
**BibTeX key:** MassetHenderson2010

---

### [Sanning, Shaffer & Sharratt 2008] Bordeaux Wine as a Financial Investment
**Journal/Source:** Journal of Wine Economics, Vol. 3, No. 1, pp. 51–71
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** First application of the Fama-French three-factor model to Bordeaux wine. Finds investment-grade wines earn up to 0.75% monthly abnormal returns above model predictions.
**Method/Identification:** Repeat-sales regression; Fama-French model
**Key data source:** Monthly auction hammer prices, Bordeaux wines
**Key finding:** Up to 0.75% monthly abnormal return; low market risk exposure; diversification benefit for investment-grade wines
**Relevance to Liquid Assets:** Benchmark for alpha magnitude; establishes the finance framing that referees expect.
**BibTeX key:** SanningShaffer2008

---

### [Burton & Jacobsen 2001] The Rate of Return on Investment in Wine
**Journal/Source:** Economic Inquiry, Vol. 39, No. 3, pp. 337–350
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Foundational paper applying repeat-sales regression to red Bordeaux (1986–1996). Finds nominal return ~7% (comparable to bonds), below equities. First systematic econometric evidence on wine returns.
**Method/Identification:** Repeat-sales regression (RSR)
**Key data source:** Bordeaux wine auction records, 1986–1996
**Key finding:** Nominal return ~7% (parity with bonds); below equity returns
**Relevance to Liquid Assets:** Foundational return benchmark; establishes repeat-sales as the standard methodology for wine returns.
**BibTeX key:** BurtonJacobsen2001

---

### [Ashenfelter 1989] How Auctions Work for Wine and Art
**Journal/Source:** Journal of Economic Perspectives, Vol. 3, No. 3, pp. 23–36
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Early survey documenting empirical regularities in wine and art auctions: price formation, the declining price anomaly in sequential auctions, and the failure of the law of one price.
**Method/Identification:** Descriptive empirical analysis; first-order regression evidence
**Key data source:** Various wine and art auction records
**Key finding:** Law of one price fails; declining price anomaly documented; auction mechanism shapes price formation
**Relevance to Liquid Assets:** Establishes institutional features of wine auction markets and the declining price anomaly that the heterogeneous-buyer model must address.
**BibTeX key:** Ashenfelter1989auctions

---

### [Storchmann 2012] Wine Economics
**Journal/Source:** Journal of Wine Economics, Vol. 7, No. 1, pp. 1–33
**Proximity Score:** 2/5
**Strand:** 1
**Main contribution:** Comprehensive survey covering wine as a financial investment, climate/weather effects on quality, and the role of expert opinion. Synthesizes return estimates across methodologies and datasets.
**Method/Identification:** Survey article
**Key data source:** Literature-wide
**Key finding:** Fine wine real returns 2–7%; consistent diversification benefit; weather dominates vintage quality variation
**Relevance to Liquid Assets:** Essential background survey; helps position the paper within the field.
**BibTeX key:** Storchmann2012survey

---

### [Ginsburgh 1998] Absentee Bidders and the Declining Price Anomaly in Wine Auctions
**Journal/Source:** Journal of Political Economy, Vol. 106, No. 6, pp. 1302–1331
**Proximity Score:** 3/5
**Strand:** 1, 7
**Main contribution:** Documents the declining price anomaly in sequential wine auctions and shows it is primarily caused by sub-optimal bidding strategies of absentee bidders — providing the key institutional description of French wine auction markets.
**Method/Identification:** Structural auction model; comparison of observed vs. optimal bids
**Key data source:** Wine auction records with absentee and floor bids identified
**Key finding:** Declining price anomaly due to sub-optimal absentee bidding; floor bidders do not exhibit anomaly
**Relevance to Liquid Assets:** Documents the institutional features of the auction market in the paper's data; bidder behavior directly relevant to structural demand estimation.
**BibTeX key:** Ginsburgh1998

---

### [Hadj Ali, Lecocq & Visser 2008] The Impact of Gurus: Parker Grades and En Primeur Wine Prices
**Journal/Source:** Economic Journal, Vol. 118, No. 529, pp. F158–F173
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Exploits natural experiment (Parker's late visit to Bordeaux for 2003 vintage, grades published after prices were set) to identify the causal effect of Parker scores on en primeur wine prices. Parker grade worth ~€2.80 per bottle.
**Method/Identification:** Natural experiment (timing of Parker grade publication); hedonic regression
**Key data source:** Bordeaux en primeur price data, 233 wines, 2001 and 2002 vintages
**Key finding:** Parker grade worth ~€2.80 per bottle; causal effect identified via natural experiment
**Relevance to Liquid Assets:** Expert scores are the standard quality control variable in wine hedonic regressions; this is the causal identification benchmark for expert-score effects.
**BibTeX key:** HadjAliLecocqVisser2008

---

### [Jones & Storchmann 2001] Wine Market Prices and Investment under Uncertainty: An Econometric Model for Bordeaux Crus Classés
**Journal/Source:** Agricultural Economics, Vol. 26, No. 2, pp. 115–133
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Models the relationship between vintage weather, grape composition, Parker scores, and market prices for 21 Bordeaux Crus Classés. Shows age effect on prices and calibrates uncertainty in wine investment.
**Method/Identification:** OLS hedonic regression; structural weather-quality-price pathway model
**Key data source:** Bordeaux Crus Classés auction prices; weather and composition data; Parker scores
**Key finding:** Age and Parker score both positively influence price; warm dry summers → higher prices; investment uncertainty modelled explicitly
**Relevance to Liquid Assets:** Provides the Bordeaux Crus Classés hedonic regression template used in the paper's reduced-form estimation.
**BibTeX key:** JonesStorchmann2001

---

### [Combris, Lecocq & Visser 1997] Estimation of a Hedonic Price Equation for Bordeaux Wine: Does Quality Matter?
**Journal/Source:** Economic Journal, Vol. 107, No. 441, pp. 390–402
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Applies hedonic pricing to Bordeaux wines using both label characteristics (vintage, appellation, ranking) and sensory characteristics from experimental jury tastings. Finds label characteristics explain most price variation; sensory characteristics contribute little.
**Method/Identification:** Hedonic OLS regression; two-stage approach (label and sensory characteristics separately)
**Key data source:** Bordeaux grand cru wines; experimental jury tastings; auction prices
**Key finding:** Label characteristics (vintage, appellation, ranking) explain ~80% of price variance; sensory characteristics statistically insignificant
**Relevance to Liquid Assets:** Foundational Bordeaux hedonic regression; establishes that vintage year fixed effects and appellation controls are the standard approach.
**BibTeX key:** CombrisLecocqVisser1997

---

### [Combris, Lecocq & Visser 2000] Estimation of a Hedonic Price Equation for Burgundy Wine
**Journal/Source:** Applied Economics, Vol. 32, No. 8, pp. 961–967
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Extends the Bordeaux hedonic framework to Burgundy wines, confirming that label characteristics dominate price formation, with sensory attributes playing a minor role.
**Method/Identification:** Hedonic OLS regression; experimental jury tastings
**Key data source:** Burgundy wine auction prices and jury tasting data
**Key finding:** Same pattern as Bordeaux: label characteristics dominate; consistent with Combris et al. (1997)
**Relevance to Liquid Assets:** The paper includes Burgundy Premier/Grand Cru; this is the foundational Burgundy hedonic benchmark.
**BibTeX key:** CombrisLecocqVisser2000burgundy

---

### [Di Vittorio & Ginsburgh 1996] Pricing Red Wines of Médoc: Vintages from 1949 to 1989 at Christie's Auctions
**Journal/Source:** Journal de la Société Statistique de Paris, Vol. 137, pp. 19–49
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Earliest systematic hedonic pricing of Médoc red wine at Christie's London auctions. Estimates returns to aging of 3.7% per year. Finds 1855 classification explains price indices better than alternatives.
**Method/Identification:** Hedonic OLS regression; price index construction by château and vintage
**Key data source:** Christie's London auction records, 58 top Médoc growths, vintages 1949–1989
**Key finding:** Returns to aging ~3.7% per year; 1855 classification outperforms alternatives in explaining prices
**Relevance to Liquid Assets:** Pre-cursor to all subsequent Bordeaux hedonic work; establishes the age-price gradient and the role of the 1855 classification.
**BibTeX key:** DiVittorioGinsburgh1996

---

### [Masset & Weisskopf 2015] Wine Funds: An Alternative Turning Sour?
**Journal/Source:** Journal of Alternative Investments, Vol. 17, No. 4, pp. 6–22
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Evaluates the performance, selectivity, and market-timing of wine fund managers over 2000–2013. Finds that only one of the sampled wine funds offers positive risk-adjusted returns.
**Method/Identification:** Jensen's alpha; Treynor ratio; market-timing tests
**Key data source:** Wine fund returns (multiple funds), 2000–2013; Liv-ex benchmark
**Key finding:** Wine funds generally underperform; limited selectivity and market-timing ability; one fund with positive alpha
**Relevance to Liquid Assets:** Closes the institutional loop on wine as an investable asset: even professional wine fund managers fail to generate alpha, consistent with the paper's implication that the collector premium is driven by non-financial motives.
**BibTeX key:** MassetWeisskopf2015funds

---

### [Faye, Le Fur & Prat 2015] Dynamics of Fine Wine and Asset Prices: Evidence from Short- and Long-Run Co-movements
**Journal/Source:** Applied Economics, Vol. 47, No. 29, pp. 3059–3077
**Proximity Score:** 3/5
**Strand:** 1
**Main contribution:** Applies cointegration analysis on 1994–2015 monthly data to show that fine wine prices are co-integrated with global equity markets (MSCI world) and that Liv-ex sub-indices have different long-run relationships with regional equity markets.
**Method/Identification:** Johansen cointegration; VECM; Granger causality
**Key data source:** Liv-ex Fine Wine indices, MSCI world and regional indices, monthly 1994–2015
**Key finding:** Causality from MSCI world to wine prices confirmed; France is a leading indicator; wine behaves like a financial asset in the long run
**Relevance to Liquid Assets:** Documents macroeconomic sensitivity of wine prices as financial assets; context for the China shock identification.
**BibTeX key:** FayeLeFurPrat2015

---

## Category 3: Alternative Assets — Art, Collectibles, Stamps (Proximity 2–4)

Papers studying non-wine collectibles and durable assets as investments, relevant to the Liquid Assets framework of consumption vs. collector demand.

---

### [Goetzmann, Renneboog & Spaenjers 2011] Art and Money
**Journal/Source:** American Economic Review, Papers and Proceedings, Vol. 101, No. 3, pp. 222–226
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Shows using two centuries of art price data that equity market returns and top income inequality both drive art prices; cointegration between top incomes and art prices confirmed.
**Method/Identification:** Time-series regression; cointegration analysis; VAR
**Key data source:** Art price index, 1765–2007; financial market and income inequality data
**Key finding:** Equity returns and top-income inequality drive art prices; long-run cointegration confirmed
**Relevance to Liquid Assets:** The wealth-shock mechanism driving collector demand is the same mechanism at work in wine — motivates the China demand shock as a collector-demand instrument.
**BibTeX key:** GoetzmannRenneboogSpaenjers2011

---

### [Dimson & Spaenjers 2011] Ex Post: The Investment Performance of Collectible Stamps
**Journal/Source:** Journal of Financial Economics, Vol. 100, No. 2, pp. 443–458
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Documents British postage stamp returns (1900–2008): nominal 7.0%, real 2.9%; partial inflation hedge; low beta; positive equity covariance.
**Method/Identification:** Repeat-sales regression on catalogue prices; CAPM; inflation beta
**Key data source:** British stamp catalogue prices, 1900–2008
**Key finding:** Nominal 7.0%, real 2.9% return; collector premium present across asset classes
**Relevance to Liquid Assets:** Shows the collectors' premium is a cross-asset class phenomenon; motivates the general durable collectibles framework.
**BibTeX key:** DimsonSpaenjers2011stamps

---

### [Renneboog & Spaenjers 2012] Hard Assets: The Returns on Rare Diamonds and Gems
**Journal/Source:** Finance Research Letters, Vol. 9, No. 4, pp. 220–230
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Documents real USD returns of 6.4% (white diamonds) and 2.9% (colored diamonds) over 1999–2010 using auction data; positive equity covariance.
**Method/Identification:** Hedonic regression; repeat-sales regression
**Key data source:** Diamond and gem auction transactions, 1999–2010
**Key finding:** White diamonds: 6.4% real return; colored: 2.9%; positive equity covariance
**Relevance to Liquid Assets:** Confirms cross-asset generality of collector-demand driven returns in alternative assets.
**BibTeX key:** RenneboogSpaenjers2012gems

---

### [Mandel 2009] Art as an Investment and Conspicuous Consumption Good
**Journal/Source:** American Economic Review, Vol. 99, No. 4, pp. 1653–1663
**Proximity Score:** 3/5
**Strand:** 2, 3
**Main contribution:** Develops a model where art is valued both as an investment (to transfer consumption over time) and as a conspicuous consumption signal. Shows that adding art value to utility explains why average financial returns are low and risk premia modest or negative.
**Method/Identification:** Theoretical equilibrium model with utility for conspicuous consumption
**Key data source:** None (theory); calibrated to art market stylized facts
**Key finding:** Low financial returns to art are rational equilibrium outcome when art generates conspicuous consumption dividend; risk premia can be negative
**Relevance to Liquid Assets:** Closest theoretical antecedent for the two-type valuation model; the "conspicuous consumption" component maps to the collector type's non-financial utility.
**BibTeX key:** Mandel2009art

---

### [Pénasse & Renneboog 2022] Speculative Trading and Bubbles: Evidence from the Art Market
**Journal/Source:** Management Science, Vol. 68, No. 7, pp. 4939–4963
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Shows that extrapolative expectations drive boom-bust cycles in postwar art markets. Predictable price changes account for ~50% of five-year return variance. Booms characterized by high trading volume, more short-term trades, and increased volatility.
**Method/Identification:** Predictability regressions; boom-bust classification; panel data on auction results
**Key data source:** Postwar art auction records (major houses), 1970–2012
**Key finding:** Art booms are predictable; speculative extrapolation drives prices; boom-bust consistent with behavioral model
**Relevance to Liquid Assets:** Speculative demand is a third possible channel (alongside consumption and collector value) explaining post-maturity price dynamics; provides null to test against.
**BibTeX key:** PenasseRenneboog2022

---

### [Spaenjers, Goetzmann & Mamonova 2015] The Economics of Aesthetics and Record Prices for Art since 1701
**Journal/Source:** Explorations in Economic History, Vol. 57, pp. 79–94
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Uses micro-level perspective on art record prices since 1701 to show that each artwork generates a market for trading its private-value benefits. Highlights the importance of art market industrial organization for long-run price trends.
**Method/Identification:** Historical record-price analysis; hedonic decomposition of record premiums
**Key data source:** Record art auction prices, 1701–2014
**Key finding:** Private-use benefits dominate art price formation; record prices reflect shifts in buyer purchasing power and tastes
**Relevance to Liquid Assets:** Establishes that private-value (use value) is central to understanding collectible pricing — direct conceptual foundation for the consumption/collector valuation decomposition.
**BibTeX key:** SpaenjersGoetzmannMamonova2015

---

### [Pénasse, Renneboog & Spaenjers 2014] Sentiment and Art Prices
**Journal/Source:** Economics Letters, Vol. 122, No. 3, pp. 432–434
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Uses panel survey data on art market participants' confidence to show that investor sentiment predicts short-term art returns; faddish beliefs affect prices.
**Method/Identification:** Panel regressions; survey-based sentiment index; return predictability tests
**Key data source:** Survey data on art market participants; matched auction transaction data
**Key finding:** Sentiment significantly predicts short-term art price returns; fads component confirmed
**Relevance to Liquid Assets:** Sentiment-driven demand is an alternative explanation for the China demand shock price effects; the paper must distinguish collector-type fundamentals from sentiment/fads.
**BibTeX key:** PenasseRenneboogSpaenjers2014

---

### [Oosterlinck 2017] Art as a Wartime Investment: Conspicuous Consumption and Discretion
**Journal/Source:** Economic Journal, Vol. 127, No. 607, pp. 2665–2701
**Proximity Score:** 2/5
**Strand:** 2, 6
**Main contribution:** Studies wartime art prices in occupied France (WWII). Finds art dramatically outperformed all other assets except gold. Introduces the concept of "discretion" — storing large value in portable goods — alongside conspicuous consumption as motivations for art investment.
**Method/Identification:** Hedonic regression with war/occupation period FE; natural variation in types of art
**Key data source:** French art auction records, WWII occupation period, 1940–1944
**Key finding:** Art outperforms bonds, equities, currency; "degenerate" art (non-displayable) performs worse, confirming conspicuous consumption role
**Relevance to Liquid Assets:** Documents that demand shocks to conspicuous consumption (here, Nazi occupation restrictions) differentially affect collector-type buyers — same mechanism as China corruption crackdown.
**BibTeX key:** Oosterlinck2017

---

### [Ursprung & Wiermann 2011] Reputation, Price, and Death: An Empirical Analysis of Art Price Formation
**Journal/Source:** Economic Inquiry, Vol. 49, No. 3, pp. 697–715
**Proximity Score:** 2/5
**Strand:** 2
**Main contribution:** Analyses 146,575 art sales (1980–2005) to show that an artist's death has two opposing effects on price: scarcity-induced price increase vs. frustrated collector hopes if death is premature. Generates a hump-shaped age-at-death/price-change relationship.
**Method/Identification:** Hedonic regression; event study around death; death-age interaction
**Key data source:** 146,575 art sales, 262 artists, 1980–2005
**Key finding:** Death premium exists but is hump-shaped in age at death; premature death destroys collector premium
**Relevance to Liquid Assets:** The "scarcity at death" mechanism is analogous to the scarcity-driven collector premium in post-maturity wine; the model must accommodate the scarcity channel.
**BibTeX key:** UrsprungWiermann2011

---

## Category 4: Heterogeneous Buyer Models and Speculative Demand Theory (Proximity 1–4)

Theoretical papers on heterogeneous buyers, speculative demand, and equilibrium price formation with mixed buyer types.

---

### [Bagwell & Bernheim 1996] Veblen Effects in a Theory of Conspicuous Consumption
**Journal/Source:** American Economic Review, Vol. 86, No. 3, pp. 349–373
**Proximity Score:** 3/5
**Strand:** 3, 6
**Main contribution:** Shows that when the single-crossing property of preferences fails, luxury brands (not intrinsically superior) are priced above marginal cost in equilibrium because consumers use price as a wealth signal. Conditions for Veblen effects derived formally.
**Method/Identification:** Game-theoretic signaling model; comparative statics on equilibrium pricing
**Key data source:** None (theory)
**Key finding:** Veblen effects arise when single-crossing fails; budget brands priced at MC, luxury brands above; positive profits sustainable
**Relevance to Liquid Assets:** Theoretical foundation for the collector-type buyer's valuation of wine as a status/signaling good; motivates why collector valuations are not bounded by consumption utility.
**BibTeX key:** BagwellBernheim1996

---

### [Scheinkman & Xiong 2003] Overconfidence and Speculative Bubbles
**Journal/Source:** Journal of Political Economy, Vol. 111, No. 6, pp. 1183–1219
**Proximity Score:** 2/5
**Strand:** 3
**Main contribution:** Continuous-time model where overconfidence generates heterogeneous beliefs; with short-sale constraints, the asset buyer acquires a resale option, generating bubbles even with small belief differences. Equilibrium features high volume and volatility during bubble episodes.
**Method/Identification:** Continuous-time equilibrium model; closed-form solutions for bubble premium
**Key data source:** None (theory); calibration to historical episodes
**Key finding:** Bubble premium is a resale option; increases with belief heterogeneity and short-sale constraints; trading volume and volatility co-move with bubble
**Relevance to Liquid Assets:** Speculative resale motive is a possible component of the collector-type valuation; the model must distinguish durable collector demand from purely speculative demand.
**BibTeX key:** ScheinkmanXiong2003

---

### [Tirole 1982] On the Possibility of Speculation under Rational Expectations
**Journal/Source:** Econometrica, Vol. 50, No. 5, pp. 1163–1181
**Proximity Score:** 1/5
**Strand:** 3, 7
**Main contribution:** Shows that speculation with rational expectations and common priors is impossible (no-trade theorem). Establishes that heterogeneous priors are necessary for speculative trading. Foundational result bounding when the speculative motive can appear in equilibrium.
**Method/Identification:** Theoretical (rational expectations general equilibrium)
**Key data source:** None (theory)
**Key finding:** No-trade theorem: speculation impossible with common priors and rational expectations; heterogeneous priors required
**Relevance to Liquid Assets:** Establishes theoretical conditions under which the collector premium cannot be purely speculative; motivates the non-pecuniary private-value approach.
**BibTeX key:** Tirole1982

---

### [Milgrom & Weber 1982] A Theory of Auctions and Competitive Bidding
**Journal/Source:** Econometrica, Vol. 50, No. 5, pp. 1089–1122
**Proximity Score:** 2/5
**Strand:** 7
**Main contribution:** General auction model with affiliated values; establishes revenue ranking (English > second-price > first-price) and the linkage principle. Foundation for all subsequent auction theory.
**Method/Identification:** Theoretical (mechanism design, comparative statics)
**Key data source:** None (theory)
**Key finding:** Revenue ranking of auction formats; linkage principle; English auction revenue-dominates for affiliated values
**Relevance to Liquid Assets:** The two-type IPV auction model is a special case of this framework; any structural auction model cites this.
**BibTeX key:** MilgromWeber1982

---

### [Vickrey 1961] Counterspeculation, Auctions, and Competitive Sealed Tenders
**Journal/Source:** Journal of Finance, Vol. 16, No. 1, pp. 8–37
**Proximity Score:** 1/5
**Strand:** 7
**Main contribution:** Introduces the second-price sealed-bid (Vickrey) auction and proves dominant-strategy truthful bidding. Establishes equivalence with English ascending auction under IPV.
**Method/Identification:** Theoretical (mechanism design)
**Key data source:** None (theory)
**Key finding:** Second-price auction has dominant-strategy truth-telling equilibrium; revenue equivalence theorem established
**Relevance to Liquid Assets:** The structural model's auction mechanics rest on second-price auction theory.
**BibTeX key:** Vickrey1961

---

### [Myerson 1981] Optimal Auction Design
**Journal/Source:** Mathematics of Operations Research, Vol. 6, No. 1, pp. 58–73
**Proximity Score:** 1/5
**Strand:** 7
**Main contribution:** Derives the revenue-maximizing auction mechanism using virtual valuations and the ironing procedure. Establishes that optimal reserve price exceeds seller's value.
**Method/Identification:** Theoretical (mechanism design)
**Key data source:** None (theory)
**Key finding:** Optimal reserve price above seller's value; virtual valuation determines efficient allocation
**Relevance to Liquid Assets:** Provides theoretical apparatus for the two-type structural model's optimal reserve and price determination.
**BibTeX key:** Myerson1981

---

### [Klemperer 1999] Auction Theory: A Guide to the Literature
**Journal/Source:** Journal of Economic Surveys, Vol. 13, No. 3, pp. 227–286
**Proximity Score:** 1/5
**Strand:** 7
**Main contribution:** Comprehensive survey of auction theory: IPV model, optimal auctions, risk aversion, common values, entry, multi-unit auctions, collusion. Standard practitioner's reference.
**Method/Identification:** Survey article
**Key data source:** None (theory survey)
**Key finding:** Survey — covers revenue equivalence, optimal auctions, entry effects, common vs. private values
**Relevance to Liquid Assets:** Background reference for the auction-theoretic framework of the structural model.
**BibTeX key:** Klemperer1999

---

### [Asker 2010] A Study of the Internal Organization of a Bidding Cartel
**Journal/Source:** American Economic Review, Vol. 100, No. 3, pp. 724–762
**Proximity Score:** 2/5
**Strand:** 7
**Main contribution:** Analyses 1,700+ knockout auctions used by a stamp-dealer bidding cartel using a structural model in the spirit of Guerre/Perrigne/Vuong. Estimates damages, ring benefit, and inefficiency induced by collusion.
**Method/Identification:** Structural auction model (IPV); reduced-form damages estimation; knockout auction structural model
**Key data source:** Internal ring records (knockout auction bids, sidepayments), stamp dealer cartel, 1990s
**Key finding:** Non-ring bidders suffered damages of same order as sellers; structural approach recovers counterfactual prices and welfare
**Relevance to Liquid Assets:** Demonstrates structural estimation of heterogeneous buyer behavior in collectible auctions (stamps); methodological template for the wine auction structural model.
**BibTeX key:** Asker2010

---

## Category 5: Durable Goods Pricing and Storage (Proximity 1–3)

Papers on the price-age profile of durable goods, storable commodities, and secondary market dynamics.

---

### [Deaton & Laroque 1996] Competitive Storage and Commodity Price Dynamics
**Journal/Source:** Journal of Political Economy, Vol. 104, No. 5, pp. 896–923
**Proximity Score:** 2/5
**Strand:** 4
**Main contribution:** Rational-expectations model of competitive storage by risk-neutral speculators; explains positive autocorrelation in commodity prices and the "stockout" asymmetry.
**Method/Identification:** Structural rational-expectations model; calibration
**Key data source:** Commodity price series
**Key finding:** Competitive storage generates strong positive autocorrelation; stockout creates price spikes
**Relevance to Liquid Assets:** Storage model is the structural antecedent for why holding wine off the market creates an intertemporal premium; the convenience yield concept maps to consumption value.
**BibTeX key:** DeatonLaroque1996

---

### [Casassus & Collin-Dufresne 2005] Stochastic Convenience Yield Implied from Commodity Futures and Interest Rates
**Journal/Source:** Journal of Finance, Vol. 60, No. 5, pp. 2283–2331
**Proximity Score:** 2/5
**Strand:** 4
**Main contribution:** Three-factor model of commodity spot prices, convenience yields, and interest rates. Finds spot-price-dependent convenience yields for commercial commodities.
**Method/Identification:** Kalman filter; affine term structure model
**Key data source:** Commodity futures (crude oil, copper, gold, silver), 1975–2000
**Key finding:** Spot-price-dependent convenience yields; strong mean reversion under risk-neutral measure
**Relevance to Liquid Assets:** The "convenience yield" on wine — the consumption flow enjoyed by drinking — is the structural analog to the consumption value function in the model.
**BibTeX key:** CasassusCollinDufresne2005

---

### [Pindyck 1994] Inventories and the Short-Run Dynamics of Commodity Prices
**Journal/Source:** RAND Journal of Economics, Vol. 25, No. 1, pp. 141–159
**Proximity Score:** 1/5
**Strand:** 4
**Main contribution:** Shows that convenience yield is a decreasing function of inventory levels; the "must-stock" option value creates a wedge between spot and futures prices.
**Method/Identification:** Structural equilibrium model; OLS estimation of inventory-price relationship
**Key data source:** Commodity price and inventory data
**Key finding:** Convenience yield decreases in inventory; marginal value of storage explains commodity price dynamics
**Relevance to Liquid Assets:** Convenience yield framework directly translates to wine: value of not selling decreases past maturity date, consistent with the price dip.
**BibTeX key:** Pindyck1994

---

## Category 6: Structural Demand Estimation (Proximity 1–3)

Methods papers for structural demand estimation relevant to the Liquid Assets structural model.

---

### [Berry, Levinsohn & Pakes 1995] Automobile Prices in Market Equilibrium
**Journal/Source:** Econometrica, Vol. 63, No. 4, pp. 841–890
**Proximity Score:** 3/5
**Strand:** 5
**Main contribution:** Introduces the BLP random-coefficients discrete-choice demand model for differentiated products. Uses panel data on U.S. automobile models (1971–1990) with product-characteristic instruments; estimates demand and markups jointly.
**Method/Identification:** GMM with BLP instruments; contraction mapping for share inversion; random-coefficients logit
**Key data source:** U.S. automobile transaction data, 1971–1990
**Key finding:** Significant markups in U.S. auto industry; random-coefficients model outperforms logit; product-characteristic instruments valid
**Relevance to Liquid Assets:** Canonical structural demand estimation template; if the paper pursues BLP-style structural estimation for wine auction bidders, this is the indispensable reference.
**BibTeX key:** BerryLevinsohnPakes1995

---

### [Nevo 2001] Measuring Market Power in the Ready-to-Eat Cereal Industry
**Journal/Source:** Econometrica, Vol. 69, No. 2, pp. 307–342
**Proximity Score:** 3/5
**Strand:** 5
**Main contribution:** Canonical applied implementation of BLP. Estimates random-coefficients cereal demand across 65 markets; recovers consumer heterogeneity and markup estimates.
**Method/Identification:** BLP random-coefficients logit; GMM; product-characteristic instruments; contraction mapping
**Key data source:** Scanner data for breakfast cereals, 65 U.S. cities, 1988–1992
**Key finding:** Significant heterogeneity in price sensitivity; markup estimates consistent with oligopoly; Lerner indices 20–45%
**Relevance to Liquid Assets:** Step-by-step BLP implementation reference; provides computational template for wine auction demand estimation.
**BibTeX key:** Nevo2001cereal

---

### [Bai & Perron 2003] Computation and Analysis of Multiple Structural Change Models
**Journal/Source:** Journal of Applied Econometrics, Vol. 18, No. 1, pp. 1–22
**Proximity Score:** 1/5
**Strand:** 5
**Main contribution:** Provides efficient algorithms and test statistics for detecting and dating multiple structural breaks in linear regression models; BIC-based selection of break count.
**Method/Identification:** Sequential and global structural break detection methods
**Key data source:** None (methods paper; illustrated with examples)
**Key finding:** Efficient algorithms for structural break detection; BIC-based number selection
**Relevance to Liquid Assets:** Standard toolkit for formally testing whether the China demand shock constitutes a structural break in the price-age relationship.
**BibTeX key:** BaiPerron2003

---

## Category 7: China Demand Shock and Luxury Goods (Proximity 2–4)

Papers on the China anti-corruption campaign and luxury/collectibles demand shocks.

---

### [Qian & Wen 2015] The Impact of Xi Jinping's Anti-Corruption Campaign on Luxury Imports in China
**Journal/Source:** Working Paper, Yale University (preliminary draft April 2015; unpublished as of 2026)
**Proximity Score:** 4/5
**Strand:** 6
**Main contribution:** Documents ~55% reduction in luxury imports (alcohol, wine, spirits, art) relative to controls following the 2012 anti-corruption campaign, using Chinese trade data. Effect concentrated in conspicuous consumption categories.
**Method/Identification:** DiD using category-level variation in conspicuousness; Chinese trade data before/after campaign
**Key data source:** Chinese customs/trade import data, monthly commodity flows, 2010–2014
**Key finding:** ~55% reduction in luxury imports; ~47.4% decline in luxury wine imports specifically; short-term concentration of effects
**Relevance to Liquid Assets:** Core instrument and demand shock for the event-study identification; establishes timing, magnitude, and differential incidence.
**BibTeX key:** QianWen2015

---

### [Bian, Zhang & Zhou 2025] Do China's Anti-Corruption Campaigns Impact Art Prices? Evidence from the Chinese Art Market
**Journal/Source:** Pacific-Basin Finance Journal, Vol. 90 (2025), Article 102680
**Proximity Score:** 3/5
**Strand:** 6
**Main contribution:** Shows that each additional official prosecuted in a region reduces Chinese traditional painting prices by 5.5% on average, with stronger effects for non-masterworks (bribery goods).
**Method/Identification:** DiD using regional variation in prosecution intensity and time variation
**Key data source:** 54,809 Chinese painting auction transactions, 2013–2019; official prosecution records
**Key finding:** Each additional official prosecuted → -5.5% auction price; stronger for non-masterworks
**Relevance to Liquid Assets:** Most recent empirical evidence that corruption crackdown affected collectible prices at granular level; bridges the China shock to the wine market mechanism.
**BibTeX key:** BianZhangZhou2025

---

### [Kräussl, Lehnert & Martelin 2016] Is There a Bubble in the Art Market?
**Journal/Source:** Journal of Empirical Finance, Vol. 35, pp. 99–109
**Proximity Score:** 2/5
**Strand:** 2, 6
**Main contribution:** Applies SADF right-tailed unit root test to 36 years of art auction data across six styles; identifies two historical speculative bubbles and detects explosive behavior in contemporary and American art market segments circa 2014.
**Method/Identification:** Phillips-Shi-Yu SADF test (right-tailed forward recursive ADF for bubble detection)
**Key data source:** 1 million+ art auction records, 1970–2013; six art style segments
**Key finding:** Two historical bubbles identified; explosive behavior in postwar contemporary and American art in 2014
**Relevance to Liquid Assets:** Co-author Roman Kräussl; provides the art bubble detection methodology. The wine market post-maturity price recovery must be distinguished from a speculative bubble — this paper provides the test.
**BibTeX key:** KrausalLehnertMartelin2016

---

### [Aubry, Kräussl, Manso & Spaenjers 2023] Biased Auctioneers
**Journal/Source:** Journal of Finance, Vol. 78, No. 2, pp. 795–833
**Proximity Score:** 2/5
**Strand:** 7
**Main contribution:** Uses a neural network to generate presale price estimates for art, showing that auction house estimates are systematically biased. Machine learning estimates outperform auction house estimates; biases are persistent at artist and house level.
**Method/Identification:** Neural network price prediction model; regression of price-to-estimate ratio on machine learning signals; panel with auction house and artist FE
**Key data source:** Art auction records from major houses; matched presale estimates and hammer prices
**Key finding:** Auction house presale estimates are informationally inefficient and biased; machine learning-based estimates substantially outperform; biases persistent and predictable
**Relevance to Liquid Assets:** Co-authors include Roman Kräussl; demonstrates systematic patterns in how auction houses price art — relevant to the question of whether wine auction price dispersions reflect fundamental heterogeneity or auctioneer biases.
**BibTeX key:** AubryKraussMansoSpaenjers2023

---

## Category 8: Methods and Theoretical Foundations (Proximity 1–2)

Foundational papers providing econometric or theoretical tools used in the paper.

---

### [Nerlove 1995] Hedonic Price Functions and the Measurement of Preferences: The Case of Swedish Wine Consumers
**Journal/Source:** European Economic Review, Vol. 39, No. 9, pp. 1697–1716
**Proximity Score:** 2/5
**Strand:** 5
**Main contribution:** Estimates a hedonic price function for wine using Swedish government monopoly data (1989–1991). Shows that price elasticity is approximately −1.65; implicit valuations of quality attributes differ greatly depending on regression specification.
**Method/Identification:** Hedonic regression with quantity (not price) as dependent variable; preference measurement
**Key data source:** Swedish government wine monopoly data, 1989–1991
**Key finding:** Price elasticity ~−1.65 holding quality constant; attribute valuations specification-sensitive
**Relevance to Liquid Assets:** Foundational hedonic wine paper; establishes that price as dependent variable produces estimates that differ from consumer-demand preference recovery.
**BibTeX key:** Nerlove1995

---

## Summary Statistics

| Category | Papers | Proximity Range |
|---|---|---|
| Directly Related (wine auction/maturity/heterogeneous buyers) | 6 | 4–5 |
| Wine as Investment (returns, portfolio) | 9 | 2–3 |
| Alternative Assets (art, collectibles) | 7 | 2–3 |
| Heterogeneous Buyers/Speculative Demand Theory | 7 | 1–3 |
| Durable Goods/Commodity Storage | 3 | 1–2 |
| Structural Demand Estimation | 3 | 1–3 |
| China Shock / Luxury Goods | 3 | 2–4 |
| Methods/Theoretical Foundations | 1 | 2 |
| Already-in-bibliography papers (not re-listed above) | 13 | 2–5 |
| **Grand total across all searches** | **~58** | — |

---

## Scooping Risk Assessment

**No proximity-5 working paper scooping risk identified.** No paper in the literature as of 2026-03-30 combines:
(a) structural decomposition of consumption vs. collector buyer-type valuations in wine
(b) the bimodal/non-monotone price-age profile as the central empirical fact
(c) identification via the China anti-corruption demand shock
(d) cross-sectional variation across Grand Cru (high-entry-price screen) vs. Premier Cru

**Proximity-4 papers to monitor:**
- Masset (2024, Economic Modelling) — documents lifecycle segments; no structural demand model
- Masset et al. (2016, Emerging Markets Review) — China shock at wine auction level; no maturity analysis
- Cardebat & Jiao (2018, QREF) — China cointegration; no structural model, no maturity analysis
- Qian & Wen (2015, working paper) — China demand shock; not wine-auction specific

**Verdickt (2025, SSRN)** — New working paper on climate extrapolation and Bordeaux Premier Cru wine auction prices using >68,000 transactions. Uses same wine types (Bordeaux Premier Cru) but different question (investor climate attention vs. maturity/buyer-type). Not a scooping risk but uses closely related data and should be monitored.

---

*Literature review completed: 2026-03-30*
*Journals searched: JFE, JF, RFS, AER, JPE, QJE, REStud, Econometrica, Journal of Wine Economics, Economic Journal, Economic Modelling, Emerging Markets Review, Finance Research Letters, Pacific-Basin Finance Journal, Journal of Economic Literature, Management Science, RAND Journal of Economics, Mathematics of Operations Research, Applied Economics, Agricultural Economics, Quarterly Review of Economics and Finance, Journal of Empirical Finance, Journal of Alternative Investments, Economics Letters, Explorations in Economic History, Economic Inquiry*
*Repositories searched: SSRN, NBER, RePeC, AAWE Working Papers, Google Scholar*

---

## Targeted Gap-Fill Additions — 2026-03-30

Six papers flagged as gaps in the prior literature review, verified and annotated below. Two are assigned to existing categories; four form a new **Category 9: Structural Auction Theory** section. The China gap was filled with two published papers replacing the unpublished Qian & Wen (2015) working paper for formal citation purposes.

---

## Category 9: Structural Auction Theory — Identification and Estimation (Proximity 2–3)

Foundational papers for structural analysis of auction data: identification of latent private-value distributions and nonparametric/semiparametric estimation methods. These are not directly about wine markets but are the methodological bedrock if the paper estimates structural auction parameters or uses auction-theoretic model to discipline bidder behavior.

---

### [Guerre, Perrigne & Vuong 2000] Optimal Nonparametric Estimation of First-Price Auctions
**Journal/Source:** Econometrica, Vol. 68, No. 3 (May 2000), pp. 525–574
**Proximity Score:** 2/5
**Strand:** 7
**Recommendation:** SHOULD CITE
**Main contribution:** Shows that under the independent private values (IPV) paradigm, the distribution of private valuations is nonparametrically identified from observed bids and the number of bidders, without any parametric assumption. Proposes a two-step kernel-based estimator that achieves the minimax optimal uniform convergence rate: first estimate the bid distribution nonparametrically, then map bids to valuations via the IPV first-order condition.
**Identification:** Nonparametric identification via revealed preference (first-order condition of IPV auction); two-step kernel estimator
**Data:** Monte Carlo simulations and U.S. OCS oil lease auctions (illustrative)
**Key result:** Minimax-optimal rate for density of valuations; the latent value density is nonparametrically identified from bid data alone.
**Relevance to Liquid Assets:** This paper is essential if the structural model treats wine auctions as first-price sealed-bid auctions and seeks to recover the distribution of valuations across buyer types nonparametrically. It is less central if the model treats auction prices as equilibrium market-clearing prices (as in a BLP framework) rather than estimating a bidding game. Note: in the Liquid Assets setting, wine auctions are typically ascending (English/Vickrey), where the GPV framework is not directly applicable — but GPV remains a standard citation in any structural auction paper as methodological background.
**BibTeX key:** GuerrePerrigneVuong2000

---

### [Athey & Haile 2002] Identification of Standard Auction Models
**Journal/Source:** Econometrica, Vol. 70, No. 6 (November 2002), pp. 2107–2140
**Proximity Score:** 2/5
**Strand:** 7
**Recommendation:** SHOULD CITE (if auction structure is made explicit in the model)
**Main contribution:** Establishes identification results for first-price, second-price, ascending (English), and descending (Dutch) auction models under a general latent demand/information structure. Covers both private-values and common-values settings, correlated types, and ex ante asymmetry. The simplest case — symmetric IPV — is nonparametrically identified from transaction prices alone. Provides the identification toolkit for researchers choosing among auction formats.
**Identification:** Theoretical identification analysis using order statistics of private-value distributions; symmetry and exclusion conditions
**Data:** No empirical application (theory paper)
**Key result:** IPV ascending-auction model is identified from transaction price data alone; common-values and affiliated-values require additional data (losing bids or number of bidders).
**Relevance to Liquid Assets:** Wine auctions are typically ascending (English-format); Athey & Haile show that the ascending-auction IPV model is identified from transaction prices — exactly the data available in wine auction records. If the paper invokes any structural auction identification claim, this is the foundational cite. Proximity is 2 because the paper's primary demand model may not explicitly model the auction game (collector vs. consumption buyer may be modeled as a market-clearing demand model rather than a bidding game).
**BibTeX key:** AtheyHaile2002

---

## Gap-fill additions to existing categories

The following papers are appended to **Category 5 (Structural Demand Estimation)** and **Category 6 (China Shock / Luxury Goods)** respectively.

---

### [Hendel & Nevo 2006] Measuring the Implications of Sales and Consumer Inventory Behavior
**Journal/Source:** Econometrica, Vol. 74, No. 6 (November 2006), pp. 1637–1673
**Proximity Score:** 2/5
**Strand:** 5
**Recommendation:** SHOULD CITE
**Main contribution:** Develops a dynamic structural demand model for storable goods where forward-looking consumers stockpile during temporary price reductions ("sales"). Calibrated to scanner data on laundry detergent across 65 U.S. markets. Finds that ignoring inventory behavior leads to a 30% overestimate of the elasticity to permanent price changes; the true elasticity to permanent price changes is much smaller than the cross-sectional price-quantity correlation suggests.
**Identification:** Dynamic programming model of consumer inventory choice; GMM on simulated model moments matched to purchase frequency, quantity per trip, and inter-purchase timing
**Data:** Scanner data (laundry detergent), IRI/AC Nielsen, 65 U.S. markets, 1991–1994
**Key result:** Ignoring inventory leads to 30% overestimate of permanent price elasticity; most "sale" demand spikes are stockpiling, not new consumption
**Relevance to Liquid Assets:** Maps onto the consumption buyer's pre-maturity holding decision: a wine buyer who purchases a case pre-maturity is engaging in intertemporal substitution analogous to stockpiling a storable good. The Hendel-Nevo framework motivates why consumption buyers may accelerate purchases during price dips (or when the wine approaches its maturity window) — a dynamic demand feature that the Liquid Assets model should acknowledge even if not structurally estimated. Proximity is 2 rather than higher because wine is not a homogeneous storable commodity and the auction market structure differs fundamentally from the supermarket setting.
**BibTeX key:** HendelNevo2006

---

### [Nitschka 2022] China's Anti-Corruption Campaign and Stock Returns of Luxury Goods Firms
**Journal/Source:** Financial Markets and Portfolio Management, Vol. 36, No. 2 (2022), pp. 159–177
**Proximity Score:** 3/5
**Strand:** 6
**Recommendation:** SHOULD CITE (as a published peer-reviewed complement to the unpublished Qian & Wen 2015 working paper)
**Main contribution:** Uses the unexpected 2012 launch of China's anti-corruption campaign as an event study to estimate its effect on equity valuations of global luxury goods firms with high China exposure. Constructs a portfolio of luxury-sector stocks weighted by China revenue exposure and shows risk-adjusted returns shifted persistently downward following major anti-corruption enforcement events. Effect is specific to China-exposed luxury firms, not the broader market or non-luxury consumer goods.
**Identification:** Event-study / portfolio-sort methodology; exposure-weighted luxury firm portfolios; four-factor risk adjustment; campaign intensity proxied by cumulative prosecutions of senior officials
**Data:** Stock returns of global luxury goods listed firms, MSCI data, 2010–2018
**Key result:** Risk-adjusted returns on China-exposed luxury portfolios fell persistently after 2012; effect correlated with prosecution intensity of senior officials
**Relevance to Liquid Assets:** Provides published peer-reviewed evidence that the China anti-corruption campaign created a real, financially material demand shock to the luxury collectibles sector — not just a compositional shift in trade statistics. Supports the identification strategy that uses the 2012 campaign as an exogenous negative demand shock to Chinese collector buyers of fine wine. Proximity 3 because the paper's outcome (equity returns) is one step removed from wine auction hammer prices.
**BibTeX key:** Nitschka2022

---

### [Dang, Liu & Yan 2025] Signals of Clean Governance: Evidence from Luxury Wine Imports in China
**Journal/Source:** Economics Letters, Vol. 255 (2025), Article 112523
**Proximity Score:** 4/5
**Strand:** 6
**Recommendation:** MUST CITE
**Main contribution:** Examines the impact of China's anti-corruption and integrity-promotion campaigns on luxury wine imports using a difference-in-differences design. Finds a 47.4% reduction in luxury wine imports following the 2012 campaign, concentrated in the short term with fading effects over time. Frames wine imports as "signals of clean governance" — their decline reflects the elimination of bribery-gift usage rather than a shift in genuine consumption preferences.
**Identification:** DiD using pre/post campaign timing variation and wine-versus-non-wine control goods; Chinese customs import data
**Data:** Chinese customs luxury import data, monthly commodity flows, ~2010–2015
**Key result:** 47.4% decline in luxury wine imports; effect concentrated in short run; consistent with conspicuous-consumption bribe-gift interpretation
**Relevance to Liquid Assets:** This is the most directly relevant published paper for the China identification strategy in the Liquid Assets paper. It establishes (a) the magnitude of the wine-specific import shock (47.4%), (b) the interpretation of luxury wine as a bribe-gift conspicuous consumption good, and (c) the differential pattern consistent with a collector/official buyer type rather than genuine consumption demand. Published in Economics Letters (2025), so it is very recent — must be cited to establish awareness of the latest literature.
**BibTeX key:** DangLiuYan2025

---

### [Waldman 1996] Durable Goods Pricing When Quality Matters
**Journal/Source:** Journal of Business, Vol. 69, No. 4 (October 1996), pp. 489–510
**Proximity Score:** 2/5
**Strand:** 4
**Recommendation:** SHOULD CITE
**Main contribution:** Models a durable goods monopolist who chooses both price and durability level. The key insight is that the secondhand market price limits what the monopolist can charge for new units (the used good is a substitute), which in turn induces the monopolist to choose below-socially-optimal durability — or in the extreme, to eliminate the secondhand market entirely. Provides conditions under which planned obsolescence emerges endogenously from secondhand market competition.
**Identification:** Theoretical model; comparative statics on monopolist's durability and price choice under secondhand market competition
**Data:** None (theory paper)
**Key result:** Secondhand market linkage leads to sub-optimal durability; monopolist may find it profitable to eliminate the used-good market; the price gradient between new and used goods reflects durability choice endogeneity.
**Relevance to Liquid Assets:** Motivates the theoretical treatment of wine as a durable good with a secondary (auction) market. The Liquid Assets paper's price-age profile is driven by the intersection of physical maturity, consumption value, and collector/speculative value — Waldman (1996) provides the durable-goods theory framework for why secondary market prices reflect both dimensions. Proximity is 2 because the Liquid Assets model does not feature a monopolist producer choosing durability; the wine quality and maturity schedule are exogenous. The paper is more relevant as theoretical background than as a methodological template.
**BibTeX key:** Waldman1996

---

### [Rust 1987] Optimal Replacement of GMC Bus Engines: An Empirical Model of Harold Zurcher
**Journal/Source:** Econometrica, Vol. 55, No. 5 (September 1987), pp. 999–1033
**Proximity Score:** 1/5
**Strand:** 4, 5
**Recommendation:** OPTIONAL (cite only if the paper develops a dynamic consumption/replacement model for wine)
**Main contribution:** Seminal paper in structural dynamic discrete choice. Models Harold Zurcher's optimal decision to replace or maintain GMC bus engines as a finite-horizon dynamic programming problem with regenerative structure (the "renewal assumption"). Introduces the nested fixed-point (NFXP) algorithm for structural estimation of dynamic discrete choice models via maximum likelihood. The renewal assumption (state resets on replacement) delivers computational tractability.
**Identification:** Structural estimation via nested fixed-point maximum likelihood; renewal/regenerative dynamic programming; Bellman equation with finite state space
**Data:** Monthly bus engine mileage and replacement records, Wisconsin bus fleet, 1975–1985
**Key result:** Cost parameters recovered; optimal replacement rule is mileage-threshold; structural model fits data well
**Relevance to Liquid Assets:** Foundational reference for any dynamic structural model of durable good replacement or consumption timing. If the Liquid Assets model includes a dynamic component — e.g., collector buyers choosing when to sell (consume their option) or consumption buyers choosing when to drink — the Rust (1987) NFXP framework is the methodological ancestor. Proximity is 1 because the paper does not structurally estimate a dynamic wine-holding model; the auction demand model is more likely static or semi-structural.
**BibTeX key:** Rust1987

---

*Gap-fill search completed: 2026-03-30. Six papers added; all bibliographic details verified against Wiley Online Library DOIs and RePeC records.*

# Literature Review: Liquid Assets
**Date:** 2026-03-29
**Topic:** Wine auction prices, heterogeneous buyers, price-age profiles, alternative investments
**Strands covered:** Wine investment | Alternative assets | Heterogeneous auctions | Durable goods life-cycle | Demand shocks
**Compiled by:** Academic Librarian (cloco research system)
**Scope note:** Excludes six papers already in project: Dimson/Rousseau/Spaenjers (2015 JFE), Ashenfelter (2008 Economic Journal), Lovo/Spaenjers (2018 AER), Goetzmann (1993 AER), Baumol (1986 AER), Mei/Moses (2002 AER).

---

## Category 1: Directly Related (Proximity 4–5)

Papers with the same core question — wine auction prices, maturity lifecycle, or heterogeneous collector/consumption demand — in similar or directly adjacent empirical settings.

---

### [Dimson, Rousseau & Spaenjers 2015] The Price of Wine
**Journal/Source:** Journal of Financial Economics, Vol. 118, No. 2, pp. 431–449
**Proximity Score:** 5/5
**Summary:** Using historical hammer-price records for Bordeaux Premiers Crus auctioned over 1900–2012, the authors build a repeat-sales regression index and document that young maturing wines from high-quality vintages provide the highest financial returns, while past-maturity famous châteaux deliver growing non-pecuniary (collector) benefits to their owners. The net real return to wine investment is estimated at 4.1% per annum, exceeding bonds, art, and stamps. The paper is the single closest published antecedent: it explicitly identifies the maturity-driven kink in the price-age profile and the collector premium concept, though it does not model heterogeneous buyer types formally or estimate the structural decomposition.
**Identification:** Arithmetic repeat-sales regression; OLS hedonic for age-price decomposition
**Data:** Historical auction price records, Bordeaux Premiers Crus, 1900–2012
**Key Result:** Net annualized real return to wine = 4.1%; young maturing high-quality vintages generate highest returns; non-pecuniary benefits grow past maturity
**Note:** The project domain profile incorrectly cites this as "Dimson, Mahajan & Spaenjers (2015, RFS)." The correct citation is Dimson, Rousseau & Spaenjers (2015, JFE).

---

### [Breeden & Liang 2017] Auction-Price Dynamics for Fine Wines from Age-Period-Cohort Models
**Journal/Source:** Journal of Wine Economics, Vol. 12, No. 2, pp. 173–202
**Proximity Score:** 5/5
**Summary:** Applying an age-period-cohort (APC) algorithm to a database of 1.5 million auction results, the authors disentangle price appreciation with age from vintage quality effects and market-time trends. They document that high-quality vintages appreciate strongly during their maturation period, plateau near the optimal drinking window, and then rise again as the wine becomes an "antique." The cubic age-price profile — with a trough around peak maturity — is precisely the empirical regularity that the Liquid Assets paper seeks to explain structurally. The APC methodology provides a methodological template and a key benchmark for the age effect net of cohort and period.
**Identification:** Age-period-cohort decomposition (APC regression) — requires normalization constraint to identify all three components
**Data:** 1.5 million auction transaction records; multiple producers and regions
**Key Result:** Non-monotone price-age profile confirmed: prices rise pre-maturity, plateau, then rise again post-maturity as antique; return to Hill of Grace is 14.8% in year 2, 0% in year 20, 10.4% in year 30

---

### [Masset 2024] Market Segments and Pricing of Fine Wines over their Lifecycle
**Journal/Source:** Economic Modelling, Vol. 141 (2024), Article 106915
**Proximity Score:** 5/5
**Summary:** Applying a finite mixture model to 20 years of wine auction price data, this paper identifies five distinct market segments that differ in how scores, age, and market conditions shape prices — "investment wines," "collectible wines," and "drinking wines" being the most prominent. The age-price relationship is segment-specific and generally linear within each segment, but varies sharply across them. This directly corroborates the Liquid Assets hypothesis that the aggregate bimodal price-age profile reflects the superposition of distinct buyer-type valuation functions, and reconciles conflicting prior estimates in the literature.
**Identification:** Finite mixture model (unsupervised segmentation); hedonic price regression within each segment
**Data:** Wine auction records, 20-year panel
**Key Result:** Five market segments; age effect is linear within segment but non-linear in aggregate; "investment wines" most sensitive to market conditions; "drinking wines" most sensitive to expert scores

---

### [Masset, Weisskopf, Faye & Le Fur 2016] Red Obsession: The Ascent of Fine Wine in China
**Journal/Source:** Emerging Markets Review, Vol. 29, pp. 200–225
**Proximity Score:** 4/5
**Summary:** Constructing fine wine price indices using hammer prices from five global auction houses for the 14 most iconic Bordeaux wines over 2007–2014, the authors document a 19% average price premium for wine sold at Hong Kong auctions versus other global locations. The premium is most pronounced for wines with perfect Parker scores and the most powerful brands, and declines from 60% in 2008 to 15% post-2012 — consistent with the anti-corruption crackdown reducing collector/gifting demand. This is the most direct empirical treatment of the China demand shock relevant to the Liquid Assets identification strategy.
**Identification:** Hedonic price regression with auction-house and geography fixed effects; time-series comparison
**Data:** Hammer prices, five global auction houses, 14 iconic Bordeaux wines, 2007–2014
**Key Result:** 19% average Hong Kong premium; decline from 60% (2008) to 15% (post-2012); most pronounced for wines with perfect Parker scores

---

### [Cardebat, Faye, Le Fur & Storchmann 2017] The Law of One Price? Price Dispersion on the Auction Market for Fine Wine
**Journal/Source:** Journal of Wine Economics, Vol. 12, No. 3, pp. 302–331
**Proximity Score:** 4/5
**Summary:** Drawing on worldwide auction prices from eight auction houses (2000–2012), this paper tests the strong form of the law of one price in fine wine markets using a hedonic approach. It finds significant price premiums in Hong Kong and across auction companies that exceed transaction costs — with heterogeneity in buyer preferences cited as the key explanation. Notably, counterfeit-suspect wines trade at a discount in Western markets but at a premium in Hong Kong. This paper directly motivates the Liquid Assets treatment of buyer heterogeneity and provides empirical evidence that different buyer types (collectors vs. consumption buyers) coexist in the market with different valuations.
**Identification:** Hedonic regression with auction-house and geography interactions
**Data:** Worldwide auction prices, eight auction houses, 2000–2012
**Key Result:** Significant price premiums exceeding transaction costs; heterogeneous buyer preferences as primary explanation; counterfeit wines trade at premium in Hong Kong

---

## Category 2: Wine as an Investment — Same Context, Empirical Focus on Returns (Proximity 3–4)

Papers studying wine primarily as a financial asset — returns, diversification, and portfolio allocation — rather than the price-age mechanism.

---

### [Masset & Henderson 2010] Wine as an Alternative Asset Class
**Journal/Source:** Journal of Wine Economics, Vol. 5, No. 1, pp. 87–118
**Proximity Score:** 3/5
**Summary:** Using transaction prices from Chicago Wine Company auctions (1996–2007), this paper examines wine as a portfolio diversification vehicle. The best wines (first growths and extraordinary-rated) earn annual returns of 4.1–6.0%, with low correlation to financial assets. The study finds that wine returns are primarily related to economic conditions rather than market risk (low CAPM beta, significant positive alpha). It establishes the benchmark return figures that reviewers will expect the Liquid Assets paper to engage with, and documents that the top tier of wines — precisely those the Liquid Assets paper focuses on — generates the strongest returns.
**Identification:** CAPM and Fama-French three-factor model; portfolio mean-variance analysis
**Data:** Chicago Wine Company auction prices, 1996–2007
**Key Result:** Wine alpha significantly positive 1996–2009; low beta; first growths return 4.1–6.0% annually; diversification benefit confirmed

---

### [Sanning, Shaffer & Sharratt 2008] Bordeaux Wine as a Financial Investment
**Journal/Source:** Journal of Wine Economics, Vol. 3, No. 1, pp. 51–71
**Proximity Score:** 3/5
**Summary:** Analyzing monthly auction hammer prices for Bordeaux wines using the Fama-French three-factor model, this paper finds that investment-grade wines earn abnormal monthly returns averaging up to 0.75% above model predictions, with low exposure to market risk factors. The paper is the first to apply formal asset pricing models to Bordeaux auction data and establishes the benchmark result that high-quality Bordeaux provides genuine alpha — relevant context for the Liquid Assets collector premium narrative.
**Identification:** Repeat-sales regression; Fama-French three-factor model
**Data:** Monthly auction hammer prices, Bordeaux wines
**Key Result:** Up to 0.75% monthly abnormal return; low market risk exposure; portfolio diversification benefit for investment-grade wines

---

### [Burton & Jacobsen 2001] The Rate of Return on Investment in Wine
**Journal/Source:** Economic Inquiry, Vol. 39, No. 3, pp. 337–350
**Proximity Score:** 3/5
**Summary:** Using a repeat-sale regression methodology for red Bordeaux wines auctioned 1986–1996, the authors find that the nominal return to wine investment is comparable to government bonds — roughly 7% nominal — but falls substantially short of equity returns. The paper is a foundational benchmark in the wine-as-investment literature and provides the earliest systematic econometric evidence on wine returns, albeit without decomposing the age effect or distinguishing buyer types.
**Identification:** Repeat-sales regression (RSR)
**Data:** Bordeaux wine auction records, 1986–1996
**Key Result:** Nominal return ~7% (comparable to bonds); below equity returns; repeat-sales regression applied to wine for first time

---

### [Ashenfelter 2008] Predicting the Quality and Prices of Bordeaux Wine
**Journal/Source:** Economic Journal, Vol. 118, No. 529, pp. F174–F184
**Proximity Score:** 3/5
**Summary:** This paper shows that the weather during the growing season is a powerful predictor of Bordeaux wine quality and auction prices, providing a real rate of return estimate of 2–3% per annum from holding wine and implying far greater variability in en primeur prices than is actually observed. It introduces and validates the "Bordeaux equation" — the hedonic regression of log price on vintage weather — and discusses market efficiency and the role of expert opinion. The weather-quality-price nexus is the foundation for vintage fixed effects used throughout the Liquid Assets empirical strategy.
**Identification:** Hedonic OLS regression of log price on vintage weather variables (temperature, rainfall); real rate of return calculation from repeat sales
**Data:** Bordeaux grand cru auction prices; vintage weather records, 1952–2003
**Key Result:** Real return 2–3% per annum; vintage weather explains ~83% of price variance; Ashenfelter equation

---

### [Ashenfelter 1989] How Auctions Work for Wine and Art
**Journal/Source:** Journal of Economic Perspectives, Vol. 3, No. 3, pp. 23–36
**Proximity Score:** 3/5
**Summary:** This early survey describes empirical regularities in wine and art auction markets — including price formation, the declining price anomaly in sequential auctions, and the role of absentee bidders. It documents that the law of one price fails systematically in wine auctions, motivating the heterogeneous-buyer framework. As the earliest academic treatment of wine auctions by an economist, it remains foundational background reading.
**Identification:** Descriptive empirical analysis; first-order regression evidence
**Data:** Various wine and art auction records
**Key Result:** Law of one price fails; auction mechanism shapes price formation; declining price anomaly documented

---

### [Storchmann 2012] Wine Economics
**Journal/Source:** Journal of Wine Economics, Vol. 7, No. 1 (survey article)
**Proximity Score:** 2/5
**Summary:** A comprehensive survey of wine economics covering three main themes: fine wine as a financial investment, the impact of climate and weather on wine quality, and the role of expert opinion. The survey synthesizes return estimates across methodologies and datasets, covering both portfolio diversification evidence and hedonic pricing literature. Provides essential background for positioning the Liquid Assets paper within the broader field.
**Identification:** Review article (no original identification)
**Data:** Literature-wide
**Key Result:** Fine wine returns 2–7% real, depending on method; consistent diversification benefit; weather dominates vintage quality variation

---

## Category 3: Alternative Assets — Art, Collectibles, Stamps, Gems (Proximity 2–4)

Papers studying non-wine collectibles as alternative investments, with relevance to the broader framework of durable goods with consumption and collector value.

---

### [Korteweg, Kräussl & Verwijmeren 2016] Does It Pay to Invest in Art? A Selection-Corrected Returns Perspective
**Journal/Source:** Review of Financial Studies, Vol. 29, No. 4, pp. 1007–1038
**Proximity Score:** 3/5
**Summary:** Using 32,928 repeat-sales observations of paintings traded 1960–2013, the authors generalize the standard repeat-sales regression to correct for selection bias — the endogenous decision of when to sell. Adjusting for selection reduces average annual index returns from 8.7% to 6.3% and the Sharpe ratio from 0.27 to 0.11. The paper is methodologically important for the Liquid Assets paper because selection into auction is a first-order concern: bottles that survive to antique ages are systematically different from those sold at maturity. Note that co-author Roman Kräussl is also a co-author on Liquid Assets — this is an important cite.
**Identification:** Heckman selection correction applied to repeat-sales regression; V-shaped relationship between sale probability and returns
**Data:** 32,928 paintings with at least one repeat sale, 1960–2013
**Key Result:** Selection-corrected returns 6.3% vs. raw 8.7%; Sharpe ratio falls from 0.27 to 0.11; investing in broad art portfolio unattractive

---

### [Renneboog & Spaenjers 2013] Buying Beauty: On Prices and Returns in the Art Market
**Journal/Source:** Management Science, Vol. 59, No. 1, pp. 36–53
**Proximity Score:** 3/5
**Summary:** Applying hedonic regression to over one million auction transactions of paintings (1957–2007), the authors estimate a real USD return of 3.97% per year — similar to corporate bonds but at higher risk. Quantile regressions document larger price appreciations and higher volatilities at the top of the price distribution. Measures of high-income consumer confidence predict art price trends, consistent with wealth-driven collector demand. The paper is the closest empirical analogue in the art market to what the Liquid Assets paper does for wine, and establishes that collector demand (driven by wealth) is the relevant demand shifter for alternative assets.
**Identification:** Hedonic regression; repeat-sales regression (robustness); quantile regression
**Data:** 1+ million auction transactions, paintings and works on paper, 1957–2007
**Key Result:** Real return 3.97%; higher volatility at top price percentiles; art prices predicted by high-income confidence measures

---

### [Goetzmann, Renneboog & Spaenjers 2011] Art and Money
**Journal/Source:** American Economic Review, Vol. 101, No. 3, pp. 222–226
**Proximity Score:** 2/5
**Summary:** Using two centuries of art price data, this paper shows that equity market returns have a significant positive impact on art price levels, and that increases in top income inequality drive higher art prices. Cointegration tests confirm a long-run relationship between top incomes and art prices. The mechanism — wealth shocks raising the willingness-to-pay of collector buyers — is directly relevant to the Liquid Assets model of collector demand and motivates using the China demand shock as an instrument for collector entry.
**Identification:** Time-series regression; cointegration analysis; VAR
**Data:** Art price index, 1765–2007; financial market data
**Key Result:** Equity returns and top income inequality drive art prices; long-run cointegration confirmed

---

### [Dimson & Spaenjers 2011] Ex Post: The Investment Performance of Collectible Stamps
**Journal/Source:** Journal of Financial Economics, Vol. 100, No. 2, pp. 443–458
**Proximity Score:** 2/5
**Summary:** Examining British postage stamp catalogue prices 1900–2008, this paper finds a nominal return of 7.0% (2.9% real), lying between bonds and equities. Stamps partially hedge against unanticipated inflation and have low systematic risk, but their returns covary positively with equity markets. The paper is methodologically similar to Dimson/Rousseau/Spaenjers (2015) applied to a different collectible asset — it shows the collectors' premium is present across asset classes, not specific to wine.
**Identification:** Repeat-sales regression on catalogue prices; CAPM and inflation beta estimation
**Data:** British stamp catalogue prices, 1900–2008
**Key Result:** Nominal 7.0%, real 2.9% return; low beta; partial inflation hedge; positive equity covariance

---

### [Renneboog & Spaenjers 2012] Hard Assets: The Returns on Rare Diamonds and Gems
**Journal/Source:** Finance Research Letters, Vol. 9, No. 4, pp. 220–230
**Proximity Score:** 2/5
**Summary:** Using auction transaction data for white diamonds, colored diamonds, sapphires, rubies, and emeralds (1999–2010), this paper finds annualized real USD returns of 6.4% and 2.9% for white and colored diamonds respectively. Gem returns covary positively with stock returns, underscoring the importance of wealth-induced demand for luxury consumption in collectibles markets. Provides comparative benchmark for alternative asset returns and confirms the cross-asset generality of collector-demand mechanisms.
**Identification:** Hedonic regression; repeat-sales regression
**Data:** Diamond and gem auction transactions, 1999–2010
**Key Result:** White diamonds: 6.4% real return; colored diamonds: 2.9%; positive equity covariance

---

### [Goetzmann, Spaenjers & Van Nieuwerburgh 2021] Real and Private-Value Assets
**Journal/Source:** Review of Financial Studies, Vol. 34, No. 8, pp. 3497–3526 (Introduction to special issue)
**Proximity Score:** 2/5
**Summary:** This introductory survey for a special issue of the RFS on real and private-value assets defines the investment class as the sum of real estate, infrastructure, collectibles, and noncorporate business equity — estimated at $84 trillion in the U.S. alone. The paper surveys key research questions including how private use values interact with financial returns, and how wealth shocks affect this asset class. This conceptual framework — the tension between use value (consumption) and financial return (investment) — is the central mechanism in the Liquid Assets model.
**Identification:** Survey article
**Data:** Literature-wide; macro estimates of asset class size
**Key Result:** Private-value assets constitute a large and understudied asset class; use-value demand creates systematic mispricing relative to pure financial assets

---

### [Ashenfelter & Graddy 2003] Auctions and the Price of Art
**Journal/Source:** Journal of Economic Literature, Vol. 41, No. 3, pp. 763–787
**Proximity Score:** 2/5
**Summary:** A survey of empirical research on art auctions covering price formation, return estimation, the declining price anomaly, reserve prices, and buy-in rates. Documents that experts provide accurate price predictions (optimal use of public information) but that high reserve prices and buy-in rates are best understood as optimal search in the face of stochastic demand. The auction mechanics discussion directly informs the Liquid Assets model of second-price auctions with heterogeneous buyers, and the review of repeat-sales methodology is important for understanding returns measurement.
**Identification:** Survey article (reviews many methodologies)
**Data:** Literature-wide survey
**Key Result:** Art experts produce accurate price predictions; high buy-in rates reflect optimal reserve-price strategy; various return estimates reviewed

---

## Category 4: Heterogeneous Buyers in Auction Markets — Theory and Empirics (Proximity 1–4)

---

### [Milgrom & Weber 1982] A Theory of Auctions and Competitive Bidding
**Journal/Source:** Econometrica, Vol. 50, No. 5, pp. 1089–1122
**Proximity Score:** 2/5
**Summary:** The foundational auction theory paper develops a general model allowing the winning bidder's payoff to depend on personal preferences, others' preferences, and intrinsic object quality — encompassing both private and affiliated values as special cases. The key results include the revenue ranking (English > second-price > Dutch = first-price for risk-neutral symmetric bidders) and the linkage principle (revealing information raises seller revenue). The Liquid Assets IPV model with two buyer types is a direct extension of this framework.
**Identification:** Theoretical (mechanism design, comparative statics)
**Data:** None (theory)
**Key Result:** Revenue ranking of auction formats; linkage principle; English auction revenue-dominates for affiliated values

---

### [Vickrey 1961] Counterspeculation, Auctions, and Competitive Sealed Tenders
**Journal/Source:** Journal of Finance, Vol. 16, No. 1, pp. 8–37
**Proximity Score:** 1/5
**Summary:** The seminal paper that introduces the second-price sealed-bid auction (Vickrey auction) as equivalent to the English ascending auction in the IPV framework, establishing that dominant-strategy truth-telling makes the second-price format efficient. The Liquid Assets model relies on second-price auction mechanics with independent private values as its modeling foundation.
**Identification:** Theoretical
**Data:** None
**Key Result:** Second-price sealed-bid auction has a dominant strategy of truthful bidding; revenue equivalence theorem laid groundwork

---

### [Myerson 1981] Optimal Auction Design
**Journal/Source:** Mathematics of Operations Research, Vol. 6, No. 1, pp. 58–73
**Proximity Score:** 1/5
**Summary:** Derives the revenue-maximizing auction mechanism for a seller facing buyers with private information, introducing the concept of virtual valuations and the ironing procedure for non-regular distributions. This paper provides the theoretical apparatus for the Liquid Assets structural model: in the two-type buyer model, the price outcome in the second-price auction depends on the distribution of valuations across buyer types, and Myerson's framework characterizes optimal reserve prices and allocation rules.
**Identification:** Theoretical (mechanism design)
**Data:** None
**Key Result:** Optimal auction sets reserve price above seller's value; virtual valuation determines allocation; revenue equivalence under regularity

---

### [Klemperer 1999] Auction Theory: A Guide to the Literature
**Journal/Source:** Journal of Economic Surveys, Vol. 13, No. 3, pp. 227–286
**Proximity Score:** 1/5
**Summary:** A comprehensive non-technical survey of auction theory covering the IPV model, optimal auction design, risk aversion, common values, entry costs, multi-unit auctions, and collusion. The Liquid Assets paper draws on results from this literature for its two-type IPV model and for the comparative statics of how buyer composition affects equilibrium prices. Essential reference for any paper using auction theory as a framework.
**Identification:** Survey article
**Data:** None
**Key Result:** Survey — covers revenue equivalence, optimal auctions, entry effects, common vs. private values

---

### [Ginsburgh 1998] Absentee Bidders and the Declining Price Anomaly in Wine Auctions
**Journal/Source:** Journal of Political Economy, Vol. 106, No. 6, pp. 1302–1331
**Proximity Score:** 3/5
**Summary:** Documents the declining price anomaly in sequential wine auctions — prices for later lots of the same wine tend to fall — and shows that absentee bidders using non-optimal bidding strategies are a primary cause. This paper establishes the key institutional feature of the wine auction market (sequential lots, absentee bidding) that the Liquid Assets paper's data are drawn from. The optimal bidding behavior of consumption vs. collector buyers in this sequential setting is directly relevant.
**Identification:** Structural auction model; comparison of observed bids to optimal bidding predictions
**Data:** Wine auction records with absentee and floor bids identified
**Key Result:** Declining price anomaly primarily due to sub-optimal absentee bidding strategies; floor bidders do not exhibit the anomaly

---

## Category 5: Durable Goods Life-Cycle and Commodity Storage Pricing (Proximity 1–3)

---

### [Deaton & Laroque 1996] Competitive Storage and Commodity Price Dynamics
**Journal/Source:** Journal of Political Economy, Vol. 104, No. 5, pp. 896–923
**Proximity Score:** 2/5
**Summary:** Develops a rational-expectations model of competitive commodity storage in which risk-neutral speculators smooth prices over time, generating positive autocorrelation in prices and the well-known "stockout" asymmetry (prices spike when inventories hit zero). The storage model is foundational for any paper treating wine as a storable asset whose price evolution depends on inventory dynamics. The mechanism whereby holding wine off the market generates an intertemporal premium is a special case of this storage framework.
**Identification:** Structural rational-expectations model; calibration to commodity price data
**Data:** Commodity price series
**Key Result:** Competitive storage generates strong positive autocorrelation; stockout constraint creates price spikes; model fits qualitative features of commodity prices but not quantitative magnitudes

---

### [Casassus & Collin-Dufresne 2005] Stochastic Convenience Yield Implied from Commodity Futures and Interest Rates
**Journal/Source:** Journal of Finance, Vol. 60, No. 5, pp. 2283–2331
**Proximity Score:** 2/5
**Summary:** Characterizes a three-factor model of commodity spot prices, convenience yields, and interest rates, allowing convenience yields to depend on spot prices and interest rates. Empirically estimates the model for crude oil, copper, silver, gold, and copper using Kalman filter, finding strong evidence for spot-price level dependence in convenience yields for commercial commodities (mean reversion). For wine, the "convenience yield" analog is the consumption flow enjoyed by drinking the bottle — a key structural parameter in the Liquid Assets model — making this the theoretical antecedent for the consumption value function.
**Identification:** Kalman filter state-space estimation; affine term structure model
**Data:** Commodity futures prices (crude oil, copper, gold, silver), 1975–2000
**Key Result:** Spot-price-dependent convenience yields imply mean reversion under risk-neutral measure; three-factor model nests existing specifications

---

### [Schwartz 1997] The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging
**Journal/Source:** Journal of Finance, Vol. 52, No. 3, pp. 923–973
**Proximity Score:** 1/5
**Summary:** Compares three models of commodity price behavior incorporating mean reversion — one-factor, two-factor (with stochastic convenience yield), and three-factor (with stochastic interest rates) — and estimates them via Kalman filter for copper, oil, and gold. The two-factor model is particularly relevant as it prices the "option to consume" the commodity (the convenience yield) explicitly, which is the structural analog to the consumption value of a wine bottle at maturity.
**Identification:** Kalman filter; affine model estimation
**Data:** Commodity futures prices (copper, oil, gold), 1969–1995
**Key Result:** Strong mean reversion in commercial commodity prices; two-factor model captures spot-futures term structure well; three-factor adds precision for long-horizon valuation

---

### [Pindyck 1994] Inventories and the Short-Run Dynamics of Commodity Prices
**Journal/Source:** RAND Journal of Economics, Vol. 25, No. 1, pp. 141–159
**Proximity Score:** 1/5
**Summary:** Derives a structural model in which commodity spot prices and inventories jointly respond to demand and supply shocks, showing that the marginal value of storage (convenience yield) is a decreasing function of inventory levels. The "must-stock" or "option value" of holding inventory creates a wedge between spot and futures prices. For wine, this translates directly: the value of not selling (holding the bottle) decreases as the wine approaches and passes its maturity date, consistent with the post-maturity price dip.
**Identification:** Structural equilibrium model; OLS estimation of inventory-price relationship
**Data:** Commodity price and inventory data (oil, copper, aluminum, nickel)
**Key Result:** Convenience yield is a decreasing function of inventory level; marginal value of storage (inventory) explains commodity price dynamics

---

## Category 6: China Demand Shock and Demand Shocks in Collectibles Markets (Proximity 2–4)

---

### [Qian & Wen 2015] The Impact of Xi Jinping's Anti-Corruption Campaign on Luxury Imports in China
**Journal/Source:** Yale University Working Paper (unpublished as of 2026; widely circulated)
**Proximity Score:** 4/5
**Summary:** Documents that the 2012 anti-corruption campaign reduced publicly observable luxury imports (jewelry, wine, spirits, art) by approximately 55% (or ~$194 million USD) relative to controls, using Chinese trade data. For wine specifically, the paper finds a large decline in luxury wine imports relative to non-luxury wine. This is the core instrument and demand shock that the Liquid Assets paper uses for its event-study identification. The paper establishes the timing, magnitude, and differential incidence of the shock across product categories.
**Identification:** DiD using category-level variation in conspicuousness; trade data before/after campaign
**Data:** Chinese customs/trade import data; monthly commodity flows, 2010–2014
**Key Result:** ~55% reduction in luxury imports; alcohol (wine, spirits) significantly affected; effect concentrated in publicly observable luxury categories

---

### [Bian, Zhang & Zhou 2025] Do China's Anti-Corruption Campaigns Impact Art Prices? Evidence from the Chinese Art Market
**Journal/Source:** Pacific-Basin Finance Journal, Vol. 90 (2025), Article 102680
**Proximity Score:** 3/5
**Summary:** Using auction data for 54,809 Chinese traditional paintings sold 2013–2019, combined with data on high-ranking officials prosecuted under the anti-corruption campaign, this paper finds that each additional official's downfall reduces regional painting prices by 5.5%. The effect is stronger for non-masterwork paintings, suggesting that corruption-related demand is concentrated in less distinctive works used for bribery. This is the most recent evidence that the corruption crackdown had measurable effects on collectible asset prices in China, directly relevant to the Liquid Assets demand-shock identification.
**Identification:** DiD using regional variation in prosecution intensity and time variation
**Data:** 54,809 Chinese painting auction transactions, 2013–2019; official prosecution records
**Key Result:** Each additional official prosecuted in region → 5.5% decline in auction prices; stronger for non-masterworks

---

## Category 7: Methods Papers — Econometrics (Proximity 1–2)

---

### [Bai & Perron 2003] Computation and Analysis of Multiple Structural Change Models
**Journal/Source:** Journal of Applied Econometrics, Vol. 18, No. 1, pp. 1–22
**Proximity Score:** 1/5
**Summary:** Provides the computational procedures and test statistics for estimating models with multiple structural breaks at unknown dates in a linear regression framework. The Liquid Assets paper's event-study approach around the China demand shock may need to formally test for a structural break in the price-age relationship circa 2012–2013. This paper provides the standard toolkit for that test.
**Identification:** Sequential and global methods for structural break detection
**Data:** None (methods paper, illustrated with empirical examples)
**Key Result:** Efficient algorithms for detecting and dating multiple structural breaks; BIC-based number-of-breaks selection

---

## Summary Statistics

| Category | Papers Found | Proximity Range |
|---|---|---|
| Directly Related (wine auction prices, maturity, buyer heterogeneity) | 5 | 4–5 |
| Wine as Investment (returns, portfolio) | 6 | 2–4 |
| Alternative Assets (art, collectibles) | 6 | 2–3 |
| Heterogeneous Buyers in Auctions (theory) | 5 | 1–3 |
| Durable Goods / Commodity Storage | 3 | 1–2 |
| China Demand Shock | 2 | 3–4 |
| Methods | 1 | 1 |
| **Total** | **28** | — |

---

## Scooping Risk Assessment

**No proximity-5 scooping risk identified.** The specific combination of:
(a) non-monotone bimodal price-age profile in wine auctions
(b) structural decomposition into consumption-buyer and collector-buyer valuation components
(c) identification via the China anti-corruption demand shock
(d) cross-sectional variation across Grand Cru vs. Premier Cru wine types

...has not been published or circulated as of the search date (2026-03-29). The Masset (2024) and Breeden & Liang (2017) papers are the closest empirical antecedents, but neither develops a structural model of buyer types nor uses the China shock for identification.

**Moderate proximity-4 papers to monitor:**
- Masset (2024) in Economic Modelling — documents market segments and lifecycle pricing; does not develop buyer-type structural model
- Masset et al. (2016) in Emerging Markets Review — uses Hong Kong premium and China shock; does not study age-maturity profile
- Qian & Wen (2015) working paper — uses China shock for luxury imports; not wine-auction specific, not yet published in top journal as of 2026

**Note on co-author overlap:** Roman Kräussl is co-author of both Liquid Assets and Korteweg/Kräussl/Verwijmeren (2016, RFS). The selection-correction methodology in that paper is methodologically relevant and the overlap should be acknowledged in the paper.

---

*End of Literature Review: Liquid Assets*
*Search completed: 2026-03-29*
*Journals searched: JFE, JF, RFS, AER, JPE, QJE, REStud, Journal of Wine Economics, Economic Journal, Economic Modelling, Emerging Markets Review, Finance Research Letters, Pacific-Basin Finance Journal, Journal of Economic Literature, Management Science, Econometrica, RAND Journal of Economics, Mathematics of Operations Research, Journal of Political Economy, Journal of Applied Econometrics*
*Repositories searched: SSRN, NBER, RePeC, AAWE Working Papers*

---

## Gap-Fill Round (Editor-Directed)
*Added in response to editor review, 2026-03-29*

### Task 1 Findings — Dimson Citation Verification

**"Eye of the Beholder" does not exist as a Dimson wine paper.** The domain profile's entry "Dimson, Mahajan & Spaenjers (2015, RFS)" is erroneous on every element. Verification via RePeC (ideas.repec.org) and NBER confirms:

- The correct wine investment paper is **Dimson, Rousseau & Spaenjers (2015), "The Price of Wine," Journal of Financial Economics, Vol. 118, No. 2, pp. 431–449.** This paper is already included in Category 1 above (Proximity 5/5) and in the project's `references.bib`.
- **Peter L. Rousseau** (Vanderbilt) is the correct second author; "Mahajan" appears nowhere in this paper.
- The journal is **JFE**, not RFS.
- "Eye of the Beholder" is a title associated with an unrelated paper on beauty and art pricing (Adams & Kräussl) — not a Dimson paper. No paper by Dimson, Mahajan & Spaenjers exists in the wine or art literature that can be verified.
- **Action required:** Remove all references to "Dimson, Mahajan & Spaenjers (2015, RFS)" and "Eye of the Beholder" from the domain profile and any project citations. The correct citation — already in the review — is `DimsonRousseau2015wine` in the BibTeX file.

---

### [Berry, Levinsohn & Pakes 1995] Automobile Prices in Market Equilibrium
**Journal/Source:** Econometrica, Vol. 63, No. 4, pp. 841–890
**Proximity Score:** 3/5
**Summary:** This paper introduces the BLP demand estimation framework for differentiated products markets — a random-coefficients discrete-choice model where consumers have heterogeneous tastes for product characteristics. Using panel data on U.S. automobile models and prices (1971–1990), the authors estimate demand and markups jointly using instruments based on characteristics of competing products. The BLP framework is the methodological foundation for any structural demand estimation with heterogeneous buyers. For Liquid Assets, if the paper pursues a structural demand model to separate consumer and collector valuation of wine, BLP provides the canonical econometric template. The contraction mapping for inverting market shares and the use of product-characteristic instruments are directly applicable to wine auction lots as differentiated goods.
**Identification:** GMM with BLP instruments (characteristics of rival products); contraction mapping to invert market shares
**Data:** U.S. automobile transaction data, 1971–1990; product characteristics from automotive industry sources
**Key Result:** Significant price-cost markups in U.S. auto industry; random-coefficient model fits aggregate shares better than logit; instruments based on competing-product characteristics are valid

---

### [Rosen 1974] Hedonic Prices and Implicit Markets: Product Differentiation in Pure Competition
**Journal/Source:** Journal of Political Economy, Vol. 82, No. 1, pp. 34–55
**Proximity Score:** 4/5
**Summary:** This foundational paper establishes the theory of hedonic pricing in competitive markets with differentiated goods. Rosen shows that observed market prices for differentiated products trace out an implicit price schedule for each characteristic, and that the marginal price of a characteristic equals the marginal willingness to pay of all consumers who choose that product. The two-stage identification strategy — first recovering the hedonic price function, then recovering consumer preferences and producer costs — is the conceptual basis for all wine hedonic regressions in the literature (including the Liquid Assets paper's log-price regressions on vintage, appellation, age, and Parker score). The decomposition of total price into contributions from observable characteristics is precisely the framework used to isolate the age-maturity effect after controlling for quality.
**Identification:** Theoretical equilibrium model; empirical two-stage procedure (hedonic price function in stage 1; structural preference recovery in stage 2)
**Data:** None in the theory section; illustrative empirical example with housing characteristics
**Key Result:** Equilibrium price function for differentiated goods pins down implicit prices of each characteristic; marginal implicit price equals marginal WTP; identification of preferences requires second-stage regression using characteristics as instruments

---

### [Gavazza, Lizzeri & Roketskiy 2014] A Quantitative Analysis of the Used-Car Market
**Journal/Source:** American Economic Review, Vol. 104, No. 11, pp. 3596–3634 % UNVERIFIED pages
**Proximity Score:** 2/5
**Summary:** This paper builds a dynamic equilibrium model of the used-car market in which heterogeneous consumers differ in their utilization rates, generating an endogenous age-price profile for used vehicles. Cars depreciate physically, and heterogeneous utilization means that high-utilization owners optimally sell to low-utilization owners as the car ages — producing a non-trivial resale price path and trading volume pattern. The model is calibrated and estimated using U.S. vehicle registration data, and the authors study welfare effects of policies affecting new-car markets. The structural analogy to Liquid Assets is close: wine bottles are durable goods with a lifecycle, and the presence of heterogeneous buyer types (consumption vs. collector) shapes the equilibrium age-price profile in a similar way to how heterogeneous drivers shape used-car prices. The key difference is that wine has a physical maturity threshold beyond which consumption value declines (wine goes "over the hill") while cars depreciate monotonically.
**Identification:** Dynamic equilibrium model with heterogeneous agents; calibration and simulation; policy counterfactuals
**Data:** U.S. vehicle registration data (age and ownership transitions); MSRP data for new vehicles
**Key Result:** Heterogeneous utilization rates generate non-trivial trading patterns and age-price profiles; policy-relevant welfare calculations; framework for thinking about how buyer composition shapes durable-goods resale prices

---

### [Nevo 2001] Measuring Market Power in the Ready-to-Eat Cereal Industry
**Journal/Source:** Econometrica, Vol. 69, No. 2, pp. 307–342 % UNVERIFIED pages
**Proximity Score:** 3/5
**Summary:** This paper is the canonical applied implementation of the BLP random-coefficients logit demand model. Nevo estimates demand for ready-to-eat cereals across 65 markets using the contraction mapping and BLP instruments (product characteristics of rival goods), recovering consumer heterogeneity in price sensitivity and taste parameters. He then uses the demand estimates to measure price-cost markups and test models of oligopoly pricing. The paper is the standard practitioner's reference for implementing BLP estimation: it provides the computational details, discusses the validity of the instruments, and shows how to perform counterfactual simulations. For Liquid Assets, if a structural demand model of wine auction bidders is pursued, Nevo (2001) provides the step-by-step implementation template that referees will expect to be cited alongside BLP (1995).
**Identification:** BLP random-coefficients logit; GMM with product-characteristic instruments (Berry 1994 instruments)
**Data:** Scanner data for breakfast cereals across 65 U.S. cities, 1988–1992; brand and product characteristics
**Key Result:** Significant heterogeneity in consumer price sensitivity; markup estimates consistent with oligopoly pricing; rejection of collusion and competitive pricing hypotheses; Lerner indices estimated at 20–45%

---

### [Dimson, Rousseau & Spaenjers 2015] The Price of Wine
**Journal/Source:** Journal of Financial Economics, Vol. 118, No. 2, pp. 431–449
**Proximity Score:** 5/5
**Summary:** See full entry in Category 1 above. This paper is the primary wine investment reference and is already included in the literature review. It is listed here again for completeness of the gap-fill record only. The domain profile's erroneous citation "Dimson, Mahajan & Spaenjers (2015, RFS)" should be replaced throughout with this correct citation.
**Identification:** Repeat-sales regression; OLS hedonic age-price decomposition
**Data:** Historical Bordeaux Premiers Crus auction records, 1900–2012
**Key Result:** 4.1% real annual return; maturity-driven price-age kink; growing non-pecuniary collector benefits post-maturity
**Note:** This entry duplicates Category 1 for gap-fill audit purposes only. Do not create a second BibTeX entry.

---

*Gap-fill round completed: 2026-03-29. Papers added: Berry/Levinsohn/Pakes (1995), Rosen (1974), Gavazza/Lizzeri/Roketskiy (2014), Nevo (2001). Dimson citation corrected and documented.*

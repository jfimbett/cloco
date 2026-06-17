# Positioning Guide: Liquid Assets
**Date:** 2026-03-30
**Project:** Liquid Assets (Imbet, Kräussl, Piatti, Steri)
**Compiled by:** Academic Librarian (cloco research system)

---

## Suggested Contribution Statement

(Draft for researcher to adapt)

"This paper documents a novel empirical regularity — a non-monotone price-age profile in French fine-wine auctions, with a ~26% post-maturity trough at ages 32–40 absent in Burgundy Grand Cru — and provides the first structural explanation based on heterogeneous buyer composition. Using 1,068,703 transactions over 1996–2015 and a structural demand model with consumption and collector buyers, we separate the consumption value function from the collector premium and show that the composition of active bidders shifts systematically across the maturity lifecycle. We exploit the 2012 China anti-corruption shock as an exogenous demand shift to identify the collector-specific component, and use cross-sectional variation in entry prices (Grand Cru vs. Premier Cru) to validate the buyer-screening mechanism."

---

## Key Differentiators: What Makes This Paper Distinct from the 5 Most Similar Papers

### vs. Dimson, Rousseau & Spaenjers (2015, JFE) — "The Price of Wine"
- **Overlap:** Both use repeat-sales hedonic methodology on Bordeaux auction data; both note the maturity-driven kink in the price-age profile and growing non-pecuniary benefits post-maturity.
- **Differentiator:** Dimson et al. (2015) treat the non-pecuniary premium as a reduced-form finding and do not model buyer heterogeneity structurally or decompose it econometrically. Liquid Assets is the first to estimate the structural decomposition using a formal two-type model and an exogenous identification strategy. Additionally, the Liquid Assets dataset (1.07 million French domestic transactions) is an order of magnitude larger and covers the China shock period.

### vs. Breeden & Liang (2017, JWE) — "Auction-Price Dynamics for Fine Wines from Age-Period-Cohort Models"
- **Overlap:** Both document the non-monotone cubic price-age profile in wine auctions; both use large transaction datasets.
- **Differentiator:** Breeden & Liang (2017) provide the most rigorous empirical documentation of the age effect but do not provide any structural explanation — the paper's APC framework cannot identify whether the trough and recovery reflect buyer-type composition or something else. Liquid Assets provides the causal mechanism and structural estimates.

### vs. Masset (2024, Economic Modelling) — "Market Segments and Pricing of Fine Wines over Their Lifecycle"
- **Overlap:** Both argue that the non-monotone aggregate price-age profile reflects heterogeneous market segments; both use large wine auction datasets.
- **Differentiator:** Masset (2024) uses an unsupervised finite mixture model that produces segments without economic interpretation or theoretical motivation. The segments cannot be related to buyer types (consumption vs. collector) without additional assumptions. Liquid Assets uses an economically motivated two-type model with explicit utility functions, structural parameters, and causal identification via the China shock and maturity variation.

### vs. Masset, Weisskopf, Faye & Le Fur (2016, Emerging Markets Review) — "Red Obsession"
- **Overlap:** Both study the China demand shock's effect on wine prices.
- **Differentiator:** Masset et al. (2016) use aggregate price indices from 14 iconic wines at multiple auction houses and cannot separate the China shock's effect by wine age or buyer type. Liquid Assets uses transaction-level data and can test whether the shock differentially affected the post-maturity price segment (the key structural prediction). This is the cleanest structural test of the two-type model.

### vs. Lovo & Spaenjers (2018, AER) — "A Model of Trading in the Art Market"
- **Overlap:** Both papers feature heterogeneous agents with private use values trading collectible assets in auctions; both generate selection biases in observed prices and predict that price-age profiles reflect agent composition.
- **Differentiator:** Lovo & Spaenjers (2018) is a theory paper calibrated to qualitative features of the art market without formal structural estimation and without an identification strategy linking model parameters to data. Liquid Assets brings the structural model to wine auction data with a specific identification strategy (maturity threshold variation + China shock) and produces estimated structural parameters.

---

## Potential Target Journals: Ranked List

| Rank | Journal | Rationale |
|---|---|---|
| 1 | **Review of Financial Studies (RFS)** | Recent publications: Lovo & Spaenjers (2018) on art market model (now in AER, but originated in RFS orbit); Korteweg, Kräussl, Verwijmeren (2016) on art returns; Goetzmann, Spaenjers, Van Nieuwerburgh (2021) special issue. Co-editor receptive to private-value assets. Strong overlap with the paper's empirical-plus-structural profile. |
| 2 | **Journal of Finance (JF)** | Published Aubry, Kräussl, Manso, Spaenjers (2023) "Biased Auctioneers" — same co-author (Kräussl), same empirical setting (auction markets for collectibles). JF publishes structural empirical work with clean identification. |
| 3 | **American Economic Review (AER)** | Lovo & Spaenjers (2018) published there; Mandel (2009) published there. The paper's combination of structural model + cleanly identified empirical findings + policy-relevant welfare implications would fit AER's recent receptiveness to finance-economics intersection papers. |
| 4 | **Journal of Financial Economics (JFE)** | Published Dimson, Rousseau & Spaenjers (2015); natural home for papers combining asset pricing, alternative investments, and returns analysis. Lower bar for purely empirical papers; higher bar for structural work unless model is very clean. |
| 5 | **Journal of Political Economy (JPE)** | Appropriate if the structural demand model is the dominant contribution and the wine setting is framed as a laboratory for understanding durable goods with maturity. Published Ginsburgh (1998) on wine auctions. |

**Note for researcher:** The optimal journal depends on the relative weight of the structural model vs. the empirical documentation in the final paper. If the structural model is the dominant contribution and is cleanly estimated, AER or JPE are appropriate. If the empirical documentation and identification are the dominant contributions (with the model providing structure), RFS or JFE are the natural homes.

---

## Literature Gaps This Paper Fills

| Gap | How This Paper Fills It |
|---|---|
| No structural explanation for the non-monotone price-age profile | Two-type structural demand model (consumption vs. collector types) formally explains the trough and recovery |
| No causal identification of the collector premium in wine | China anti-corruption shock provides exogenous variation in collector-type demand; pre/post comparison identifies the collector premium |
| No exploitation of maturity threshold as an identification variable | Variation in maturity dates across wine types (from Tastingbook) is used as the key cross-sectional identification source |
| No test of buyer-screening via entry price | Comparison of Grand Cru (high entry price, muted dip) vs. Premier Cru (lower entry price, pronounced dip) directly tests the screening mechanism |
| No structural demand estimation in wine auction markets | BLP-style or mixture-model structural estimation applied for the first time to wine auction data |
| No French domestic auction market dataset at this scale | 1.07 million transactions from French domestic auctions is a data contribution in itself |

---

## Risks: Papers That Must Be Addressed Head-On

### Proximity-5 Risks: None Identified
No published or circulating paper directly competes with the full combination of this paper's contributions.

### Proximity-4 Papers That Must Be Engaged

**1. Masset (2024, Economic Modelling)**
The editor or referee will almost certainly ask: "How does your two-type model differ from Masset's (2024) five-segment finite mixture model?" The answer must distinguish economically-motivated structural estimation from atheoretical unsupervised segmentation, and must show that the structural model generates testable predictions (buyer composition shifts across maturity) that Masset's model cannot.

**2. Breeden & Liang (2017, JWE)**
The APC benchmark is the standard against which the paper's age effect must be compared. The paper should include a section reconciling its estimates with Breeden & Liang's (2017) results.

**3. Dimson, Rousseau & Spaenjers (2015, JFE)**
Every referee of a wine investment paper will ask for the comparison with Dimson et al. (2015). The paper must show either that its data confirms their main finding (4.1% real return) or that French domestic auction data produces different estimates and explain why.

**4. Lovo & Spaenjers (2018, AER)**
Referees at top journals will compare the paper's theoretical model directly to Lovo & Spaenjers (2018). The paper must clearly articulate what the wine-specific features (biological maturity, consumption value function, maturity threshold) add over the art market model — and why these are not just cosmetic modifications.

**5. Qian & Wen (2015, working paper)**
The China demand shock instrument needs the Qian & Wen (2015) citation and must engage with their estimates of the shock magnitude. Potential referee concern: "Is the shock large enough to identify the collector-type premium, or is it just a market-wide demand shock?" The paper should show the differential impact by wine age (pre-maturity vs. post-maturity) to address this concern directly.

---

## Additional Advisory Notes

**Co-author flag:** Roman Kräussl is co-author of both Liquid Assets and Korteweg, Kräussl & Verwijmeren (2016, RFS) on selection-corrected art returns. This connection should be acknowledged in the paper; the selection-correction methodology from that paper is relevant for any repeat-sales component of the analysis.

**Strand 7 coverage:** The paper's structural model uses auction theory (second-price IPV auctions with two buyer types). The auction theory literature (Vickrey 1961; Milgrom & Weber 1982; Myerson 1981) must be cited. Klemperer (1999) survey provides the background reference.

**Alternative asset benchmarks:** Referees will expect the paper to benchmark wine returns against art, stamps, and financial assets. The Dimson-Spaenjers (2014) "emotional assets" paper provides these cross-asset benchmarks in one place.

---

*Positioning guide completed: 2026-03-30*

# Research Specification: Liquid Assets

**Date:** 2026-03-29
**Researcher:** Juan F. Imbet, Paris Dauphine University - PSL
**Co-authors (alphabetical by last name):**
- Juan F. Imbet, Paris Dauphine University - PSL
- Roman Kräussl, Bayes Business School, City St George's University of London
- Ilaria Piatti, Queen Mary University of London
- Roberto Steri, University of Luxembourg

**Acknowledgments (first-page footnote):** Lucie Bourdychova, Xin Ning. Do NOT acknowledge Duc.

---

## Project Type

`structural` — with substantial reduced-form empirical work alongside the structural model. Estimation vs. calibration of structural parameters TBD pending data availability and model complexity.

---

## Recommended Pipeline

```
/onboard-ra              # First: audit existing data and code (run now)
/lit-review              # Complete the literature review (prior work in old/)
/find-data               # Assess maturity data from Tastingbook + scraping plan
/identify_reducedform    # Design reduced-form empirical strategy
/theory-model            # Develop structural model of heterogeneous buyer types
/data-analysis           # Implement cleaning, reduced-form, structural estimation
/draft-paper             # Write manuscript sections
/review-paper            # Peer review simulation
```

---

## Research Question

What drives the bimodal price-age relationship in fine wine auctions, and how do heterogeneous buyers — consumption-oriented versus collector/investor-oriented — interact to determine prices across the maturity lifecycle of a bottle?

---

## Motivation

Fine wine occupies a unique position among assets: it is simultaneously a consumption good with a biological maturity date and a collectible whose value may *increase* precisely because it can no longer be consumed in the conventional sense. This duality creates a testable prediction about the shape of the price-age profile — prices should first rise as the wine approaches peak drinkability, then fall as consumption value decays past maturity, then rise again as scarcity and prestige compound.

Existing work (Dimson, Mahajan & Spaenjers 2015; Ashenfelter 2008; Goetzmann 1993) treats wine primarily as a financial asset and focuses on returns and diversification benefits. This paper takes a different approach: it uses the maturity lifecycle as a structural feature that separates buyer types, enabling identification of the collector premium and the consumption value independently.

The setting — French wine auctions over approximately a decade — is unusually rich. The data includes variation in wine type, vintage quality, auction house, lot composition, and time period that spans major demand shocks (including the Chinese market entry and the corruption-driven withdrawal circa 2012–2013). This combination of institutional detail and demand-side variation is rare in the alternative assets literature.

---

## Hypothesis

The bimodal price-age profile reflects the superposition of two valuation functions: (1) consumption value, which peaks at maturity and decays to zero thereafter; and (2) collector/scarcity value, which is either flat or increasing in age. The relative weight of these two components in the auction price depends on the composition of active bidders — dominated by consumption buyers near maturity and by collectors far from it. Exogenous shifts in collector demand (e.g., the China shock) should disproportionately affect prices in the post-maturity segment of the age distribution.

---

## Theoretical Model

- **Model type:** Heterogeneous-agent auction model with private valuations; potentially dynamic (forward-looking collector buyers who anticipate resale)
- **Key agents/players:**
  - *Consumption buyers*: Value wine for drinking; valuation peaks at maturity, collapses thereafter; understand (or approximately know) the maturity date
  - *Collector/investor buyers*: Value wine for holding and resale; valuation is driven by scarcity, prestige, and expected resale to future collectors; maturity-agnostic or maturity-positive (very old bottles are more prestigious)
  - *Status/unsophisticated buyers* (possible third type): Buy wine as a luxury status signal; do not adjust for maturity; potentially important in the China demand story
- **Core mechanism:** In a standard auction, the price is determined by the second-highest valuation. As age passes maturity, consumption buyers drop out; price is set by collector valuations. The post-maturity price increase reflects growing scarcity (surviving bottles fewer over time) and/or a collector prestige premium that compounds with age.
- **Main predictions:**
  1. Price-age profile is non-monotone (inverted-U for consumption component, weakly increasing for collector component)
  2. The price trough occurs near the estimated maturity date
  3. Post-maturity prices are more sensitive to collector demand shocks (China) than pre-maturity prices
  4. Wines with clearer, more universally-known maturity windows (e.g., grand cru Bordeaux) should have sharper price troughs than wines with diffuse maturity windows
- **Structural parameters (if estimated):** Share of buyer types in the bidder population, consumption value function parameters (peak age, decay rate), collector premium parameters (scarcity elasticity, prestige premium), maturity date $\tau_i$ per wine type

---

## Empirical Strategy

- **Method:** Two-part strategy
  1. *Reduced-form*: Hedonic price regressions establishing the bimodal age-price profile; event study around the China demand shock; cross-sectional comparisons across wine types with sharp vs. diffuse maturity
  2. *Structural*: Demand estimation separating buyer types — either BLP-style discrete choice or a mixture-model approach matching moments from the price-age distribution
- **Treatment:** Wine age relative to estimated maturity date ($a_i - \hat{\tau}_i$)
- **Control:** Wines of the same château/appellation in different age ranges; same-vintage bottles auctioned at different points in time
- **Key identifying assumption for reduced-form:** Conditional on château × vintage fixed effects and lot characteristics, the maturity threshold is the only non-linear shifter of log price
- **Key identifying assumption for structural:** Tastingbook-derived maturity estimates are informative about true biological maturity and uncorrelated with unobserved auction-level demand shocks
- **Robustness checks:**
  - Restricting to wines where Tastingbook has high-confidence maturity dates
  - Allowing for measurement error in maturity estimates (bounds approach or IV)
  - Placebo maturity dates (falsification test)
  - Separating auction houses with different buyer composition (if data permits)
  - China shock event study: pre-trend test, placebo years

---

## Data

- **Primary dataset:** French wine auction records; lot-level transactions; ~10 years ending ~2020; variables include hammer price, vintage year, château/appellation, wine type, lot size (bottles vs. cases), auction house, approximate buyer geography
- **Key variables:** Log hammer price, wine age at auction, maturity estimate ($\hat{\tau}_i$ from Tastingbook or estimated model), wine type (grand cru, premier cru, appellation), vintage quality score, lot size
- **Sample:** Auction lot as unit of observation; time period TBD pending data audit; N TBD
- **Maturity data:** Tastingbook (scraped); econometric maturity model for wines not covered — likely a hedonic regression of Tastingbook maturity on wine characteristics, used to predict maturity out-of-sample
- **Data quality note:** Multiple RAs contributed to data cleaning. Duc's contributions require independent verification. Lucie Bourdychova's and Xin Ning's work is considered reliable.

---

## Expected Results

The team is deliberately agnostic about magnitudes and is committed to letting the data speak first. The prior is that the bimodal price-age pattern exists in the data and is driven by the mechanism described above — but the relative importance of scarcity, prestige, and unsophisticated buyers in the post-maturity price recovery is an empirical question. The China shock analysis will be used to test whether the post-maturity segment responds differentially, which is the cleanest structural test of the two-type model.

---

## Contribution

This paper makes two contributions: first, it documents a novel empirical regularity in wine auction markets — the bimodal price-age profile — and provides causal evidence for the mechanism using demand shocks. Second, it develops and estimates a structural model of heterogeneous buyers that quantifies the consumption vs. collector components of wine valuation. More broadly, the model applies to any durable good with a biological or technological maturity date where both consumption and collectible demand coexist (whisky, vintage cars, art with physical decay).

---

## Open Questions

1. **Estimation vs. calibration:** The structural model may be calibrated to moments rather than formally estimated, depending on data richness and computational feasibility. Decision pending data audit and model development by co-authors.
2. **Third buyer type:** Whether to include a formal "status/unsophisticated buyer" type or treat this as a special case of collector buyers needs to be resolved in model development.
3. **Maturity model:** The econometric model for estimating maturity for Tastingbook-missing wines needs to be specified — functional form, covariates, validation strategy.
4. **China demand shock:** Need to confirm the auction data spans 2010–2015 and has sufficient observations to run the event study. Buyer geography variable quality TBD.
5. **Literature review:** Prior literature review is in `old/` folder. Needs to be recovered, assessed, and completed. Run `/lit-review` after `/onboard-ra`.
6. **Co-author model:** Co-authors are independently developing the theoretical model. Coordination needed before structural estimation begins to ensure the model estimated here matches their framework.

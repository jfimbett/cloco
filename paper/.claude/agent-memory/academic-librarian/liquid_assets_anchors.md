---
name: Liquid Assets — Literature Anchors
description: Key papers, citation errors found, and scooping risks for the wine auction / heterogeneous buyers paper
type: project
---

## CRITICAL CITATION CORRECTION (VERIFIED 2026-03-29)
The project domain profile lists "Dimson, Mahajan & Spaenjers (2015, RFS)" — this is WRONG on every element:
- The second author is **Peter L. Rousseau** (not Mahajan) — VERIFIED via RePeC
- The journal is **Journal of Financial Economics (JFE)** (not RFS) — VERIFIED via RePeC
- The title is **"The Price of Wine"** — VERIFIED via RePeC (ideas.repec.org/a/eee/jfinec/v118y2015i2p431-449.html)
Correct: Dimson, Rousseau & Spaenjers (2015), "The Price of Wine," JFE 118(2):431–449.
"Eye of the Beholder" is NOT a Dimson wine paper. It cannot be found in the wine or art literature
as a Dimson/Mahajan/Spaenjers paper. The title "Eye of the Beholder" is associated with a different
art-and-beauty paper (Adams & Kräussl), not Dimson. The domain profile entry was entirely fabricated.

## GAP-FILL ROUND PAPERS ADDED (2026-03-29)
- Berry/Levinsohn/Pakes (1995) Econometrica 63(4):841-890 — BLP demand estimation — Proximity 3
  VERIFIED: confirmed via NBER WP #4264 which states exact journal citation
- Rosen (1974) JPE 82(1):34-55 — hedonic pricing — Proximity 4
  VERIFIED: confirmed via RePeC (ideas.repec.org/a/ucp/jpolec/v82y1974i1p34-55.html)
- Gavazza/Lizzeri/Roketskiy (2014) AER 104(11):3596-3634 — durable goods, heterogeneous buyers — Proximity 2
  PAGES UNVERIFIED: volume/issue known but pages marked % UNVERIFIED in bib
- Nevo (2001) Econometrica 69(2):307-342 — BLP implementation — Proximity 3
  PAGES UNVERIFIED: DOI 10.1111/1468-0262.00194 known; pages marked % UNVERIFIED in bib

## Anchor Papers by Strand

### Strand 1 — Wine Auction Prices / Maturity
- Dimson/Rousseau/Spaenjers 2015 JFE — long-run repeat-sales; identifies maturity kink and collector premium conceptually
- Breeden/Liang 2017 JWE — APC decomposition of 1.5M auction records; cubic age-price profile documented
- Masset 2024 Economic Modelling — five market segments via finite mixture model; lifecycle pricing confirmed
- Masset/Weisskopf/Faye/Le Fur 2016 Emerging Markets Review — China shock → 19% HK premium; declined 60% to 15% post-2012
- Cardebat/Faye/Le Fur/Storchmann 2017 JWE vol 12 — price dispersion > transaction costs; heterogeneous buyers as explanation

### Strand 2 — Alternative Assets
- Korteweg/Kräussl/Verwijmeren 2016 RFS — selection-corrected art returns; NOTE: Kräussl is co-author of Liquid Assets
- Renneboog/Spaenjers 2013 Management Science — 1M+ art transactions; wealth-driven collector demand
- Goetzmann/Renneboog/Spaenjers 2011 AER — art + money; top incomes drive collectible prices
- Dimson/Spaenjers 2011 JFE — stamps; 7% nominal, 2.9% real
- Goetzmann/Spaenjers/Van Nieuwerburgh 2021 RFS — "real and private-value assets" framework; $84T asset class

### Strand 3 — Auction Theory
- Milgrom/Weber 1982 Econometrica — affiliated values; revenue ranking of auction formats
- Vickrey 1961 Journal of Finance — second-price auction; dominant-strategy truth-telling
- Myerson 1981 Mathematics of Operations Research — optimal auction; virtual valuations
- Klemperer 1999 Journal of Economic Surveys — survey of auction theory
- Ginsburgh 1998 JPE — declining price anomaly in wine auctions; absentee bidders

### Strand 4 — Commodity Storage / Durable Goods
- Deaton/Laroque 1996 JPE — competitive storage model; stockout asymmetry
- Casassus/Collin-Dufresne 2005 JF — stochastic convenience yield (analog to consumption value)
- Schwartz 1997 JF — three-factor commodity model; convenience yield
- Pindyck 1994 RAND JE — inventory-price model; marginal value of storage

### Strand 5 — China Demand Shock
- Qian/Wen 2015 working paper — Xi anti-corruption → 55% luxury import decline; key instrument
- Bian/Zhang/Zhou 2025 Pacific-Basin Finance Journal — Chinese art prices drop 5.5% per official prosecuted

## Scooping Risk
NO proximity-5 competitor identified as of 2026-03-29.
Closest risks (proximity 4):
- Masset 2024 (segments but no structural buyer-type model, no China shock)
- Qian/Wen 2015 (China shock but not wine-auction specific, unpublished)
- Masset et al. 2016 (China shock + Hong Kong but not age-maturity profile)

## Most-Used Datasets in Wine Economics
- Chicago Wine Company auction prices (used by Masset/Henderson 2010)
- Liv-ex index (time-series benchmark; referenced in most return papers)
- French wine auction records (project-specific proprietary dataset)
- Tastingbook (maturity ratings; scraped; sparse for post-maturity wines)

## Common Identification Strategies
- Repeat-sales regression (Goetzmann 1993, Burton/Jacobsen 2001, Dimson/Rousseau/Spaenjers 2015)
- Hedonic log-price regression with vintage FE and château FE (standard)
- Age-Period-Cohort decomposition (Breeden/Liang 2017)
- DiD with China shock as treatment (Qian/Wen 2015, Masset et al. 2016)
- Finite mixture model for segment identification (Masset 2024)
- Selection-corrected repeat-sales (Korteweg/Kräussl/Verwijmeren 2016)

**Why:** These patterns appear consistently across the wine economics and art market literatures and will be expected by referees.
**How to apply:** Cite the relevant anchor for any method used; use standard hedonic controls (vintage FE, château FE, lot size).

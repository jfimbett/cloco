# Literature Review: Liquid Assets
**Date:** 2026-03-30
**Query:** Wine as investment, heterogeneous buyer models, durable goods pricing, collectibles markets — comprehensive coverage
**Editor score:** 82/100 (PASS after gap-fill)
**Papers found:** 58 new (13 already in bibliography)

---

## Summary

The literature on fine wine as an investment asset is well-developed empirically but structurally thin. Three facts are established without dispute: (1) investment-grade wine delivers nominal returns of 5–9% p.a. with low equity beta and diversification benefits (Dimson, Rousseau & Spaenjers 2015; Sanning et al. 2008; Burton & Jacobsen 2001); (2) the aggregate price-age profile is non-monotone — prices rise pre-maturity, plateau, and recover at antique ages (Breeden & Liang 2017); (3) this non-linearity in aggregate prices reflects underlying market-segment heterogeneity (Masset 2024). What does not exist is a structural explanation for *why* the trough occurs, who causes it, and why some wine types (Burgundy Grand Cru) escape it. **Liquid Assets fills this gap.**

The closest structural antecedent is Lovo & Spaenjers (2018, AER), a two-type heterogeneous buyer model for the art market. Mandel (2009, AER) provides earlier theoretical motivation for collectibles as both investment and conspicuous consumption goods. Neither paper brings the structural model to data with a formal identification strategy. The China demand shock literature (Qian & Wen 2015; Masset et al. 2016; Dang, Liu & Yan 2025) establishes a plausibly exogenous variation in collector-type demand that Liquid Assets can exploit.

The durable goods analogy (Gavazza et al. 2014; Hendel & Nevo 2006) grounds the consumption buyer's intertemporal holding decision. The auction theory literature (Milgrom & Weber 1982; Athey & Haile 2002) provides identification justification for recovering valuations from hammer prices in ascending auctions.

---

## Key Papers

### Masset (2024) — Market Segments and Pricing of Fine Wines over Their Lifecycle
- **Journal:** Economic Modelling, Vol. 141, Article 106915
- **Proximity:** 5/5 — most direct empirical antecedent
- **Main contribution:** Finite mixture model on 20 years of auction data identifies five market segments (investment, collectible, drinking wines); shows the non-monotone aggregate age profile is the superposition of linear within-segment effects.
- **Method:** Finite mixture model; hedonic regression within segments
- **Key finding:** Non-linearity in aggregate price-age profile fully explained by segment composition shifts
- **Relevance:** Corroborates the buyer-heterogeneity mechanism but lacks a structural model or exogenous identification. Liquid Assets provides both.
- **BibTeX key:** `masset2024`

### Breeden & Liang (2017) — Auction-Price Dynamics for Fine Wines from APC Models
- **Journal:** Journal of Wine Economics, 12(2):173–202 *(already in bibliography)*
- **Proximity:** 5/5
- **Key finding:** Non-monotone cubic age-price profile with trough and antique recovery; Hill of Grace: +14.8% return at year 2, near 0% at year 20, +10.4% at year 30
- **Relevance:** Best empirical documentation of the pattern this paper explains structurally.

### Dang, Liu & Yan (2025) — Signals of Clean Governance: Luxury Wine Imports in China
- **Journal:** Economics Letters, 255:112523 — **MUST CITE (published 2025)**
- **Proximity:** 4/5
- **Main contribution:** Published peer-reviewed paper estimating ~47% decline in luxury wine imports following the Xi Jinping anti-corruption campaign (2012–2013); documents the bribe-gift mechanism.
- **Method:** Difference-in-differences on Chinese customs data
- **Key finding:** 47.4% decline in luxury wine imports; effect concentrated in bribe-prone goods
- **Relevance:** Published version of the wine-specific demand shock for the identification strategy. Replaces or supplements Qian & Wen (2015) working paper.
- **BibTeX key:** `dangliu2025`

### Masset, Weisskopf, Faye & Le Fur (2016) — Red Obsession
- **Journal:** Emerging Markets Review, 29:200–225
- **Proximity:** 4/5
- **Key finding:** 19% average Hong Kong auction premium for 14 iconic Bordeaux wines; peak 60% in 2008, declining to 15% post-2012 anti-corruption campaign
- **Relevance:** Direct treatment of China demand shock at wine auction level; provides event-study benchmarks.
- **BibTeX key:** `massetweisskopf2016`

### Cardebat & Jiao (2018) — Long-Term Financial Drivers of Fine Wine Prices
- **Journal:** Quarterly Review of Economics and Finance, 67:347–361
- **Proximity:** 4/5
- **Key finding:** Cointegration between Chinese equity markets and Bordeaux premier cru prices; emerging buyers are Veblen-sensitive
- **Relevance:** Financial-market evidence for the China collector demand channel.
- **BibTeX key:** `cardebatjiao2018`

### Cardebat, Faye, Le Fur & Storchmann (2017) — The Law of One Price?
- **Journal:** Journal of Wine Economics, 12(3):302–331
- **Proximity:** 4/5
- **Key finding:** Law of one price rejected in fine wine; heterogeneous buyer preferences (not just transaction costs) explain price dispersion across auction houses and geographies
- **Relevance:** Direct motivation for the two-type buyer model — different buyers coexist with systematically different valuations.
- **BibTeX key:** `cardebatfaye2017`

### Dimson & Spaenjers (2014) — Investing in Emotional Assets
- **Journal:** Financial Analysts Journal, 70(2):20–25
- **Proximity:** 4/5
- **Key finding:** Collectibles real return 2.4–2.8% p.a.; coins "emotional dividend" concept (non-pecuniary ownership benefit)
- **Relevance:** Establishes "emotional dividend" — the concept closest to the collector premium in the structural model.
- **BibTeX key:** `dimsonspaenjers2014`

### Lovo & Spaenjers (2018) — A Model of Trading in the Art Market
- **Journal:** American Economic Review, 108(3):744–774 *(already in bibliography)*
- **Proximity:** 4/5
- **Relevance:** Canonical structural antecedent — two-type heterogeneous buyer model for collectibles. Liquid Assets is the empirical companion with estimated structural parameters and a formal identification strategy.

### Mandel (2009) — Art as Investment and Conspicuous Consumption Good
- **Journal:** American Economic Review, 99(4):1653–1663
- **Proximity:** 3–4/5
- **Key finding:** Equilibrium art price reflects both investment and conspicuous consumption dividends; predicts low financial returns as equilibrium
- **Relevance:** Theoretical antecedent to the two-type model; frames collector value as a non-pecuniary dividend distinct from financial return.
- **BibTeX key:** `mandel2009`

### Ginsburgh (1998) — Absentee Bidders and the Declining Price Anomaly in Wine Auctions
- **Journal:** Journal of Political Economy, 106(6):1302–1331
- **Proximity:** 3/5
- **Key finding:** French wine auctions (absentee bidding, sequential lots) generate declining price anomalies; heterogeneous bidder strategies documented
- **Relevance:** Documents French auction institutional features relevant to the paper's setting; supports heterogeneous bidder interpretation.
- **BibTeX key:** `ginsburgh1998`

### Bagwell & Bernheim (1996) — Veblen Effects in a Theory of Conspicuous Consumption
- **Journal:** American Economic Review, 86(3):349–373
- **Proximity:** 3/5
- **Relevance:** Foundational theory for why collector-type buyers pay above marginal cost; theoretical grounding for the collector valuation component.
- **BibTeX key:** `bagwellbernheim1996`

### Hadj Ali, Lecocq & Visser (2008) — The Impact of Gurus: Parker Grades
- **Journal:** Economic Journal, 118(529):F158–F173
- **Proximity:** 3/5
- **Method:** Natural experiment (2003 Parker non-rating event)
- **Relevance:** Cleanest causal identification in wine pricing literature; provides methodological benchmark.
- **BibTeX key:** `hadjali2008`

### Combris, Lecocq & Visser (1997) — Hedonic Price Equation for Bordeaux Wine
- **Journal:** Economic Journal, 107(441):390–402
- **Proximity:** 3/5
- **Relevance:** Foundational Bordeaux hedonic regression; standard referees will expect this cited.
- **BibTeX key:** `combrislv1997`

### Aubry, Kräussl, Manso & Spaenjers (2023) — Biased Auctioneers
- **Journal:** Journal of Finance, 78(2):795–833
- **Proximity:** 3/5 — co-author paper (Kräussl)
- **Relevance:** Same empirical setting (auction markets for collectibles); demonstrates JF receptiveness to this research program.
- **BibTeX key:** `aubry2023`

### Pénasse & Renneboog (2022) — Speculative Trading and Bubbles: Art Market
- **Journal:** Management Science, 68(7):4939–4963
- **Proximity:** 3/5
- **BibTeX key:** `penasse2022`

### Scheinkman & Xiong (2003) — Overconfidence and Speculative Bubbles
- **Journal:** Journal of Political Economy, 111(6):1183–1219
- **Proximity:** 2–3/5
- **Relevance:** Alternative theoretical mechanism for collector premium (speculative resale option); paper should discuss and distinguish.
- **BibTeX key:** `scheinkmanxiong2003`

### Hendel & Nevo (2006) — Sales and Consumer Inventory Behavior
- **Journal:** Econometrica, 74(6):1637–1673
- **Proximity:** 2/5
- **Relevance:** Canonical storable goods model; grounds the consumption buyer's pre-maturity holding decision.
- **BibTeX key:** `hendelnevo2006`

### Athey & Haile (2002) — Identification of Standard Auction Models
- **Journal:** Econometrica, 70(6):2107–2140
- **Proximity:** 2/5
- **Relevance:** Ascending auction IPV models identified from transaction prices alone — justifies demand-side identification without losing-bid data.
- **BibTeX key:** `atheyhaileid2002`

### Guerre, Perrigne & Vuong (2000) — Nonparametric Estimation of First-Price Auctions
- **Journal:** Econometrica, 68(3):525–574
- **Proximity:** 2/5
- **Relevance:** Canonical background for structural auction estimation.
- **BibTeX key:** `guerre2000`

---

## Thematic Organization

### Theoretical Contributions
- Lovo & Spaenjers (2018) — two-type collectibles market model *(canonical antecedent)*
- Mandel (2009) — art as investment + conspicuous consumption
- Bagwell & Bernheim (1996) — Veblen effect theory
- Scheinkman & Xiong (2003) — speculative resale premium
- Tirole (1982) — theoretical bounds on speculation

### Empirical: Wine Prices and Investment
- Dimson, Rousseau & Spaenjers (2015) — wine returns, long-run
- Breeden & Liang (2017) — non-monotone age profile (APC)
- Masset (2024) — market segments explain aggregate non-linearity
- Masset et al. (2016) — China demand shock at HK auctions
- Dang, Liu & Yan (2025) — wine import collapse from anti-corruption
- Cardebat & Jiao (2018) — China as long-run Bordeaux driver
- Cardebat et al. (2017) — law of one price rejected; heterogeneous buyers
- Ginsburgh (1998) — French auction institutional features
- Combris et al. (1997/2000) — Bordeaux/Burgundy hedonic benchmarks
- Hadj Ali et al. (2008) — Parker effect causal identification

### Empirical: Art & Collectibles Analogues
- Goetzmann (1993), Mei & Moses (2002), Korteweg et al. (2016) — returns and selection
- Renneboog & Spaenjers (2013), Pénasse & Renneboog (2022) — art price dynamics
- Aubry, Kräussl, Manso & Spaenjers (2023) — biased auctioneers (co-author)
- Dimson & Spaenjers (2014) — emotional dividend across collectibles

### Methods and Structural Estimation
- Rosen (1974) — hedonic prices
- Goetzmann (1993) — repeat-sales index
- Berry, Levinsohn & Pakes (1995); Nevo (2001) — BLP demand estimation
- Athey & Haile (2002) — ascending auction identification
- Guerre, Perrigne & Vuong (2000) — structural auction estimation
- Hendel & Nevo (2006) — storable goods demand
- Gavazza, Lizzeri & Roketskiy (2014) — used-car secondary market

---

## Gaps and Opportunities

1. **No published paper structurally estimates buyer-type shares from wine auction data** — primary contribution of Liquid Assets.
2. **Maturity threshold as identification variable is novel** — no prior paper uses wine maturity windows as a structural feature.
3. **French domestic auction market dataset is unprecedented** — all major work uses London, Chicago, or multi-house global samples.
4. **Burgundy vs. Bordeaux structural comparison** — the buyer-screening prediction (Grand Cru escapes trough) is untested structurally.
5. **Antique premium unexplained** — documented by Breeden & Liang (2017) but not identified as collector-type dominance.

---

## Research Frontier

### Active Debates
- Whether wine/art returns are positive or zero after selection correction (Korteweg et al. 2016 vs. earlier work)
- Whether the China demand shock permanently altered buyer composition
- Speculative demand (Scheinkman & Xiong 2003) vs. collector use value (Lovo & Spaenjers 2018) as the mechanism

### Recent Working Papers
- **Verdickt (2025, SSRN #5386662)** — "Climate Extrapolation and Relative Asset Pricing: Evidence from Bordeaux Premier Cru Wine Auctions" — overlapping data, different question (investor climate attention biases). Not a scooping risk; cite as contemporaneous.

---

## BibTeX Entries to Add to `paper/references.bib`

> `references.bib` is protected from automatic edits. Paste these entries manually.

```bibtex
@article{masset2024,
  author  = {Masset, Philippe},
  title   = {Market Segments and Pricing of Fine Wines over Their Lifecycle},
  journal = {Economic Modelling},
  year    = {2024},
  volume  = {141},
  pages   = {106915},
  doi     = {10.1016/j.econmod.2024.106915}
}

@article{dangliu2025,
  author  = {Dang, Jingqi and Liu, Cong and Yan, Ru},
  title   = {Signals of Clean Governance: {E}vidence from Luxury Wine Imports in {C}hina},
  journal = {Economics Letters},
  year    = {2025},
  volume  = {255},
  pages   = {112523},
  doi     = {10.1016/j.econlet.2025.112523}
}

@article{massetweisskopf2016,
  author  = {Masset, Philippe and Weisskopf, Jean-Philippe and Faye, Beno\^{i}t and Le Fur, Eric},
  title   = {Red Obsession: The Ascent of Fine Wine in {C}hina},
  journal = {Emerging Markets Review},
  year    = {2016},
  volume  = {29},
  pages   = {200--225},
  doi     = {10.1016/j.ememar.2016.08.014}
}

@article{cardebatjiao2018,
  author  = {Cardebat, Jean-Marie and Jiao, Linda},
  title   = {The Long-Term Financial Drivers of Fine Wine Prices: The Role of Emerging Markets},
  journal = {Quarterly Review of Economics and Finance},
  year    = {2018},
  volume  = {67},
  pages   = {347--361},
  doi     = {10.1016/j.qref.2017.07.016}
}

@article{cardebatfaye2017,
  author  = {Cardebat, Jean-Marie and Faye, Beno\^{i}t and Le Fur, Eric and Storchmann, Karl},
  title   = {The Law of One Price? {P}rice Dispersion on the Auction Market for Fine Wine},
  journal = {Journal of Wine Economics},
  year    = {2017},
  volume  = {12},
  number  = {3},
  pages   = {302--331},
  doi     = {10.1017/jwe.2017.40}
}

@article{dimsonspaenjers2014,
  author  = {Dimson, Elroy and Spaenjers, Christophe},
  title   = {Investing in Emotional Assets},
  journal = {Financial Analysts Journal},
  year    = {2014},
  volume  = {70},
  number  = {2},
  pages   = {20--25},
  doi     = {10.2469/faj.v70.n2.8}
}

@article{mandel2009,
  author  = {Mandel, Benjamin R.},
  title   = {Art as an Investment and Conspicuous Consumption Good},
  journal = {American Economic Review},
  year    = {2009},
  volume  = {99},
  number  = {4},
  pages   = {1653--1663},
  doi     = {10.1257/aer.99.4.1653}
}

@article{bagwellbernheim1996,
  author  = {Bagwell, Laurie Simon and Bernheim, B. Douglas},
  title   = {Veblen Effects in a Theory of Conspicuous Consumption},
  journal = {American Economic Review},
  year    = {1996},
  volume  = {86},
  number  = {3},
  pages   = {349--373}
}

@article{scheinkmanxiong2003,
  author  = {Scheinkman, Jos{\'e} A. and Xiong, Wei},
  title   = {Overconfidence and Speculative Bubbles},
  journal = {Journal of Political Economy},
  year    = {2003},
  volume  = {111},
  number  = {6},
  pages   = {1183--1219},
  doi     = {10.1086/378531}
}

@article{ginsburgh1998,
  author  = {Ginsburgh, Victor},
  title   = {Absentee Bidders and the Declining Price Anomaly in Wine Auctions},
  journal = {Journal of Political Economy},
  year    = {1998},
  volume  = {106},
  number  = {6},
  pages   = {1302--1331},
  doi     = {10.1086/250048}
}

@article{combrislv1997,
  author  = {Combris, Pierre and Lecocq, S{\'e}bastien and Visser, Michael},
  title   = {Estimation of a Hedonic Price Equation for {B}ordeaux Wine: Does Quality Matter?},
  journal = {Economic Journal},
  year    = {1997},
  volume  = {107},
  number  = {441},
  pages   = {390--402},
  doi     = {10.1111/j.0013-0133.1997.165.x}
}

@article{hadjali2008,
  author  = {Hadj Ali, H{\'e}la and Lecocq, S{\'e}bastien and Visser, Michael},
  title   = {The Impact of Gurus: {P}arker Grades and {E}n {P}rimeur Wine Prices},
  journal = {Economic Journal},
  year    = {2008},
  volume  = {118},
  number  = {529},
  pages   = {F158--F173},
  doi     = {10.1111/j.1468-0297.2008.02147.x}
}

@article{aubry2023,
  author  = {Aubry, Mathieu and Kr{\"a}ussl, Roman and Manso, Gustavo and Spaenjers, Christophe},
  title   = {Biased Auctioneers},
  journal = {Journal of Finance},
  year    = {2023},
  volume  = {78},
  number  = {2},
  pages   = {795--833},
  doi     = {10.1111/jofi.13203}
}

@article{penasse2022,
  author  = {P{\'e}nasse, Julien and Renneboog, Luc},
  title   = {Speculative Trading and Bubbles: Evidence from the Art Market},
  journal = {Management Science},
  year    = {2022},
  volume  = {68},
  number  = {7},
  pages   = {4939--4963},
  doi     = {10.1287/mnsc.2021.4088}
}

@article{atheyhaileid2002,
  author  = {Athey, Susan and Haile, Philip A.},
  title   = {Identification of Standard Auction Models},
  journal = {Econometrica},
  year    = {2002},
  volume  = {70},
  number  = {6},
  pages   = {2107--2140},
  doi     = {10.1111/j.1468-0262.2002.00435.x}
}

@article{hendelnevo2006,
  author  = {Hendel, Igal and Nevo, Aviv},
  title   = {Measuring the Implications of Sales and Consumer Inventory Behavior},
  journal = {Econometrica},
  year    = {2006},
  volume  = {74},
  number  = {6},
  pages   = {1637--1673},
  doi     = {10.1111/j.1468-0262.2006.00721.x}
}

@article{guerre2000,
  author  = {Guerre, Emmanuel and Perrigne, Isabelle and Vuong, Quang},
  title   = {Optimal Nonparametric Estimation of First-Price Auctions},
  journal = {Econometrica},
  year    = {2000},
  volume  = {68},
  number  = {3},
  pages   = {525--574},
  doi     = {10.1111/1468-0262.00123}
}

@article{nitschka2022,
  author  = {Nitschka, Thomas},
  title   = {China's Anti-Corruption Campaign and Stock Returns of Luxury Goods Firms},
  journal = {Financial Markets and Portfolio Management},
  year    = {2022},
  volume  = {36},
  number  = {2},
  pages   = {159--177},
  doi     = {10.1007/s11408-021-00396-2}
}

@unpublished{qianwen2015,
  author = {Qian, Nancy and Wen, Jaya},
  title  = {The Impact of {X}i {J}inping's Anti-Corruption Campaign on Luxury Imports in {C}hina},
  note   = {Working Paper, Yale University, April 2015},
  year   = {2015}
}
```

---

## Supporting Files

| File | Contents |
|------|----------|
| `quality_reports/literature/liquid-assets/annotated_bibliography.md` | Full annotated bibliography, 58 papers, 8 strands |
| `quality_reports/literature/liquid-assets/references.bib` | BibTeX for all 58 papers |
| `quality_reports/literature/liquid-assets/frontier_map.md` | What is established, methodological frontier, data gaps, open questions |
| `quality_reports/literature/liquid-assets/positioning.md` | Contribution statement, differentiators, journal ranking, gap-to-paper mapping |
| `quality_reports/lit_review_editor_review.md` | Editor critique: score 82/100, gap analysis |

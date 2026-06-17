# Editor Review -- Literature Review: Liquid Assets
**Date:** 2026-03-30
**Mode:** Lit Critic (Phase 1) -- Re-review after librarian revision
**Score:** 82/100
**Decision:** Pass

## Executive Summary

The revised literature collection represents a substantial improvement over the prior submission (62/100). The librarian has addressed the critical BibTeX errors (Dimson citation corrected), added structural demand estimation methods (BLP, Nevo), included Rosen (1974) in the project bibliography, expanded the annotated bibliography to 45 new papers plus 13 anchors, and produced a well-structured frontier map. The collection now passes the 80-point threshold, but residual gaps in structural auction estimation methods and the durable goods aging strand prevent a higher score.

## Issues Found

### 1. Missing Guerre, Perrigne & Vuong (2000, Econometrica) -- Severity: Medium -- Deduction: -5

The frontier map explicitly names "Guerre, Perrigne & Vuong 2000 in QJE" as being on the structural estimation frontier, and the Asker (2010) entry describes its model as "in the spirit of Guerre/Perrigne/Vuong." Yet GPV (2000) does not appear as a standalone annotated entry in the bibliography, nor does it have a BibTeX entry in the librarian's `references.bib`. For a paper that proposes structural estimation of auction demand with heterogeneous buyer types, the foundational nonparametric identification paper for private-value auctions is not optional. The correct citation is: Guerre, Perrigne & Vuong (2000), "Optimal Nonparametric Estimation of First-Price Auctions," *Econometrica*, 68(3), 525-574. Note also that the frontier map incorrectly attributes GPV to QJE rather than Econometrica.

**Why it matters:** A JFE referee evaluating a structural auction model will check whether the authors cite GPV. Its absence signals unfamiliarity with the structural auctions literature.

### 2. Missing Hendel & Nevo (2006, Econometrica) on storable goods -- Severity: Medium -- Deduction: -5

The prior review specifically flagged Hendel & Nevo (2006), "Measuring the Implications of Sales and Consumer Inventory Behavior," *Econometrica*, as directly relevant to the storable goods with forward-looking consumers strand. The revised bibliography still does not include it. Wine is a storable good with intertemporal substitution. Consumers decide when to drink (consume) or continue holding (store). The Hendel & Nevo framework of forward-looking inventory management maps directly onto the consumption buyer's optimization problem in the structural model. The durable goods strand currently has only 3 papers (Deaton & Laroque, Casassus & Collin-Dufresne, Pindyck), all on commodity storage rather than consumer durables with heterogeneous agents.

**Why it matters:** The paper's structural model features a consumption buyer who times consumption based on maturity. Hendel & Nevo is the canonical reference for this type of consumer behavior.

### 3. Qian & Wen (2015) remains unpublished after 11 years -- Severity: Low-Medium -- Deduction: -3

This was flagged in the prior review. Qian & Wen (2015) is still listed as "Working Paper, Yale University (preliminary draft April 2015; unpublished as of 2026)." The paper has not been published in 11 years. The bibliography does not identify a published alternative documenting the China anti-corruption campaign's quantitative effect on luxury imports. While the shock itself is well-documented in published work (Bian et al. 2025 for art; Masset et al. 2016 for wine premiums), the specific magnitude claim ("~55% reduction in luxury imports, ~47% for wine") rests on an unpublished source. The librarian should either: (a) verify whether this paper has since been published under a different title, (b) identify a published alternative for the magnitude estimate, or (c) explicitly note this risk in a "caveats" section. This is a low-medium issue because the identification strategy does not depend solely on Qian & Wen -- Masset et al. (2016) provides published evidence of the demand shock at the auction level.

### 4. Frontier map misattributes GPV journal -- Severity: Low -- Deduction: -2

Line 44 of the frontier map states "Guerre, Perrigne & Vuong 2000 in QJE." GPV (2000) was published in *Econometrica*, not the *Quarterly Journal of Economics*. This is an incorrect journal attribution in a methods-critical paper. While minor in isolation, factual errors in a literature review undermine credibility.

### 5. No Paarsch & Hong (2006) textbook reference -- Severity: Low -- Deduction: -2

The frontier map names "Paarsch & Hong 2006" as part of the structural auction estimation frontier but does not include it in the annotated bibliography or BibTeX. This is the standard textbook (*An Introduction to the Structural Econometrics of Auction Data*, MIT Press) for anyone estimating structural auction models. For a paper that positions itself as bringing structural estimation to wine auctions, the reference textbook should appear in the bibliography.

### 6. Ginsburgh (1998) proximity score underrates importance -- Severity: Low -- Deduction: -1

Ginsburgh (1998, JPE) is assigned proximity 3/5. This is the only paper in the entire bibliography that studies heterogeneous bidder behavior in wine auctions using a structural model. Given the Liquid Assets paper proposes exactly this -- a structural model of heterogeneous buyers in wine auctions -- Ginsburgh (1998) should be proximity 4/5. The prior review flagged this; it has not been adjusted.

## Score Breakdown

- Starting: 100
- Missing GPV (2000, Econometrica) -- structural auction foundation: -5
- Missing Hendel & Nevo (2006, Econometrica) -- storable goods with forward-looking consumers: -5
- Qian & Wen (2015) unpublished status unresolved: -3
- Frontier map GPV journal misattribution: -2
- Missing Paarsch & Hong (2006) textbook: -2
- Ginsburgh proximity score underrated: -1
- **Final: 82/100**

## Required Actions

1. **Add GPV (2000) to the annotated bibliography and BibTeX.** Guerre, E., Perrigne, I., & Vuong, Q. (2000). "Optimal Nonparametric Estimation of First-Price Auctions." *Econometrica*, 68(3), 525-574. Assign proximity 2/5 (methods foundation). Also correct the journal attribution in the frontier map from "QJE" to "Econometrica."

2. **Add Hendel & Nevo (2006) to the annotated bibliography and BibTeX.** Hendel, I. & Nevo, A. (2006). "Measuring the Implications of Sales and Consumer Inventory Behavior." *Econometrica*, 74(6), 1637-1673. Assign proximity 2/5 (durable goods strand). Connect the relevance note to the consumption buyer's intertemporal optimization in the Liquid Assets model.

3. **Add Paarsch & Hong (2006) to the BibTeX.** Paarsch, H. J. & Hong, H. (2006). *An Introduction to the Structural Econometrics of Auction Data*. MIT Press. A brief entry is sufficient -- this is a methods textbook, not a research contribution requiring full annotation.

4. **Address the Qian & Wen (2015) publication status.** Either find a published successor or add a caveat note in the frontier map noting the reliance on an unpublished source for the import-magnitude estimate. The identification strategy itself is not threatened because Masset et al. (2016) provides published evidence, but the specific magnitude claim should have a published backing.

5. **Upgrade Ginsburgh (1998) proximity from 3/5 to 4/5.** It is the only structural auction model paper applied to wine markets in the entire literature.

## What Was Done Well

- **BibTeX corrections executed.** The Dimson (2015) entry is now correct: Rousseau, JFE, Vol. 118. This was the single highest-priority fix from the prior review and it has been completed in the main project bibliography.

- **Structural demand estimation strand now covered.** BLP (1995) and Nevo (2001) are in the annotated bibliography with clear, accurate summaries and correct BibTeX entries. This was the most critical content gap from the prior review.

- **Frontier map is excellent.** The "What Has Been Established," "Methodological Frontier," "Data Frontier," and "Open Questions" structure is precisely what a paper introduction and literature review should draw from. The positioning statement at the end -- "No published paper has combined (1) + (2) + (3)" -- is crisp and defensible.

- **Rosen (1974) and Gavazza et al. (2014) are now in the project bibliography.** These anchor papers were flagged as missing in the prior review and have been added.

- **Scooping risk assessment is rigorous and current.** The Verdickt (2025) monitoring note is exactly the right level of diligence. The four-part uniqueness claim is well-constructed.

- **Coverage breadth is strong.** 58 total papers across 8 categories, spanning wine economics, alternative assets, auction theory, structural estimation, durable goods, and the China shock. The search covered 26+ journals and 5 repositories. This is appropriate scope for a JFE-level submission.

- **Working paper reliance is minimal.** Only 1 of 45 new papers is unpublished (Qian & Wen 2015). This is well below the 50% threshold and far better than typical early-stage literature reviews.

- **BibTeX completeness for the new bibliography.** All 45 new papers have complete BibTeX entries in the librarian's `references.bib` (46 entries total including one duplicate Bagwell & Bernheim key). This was a requirement and it has been met.

## Papers to Search For (Priority Order -- Top 5 Gaps)

1. **Guerre, Perrigne & Vuong (2000)** -- "Optimal Nonparametric Estimation of First-Price Auctions," *Econometrica* 68(3):525-574. Foundational structural auction estimation. Search: author names + Econometrica 2000.

2. **Hendel & Nevo (2006)** -- "Measuring the Implications of Sales and Consumer Inventory Behavior," *Econometrica* 74(6):1637-1673. Storable goods with forward-looking consumers. Search: Hendel Nevo Econometrica 2006.

3. **Paarsch & Hong (2006)** -- *An Introduction to the Structural Econometrics of Auction Data*, MIT Press. Textbook for structural auction estimation. Search: Paarsch Hong MIT Press 2006.

4. **Published source for China luxury import decline magnitude** -- to replace or supplement Qian & Wen (2015). Search: "anti-corruption campaign" + "luxury imports" + China + published journal article. Consider: Lin et al. (2020 JDE), Ke et al. (2021 JPubE), or Chen & Kung (2019 QJE) on the broader anti-corruption effects.

5. **Athey & Haile (2002)** -- "Identification of Standard Auction Models," *Econometrica* 70(6):2107-2140. Identification conditions for structural auction models with heterogeneous bidders. Directly relevant if the structural model relies on auction-theoretic identification rather than BLP-style product-market identification. Search: Athey Haile Econometrica 2002.

---

*Review completed: 2026-03-30*
*Reviewer: Academic Editor (cloco research system)*
*Prior review: 2026-03-29 (score: 62/100, decision: Revise)*
*Status: PASS -- score 82/100 exceeds 80 threshold; literature collection approved to proceed*
*Recommended: Address Required Actions 1-5 before paper drafting to prevent citation gaps surfacing at peer review*

# Editor Review — Combined Literature Coverage, "Distributional Debt Capacity: Optimal Transport and Corporate Leverage"

**Date:** 2026-06-14
**Mode:** Lit Critic (Discovery phase, medium severity)
**Score:** 88/100
**Decision:** Pass (≥ 80)

---

## Executive Summary

The four parallel searches deliver genuinely strong, well-balanced coverage across all four pillars of the paper (OT theory/applications, GMM/SMM methodology, debt-capacity theory/empirics, credit spreads/capital supply), and — critically — both title-sharing and puzzle-anchoring competitors were caught: Rampini-Viswanathan (2010) is flagged Proximity 5 with a correct differentiation strategy, and Collin-Dufresne-Goldstein-Martin (2001) is flagged Proximity 5 in two separate searches. This is a Pass. The deductions are for a small number of avoidable gaps (a missing seminal financial-intermediation paper, an inconsistency in one librarian's proximity scale, light coverage of one methods sub-strand, and a handful of incomplete/duplicated BibTeX entries), none of which threaten the positioning.

The single most important finding: **the two papers most likely to cause a desk-level "this has been done" reaction — Rampini-Viswanathan (2010), which shares the exact title phrase "the distribution of debt capacity," and CDGM (2001), the credit-spread-puzzle anchor — are both present, scored at maximum proximity, and accompanied by explicit mechanism-level differentiation.** The literature base is submission-grade in its bones.

---

## Coverage Assessment

### Strand balance — strong
| Strand | Source file | New papers | Verdict |
|--------|-------------|-----------|---------|
| OT in finance/econ | lit_review_ot_finance.md | ~30 new | Excellent breadth: martingale OT, DRO, matching, barycenters, computation |
| GMM/SMM methodology | lit_review_smm_estimation/ | ~25 new | Complete econometric spine: Hansen, Newey-West, Andrews, partial-ID, moment selection |
| Debt capacity | lit_review_debt_capacity.md | ~20 new | Both title-competitor (RV 2010/2013) and empirical benchmark (Lian-Ma) anchored |
| Credit spreads / capital supply | lit_review_credit_spreads_capital_supply/ | ~30 new | The strongest of the four: spread-puzzle, intermediary AP, TRACE methodology, lender heterogeneity |

The four strands map cleanly onto the paper's four moving parts (W1/W2 theory, the SMM/constrained-GMM estimator, the debt-capacity object, and the spread/supply identification). No strand is starved.

### Journal-quality distribution — strong
The overwhelming majority of catalogued papers are in Top-5 finance/econ outlets (JF, RFS, JFE, AER, JPE, QJE, Econometrica, ReStud) or top math-finance journals (Finance and Stochastics, Mathematical Finance, Annals of Statistics). Working-paper reliance is well under the 50% flag threshold — the unpublished entries (Back et al., Malamud-Cieslak-Schrimpf, Greenwald 2019, Kermani-Ma 2022, Ivashina-Vallee, Galichon-Henry 2026 guide) are each justified by being the unique source for a specific point. No deduction on this axis.

### Recency — strong
Multiple 2024–2026 publications are present and correctly flagged as the live competitive frontier: Bretscher-Schmid-Sen-Sharma (RFS 2026), Huang-Nozawa-Shi (JF 2025), Greenwald-Krainer-Paul (JF 2025), Benmelech-Kumar-Rajan (JF 2024), Boerma-Tsyvinski-Zimin (JPE 2025). The credit-spreads search's scooping-risk monitoring of the RFS and JF pipelines is exactly the right instinct at Discovery.

### Scooping assessment — credible
The "no Proximity-5 scoop with same framework" conclusion is defensible: each search ran the right query combinations ("Wasserstein"+"debt capacity", "optimal transport"+"capital structure"), and the nearest neighbors (Bretscher et al. demand-system; Goldberg-Nozawa liquidity supply; Gomes-Schmid structural equilibrium) are correctly characterized as adjacent-not-competing with concrete differentiators.

---

## Issues Found

### Issue 1 — Missing seminal financial-intermediation paper: Diamond (1984) — Severity: Medium — Deduction: −6
The debt-capacity and credit-supply strands lean heavily on costly-state-verification (Townsend 1979; Gale-Hellwig 1985) and collateral (Rampini-Viswanathan) foundations but **omit Diamond (1984, ReStud), "Financial Intermediation and Delegated Monitoring."** For a paper whose entire object is the matching between a continuum of borrowers (μ_it) and an aggregate capital supply (ν_t) intermediated by lenders, delegated monitoring is a first-order theoretical ancestor — it is the canonical reason the lender side aggregates into a single ν at all. Any corporate-finance referee will expect it cited alongside Holmstrom-Tirole (1997). This is the one genuinely seminal omission.

### Issue 2 — Proximity-scale inconsistency across the four searches — Severity: Medium — Deduction: −4
The four librarians used **two incompatible proximity conventions.** The debt-capacity and credit-spreads searches use 5 = closest/direct-competitor (correct, and Villani/Brenier sit at 1 = foundational). The OT-finance search **inverts this**: it labels Backhoff-Veraguas, Gunsilius, Galichon-Salanie, and the Galichon-Henry guide as "Proximity 1/5" and explicitly says "Proximity 1 (directly uses OT... must cite)," while scoring already-cited foundational math (Brenier, Gangbo-McCann, Villani) at 3/5. Within the OT file the scale is internally consistent, but **across the combined bibliography the same numeral means opposite things** — a reader merging the four files will mis-rank papers. Because the prioritized list below has to reconcile this by hand, the inconsistency is real and must be normalized before these scores feed any downstream ranking.

### Issue 3 — Thin coverage of the Fréchet-mean / Wasserstein-barycenter estimation strand — Severity: Medium — Deduction: −3
The paper's identification hinges on estimating ν_t as the **Fréchet mean of firm cash-flow distributions** (per the contribution statement and domain profile). Yet the barycenter/Fréchet-mean estimation literature is represented essentially only by Gunsilius (2023) (application) and Panaretos-Zemel (2019) (general survey). The foundational **Agueh-Carlier (2011, SIAM J. Math. Anal.), "Barycenters in the Wasserstein Space"** — the paper that establishes existence, uniqueness, and characterization of exactly the object the estimator computes — is absent, as is any treatment of barycenter consistency/CLT (e.g., the del Barrio-Loubes line). For a referee probing whether the Fréchet-mean estimator is well-posed and whether its sampling distribution is known, this is a coverage hole in the methodological core, not the periphery.

### Issue 4 — Incomplete and duplicated BibTeX entries — Severity: Low — Deduction: −3 (−1.5 incomplete ×2)
Two specific BibTeX defects in the OT-finance file:
- `@book{Brenier1991polar, ... journal = {Communications on Pure and Applied Mathematics} ...}` — entry type is `@book` but the fields are a journal article; will mis-render and may break the build. Should be `@article`.
- The combined set contains **duplicate keys for the same paper across files**: CDGM (2001) appears as `CollinDufresne2001determinants` (credit-spreads file) and `CollinDufresneGoldsteinMartin2001determinants` (smm file); CDG (2001) "stationary leverage" appears as `CollinDufresneGoldstein2001credit` (smm file) only. When the four `.bib` files are merged into the single `paper/references.bib`, these collide or fragment. A de-duplication/key-reconciliation pass is required before merge. (Note: this is a merge-readiness defect, not a missing-entry defect — every cited paper does have at least one complete entry.)

### Issue 5 — Greenwald (2019) and a few key new papers risk staying as working-paper-only citations — Severity: Low — Deduction: −0 (advisory)
Greenwald (2019) is cited as the closest structural antecedent for cash-flow-based debt capacity but remains `@unpublished`. No deduction (it is genuinely the best source and the reliance is light), but flag for the writer: confirm current publication status before submission, as a stale "working paper" cite for your single closest structural competitor invites a referee comment.

---

## Score Breakdown
- Starting: 100
- Issue 1 (missing seminal: Diamond 1984): −6
- Issue 2 (proximity-scale inconsistency across searches): −4
- Issue 3 (thin Fréchet-mean/barycenter estimation strand): −3
- Issue 4 (incomplete/duplicated BibTeX, merge-readiness): −3
- Issue 5 (advisory): −0
- **Final: 88/100 — Pass**

*(Discovery-phase severity applied: per the severity gradient, missing-citation and notation deductions are scaled toward the low end. The same Diamond omission would be −20 at Peer Review; here it is −6.)*

---

## Prioritized Citation List

New papers only (not already in `paper/references.bib`). Sorted by **(a) priority, then (b) strand.** Proximity scales normalized to the 5 = closest convention.

### Priority 1 — Must Cite

**Debt capacity**
- Rampini & Viswanathan (2010, JF) — *shares the title phrase "the distribution of debt capacity"; must differentiate in the Introduction (mechanism: W1/OT vs. collateral/limited-enforcement).*
- Rampini & Viswanathan (2013, JFE) — dynamic extension; cite as the collateral-constraint benchmark.
- Greenwald (2019) — closest structural model of cash-flow-based debt capacity (two-covenant system); confirm pub status.
- Kermani & Ma (2022) — going-concern vs. asset-based debt; empirical motivation for μ_it as the relevant object.

**Credit spreads / capital supply**
- Collin-Dufresne, Goldstein & Martin (2001, JF) — *the credit-spread-puzzle anchor; the unexplained common factor is precisely what W1 is claimed to name. Must address head-on.*
- Gilchrist & Zakrajšek (2012, AER) — EBP as the time-series analog of the W1 channel; primary comparator.
- Nozawa (2017, JF) — definitive cross-section-of-spreads decomposition; the paper's cross-sectional claim is judged against this.
- Siriwardane (2019, JF) — capital shocks → spreads; direct empirical competitor (CDS vs. TRACE).
- Bretscher, Schmid, Sen & Sharma (2026, RFS) — published demand-system competitor; frame as complementary, run the horse race.
- He & Krishnamurthy (2013, AER) — intermediary-capital theoretical foundation for the supply-side interpretation of ν_t.
- Adrian, Etula & Muir (2014, JF) — broker-dealer leverage as the empirical capital-supply proxy; validates ν_t against FRED.

**GMM/SMM methodology**
- Hansen (1982, Ecta) — primary GMM reference + J-test.
- Newey & West (1987, Ecta) — weighting-matrix / HAC standard.
- Strebulaev & Whited (2012, FnT) — definitive structural-corporate-finance estimation survey.
- Duffie & Singleton (1993, Ecta) + Lee & Ingram (1991, J.Econometrics) — SMM foundations (for pre-estimation of μ_it).

**OT in finance/econ**
- Gunsilius (2023, Ecta) — Wasserstein barycenter as counterfactual; closest applied-econometrics antecedent for the Fréchet-mean estimator.
- Galichon & Salanié (2022, ReStud) — OT matching identification; the logic the firm–capital coupling follows. *(already partly in bib — verify)*
- Panaretos & Zemel (2019, Ann. Rev. Stat.) — sampling/inference properties of empirical Wasserstein distances; needed for first-stage uncertainty.

**Missing seminal (Issue 1) — add**
- Diamond (1984, ReStud) — delegated monitoring; the reason the lender side aggregates into ν_t.

**Missing methods foundation (Issue 3) — add**
- Agueh & Carlier (2011, SIAM J. Math. Anal.) — existence/uniqueness/characterization of the Wasserstein barycenter (= the Fréchet-mean object being estimated).

### Priority 2 — Should Cite

**Debt capacity**
- Hart & Moore (1994, QJE); Kiyotaki & Moore (1997, JPE); Nikolov-Schmid-Steri (2021, JFE); DeAngelo-DeAngelo-Whited (2011, JFE — verify, may be in bib); Greenwald-Krainer-Paul (2025, JF); Chaney-Sraer-Thesmar (2012, AER); Farre-Mensa & Ljungqvist (2016, RFS); Gormley & Matsa (2014, RFS — methods, FE warning).

**Credit spreads / capital supply**
- Chen (2010, JF); Chen-Collin-Dufresne-Goldstein (2009, RFS); Huang-Nozawa-Shi (2025, JF); Feldhütter-Schaefer (2018, RFS); Huang-Huang (2012, RAPS); He-Kelly-Manela (2017, JFE); Adrian-Shin (2010, JFI; 2014, RFS); Goldberg-Nozawa (2021, JF); Chernenko-Sunderam (2012, RFS); Becker-Ivashina (2015, JF); Faulkender-Petersen (2006, RFS); Gomes-Schmid (2021, JF); Dick-Nielsen-Feldhütter-Lando (2012, JFE — TRACE methodology); Bao-Pan-Wang (2011, JF — illiquidity control).

**GMM/SMM methodology**
- Hansen-Singleton (1982, Ecta); Andrews (1991, Ecta); Newey-McFadden (1994, Handbook); Sargan (1958, Ecta); Burnside-Eichenbaum (1996, JBES — moment-count defense); Gouriéroux-Monfort-Renault (1993, JAE); Erickson-Whited (2000, JPE); Bloom (2009, Ecta).

**OT in finance/econ**
- Backhoff-Veraguas et al. (2020, F&S — adapted Wasserstein, defends static-vs-dynamic choice); Blanchet-Murthy (2019, MOR); Mohajerin Esfahani-Kuhn (2018, Math. Prog. — DRO tractability); Lindenlaub-Postel-Vinay (2023, JPE); Galichon (2017, Econometrics J.) / Galichon-Henry (2026 guide).

### Priority 3 — Optional

**Credit spreads / lender heterogeneity / TRACE**
- Longstaff-Schwartz (1995); Longstaff-Mithal-Neis (2005); Ericsson-Renault (2006); Friewald-Jankowitsch-Subrahmanyam (2012); Chen-Cui-He-Milbradt (2018); He-Milbradt (2014); Bhamra-Kuehn-Strebulaev (2010); Kuehn-Schmid (2014); Koijen-Yogo (2023); Colla-Ippolito-Li (2013); Rauh-Sufi (2010); Flannery-Nikolova-Oztekin (2012); Benmelech-Kumar-Rajan (2024); Erel-Julio-Kim-Weisbach (2012); Greenwood-Hanson-Shleifer-Sorensen (2022); Ivashina-Laeven-Moral-Benito (2022); Becker-Ivashina (2016).

**OT theory/computation/math-finance**
- Beiglböck-Henry-Labordère-Penkner (2013); Dolinsky-Soner (2014); Hobson-Neuberger (2012); Acciaio et al. (2016); Guo-Loeper-Wang (2022); Eckstein et al. (2021); Cuturi (2013); Peyré-Cuturi (2019); Bartl et al. (2021); Pflug-Pichler (2012); Hallin et al. (2021); Chernozhukov-Fernández-Val-Melly (2013); Lacker (2018); Birghila-Pflug (2019); Fajgelbaum-Schaal (2020); Boerma-Tsyvinski-Zimin (2025); Nguyen et al. (2024); Blanchet-Chen-Zhou (2022).

**GMM partial-ID / robustness**
- Chernozhukov-Lee-Rosen (2013); Andrews-Shi (2013); Kaido-Molinari-Stoye (2019); Andrews-Guggenberger (2019); Andrews (1999); Andrews-Monahan (1992); Nevo (2000); Koijen-Yogo (2019); Krusell-Smith (1998); Cagetti-De Nardi (2006); Albuquerque-Hopenhayn (2004); Whited-Zhao (2021); Ottonello-Winberry (2020); Gomes-Schmid (2010); Gomes (2001); DeMarzo-Fishman (2007); Brunnermeier-Sannikov (2014); Griliches-Hausman (1986).

**Theory foundations (verify against bib — several already present)**
- Stiglitz-Weiss (1981); Aghion-Bolton (1992); Bernanke-Gertler (1989); Geanakoplos (2010); Brunnermeier-Pedersen (2009); Allen-Gale (2004); Brunnermeier-Krishnamurthy (2020); MacKay-Phillips (2005 — verify); Almeida-Campello-Laranjeira-Weisbenner (2012); Demiroglu-James (2010); Ivashina-Vallee (2020).

---

## Required Actions
1. **Add Diamond (1984, ReStud)** to the bibliography and position it in the related-literature section alongside Holmstrom-Tirole (1997) as the delegated-monitoring foundation for aggregating the lender side into ν_t.
2. **Add Agueh-Carlier (2011)** and at least one barycenter consistency/CLT reference (del Barrio-Loubes line or equivalent) to support the well-posedness and sampling theory of the Fréchet-mean estimator of ν_t.
3. **Normalize the proximity scale** across all four search outputs to a single convention (5 = closest competitor) before any score feeds downstream ranking; re-rank the OT-finance file's "Proximity 1" applied papers as Proximity 5.
4. **Run a BibTeX de-duplication and key-reconciliation pass** when merging the four `.bib` files into `paper/references.bib`: fix `@book{Brenier1991polar}` → `@article`; resolve the duplicate CDGM (2001) keys; confirm no key collisions.
5. **Confirm publication status** of Greenwald (2019) and any other `@unpublished` Priority-1/2 entries before the manuscript cites them as closest competitors.
6. **Cross-check the "already in bib" Priority-2/3 items flagged "verify"** (Galichon-Salanié, DeAngelo-DeAngelo-Whited 2011, MacKay-Phillips) against the 68-entry `paper/references.bib` to avoid duplicate insertion.

---

## What Was Done Well
- **Both danger papers caught.** Rampini-Viswanathan (2010) and CDGM (2001) — the two most likely sources of a "this is already done" reaction — are each at maximum proximity with concrete, mechanism-level differentiation already drafted. This is the single most important thing a Discovery-phase lit review for this paper had to get right, and it did.
- **The credit-spreads/capital-supply search is exemplary.** It anchors the paper's central empirical claim (W1 names the CDGM common factor / EBP) to the right four-to-five comparators, supplies the TRACE methodology controls the empirics will need, and monitors the live RFS/JF pipeline for scooping. The per-paper FLAG annotations on Proximity-5 entries are exactly the right level of editorial signal.
- **The GMM/SMM spine is complete and honestly positioned.** The frontier map's admission that the 10-spread-moment constrained-GMM design "sits at the established, rigorous core, not at the frontier" is the correct, referee-disarming framing — and the Burnside-Eichenbaum moment-count defense is pre-loaded.
- **Strand balance and journal quality are submission-grade**, with working-paper reliance well under threshold and a strong 2024–2026 recency profile.

# Citation Audit Report
**Date:** 2026-05-14
**Bib file:** paper/references.bib
**Paper:** paper/main.tex

---

## Summary

- Total entries in .bib: 33
- Total citations used in paper: 28
- Unused entries: 5
- CRITICAL issues: 0
- MAJOR issues: 0
- Hallucination suspects (corrected): 2 — both fixed in this session
- Advisory: 1 (missing DOI, entry correct)

---

## CRITICAL Issues

None.

---

## MAJOR Issues

None.

---

## Hallucination / Accuracy Flags

| Key | Status | Filed As | What Web Search Found | Action |
|-----|--------|----------|-----------------------|--------|
| `basak2007optimal` | FIXED | Basak, Pavlova & Shapiro (2007), RFS | Paper confirmed (RFS vol 20 no 5 pp 1583–1621). DOI `hhm037` belongs to Duffie, Garleanu & Pedersen. Correct DOI is `10.1093/rfs/hhm026` | DOI corrected in .bib |
| `HuangSialmZhang2011` | FIXED | Huang, Sialm & Zhang (2011), RFS | Paper confirmed (RFS vol 24 no 8 pp 2575–2616, DOI `10.1093/rfs/hhr001`). First author is **Jennifer C. Huang** (UT Austin / now HKUST), not Jing-Zhi Huang (Penn State) | Author corrected in .bib |

---

## Advisory

| Key | Note |
|-----|------|
| `sirri1998costly` | No DOI in .bib. Paper verified (JF vol 53 no 5, 1998, pp 1589–1622). Correct DOI: `10.1111/0022-1082.00066`. Non-blocking; add at your discretion. |

---

## Unused Entries (informational)

These keys are in `references.bib` but not cited anywhere in the paper. They are not errors — they may be retained for future use or removed to keep the bibliography clean.

| Key | Entry |
|-----|-------|
| `ross1973economic` | Ross, Stephen A. (1973) "The economic theory of agency: The principal's problem," AER |
| `he2012model` | He & Krishnamurthy (2012) "A model of capital and crises," JPE |
| `ma2019portfolio` | Ma, Tang & Gomez (2019) "Portfolio manager compensation and mutual fund risk taking," JFE |
| `barber2016which` | Barber, Huang & Odean (2016) "Which factors matter to investors?" JFE (also missing volume/number/pages) |
| `kosowski2006can` | Kosowski, Timmermann, Wermers & White (2006) "Can mutual fund 'stars' really pick stocks?" JF |

---

## VERIFIED Entries (26 of 28 cited entries confirmed)

All 26 entries below were confirmed via web search (Semantic Scholar, journal DOI resolvers, NBER, SSRN). Fields — author, year, journal, title — match the .bib record.

| Key | Verification |
|-----|-------------|
| `berk2004mutual` | VERIFIED — JPE 112(6), 2004 |
| `BebchukCohenHirst2017` | VERIFIED — JEP 31(3), 2017, DOI confirmed |
| `Gil-Bazo2008` | VERIFIED — JEBO 67(3-4), 2008, DOI confirmed |
| `Ippolito1992ConsumerReaction` | VERIFIED — JLE 35(1), 1992, DOI confirmed |
| `BrownHarlowStarks1996` | VERIFIED — JF 51(1), 1996, DOI confirmed |
| `sirri1998costly` | VERIFIED — JF 53(5), 1998 (DOI advisory — see above) |
| `chevalier1997risk` | VERIFIED — JPE 105(6), 1997 |
| `Holmstrom1979` | VERIFIED — Bell Journal of Economics 10(1), 1979, DOI confirmed |
| `AdmatiPfleiderer1997` | VERIFIED — Journal of Business 70(3), 1997, DOI confirmed |
| `JensenMeckling1976` | VERIFIED — JFE 3(4), 1976, DOI confirmed |
| `Musto1999` | VERIFIED — JF 54(3), 1999, DOI confirmed |
| `CarhartKanielMustoReed2002` | VERIFIED — JF 57(2), 2002, DOI confirmed |
| `Starks1987` | VERIFIED — JFQA 22(1), 1987, DOI confirmed |
| `HolmstromMilgrom1987` | VERIFIED — Econometrica 55(2), 1987, DOI confirmed |
| `campbell2002strategic` | VERIFIED — OUP book, 2002 |
| `guiso2018time` | VERIFIED — JFE 128(3), 2018, DOI confirmed |
| `carhart1997persistence` | VERIFIED — JF 52(1), 1997, DOI confirmed |
| `fung2004hedge` | VERIFIED — FAJ 60(5), 2004, DOI confirmed |
| `ferreira2012flow` | VERIFIED — Journal of Banking & Finance 36(6), 2012, DOI confirmed |
| `barras2010false` | VERIFIED — JF 65(1), 2010, DOI confirmed |
| `Carpenter2000` | VERIFIED — JF 55(5), 2000, DOI confirmed |
| `CuocoKaniel2011` | VERIFIED — JFE 101(2), 2011, DOI confirmed |
| `HuangSialmZhang2011` | FIXED then VERIFIED — RFS 24(8), 2011, DOI confirmed |
| `OuYang2003` | VERIFIED — RFS 16(1), 2003, DOI confirmed |
| `VayanosWoolley2013` | VERIFIED — RFS 26(5), 2013, DOI confirmed |
| `GetmanskyLoMakarov2004` | VERIFIED — JFE 74(3), 2004, DOI confirmed |
| `BollenPool2009` | VERIFIED — JF 64(5), 2009, DOI confirmed |
| `basak2007optimal` | FIXED then VERIFIED — RFS 20(5), 2007, DOI corrected |

---

## MINOR Issues

None beyond the advisory DOI note for `sirri1998costly`.

---

## Methodology

**Step 1 — Citation extraction:** All `.tex` files under `paper/` grepped for `\cite`, `\citet`, `\citep`, `\citeauthor`, `\citeyear`, `\citealt`, `\nocite` including natbib optional-argument forms `\citep[][]{key}`. 28 unique keys identified.

**Step 2 — Structural audit:** All 33 .bib entries checked for required fields (author, title, year, journal/publisher), plausible year range, duplicate keys, and cross-reference against paper citations. No missing entries; no duplicates.

**Step 3 — Hallucination audit:** All 28 cited entries dispatched in batches to web-search verification agents (Semantic Scholar, journal DOI resolvers, SSRN, NBER). Results: 26 VERIFIED, 2 SUSPECT — both corrected.

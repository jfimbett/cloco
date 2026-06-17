---
name: domain-debt-capacity
description: Literature anchor for distributional debt capacity project — OT/Wasserstein framework; key papers, scooping risks, datasets
metadata:
  type: project
---

# Project: Distributional Debt Capacity via Wasserstein Distance

**Core claim**: δ_i = W1(µ_i, ν)/2 where µ_i is firm cash flow distribution, ν is aggregate capital supply distribution.

## Anchor Papers (must cite, highest proximity)

| Paper | Journal | Year | Proximity | Why Critical |
|-------|---------|------|-----------|--------------|
| Rampini-Viswanathan | JF | 2010 | 5 | Title uses "distribution of debt capacity"; collateral-based counterpart |
| Rampini-Viswanathan | JFE | 2013 | 5 | Dynamic extension; same object, different mechanism |
| Lian-Ma | QJE | 2021 | 5 | Empirical benchmark: 80% of US corporate debt is EBC-based |
| Hart-Moore | QJE | 1994 | 4 | Debt capacity from inalienability; incomplete contracts |
| Kiyotaki-Moore | JPE | 1997 | 4 | Endogenous borrowing constraints tied to asset value distribution |
| Greenwald | MIT WP | 2019 | 4 | Closest structural model; cash-flow covenants → debt capacity |
| Kermani-Ma | NBER WP | 2022 | 4 | Going-concern vs. discrete-asset debt; 80% cash-flow-based |
| Nikolov-Schmid-Steri | JFE | 2021 | 4 | SMM tests of financing constraint models — same estimation method |

## Scooping Risks (must address in Introduction)

1. **Rampini-Viswanathan 2010** — title "distribution of debt capacity" overlaps directly; distinguish by mechanism (OT distance vs. collateral constraint)
2. **Lian-Ma 2021** — empirical documentation of EBCs; your paper provides the theory they lack
3. **Greenwald 2019** — structural model of cash-flow-based debt capacity; your paper derives optimal contract rather than imposing covenant forms

## Key Datasets in This Literature

- **DealScan**: loan covenant data (Lian-Ma, Demiroglu-James, Ivashina-Vallee)
- **Compustat Quarterly**: operating cash flows (oancfy), leverage, assets
- **Capital IQ**: debt contracts, bond covenants (Kermani-Ma)
- **FRED / Flow of Funds**: aggregate credit supply ν_t (Fed H.8, Z.1)
- **Federal Reserve Y-14 supervisory data**: near-universe of large-bank loans (Greenwald-Krainer-Paul 2025) — access restricted

## Common Identification Strategies in This Field

- **SMM**: Hennessy-Whited (2007), Nikolov-Schmid-Steri (2021) — template for structural estimation
- **IV (collateral shocks)**: Chaney-Sraer-Thesmar (2012) — real estate prices × land supply inelasticity
- **RDD (covenant violations)**: Chava-Roberts (2008) style, used by Lian-Ma (2021)
- **DiD (debt maturity)**: Almeida et al. (2012) — pre-crisis maturity × crisis timing

## Cross-Sectional Leverage Horse Race Controls (must beat)

Frank-Goyal (2009) six factors: median industry leverage (+), market-to-book (–), tangibility (+), profitability (–), log assets (+), expected inflation (+). Published in Financial Management (not JFE).

## Key Theoretical Foundations

- Townsend (1979, JET) — optimal contracts under CSV; ancestor of all cash-flow-based lending
- Gale-Hellwig (1985, REStud) — standard debt is optimal under CSV
- Brenier (1991, CPAM) — polar factorization; mathematical basis for quantile coupling result
- Villani (2009, Springer) — OT textbook; W1 dual representation

## Methodological Note

DeAngelo-DeAngelo-Whited (2011, JFE) show spare debt capacity has option value — motivates why firms do not fully exhaust δ_i. Use as justification for why empirical leverage < δ_i.

## Output Files (from 2026-06-14 search)

- `paper/quality_reports/lit_review_debt_capacity.md` — annotated bibliography (34 papers)
- `paper/quality_reports/references_debt_capacity.bib` — complete BibTeX (34 entries)

**Why**: This is the primary literature map for the OT debt capacity paper. Update when new papers are found or when scooping risk status changes.
**How to apply**: Load these anchors at the start of any lit review, positioning, or drafting task for this project.

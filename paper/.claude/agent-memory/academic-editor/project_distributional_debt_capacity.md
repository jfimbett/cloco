---
name: project-distributional-debt-capacity
description: Key positioning facts and recurring review hazards for the "Distributional Debt Capacity" (optimal transport / Wasserstein) paper
metadata:
  type: project
---

# Distributional Debt Capacity — editor-relevant facts

Paper: W1/W2 Wasserstein distances characterize debt capacity as W1(mu_it, nu_t), mu_it = firm cash-flow dist, nu_t = aggregate capital supply dist. nu_t estimated as Frechet mean of firm distributions (FRED-anchored). kappa via constrained GMM with 10 decile-mean TRACE spread moments. Main result: within-firm beta = -0.163*** (t=-9.1); interior-decile beta = -0.382** (t=-2.8).

## Two "danger papers" — must always be present and differentiated
- **Rampini & Viswanathan (2010, JF)** "Collateral, Risk Management, and the Distribution of Debt Capacity" — shares the exact title phrase. Differentiator: W1/OT mechanism vs. collateral/limited-enforcement. If a draft drops this cite, flag hard.
- **Collin-Dufresne-Goldstein-Martin (2001, JF)** — credit-spread-puzzle anchor; the unexplained common factor is what W1 is claimed to name. Must be addressed head-on in intro.
- Both are NOT in the original 68-entry `paper/references.bib`; they came in via the librarian searches. Confirm they get merged.

## Recurring review hazards for this paper
- **Frechet-mean estimator well-posedness**: needs Agueh-Carlier (2011) for barycenter existence/uniqueness + a barycenter consistency/CLT cite. Easy to omit; methodological core, not periphery.
- **Diamond (1984, ReStud)** delegated monitoring — the reason the lender side aggregates into a single nu_t. Seminal omission risk alongside Holmstrom-Tirole (1997).
- **Circularity referee concern**: nu_t anchored to FRED Flow-of-Funds (observable), not to leverage — defense is in positioning.md.
- **Credit-spread-puzzle critique**: paper uses spread *levels* in cross-section (not changes), nu_t absorbs supply factor, J-test reveals rejection.

## Lit-review process note
- The four parallel librarian searches used **two incompatible proximity scales**: debt-capacity & credit-spreads use 5=closest; the OT-finance file inverts it (1=closest, "Proximity 1 must cite"). Normalize to 5=closest before merging any ranking.
- Lit synthesis (2026-06-14): scored 88/100, Pass. Report at `paper/quality_reports/lit_review_synthesis_editor.md`.

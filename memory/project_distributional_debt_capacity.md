---
name: project-distributional-debt-capacity
description: Core context for the distributional debt capacity paper — project type, research question, empirical strategy, contribution
metadata:
  type: project
---

**Project:** Distributional Debt Capacity — An Optimal Transport Framework for Capital Structure

**Research question:** Does W1(μ_it, ν_t) — the Wasserstein distance between firm cash flow distributions and aggregate capital supply distribution — explain cross-sectional leverage heterogeneity beyond mean and variance?

**Project type:** Structural estimation (type C). Formal OT model + SMM estimation.

**Why:** The existing draft (old/main.tex) is mathematically rigorous but lacks finance intuition and has hallucinated empirical numbers. The rewrite must be finance-first.

**Key theoretical results (from old/main.tex — correct):**
- Optimal contract = quantile coupling D*(X) = F_ν^{-1}(F_μ(X)) (Brenier's theorem)
- Exact result: expected default shortfall = W1(μ_i, ν)/2
- Leverage strictly decreasing in W1(μ_i, ν) (Proposition leverage_wasserstein)
- Aggregate deadweight cost = W2²(μ, ν) at social planner level

**Structural parameters:** θ = (α_ν, σ_ν, κ) estimated via SMM. ν ~ LogNormal(α_ν, σ_ν²) — FREE parameters inside SMM, NOT pre-measured from external data. Using bond deal sizes as ν proxy is circular (they are equilibrium outcomes). Identification comes entirely from cross-equation restriction.

**μ_it:** Pre-estimated OUTSIDE SMM loop. LogNormal from 20-quarter rolling window MLE on quarterly Compustat `oancfy/atq` (baseline) and `(ibq+dpq)/atq` (robustness). Minimum 8 quarters. Winsorize at 1-99% by fiscal year.

**Data confirmed:**
- Compustat Quarterly (`comp.fundq`, WRDS): cash flows from 1988 (SFAS 95 boundary for oancfy)
- CRSP (WRDS): market equity via CCM merge
- Mergent FISD (`fisd.fisd_mergedissue`, WRDS): bond spreads at issuance, reliable from 1995
- NO FRED/Flow of Funds needed for ν (ν is estimated inside SMM)

**Sample periods:** Leverage panel 1988–2024; SMM spread moments 1995–2024 (FISD start).

**SMM standard errors:** Block bootstrap (500 reps, block = firm × year) + HAC weighting matrix. Cross-equation correlation from common macro shocks handled by block structure.

**Identification:** Cross-equation restriction — same θ must fit BOTH leverage distribution moments (Compustat/CRSP) AND spread distribution moments (Mergent FISD). These are independent datasets. J-test (Hansen 1982) is the overidentification test.

**Key contribution vs. Leland/Strebulaev/Gomes-Schmid:** All existing structural capital structure models treat capital supply as a price (r_f). This paper introduces capital supply as a distribution ν — a first in the literature. Sufficient statistic shifts from σ to W1(μ_i, ν).

**Research spec:** quality_reports/research_spec_distributional_debt_capacity.md
**Domain profile:** .claude/rules/domain-profile.md
**Existing draft:** old/main.tex (math correct, finance framing needs full rewrite)

**How to apply:** Use this context when any agent works on this project to avoid re-deriving the research design from scratch.

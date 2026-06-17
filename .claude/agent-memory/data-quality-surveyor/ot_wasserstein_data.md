---
name: ot-wasserstein-data
description: Data and identification issues specific to papers using optimal transport / Wasserstein distance as an empirical tool in economics/finance
metadata:
  type: feedback
---

## Optimal Transport Papers — Data Issues

### 1. The ν_t Measurement Problem Is Always the Paper's Weakest Point
Papers applying optimal transport to economic/finance settings always have a well-defined μ_i (the "sender" distribution, e.g., firm cash flows) but face a hard measurement problem for ν (the "receiver" distribution, e.g., capital supply). No standard data source provides a cross-sectional distribution of lender capacity or capital supply. All candidate proxies are either:
- Equilibrium allocations (biased by demand)
- Aggregate scalars (no cross-sectional shape)
- Administrative data that requires nontrivial aggregation

Always grade ν_t measurement as the highest-risk component and require the Explorer to identify at least two independent approaches with explicit theoretical defense of the supply-side interpretation.

### 2. W1 Distance Is Only a Valid Moment if Distributional Assumptions Are Tested
The W1 distance between two parametric distributions (e.g., LogNormal) is a closed-form function of their parameters. But if the true data-generating process is not log-normal, the W1 computed from estimated log-normal parameters is not the true W1 — it is a function of moment-matched approximations. Any SMM using W1 as a structural moment must include a distributional fit test (KS, AD, or Q-Q assessment) on the within-firm rolling window residuals. Without this, the SMM objective is optimizing the wrong distance.

### 3. Circularity Risk: OT Output ≠ OT Input
In the Brenier-Kantorovich framework, the optimal coupling maps firms to capital allocations. If the empirical ν_t is measured from equilibrium capital allocations (what lenders actually deployed), then ν_t is an output of the optimal transport problem, not an input. Measuring ν_t from outcomes and then computing W1(μ_it, ν_t) to explain those same outcomes is circular. This must be flagged as a potential deal-breaker whenever OT is used structurally and ν is measured from transaction data.

### 4. Welfare Claims (W2²) Require Full-Population Validity
OT welfare metrics (W2² as aggregate deadweight cost) are integrals over the full joint distribution. If the data covers only a selected subpopulation (public firms, bond issuers), the welfare calculation does not apply to the full economy even if the structural model is estimated consistently within the sample. Require explicit discussion of scope of welfare claims.

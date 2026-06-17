# Domain Profile

## Field

**Primary:** Corporate Finance — Capital Structure
**Adjacent subfields:** Financial Intermediation, Macro-Finance, Asset Pricing, Mathematical Finance

---

## Target Journals (ranked by tier)

| Tier | Journals |
|------|----------|
| Top-5 | Journal of Finance, Review of Financial Studies, Journal of Financial Economics |
| Top field | AER, JPE (for structural estimation + theory angle), Journal of Financial Intermediation |
| Strong field | Journal of Corporate Finance, Review of Finance |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| Compustat Quarterly | Panel | WRDS | Firm cash flows (oancfy), book leverage, assets — use for rolling μ_it estimation |
| CRSP | Panel | WRDS | Market leverage, equity returns |
| Capital IQ | Debt issuance | WRDS/S&P | Credit spreads at issuance, covenant data |
| FRED / Flow of Funds | Aggregate | Public | Capital supply distribution ν_t — credit market instruments, Fed balance sheet |

---

## Structural Estimation Setup

- **Firm cash flow distribution** $\mu_{it}$: pre-estimated from 20-quarter (5-year) rolling window, log-normal parametric family. Minimum 8 quarters for inclusion.
- **Capital supply distribution** $\nu_t$: parameterized as log-normal, time-varying location anchored to FRED aggregates. Estimated jointly inside SMM.
- **Structural parameters** $\theta = (\alpha_\nu, \sigma_\nu, \kappa)$ where $\alpha_\nu(t) = a_0 + a_1 z_t$ with $z_t$ from FRED.
- **Estimation method:** Simulated Method of Moments (SMM), following BLP (1995) architecture.
- **Standard errors:** Bootstrap full procedure (resample firms → re-estimate $\hat{\mu}_{it}$ → re-run SMM) to account for first-stage uncertainty.

---

## Common Identification Strategies

| Strategy | Typical Application | Key Assumption to Defend |
|----------|-------------------|------------------------|
| Structural SMM | Estimate ν and κ jointly from cross-section of leverage + spreads | Model correctly specified; ν anchored to FRED prevents circularity |
| Cross-equation restriction | Same θ must explain both leverage distribution and spread distribution | Overidentifying restriction — key test of the model |
| Time-series variation in ν_t | Aggregate capital supply shifts (QE, crises) shift W_1 for all firms | Shift in ν_t is exogenous to firm-level μ_it |

---

## Field Conventions

- Report **book leverage** (debt/assets) and **market leverage** (debt/(debt+market equity)) separately
- Credit spreads in **basis points**
- Wasserstein distances normalized by mean capital supply $\mathbb{E}_\nu[Y]$ for scale-free comparison
- Cluster standard errors at **firm level** for panel regressions; discuss time-series clustering separately
- Always include **firm fixed effects** and **year-quarter fixed effects**
- Industry classification: **SIC 2-digit** (exclude financials SIC 6000-6999, utilities SIC 4900-4999 as standard)
- When reporting structural estimates, always include **model fit statistics** (SMM objective, overidentification test)

---

## Notation Conventions

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| $\mu_{it}$ | Firm $i$'s cash flow distribution at time $t$ | Don't use $F_i$ without subscript $t$ |
| $\nu_t$ | Capital supply distribution at time $t$ | Don't call it "lender distribution" — it's aggregate capital supply |
| $W_1(\mu, \nu)$ | 1-Wasserstein distance (governs individual debt capacity) | Don't confuse with $W_2$ (governs aggregate deadweight cost) |
| $W_2(\mu, \nu)$ | 2-Wasserstein distance (governs social planner LP objective) | Never use $W_2^2$ and $W_2$ interchangeably in text |
| $\lambda_i^*$ | Optimal borrowing scale | Don't call it "leverage" directly — it's the scale applied to the optimal contract |
| $L_i^*$ | Optimal leverage $= \lambda_i^* \mathbb{E}_\nu[Y] / \mathbb{E}_{\mu_i}[X]$ | Always define on first use |
| $\kappa$ | Deadweight bankruptcy cost scaling | Distinguish from $\kappa(\lambda)$ truncation correction |
| $\theta$ | Structural parameter vector $(\alpha_\nu, \sigma_\nu, \kappa)$ | |

---

## Seminal References

| Paper | Why It Matters |
|-------|---------------|
| Modigliani-Miller (1958, 1963) | Capital structure irrelevance + tax shield benchmark — must cite |
| Merton (1974) | Structural default model — asset volatility as the key risk measure |
| Leland (1994) | Gold standard for structural capital structure — your model nests this as special case |
| Strebulaev (2007) | Dynamic structural capital structure estimation — closest existing structural paper |
| Frank and Goyal (2009) | Empirical leverage determinants horse race — your W1 must beat their controls |
| Rajan and Zingales (1995) | Cross-country leverage determinants — supply-side interpretation |
| Villani (2009) | Optimal transport theory — theoretical foundation |
| Brenier (1991) | Polar factorization theorem — source of the quantile coupling result |
| Berry, Levinsohn, Pakes (1995) | SMM estimation architecture — cite for methodology |

---

## Field-Specific Referee Concerns

- **"Why not just use variance?"** — Must show W1 explains leverage variation beyond mean and variance; the shape component beyond moments is the key test
- **"Circularity: you fit ν to explain leverage"** — Defend by anchoring ν to FRED capital supply data, not just leverage moments
- **"Log-normal for μ_it is too restrictive"** — Robustness: try non-parametric rolling CDF or gamma distribution; show W1 results are robust
- **"Compustat cash flows are accounting, not economic"** — Discuss operating cash flow (oancfy) vs. EBITDA; try both
- **"Why not a dynamic model?"** — The static model is a benchmark; dynamic extension is future work; static OT gives exact analytical results that dynamic models cannot
- **"The Wasserstein distance is not identified separately from κ"** — Show that W1 is computed from pre-estimated distributions, κ is identified from spread equation separately
- **"Financials and utilities should not be excluded"** — Report results including them as robustness

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| W1/W2 ratio approximation | ±14% | Confirmed empirically in paper (inter-decile range 0.72–1.11) |
| SMM overidentification test | p > 0.10 | Standard threshold for model fit |
| Bootstrap standard errors | 500 replications minimum | Stability of SMM objective |

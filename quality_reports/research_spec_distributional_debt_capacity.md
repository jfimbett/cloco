# Research Specification: Distributional Debt Capacity

**Date:** 2026-06-13
**Researcher:** Juan F. Imbet
**Institution:** Paris Dauphine University — PSL

---

## Project Type

`structural` — formal theoretical model (Kantorovich LP / optimal transport) with structural parameter estimation (SMM).

---

## Recommended Pipeline

```
/lit-review "optimal transport capital structure Wasserstein debt"
/find-data "Compustat quarterly cash flows CRSP leverage Capital IQ spreads FRED Flow of Funds"
/identify_reducedform "distributional mismatch leverage heterogeneity"   # for reduced-form validation
/data-analysis "SMM estimation structural capital structure"
/draft-paper "introduction empirical strategy results"
/proofread paper/main.tex
/review-paper paper/main.tex
```

---

## Research Question

Does the distributional shape mismatch between firm cash flow distributions and the aggregate capital supply distribution — measured by the Wasserstein distance $W_1(\mu_{it}, \nu_t)$ — constitute a sufficient statistic for corporate debt capacity that explains cross-sectional leverage heterogeneity beyond what firm-level mean and variance can predict?

---

## Motivation

The corporate capital structure literature has a well-documented puzzle: leverage varies enormously across firms with similar observable risk characteristics. Standard structural models (Leland 1994, Strebulaev 2007) predict leverage from asset volatility, tax rates, and bankruptcy costs — but two firms with identical volatility and tax exposure can have very different leverage in the data. The residual heterogeneity is large and persistent.

Existing structural models treat capital supply as a **price** — the risk-free rate $r_f$. Lenders are infinitely elastic; any firm can borrow any amount at the same rate. The only supply-side primitive is a scalar. This paper introduces capital supply as a **distribution** $\nu_t$ — a first in the structural capital structure literature. The central claim is that debt capacity is determined not just by the firm's own risk profile, but by how the shape of the firm's cash flow distribution aligns with the shape of aggregate capital supply. Firms whose cash flow distributions are "far" from the capital supply distribution in Wasserstein distance are credit-constrained relative to what their means and variances alone would predict.

This matters for policy: in standard models, credit supply is stimulated by lowering $r_f$. In this model, financial intermediaries that reduce distributional mismatch — transforming $\nu$ to better match the cross-section of firm $\mu_i$ — are welfare-improving even without changing the risk-free rate. The aggregate deadweight cost of bankruptcy equals $W_2^2(\mu, \nu)$ — a measurable, policy-relevant quantity.

---

## Hypothesis

**H1 (Cross-sectional):** $W_1(\hat{\mu}_{it}, \hat{\nu}_t)$ negatively predicts firm leverage, conditional on mean cash flows, volatility, firm size, market-to-book, tangibility, and profitability. The shape component of $W_1$ beyond mean and variance has independent predictive power.

**H2 (Supply-side):** Time-series shifts in $\hat{\nu}_t$ — holding firm-level $\hat{\mu}_{it}$ fixed — generate leverage changes in the direction predicted by the model. Aggregate capital supply distributional shifts are a new macro primitive for credit cycles.

**H3 (Structural fit):** A three-parameter structural model $\theta = (\alpha_\nu, \sigma_\nu, \kappa)$ estimated via SMM simultaneously fits the cross-sectional distribution of leverage and the cross-sectional distribution of credit spreads — with the same $\theta$.

---

## Theoretical Model

- **Model type:** Kantorovich linear program (optimal transport) for debt contracting
- **Key agents:** Continuum of firms with cash flow distributions $\{\mu_i\}$; aggregate capital supply distribution $\nu$; competitive lenders
- **Core mechanism:** The social planner minimizes expected deadweight bankruptcy costs over all joint distributions (couplings) of firm cash flows and promised payments. LP duality yields firm-specific contingent shadow prices. Under quadratic cost, Brenier's theorem delivers the optimal contract as the quantile coupling $D^*(X) = F_\nu^{-1}(F_\mu(X))$.
- **Main exact result:** Expected default shortfall at the individual optimal contract equals $W_1(\mu_i, \nu)/2$ — exact, no approximation.
- **Leverage result:** Equilibrium leverage $\lambda_i^*$ is strictly decreasing in $W_1(\mu_i, \nu)$ (under Assumptions 3.3 and 3.4 in the paper).
- **Aggregate welfare:** Social deadweight cost equals $W_2^2(\mu, \nu)$ at the planner's optimum.
- **Structural parameters to estimate:** $\theta = (\alpha_\nu, \sigma_\nu, \kappa)$ where $\nu \sim \text{LogNormal}(\alpha_\nu(t), \sigma_\nu^2)$ and $\kappa$ scales bankruptcy costs.

---

## Data

- **Primary datasets:**
  - **Compustat Quarterly** (`comp.fundq`, WRDS): firm cash flows, book assets, book debt — clean cash flow sample from 1988 (SFAS 95 boundary for `oancfy`)
  - **CRSP** (WRDS): market equity prices via CCM merge (`crsp.ccmxpf_lnkhist`, `linktype IN ('LC','LU','LS')`, `linkprim IN ('P','C')`)
  - **Mergent FISD** (`fisd.fisd_mergedissue`, WRDS): credit spreads at bond issuance — reliable from 1995; covers both investment-grade and high-yield

- **Key variables:**
  - *Firm cash flow distribution* $\hat{\mu}_{it}$: log-normal parameters $(\hat{\alpha}_{it}, \hat{\sigma}_{it})$ from 20-quarter rolling window MLE on quarterly `oancfy / atq` (baseline) and `(ibq + dpq) / atq` (robustness). Minimum 8 quarters for inclusion. Winsorize cash flows at 1%–99% by fiscal year before fitting.
  - *Capital supply distribution* $\hat{\nu}$: free parameters $(\alpha_\nu, \sigma_\nu)$ estimated entirely inside SMM — not pre-measured from external data (avoids circular identification from equilibrium allocations).
  - *Outcome — leverage*: book leverage `(dlttq + dlcq) / atq`; market leverage `(dlttq + dlcq) / (dlttq + dlcq + cshoq × prccq)`. Exclude observations with negative book equity (`ceqq < 0`).
  - *Outcome — spreads*: offering yield minus maturity-matched Treasury yield from Mergent FISD, in basis points. Used for $\kappa$ identification only (sample: bond-issuing firms, 1995–2024).
  - *Controls*: `log(atq)` (size), `(cshoq × prccq) / ceqq` (market-to-book), `oibdpq / atq` (profitability), `ppentq / atq` (tangibility), rolling standard deviation of cash flows (volatility)

- **Sample:** Firm-quarter observations, 1988–2024 for leverage panel; 1995–2024 for SMM spread moments. Exclude financials (SIC 6000–6999) and utilities (SIC 4900–4999) in baseline. Report results including them as robustness.

- **Sample period note:** The 1988–1994 data contributes to computing rolling $\hat{\mu}_{it}$ and the leverage panel but not to the spread-identified SMM moments (FISD coverage starts 1995).

- **Unit of observation:** Firm-quarter for panel regressions; firm-issuance for spread tests.

---

## Empirical Strategy

### Stage 1: Pre-estimation of $\hat{\mu}_{it}$ (outside SMM loop)

For each firm-quarter $(i,t)$ with at least 8 trailing quarterly observations:
1. Collect trailing 20-quarter operating cash flows scaled by assets
2. **Baseline:** `oancfy` differenced within fiscal year to get quarterly flows
3. **Robustness:** `ibq + dpq` (net income + depreciation) — available pre-1988, used as check
4. Fit log-normal via MLE: $(\hat{\alpha}_{it}, \hat{\sigma}_{it})$ — treated as data in all subsequent steps
5. Robustness: test log-normality via Kolmogorov-Smirnov per firm; report fraction of rejections

### Stage 2: SMM Estimation of $\theta = (\alpha_\nu, \sigma_\nu, \kappa)$

**Key design decision:** $\nu_t \sim \text{LogNormal}(\alpha_\nu, \sigma_\nu^2)$ is estimated as **free parameters inside SMM** — not pre-measured from external data. This avoids circular identification (bond deal sizes are equilibrium outcomes, not exogenous supply). The discipline comes entirely from the cross-equation restriction: the same $(\alpha_\nu, \sigma_\nu)$ must simultaneously fit both the leverage distribution moments and the spread distribution moments from two independent datasets (Compustat and Mergent FISD).

**Simulation:** Given $\theta$ and $\{\hat{\mu}_{it}\}$:
1. Construct $\nu(\theta) \sim \text{LogNormal}(\alpha_\nu, \sigma_\nu^2)$ — time-invariant baseline; time-varying extension adds $\alpha_\nu(t)$ indexed to aggregate credit conditions as robustness
2. Compute $W_1(\hat{\mu}_{it}, \nu(\theta))$ numerically for each firm-quarter (1D integral over quantile functions)
3. Solve participation constraint $G_i(\lambda; \theta) = 0$ numerically for model-implied $\hat{\lambda}_{it}^*(\theta)$
4. Compute model-implied spreads $\hat{s}_{it}(\theta) = \kappa \cdot W_1(\hat{\mu}_{it}, \nu(\theta)) / (2\mathbb{E}_{\nu(\theta)}[Y])$

**Moments targeted** (cross-equation restriction is the key identifying test):

| Moment | Data Source | Identifies |
|--------|-------------|-----------|
| Mean leverage by $W_1$ decile (10 moments) | Compustat/CRSP | $\alpha_\nu, \sigma_\nu$ jointly |
| Variance of leverage within $W_1$ decile (10 moments) | Compustat/CRSP | $\sigma_\nu$ |
| Mean spread by $W_1$ decile (10 moments) | Mergent FISD | $\kappa$ |
| Overall mean leverage | Compustat/CRSP | $\alpha_\nu$ level |
| Correlation of leverage with spreads across firms | Both | **Overidentifying restriction** |

**Key test:** The same $\hat{\theta}$ must simultaneously fit both leverage and spread moments drawn from independent datasets. Failure of the $J$-test (Hansen 1982) is evidence against the model.

**Standard errors:** Block bootstrap (500 replications, block = firm × year) to account for cross-equation correlation from common macro shocks. Covers first-stage uncertainty in $\hat{\mu}_{it}$ and cross-equation dependence between leverage and spread moments.

**SMM weighting matrix:** HAC-corrected (Newey-West) to handle serial correlation in moment conditions; block-structured across the two datasets to reflect their distinct sampling processes.

### Stage 3: Reduced-Form Validation

After structural estimation, validate the key mechanism with panel regressions:

$$L_{it} = \beta_0 + \beta_1 W_1(\hat{\mu}_{it}, \hat{\nu}_t) + \beta_2 \bar{X}_{it} + \beta_3 \hat{\sigma}_{it} + \gamma' \text{Controls}_{it} + \alpha_i + \alpha_t + \varepsilon_{it}$$

**Key test:** $\beta_1 < 0$ (higher distributional distance → lower leverage) and $\beta_1$ remains significant after conditioning on $\bar{X}_{it}$ and $\hat{\sigma}_{it}$ separately — meaning the shape component of $W_1$ beyond mean and variance has independent predictive power.

---

## Expected Results

- **Structural fit:** The three-parameter model fits the leverage distribution and spread distribution simultaneously with reasonable $\hat{\kappa}$ (expected range 10–30% of face value, consistent with existing structural estimates)
- **H1:** $W_1$ decile explains a substantial share of cross-sectional leverage variation beyond standard determinants; the shape component ($W_1$ residualized on mean and variance) is statistically significant
- **H2:** Quarters with compressed $\hat{\nu}_t$ (e.g., post-QE, pre-crisis) show lower $W_1$ for all firms and higher aggregate leverage, consistent with supply-side channel
- **H3:** Overidentification test passes ($p > 0.10$), confirming the model's cross-equation restriction

---

## Contribution

**vs. Leland (1994), Strebulaev (2007), Gomes-Schmid (2010):** Every existing structural capital structure model treats capital supply as a price (the risk-free rate). This paper introduces the distribution of capital supply $\nu$ as a new structural primitive — a first in the literature. The sufficient statistic for debt capacity shifts from scalar volatility $\sigma$ to the distributional distance $W_1(\mu_i, \nu)$. Two firms with identical volatility but different distributional shapes relative to capital supply have different debt capacity.

**vs. reduced-form leverage literature (Frank-Goyal 2009, Rajan-Zingales 1995):** Provides a structural microfoundation for why supply-side conditions affect leverage, with exact welfare implications ($W_2^2(\mu, \nu)$ as aggregate deadweight cost).

**vs. financial intermediation literature:** Formalizes the welfare role of intermediaries as distributionally transforming $\nu$ to reduce $W_2^2(\mu, \nu)$ — a new channel distinct from liquidity provision or information production.

---

## Open Questions

1. **Dynamic extension:** The model is static. A dynamic version with $\nu_t$ evolving stochastically would generate debt issuance timing predictions. Left for future work.
2. **Non-log-normal $\mu_{it}$:** Robustness of rolling window estimation to departures from log-normality. Consider gamma or empirical CDF as alternatives.
3. **Measurement of $\nu_t$:** The appropriate empirical counterpart to aggregate capital supply is debated. Candidates: Flow of Funds credit instruments, syndicated loan issuance distribution, bond market issuance distribution. Needs sensitivity analysis.
4. **Endogeneity of $\hat{\mu}_{it}$:** Firms may adjust investment to change their cash flow distribution in response to credit conditions. Lagging $\hat{\mu}_{it}$ by one year partially addresses this.
5. **Finance intuition in the paper:** The existing draft (old/main.tex) presents the mathematics without sufficient economic motivation. The introduction and model sections need a full rewrite with finance-first framing before submission.

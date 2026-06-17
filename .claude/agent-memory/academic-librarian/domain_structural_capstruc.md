---
name: structural-capital-structure-estimation
description: SMM estimation papers, moment conditions, and data sources for structural capital structure research
metadata:
  type: reference
---

## Core Structural Capital Structure Papers

| Paper | Method | Key moments | Data |
|-------|--------|-------------|------|
| Hennessy-Whited (JF 2005) | Dynamic programming + calibration | Leverage, investment/K, dividends | Compustat 1980–2000 |
| Hennessy-Whited (JF 2007) | SMM | Leverage, investment, cash, payout | Compustat 1988–2003 |
| Strebulaev (JF 2007) | Dynamic trade-off + simulation | Leverage-profitability correlation | Compustat calibration |
| Nikolov-Whited (JF 2014) | SMM | Leverage, cash, dividends, investment | Compustat 1980–2008 |
| Morellec-Nikolov-Schuerhoff (JF 2012) | SMM | Leverage, investment, dividends | Compustat + governance data 1990–2008 |

## Typical SMM Moment Conditions for Capital Structure

- Mean leverage ratio (book and market)
- Standard deviation of leverage
- Mean profitability
- Serial correlation of leverage
- Investment-to-capital ratio
- Dividend payout ratio
- Cash-to-assets ratio

## Standard Datasets

- **Compustat (Fundamentals Annual):** Primary source; US public firms; standard SIC 2000–3999 (manufacturing) subsample commonly used
- **CRSP:** Returns data; needed for market leverage calculation
- **DealScan:** Loan-level covenant terms and credit spreads
- **Mergent FISD:** Bond issuance data
- **Morningstar/CRSP Mutual Fund:** Fund holdings for capital supply identification

## Journal Norms for This Literature

- JF, RFS, JFE all publish structural capital structure papers
- SMM papers typically use 8–15 moments; standard errors via parametric bootstrap
- Model fit assessed by comparing targeted and non-targeted moments

**How to apply:** When estimating the Wasserstein-distance capital structure model, match the moment conditions above plus add the empirical Wasserstein distance W1_hat(μ_i, ν_t) as an additional targeted moment. Hennessy-Whited (2007) is the closest methodological template.

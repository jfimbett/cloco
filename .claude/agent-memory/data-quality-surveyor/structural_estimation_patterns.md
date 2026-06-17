---
name: structural-estimation-patterns
description: Recurring identification and measurement issues in SMM/GMM structural estimation papers in corporate finance
metadata:
  type: feedback
---

## Recurring Issues in Structural Estimation Data Assessments

### 1. Common-Shock Contamination in SMM Moment Conditions
SMM papers targeting multiple moment groups (e.g., leverage moments + spread moments) frequently treat data sources as independent when they share macro shocks. The efficient GMM weighting matrix is not block-diagonal when common factors drive both sets of moments. Assessments must explicitly ask: are the moment condition errors correlated across equations? If yes, standard errors under block-diagonal W will be understated.

**Why:** Seen in distributional debt capacity paper where ν_t (parameterized from FRED aggregates) was simultaneously correlated with both the leverage panel and the spread panel.

**How to apply:** For any SMM paper with cross-equation restrictions, require the assessment to discuss whether moment condition errors are orthogonal across equations. If not, require proposal for block-structured weighting or HAC correction.

### 2. Equilibrium Outcomes Misidentified as Supply Primitives
In structural papers with supply-demand frameworks, assessments routinely propose using equilibrium transaction data (deal sizes, issuance volumes) as proxies for supply-side primitives (lender capacity, capital supply distributions). This is circular: the equilibrium allocation is an output of the model, not an input. Any ν_t measured from equilibrium outcomes (bond deal sizes, loan volumes) reflects both supply and demand — it cannot identify a pure supply primitive without additional exclusion restrictions.

**Why:** Bond deal size distribution from Mergent FISD was recommended as proxy for ν_t in distributional debt capacity paper.

**How to apply:** When a structural paper's theory has a supply primitive, ask explicitly: is the proposed empirical measure a supply-only object or a joint supply-demand equilibrium outcome? If the latter, demand a theoretical argument for why the equilibrium object recovers the supply primitive.

### 3. Sample Mismatch Between Identification and Estimation Population
SMM papers frequently identify structural parameters from a subset of the full sample (e.g., bond-issuing firms for credit spread moments) and then apply those parameters to the full sample (all Compustat firms for leverage moments). If the identifying subset is systematically different from the full sample on dimensions related to the structural parameter (e.g., bankruptcy costs for rated vs. unrated firms), the estimate is biased for the full population.

**Why:** κ (bankruptcy cost) was identified from Mergent FISD bond issuers (large, rated firms) but applied to all Compustat firms in the leverage panel.

**How to apply:** Always check whether the identifying sample (observations that contribute to parameter-specific moments) and the estimation sample (observations used for model fit) are the same population. If not, require discussion of generalizability.

### 4. Rolling Window Creates Non-Random Sample Attrition
Any paper using rolling window pre-estimation (MLE of distributional parameters, rolling betas, etc.) excludes firms with insufficient history or data gaps. This attrition is non-random: IPO firms, restructuring firms, and firms with restatements are disproportionately excluded. These excluded firms tend to be exactly the theoretically interesting cases (high leverage change, high uncertainty). Always require an analysis of excluded vs. included firm characteristics.

### 5. Sample Start Date Misdescribed When Multiple Data Constraints Apply
Papers with multiple data sources often describe the sample as starting at the earliest available date for any single component, when the effectively identified sample starts at the latest binding constraint across all moment conditions. Always trace through: what is the earliest date at which ALL required moment conditions can be computed simultaneously?

**Why:** Distributional debt capacity paper described sample as 1988 Q1 — 2024 Q4 but the SMM requires credit spreads (1995+), so the fully identified model cannot begin before 1995.

---
name: Referee calibration notes
description: Calibration benchmarks and recurring issues from peer reviews of finance/economics papers
type: feedback
---

## JF/RFS Bar for Empirical Papers
- Descriptive facts alone are insufficient; need either clean causal identification or estimated structural model
- Unconditional regressions without FE are never the main spec at a top journal
- Low R-squared in hedonic regressions must be acknowledged and contextualized
- Cross-sectional comparisons across categories must address confounders beyond the focal mechanism

## Recurring Issues in Alternative Assets Papers
- Survivorship/selection bias: which items reach auction and when is endogenous
- Supply-side timing: sellers anticipate price patterns, making observed trough an equilibrium outcome
- Maturity/quality endogeneity: quality ratings correlate with both prices and maturity windows
- External validity: results from one asset class (wine, art) must be framed as general durable-goods insights

## Data Construction Red Flags
- Imputation models dominated by a single feature effectively collapse the imputed variable into that feature
- Maturity caps that bind for >90% of observations eliminate cross-sectional variation
- Target encoding without leave-one-out introduces small upward bias in CV metrics

## Scoring Calibration
- 90+ = genuinely strong, ready to accept or nearly so
- 70-79 = real potential but significant work remains (major revisions)
- 60-69 = multiple fundamental issues but salvageable with substantial revision
- <50 = fatal flaws in identification or data
- Incomplete papers (missing sections, placeholder proofs) cannot score above ~65 regardless of idea quality

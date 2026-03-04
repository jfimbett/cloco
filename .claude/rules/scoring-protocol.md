# Scoring Protocol (Rule 9)

**How individual agent scores aggregate into the overall project score.**

## Weighted Aggregation

The overall project score that gates submission (>= 95) is a weighted aggregate:

| Component | Weight | Source Agent |
|-----------|--------|-------------|
| Literature coverage | 10% | academic-editor's score of academic-librarian |
| Data quality | 10% | data-quality-surveyor's score of explorer |
| Identification validity | 25% | identification-critic's score of causal-strategist |
| Code quality | 15% | debugger's score of Coder (main Claude) |
| Paper quality | 25% | Average of blind-peer-referee instance 1 + instance 2 scores |
| Manuscript polish | 10% | academic-proofreader's score of economics-paper-writer |
| Replication readiness | 5% | replication-verifier pass/fail (0 or 100) |

## Minimum Per Component

No component can be below 80 for submission. A perfect literature review can't compensate for broken identification.

## Score Sources

- Each critic produces a score from 0 to 100 based on its deduction table
- Scores start at 100 and deduct for issues found
- The replication-verifier is pass/fail (mapped to 0 or 100)
- blind-peer-referee scores are averaged: `(Referee_1 + Referee_2) / 2`

## Gate Thresholds

| Gate | Overall Score | Per-Component Minimum | Action |
|------|--------------|----------------------|--------|
| Commit | >= 80 | None enforced | Allowed |
| PR | >= 90 | None enforced | Allowed |
| Submission | >= 95 | >= 80 per component | Allowed |
| Below 80 | < 80 | — | Blocked |

## Type-Specific Scoring Weights

The orchestrator reads `project_type` from the research spec and applies the matching weight table. Missing components are excluded and remaining weights renormalized.

| Component | Source Agent | Empirical | Theory | Structural | Empirical+Theory |
|-----------|-------------|-----------|--------|------------|-----------------|
| Literature coverage | academic-editor | 10% | 15% | 10% | 10% |
| Data quality | data-quality-surveyor | 10% | — | 10% | 10% |
| Theory model | theory-critic | — | 40% | 15% | 10% |
| Identification validity | identification-critic | 25% | — | — | 20% |
| Structural estimation | structural-critic | — | — | 20% | — |
| Code quality | debugger | 15% | — | 15% | 15% |
| Paper quality | blind-peer-referee avg | 25% | 30% | 20% | 25% |
| Manuscript polish | academic-proofreader | 10% | 15% | 5% | 5% |
| Replication readiness | replication-verifier | 5% | — | 5% | 5% |
| **Total** | | **100%** | **100%** | **100%** | **100%** |

The default table (all components, empirical weights) is shown above. The orchestrator selects the column matching `project_type` from the research spec.

## When Components Are Missing

Not every project uses all components. If a component hasn't been scored:
- It's excluded from the weighted average
- Remaining weights are renormalized
- Example: no literature review → weights become 11%, 28%, 17%, 28%, 11%, 6%

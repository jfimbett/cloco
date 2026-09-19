# Quality Report — [branch-name] — YYYY-MM-DD

**Merge:** [branch] → [main]
**Project type:** [empirical / theory / structural / empirical+theory]

## Aggregate
**Weighted score:** XX/100   **Gate:** [Commit ≥80 / PR ≥90 / Submission ≥95]

| Component | Critic | Score | Weight | Weighted |
|-----------|--------|-------|--------|----------|
| Literature coverage | academic-editor | | | |
| Data quality | data-quality-surveyor | | | |
| Theory model | theory-critic | | | |
| Identification validity | identification-critic | | | |
| Structural estimation | structural-critic | | | |
| Code quality | debugger | | | |
| Paper quality | blind-peer-referee (avg) | | | |
| Manuscript polish | academic-proofreader | | | |
| Replication readiness | replication-verifier | PASS/FAIL | | |

Missing components excluded; weights renormalised (see `scoring-protocol.md`).

## Blocking issues (score < 80 components)
- …

## Recommendations (non-blocking)
- …

## Verification
- [ ] `latexmk -pdf -cd paper/main.tex` compiles
- [ ] All scripts run end-to-end
- [ ] Outputs fresher than inputs

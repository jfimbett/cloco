# Adversarial Pairing (Rule 1)

**Every worker agent has a paired critic. The research-orchestrator never dispatches a creator without scheduling its critic.**

## Worker-Critic Pairs

| Worker (Creator) | Critic (Reviewer) | What's Reviewed |
|-----------------|-------------------|-----------------|
| academic-librarian | academic-editor | Literature coverage, gaps, recency |
| explorer | data-quality-surveyor | Data feasibility, quality, identification fit |
| causal-strategist | identification-critic | Identification validity, assumptions, robustness |
| econ-finance-theorist | theory-critic | Theoretical model validity, equilibrium correctness |
| structural-estimation-expert | structural-critic | Structural model design, estimation validity |
| Coder (main Claude instance) | debugger | Code quality, reproducibility, code-strategy alignment |
| economics-paper-writer | academic-proofreader | Manuscript polish, LaTeX quality, hedging |

## Peer Review (Special Case)

Peer Review uses a different structure — the academic-editor dispatches two independent blind-peer-referee instances:

1. academic-editor assigns the paper to blind-peer-referee instance 1 and instance 2 (blind, independent)
2. Both referees produce scored reports
3. academic-editor synthesizes a decision: Accept / Minor Revisions / Major Revisions / Reject

## Enforcement

- The research-orchestrator checks: if a creator artifact exists without a critic score, it is **not approved**
- No artifact advances to the next phase without its critic's score >= 80
- Critics produce scores; creators produce artifacts — never the reverse

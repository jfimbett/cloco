# Three Strikes Escalation (Rule 7)

**If a worker-critic pair fails to converge after 3 rounds, the research-orchestrator escalates.**

## The Protocol

```
Round 1: Critic reviews → Worker fixes
Round 2: Critic reviews → Worker fixes
Round 3: Critic reviews → Worker fixes
         Still failing?
              ↓
         ESCALATION
```

## Escalation Routing

| Pair | Escalation Target | What Happens |
|------|-------------------|--------------|
| Coder (main Claude) + debugger | econometrics-critic | Re-evaluates whether the strategy memo is implementable |
| economics-paper-writer + academic-proofreader | academic-editor | Structural rewrite, not just polish |
| causal-strategist + identification-critic | User | Fundamental design question — needs human judgment |
| econ-finance-theorist + theory-critic | User | Theoretical design deadlock — needs human judgment |
| structural-estimation-expert + structural-critic | User | Structural model deadlock — needs human judgment |
| academic-librarian + academic-editor | User | Scope disagreement — user decides breadth vs depth |
| explorer + data-quality-surveyor | User | Data feasibility deadlock — user decides resource trade-offs |

## Rules

- **Max 3 rounds per pair per invocation** — no infinite loops
- **Escalation is logged** in the research journal with strike count
- **User escalation requires a clear question** — not "they disagree," but "[critic] requires X, which contradicts Y. Which takes priority?"
- **Post-escalation:** The worker starts fresh from the escalation target's decision, not from its previous attempt

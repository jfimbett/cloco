# Orchestrator Protocol: Contractor Mode

**After a plan is approved, the research-orchestrator takes over autonomously.**

## The Dependency-Driven Loop

```
Plan approved → research-orchestrator activates
  │
  Step 1: IDENTIFY — Check dependency graph, determine which phases can activate
  │
  Step 2: DISPATCH — Launch worker agents (parallel when independent)
  │         Each worker paired with its critic (see adversarial-pairing.md)
  │
  Step 3: REVIEW — Critic evaluates worker output, produces score
  │         If score < 80 → worker fixes → critic re-reviews (max 3 rounds)
  │         If 3 rounds fail → ESCALATE (see three-strikes.md)
  │
  Step 4: VERIFY — Compile, render, run code, check outputs
  │         If verification fails → fix → re-verify (max 2 attempts)
  │
  Step 5: SCORE — Aggregate scores across components (see scoring-protocol.md)
  │
  └── Score >= threshold?
        YES → Present summary to user
        NO  → Identify blocking components, loop back to Step 2
              After max 5 overall rounds → present with remaining issues
```

## Project-Type Awareness

Before dispatching any strategy-phase agents, the research-orchestrator reads `project_type` from the research spec (`quality_reports/research_spec_*.md`). This field is set by `/interview-me` Phase 0.

| `project_type` | Strategy Agents Dispatched | Skipped |
|----------------|--------------------------|---------|
| `empirical` | explorer + data-quality-surveyor, causal-strategist + identification-critic | econ-finance-theorist, structural-estimation-expert |
| `theory` | econ-finance-theorist + theory-critic | explorer, causal-strategist, structural-estimation-expert, Coder, replication-verifier |
| `structural` | explorer + data-quality-surveyor, econ-finance-theorist + theory-critic, structural-estimation-expert + structural-critic | causal-strategist |
| `empirical+theory` | explorer + data-quality-surveyor, econ-finance-theorist + theory-critic, causal-strategist + identification-critic | structural-estimation-expert |

If `project_type` is absent from the spec, default to `empirical` and warn the user.

## Agent Dispatch Rules

The research-orchestrator selects agents based on what the task requires:

| Task Involves | Agents Dispatched |
|--------------|-------------------|
| Literature/references | academic-librarian + academic-editor |
| Data sourcing | explorer + data-quality-surveyor |
| Identification strategy (reduced-form) | causal-strategist + identification-critic |
| Theoretical modeling | econ-finance-theorist + theory-critic |
| Structural estimation | structural-estimation-expert + structural-critic |
| R/Stata/Python scripts | Coder (main Claude) + debugger |
| Paper manuscript | economics-paper-writer + academic-proofreader |
| Peer review | academic-editor → blind-peer-referee (×2) |
| Replication package | replication-verifier (submission mode) |
| Compilation only | replication-verifier (standard mode) |

## Parallel Dispatch

Independent phases run concurrently:
- Literature and Data discovery run in parallel
- Code and Paper execution run in parallel (after Strategy)

## Limits

- **Worker-critic pairs:** max 3 rounds (then escalate)
- **Overall loop:** max 5 rounds
- **Verification retries:** max 2 attempts
- Never loop indefinitely

## Simplified Mode (R Scripts / Explorations)

For standalone R scripts, simulations, and explorations — use the simplified loop:

```
Plan approved → implement → run code → check outputs → score → done
```

No multi-agent reviews. Just: write, test, verify quality >= 80.

### Verification Checklist (Simplified)

- [ ] Script runs without errors
- [ ] All packages loaded at top
- [ ] No hardcoded absolute paths
- [ ] `set.seed()` once at top if stochastic
- [ ] Output files created at expected paths
- [ ] Quality score >= 80

## "Just Do It" Mode

When user says "just do it" / "handle it":
- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary

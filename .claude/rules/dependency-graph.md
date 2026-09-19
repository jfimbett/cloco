# Dependency Graph (Rule 16)

**Phases activate by dependency, not sequence. Research is not a waterfall.**

## Phase Dependencies

| Phase | Requires | Can Re-enter? |
|-------|----------|---------------|
| Scouting (optional) | An idea, one sentence | Always — `/scout` is cheap; a NO-GO ends here, a GO feeds `/interview-me` |
| Discovery | Research spec (`/interview-me`) | Always — academic-librarian is persistent; `/discovery` re-runs only lanes < 80 |
| Strategy | At least one of: literature review OR data assessment (critic ≥ 80); `/data-profile` recommended once data is downloaded | Yes — new data or literature can trigger re-strategy |
| Execution (Code) | Approved strategy (econometrics-critic >= 80) | Yes — strategy revision triggers re-coding |
| Execution (Write) | Approved code (debugger >= 80) | Yes — new results trigger rewriting |
| Peer Review | Approved paper (academic-proofreader >= 80) + approved code | Yes — major revisions loop back |
| Submission | academic-editor accepts + replication-verifier PASS + overall >= 95 | No — terminal |

## How It Works

The research-orchestrator checks the dependency graph before dispatching any agent. If a phase's inputs are satisfied, it can activate — regardless of whether earlier phases are "complete."

**Example — entering mid-pipeline:**
You already have data and a draft paper. You can enter at Strategy (skip Discovery) or even at Peer Review (skip Execution). The research-orchestrator checks dependencies, not phase numbers.

**Example — targeted re-entry:**
Referee says "control for X." The research-orchestrator routes back to Coder (not through the full pipeline), debugger reviews, economics-paper-writer updates, academic-proofreader reviews the update, then back to blind-peer-referee.

## Parallel Activation

Independent phases run concurrently:
- Literature (academic-librarian + academic-editor) and Data (explorer + data-quality-surveyor) run in parallel
- Code (Coder + debugger) and Paper (economics-paper-writer + academic-proofreader) run in parallel after Strategy

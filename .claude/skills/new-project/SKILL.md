---
name: new-project
description: Full research pipeline from idea to paper. Orchestrates all phases — interview, literature review, data discovery, identification strategy, analysis, paper drafting, and peer review. Use when starting a new research project from scratch.
disable-model-invocation: true
argument-hint: "[research topic or 'interactive' for guided start]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task", "WebSearch", "WebFetch"]
---

# New Project

Launch a full research pipeline from idea to paper, orchestrated through the dependency graph.

**Input:** `$ARGUMENTS` — a research topic or `interactive` for a guided start via `/interview-me`.

---

## Pipeline Overview

This skill orchestrates the full v3 dependency graph. Each phase activates when its dependencies are met. The orchestrator manages agent dispatch, three-strikes escalation, and quality gates.

```
Phase 0: Scouting (optional, cheap)
  └── /scout → go/no-go verdict (idea-critic)

Phase 1: Discovery
  ├── /interview-me → Research Spec + Domain Profile
  └── /discovery → /lit-review ∥ /find-data with critic loops + bib merge

Phase 2: Strategy (depends on Phase 1)
  ├── /find-data → Data Assessment
  └── /identify → Strategy Memo + Robustness Plan

Phase 3: Execution (depends on Phase 2)
  ├── /data-analysis → Scripts + Tables + Figures
  └── /draft-paper → Paper Sections

Phase 4: Peer Review (depends on Phase 3)
  ├── /review-paper → Referee Reports + Editorial Decision
  └── /paper-excellence → Aggregate Score

Phase 5: Submission (depends on Phase 4, score >= 95)
  ├── /target-journal → Journal Recommendations
  ├── /data-deposit → Replication Package
  └── /submit → Final Verification
```

---

## Workflow

### Step 1: Discovery Phase

1. **If `interactive` or no research spec exists:**
   Run `/interview-me` to produce:
   - Research specification (`quality_reports/research_spec_*.md`)
   - Domain profile (`.claude/rules/domain-profile.md`) — if still template
   Then run `/setup-project`: the checkout now holds a project and must leave the template identity — folder `cloco-<slug>`, its own GitHub repository (private/public), template kept as remote `template`. Pushes to the template are blocked until this is done.

2. **Run `/discovery`** (reads the spec, runs `/lit-review` and — unless `project_type` is `theory` — `/find-data` in parallel, each with its critic loop, merges BibTeX into `paper/references.bib`, writes `quality_reports/discovery_report_*.md`).

**Gate:** Research spec exists and the Discovery Report says Strategy is unlocked (at least one lane ≥ 80).

*If the user has not committed to the idea yet,* run `/scout [topic]` first; only proceed to the interview on a GO verdict.

### Step 2: Strategy Phase (project-type branching)

Read `project_type` from the research spec produced in Step 1, then follow the matching path:

| `project_type` | Skills to Run | Skills to Skip |
|----------------|--------------|----------------|
| `empirical` | `/data-profile` → `/identify` | `/theory-model`, `/structural-estimation` |
| `theory` | `/theory-model` | `/find-data`, `/identify`, `/data-analysis`, `/structural-estimation` |
| `structural` | `/data-profile` → `/theory-model` → `/structural-estimation` | `/identify` |
| `empirical+theory` | `/data-profile` → `/theory-model` → `/identify` | `/structural-estimation` |

**Branching logic:**

- **`empirical`:**
  3. (Data lane already done by `/discovery`; once data is downloaded run `/data-profile` to verify panel/treatment structure)
  4. Run `/identify` — causal-strategist + identification-critic
  **Gate:** Strategy memo score >= 80

- **`theory`:**
  3. Run `/theory-model` — econ-finance-theorist + theory-critic
  **Gate:** Theory model score >= 80. Skip to Step 3b (paper drafting only).

- **`structural`:**
  3. (Data lane already done by `/discovery`; run `/data-profile` once data is in hand)
  4. Run `/theory-model` — econ-finance-theorist + theory-critic
  5. Run `/structural-estimation` — structural-estimation-expert + structural-critic + debugger
  **Gate:** All three scores >= 80

- **`empirical+theory`:**
  3. (Data lane already done by `/discovery`; run `/data-profile` once data is in hand)
  4. Run `/theory-model` — econ-finance-theorist + theory-critic (theory predictions drive empirical design)
  5. Run `/identify` — causal-strategist + identification-critic
  **Gate:** Theory model and strategy memo both >= 80

### Step 3: Execution Phase

**3a. Code (skip for `theory`):**
Run `/data-analysis` — Coder writes scripts, Debugger reviews code.

**3b. Paper (all types):**
Run `/draft-paper` — Writer drafts sections, Humanizer pass strips AI patterns.

**Gate:** Code must pass Debugger review (if applicable). Paper sections must exist.

### Step 4: Peer Review Phase

7. **Run `/paper-excellence`** for comprehensive review:
   - econometrics-critic + debugger + academic-proofreader + replication-verifier in parallel
   - Weighted aggregate score computed

8. **Run `/review-paper`** for simulated peer review:
   - 2 blind Referees + Editor

**Gate:** Aggregate score >= 80 (commit-ready). Score >= 90 for submission.

### Step 5: Submission Phase (optional, user-triggered)

9. **Run `/target-journal`** for journal recommendations
10. **Run `/data-deposit`** for replication package
11. **Run `/submit`** for final verification

---

## User Interaction Points

The pipeline pauses for user input at these points:
- After interview (approve research spec)
- After strategy memo (approve identification strategy)
- After data analysis (review results before paper drafting)
- After peer review (review feedback before revision)
- Before submission (approve journal choice)

Between pauses, the orchestrator runs autonomously per `orchestrator-protocol.md`.

---

## Principles

- **This is always orchestrated.** Unlike other skills, `/new-project` always runs through the full pipeline.
- **Dependency-driven.** Phases activate by dependency, not forced sequence.
- **Quality-gated.** Each phase transition requires passing quality checks.
- **User retains control.** Pipeline pauses at key decision points.
- **Resumable.** If interrupted, the pipeline resumes from the last completed phase.

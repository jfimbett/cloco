---
name: pipeline-status
description: |
  Show the current research pipeline status for the active project, or display
  the pipeline guide for a specific project type. Reads the research spec,
  research journal, and active plans to determine phase, scores, and next steps.
author: Claude Code Academic Workflow
version: 1.0.0
argument-hint: "[optional: empirical | theory | structural | empirical+theory]"
allowed-tools: ["Read", "Glob", "Bash"]
---

# /pipeline-status — Research Pipeline Dashboard

Show where you are in the cloco research pipeline, with phase statuses, scores,
and the next command to run.

**Usage:**
- `/pipeline-status` — dashboard for active project (or Getting Started if none)
- `/pipeline-status empirical` — pipeline guide for empirical projects
- `/pipeline-status theory` — pipeline guide for theory projects
- `/pipeline-status structural` — pipeline guide for structural projects
- `/pipeline-status empirical+theory` — pipeline guide for combined projects

---

## Step 1: Determine Mode

Check `$ARGUMENTS`:
- If `$ARGUMENTS` is non-empty and matches one of `empirical`, `theory`,
  `structural`, `empirical+theory` → **Mode C** (static type guide)
- Otherwise → look for a research spec to choose Mode A or B

## Step 2 (Modes A & B): Find Research Spec

```bash
ls quality_reports/research_spec_*.md 2>/dev/null | head -1
```

- If found → **Mode A** (full dashboard)
- If not found → **Mode B** (Getting Started)

---

## Mode A — Full Dashboard (active project)

### Data Collection

**2a. Read the research spec:**
```bash
cat quality_reports/research_spec_*.md 2>/dev/null | head -60
```
Extract: `project_name`, `project_type` (empirical/theory/structural/empirical+theory).
If `project_type` is absent, default to `empirical`.

**2b. Read the research journal:**
```bash
cat quality_reports/research_journal.md 2>/dev/null
```
Parse all entries for `**Phase:**` and `**Score:**` fields.
Group by phase. A component is "done" when its score >= 80.
The last entry gives the `last_action` summary (agent + score).

**2c. Find the active plan:**
```bash
ls -lt .claude/plans/*.md 2>/dev/null | head -1
```

### Phase Detection Algorithm

Phases (in order): Discovery → Strategy → Execution → Peer Review → Submission

A phase is **done** when ALL its required components for the project type are done (score >= 80).

| Phase | Empirical components | Theory components | Structural components | Empirical+Theory components |
|-------|---------------------|------------------|----------------------|--------------------------|
| Discovery | Literature (academic-librarian) + Data (explorer) | Literature only | Literature + Data | Literature + Data |
| Strategy | Causal strategy (causal-strategist) | Theory model (econ-finance-theorist) | Structural model (structural-estimation-expert) | Theory model + Causal strategy |
| Execution | Code (Coder/debugger) + Paper draft | Paper draft only | Code + Paper draft | Code + Paper draft |
| Peer Review | blind-peer-referee (avg >= 80) | blind-peer-referee (avg >= 80) | blind-peer-referee (avg >= 80) | blind-peer-referee (avg >= 80) |
| Submission | replication-verifier PASS + overall >= 95 | overall >= 95 | replication-verifier PASS + overall >= 95 | replication-verifier PASS + overall >= 95 |

**Current phase = first phase that is NOT done.**
If all phases done → current phase = Submission (completed).

### Overall Score Calculation

Compute the weighted aggregate using components that have scores.
Weights by project type (from scoring-protocol.md):

| Component | Empirical | Theory | Structural | Empirical+Theory |
|-----------|-----------|--------|------------|-----------------|
| Literature | 10% | 15% | 10% | 10% |
| Data quality | 10% | — | 10% | 10% |
| Theory model | — | 40% | 15% | 10% |
| Identification | 25% | — | — | 20% |
| Structural estimation | — | — | 20% | — |
| Code quality | 15% | — | 15% | 15% |
| Paper quality (avg referees) | 25% | 30% | 20% | 25% |
| Manuscript polish | 10% | 15% | 5% | 5% |
| Replication | 5% | — | 5% | 5% |

Renormalize if components are missing (no score yet).

### Next Skill Command

| Current Phase | Empirical | Theory | Structural | Empirical+Theory |
|--------------|-----------|--------|------------|-----------------|
| Discovery | `/lit-review [topic]` | `/lit-review [topic]` | `/lit-review [topic]` | `/lit-review [topic]` |
| Strategy | `/identify [question]` | `/theory-model [topic]` | `/theory-model [topic]` | `/theory-model [topic]` |
| Execution | `/data-analysis [dataset]` | `/draft-paper [section]` | `/data-analysis [dataset]` | `/data-analysis [dataset]` |
| Peer Review | `/review-paper [file]` | `/review-paper [file]` | `/review-paper [file]` | `/review-paper [file]` |
| Submission | `/submit [journal]` | `/submit [journal]` | `/submit [journal]` | `/submit [journal]` |

### Dashboard Output

Print this ASCII dashboard (adapt to actual data):

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO RESEARCH PIPELINE STATUS                       ║
╠══════════════════════════════════════════════════════════════╣
║  Project:   [project_name]                                   ║
║  Type:      [project_type]                   Phase N of 5    ║
╠══════════════════════════════════════════════════════════════╣
║  PIPELINE                                                    ║
║                                                              ║
║  [✅|▶|○]  1 · Discovery                                     ║
║      ├─ Literature review     academic-librarian   XX/100    ║
║      └─ Data discovery        explorer             XX/100    ║
║                                                              ║
║  [✅|▶|○]  2 · Strategy              [← YOU ARE HERE]        ║
║      ├─ [strategy component]                  [status]       ║
║      └─ Econometrics review               [status]           ║
║                                                              ║
║  [✅|▶|○]  3 · Execution                      [locked?]      ║
║      ├─ Code analysis         debugger         [score]       ║
║      └─ Paper draft           proofreader      [score]       ║
║                                                              ║
║  [✅|▶|○]  4 · Peer Review                    [locked?]      ║
║      └─ Blind peer review     referee avg      [score]       ║
║                                                              ║
║  [✅|▶|○]  5 · Submission                     [locked?]      ║
║      └─ Replication package   verifier         [PASS/FAIL]   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  LAST ACTION                                                 ║
║  [last journal entry summary — agent, score, date]           ║
╠══════════════════════════════════════════════════════════════╣
║  NEXT STEP                                                   ║
║  → /[skill] [hint]                                           ║
║    Runs: [agents dispatched]                                 ║
║    Required: 80/100 to unlock [next phase]                   ║
╠══════════════════════════════════════════════════════════════╣
║  QUALITY GATES                                               ║
║  Commit ≥80: [✅|○]   PR ≥90: [✅|○]   Submit ≥95: [✅|○]  ║
║  Overall score: [XX/100 or N/A]                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Phase icons:** ✅ = done (all components >= 80), ▶ = current, ○ = locked
**Component status:** show score (e.g. `87/100`) or `not started` or `in progress`

---

## Mode B — Getting Started (no project found)

Print this banner:

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO — GETTING STARTED                              ║
╠══════════════════════════════════════════════════════════════╣
║  No active research project found.                           ║
║                                                              ║
║  Start a project:                                            ║
║    /new-project [topic]    Full pipeline: idea → paper       ║
║    /interview-me [topic]   Interview → research spec         ║
║                                                              ║
║  Or jump to a standalone task:                               ║
║    /lit-review [topic]     Literature search                 ║
║    /find-data [question]   Data discovery                    ║
║    /draft-paper [section]  Write paper sections              ║
║    /review-code [file]     Code quality audit                ║
║    /proofread [file]       Manuscript review                 ║
║    /review-paper [file]    Simulated peer review             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Mode C — Static Pipeline Guide (type argument provided)

### Empirical (`/pipeline-status empirical`)

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO PIPELINE GUIDE — EMPIRICAL PROJECT             ║
╠══════════════════════════════════════════════════════════════╣
║  Phase 1 · Discovery                                         ║
║    /interview-me [topic]   → Research spec + project_type    ║
║    /lit-review [topic]     → academic-librarian + editor     ║
║    /find-data [question]   → explorer + data-quality-surveyor║
║                                                              ║
║  Phase 2 · Strategy                                          ║
║    /identify [question]                          ║
║                            → causal-strategist + critic      ║
║    Required: 80/100 to advance  (weight: 25% of score)       ║
║                                                              ║
║  Phase 3 · Execution                                         ║
║    /data-analysis [dataset] → Coder + debugger              ║
║    /draft-paper [section]   → economics-paper-writer         ║
║    /proofread [file]         → academic-proofreader          ║
║                                                              ║
║  Phase 4 · Peer Review                                       ║
║    /review-paper [file]    → 2× blind-peer-referee           ║
║                                                              ║
║  Phase 5 · Submission                                        ║
║    /target-journal [paper] → journal selection               ║
║    /audit-replication [dir]→ replication-verifier            ║
║    /submit [journal]       → final gate ≥95                  ║
╠══════════════════════════════════════════════════════════════╣
║  Scoring weights: Identification 25%, Paper 25%, Code 15%,  ║
║  Lit 10%, Data 10%, Polish 10%, Replication 5%               ║
╚══════════════════════════════════════════════════════════════╝
```

### Theory (`/pipeline-status theory`)

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO PIPELINE GUIDE — THEORY PROJECT                ║
╠══════════════════════════════════════════════════════════════╣
║  Phase 1 · Discovery                                         ║
║    /interview-me [topic]   → Research spec + project_type    ║
║    /lit-review [topic]     → academic-librarian + editor     ║
║                                                              ║
║  Phase 2 · Strategy                                          ║
║    /theory-model [topic]   → econ-finance-theorist + critic  ║
║    Required: 80/100 to advance  (weight: 40% of score)       ║
║                                                              ║
║  Phase 3 · Execution                                         ║
║    /draft-paper [section]  → economics-paper-writer          ║
║    /proofread [file]       → academic-proofreader            ║
║                                                              ║
║  Phase 4 · Peer Review                                       ║
║    /review-paper [file]    → 2× blind-peer-referee           ║
║                                                              ║
║  Phase 5 · Submission                                        ║
║    /target-journal [paper] → journal selection               ║
║    /submit [journal]       → final gate ≥95                  ║
╠══════════════════════════════════════════════════════════════╣
║  NOTE: Theory projects skip data, code, and replication.    ║
║  Scoring weights: Theory model 40%, Paper 30%, Lit 15%,     ║
║  Manuscript polish 15%                                       ║
╚══════════════════════════════════════════════════════════════╝
```

### Structural (`/pipeline-status structural`)

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO PIPELINE GUIDE — STRUCTURAL PROJECT            ║
╠══════════════════════════════════════════════════════════════╣
║  Phase 1 · Discovery                                         ║
║    /interview-me [topic]   → Research spec + project_type    ║
║    /lit-review [topic]     → academic-librarian + editor     ║
║    /find-data [question]   → explorer + data-quality-surveyor║
║                                                              ║
║  Phase 2 · Strategy                                          ║
║    /theory-model [topic]   → econ-finance-theorist + critic  ║
║    /structural-estimation  → structural-expert + critic      ║
║    Required: 80/100 to advance  (weight: 35% of score)       ║
║                                                              ║
║  Phase 3 · Execution                                         ║
║    /data-analysis [dataset] → Coder + debugger              ║
║    /draft-paper [section]   → economics-paper-writer         ║
║    /proofread [file]         → academic-proofreader          ║
║                                                              ║
║  Phase 4 · Peer Review                                       ║
║    /review-paper [file]    → 2× blind-peer-referee           ║
║                                                              ║
║  Phase 5 · Submission                                        ║
║    /target-journal [paper] → journal selection               ║
║    /audit-replication [dir]→ replication-verifier            ║
║    /submit [journal]       → final gate ≥95                  ║
╠══════════════════════════════════════════════════════════════╣
║  Scoring: Structural 20%, Theory model 15%, Paper 20%,      ║
║  Code 15%, Lit 10%, Data 10%, Polish 5%, Replication 5%     ║
╚══════════════════════════════════════════════════════════════╝
```

### Empirical+Theory (`/pipeline-status empirical+theory`)

```
╔══════════════════════════════════════════════════════════════╗
║         CLOCO PIPELINE GUIDE — EMPIRICAL+THEORY PROJECT      ║
╠══════════════════════════════════════════════════════════════╣
║  Phase 1 · Discovery                                         ║
║    /interview-me [topic]   → Research spec + project_type    ║
║    /lit-review [topic]     → academic-librarian + editor     ║
║    /find-data [question]   → explorer + data-quality-surveyor║
║                                                              ║
║  Phase 2 · Strategy                                          ║
║    /theory-model [topic]   → econ-finance-theorist + critic  ║
║    /identify   → causal-strategist + critic      ║
║    Required: 80/100 to advance  (weights: 10% + 20%)         ║
║                                                              ║
║  Phase 3 · Execution                                         ║
║    /data-analysis [dataset] → Coder + debugger              ║
║    /draft-paper [section]   → economics-paper-writer         ║
║    /proofread [file]         → academic-proofreader          ║
║                                                              ║
║  Phase 4 · Peer Review                                       ║
║    /review-paper [file]    → 2× blind-peer-referee           ║
║                                                              ║
║  Phase 5 · Submission                                        ║
║    /target-journal [paper] → journal selection               ║
║    /audit-replication [dir]→ replication-verifier            ║
║    /submit [journal]       → final gate ≥95                  ║
╠══════════════════════════════════════════════════════════════╣
║  Scoring: Identification 20%, Paper 25%, Code 15%, Lit 10%, ║
║  Data 10%, Theory 10%, Polish 5%, Replication 5%            ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Notes

- Scores are read from `quality_reports/research_journal.md` — the journal is
  the single source of truth for pipeline progress
- If the journal is missing or empty, all components show `not started`
- Phase detection is conservative: a phase is "done" only when ALL its required
  components score >= 80; a single component below threshold keeps the phase open
- The overall score is computed only when at least one component has a score;
  otherwise it shows `N/A`
- `/pipeline-status` is safe to run at any time; it is read-only

# Research Journal (Auto-Append Rule)

**After every agent produces a report, append a summary entry to `quality_reports/research_journal.md`.**

## Entry Format

```markdown
### YYYY-MM-DD HH:MM — [Agent Name]
**Phase:** [Discovery/Strategy/Execution/Peer Review/Presentation]
**Target:** [file or topic reviewed]
**Score:** [XX/100 or PASS/FAIL or N/A]
**Verdict:** [one line — the key finding or decision]
**Report:** [link to full report]
```

## Automation

Agent-report entries are written **automatically** by `.claude/hooks/journal-append.py` after every dispatch of a research agent through the Agent tool (score is parsed from `**Score:** XX/100`, `PASS`/`FAIL`, or a `Verdict: … XX/100` line; make sure critics print one). Claude still appends by hand: phase transitions, strike counts, escalations, editorial decisions, user overrides, and `/scout` verdicts.

## Rules

- **Append only** — never overwrite or edit previous entries
- **One entry per agent invocation** — not per issue
- **Create the file** if it doesn't exist, with header: `# Research Journal — [Project Name]`
- **Include escalation events:** "Strike 2/3 — Debugger flagged code-strategy misalignment"
- **Include phase transitions:** "Phase 2 → Phase 3: Econometrician approved (score: 88)"
- **Include editorial decisions:** "Editor decision: Minor Revisions"

## What Gets Logged

| Event | Logged? |
|-------|---------|
| Agent review report | Yes — score + verdict |
| Phase transition | Yes — which phase, approval score |
| Escalation (three strikes) | Yes — strike count, escalation target |
| User override | Yes — what was overridden and why |
| R&R comment routing | Yes — classification + routing target |
| Score changes | Yes — before/after when resubmitted |

## Relationship to Other Logs

- **Session logs** (`quality_reports/session_logs/`) — per-session, detailed, ephemeral
- **Session report** (`SESSION_REPORT.md`) — consolidated operations log
- **Research journal** (`quality_reports/research_journal.md`) — agent-level research history, append-only

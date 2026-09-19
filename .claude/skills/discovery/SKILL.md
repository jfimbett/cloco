---
name: discovery
description: Run the entire Discovery phase in one command from an existing research spec — literature review (librarian + editor) and data discovery (explorer + surveyor) in parallel, project-type aware, with critic loops, journal entries, a merged bibliography, and a consolidated Discovery Report that says whether Strategy is unlocked. Use after /interview-me, or whenever the user says "do the discovery phase", "get the lit and data going", or "run phase 1".
disable-model-invocation: true
argument-hint: "[optional: path to research spec — defaults to the most recent quality_reports/research_spec_*.md]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "WebSearch", "WebFetch", "Task"]
---

# Discovery

One command for Phase 1. Reads the research spec, dispatches the discovery worker–critic pairs that the project type needs, runs each pair through its revision loop, merges BibTeX into the paper, and reports whether the Strategy phase is unlocked.

**Input:** `$ARGUMENTS` — optional spec path. Without it, use the most recently modified `quality_reports/research_spec_*.md`. If none exists, stop and tell the user to run `/interview-me` (or `/scout` if they are not yet sure about the idea).

---

## Step 1: Read the spec and choose the lanes

Extract from the spec: title, `project_type`, research question, hypothesis, data section, theoretical model section.

| `project_type` | Literature lane | Data lane |
|----------------|-----------------|-----------|
| `empirical` | yes | yes |
| `theory` | yes (emphasise theoretical foundations + methods papers) | **no** |
| `structural` | yes (add: papers estimating similar models, their moments/data) | yes |
| `empirical+theory` | yes (both empirical and theoretical strands) | yes |

If `project_type` is absent, default to `empirical` and say so.

Also check what already exists: `quality_reports/literature/*/`, `quality_reports/data/*/`, and `quality_reports/research_journal.md`. A lane whose critic score is already ≥ 80 in the journal is **skipped** unless the user says `--force`.

## Step 2: Dispatch the lanes in parallel

Launch the two workers in **one message**.

**Literature lane** — `academic-librarian`, full protocol (see `/lit-review`). Pass the research question, hypothesis, the type-specific emphasis from the table above, `domain-profile.md` tiers, and any papers already in `paper/references.bib`. Output to `quality_reports/literature/[slug]/`.

**Data lane** — `explorer`, Discovery mode (Inventory first if `data/raw` or `data/processed` is non-empty). Pass the data requirements from the spec: outcome, treatment, unit, period, geography, and the design implied by the Empirical Strategy section. Output to `quality_reports/data/[slug]/`.

## Step 3: Critics, with revision loops

As each worker returns, dispatch its critic (do not wait for the other lane):

- `academic-editor` in Lit Critic mode on `quality_reports/literature/[slug]/` → score.
- `data-quality-surveyor` on `quality_reports/data/[slug]/data_assessment.md` → score.

Severity for both: **Discovery** (constructive) per `severity-gradient.md`.

If a score is < 80: re-dispatch the worker with the critic's Required Actions verbatim, then re-run the critic. Maximum **3 rounds per pair** (`three-strikes.md`). After three failures, stop that lane and prepare the escalation question for the user.

## Step 4: Merge the bibliography

When the literature lane passes, append the librarian's entries to the central bibliography without duplicates:

```bash
python3 .claude/scripts/merge_bib.py quality_reports/literature/[slug]/references.bib --target paper/references.bib
```

Report how many entries were added and skipped. (`paper/references.bib` is protected from direct edits; this script is the sanctioned path.)

## Step 5: Consolidated Discovery Report

Write `quality_reports/discovery_report_[slug].md`:

```markdown
# Discovery Report — [Title]
**Date:** YYYY-MM-DD   **Project type:** [type]

## Gate
| Lane | Worker | Critic | Score | Rounds | Status |
|------|--------|--------|-------|--------|--------|
| Literature | academic-librarian | academic-editor | XX/100 | n | PASS / FAIL / ESCALATED |
| Data | explorer | data-quality-surveyor | XX/100 | n | PASS / FAIL / SKIPPED (theory) |

**Strategy phase unlocked:** YES / NO — [dependency-graph.md: needs at least one lane ≥ 80; for structural/empirical+theory both are strongly recommended]

## Positioning (from positioning.md)
[suggested contribution statement + 2–3 key differentiators + scooping risks]

## Data path (from data_assessment.md)
[recommended dataset(s), grade, deal-breakers, access actions with owners/dates]

## Contradictions between lanes
[e.g., "closest papers use dataset X; explorer graded X as D — resolve before /identify"]

## Open questions for the user
[…]

## Next command
[/identify | /theory-model | /structural-estimation — per project type]
```

## Step 6: Journal and report

The `journal-append` hook logs each agent dispatch automatically. Add by hand to `quality_reports/research_journal.md`:
- `Phase 1 → Phase 2: Discovery complete (lit XX, data XX)` when unlocked, or
- `Strike n/3 — [pair]` lines and any escalation.

Then print to the user:

```
✅ DISCOVERY — [title]
Literature  XX/100  (n rounds)   Data  XX/100  (n rounds)
Bibliography: +N entries merged into paper/references.bib
Strategy unlocked: YES → next: /identify "[question]"
Report: quality_reports/discovery_report_[slug].md
```

---

## Principles

- **Parallel by default.** Literature and data never wait on each other.
- **Critics are mandatory.** No lane passes without its critic's score, per `adversarial-pairing.md`.
- **Idempotent.** Re-running skips lanes already ≥ 80; `--force` re-runs everything.
- **Escalate with a question, not a complaint.** After three strikes: "The surveyor requires a pre-period; no source has one before 2015. Shift the sample window, or change the outcome?"

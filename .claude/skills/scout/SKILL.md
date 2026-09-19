---
name: scout
description: Fast go/no-go triage of a research idea BEFORE committing to the full pipeline. Runs a literature quick-scan (academic-librarian, capped), a data quick-scan (explorer, capped), and an idea-critic verdict in one shot. Produces a one-page scouting memo with novelty, identification, data feasibility, and scooping risk. Use when the user asks "is this worth doing?", "should I pursue X?", or wants to compare several ideas cheaply.
disable-model-invocation: true
argument-hint: "[one research idea, or path to a research_ideation report to scout every candidate]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "WebSearch", "WebFetch", "Task"]
---

# Scout

Triage a research idea in ~10 minutes of agent time. The output is a **verdict**, not a plan: GO → run `/interview-me`; REFRAME → fix the blocking dimension first; NO-GO → move on.

**Input:** `$ARGUMENTS` — a single idea in one or two sentences, or a path to `quality_reports/research_ideation_*.md` (scouts each candidate, max 5).

**Existing paper instead of an idea?** If `$ARGUMENTS` is a path to a PDF, a `.tex`, a `.docx`, or a folder of old materials (a drawer paper, an abandoned draft, notes plus data), do not scout it — hand it to `/revive` with the same arguments. Revival reconstructs the paper, checks what changed since it stalled, and reuses the sunk work; scouting would treat it as a blank idea.

---

## Why this exists

The full pipeline (`/interview-me` → `/lit-review` → `/find-data` → `/identify`) costs hours of agent time and a long interview. Most ideas die on one of three questions — *is it new, can it be identified, does the data exist* — that can be answered cheaply. Scouting answers them first.

---

## Workflow

### Step 1: Frame the idea (no agents)

Write a three-line **scouting brief** from `$ARGUMENTS` plus `.claude/rules/domain-profile.md`:
- **Claim:** the causal or descriptive statement in one sentence (X → Y for whom)
- **Variation:** the candidate source of exogenous variation, if any is implied
- **Unit / period / setting**

If the idea is too vague to fill all three lines, fill what you can and mark the rest `UNSPECIFIED` — the critic will penalise it, which is the point.

### Step 2: Parallel quick-scans (two agents, launched together)

Dispatch **both** in a single message so they run concurrently.

**academic-librarian — Quick-Scan mode:**
```
Quick-scan (NOT a full review). Research idea: [scouting brief].
Return, inline, no files:
  1. The 5–8 closest papers (published or WP, last 10 years), each with:
     author-year, venue, one-line finding, identification strategy, proximity score 1–5.
  2. Scooping check: any WP in the last 24 months on the same question and setting? List them.
  3. One sentence: what the frontier map would say this idea adds — or "nothing obvious".
Cap: 8 papers. Do not write files. Do not fabricate; mark unverifiable items UNVERIFIED.
```

**explorer — Quick-Scan mode:**
```
Quick-scan (NOT a full assessment). Research idea: [scouting brief].
Return, inline, a single table of the 3–5 most plausible datasets:
  dataset | provider | access (public/registration/application/commercial) | unit & frequency |
  coverage (years, geography) | feasibility grade A–D | supports the design? (pre/post panel, running variable, instrument)
Then one line: the required variable most likely to be MISSING from every source.
Cap: 5 rows. Do not write files.
```

### Step 3: Assemble the scouting memo

Combine the brief and both scans into `quality_reports/scout_[slug].md`:

```markdown
# Scouting Memo — [Idea]
**Date:** YYYY-MM-DD
**Brief:** [claim / variation / unit-period-setting]

## Literature quick-scan
[librarian table + scooping list + frontier sentence]

## Data quick-scan
[explorer table + missing-variable line]

## Open unknowns
[what neither scan could establish]
```

### Step 4: Verdict (idea-critic)

Dispatch `idea-critic`:
```
Mode: Scouting. Review quality_reports/scout_[slug].md.
Severity: Discovery (constructive). Score all five dimensions, apply deductions,
issue GO / REFRAME / NO-GO with the killer question and the ordered list of what would raise the score.
Save to quality_reports/idea_review_[slug].md.
```

Append the critic's verdict block to the scouting memo under `## Verdict`.

### Step 5: Report to the user

```
🔭 SCOUT — [idea]
Verdict: [GO / REFRAME / NO-GO]  ([XX/100])
Novelty XX · Contribution XX · Identification XX · Data XX · Scooping XX

Killer question: [one line]
Closest paper:   [author-year, venue] — [how the idea differs / or "not differentiated"]
Best data:       [dataset, grade] — [what's missing]

Next: [GO → /interview-me "[idea]"] | [REFRAME → "fix X, then /scout again"] | [NO-GO → "drop; revisit if Y"]
Memo: quality_reports/scout_[slug].md
```

When scouting an ideation report, run Steps 1–4 for each candidate (parallelise the quick-scans across candidates where possible) and finish with a ranked table of verdicts.

---

## Limits

- Quick-scans are capped; a GO verdict still requires the full `/lit-review` and `/find-data` later — scouting reduces false starts, it does not replace Discovery.
- Scout scores are **advisory** and are not part of the weighted project score.
- The journal-append hook logs the three agent runs automatically; add a `Scout verdict: …` line to `quality_reports/research_journal.md` by hand if the idea proceeds.
- Scouting is for ideas that do not yet exist as a paper. For an old draft with text, code, or data behind it, `/revive` is the right entry point.

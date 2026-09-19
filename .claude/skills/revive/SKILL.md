---
name: revive
description: Rescue an old or abandoned working paper. Point it at whatever survives — a PDF, a .tex folder, notes, a .bib, old code, old data extracts — and it reconstructs where the project stood, finds out what changed in the literature and data since it stalled, gets an idea-critic REVIVE / REFRAME / RETIRE verdict, and on REVIVE writes a pre-filled research spec plus a revival plan that enters the pipeline mid-stream. Use when the user says "save this paper", "I stopped working on this", "old draft", "can this be salvaged", or passes a path to /scout.
disable-model-invocation: true
argument-hint: "[path to PDF / folder / files of the old paper] [--slug NAME] [--no-questions]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Edit", "WebSearch", "WebFetch", "Task"]
---

# Revive

Turn a drawer paper into a pipeline entry point. The output is a **verdict plus a plan**: REVIVE → a pre-filled spec and the exact phase to re-enter; REFRAME → what must change before it is worth re-entering; RETIRE → an archive note that records what is salvageable.

**Input:** `$ARGUMENTS` — one or more paths (a PDF, a project folder, a Dropbox folder, individual files). Optional `--slug NAME` (default: derived from the title) and `--no-questions` (skip the gap interview; every unknown is marked ASSUMED).

---

## Why this exists

An abandoned paper is not a new idea: the question, the data, and often 80% of the code and text already exist. What is missing is a *current* answer to four things — has it been scooped, does the design still meet today's standards, is the data still reachable, and why did it actually stall. `/scout` answers the first two for a fresh idea; `/revive` answers all four for an existing artefact and then reuses the sunk work instead of restarting the pipeline.

---

## Workflow

### Step 1: Intake (script, no agents)

```bash
python3 .claude/scripts/paper_intake.py <paths…> --slug <slug>
```

Writes `quality_reports/revival/<slug>/inventory.md`, `manifest.json`, and `extracted/*.txt` (gitignored). Then:

1. Read `inventory.md`. If the summary says PDFs were unreadable, tell the user (`brew install poppler` or `pip install pypdf`) and continue with what was read.
2. Read the extracted text of the **main manuscript** (the main `.tex` if one exists, else the largest `manuscript-pdf`). Read any `notes`, `README`, `ARCHIVE*`, or `TODO` files in full — they usually contain the stall reason.
3. If the folder contains an archive note in the `templates/archive-readme.md` format (`**Revisit if:**` line), quote it in the memo.

**Never copy data files into the repository.** Data stays where it is; Step 6 registers it in place.

### Step 2: Reconstruct the paper (your own reading, no agents)

Write the **revival brief** at the top of `quality_reports/revival/<slug>/revival_memo.md`:

```markdown
# Revival Memo — [Title]
**Date:** YYYY-MM-DD · **Materials:** [paths] · **Last touched:** [newest mtime / latest year in text]
**Stalled at:** [phase — Discovery / Strategy / Execution (code) / Execution (write) / Peer Review — with evidence]

## Brief
- **Claim:** [X → Y for whom, as the paper states it]
- **Variation:** [the identification source the paper uses]
- **Design:** [method as written; flag anything the literature has since superseded, e.g. TWFE with staggered timing]
- **Data:** [sources named · sample period · what is on disk vs. what must be re-pulled]
- **Results claimed:** [headline estimates with units, from the text]
- **State of the artefacts:** [manuscript words / sections present / tables / figures; code languages, hard-coded paths, runs?; bib horizon year]

## Stall diagnosis
[Why it stopped, from notes + text hints (referee report, data access, identification concern, life). Mark INFERRED vs STATED.]
```

`project_type` for the spec follows the paper: propositions and proofs without estimation → `theory`; a structural model estimated on data → `structural`; a model section motivating a reduced-form test → `empirical+theory`; otherwise `empirical`.

### Step 3: Gap interview (one message, ≤ 4 questions)

Unless `--no-questions` was passed, ask the user directly in text — **not** with AskUserQuestion — only what the materials cannot answer, typically:

1. Why did you stop? (referee reports? data? co-author? time?) Anything to add to the stall diagnosis above?
2. Which data do you still have access to, and where is it now?
3. Are there referee reports, discussant slides, or seminar feedback not in the folder?
4. What is the ambition now — same journal tier, a shorter paper, a different framing?

Wait for the reply, fold it into the memo (`## User input`), and mark anything still unknown `ASSUMED`. If the user says "skip" or "just do it", proceed with assumptions.

### Step 4: What changed since it stalled (two agents, launched together)

Dispatch **both** in one message. The framing differs from `/scout`: the question is not "is this new" but "is it *still* new, and what moved".

**academic-librarian — Quick-Scan mode (revival framing):**
```
Quick-scan for a REVIVAL (NOT a full review). The paper below stalled around [year]; its bibliography stops at [bib horizon year].
Brief: [claim / variation / design / data / results].
Return inline, no files:
  1. Papers on the same question or setting published or circulated AFTER [bib horizon year]: author-year, venue, finding, identification, proximity 1–5. Cap 8.
  2. Scooping check: has the paper's headline result been published? By whom? Does anything remain (setting, mechanism, horizon, heterogeneity)?
  3. Methodological shifts since [year] that a referee would now demand for this design (e.g. staggered-DiD estimators, bandwidth selection, weak-IV inference, pre-registration norms). One line each.
  4. One sentence: the strongest *current* positioning for this paper — or "superseded".
Mark unverifiable items UNVERIFIED. Do not fabricate.
```

**explorer — Inventory + Quick-Scan mode (revival framing):**
```
REVIVAL data check (NOT a full assessment). Read quality_reports/revival/<slug>/inventory.md (Data + Code sections).
Sample period in the paper: [period]. Sources named: [list]. Files on disk: [list with sizes].
Return inline:
  1. For each source named: still available? via the registry / WRDS / provider? access grade A–D; can coverage be extended past [last sample year]? one line each.
  2. Local files: usable as-is (format readable, not corrupt), or must be re-pulled? Note any file that must NOT enter git (≥20 MB, licensed).
  3. New datasets since [year] that would strengthen the design (better treatment measure, longer panel, granular outcome). Cap 3.
  4. One line: the single data step that gates a re-run of the main table.
Do not write files.
```

Append both returns to the memo under `## Literature since [year]` and `## Data today`.

### Step 5: Verdict (idea-critic, Revival mode)

```
Mode: Revival. Review quality_reports/revival/<slug>/revival_memo.md (brief, stall diagnosis, user input, literature since, data today) together with quality_reports/revival/<slug>/inventory.md.
Severity: Discovery (constructive) — sunk work counts only if it is reusable.
Score the five revival dimensions, apply deductions, issue REVIVE / REFRAME / RETIRE, name the killer question,
state the pipeline re-entry phase, and list the ordered steps that would raise the score.
Save to quality_reports/revival/<slug>/idea_review.md.
```

Append the critic's verdict block to the memo under `## Verdict`. Add by hand to `quality_reports/research_journal.md`: `Revival verdict: <slug> — REVIVE/REFRAME/RETIRE (XX/100), re-entry at <phase>`.

### Step 6: Act on the verdict

**REVIVE** — set the project up so the pipeline can enter mid-stream (`dependency-graph.md`):

1. **Spec.** Write `quality_reports/research_spec_<slug>.md` in the `/interview-me` format, pre-filled from the memo, with `project_name:`, `project_type:`, and `project_slug:` (two or three kebab-case words; the repo becomes `cloco-<slug>`) lines near the top and a `## Provenance` section pointing at the legacy materials and the revival memo. Sections the materials do not support get `[TO CONFIRM]`, not invented content. Fill `.claude/rules/domain-profile.md` if it still holds placeholders.
2. **Bibliography.** If a `.bib` was found: `python3 .claude/scripts/merge_bib.py <old.bib>` into `paper/references.bib` (dedupes). Papers the librarian surfaced go into `quality_reports/literature/<slug>/references.bib` for the next `/lit-review` to merge.
3. **Data.** For every usable local file, register in place: `python3 .claude/scripts/data_registry.py add <name> --path '<${DROPBOX_ROOT}/…>' --stage external --source '<provider>, pulled <year>, legacy'`. If a file sits outside every configured root, ask the user to move it under `${DROPBOX_ROOT}` (never into the repo) or add a `DATA_ROOT`. Then `/data-profile <name>` on the main analysis file.
4. **Manuscript.** If a main `.tex` exists and `paper/main.tex` is still the template: copy the legacy sources into `paper/legacy/<slug>/` (sources only — no PDFs, no build artefacts) and record in the plan that `/draft-paper` should rebuild `paper/main.tex` from them section by section rather than from scratch. If `paper/main.tex` already holds another project, stop and ask.
5. **Code.** Copy scripts into `code/legacy/<slug>/` unchanged. Do not fix them here; the plan routes them through `/review-code` and `/data-analysis`, which replace hard-coded paths with `data_path()`.
6. **Identity.** Run `python3 .claude/scripts/project_setup.py status`; if `needs-detach`, the first line of the revival plan's next commands is `/setup-project` (own folder name and GitHub repository before any push).
7. **Revival plan.** Write `quality_reports/revival/<slug>/revival_plan.md`:

```markdown
# Revival Plan — [Title]
**Verdict:** REVIVE (XX/100) · **Re-entry phase:** [Strategy / Execution (code) / Execution (write) / Peer Review]
**project_type:** [type] · **Spec:** quality_reports/research_spec_<slug>.md

## Keep / Redo / Add
| Component | Decision | Why | Command |
|-----------|----------|-----|---------|
| Literature | update from [year] | … | /lit-review "…" |
| Data | re-pull X, keep Y | … | /wrds fetch … · /data-profile … |
| Identification | redo with [estimator] | referee concern / method shift | /identify "…" |
| Code | port legacy scripts | hard-coded paths, no seed | /review-code code/legacy/<slug>/… → /data-analysis |
| Manuscript | keep Intro/Data, rewrite Strategy/Results | … | /draft-paper … |
| Referee reports | address R1.2, R2.1 | … | /respond-to-referee <report> |

## Ordered next commands
1. …
2. …

## Risks
- [scooping / data access / design]
```

**REFRAME** — write the memo's `## Reframing` section from the critic's "what would raise the score" list, write the revival plan with only the reframing steps, and stop. Do not create a spec. Suggest re-running `/revive` (same paths, `--no-questions`) after the blocking item is fixed.

**RETIRE** — write `quality_reports/revival/<slug>/ARCHIVE.md` in the `templates/archive-readme.md` format, with the **Salvageable** line naming concrete reusable pieces (a cleaned dataset, a code module, a literature section) and **Revisit if** taken from the critic. Nothing else is created.

### Step 7: Report to the user

```
🩺 REVIVE — [Title]
Stalled: [year] at [phase] — [stall reason, one line]
Verdict: [REVIVE / REFRAME / RETIRE]  ([XX/100])
Still novel XX · Contribution XX · Design today XX · Data & code salvage XX · Scooping XX

Killer question: [one line]
Since [year]:      [closest new paper — how this differs / "headline result published by …"]
Data today:        [gate step — e.g. "re-pull Compustat 2017–2025 via /wrds; SIRENE extract on disk is usable"]
Salvage:           [manuscript N words (keep sections …) · code N scripts (port) · bib N entries (merge)]

Re-entry: [phase] → next: [ordered commands]
Files: quality_reports/revival/<slug>/{inventory,revival_memo,idea_review,revival_plan}.md
```

---

## Limits

- Quick-scans are capped; a REVIVE verdict still routes through the normal critics (`/lit-review`, `/data-profile`, `/identify`, `/review-code`) — revival skips phases only where the dependency graph says their inputs are already satisfied.
- Revival scores are **advisory** and not part of the weighted project score.
- The intake script never modifies or copies user files. Copies into `paper/legacy/` and `code/legacy/` happen only in Step 6 on REVIVE and only for source files.
- One paper per run. Several drawer papers → run `/revive` once per folder and compare the verdicts.

# cloco — Research Orchestration for Economics with Claude Code

> **A multi-agent, quality-gated research pipeline for economics papers — from idea to submission — built on top of Claude Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20Code-blueviolet)](https://claude.ai/code)
[![Upstream: clo-author](https://img.shields.io/badge/Upstream-clo--author-blue)](https://hsantanna88.github.io/clo-author/)

---

## Lineage & Credits

> Built on top of [**clo-author**](https://hsantanna88.github.io/clo-author/) by Hugo Sant'Anna,
> which is itself a fork of [**claude-code-my-workflow**](https://github.com/pedrohcgs/claude-code-my-workflow)
> by Pedro H.C. Sant'Anna (Emory University).
>
> Extended for financial economics research at **EDHEC Business School**
> by [Juan F. Imbet](https://github.com/jfimbet).

This project would not exist without the pioneering infrastructure work from both upstream projects. The core orchestration philosophy, agent-critic pairing pattern, and quality-gate system originate there.

---

## What This Is

Economics research pipelines are fragmented: literature review in one tool, data analysis in another, writing in a third, with no systematic quality enforcement across stages. Claude Code makes it possible to build an autonomous contractor that manages the full research lifecycle — dispatching specialized agents, enforcing quality gates, and tracking every decision.

`cloco` extends the upstream infrastructure with:

- **Four project-type-aware pipelines** (`empirical`, `theory`, `structural`, `empirical+theory`) with type-specific scoring weights, so a pure theory paper isn't penalized for lacking data.
- **Specialist creators and critics**: `econ-finance-theorist` / `theory-critic`, `structural-estimation-expert` / `structural-critic`, `causal-strategist` / `identification-critic`.
- **Automated early stages**: `/scout` (10-minute go/no-go triage with an `idea-critic`), `/revive` (rescue an abandoned working paper from a PDF, notes, old code and data: reconstruct, check what changed since it stalled, REVIVE / REFRAME / RETIRE verdict, pre-filled spec and re-entry plan), `/discovery` (the whole Phase 1 — literature ∥ data, critic loops, bibliography merge — in one command), `/data-profile` (automated dataset profiling: panel key, pre-period, staggered treatment, codebook), and a rewritten `explorer` that actually discovers data.
- **Data that lives outside git, with its location inside git**: `data/registry.json` maps every dataset to a `${DROPBOX_ROOT}/…` path template with provenance; `code/utils/data_paths.{py,R}` resolve it per machine; a `path-guard` hook flags hard-coded Dropbox/home paths in code.
- **WRDS without the web downloader**: `/wrds` explores libraries, tables, and columns and `fetch`es SQL pulls straight to Dropbox, auto-registered and profiled — when the author has credentials; silent no-op otherwise.
- **A git steward**: a `git-steward` agent plus a `secrets-guard` hook that blocks any `git commit`/`git push` carrying credentials, data files, or oversized blobs; repo audits, history scans, worktree proposals for parallel work (R&R vs. analysis, talk vs. paper), branch cleanup, submission tags.
- **A terminal that knows where the project is**: a two-line Claude Code status line (project · phase · next command · gates │ git · data registry · context bar · model) plus terminal tab titles, a session-welcome banner, and `make status` for the same dashboard from the shell — all fed by one `project_state.py`.
- **Automated bookkeeping**: a `journal-append` hook that writes the research journal after every agent dispatch, a session-welcome banner with phase, next command, and lesson count, and portable stdlib-only hooks (`python3`, 3.9+).
- **A lessons protocol** that captures project-specific corrections and prevents recurring mistakes.

---

## Architecture at a Glance

```
/scout [idea]  →  GO / REFRAME / NO-GO          (optional, ~10 min, idea-critic)
       │ GO
/interview-me  →  Research Spec + Domain Profile
       │                                        /revive [old paper] → REVIVE / REFRAME / RETIRE
       │                                              └─ pre-filled spec, enters below at the phase the critic names
       │
/discovery     →  /lit-review ∥ /find-data  (critic loops, bib merge, Discovery Report)
       │
/data-profile  →  panel key · pre-period · treatment timing · codebook   (once data is on disk)
       │
       ├─ [empirical]────────── /identify ──────────────────────────────────────────┐
       ├─ [theory]───────────── /theory-model ───────────────────────────────────────┤
       ├─ [structural]────────── /theory-model ─── /structural-estimation ──────────┤
       └─ [empirical+theory] ── /theory-model ─── /identify ────────────────────────┘
                                                                          │
                                              /data-analysis  (if not pure theory)
                                                                          │
                                                                   /draft-paper
                                                                          │
                                                     /paper-excellence → /review-paper
                                                                          │
                                                                      /submit
```

Every creator agent is paired with a critic. Every artifact must score ≥ 80 before advancing. Nothing ships below the gate threshold.

---

## Four Research Pipelines

### A — Empirical

```
Research Spec
    ├── academic-librarian  ──[parallel]──  explorer
    │         ↓ academic-editor               ↓ data-quality-surveyor
    └──────── causal-strategist
                    ↓ identification-critic
              Coder (main Claude)
                    ↓ debugger
              economics-paper-writer
                    ↓ academic-proofreader
              blind-peer-referee ×2
                    ↓ academic-editor
              replication-verifier  →  submit
```

### B — Theory

```
Research Spec
    ├── academic-librarian  ──[no data needed]
    │         ↓ academic-editor
    └──────── econ-finance-theorist
                    ↓ theory-critic
              economics-paper-writer
                    ↓ academic-proofreader
              blind-peer-referee ×2
                    ↓ academic-editor  →  submit
```

### C — Structural

```
Research Spec
    ├── academic-librarian  ──[parallel]──  explorer
    │         ↓ academic-editor               ↓ data-quality-surveyor
    ├──────── econ-finance-theorist
    │               ↓ theory-critic
    └──────── structural-estimation-expert
                    ↓ structural-critic
              Coder (main Claude)
                    ↓ debugger
              economics-paper-writer  →  replication-verifier  →  submit
```

### D — Empirical + Theory

```
Research Spec
    ├── academic-librarian  ──[parallel]──  explorer
    │         ↓ academic-editor               ↓ data-quality-surveyor
    ├──────── econ-finance-theorist   ──[parallel]──  causal-strategist
    │               ↓ theory-critic                        ↓ identification-critic
    └─────────────────────────────────────────────────────
              Coder (main Claude)  →  economics-paper-writer  →  submit
```

---

## 39 Skills

| Category | Skill | What It Does |
|----------|-------|-------------|
| **Pipeline** | `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| | `/interview-me [topic]` | Interactive research interview → spec + domain profile |
| | `/discovery` | **Phase 1 in one command**: lit-review ∥ find-data, critic loops, bib merge, Discovery Report |
| **Ideation** | `/research-ideation [topic]` | 3–5 research questions + strategies, ranked by `idea-critic` |
| | `/scout [idea]` | **Go/no-go triage**: capped librarian + explorer quick-scans → `idea-critic` verdict |
| | `/revive [path]` | **Rescue an abandoned paper**: intake PDF / .tex / notes / .bib / code / data → librarian + explorer "what changed since" → `idea-critic` REVIVE / REFRAME / RETIRE → pre-filled spec + revival plan (enters the pipeline mid-stream) |
| **Literature** | `/lit-review [topic]` | Librarian + Editor: literature search + synthesis + dedupe-merge into `paper/references.bib` |
| **Theory & Structural** | `/theory-model [question]` | Theorist + theory-critic: formal model design |
| | `/structural-estimation [spec]` | Structural expert + structural-critic: estimation design |
| **Data & Strategy** | `/find-data [question]` | Explorer + Surveyor: data discovery (9 source categories) + assessment |
| | `/data-profile [name\|file]` | **Automated profiling** of data on disk: panel key, balance, pre-period, staggered cohorts, codebook → Surveyor critique |
| | `/data-registry [cmd]` | **Where every dataset lives** — Dropbox / local / WRDS, with provenance; `setup` on a new machine, `check` before reading anything |
| | `/wrds [cmd]` | **WRDS from the session**: `search`, `tables`, `describe`, `sample`, `count`, `query`, `fetch` → Dropbox, registered, profiled |
| | `/identify [question]` | Strategist + identification-critic: identification strategy |
| | `/pre-analysis-plan [spec]` | Strategist: draft PAP (AEA/OSF/EGAP) |
| **Analysis & Writing** | `/data-analysis [dataset]` | Coder + Debugger: end-to-end analysis |
| | `/draft-paper [section]` | Writer: draft paper sections + humanizer pass |
| | `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| **Quality & Review** | `/econometrics-check [file]` | Econometrician: 4-phase causal inference audit |
| | `/review-code [file]` | Debugger: code quality review (standalone) |
| | `/proofread [file]` | Proofreader: 6-category manuscript review |
| | `/paper-excellence [file]` | Multi-agent parallel review + weighted score |
| | `/review-paper [file]` | 2 Referees + Editor: simulated peer review |
| | `/validate-bib` | Cross-reference citations vs bibliography |
| **Submission** | `/target-journal [paper]` | Editor: journal targeting + submission strategy |
| | `/respond-to-referee [report]` | Revision routing per revision-protocol |
| | `/audit-replication [dir]` | Verifier: 10-check submission audit |
| | `/data-deposit` | Coder + Verifier: AEA replication package |
| | `/submit [journal]` | Final gate: score ≥ 95, all components ≥ 80 |
| **Presentations** | `/create-talk [format]` | Storyteller + Discussant: Beamer/Quarto talk from paper |
| | `/visual-audit [file]` | Slide layout audit |
| **Infrastructure** | `/commit [msg]` | Stage, commit, PR, merge |
| | `/git-steward [cmd]` | **Repo hygiene**: `audit`, `secrets`, `history-scan`, `worktree NAME`, `cleanup`, `tag JOURNAL`, `pr` |
| | `/humanizer [file]` | Strip 24 AI writing patterns |
| | `/journal` | Research journal timeline |
| | `/context-status` | Session health + context usage |
| | `/learn` | Extract session discoveries into skills |
| | `/pipeline-status [type]` | Pipeline dashboard + per-type guide |
| | `/deploy` | Quarto render + GitHub Pages sync |

---

## 21 Agents

| Agent | Role | Paired Critic |
|-------|------|--------------|
| `research-orchestrator` | Master controller — manages the dependency graph, dispatches agents, enforces quality gates | — |
| `idea-critic` | Scores research ideas on novelty, contribution, identification credibility, data feasibility, scooping risk → GO / REFRAME / NO-GO; Revival mode scores an abandoned paper → REVIVE / REFRAME / RETIRE with a re-entry phase | — (critic for `/scout`, `/research-ideation`, `/revive`) |
| `academic-librarian` | Systematic literature search across top journals, NBER, SSRN, RePeC; quick-scan mode for `/scout` | `academic-editor` |
| `academic-editor` | Literature critique + peer review dispatcher | — |
| `blind-peer-referee` | Simulated adversarial referee — two instances per paper | — |
| `explorer` | Data discovery across 9 source categories; checks the data registry and (with credentials) WRDS first so assessments cite real tables and columns; Inventory mode for local files; quick-scan for `/scout` | `data-quality-surveyor` |
| `data-quality-surveyor` | Data quality critique: validity, sample, identification fit — on assessments and on `/data-profile` output | — |
| `causal-strategist` | Identification strategy design: DiD, IV, RDD, event study | `identification-critic` |
| `identification-critic` | Reduced-form identification review: assumptions, inference, robustness | — |
| `econ-finance-theorist` | Formal economic/finance model builder — equilibrium, proofs, LaTeX | `theory-critic` |
| `theory-critic` | Proof rigor, equilibrium validity, economic coherence | — |
| `structural-estimation-expert` | Structural model design + estimation strategy (MLE, GMM, SMM) | `structural-critic` |
| `structural-critic` | Microfoundations, parameter identification, solution feasibility | — |
| `econometrics-critic` | Standalone `/econometrics-check` audits and the Coder+debugger escalation path | — |
| `Coder` (main Claude) | R / Python / Stata analysis scripts | `debugger` |
| `debugger` | Code quality: 12-category audit — reproducibility, alignment, polish | — |
| `economics-paper-writer` | Paper drafting with anti-hedging, effect sizes, econometric notation | `academic-proofreader` |
| `academic-proofreader` | Manuscript polish: 6-category review — structure, claims, writing, grammar | — |
| `storyteller` | Beamer / Quarto presentation builder derived from `paper/main.tex` | `discussant` |
| `discussant` | Slide quality review: layout, paper fidelity, narrative arc | — |
| `replication-verifier` | Replication audit: compilation, script execution, output freshness | — |
| `git-steward` | Repository hygiene: secrets/data/large-file audits, worktree and branch planning, cleanup, submission tags; runs state-changing git only on explicit request | — |

---

## Governance: 24 Rules

The `.claude/rules/` directory contains the operational rules Claude follows:

| Rule File | What It Governs |
|-----------|----------------|
| `adversarial-pairing.md` | Every creator has a paired critic; critics never edit |
| `data-management.md` | Data outside git, registry inside git; Dropbox roots via `.env`; no hard-coded paths; WRDS pulls via `/wrds` |
| `dependency-graph.md` | Phases activate by dependency, not sequence |
| `domain-profile.md` | Field-specific conventions, journals, data sources |
| `git-hygiene.md` | What never enters git; branching model; worktrees for parallel work; secret-rotation protocol |
| `exploration-fast-track.md` | Fast-track protocol for exploratory work |
| `exploration-folder-protocol.md` | `explorations/` folder conventions and quality gate (60/100) |
| `lessons-protocol.md` | Append-only lessons log for project-specific corrections |
| `meta-governance.md` | Generic vs specific content — what commits, what stays local |
| `orchestrator-protocol.md` | Contractor mode: dependency loop, verification, limits |
| `pdf-processing.md` | Rules for reading and extracting content from PDFs |
| `plan-first-workflow.md` | Enter plan mode for non-trivial tasks; requirements spec |
| `quality-gates.md` | Score thresholds: 80 (commit), 90 (PR), 95 (submission) |
| `research-journal.md` | Append-only agent log after every agent invocation |
| `revision-protocol.md` | R&R cycle: classify referee comments, route to agents |
| `scoring-protocol.md` | Weighted aggregation formula; type-specific weight tables |
| `separation-of-powers.md` | Critics never create; creators can't self-score |
| `session-logging.md` | Three log triggers: post-plan, incremental, end-of-session |
| `session-reporting.md` | `SESSION_REPORT.md` — consolidated append-only operations log |
| `severity-gradient.md` | Critics calibrate severity by phase: Discovery → Peer Review |
| `single-source-of-truth.md` | `paper/main.tex` is authoritative; talks derive from it |
| `standalone-access.md` | Any skill can run standalone, bypassing the pipeline |
| `table-generator.md` | Standards for generating LaTeX/Markdown tables from code |
| `three-strikes.md` | Worker-critic pairs: max 3 rounds, then escalate |

---

## Hooks

The `.claude/hooks/` directory contains Python/shell hooks that enforce workflow discipline:

All hooks are stdlib-only Python invoked as `python3` (3.9+), so they run unchanged on macOS, Linux, and Windows.

| Hook | Event | Purpose |
|------|-------|---------|
| `session-welcome.py` | SessionStart (startup/resume/clear) | Banner with project, phase, last action, next command, gates, git, data registry, lessons (via `project_state.py`) |
| `post-compact-restore.py` | SessionStart (compact) | Restores plan/task/decisions after auto-compression |
| `path-guard.py` | PostToolUse (Write/Edit on `code/**`) | Flags hard-coded home/Dropbox/drive-letter paths; points to `data_path()` |
| `journal-append.py` | PostToolUse (Agent) | **Auto-writes `quality_reports/research_journal.md`** after every research-agent dispatch: agent, phase, target, score, verdict, report path |
| `protect-files.py` | PreToolUse (Write/Edit) | Blocks edits to protected files (`paper/references.bib`, approved strategy memos, referee reports) |
| `secrets-guard.py` | PreToolUse (Bash `git commit`/`push`/`add`) | **Blocks** commits/pushes carrying credentials, `.env`/`.pgpass`/keys, data files, or blobs ≥ 20 MB; `--no-verify` overrides with a stated reason |
| `quality-gate.py` | PreToolUse (Bash `git commit`) | Blocks commits whose latest quality report scores below 80 |
| `verify-reminder.py` | PostToolUse (Write/Edit) | Reminds Claude to compile/run after editing `.tex`, `.qmd`, `.R`, `.py`, `.do`, `.jl` |
| `context-monitor.py` | PostToolUse | Progressive context-usage warnings; suggests `/learn` |
| `log-reminder.py` | Stop | Blocks stopping after 15 responses without a session-log update |
| `pre-compact.py` | PreCompact | Saves plan state + decisions before compression |
| `notify.py` | Notification | Desktop notification (macOS / Linux / Windows) |
| `post-merge.sh` | manual | Prompts for `[LEARN]` entries after a merge |

### Helper scripts (`.claude/scripts/`)

| Script | Used by | What it does |
|--------|---------|-------------|
| `profile_data.py` | `/data-profile`, `explorer` (Inventory) | Profiles csv/tsv/parquet/dta/xlsx: types, missingness, distributions, panel key & balance, treated units, staggered cohorts; writes `_profile.md` + `_codebook.csv`. Uses pandas if present, pure-Python fallback otherwise |
| `data_registry.py` | `/data-registry`, `explorer`, `code/utils/data_paths.*` | `list` / `check` / `where` / `add` / `remove` / `roots` on `data/registry.json`; resolves `${DROPBOX_ROOT}`-style templates through `.env` |
| `wrds_client.py` | `/wrds`, `explorer` | WRDS catalogue exploration and SQL `fetch` (via `wrds` package or direct psycopg2); registers pulls with the SQL as provenance; exits 3 without credentials |
| `git_tools.py` | `/git-steward`, `secrets-guard`, welcome banner | `status`, `audit`, `secrets --staged/--unpushed/--tree/--history N`, `bigfiles`, `worktree new/list/remove/prune` |
| `merge_bib.py` | `/lit-review`, `/discovery` | Appends librarian BibTeX into `paper/references.bib` without duplicates (key, DOI, title/author/year) |

---

## Terminal Status

Everything that reports project state reads one script, `.claude/scripts/project_state.py` (spec → type, journal → phase & scores & gates, git, data registry, lessons), so the four views never disagree:

| View | Where | What |
|------|-------|------|
| **Status line** | bottom of Claude Code, every turn + every 10 s (`statusLine` in `.claude/settings.json`) | `cloco · <project> · empirical · Phase 2 Strategy ▸ /identify   Commit ✓ PR ○ Submit ○ 84.5`<br>`master ↑0 ↓0 3 dirty · 1 wt │ data 4 reg · 1 missing │ ctx ▓▓▓▓░░░░░░ 38% │ Fable 5.1` |
| **Tab title** | terminal tab/window (set by the status line via OSC 0; `CLOCO_NO_TITLE=1` disables) | `cloco · Strategy · master*` — tells worktree sessions apart |
| **Welcome banner** | SessionStart hook | project, phase, last agent action, next command, gates, git, data, lessons |
| **Shell dashboard** | `make status` / `make watch` (`.claude/scripts/dashboard.py`) | the `/pipeline-status` box + git audit line, without opening Claude |

Colour cues: dirty tree on `master` in yellow, missing registered data in red, context bar yellow ≥ 70 % and red ≥ 85 %. No session cost is shown. Other `make` targets: `audit`, `data`, `wrds`, `paper`, `clean`.

## Quality Gates & Scoring

### Gates

| Score | Gate | Condition |
|-------|------|-----------|
| ≥ 95 | Submission | All individual components ≥ 80 |
| ≥ 90 | PR | Weighted aggregate |
| ≥ 80 | Commit | Weighted aggregate |
| 60 | Exploration | `explorations/` folder — advisory only |
| < 80 | Blocked | Must fix before advancing |

### Type-Specific Scoring Weights

The orchestrator reads `project_type` from the research spec and applies the matching weight column. Missing components are excluded and remaining weights are renormalized.

| Component | Source Agent | Empirical | Theory | Structural | Emp+Theory |
|-----------|-------------|:---------:|:------:|:----------:|:----------:|
| Literature coverage | `academic-editor` | 10% | 15% | 10% | 10% |
| Data quality | `data-quality-surveyor` | 10% | — | 10% | 10% |
| Theory model | `theory-critic` | — | 40% | 15% | 10% |
| Identification validity | `identification-critic` | 25% | — | — | 20% |
| Structural estimation | `structural-critic` | — | — | 20% | — |
| Code quality | `debugger` | 15% | — | 15% | 15% |
| Paper quality | blind-peer-referee avg | 25% | 30% | 20% | 25% |
| Manuscript polish | `academic-proofreader` | 10% | 15% | 5% | 5% |
| Replication readiness | `replication-verifier` | 5% | — | 5% | 5% |
| **Total** | | **100%** | **100%** | **100%** | **100%** |

---

## Quick Start

**Prerequisites:**
- [Claude Code](https://claude.ai/code): `npm install -g @anthropic/claude-code`
- [GitHub CLI](https://cli.github.com): `gh auth login`
- LaTeX distribution (for paper compilation): TeX Live or MiKTeX

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/jfimbet/cloco && cd cloco

# 2. Open CLAUDE.md and fill in your project details
#    Replace [Your Project Name] and [Your Institution]

# 3. Fill in .claude/rules/domain-profile.md with your field,
#    target journals, data sources, and identification strategies

# 4. Start Claude Code
claude

# 5. Not sure the idea is worth a paper? Ten-minute triage:
/scout "your idea in one sentence"

#    Or rescue a paper you stopped working on (PDF, .tex folder, notes, old data):
/revive ~/Dropbox/old_papers/branch_closures

# 6. On a GO verdict, formalise it and run Phase 1 in one command:
/interview-me [your research topic]
/discovery

# 7. Point the project at your data folders (once per machine) and, if you have WRDS, test it:
cp .env.example .env        # set DROPBOX_ROOT=~/Dropbox (and WRDS_USERNAME, or use ~/.pgpass)
/data-registry setup
/wrds test

# 8. Pull and profile — no manual downloads:
/wrds fetch "SELECT permno, date, ret FROM crsp.msf WHERE date >= '2010-01-01'" --name crsp_msf_2010_on
/data-profile crsp_msf_2010_on
```

That's it. The session-welcome banner tells you the next command every time you open Claude Code; `/pipeline-status` shows the full dashboard.

---

## Folder Structure

```
cloco/
├── CLAUDE.md                       # Project instructions for Claude
├── README.md                       # This file
├── SESSION_REPORT.md               # Consolidated append-only operations log
├── .gitignore
├── .claude/
│   ├── agents/                     # 21 agent definitions
│   ├── skills/                     # 39 skill definitions
│   ├── rules/                      # 24 governance rules
│   ├── hooks/                      # Workflow enforcement hooks (python3, stdlib only)
│   ├── scripts/                    # project_state.py, statusline.py, dashboard.py, profile_data.py, merge_bib.py,
│   │                               #   data_registry.py, wrds_client.py, git_tools.py, paper_intake.py
│   ├── lessons/
│   │   └── LESSONS.md              # Project-specific corrections (append-only)
│   ├── plans/ · specs/ · state/    # gitignored: plans, requirement specs, local memory
│   └── agent-memory/               # Per-agent persistent memory
├── paper/
│   ├── main.tex                    # Single source of truth
│   ├── references.bib
│   ├── sections/
│   ├── figures/
│   ├── tables/
│   └── appendix/
├── code/                           # Analysis scripts (R, Python, Stata)
│   └── utils/data_paths.{py,R}     # data_path("name") / out_path("name") — code never hardcodes a path
├── data/
│   ├── registry.json               # COMMITTED: name → ${DROPBOX_ROOT}/... template, stage, source, SQL/script
│   ├── raw/                        # gitignored scratch; canonical raw data lives in Dropbox
│   └── processed/                  # gitignored intermediates
├── .env.example                    # DROPBOX_ROOT, DATA_ROOT, WRDS_USERNAME — copy to .env (gitignored)
├── Makefile                        # make status | watch | audit | data | wrds | paper | clean
├── talks/                          # Beamer / Quarto presentations
├── output/                         # Intermediate results and logs
├── replication/                    # Replication package
├── quality_reports/
│   ├── session_logs/               # Per-session logs
│   ├── literature/<slug>/          # annotated_bibliography.md, references.bib, frontier_map.md, positioning.md
│   ├── data/<slug>/                # data_assessment.md, variable_map.csv (+ profiles/ from /data-profile)
│   ├── strategy/<slug>/            # strategy_memo.md, pseudo_code.md, robustness_plan.md, falsification_tests.md
│   ├── scout_*.md · idea_review_*.md · discovery_report_*.md
│   ├── revival/<slug>/             # inventory.md, revival_memo.md, idea_review.md, revival_plan.md (extracted/ gitignored)
│   └── research_journal.md         # Agent-level history — auto-appended by journal-append.py
├── templates/                      # Session log, quality report templates
└── master_supporting_docs/         # Reference papers and data documentation
```

---

## Customization

### 1. Fill in your domain profile

Edit `.claude/rules/domain-profile.md`:
- **Field** — your primary field and adjacent subfields
- **Target journals** — ranked by tier
- **Common data sources** — with access and quirk notes
- **Identification strategies** — the ones your field uses
- **Field conventions** — notation, clustering, welfare analysis expectations

### 2. Adjust quality thresholds

Edit `.claude/rules/quality-gates.md` to raise or lower gate thresholds for your standards. The defaults (80/90/95) are conservative.

### 3. Set your project type

When you run `/interview-me`, Claude will ask for your project type. This sets the scoring weight column used throughout the pipeline. You can also set it manually in the research spec.

### 4. Data locations and WRDS

Data is never committed; its location is. Copy `.env.example` to `.env` and set `DROPBOX_ROOT` (and `DATA_ROOT` for an external drive). Register every dataset once — `python3 .claude/scripts/data_registry.py add NAME --path '${DROPBOX_ROOT}/proj/data/x.parquet' --stage raw --source '...'` — and read it in code with `data_path("NAME")`. Keep the git repo *outside* the Dropbox folder. With WRDS credentials in `~/.pgpass` (or `WRDS_USERNAME` in `.env`), `/wrds fetch` pulls data straight to Dropbox and registers it; `pip install wrds` (or `psycopg2-binary pandas pyarrow`).

### 5. Git hygiene

The `secrets-guard` hook refuses to commit or push credentials, data files, or large blobs. `/git-steward audit` before a push after touching data or credentials; `/git-steward worktree NAME` when two streams (e.g. a referee response and new analysis) must run in parallel; `/git-steward history-scan 500` before making the repo public. See `.claude/rules/git-hygiene.md`.

### 6. Local settings

Machine-specific settings (LaTeX paths, personal tool preferences) go in `.claude/settings.local.json` (gitignored) or `.claude/state/personal-memory.md` (gitignored). These stay local — the repo only commits generic patterns.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

The upstream projects ([clo-author](https://hsantanna88.github.io/clo-author/) and [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)) are also MIT licensed.

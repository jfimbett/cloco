# CLAUDE.MD Financial Economics Research with Claude Code

<!-- 
Keep under 150 lines, since Claude loads it every session.
-->

**Project**: [Your Project Name]
**Institution**: Paris Dauphine University - PSL
**Branch**: main
**Authors**: Juan F. Imbet 

---

## Core Principles

- **Scout before you commit** -- `/scout [idea]` is a 10-minute go/no-go; run it before `/interview-me` unless the idea is already settled.
- **Plan first** -- enter plan mode before non-trivial tasks.
- **Verify after** -- compile and confirm output at the end of every task
- **Single source of truth** -- `paper/main.tex` is authoritative; talks and supplements derive from it
- **Data lives outside git; its location lives in git** -- canonical data in `${DROPBOX_ROOT}` (never a git repo inside Dropbox), scratch in `data/` (gitignored), every file in `data/registry.json`; code reads paths via `code/utils/data_paths.{py,R}`, never literals. WRDS pulls go through `/wrds`. See `.claude/rules/data-management.md`.
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `scoring-protocol.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to MEMORY.md
- **Lessons log** -- after any mistake or user correction, append an entry to `.claude/lessons/LESSONS.md`; read it at the start of every session
- **Update CLAUDE.md** -- if you find yourself writing the same instructions repeatedly, add a new command or guideline here. Also, update every time there is an important change.

---

## Folder Structure

```
[root]/
├── CLAUDE.md                   # This file: guidelines for working with Claude
├── .claude/                    # Internal files for Claude's operation (agents, skills, rules, hooks, scripts)
├── paper/                      # Main paper source files
│   ├── main.tex                # Main LaTeX file (single source of truth)
│   ├── refrences.bib           # Centralized bibliography file
│   ├── sections/               # Individual section files
│   ├── figures/                # Generated figures
│   ├── tables/                 # Generated tables
│   ├── appendix/               # Appendix materials
│   ├── online-appendix/        # Online appendix materials, if any
│   └── styles/                 # LaTeX style files, if any
├── talks/                      # Presentation materials 
├── data/                       # Scratch data only (gitignored) + the committed registry
│   ├── registry.json           # Logical name → ${DROPBOX_ROOT}/... path, stage, provenance (COMMITTED)
│   ├── raw/                    # Intermediate extracts (gitignored); canonical raw data lives in Dropbox
│   └── processed/              # Intermediate cleaned data (gitignored)
├── output/                     # Intermediate results, logs and temp files.
├── replication/                # Replication package materials
├── code/                       # All the code for the project.
│   └── utils/data_paths.{py,R} # data_path(name) / out_path(name) — the only way code touches data files
├── templates/                  # Session log, quality report templates
├── quality_reports/            # Paper quality artifacts only: scores, session logs, merge reports, research journal
├── master_supporting_docs/     # Reference papers and data docs if needed
└── .claude/
    ├── lessons/                # Lessons learned: mistakes, corrections, prevention rules
    ├── plans/                  # Agent plan files (internal, gitignored by convention)
    └── specs/                  # Requirements spec files (internal, gitignored by convention)
```

---

## Commands 

<!-- Command to compile the paper with LaTeX -->
```bash
latexmk -pdf -cd paper/main.tex        # full build (handles bib, cross-refs)
latexmk -pdf -cd -pvc paper/main.tex   # continuous preview mode (auto-recompile on save)
latexmk -cd -C paper/main.tex          # clean all auxiliary files
python3 .claude/scripts/profile_data.py data/raw/file.csv      # dataset profile + codebook
python3 .claude/scripts/data_registry.py check                         # every dataset present on this machine?
python3 .claude/scripts/wrds_client.py search crsp                     # WRDS catalogue (needs ~/.pgpass or WRDS_USERNAME in .env)
python3 .claude/scripts/merge_bib.py quality_reports/literature/<slug>/references.bib   # dedupe-merge into paper/references.bib
```

**Hooks** run with `python3` (3.9+, stdlib only). `journal-append.py` writes research-journal entries automatically after every research-agent dispatch — critics must print `**Score:** XX/100` for it to parse.

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks (reported, non-blocking) |

See `scoring-protocol.md` for weighted aggregation formula.

---


## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/scout [idea]` | Go/no-go triage: librarian + explorer quick-scans → idea-critic verdict |
| `/interview-me [topic]` | Interactive research interview → spec + domain profile |
| `/discovery` | Phase 1 in one command: lit-review ∥ find-data with critic loops + bib merge |
| `/lit-review [topic]` | Librarian + Editor: literature search + synthesis + bib merge |
| `/find-data [question]` | Explorer + Surveyor: data discovery + assessment |
| `/data-profile [name|file]` | Automated dataset profiling (panel key, treatment timing, codebook) + surveyor critique |
| `/data-registry [cmd]` | Where every dataset lives (Dropbox / local / WRDS) with provenance; `setup` on a new machine |
| `/wrds [cmd]` | Explore WRDS libraries/tables/columns and `fetch` SQL pulls straight to Dropbox, auto-registered |
| `/identify [question]` | causal-strategist + identification-critic: design identification strategy |
| `/data-analysis [dataset]` | Coder + Debugger: end-to-end analysis |
| `/draft-paper [section]` | Writer: draft paper sections + humanizer pass |
| `/econometrics-check [file]` | Econometrician: 4-phase causal inference audit |
| `/review-code [file]` | Debugger: code quality review (standalone) |
| `/proofread [file]` | Proofreader: 6-category manuscript review |
| `/paper-excellence [file]` | Multi-agent parallel review + weighted score |
| `/review-paper [file]` | 2 Referees + Editor: simulated peer review |
| `/respond-to-referee [report]` | Revision routing per revision-protocol |
| `/target-journal [paper]` | Editor: journal targeting + submission strategy |
| `/submit [journal]` | Final gate: score >= 95, all components >= 80 |
| `/create-talk [format]` | Storyteller + Discussant: Beamer talk from paper |
| `/pre-analysis-plan [spec]` | Strategist: draft PAP (AEA/OSF/EGAP) |
| `/audit-replication [dir]` | Verifier: 10-check submission audit |
| `/data-deposit` | Coder + Verifier: AEA replication package |
| `/humanizer [file]` | Strip 24 AI writing patterns |
| `/journal` | Research journal timeline |
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/validate-bib` | Cross-reference citations |
| `/commit [msg]` | Stage, commit, PR, merge |
| `/research-ideation [topic]` | Research questions + strategies → idea-critic ranking |
| `/visual-audit [file]` | Slide layout audit |
| `/learn` | Extract session discoveries into skills |
| `/context-status` | Session health + context usage |
| `/deploy` | Quarto render + GitHub Pages sync |
| `/pipeline-status [type]` | Pipeline dashboard + guide (type: empirical\|theory\|structural\|empirical+theory) |

---





# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates via dependency graph)

---

## Step −1: Scout (optional, 10 minutes)

Not sure the idea deserves a project? `/scout [idea]` runs capped literature and data quick-scans and an `idea-critic` verdict: **GO** → `/interview-me`; **REFRAME** → fix the blocking dimension; **NO-GO** → move on. Several ideas? `/research-ideation [topic]` then `/scout` the ideation report.

## Step 0: Choose Project Type

Run `/interview-me` first. Phase 0 always asks:

> "What kind of paper are you writing?"

| Type | Code | Core Deliverable |
|------|------|-----------------|
| Reduced-Form Empirical | `empirical` | Estimated causal effect |
| Pure Theory | `theory` | Propositions + proofs |
| Structural Estimation | `structural` | Estimated structural parameters |
| Empirical + Motivating Theory | `empirical+theory` | Causal estimates + theoretical motivation |

The answer is recorded as `project_type` in your research spec and determines which pipeline runs.

---

## Pipelines by Project Type

### (A) Reduced-Form Empirical

```
/interview-me (type: empirical)
    ↓
/discovery   = /lit-review ∥ /find-data + critics + bib merge
    ↓
/data-profile  (once data is downloaded — panel key, pre-period, treatment timing)
    ↓
/identify  (causal-strategist + identification-critic)
    ↓
/data-analysis  (Coder + Debugger)
    ↓
/draft-paper  (Writer + Proofreader)
    ↓
/paper-excellence → /review-paper
    ↓
/submit
```

Scoring: Literature 10% · Data 10% · Identification 25% · Code 15% · Paper 25% · Polish 10% · Replication 5%

---

### (B) Pure Theory

```
/interview-me (type: theory)
    ↓
/discovery   = /lit-review only (no data lane)
    ↓
/theory-model  (econ-finance-theorist + theory-critic)
    ↓
/draft-paper  (Writer + Proofreader)
    ↓
/paper-excellence → /review-paper
    ↓
/submit
```

Scoring: Literature 15% · Theory 40% · Paper 30% · Polish 15%
Skipped: `/find-data`, `/identify`, `/data-analysis`, `/audit-replication`

---

### (C) Structural Estimation

```
/interview-me (type: structural)
    ↓
/discovery   = /lit-review ∥ /find-data + critics + bib merge
    ↓
/data-profile
    ↓
/theory-model  (econ-finance-theorist + theory-critic)
    ↓
/structural-estimation  (structural-expert + structural-critic + Debugger)
    ↓
/draft-paper  (Writer + Proofreader)
    ↓
/paper-excellence → /review-paper
    ↓
/submit
```

Scoring: Literature 10% · Data 10% · Theory 15% · Structural 20% · Code 15% · Paper 20% · Polish 5% · Replication 5%
Skipped: `/identify`

---

### (D) Empirical + Motivating Theory

```
/interview-me (type: empirical+theory)
    ↓
/discovery   = /lit-review ∥ /find-data + critics + bib merge
    ↓
/data-profile
    ↓
/theory-model  (econ-finance-theorist + theory-critic)
    ↓
/identify  (causal-strategist + identification-critic)   ← theory predictions tested here
    ↓
/data-analysis  (Coder + Debugger)
    ↓
/draft-paper  (Writer + Proofreader)
    ↓
/paper-excellence → /review-paper
    ↓
/submit
```

Scoring: Literature 10% · Data 10% · Theory 10% · Identification 20% · Code 15% · Paper 25% · Polish 5% · Replication 5%
Skipped: `/structural-estimation`

---

Enter at any stage. Use `/new-project` for the full orchestrated pipeline.

---

## Key Skills by Research Stage

### Ideation & Discovery
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/research-ideation [topic]` | idea-critic | 3–5 research questions + strategies, critic-ranked |
| `/scout [idea]` | Librarian + Explorer (quick) → idea-critic | 10-minute go/no-go triage |
| `/interview-me [topic]` | — | Interactive Q&A → research spec + domain profile |
| `/discovery` | Librarian + Editor ∥ Explorer + Surveyor | Phase 1 in one command, critic loops, bib merge, Discovery Report |
| `/lit-review [topic]` | Librarian + Editor | Literature search + synthesis + bib merge |

### Theory & Structural
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/theory-model [spec]` | Theorist + theory-critic | Formal model + propositions |
| `/structural-estimation [spec]` | Structural-expert + structural-critic | Model estimation + fit |

### Data & Strategy
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/find-data [question]` | Explorer + Surveyor | Data discovery + quality assessment |
| `/data-registry [cmd]` | — | Where every dataset lives (Dropbox/local/WRDS); `setup` per machine, `check` before reading |
| `/wrds [cmd]` | — | Explore WRDS catalogue; `fetch` SQL → Dropbox, registered, profiled |
| `/data-profile [name\|file]` | profiler script + Surveyor | Panel key, treatment timing, codebook, critique of data in hand |
| `/identify [question]` | Strategist + identification-critic | Design identification strategy |
| `/pre-analysis-plan [spec]` | Strategist | Draft PAP (AEA/OSF/EGAP) |

### Analysis & Writing
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/data-analysis [dataset]` | Coder + Debugger | End-to-end analysis + code review |
| `/draft-paper [section]` | Writer | Paper sections + humanizer pass |
| `/compile-latex [file]` | — | 3-pass XeLaTeX + bibtex |

### Quality & Review
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/econometrics-check [file]` | Econometrician | 4-phase causal inference audit |
| `/review-code [file]` | Debugger | Code quality review (standalone) |
| `/proofread [file]` | Proofreader | 6-category manuscript review |
| `/paper-excellence [file]` | 4 parallel | Multi-agent review + weighted score |
| `/review-paper [file]` | 2 Referees + Editor | Simulated peer review |
| `/validate-bib` | — | Cross-reference citations |

### Submission & Deposit
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/target-journal [paper]` | Editor | Journal targeting + strategy |
| `/respond-to-referee [report]` | Writer + routing | Point-by-point response |
| `/data-deposit` | Coder + Verifier | AEA replication package |
| `/audit-replication [dir]` | Verifier | 10-check submission audit |
| `/submit [journal]` | Verifier + scoring | Final gate (score >= 95) |

### Presentations
| Command | Agents | What It Does |
|---------|--------|-------------|
| `/create-talk [format]` | Storyteller + Discussant | Beamer talk (4 formats) |
| `/visual-audit [file]` | — | Slide layout audit |

### Infrastructure
| Command | What It Does |
|---------|-------------|
| `/commit [msg]` | Stage, commit, PR, merge |
| `/humanizer [file]` | Strip 24 AI writing patterns |
| `/journal` | Research journal timeline |
| `/context-status` | Session health + context usage |
| `/learn` | Extract discoveries into skills |
| `/deploy` | Build + deploy to GitHub Pages |

---

## Quality Gates

| Score | Gate | What It Means |
|-------|------|--------------|
| >= 95 | Submission | Ready for top-5 (all components >= 80) |
| >= 90 | PR | Ready to submit (minor polish recommended) |
| >= 80 | Commit | Ready to commit (address major issues before submission) |
| < 80 | **Blocked** | Must fix critical/major issues |
| -- | Advisory | Talks: reported only, non-blocking |

**Type-specific default weights** (see `scoring-protocol.md` for full tables):

| Component | Empirical | Theory | Structural | Empirical+Theory |
|-----------|-----------|--------|------------|-----------------|
| Literature | 10% | 15% | 10% | 10% |
| Data quality | 10% | — | 10% | 10% |
| Theory model | — | 40% | 15% | 10% |
| Identification | 25% | — | — | 20% |
| Structural | — | — | 20% | — |
| Code quality | 15% | — | 15% | 15% |
| Paper quality | 25% | 30% | 20% | 25% |
| Polish | 10% | 15% | 5% | 5% |
| Replication | 5% | — | 5% | 5% |

---

## Worker-Critic Pairs by Research Type

| Worker | Critic | Used In |
|--------|--------|---------|
| main Claude (`/scout`, `/research-ideation`) | idea-critic | Pre-pipeline, all types (advisory) |
| academic-librarian | academic-editor | All types |
| explorer | data-quality-surveyor | empirical, structural, empirical+theory |
| econ-finance-theorist | theory-critic | theory, structural, empirical+theory |
| structural-estimation-expert | structural-critic | structural |
| causal-strategist | identification-critic | empirical, empirical+theory |
| Coder (main Claude) | debugger | empirical, structural, empirical+theory |
| economics-paper-writer | academic-proofreader | All types |

---

## I Ask You When

- **Design forks:** "Option A vs. Option B. Which?"
- **Identification choice:** "CS DiD vs. Sun-Abraham for this setting?"
- **Model design deadlock:** "Theorist and Critic can't agree — your call"
- **Disagreement with referee:** "DISAGREE classification — please review"
- **After 3 strikes:** "Worker and Critic can't converge — your call"

## I Just Execute When

- Code fix is obvious (bug, pattern)
- Verification (compilation, tolerance checks)
- Documentation (logs, commits)
- Plotting (per established standards)

---

## Data Rules (one paragraph)

Canonical data → `${DROPBOX_ROOT}` (repo is never inside Dropbox). Scratch → `data/` (gitignored). Every file → `data/registry.json` (committed). Code → `data_path("name")`, never a literal path (`path-guard` hook will nag). WRDS → `/wrds fetch`, never the web downloader. Details: `.claude/rules/data-management.md`.

## Exploration Mode

For experimental work:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research value check
- See `.claude/rules/exploration-fast-track.md`

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.

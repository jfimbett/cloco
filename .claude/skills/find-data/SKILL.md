---
name: find-data
description: Data discovery and assessment dispatching the explorer agent (finder) and data-quality-surveyor agent (critic). Searches public, administrative, survey, and novel data sources. Scores feasibility and measurement quality.
disable-model-invocation: true
argument-hint: "[research question or data requirements description]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "WebSearch", "WebFetch", "Task"]
---

# Find Data

Discover and assess datasets by dispatching the **Explorer** (data finder) and **data-quality-surveyor** (data critic).

**Input:** `$ARGUMENTS` — research question, variable requirements, or description of needed data.

---

## Workflow

### Step 1: Context Gathering

1. Read research spec if it exists (`quality_reports/research_spec_*.md`)
2. Read strategy memo if it exists (`quality_reports/strategy_memo_*.md`)
3. Read `.claude/rules/domain-profile.md` for common data sources in the field
4. Understand what variables are needed: treatment, outcome, controls, time period, geography
5. Run `python3 .claude/scripts/data_registry.py check` (what we already have) and `python3 .claude/scripts/wrds_client.py test` (do we have WRDS?) — pass both results to the explorer

### Step 2: Launch Explorer Agent

Check whether `data/raw/` or `data/processed/` already contain files. Then delegate to the `explorer` agent via Task tool:

```
Prompt: Produce a data assessment for "[research question/requirements]".
Mode: Discovery  (or: Inventory first, then Discovery for gaps — local files exist under data/)
Data requirements: outcome [..], treatment [..], unit [..], period [..], geography [..],
  design the data must support [pre/post panel | running variable | instrument | ..].
Follow your full search protocol (all nine source categories; field-standard sources first).
For each candidate record access level, unit/structure, coverage, key variables BY COLUMN NAME
where a codebook is reachable, linkage keys, feasibility grade A–D, fit to design, known issues, papers that used it.
Outputs: quality_reports/data/[slug]/data_assessment.md and variable_map.csv
  (+ local_inventory.md in Inventory mode).
```

### Step 3: Launch data-quality-surveyor Agent (Data Critic)

After Explorer returns, delegate to the `data-quality-surveyor` agent:

```
Prompt: Review the data assessment at quality_reports/data/[slug]/data_assessment.md (and variable_map.csv).
For each proposed dataset, check:
  1. Measurement validity — does the variable actually measure what we need?
  2. Sample selection — who's in the data? Who's missing?
  3. External validity — can we generalize from this sample?
  4. Identification compatibility — does this data support the proposed design?
  5. Known issues — documented problems with this dataset in the literature
Score each dataset. Flag deal-breakers.
Save critique to quality_reports/data/[slug]/data_critique.md
```

### Step 4: Synthesize Recommendations

After both agents return, present:

```markdown
# Data Assessment: [Topic]
**Date:** [YYYY-MM-DD]

## Recommended Datasets (ranked)

### 1. [Dataset Name] — Feasibility: [A/B/C/D]
- **Why:** [Best match for research question]
- **Variables:** [Key variables available]
- **Concerns:** [data-quality-surveyor's critique]
- **Access:** [How to obtain]

### 2. [Dataset Name] — Feasibility: [A/B/C/D]
...

## Rejected Datasets
| Dataset | Reason for Rejection |
|---------|---------------------|
| [Name] | [data-quality-surveyor's deal-breaker] |

## Data Gaps
[Variables needed but not found in any dataset]

## Next Steps
[Concrete actions: apply for access, download, contact provider]
```

### Step 5: Iterate and hand off

- Surveyor score < 80 → re-dispatch the explorer with the surveyor's Required Actions (max 3 rounds, then escalate to the user with a specific question).
- For WRDS-hosted picks, run the explorer's Pull Plan through `/wrds fetch` (auto-registers to `${DROPBOX_ROOT}`); for downloads, save to Dropbox and `/data-registry add`.
- Once a dataset is on disk, run `/data-profile <registered name>` — it verifies the panel key, pre-period, and treatment variation with real numbers before `/identify`.
- The `journal-append` hook logs both agent runs; add a `Data lane: PASS/FAIL` line to `quality_reports/research_journal.md` by hand.

---

## Principles

- **Explorer finds, data-quality-surveyor critiques.** Never skip the critique step.
- **Feasibility matters.** A perfect dataset you can't access is useless.
- **Domain-profile aware.** Check common data sources for the field first.
- **Measurement validity is key.** The data-quality-surveyor catches "this variable doesn't actually measure what you think."
- **Be honest about limitations.** Every dataset has them — document them upfront.

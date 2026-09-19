---
name: data-profile
description: Automated profiling of a dataset that is already on disk — variable types, missingness, distributions, panel structure (unit × time, balance, duplicates), treatment variation (treated units, staggered cohorts), and a draft codebook — followed by a data-quality-surveyor critique grounded in the real numbers. Bridges data discovery and identification. Use when data has been downloaded, when the user says "profile this", "what's in this file", "check the panel", or before /identify and /data-analysis.
disable-model-invocation: true
argument-hint: "[registered dataset NAME, a file path, or a directory] [--id COL] [--time COL] [--treat COL]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Task"]
---

# Data Profile

Turn a raw file into facts the strategist and the surveyor can act on: does the panel key hold, is there a pre-period, how many treated units, is treatment staggered, which variables are unusable.

**Input:** `$ARGUMENTS` — a file or directory path plus optional `--id`, `--time`, `--treat` column hints.

---

## Workflow

### Step 1: Locate and size

- If `$ARGUMENTS` is not an existing path, treat it as a **registry name**: `python3 .claude/scripts/data_registry.py where NAME`. Profile the resolved file. If the registry says MISSING, stop and offer `/wrds fetch` (if the entry has a `query`) or the producing script.

- If a directory: `Glob` for `*.csv *.tsv *.parquet *.dta *.xlsx *.json` (recursive). Profile each; cap at 10 files (ask the user to narrow if more).
- Files > 2 GB: warn and profile a sample (`head -n 500000` into the scratchpad) rather than the whole file.
- `.rds`/`.RData`: ask the user to export to parquet/csv (`arrow::write_parquet(df, "file.parquet")`) — the profiler does not read R binaries.

### Step 2: Run the profiler

```bash
python3 .claude/scripts/profile_data.py "<file>" --out quality_reports/data/profiles [--id COL] [--time COL] [--treat COL]
```

Outputs `quality_reports/data/profiles/<stem>_profile.md` and `<stem>_codebook.csv`. If the script reports `csv-fallback`, note that distributions are computed on at most 200k rows; suggest installing pandas (`pip install pandas pyarrow`) for full coverage.

If the script's automatic role detection picked the wrong id/time/treatment column (check the `Structure` block), re-run with explicit `--id/--time/--treat`.

### Step 3: Read the profile against the research spec

Read `quality_reports/research_spec_*.md` and, if present, `quality_reports/data/*/variable_map.csv` and `quality_reports/strategy/*/strategy_memo.md`. Then answer explicitly, in your own words:

1. **Variable map:** for each required variable (outcome, treatment, controls) — found by name / found as proxy / MISSING.
2. **Design support:** pre-period length before first treatment; never-treated units; running-variable density if RDD; instrument present if IV.
3. **Red flags from the profile:** duplicate keys, unbalanced panel, ≥30% missingness on a key variable, constant columns, staggered timing (→ CS/SA/stacked estimators, not plain TWFE).
4. **Cleaning tasks implied:** type coercions, date parsing, deduplication, unit harmonisation, top-coding, winsorisation candidates.

### Step 4: Fill the codebook

Open `<stem>_codebook.csv` and fill `label`, `source`, and `construction` for every variable you can identify from the spec, the explorer's variable map, or the provider's documentation. Leave unknowns blank rather than guessing.

### Step 5: Critic pass

Dispatch `data-quality-surveyor`:
```
Review the dataset profile at quality_reports/data/profiles/<stem>_profile.md together with
the codebook <stem>_codebook.csv and the research spec.
This is a PROFILE of data in hand, not a proposal — ground every deduction in the reported numbers
(missingness, panel balance, treated-unit counts, timing).
Score measurement validity, sample selection, external validity, identification compatibility.
Save to quality_reports/data/profiles/<stem>_critique.md
```

### Step 6: Report

```
📊 DATA PROFILE — <file>
Rows N · Cols K · Panel: <id> × <time> (units U, periods T, balanced Y/N)
Treatment: <col> — treated units X, cohorts {...}, staggered Y/N, pre-periods before first treatment: P
Variable map: outcome ✅ | treatment ✅ | controls 4/6 (missing: …)
Flags: [top 3]
Surveyor score: XX/100 — [verdict line]

Cleaning to-do (→ /data-analysis Stage 0): [3–6 bullets]
Next: /identify "[question]"  (or fix data first if the surveyor flagged a deal-breaker)
Files: quality_reports/data/profiles/<stem>_profile.md · _codebook.csv · _critique.md
```

---

## Principles

- **Numbers, not impressions.** Every claim about the data cites the profile.
- **Never modify the input file.** Cleaning is the Coder's job in `/data-analysis`.
- **Staggered timing is a design fact,** not a footnote — surface it before the strategist writes the memo.
- **The codebook is a living artefact.** The Coder extends it; the replication package ships it.

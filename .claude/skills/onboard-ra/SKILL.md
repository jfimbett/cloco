---
name: onboard-ra
description: RA onboarding audit — explore all project folders and code, inspect data files directly, and produce a structured project-state document that enables a clean restart. Use at the start of a project hand-off or when picking up work from multiple prior contributors.
argument-hint: "[optional: specific subdirectory or focus area to audit]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent", "Task"]
---

# RA Onboarding Audit

You are acting as a **new research assistant** joining the project for the first time. Your job is to survey everything that has been done, understand the state of the data and code, and produce a single document that gives future contributors (human or AI) a clear picture of where things stand and what needs to happen next.

**Input:** `$ARGUMENTS` — an optional subdirectory or focus area. If blank, audit the entire project.

---

## Guiding Principles

- **Trust nothing blindly.** Code may be broken, data may have errors, file names may be misleading. Verify by reading and running.
- **Be a detective, not a librarian.** Don't just list files — understand what each script does, whether it ran successfully, and whether its outputs match expectations.
- **Flag Duc's work explicitly.** Per project memory, one RA (Duc) has known quality issues. Any file with "duc", "Duc", or authored by Duc in a comment header must be flagged for extra verification.
- **Distinguish raw from processed.** Data files in `data/raw/` are inputs; files in `data/processed/` are derived. Understand the chain.
- **Note what is missing.** If a script references a file that doesn't exist, or a README mentions analysis not yet done, flag it.

---

## Audit Steps

### Step 1: Project Structure Scan

Map the full directory tree (skip `.git`, `__pycache__`, `.aux`, `.log`, `.synctex.gz`, binary files):

- List all directories and their purpose
- List all code files by language (R, Python, Stata, Julia, shell)
- List all data files (CSV, RDS, DTA, parquet, xlsx) with sizes
- List all output files (tables, figures, PDFs)
- List all documentation (README, CLAUDE.md, markdown notes)

Use Glob patterns:
- `**/*.R`, `**/*.py`, `**/*.do`, `**/*.jl` — code
- `**/*.csv`, `**/*.rds`, `**/*.RDS`, `**/*.dta`, `**/*.parquet`, `**/*.xlsx` — data
- `**/*.tex`, `**/*.pdf` — paper/output
- `**/*.md` — documentation

---

### Step 2: Code Audit

For each code file found, read it and record:

| File | Language | Purpose (inferred) | Inputs | Outputs | Status | RA Attribution | Issues |
|------|-----------|--------------------|--------|---------|--------|---------------|--------|
| path/script.R | R | Cleans raw auction data | data/raw/auctions.csv | data/processed/clean.rds | Appears complete | Unknown | None found |

**Status options:**
- `Complete` — script runs top to bottom with no obvious errors
- `Incomplete` — TODOs, commented-out sections, missing output files
- `Broken` — references files that don't exist, syntax errors visible
- `Unknown` — can't determine without running

**RA Attribution:** Check script headers, git blame output, or file names for authorship clues.

**Flag for Duc:** If any file is attributed to "Duc" or has naming patterns like `duc_`, `by_duc`, or similar — mark it as `⚠️ VERIFY (Duc's work)` in the Issues column.

---

### Step 3: Data Inspection

For each data file, inspect its contents directly:

**For CSV files:** Use Bash to run a quick inspection:
```bash
# Row count, column names, first few rows
python -c "import pandas as pd; df=pd.read_csv('path'); print(df.shape); print(df.columns.tolist()); print(df.head(3).to_string())"
# Or with R:
# Rscript -e "df <- read.csv('path'); cat(nrow(df), ncol(df), '\n'); print(names(df)); print(head(df, 3))"
```

**For RDS files:**
```bash
Rscript -e "df <- readRDS('path'); cat(class(df), '\n'); cat(nrow(df), ncol(df), '\n'); print(names(df)); print(head(df, 3))"
```

**For DTA (Stata) files:**
```bash
python -c "import pandas as pd; df=pd.read_stata('path'); print(df.shape); print(df.columns.tolist()); print(df.head(3).to_string())"
```

For each data file record:

| File | Rows | Columns | Key Variables | Date Range | Issues |
|------|------|---------|---------------|------------|--------|

Pay special attention to:
- Missing values in key columns
- Date/vintage year coverage
- Whether the file matches what the code expects
- Duplicate rows or obvious data quality problems

---

### Step 4: Pipeline Reconstruction

Based on Steps 2 and 3, reconstruct the data pipeline:

```
raw data → [script A] → intermediate → [script B] → final dataset → [analysis script] → outputs
```

For each step:
- Does the input file exist?
- Does the output file exist?
- Does the script that produces it appear complete?
- Are there gaps (output missing, script not written yet)?

---

### Step 5: Verification Checks

Run a targeted set of checks:

1. **Missing files:** For every `read_csv("...")`, `readRDS("...")`, `load("...")` in the code, verify the referenced file exists.
2. **Output freshness:** If a script produces `data/processed/X.rds`, check if X.rds exists and is newer than the script.
3. **Duc's work:** List every file attributed to Duc. For each, note what it claims to do and flag it for independent re-verification.
4. **Hardcoded paths:** Flag any absolute paths (e.g., `C:/Users/...`, `/home/...`) that will break on other machines.
5. **Undocumented files:** Data files with no corresponding code that creates or reads them — could be orphans or undocumented inputs.

---

### Step 6: Produce the Onboarding Document

Save to: `output/project_state_YYYY-MM-DD.md`

````markdown
# Project State: [Project Name]
**Audit Date:** YYYY-MM-DD
**Auditor:** Claude (onboard-ra skill)

---

## 1. Executive Summary

[3-5 sentences: what's been done, what's the state of the data, what are the main issues, and what should happen next]

---

## 2. Directory Map

[Annotated tree of all relevant directories]

---

## 3. Data Inventory

| File | Location | Rows | Columns | Coverage | Status | Notes |
|------|----------|------|---------|----------|--------|-------|

**Data pipeline:**
```
[reconstructed pipeline diagram]
```

---

## 4. Code Inventory

| Script | Language | Purpose | Status | RA | Issues |
|--------|----------|---------|--------|----|--------|

---

## 5. ⚠️ Items Requiring Verification

### Duc's Work
[List every file, what it claims to do, and what specifically to re-verify]

### Broken/Missing Links
[List every missing file reference]

### Hardcoded Paths
[List every absolute path found]

---

## 6. Pipeline Gaps

[What analysis is referenced in documentation but not yet coded?]
[What data is expected but not yet available?]
[What outputs are missing?]

---

## 7. Recommended Next Steps

Prioritized list of actions to bring the project to a clean, reproducible state:

1. [Highest priority — e.g., re-verify Duc's cleaning script]
2. [Second priority]
3. ...

---

## 8. Open Questions for the Team

[Questions that can only be answered by the research team, not by reading the files]
````

---

## Output

When complete, report to the user:

1. A brief verbal summary (3-5 sentences on the state of the project)
2. The path to the saved `project_state_YYYY-MM-DD.md`
3. The top 3 action items
4. Any critical blockers (missing data, broken scripts, Duc verification items)

---
name: verify-citations
description: Full bibliography audit for an academic paper. Verifies every citation is (1) structurally correct in the .bib file, (2) actually cited in the paper, and (3) a real publication — author names, year, journal, and title verified via web search. Flags hallucinated or inaccurate references.
allowed-tools: ["Read", "Grep", "Glob", "Write", "Agent", "WebSearch"]
---

# Verify Citations

Full three-layer audit: structural integrity → cross-reference → hallucination check.

**Input:** `<bib_file>` — path to .bib file. Defaults to `paper/references.bib`.

---

## Workflow

### Step 1: Extract all citation keys used in the paper

Grep all `.tex` files under `paper/` for citation commands:
```
\cite{, \citet{, \citep{, \citeauthor{, \citeyear{, \citealt{, \nocite{
```
Collect every unique citation key referenced in the paper.

### Step 2: Parse the .bib file

Read `<bib_file>` (default `paper/references.bib`) and extract for each entry:
- Citation key
- Entry type (`@article`, `@book`, `@incollection`, `@working paper`, etc.)
- Required fields: `author`, `title`, `year`, `journal` (or `booktitle` / `publisher`)
- Optional fields: `volume`, `number`, `pages`, `doi`, `url`

### Step 3: Structural audit (no web needed)

For each bib entry:

| Check | Severity | Flag |
|-------|----------|------|
| Citation key in paper but not in .bib | CRITICAL | Missing entry |
| Entry in .bib but not cited anywhere | INFO | Unused entry |
| Required field missing (author/title/year/journal) | MAJOR | Incomplete entry |
| Year outside plausible range (< 1900 or > current year + 1) | MAJOR | Implausible year |
| Author field not in `Lastname, Firstname` or `Firstname Lastname` format | MINOR | Formatting |
| Malformed characters or encoding issues | MINOR | Encoding |
| Duplicate citation keys | CRITICAL | Duplicate |

### Step 4: Hallucination / accuracy audit (web verification)

**This is the core new capability.** For every citation key that IS cited in the paper, dispatch a web-search verification agent.

Launch a `general-purpose` agent with the following prompt template for each batch of 5–10 entries (batch to reduce agent count):

```
You are verifying whether academic citations are real and accurate.
For each entry below, search the web (Semantic Scholar, Google Scholar, SSRN, NBER, journal websites)
to verify:
  1. Does a paper with this title actually exist?
  2. Are the authors correct (right names, right order)?
  3. Is the year correct?
  4. Is the journal/venue correct?
  5. Is the DOI or URL resolvable (if present)?

For each entry, return one of:
  - VERIFIED: all fields confirmed
  - LIKELY OK: paper exists but minor discrepancy (e.g. slightly different title spelling)
  - SUSPECT: paper may not exist or fields are wrong — explain what you found
  - HALLUCINATED: paper definitively does not exist with these details

Entries to verify:
[paste bib entries here]

Return a structured table: Key | Status | Notes
```

Run verification agents in parallel (max 3 agents simultaneously, each handling a batch).

### Step 5: Compile the report

Save to `quality_reports/citation_audit.md` using this format:

```markdown
# Citation Audit Report
**Date:** YYYY-MM-DD
**Bib file:** paper/references.bib
**Paper:** paper/main.tex

## Summary
- Total entries in .bib: N
- Total citations used in paper: N
- Unused entries: N
- CRITICAL issues: N
- MAJOR issues: N
- Hallucination suspects: N

## CRITICAL Issues (must fix before submission)
[List with bib key, issue, fix]

## MAJOR Issues
[List with bib key, issue, recommendation]

## Hallucination / Accuracy Flags
| Key | Status | Filed As | What Web Search Found |
|-----|--------|----------|-----------------------|
...

## Unused Entries (informational)
[List of keys in .bib but not cited]

## VERIFIED entries
[Count only — full list omitted for brevity]

## MINOR Issues
[List]
```

### Step 6: Present summary to user

Report:
- Total citations audited
- Any CRITICAL or hallucinated entries (full detail)
- Any MAJOR structural issues
- Count of verified entries
- Path to full report

---

## Principles

- **Web-first for hallucination.** Do not rely on the model's training knowledge to verify a citation — always search the web. Training data can itself contain hallucinated references.
- **SSRN and NBER first** for working papers; journal websites for published articles; Semantic Scholar as a broad fallback.
- **Flag, don't delete.** The skill reports issues; the author decides what to fix.
- **Conservative on HALLUCINATED.** Only mark as HALLUCINATED if multiple searches find no evidence of the paper. Use SUSPECT for ambiguous cases.
- **DOI is ground truth.** If a DOI is present and resolves correctly, treat the entry as VERIFIED even if other fields have minor discrepancies.

---

## Files to scan (default)
```
paper/**/*.tex
paper/appendix/*.tex
```

## Bibliography location (default)
```
paper/references.bib
```

## Output
```
quality_reports/citation_audit.md
```

---
name: lit-review
description: Structured literature search dispatching the academic-librarian agent for collection and academic-editor agent for coverage critique. Searches top-5 journals, NBER/SSRN, and field journals. Produces synthesis with gap identification and BibTeX entries.
disable-model-invocation: true
argument-hint: "[topic, paper title, or research question]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "WebSearch", "WebFetch", "Task"]
---

# Literature Review

Conduct a structured literature search and synthesis by dispatching the **academic-librarian** (collector) and **Editor** (critic).

**Input:** `$ARGUMENTS` — a topic, paper title, research question, or phenomenon to investigate.

---

## Workflow

### Step 1: Context Gathering

1. Parse the topic from `$ARGUMENTS`
2. Read `.claude/rules/domain-profile.md` for field-specific journal tiers and seminal references
3. Check `master_supporting_docs/` for uploaded papers
4. Read `paper/references.bib` for papers already in the project

### Step 2: Launch academic-librarian Agent

Delegate to the `academic-librarian` agent via Task tool:

```
Prompt: Search for literature on "[topic]".
Search protocol:
  1. Top-5 journals (AER, Econometrica, QJE, JPE, REStud)
  2. Field journals from domain-profile.md
  3. NBER/SSRN/IZA working papers
  4. Citation chains (forward + backward from key papers)
Assign proximity scores (1-5) to each paper found.
Produce annotated bibliography with BibTeX entries.
Save to quality_reports/lit_review_[sanitized_topic].md
```

### Step 3: Launch Editor Agent (Lit Critic Mode)

After academic-librarian returns, delegate to the `academic-editor` agent:

```
Prompt: Review the literature collection at quality_reports/lit_review_[topic].md.
Mode: Literature critic (Phase 1).
Check for:
  - Coverage gaps (missing seminal papers, missing strands)
  - Journal quality distribution (too many working papers?)
  - Scope appropriateness (too broad or too narrow?)
  - Missing methodological context
Flag gaps for academic-librarian to fill.
```

### Step 4: Fill Gaps (if needed)

If Editor identifies gaps:
1. Re-dispatch academic-librarian for targeted searches (max 1 round)
2. Merge new findings into the report

### Step 5: Merge BibTeX into the paper

`paper/references.bib` is protected from direct edits. Append the librarian's entries without duplicates:

```bash
python3 .claude/scripts/merge_bib.py quality_reports/literature/[slug]/references.bib --target paper/references.bib
```

Report entries added vs skipped (duplicates by key, DOI, or title/author/year).

### Step 6: Present Results

```markdown
# Literature Review: [Topic]
**Date:** [YYYY-MM-DD]
**Query:** [Original query]

## Summary
[2-3 paragraph overview of the state of the literature]

## Key Papers
### [Author (Year)] — [Short Title]
- **Journal:** [venue]
- **Proximity:** [1-5 score]
- **Main contribution:** [1-2 sentences]
- **Identification strategy:** [DiD / IV / RDD / SC / descriptive]
- **Key finding:** [result with effect size]
- **Relevance:** [why it matters for our research]

## Thematic Organization
### Theoretical Contributions
### Empirical Findings
### Methodological Innovations

## Gaps and Opportunities
1. [Gap 1 — what's missing and why it matters]
2. [Gap 2]

## Research Frontier
### Active Debates
### Recent Working Papers to Watch
### Emerging Methods

## Suggested Next Steps

## BibTeX Entries
```bibtex
@article{...}
```
```

---

## Principles

- **Be honest about uncertainty.** If you cannot verify a citation, mark as `% UNVERIFIED`.
- **Prioritize published work** over working papers. Note publication status.
- **Note when WPs became published** — cite the published version.
- **Do NOT fabricate citations.** Flag any uncertain details.
- **Identification strategy is key.** Always note how each paper identifies effects.
- **Effect sizes matter.** Report magnitudes, not just signs.
- **Proximity scoring:** 5 = directly competes, 1 = background/foundational (matches the librarian's scale).
- **Need a fast read instead?** `/scout [idea]` runs a capped quick-scan (8 papers) plus a go/no-go verdict; run this full review once the idea is a GO.
- **Running Phase 1 end-to-end?** `/discovery` runs this skill and `/find-data` in parallel with critic loops and the bib merge.

---
name: Analysis script code patterns
description: Recurring code quality patterns in code/analysis/ Python scripts -- path conventions, duplication, save patterns
type: project
---

Scripts 05 and 06 use `ROOT = Path(__file__).resolve().parent.parent.parent` for paths -- this is the project convention. Scripts 07 and 08 use bare relative paths (`"data/processed/..."`) which breaks the convention.

Scripts 07 and 08 are exploratory/diagnostic and save nothing to disk -- all output is console-only. Script 09 is the paper-output generator and saves all tables/figures correctly.

**Why:** The coder likely wrote 07/08 as quick exploratory scripts and never promoted them to pipeline-quality. Script 09 consolidates the final outputs.

**How to apply:** On future reviews, check that any script whose results feed the paper uses ROOT-anchored paths and saves structured output. Flag exploratory scripts that remain console-only if their results are cited in the paper.

Hardcoded statistics in 09_paper_tables_figures.py Appendix Table A3 (lines 511-544) are a reproducibility risk -- values are manually transcribed from script 05 output rather than computed.

Massive data-loading code duplication across 07, 08, 09 (identical parquet load + filter + age_norm computation). Recommend shared utility module.

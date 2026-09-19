# Session Log — 2026-09-19 — /revive skill

**Goal:** Add a skill that rescues an abandoned working paper (old PDF, notes, data, code) and re-enters the pipeline with the sunk work reused.

**Approach:** Standalone `/revive [path]` (scout delegates path inputs to it): stdlib intake script → reconstruction memo → gap interview → librarian/explorer "what changed since" → idea-critic Revival mode (REVIVE / REFRAME / RETIRE, re-entry phase) → pre-filled spec + revival plan.

**Decisions:**
- Not a `/scout` mode: different inputs (files) and outputs (spec + plan). `/scout` hands paths over.
- Intake never copies or edits user files; data registered in place (`--stage external`); extracted text gitignored.
- Revival verdict advisory, same cut-offs as scout (75 / 55).

**Verification:** synthetic fixture (tex, compiled pdf, bib, R + Stata, csv dup, NOTES.md) → correct title/JEL/period/sources/methods/stall hints; PDF-only input; missing path exit 2; welcome hook + journal regex under python3 3.9.

**Open:** real-world run on an actual drawer paper; `pdftotext` not installed on this machine (pypdf 6.x is, and works).

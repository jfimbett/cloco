---
name: Dimson citation propagation error
description: The dimson2015 BibTeX key cites the wrong paper (art beliefs instead of wine prices); error propagated to domain profile, research spec, and theory model
type: project
---

The `dimson2015` entry in `paper/refrences.bib` is for "Eye of the Beholder" (Dimson, Mahajan & Spaenjers 2015, RFS) -- an art market paper. The correct anchor paper is "The Price of Wine" (Dimson, Rousseau & Spaenjers 2015, JFE Vol. 118). The error has propagated to:
- `.claude/rules/domain-profile.md` (seminal references table)
- `quality_reports/research_spec_liquid_assets.md` (motivation section)
- `quality_reports/theory_model_2026-03-29.md` (positioning paragraph)

**Why:** Two Dimson/Spaenjers papers published in 2015 with partially overlapping author sets. Easy to confuse.
**How to apply:** When correcting, must fix all four locations. The librarian flagged this correctly but the BibTeX was never updated.

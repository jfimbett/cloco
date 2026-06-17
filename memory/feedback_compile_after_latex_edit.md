---
name: feedback-compile-after-latex-edit
description: After every edit to any .tex file in paper/, compile immediately with latexmk
metadata:
  type: feedback
---

After every modification to any `.tex` file in `paper/` (including sections, appendix, main.tex, or references.bib), compile the paper immediately using:

```
latexmk -pdf -cd paper/main.tex
```

Do not batch LaTeX edits and compile only at the end. Compile after each individual edit so errors are caught immediately and traced to the specific change that caused them.

**Why:** User explicitly requested this — LaTeX errors compound quickly across sections; compiling per-edit localizes the failure to the exact change.

**How to apply:** Any time a Write or Edit tool call touches a `.tex` or `.bib` file in `paper/`, the next action must be a Bash call running `latexmk -pdf -cd paper/main.tex`. No exceptions.

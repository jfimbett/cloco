# Design: Co-author Markdown Editing Pipeline

**Date:** 2026-05-16  
**Status:** APPROVED  
**Context:** Frank Fabozzi needs to edit paper prose without knowing LaTeX. Converting the multi-file LaTeX paper to a single Pandoc Markdown file enables plain-text editing; a compile script regenerates the PDF.

---

## Goal

Produce `paper/paper_coauthor.md` — a single Markdown file containing all prose-heavy sections of the paper — plus a one-command build pipeline that converts it back to a compilable LaTeX document and PDF.

---

## Files Created

| File | Purpose |
|------|---------|
| `paper/paper_coauthor.md` | Frank's editing file — single source for main body |
| `compile_md.py` | Build script at project root: pandoc → latexmk → PDF |
| `paper/main_from_md.tex` | Thin LaTeX wrapper with preamble; inputs pandoc output |

## Files Untouched

| File | Reason |
|------|--------|
| `paper/main.tex` | Original stays as backup |
| `paper/sections/*.tex` | Original section files preserved |
| `paper/appendix/appendix.tex` | Too math-heavy; not for Frank to edit |
| `paper/sections/figures.tex` | Pure `\begin{figure}` blocks; not prose |
| `paper/references.bib` | Bibliography unchanged |

---

## `paper_coauthor.md` — Content Scope

Sections included (in order):
1. Introduction (`sections/introduction.tex`)
2. The Model (`sections/model.tex`)
3. The Contract (`sections/contract.tex`)
4. Calibration (`sections/calibration.tex`)
5. Numerical Results (`sections/numerical.tex`)
6. Conclusion (`sections/conclusion.tex`)

Sections excluded (remain as `.tex`, referenced from wrapper):
- Figures section — pure LaTeX float blocks
- Appendix — dense math derivations
- Title page — stays in wrapper
- Bibliography call — stays in wrapper

---

## Conversion Rules

| LaTeX construct | Markdown equivalent |
|----------------|-------------------|
| `\section{X}` + `\label{sec:y}` | `# X {#sec:y}` |
| `\subsection{X}` | `## X` |
| `\subsubsection{X}` | `### X` |
| `\emph{X}` | `*X*` |
| `\textbf{X}` | `**X**` |
| `\footnote{X}` | `^[X]` (Pandoc inline footnote) |
| Simple unnested display math | `$$...$$` |
| `\begin{equation}` with `\label` | kept as raw LaTeX block |
| `\begin{align}`, `\begin{cases}` | kept as raw LaTeX block |
| `\citep{}`, `\citet{}` | kept as raw LaTeX (pass-through) |
| `\ref{sec:...}`, `\eqref{...}` | kept as raw LaTeX (pass-through) |

A comment block at the top of the `.md` file instructs Frank:
- Edit prose freely
- Skip `\begin{...} ... \end{...}` blocks (math environments)
- Do not change citation keys inside `\citep{}` / `\citet{}`

---

## `main_from_md.tex` — Wrapper Structure

```
[full preamble from main.tex — packages, macros, theorems]
\begin{document}
[title page from main.tex]
\doublespacing
\pagenumbering{arabic}
\setlength{\parindent}{1cm}

\input{sections_from_md}     ← pandoc output goes here

\pagebreak
\input{sections/figures}
\pagebreak
\addcontentsline{toc}{section}{References}
\bibliographystyle{chicago}
\bibliography{references}
\clearpage
\appendix
\input{appendix/appendix}
\end{document}
```

---

## `compile_md.py` — Build Script

```python
# compile_md.py — lives at project root. Run: python compile_md.py
import subprocess, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))  # project root

steps = [
    # 1. Convert markdown → latex body
    ["pandoc",
     "paper/paper_coauthor.md",
     "--from", "markdown+raw_tex",
     "--to", "latex",
     "--output", "paper/sections_from_md.tex"],
    # 2. Compile to PDF
    ["latexmk", "-pdf", "-cd", "paper/main_from_md.tex"],
]

for cmd in steps:
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}")
        sys.exit(1)

print("Done — PDF at paper/main_from_md.pdf")
```

---

## Roundtrip Fidelity

- Prose, footnotes, section structure: exact
- Equations with `\label{}`: exact (raw LaTeX passthrough)
- Citations and cross-references: exact (raw LaTeX passthrough)
- Preamble macros (`\Sharpe`, `\Kcal`, etc.): exact (defined in wrapper, not converted)
- Minor cosmetic differences possible in whitespace/spacing; do not affect PDF output

---

## Dependencies

- **Pandoc** — `winget install pandoc` (Windows) or `brew install pandoc` (Mac)
- **latexmk** — already installed (used for existing paper compilation)
- **Python 3** — already available

---

## Out of Scope

- Converting appendix or figures section to Markdown
- Changing bibliography format (stays natbib/chicago)
- Roundtrip editing (Frank edits `.md`; changes are NOT automatically synced back to `sections/*.tex`)

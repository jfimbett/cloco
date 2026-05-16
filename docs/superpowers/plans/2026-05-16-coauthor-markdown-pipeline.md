# Co-author Markdown Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce `paper/paper_coauthor.md` (single editable Markdown file of the paper body), `paper/main_from_md.tex` (LaTeX wrapper with preamble), and `compile_md.py` (build script) — and verify the resulting PDF compiles.

**Architecture:** Pandoc converts `paper_coauthor.md` (Markdown + raw LaTeX passthrough) → `paper/sections_from_md.tex` (LaTeX body). `main_from_md.tex` wraps it with the existing preamble. `latexmk` produces the PDF.

**Tech Stack:** Pandoc (`pandoc --from markdown+raw_tex --to latex`), Python 3 subprocess, latexmk/pdflatex

---

## Conversion rules (applied in Task 1)

| LaTeX | Markdown |
|---|---|
| `\section{X}` + `\label{sec:y}` (next line) | `# X {#sec:y}` |
| `\subsection{X}` + `\label{y}` (next line) | `## X {#y}` |
| `\subsection{X}` (no label) | `## X` |
| `\texorpdfstring{$x$}{x_text}` in header | `$x$` |
| `\footnote{TEXT}` | `^[TEXT]` |
| All display math (`\begin{equation}`, `\begin{align}`, `\[...\]`) | kept as raw LaTeX block |
| Inline `$...$` | kept as-is |
| `\citep{}`, `\citet{}` | kept as raw LaTeX |
| `\ref{}`, `\eqref{}`, `\label{}` | kept as raw LaTeX |
| `\begin{remark}...\end{remark}` | kept as raw LaTeX |

---

## Task 1: Create `paper/paper_coauthor.md`

**Files:**
- Create: `paper/paper_coauthor.md`

- [ ] **Step 1: Write the file**

The file starts with an editing guide comment block, then contains all 6 sections with the conversion rules applied. Key structural notes:

- Header comment explains editing rules to Frank
- Sections in order: Introduction, The Model, Contract Design, Calibration, Numerical, Conclusion
- All display math kept as raw LaTeX blocks (not converted to `$$...$$`)
- All inline math kept as `$...$`
- All citations and cross-refs kept as raw LaTeX
- `\footnote{}` → `^[...]`
- `\section{}`+`\label{}` → `# Title {#label}`

Full file content: created in execution step.

- [ ] **Step 2: Verify structure**

```bash
grep -n "^#" paper/paper_coauthor.md
```
Expected output (6 top-level sections, subsections indented):
```
# Introduction {#sec:introduction}
# The Model {#sec:environment}
## Setup
## Manager's problem and incentives {#sec:manager}
## Incentive compatibility: Implementing a target $\sigma_d$ {#subsec:IC}
# Contract Design: Investor's Problem {#sec:contract}
## Investor's Problem and Equilibrium {#sec:investor}
# Calibration {#sec:calibration}
# Numerical Illustration {#sec:numerical}
# Conclusion {#sec:conclusion}
```

- [ ] **Step 3: Commit**

```bash
git add paper/paper_coauthor.md
git commit -m "feat: add coauthor markdown file for Frank's editing"
```

---

## Task 2: Create `paper/main_from_md.tex`

**Files:**
- Create: `paper/main_from_md.tex`
- Reference: `paper/main.tex` (copy preamble + structure verbatim, change only the section inputs)

- [ ] **Step 1: Write the wrapper**

Content = `main.tex` verbatim except replace:
```latex
\input{sections/introduction}
\input{sections/model}
\input{sections/contract}
\input{sections/calibration}
\input{sections/numerical}
\input{sections/conclusion}
```
with:
```latex
\input{sections_from_md}
```

Keep unchanged: title page, `\pagebreak\input{sections/figures}`, bibliography call, appendix input.

- [ ] **Step 2: Commit**

```bash
git add paper/main_from_md.tex
git commit -m "feat: add main_from_md.tex wrapper for pandoc pipeline"
```

---

## Task 3: Create `compile_md.py`

**Files:**
- Create: `compile_md.py` (project root)

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""
compile_md.py — Convert paper/paper_coauthor.md to PDF via pandoc + latexmk.
Usage: python compile_md.py
"""
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\nFAILED at step: {' '.join(cmd)}")
        sys.exit(1)


# Step 1: Markdown → LaTeX body (pandoc, no standalone = body only)
run([
    "pandoc",
    "paper/paper_coauthor.md",
    "--from", "markdown+raw_tex",
    "--to", "latex",
    "--output", "paper/sections_from_md.tex",
])

# Step 2: Compile to PDF
run(["latexmk", "-pdf", "-cd", "paper/main_from_md.tex"])

print("\n✓ Done — PDF at paper/main_from_md.pdf")
```

- [ ] **Step 2: Commit**

```bash
git add compile_md.py
git commit -m "feat: add compile_md.py build script for coauthor pipeline"
```

---

## Task 4: Run and verify

**Files:**
- Generated: `paper/sections_from_md.tex` (pandoc output, intermediate)
- Generated: `paper/main_from_md.pdf` (final output)

- [ ] **Step 1: Check pandoc is installed**

```bash
pandoc --version
```
Expected: version string. If missing: `winget install pandoc`

- [ ] **Step 2: Run compile_md.py**

```bash
python compile_md.py
```
Expected: no errors, ends with `✓ Done — PDF at paper/main_from_md.pdf`

- [ ] **Step 3: Verify PDF exists and has content**

```bash
ls -la paper/main_from_md.pdf
```
Expected: file exists, size > 500KB

- [ ] **Step 4: Spot-check pandoc output**

```bash
head -80 paper/sections_from_md.tex
```
Expected: LaTeX section commands, no `\documentclass` (body only).

- [ ] **Step 5: Commit generated wrapper (not sections_from_md.tex — that's intermediate)**

```bash
git add compile_md.py paper/main_from_md.tex paper/paper_coauthor.md
git commit -m "feat: complete coauthor markdown pipeline — compiles to PDF"
```

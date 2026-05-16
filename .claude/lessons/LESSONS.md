# Lessons Learned

Append-only log of mistakes, corrections, and prevention strategies.
Read this at the start of every session. Never edit or delete past entries.

### 2026-05-16 — pandoc/latex
**Mistake:** Used `\[...\]` display math blocks in a Pandoc Markdown file intended for `--from markdown+raw_tex`. Pandoc 3.8 treats `\[` as an escaped bracket `{[}` rather than display math, causing fatal LaTeX errors (`\mathbb allowed only in math mode`).
**Correction:** Use `$$...$$` for unnumbered display math in Pandoc Markdown files. Reserve `\begin{equation}`, `\begin{align}` etc. (with `\begin{...}`) for numbered equations — Pandoc correctly passes those through as raw LaTeX.
**Prevention:** When writing a `.md` file destined for pandoc LaTeX output, never use `\[...\]`; always use `$$...$$` for unlabeled display math. Also replace `~\ref{...}` and `~\eqref{...}` with a plain space ` \ref{...}` — Pandoc converts `~` to `\textasciitilde{}` which produces a visible tilde character in the output.

---

## Format

```
### YYYY-MM-DD — [Category]
**Mistake:** What went wrong or what was done incorrectly.
**Correction:** What the right approach is.
**Prevention:** Concrete rule or check to avoid repeating this.
```

Categories: `workflow` · `tools` · `writing` · `econometrics` · `code` · `latex` · `agents` · `planning`

---

<!-- New lessons go below this line, most recent first -->

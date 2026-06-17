---
name: migrate-overleaf
description: Sync the overleaf/ folder with the current content of paper/. Copies all LaTeX source, figures, tables, appendix, and bibliography. Puts the model section as overleaf/model.tex (top-level) for easy coauthor access. Run whenever paper/ changes and you want to push to Overleaf.
allowed-tools: ["Bash", "Read", "Write", "Glob"]
---

# Migrate paper/ → overleaf/

Sync the `overleaf/` folder with the current state of `paper/`. This is a one-way sync: `paper/` is the source of truth; `overleaf/` is the Overleaf-ready export.

## Steps

### 1. Recreate directory structure

```bash
mkdir -p overleaf/sections overleaf/figures overleaf/tables overleaf/appendix
```

### 2. Copy section files (all except 03_model)

```bash
cp paper/sections/01_introduction.tex  overleaf/sections/
cp paper/sections/02_data.tex          overleaf/sections/
cp paper/sections/04_empirics.tex      overleaf/sections/
cp paper/sections/05_results.tex       overleaf/sections/
cp paper/sections/06_conclusion.tex    overleaf/sections/
```

### 3. Copy model section to top-level (coauthor-visible)

```bash
cp paper/sections/03_model.tex overleaf/model.tex
```

The model lives at `overleaf/model.tex` (not buried in `sections/`) so coauthors can find it immediately in Overleaf's file tree.

### 4. Copy figures, tables, appendix, bibliography

```bash
cp paper/figures/*.pdf    overleaf/figures/ 2>/dev/null || true
cp paper/figures/*.png    overleaf/figures/ 2>/dev/null || true
cp paper/tables/*.tex     overleaf/tables/
cp paper/appendix/*.tex   overleaf/appendix/
cp paper/references.bib    overleaf/
```

### 5. Write overleaf/main.tex

Write `overleaf/main.tex` as an exact copy of `paper/main.tex` with ONE change:
- Replace `\input{sections/03_model}` with `\input{model}`

Read `paper/main.tex` first, then write `overleaf/main.tex` with that substitution.

### 6. Verify

Run a quick sanity check:
```bash
diff <(grep "\\\\input" paper/main.tex) <(grep "\\\\input" overleaf/main.tex)
```

Expected diff: only the model line differs (`sections/03_model` → `model`).

Count files:
```bash
echo "Sections: $(ls overleaf/sections/ | wc -l)"
echo "Figures:  $(ls overleaf/figures/  | wc -l)"
echo "Tables:   $(ls overleaf/tables/   | wc -l)"
echo "Appendix: $(ls overleaf/appendix/ | wc -l)"
```

### 7. Report

Print a summary:
```
overleaf/ synced from paper/
  Sections:   N files (+ model.tex at top level)
  Figures:    N files
  Tables:     N files
  Appendix:   N files
  Bib:        references.bib
  Model:      overleaf/model.tex  ← coauthors edit this
```

## Notes

- `overleaf/` is committed to git — coauthors pull it and upload to Overleaf
- `paper/` is always the local source of truth; never edit `overleaf/` files locally
- If a new section is added to `paper/sections/`, add a copy step here
- Figures must be PDF or PNG; Overleaf supports both
- The `endfloat` package is included — coauthors may need to install it in Overleaf (it is available in Overleaf's TeX Live distribution by default)

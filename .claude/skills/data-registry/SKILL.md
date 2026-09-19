---
name: data-registry
description: Show, verify, and maintain the project's data registry (data/registry.json) — the committed map of where every dataset lives (Dropbox, project data/ folder, external drive) with provenance. Use when the user asks "where is the data", "register this file", "check the data paths", or before any script reads a dataset. Also sets up .env roots on a new machine.
disable-model-invocation: true
argument-hint: "[list | check | where NAME | add NAME --path ... --stage ... --source ... | setup]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Edit"]
---

# Data Registry

Data lives outside git (Dropbox for canonical files, `data/` gitignored for intermediates). `data/registry.json` is the committed record of **where** each dataset is and **how** it was produced. This skill keeps it honest.

**Input:** `$ARGUMENTS` — a subcommand; empty means `check`.

---

## Subcommands

### `setup` — first run on a new machine
1. If `.env` does not exist, copy `.env.example` to `.env`.
2. Run `python3 .claude/scripts/data_registry.py roots`. For every `✗` root, ask the user for the correct folder (e.g. `~/Dropbox`, `~/Library/CloudStorage/Dropbox`, an external drive) and write it to `.env` as `DROPBOX_ROOT=...` / `DATA_ROOT=...`.
3. Ensure `data/raw/` and `data/processed/` exist (`mkdir -p`), and that `.gitignore` excludes their contents.
4. Run `check` and report.

### `list`
`python3 .claude/scripts/data_registry.py list` — print the table. Add one line per entry on **what it is for** if the description is empty (ask the user; then `add --force` with `--description`).

### `check` (default)
`python3 .claude/scripts/data_registry.py check`. For every `✗`:
- **unset variable** → run `setup` for that root
- **MISSING** → the file is not on this machine. If the registry has a `query` (WRDS) offer `/wrds fetch` to re-pull; if it has a `script`, offer to run it; otherwise tell the user which Dropbox folder to sync.

### `where NAME`
Print the resolved absolute path. Use this before any `Read`/`Bash` on data.

### `add NAME --path TEMPLATE --stage STAGE --source SOURCE [...]`
Register a file. Enforce:
- `--path` uses `${DROPBOX_ROOT}` or `${DATA_ROOT}` for anything canonical; `${PROJECT_ROOT}/data/...` only for `intermediate` stage
- `--source` names the provider or the producing script; add `--query` for SQL pulls and `--depends` for derived files
- After registering, suggest `/data-profile NAME` if the file is tabular

### `remove NAME`
Unregister (never deletes the file).

---

## Output to the user

```
📁 DATA REGISTRY — N datasets
Roots: DROPBOX_ROOT ✓ ~/Dropbox   DATA_ROOT ✗ (unset)
✓ crsp_msf_2000_2023   raw          parquet   1.2GB   ${DROPBOX_ROOT}/cloco/data/raw/crsp_msf_2000_2023.parquet
✗ panel_clean          processed    MISSING   → run code/02_build_panel.R
Problems: 1 — [what to do]
```

---

## Principles

- **Registry before file.** If it is not registered, scripts must not read it.
- **Templates, not absolute paths.** `${DROPBOX_ROOT}/...` works on every machine; `/Users/juan/Dropbox/...` works on one.
- **Provenance is mandatory.** Source + query/script + date for every entry.
- **Never touch Dropbox contents from git.** The repo is never inside the Dropbox folder and vice-versa.

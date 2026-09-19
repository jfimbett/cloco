# data/

Nothing in this folder is tracked by git except `registry.json`, this README, and `.gitkeep` files.

- `registry.json` — committed map of every dataset: logical name → `${VAR}` path template, stage, source, SQL/script provenance. Maintain with `python3 .claude/scripts/data_registry.py` or `/data-registry`.
- `raw/`, `processed/` — **scratch only** (gitignored). Canonical data lives in `${DROPBOX_ROOT}/<project>/data/` outside the repo.
- Roots are set per machine in `.env` (see `.env.example`).

See `.claude/rules/data-management.md`.

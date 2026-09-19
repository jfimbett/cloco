---
paths:
  - "data/**"
  - "code/**"
  - "replication/**"
---

# Data Management: Registry, Dropbox, and WRDS

**Data never lives in git. Its location always does.**

## Where data lives

| Kind | Location | In git? |
|------|----------|---------|
| Canonical raw pulls, licensed data, anything that must survive a laptop | `${DROPBOX_ROOT}/<project>/data/...` (Dropbox or any synced folder **outside** the repo — we do not put git repos inside Dropbox) | No |
| Intermediate / scratch files (samples, cache, one-off extracts) | `data/raw/`, `data/processed/` inside the repo | No — gitignored |
| The **registry** of where every dataset is, with provenance | `data/registry.json` | **Yes** |
| Machine-specific roots (`DROPBOX_ROOT`, `DATA_ROOT`, WRDS username) | `.env` | No — gitignored; `.env.example` is committed |
| Codebooks, profiles, variable maps | `quality_reports/data/` | Yes |

## The registry is the source of truth

`data/registry.json` maps a **logical name** (`crsp_msf_2000_2023`) to a **path template** with `${VAR}` placeholders, a stage (`raw` / `intermediate` / `processed` / `external`), the source, the SQL or script that produced it, and its inputs (`depends_on`). Every machine resolves the same template through its own `.env`.

```bash
python3 .claude/scripts/data_registry.py list            # what exists
python3 .claude/scripts/data_registry.py check           # is every file where it should be on THIS machine?
python3 .claude/scripts/data_registry.py where NAME      # absolute path
python3 .claude/scripts/data_registry.py add NAME --path '${DROPBOX_ROOT}/proj/data/x.parquet' --stage raw --source '...'
```

`/data-registry` wraps these and reads the registry into the session.

## Code never hardcodes a path

Scripts obtain paths through the helpers, never through string literals:

```python
# Python — code/utils/data_paths.py
from utils.data_paths import data_path, out_path
df = pd.read_parquet(data_path("crsp_msf_2000_2023"))
df.to_parquet(out_path("panel_clean", stage="processed"))   # registers on first save
```

```r
# R — code/utils/data_paths.R
source("code/utils/data_paths.R")
df <- arrow::read_parquet(data_path("crsp_msf_2000_2023"))
```

The `path-guard` hook flags `/Users/...`, `C:\...`, and `Dropbox/` literals written into `code/`; the debugger deducts for them (`quality-gates.md`: hardcoded absolute paths, −20).

## Every derived file is registered

When a script writes a processed dataset, it registers it (the helpers do this automatically via `out_path(..., register=TRUE)`) with `depends_on` pointing at its inputs. The replication verifier reads the registry to check that every file the paper needs has a producer.

## WRDS

If the author has WRDS credentials (`~/.pgpass` or `WRDS_USERNAME` in `.env`), data discovery and pulls go through `.claude/scripts/wrds_client.py` — no manual web downloads:

- `/wrds search crsp` · `/wrds tables comp` · `/wrds describe crsp.msf` · `/wrds sample comp.funda`
- `/wrds fetch "SELECT ..." --name NAME` writes to `${DROPBOX_ROOT}/…` by default, registers the pull with the SQL as provenance, and hands off to `/data-profile`.
- The `explorer` agent runs a WRDS `search`/`describe` pass first whenever credentials exist, so its assessment names real tables and columns.
- Without credentials every WRDS command exits with a setup message and nothing else changes.

## Rules for Claude

1. Before reading any data file, run `data_registry.py check` (or `/data-registry`) — never guess a Dropbox path.
2. Register every pull and every derived dataset; a file that is not in the registry does not exist for the pipeline.
3. Default destination for pulls is `${DROPBOX_ROOT}`; `data/raw` is for scratch only and may be deleted at any time.
4. Never commit files under `data/raw` or `data/processed`; never write credentials anywhere but `.env` or `~/.pgpass`.
5. Prefer WRDS SQL with explicit column lists and date filters over `SELECT *` pulls of full tables.

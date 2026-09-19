---
name: wrds
description: Explore and pull data from WRDS (CRSP, Compustat, IBES, TRACE, Dealscan, BoardEx, Audit Analytics, ...) directly from the session when the author has credentials — list libraries and tables, describe columns, sample rows, count, run SQL, and fetch to Dropbox with automatic registration and profiling. Use when the user says "check WRDS", "what's in crsp", "pull Compustat", "get CRSP monthly returns", or when /find-data needs real table names. Exits cleanly with setup instructions if no credentials exist.
disable-model-invocation: true
argument-hint: "[test | search KEYWORD | libraries | tables LIB | describe LIB.TABLE | sample LIB.TABLE | count LIB.TABLE | query \"SQL\" | fetch \"SQL\" --name NAME]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Task"]
---

# WRDS

Skip the web downloader. Explore the WRDS PostgreSQL catalogue and pull exactly the columns and dates you need, straight into the registered data location.

**Input:** `$ARGUMENTS` — a subcommand for `.claude/scripts/wrds_client.py`. Empty → `test`.

---

## Step 0: Credentials

Run `python3 .claude/scripts/wrds_client.py test`.
- Exit 0 → connected; continue.
- Exit 3 → no credentials. Show the setup message (`~/.pgpass` line or `WRDS_USERNAME` in `.env`), remind that `.env` and `~/.pgpass` are never committed, and stop. Do **not** ask the user to paste a password into the chat.
- Connection error mentioning Duo/MFA → tell the user to approve the prompt on their device and retry; WRDS may require it on first connection from a new machine.
- `ModuleNotFoundError` → `pip install wrds` (or `pip install psycopg2-binary pandas pyarrow` for the direct-SQL fallback).

## Step 1: Explore (read-only, cheap)

| Need | Command |
|------|---------|
| Which libraries mention X? | `search crsp` |
| What tables does a library have? | `tables comp --grep funda` |
| Columns, types | `describe crsp.msf` |
| A look at the data | `sample comp.funda --n 20` |
| How big is a pull going to be? | `count crsp.dsf --where "date >= '2015-01-01'"` |
| Ad-hoc check | `query "SELECT permno, date, ret FROM crsp.msf WHERE date BETWEEN '2020-01-01' AND '2020-03-31' LIMIT 100"` |

Always `count` before a `fetch` larger than a few million rows; warn the user if the pull exceeds ~5 GB and propose column/date filters.

Common anchors (verify with `describe` — schemas change):
- CRSP: `crsp.msf` / `crsp.dsf` (returns), `crsp.msenames` / `crsp.stocknames` (names, SIC), `crsp.ccmxpf_linktable` (CRSP–Compustat link)
- Compustat: `comp.funda` (annual, filter `indfmt='INDL' and datafmt='STD' and popsrc='D' and consol='C'`), `comp.fundq`, `comp.company`
- IBES: `ibes.statsum_epsus`, `ibes.actu_epsus`; TRACE: `trace.trace_enhanced`; Dealscan: `dealscan.*`; Fama–French: `ff.factors_monthly`

## Step 2: Fetch

```bash
python3 .claude/scripts/wrds_client.py fetch "SELECT permno, date, ret, prc, shrout FROM crsp.msf WHERE date >= '2000-01-01'" \
    --name crsp_msf_2000_on --dest '${DROPBOX_ROOT}/<project>/data/raw' --format parquet
```

- Default destination is Dropbox (`${DROPBOX_ROOT}/…`); use `--dest data/raw` only for scratch extracts.
- The script registers the file in `data/registry.json` with the SQL as provenance (`--no-register` to skip).
- The pull is logged: append one line to the current session log with name, rows, destination.

## Step 3: Profile and hand off

Run `/data-profile <resolved path>` (or `python3 .claude/scripts/profile_data.py "$(python3 .claude/scripts/data_registry.py where NAME)"`). Report:

```
🏛 WRDS — [subcommand]
[result table / row count / path]
Registered as: NAME → ${DROPBOX_ROOT}/... (N rows)
Next: /data-profile NAME
```

---

## Principles

- **Explicit columns and dates.** No `SELECT *` on full tables; WRDS throttles and Dropbox fills.
- **Reproducible pulls.** The SQL in the registry is the replication record; the Coder re-runs it, not a downloaded ZIP.
- **Credentials stay local.** Never echo passwords; never write them to any tracked file.
- **Verify schemas.** Column names differ across libraries and versions — `describe` before you write SQL.

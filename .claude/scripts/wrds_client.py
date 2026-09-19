#!/usr/bin/env python3
"""
WRDS client — explore and pull data from Wharton Research Data Services
without manual downloads, and register what you pull.

Credentials (checked in this order):
    1. ~/.pgpass line:  wrds-pgdata.wharton.upenn.edu:9737:wrds:USERNAME:PASSWORD
    2. WRDS_USERNAME (+ optional WRDS_PASSWORD) in the environment or .env
    3. interactive prompt (username, then password)
No credentials → every command exits 3 with a setup message; nothing else breaks.

Backend: the official `wrds` package if installed (pip install wrds), otherwise
a direct PostgreSQL connection through psycopg2 (host wrds-pgdata.wharton.upenn.edu,
port 9737, db wrds, sslmode=require). Either way you need network access and a
WRDS account with database access; WRDS may require Duo MFA on first connection.

Usage:
    python3 .claude/scripts/wrds_client.py test
    python3 .claude/scripts/wrds_client.py libraries [--grep crsp]
    python3 .claude/scripts/wrds_client.py tables LIBRARY [--grep msf]
    python3 .claude/scripts/wrds_client.py describe LIBRARY.TABLE
    python3 .claude/scripts/wrds_client.py sample LIBRARY.TABLE [--n 20]
    python3 .claude/scripts/wrds_client.py count LIBRARY.TABLE [--where "date >= '2020-01-01'"]
    python3 .claude/scripts/wrds_client.py query "SELECT ..." [--limit 1000]
    python3 .claude/scripts/wrds_client.py fetch "SELECT ..." --name crsp_msf_2000_2023 \
        [--dest '${DROPBOX_ROOT}/proj/data' | --dest data/raw] [--format parquet|csv] [--no-register]
    python3 .claude/scripts/wrds_client.py search KEYWORD     # libraries + tables whose names match

`fetch` writes the file, registers it in data/registry.json with the SQL as
provenance, and prints the path. Run profile_data.py on it next.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_registry import load_env, resolve  # noqa: E402

HOST, PORT, DB = "wrds-pgdata.wharton.upenn.edu", 9737, "wrds"
NO_CREDS = 3

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None


# --------------------------------------------------------------------------- #
# Credentials & connection
# --------------------------------------------------------------------------- #
def pgpass_credentials() -> tuple[str | None, str | None]:
    pgpass = Path(os.environ.get("PGPASSFILE", Path.home() / ".pgpass"))
    if not pgpass.exists():
        return None, None
    for line in pgpass.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split(":")
        if len(parts) >= 5 and parts[0] in (HOST, "*") and parts[2] in (DB, "*"):
            return parts[3], ":".join(parts[4:])
    return None, None


def credentials(interactive: bool = True) -> tuple[str | None, str | None]:
    env = load_env()
    user = env.get("WRDS_USERNAME") or os.environ.get("WRDS_USERNAME")
    pw = env.get("WRDS_PASSWORD") or os.environ.get("WRDS_PASSWORD")
    if not user or not pw:
        pg_user, pg_pw = pgpass_credentials()
        user = user or pg_user
        pw = pw or pg_pw
    if not user and interactive and sys.stdin.isatty():
        user = input("WRDS username: ").strip() or None
    if user and not pw and interactive and sys.stdin.isatty():
        pw = getpass.getpass("WRDS password: ") or None
    return user, pw


def setup_message() -> str:
    return (
        "No WRDS credentials found.\n"
        "  Option A (recommended): create ~/.pgpass with\n"
        f"      {HOST}:{PORT}:{DB}:YOUR_USERNAME:YOUR_PASSWORD\n"
        "    and run: chmod 600 ~/.pgpass\n"
        "  Option B: add WRDS_USERNAME=... (and optionally WRDS_PASSWORD=...) to .env (gitignored)\n"
        "  Then: python3 .claude/scripts/wrds_client.py test\n"
        "  Backend: pip install wrds   (or psycopg2 for the direct-SQL fallback)"
    )


class Conn:
    """Thin wrapper over either the wrds package or a raw psycopg2 connection."""

    def __init__(self, user: str, pw: str | None):
        self.backend = None
        self.db = None
        try:
            import wrds  # type: ignore

            os.environ.setdefault("PGPASSWORD", pw or "")
            self.db = wrds.Connection(wrds_username=user, autoconnect=True)
            self.backend = "wrds"
            return
        except ImportError:
            pass
        except Exception as exc:
            sys.stderr.write(f"wrds package connection failed: {exc}\n")
        try:
            import psycopg2  # type: ignore

            self.db = psycopg2.connect(host=HOST, port=PORT, dbname=DB, user=user, password=pw, sslmode="require", connect_timeout=30)
            self.backend = "psycopg2"
        except ImportError:
            raise SystemExit("Neither `wrds` nor `psycopg2` is installed. Run: pip install wrds")
        except Exception as exc:
            raise SystemExit(f"Connection failed: {exc}\nIf WRDS asks for Duo/MFA, approve the prompt and retry.")

    def frame(self, sql: str):
        """Return a pandas DataFrame (pandas required) or list of dict rows."""
        if self.backend == "wrds":
            return self.db.raw_sql(sql)
        cur = self.db.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        cur.close()
        if pd is not None:
            return pd.DataFrame(rows, columns=cols)
        return [dict(zip(cols, r)) for r in rows]

    def libraries(self) -> list[str]:
        if self.backend == "wrds":
            return sorted(self.db.list_libraries())
        df = self.frame("SELECT DISTINCT table_schema FROM information_schema.tables ORDER BY 1")
        return [r["table_schema"] for r in _records(df)]

    def tables(self, lib: str) -> list[str]:
        if self.backend == "wrds":
            return sorted(self.db.list_tables(library=lib))
        df = self.frame(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{lib}' ORDER BY 1")
        return [r["table_name"] for r in _records(df)]

    def describe(self, lib: str, table: str):
        if self.backend == "wrds":
            return self.db.describe_table(library=lib, table=table)
        return self.frame(
            "SELECT column_name AS name, data_type AS type, is_nullable AS nullable "
            f"FROM information_schema.columns WHERE table_schema='{lib}' AND table_name='{table}' ORDER BY ordinal_position"
        )

    def close(self):
        try:
            self.db.close()
        except Exception:
            pass


def _records(df) -> list[dict]:
    if pd is not None and isinstance(df, pd.DataFrame):
        return df.to_dict("records")
    return df


def connect(interactive=True) -> Conn:
    user, pw = credentials(interactive)
    if not user:
        print(setup_message())
        sys.exit(NO_CREDS)
    return Conn(user, pw)


def split_ref(ref: str) -> tuple[str, str]:
    if "." not in ref:
        raise SystemExit("use LIBRARY.TABLE, e.g. crsp.msf")
    lib, table = ref.split(".", 1)
    return lib.lower(), table.lower()


def print_frame(df, max_rows: int = 50):
    if pd is not None and isinstance(df, pd.DataFrame):
        with pd.option_context("display.max_columns", 40, "display.width", 200, "display.max_rows", max_rows):
            print(df.head(max_rows).to_string(index=False))
    else:
        for r in df[:max_rows]:
            print(json.dumps(r, default=str))


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_test(args):
    c = connect()
    libs = c.libraries()
    print(f"connected via {c.backend}; {len(libs)} libraries visible (e.g. {', '.join(libs[:8])})")
    c.close()


def cmd_libraries(args):
    c = connect()
    libs = [l for l in c.libraries() if not args.grep or re.search(args.grep, l, re.I)]
    print("\n".join(libs))
    print(f"\n{len(libs)} libraries")
    c.close()


def cmd_tables(args):
    c = connect()
    tabs = [t for t in c.tables(args.library.lower()) if not args.grep or re.search(args.grep, t, re.I)]
    print("\n".join(tabs))
    print(f"\n{len(tabs)} tables in {args.library}")
    c.close()


def cmd_search(args):
    c = connect()
    hits = []
    for lib in c.libraries():
        if re.search(args.keyword, lib, re.I):
            hits.append((lib, "*"))
    # table-level search through information_schema in one query (fast on both backends)
    df = c.frame(
        "SELECT table_schema, table_name FROM information_schema.tables "
        f"WHERE table_name ILIKE '%{args.keyword}%' ORDER BY 1,2 LIMIT 300"
    )
    hits += [(r["table_schema"], r["table_name"]) for r in _records(df)]
    for lib, t in hits:
        print(f"{lib}.{t}")
    print(f"\n{len(hits)} match(es)")
    c.close()


def cmd_describe(args):
    lib, table = split_ref(args.ref)
    c = connect()
    print_frame(c.describe(lib, table), max_rows=500)
    c.close()


def cmd_sample(args):
    lib, table = split_ref(args.ref)
    c = connect()
    print_frame(c.frame(f"SELECT * FROM {lib}.{table} LIMIT {int(args.n)}"), max_rows=int(args.n))
    c.close()


def cmd_count(args):
    lib, table = split_ref(args.ref)
    where = f" WHERE {args.where}" if args.where else ""
    c = connect()
    df = c.frame(f"SELECT COUNT(*) AS n FROM {lib}.{table}{where}")
    print(_records(df)[0]["n"])
    c.close()


def cmd_query(args):
    sql = args.sql.strip().rstrip(";")
    if args.limit and not re.search(r"\blimit\b", sql, re.I):
        sql += f" LIMIT {int(args.limit)}"
    c = connect()
    df = c.frame(sql)
    print_frame(df, max_rows=int(args.limit or 50))
    c.close()


def cmd_fetch(args):
    sql = args.sql.strip().rstrip(";")
    if pd is None:
        raise SystemExit("fetch requires pandas (pip install pandas pyarrow)")
    c = connect()
    df = c.frame(sql)
    c.close()
    fmt = args.format
    dest_dir, missing = resolve(args.dest)
    if missing:
        raise SystemExit(f"{missing} not set in .env; cannot resolve --dest {args.dest}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"{args.name}.{fmt}"
    if fmt == "parquet":
        df.to_parquet(out, index=False)
    else:
        df.to_csv(out, index=False)
    print(f"wrote {len(df):,} rows × {df.shape[1]} cols → {out}")

    if not args.no_register:
        template = args.dest.rstrip("/") + f"/{args.name}.{fmt}"
        cmd = [
            sys.executable, str(Path(__file__).parent / "data_registry.py"), "add", args.name,
            "--path", template, "--stage", "raw", "--source", "WRDS", "--format", fmt,
            "--query", sql, "--rows", str(len(df)), "--force",
            "--description", args.description or f"WRDS pull {datetime.now():%Y-%m-%d}",
        ]
        subprocess.run(cmd, check=False)
    print(f"next: python3 .claude/scripts/profile_data.py \"{out}\"")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("test").set_defaults(fn=cmd_test)
    s = sub.add_parser("libraries"); s.add_argument("--grep"); s.set_defaults(fn=cmd_libraries)
    s = sub.add_parser("tables"); s.add_argument("library"); s.add_argument("--grep"); s.set_defaults(fn=cmd_tables)
    s = sub.add_parser("search"); s.add_argument("keyword"); s.set_defaults(fn=cmd_search)
    s = sub.add_parser("describe"); s.add_argument("ref"); s.set_defaults(fn=cmd_describe)
    s = sub.add_parser("sample"); s.add_argument("ref"); s.add_argument("--n", default=20); s.set_defaults(fn=cmd_sample)
    s = sub.add_parser("count"); s.add_argument("ref"); s.add_argument("--where"); s.set_defaults(fn=cmd_count)
    s = sub.add_parser("query"); s.add_argument("sql"); s.add_argument("--limit", type=int, default=1000); s.set_defaults(fn=cmd_query)
    s = sub.add_parser("fetch")
    s.add_argument("sql"); s.add_argument("--name", required=True)
    s.add_argument("--dest", default="${DROPBOX_ROOT}/cloco/data/raw", help="folder; ${DROPBOX_ROOT}/... recommended, or data/raw for scratch")
    s.add_argument("--format", choices=("parquet", "csv"), default="parquet")
    s.add_argument("--description"); s.add_argument("--no-register", action="store_true")
    s.set_defaults(fn=cmd_fetch)
    args = ap.parse_args()
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

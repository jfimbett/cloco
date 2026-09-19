#!/usr/bin/env python3
"""
Data registry — the single source of truth for WHERE every dataset lives.

The registry file (data/registry.json) is committed to git. The data itself is
not: canonical files live in Dropbox (or any folder outside the repo), and
intermediate files live under data/ which is gitignored. Paths in the registry
are written with ${VAR} placeholders (e.g. ${DROPBOX_ROOT}/cloco/crsp.parquet)
so the same registry works on every machine; each machine sets the variables
in .env (gitignored) — see .env.example.

Usage:
    python3 .claude/scripts/data_registry.py list [--json]
    python3 .claude/scripts/data_registry.py check              # every entry: exists? size? mtime?
    python3 .claude/scripts/data_registry.py where NAME         # print resolved absolute path
    python3 .claude/scripts/data_registry.py add NAME --path '${DROPBOX_ROOT}/proj/file.parquet' \
        --stage raw|intermediate|processed --source "CRSP via WRDS" [--description ..] \
        [--format parquet] [--query "select ..."] [--script code/01_pull.py] [--rows N]
    python3 .claude/scripts/data_registry.py remove NAME
    python3 .claude/scripts/data_registry.py roots              # show resolved ${VAR} roots

Conventions:
    ${DROPBOX_ROOT}  canonical, long-lived data (never in git)
    ${PROJECT_ROOT}  this repository (data/raw, data/processed are gitignored)
    ${DATA_ROOT}     optional extra root (external drive, server mount)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
REGISTRY = PROJECT_ROOT / "data" / "registry.json"
ENV_FILE = PROJECT_ROOT / ".env"
STAGES = ("raw", "intermediate", "processed", "external")
VAR_RE = re.compile(r"\$\{([A-Z0-9_]+)\}")


# --------------------------------------------------------------------------- #
# Environment / roots
# --------------------------------------------------------------------------- #
def load_env() -> dict[str, str]:
    """Read .env (KEY=VALUE lines) without overriding real environment variables."""
    env: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = os.path.expanduser(v.strip().strip('"').strip("'"))
    env.update({k: v for k, v in os.environ.items() if k in env or k in ("DROPBOX_ROOT", "DATA_ROOT", "PROJECT_ROOT")})
    env.setdefault("PROJECT_ROOT", str(PROJECT_ROOT))
    if "DROPBOX_ROOT" not in env:
        for guess in (Path.home() / "Dropbox", Path.home() / "Library/CloudStorage/Dropbox"):
            if guess.exists():
                env["DROPBOX_ROOT"] = str(guess)
                break
    return env


def resolve(path_template: str, env: dict[str, str] | None = None) -> tuple[Path, list[str]]:
    """Expand ${VAR} placeholders. Returns (path, missing_vars)."""
    env = env or load_env()
    missing: list[str] = []

    def sub(m):
        var = m.group(1)
        if var in env:
            return env[var]
        missing.append(var)
        return m.group(0)

    expanded = VAR_RE.sub(sub, path_template)
    p = Path(os.path.expanduser(expanded))
    if not p.is_absolute() and not missing:
        p = PROJECT_ROOT / p
    return p, missing


# --------------------------------------------------------------------------- #
# Registry IO
# --------------------------------------------------------------------------- #
def load_registry() -> dict:
    if not REGISTRY.exists():
        return {"version": 1, "datasets": {}}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save_registry(reg: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    reg["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_list(args) -> int:
    reg = load_registry()
    if args.json:
        print(json.dumps(reg, indent=2))
        return 0
    if not reg["datasets"]:
        print("registry is empty — add with: data_registry.py add NAME --path '${DROPBOX_ROOT}/...' --stage raw --source '...'")
        return 0
    print(f"{'name':<28} {'stage':<12} {'format':<8} {'source':<28} path")
    for name, d in sorted(reg["datasets"].items()):
        print(f"{name:<28} {d.get('stage',''):<12} {d.get('format',''):<8} {d.get('source','')[:27]:<28} {d.get('path','')}")
    return 0


def cmd_check(args) -> int:
    reg = load_registry()
    env = load_env()
    problems = 0
    for name, d in sorted(reg["datasets"].items()):
        p, missing = resolve(d.get("path", ""), env)
        if missing:
            print(f"✗ {name:<28} unset variable(s): {', '.join('${'+m+'}' for m in missing)}  → add to .env")
            problems += 1
        elif p.exists():
            st = p.stat()
            size = human(st.st_size) if p.is_file() else "dir"
            print(f"✓ {name:<28} {size:>8}  {datetime.fromtimestamp(st.st_mtime):%Y-%m-%d}  {p}")
        else:
            print(f"✗ {name:<28} MISSING  {p}")
            problems += 1
    if not reg["datasets"]:
        print("registry is empty")
    print(f"\n{len(reg['datasets'])} registered, {problems} problem(s)")
    return 1 if problems else 0


def cmd_where(args) -> int:
    reg = load_registry()
    d = reg["datasets"].get(args.name)
    if not d:
        sys.stderr.write(f"not registered: {args.name}\n")
        return 1
    p, missing = resolve(d["path"])
    if missing:
        sys.stderr.write(f"unset: {missing}\n")
        return 1
    print(p)
    return 0


def cmd_add(args) -> int:
    reg = load_registry()
    if args.name in reg["datasets"] and not args.force:
        sys.stderr.write(f"{args.name} already registered (use --force to overwrite)\n")
        return 1
    p, missing = resolve(args.path)
    entry = {
        "path": args.path,
        "stage": args.stage,
        "source": args.source,
        "description": args.description or "",
        "format": args.format or p.suffix.lstrip(".").lower(),
        "registered": datetime.now().strftime("%Y-%m-%d"),
        "tracked_in_git": False,
    }
    if args.query:
        entry["query"] = args.query
    if args.script:
        entry["script"] = args.script
    if args.rows is not None:
        entry["rows"] = args.rows
    if args.depends:
        entry["depends_on"] = args.depends
    if not missing and p.exists() and p.is_file():
        entry["size_bytes"] = p.stat().st_size
    elif missing:
        sys.stderr.write(f"note: {missing} not set in .env — path recorded but cannot be verified here\n")
    reg["datasets"][args.name] = entry
    save_registry(reg)
    print(f"registered {args.name} → {args.path}")
    return 0


def cmd_remove(args) -> int:
    reg = load_registry()
    if args.name not in reg["datasets"]:
        sys.stderr.write(f"not registered: {args.name}\n")
        return 1
    del reg["datasets"][args.name]
    save_registry(reg)
    print(f"removed {args.name} (file untouched)")
    return 0


def cmd_roots(args) -> int:
    env = load_env()
    for k in sorted(k for k in env if k.endswith("_ROOT")):
        flag = "✓" if Path(env[k]).exists() else "✗ (not found)"
        print(f"{k:<16} {flag}  {env[k]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("check"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("where"); s.add_argument("name"); s.set_defaults(fn=cmd_where)
    s = sub.add_parser("roots"); s.set_defaults(fn=cmd_roots)
    s = sub.add_parser("remove"); s.add_argument("name"); s.set_defaults(fn=cmd_remove)
    s = sub.add_parser("add")
    s.add_argument("name")
    s.add_argument("--path", required=True, help="use ${DROPBOX_ROOT}/... or ${PROJECT_ROOT}/data/...")
    s.add_argument("--stage", choices=STAGES, required=True)
    s.add_argument("--source", required=True, help="provenance, e.g. 'CRSP monthly via WRDS'")
    s.add_argument("--description")
    s.add_argument("--format")
    s.add_argument("--query")
    s.add_argument("--script")
    s.add_argument("--rows", type=int)
    s.add_argument("--depends", nargs="*", help="names of registered inputs this file is built from")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_add)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

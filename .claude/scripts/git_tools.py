#!/usr/bin/env python3
"""
Git tooling for the git-steward agent, the secrets-guard hook, and /git-steward.

Usage:
    python3 .claude/scripts/git_tools.py status                 # one-line branch/ahead/behind/dirty/worktrees
    python3 .claude/scripts/git_tools.py audit [--json]         # full repo hygiene audit → report
    python3 .claude/scripts/git_tools.py secrets [--staged | --unpushed | --tree | --history N]
    python3 .claude/scripts/git_tools.py bigfiles [--mb 20]     # tracked files over threshold
    python3 .claude/scripts/git_tools.py worktree new NAME [--from master]
    python3 .claude/scripts/git_tools.py worktree list
    python3 .claude/scripts/git_tools.py worktree remove NAME [--delete-branch]
    python3 .claude/scripts/git_tools.py worktree prune

Exit codes: 0 clean, 1 findings, 2 git error. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

# --------------------------------------------------------------------------- #
# Secret patterns (name, regex, severity). Kept conservative to avoid noise.
# --------------------------------------------------------------------------- #
SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "critical"),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b"), "critical"),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"), "critical"),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{20,}\b"), "critical"),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "critical"),
    ("Slack token", re.compile(r"\bxox[abprs]-[0-9A-Za-z\-]{10,}\b"), "critical"),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"), "critical"),
    ("pgpass line (WRDS)", re.compile(r"wrds-pgdata\.wharton\.upenn\.edu:\d+:\w+:[^:\s]+:[^\s]+"), "critical"),
    ("Password assignment", re.compile(r"(?i)\b(?:password|passwd|pwd|WRDS_PASSWORD)\s*[:=]\s*['\"][^'\"\s]{4,}['\"]"), "high"),
    ("API key assignment", re.compile(r"(?i)\b(?:api[_\-]?key|secret[_\-]?key|access[_\-]?token|auth[_\-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-/+=]{12,}['\"]"), "high"),
    ("Bearer token", re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._\-]{20,}"), "high"),
    ("Database URL with password", re.compile(r"(?i)\b(?:postgres|postgresql|mysql|mongodb)://[^:\s/]+:[^@\s]+@"), "high"),
]
ALLOWLIST = re.compile(r"(?i)(YOUR_USERNAME|YOUR_PASSWORD|\b(?:USER|USERNAME):(?:PASSWORD|PASSWD)\b|xxxx|example|placeholder|<[A-Z_]+>|\$\{[A-Z_]+\})")

SECRET_FILENAMES = [
    re.compile(r"(^|/)\.env(\.(?!example$|template$|sample$).+)?$"), re.compile(r"(^|/)\.pgpass$"), re.compile(r"(^|/)\.netrc$"),
    re.compile(r"(^|/)id_(rsa|ed25519|ecdsa|dsa)(\.pub)?$"), re.compile(r"\.(pem|key|p12|pfx)$"),
    re.compile(r"(^|/)credentials\.json$"), re.compile(r"(^|/)settings\.local\.json$"),
    re.compile(r"(^|/)\.claude/state/"), re.compile(r"(^|/)service[-_]account.*\.json$"),
]
DATA_EXT = (".parquet", ".dta", ".rds", ".rdata", ".feather", ".sas7bdat", ".sav", ".h5", ".hdf5", ".zip", ".gz", ".7z")
DATA_DIRS = ("data/raw/", "data/processed/")
GITHUB_HARD_LIMIT_MB = 100
BIG_MB_DEFAULT = 20
MAX_SCAN_BYTES = 4_000_000


# --------------------------------------------------------------------------- #
# git helpers
# --------------------------------------------------------------------------- #
def git(*args, check=False, text=True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=text, check=check)


def git_out(*args) -> str:
    r = git(*args)
    return r.stdout.strip() if r.returncode == 0 else ""


def in_repo() -> bool:
    return git("rev-parse", "--is-inside-work-tree").returncode == 0


def current_branch() -> str:
    return git_out("branch", "--show-current") or "(detached)"


def upstream() -> str:
    return git_out("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")


def ahead_behind() -> tuple[int, int]:
    out = git_out("rev-list", "--left-right", "--count", "@{u}...HEAD")
    if not out:
        return (0, 0)
    behind, ahead = out.split()
    return int(ahead), int(behind)


# --------------------------------------------------------------------------- #
# scanning
# --------------------------------------------------------------------------- #
def scan_text(text: str, label: str) -> list[dict]:
    hits = []
    for name, pat, sev in SECRET_PATTERNS:
        for m in pat.finditer(text):
            ctx = text[max(0, m.start() - 40): m.end() + 20]
            if ALLOWLIST.search(ctx):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            hits.append({"type": name, "severity": sev, "where": f"{label}:{line_no}", "snippet": redact(m.group(0))})
    return hits


def redact(s: str) -> str:
    return s[:6] + "…" + s[-3:] if len(s) > 12 else "…"


def scan_paths(paths: list[str]) -> list[dict]:
    hits = []
    for p in paths:
        norm = p.replace("\\", "/")
        if any(pat.search(norm) for pat in SECRET_FILENAMES):
            hits.append({"type": "Secret-bearing filename", "severity": "critical", "where": norm, "snippet": ""})
        if norm.startswith(DATA_DIRS) and not norm.endswith((".gitkeep", "README.md", "registry.json")):
            hits.append({"type": "Data file under data/", "severity": "high", "where": norm, "snippet": ""})
        elif norm.lower().endswith(DATA_EXT):
            hits.append({"type": "Binary data file", "severity": "high", "where": norm, "snippet": ""})
    return hits


def staged_files() -> list[str]:
    return [l for l in git_out("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if l]


def scan_staged() -> list[dict]:
    hits = scan_paths(staged_files())
    diff = git_out("diff", "--cached", "--unified=0")
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    hits += scan_text(added[:MAX_SCAN_BYTES], "staged diff")
    for f in staged_files():
        r = git("cat-file", "-s", f":{f}")
        if r.returncode == 0 and r.stdout.strip().isdigit():
            mb = int(r.stdout.strip()) / 1e6
            if mb >= BIG_MB_DEFAULT:
                sev = "critical" if mb >= GITHUB_HARD_LIMIT_MB else "high"
                hits.append({"type": f"Large file ({mb:.0f} MB)", "severity": sev, "where": f, "snippet": ""})
    return hits


def scan_unpushed() -> list[dict]:
    """Scan commits not on the upstream; without an upstream, the last 5 commits."""
    if upstream():
        rng, label = ["@{u}..HEAD"], "@{u}..HEAD"
    else:
        rng, label = ["-5"], "last 5 commits (no upstream)"
    files = sorted({l for l in git_out("log", "--name-only", "--diff-filter=ACMR", "--format=", *rng).splitlines() if l})
    hits = scan_paths(files)
    diff = git_out("log", "-p", "--unified=0", "--format=commit %h", *rng)
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    hits += scan_text(added[:MAX_SCAN_BYTES], f"unpushed ({label})")
    return hits


def scan_tree() -> list[dict]:
    files = [l for l in git_out("ls-files").splitlines() if l]
    hits = scan_paths(files)
    for f in files:
        p = PROJECT_ROOT / f
        try:
            if p.stat().st_size > MAX_SCAN_BYTES or p.suffix.lower() in (".pdf", ".png", ".jpg", ".parquet", ".dta"):
                continue
            hits += scan_text(p.read_text(encoding="utf-8", errors="ignore"), f)
        except OSError:
            continue
    return hits


def scan_history(n: int) -> list[dict]:
    diff = git_out("log", "-p", "--unified=0", f"-{n}", "--format=commit %h")
    hits = []
    for chunk in re.split(r"^commit ", diff, flags=re.M):
        if not chunk.strip():
            continue
        sha, _, body = chunk.partition("\n")
        added = "\n".join(l[1:] for l in body.splitlines() if l.startswith("+") and not l.startswith("+++"))
        hits += scan_text(added, f"commit {sha.strip()}")
    return hits


def bigfiles(mb: float) -> list[dict]:
    out = []
    for f in git_out("ls-files").splitlines():
        p = PROJECT_ROOT / f
        try:
            size = p.stat().st_size / 1e6
        except OSError:
            continue
        if size >= mb:
            out.append({"file": f, "mb": round(size, 1)})
    return sorted(out, key=lambda d: -d["mb"])


# --------------------------------------------------------------------------- #
# audit
# --------------------------------------------------------------------------- #
def audit() -> dict:
    rep: dict = {"branch": current_branch(), "upstream": upstream() or None}
    rep["ahead"], rep["behind"] = ahead_behind()
    status = git_out("status", "--porcelain")
    rep["uncommitted"] = len([l for l in status.splitlines() if l])
    rep["remote"] = git_out("remote", "get-url", "origin")
    rep["remote_insecure"] = rep["remote"].startswith("http://")
    rep["default_branch_dirty"] = rep["branch"] in ("master", "main") and rep["uncommitted"] > 0
    rep["worktrees"] = [l.split()[0] for l in git_out("worktree", "list").splitlines()][1:]
    rep["stale_branches"] = [
        b.strip() for b in git_out("branch", "--merged", "master").splitlines()
        if b.strip() and not b.strip().startswith("*") and b.strip() not in ("master", "main")
    ]
    gi = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8", errors="ignore") if (PROJECT_ROOT / ".gitignore").exists() else ""
    rep["gitignore_missing"] = [pat for pat in (".env", ".claude/settings.local.json", ".claude/state/", "data/raw/*", "*.parquet") if pat not in gi]
    rep["secrets_tree"] = scan_tree()
    rep["secrets_staged"] = scan_staged()
    rep["bigfiles"] = bigfiles(BIG_MB_DEFAULT)
    rep["tracked_data_files"] = [h["where"] for h in rep["secrets_tree"] if h["type"] in ("Data file under data/", "Binary data file")]
    rep["last_commit_age_days"] = None
    ts = git_out("log", "-1", "--format=%ct")
    if ts:
        import time
        rep["last_commit_age_days"] = round((time.time() - int(ts)) / 86400, 1)
    rep["findings"] = len(rep["secrets_tree"]) + len(rep["secrets_staged"]) + len(rep["bigfiles"]) + len(rep["gitignore_missing"]) + int(rep["remote_insecure"])
    return rep


def print_audit(rep: dict) -> None:
    ok = lambda b: "✓" if b else "✗"
    print(f"Branch     {rep['branch']}  (upstream {rep['upstream'] or 'none'}; ahead {rep['ahead']}, behind {rep['behind']})")
    print(f"Working    {rep['uncommitted']} uncommitted change(s){'  ← on the default branch' if rep['default_branch_dirty'] else ''}")
    print(f"Remote     {rep['remote']}  {'✗ http:// — switch to https://' if rep['remote_insecure'] else '✓'}")
    print(f"Worktrees  {len(rep['worktrees'])} extra: {', '.join(rep['worktrees']) or '—'}")
    print(f"Merged branches to delete: {', '.join(rep['stale_branches']) or '—'}")
    print(f".gitignore {ok(not rep['gitignore_missing'])} {'missing: ' + ', '.join(rep['gitignore_missing']) if rep['gitignore_missing'] else 'covers env, local settings, state, data'}")
    print(f"Secrets in tree    {ok(not rep['secrets_tree'])} {len(rep['secrets_tree'])}")
    for h in rep["secrets_tree"][:10]:
        print(f"    [{h['severity']}] {h['type']} — {h['where']} {h['snippet']}")
    print(f"Secrets staged     {ok(not rep['secrets_staged'])} {len(rep['secrets_staged'])}")
    for h in rep["secrets_staged"][:10]:
        print(f"    [{h['severity']}] {h['type']} — {h['where']} {h['snippet']}")
    print(f"Large tracked files {ok(not rep['bigfiles'])} {len(rep['bigfiles'])} ≥ {BIG_MB_DEFAULT} MB")
    for b in rep["bigfiles"][:10]:
        print(f"    {b['mb']} MB  {b['file']}")
    print(f"\n{rep['findings']} finding(s)")


# --------------------------------------------------------------------------- #
# worktrees
# --------------------------------------------------------------------------- #
def worktree_dir(name: str) -> Path:
    return PROJECT_ROOT.parent / f"{PROJECT_ROOT.name}-wt" / name


def cmd_worktree(args) -> int:
    if args.action == "list":
        print(git_out("worktree", "list") or "(none)")
        return 0
    if args.action == "prune":
        r = git("worktree", "prune", "-v")
        print(r.stdout or r.stderr or "pruned")
        return r.returncode
    if args.action == "new":
        path = worktree_dir(args.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        base = args.base or "master"
        exists = git("rev-parse", "--verify", "--quiet", args.name).returncode == 0
        cmd = ["worktree", "add", str(path)] + ([args.name] if exists else ["-b", args.name, base])
        r = git(*cmd)
        if r.returncode:
            sys.stderr.write(r.stderr)
            return 2
        # share the machine-specific .env so the registry resolves in the worktree
        env = PROJECT_ROOT / ".env"
        if env.exists() and not (path / ".env").exists():
            try:
                os.symlink(env, path / ".env")
            except OSError:
                (path / ".env").write_text(env.read_text())
        print(f"worktree ready: {path}  (branch {args.name}, from {base})")
        print(f"open with:  cd {path} && claude")
        return 0
    if args.action == "remove":
        path = worktree_dir(args.name)
        r = git("worktree", "remove", str(path), *(["--force"] if args.force else []))
        if r.returncode:
            sys.stderr.write(r.stderr)
            return 2
        print(f"removed worktree {path}")
        try:
            path.parent.rmdir()  # drop ../<repo>-wt if now empty
        except OSError:
            pass
        if args.delete_branch:
            r = git("branch", "-d", args.name)
            print(r.stdout or r.stderr)
        return 0
    return 2


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def cmd_status(args) -> int:
    a, b = ahead_behind()
    dirty = len([l for l in git_out("status", "--porcelain").splitlines() if l])
    wts = max(len(git_out("worktree", "list").splitlines()) - 1, 0)
    up = upstream()
    parts = [f"branch {current_branch()}"]
    parts.append(f"↑{a} ↓{b}" if up else "no upstream")
    parts.append(f"{dirty} uncommitted" if dirty else "clean")
    if wts:
        parts.append(f"{wts} worktree(s)")
    print(" · ".join(parts))
    return 0


def cmd_audit(args) -> int:
    rep = audit()
    if args.json:
        print(json.dumps(rep, indent=2, default=str))
    else:
        print_audit(rep)
    return 1 if rep["findings"] else 0


def cmd_secrets(args) -> int:
    if args.history:
        hits = scan_history(args.history)
        label = f"last {args.history} commits"
    elif args.tree:
        hits, label = scan_tree(), "tracked files"
    elif args.unpushed:
        hits, label = scan_unpushed(), "unpushed commits"
    else:
        hits, label = scan_staged(), "staged changes"
    if args.json:
        print(json.dumps(hits, indent=2))
    else:
        for h in hits:
            print(f"[{h['severity']}] {h['type']} — {h['where']} {h['snippet']}")
        print(f"{len(hits)} finding(s) in {label}")
    return 1 if hits else 0


def cmd_bigfiles(args) -> int:
    rows = bigfiles(args.mb)
    for r in rows:
        print(f"{r['mb']:>8} MB  {r['file']}")
    print(f"{len(rows)} file(s) ≥ {args.mb} MB")
    return 1 if rows else 0


def main() -> int:
    if not in_repo():
        sys.stderr.write("not a git repository\n")
        return 2
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    s = sub.add_parser("audit"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_audit)
    s = sub.add_parser("secrets")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true"); g.add_argument("--unpushed", action="store_true")
    g.add_argument("--tree", action="store_true"); g.add_argument("--history", type=int, metavar="N")
    s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_secrets)
    s = sub.add_parser("bigfiles"); s.add_argument("--mb", type=float, default=BIG_MB_DEFAULT); s.set_defaults(fn=cmd_bigfiles)
    s = sub.add_parser("worktree")
    s.add_argument("action", choices=("new", "list", "remove", "prune"))
    s.add_argument("name", nargs="?")
    s.add_argument("--from", dest="base"); s.add_argument("--delete-branch", action="store_true"); s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_worktree)
    args = ap.parse_args()
    if args.cmd == "worktree" and args.action in ("new", "remove") and not args.name:
        ap.error("worktree new/remove need NAME")
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

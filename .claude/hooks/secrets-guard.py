#!/usr/bin/env python3
"""
Secrets Guard Hook

Fires on PreToolUse for Bash. When the command is a `git commit`, `git push`,
or `git add` of a sensitive path, it scans what is about to leave the working
tree — staged content for commits, unpushed commits for pushes — for
credentials, secret-bearing filenames (.env, .pgpass, keys), data files that
belong in Dropbox, and blobs above GitHub's size limits. Any critical/high
finding BLOCKS the command with the list of offending locations.

Override: append --no-verify to the git command (logged as a user override).
Fails open on any internal error.

Hook Event: PreToolUse (matcher: "Bash")
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
sys.path.insert(0, str(PROJECT_ROOT / ".claude" / "scripts"))

COMMIT_RE = re.compile(r"\bgit\b[^|;&]*\bcommit\b")
PUSH_RE = re.compile(r"\bgit\b[^|;&]*\bpush\b")
ADD_RE = re.compile(r"\bgit\b[^|;&]*\badd\b(.*)")
SENSITIVE_ADD = re.compile(r"(^|[\s/])(\.env(\.(?!example|template|sample)\w+)?|\.pgpass|\.netrc|id_rsa|id_ed25519|[^\s]*\.pem|[^\s]*\.key|settings\.local\.json|\.claude/state)(\s|$)")


def block(reason: str) -> None:
    json.dump({"decision": "block", "reason": reason}, sys.stdout)


def fmt(hits: list[dict]) -> str:
    lines = [f"  [{h['severity']}] {h['type']} — {h['where']} {h.get('snippet', '')}".rstrip() for h in hits[:12]]
    if len(hits) > 12:
        lines.append(f"  … and {len(hits) - 12} more")
    return "\n".join(lines)


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0
    if hook_input.get("tool_name") != "Bash":
        return 0
    cmd = hook_input.get("tool_input", {}).get("command", "") or ""
    if "--no-verify" in cmd:
        return 0

    is_commit, is_push = bool(COMMIT_RE.search(cmd)), bool(PUSH_RE.search(cmd))
    m_add = ADD_RE.search(cmd)
    if m_add and SENSITIVE_ADD.search(m_add.group(1)):
        block(
            "secrets-guard: that `git add` names a credential or local-settings file "
            "(.env / .pgpass / keys / settings.local.json / .claude/state). These are gitignored on purpose. "
            "If you really need to track it, explain why and use --no-verify."
        )
        return 0
    if not (is_commit or is_push):
        return 0

    from git_tools import scan_staged, scan_unpushed  # type: ignore

    hits = []
    if is_commit:
        hits += scan_staged()
    if is_push:
        hits += scan_unpushed()
    serious = [h for h in hits if h["severity"] in ("critical", "high")]
    if not serious:
        return 0

    what = "commit" if is_commit else "push"
    block(
        f"secrets-guard: blocked `git {what}` — {len(serious)} finding(s) that must not reach the repository:\n"
        f"{fmt(serious)}\n"
        "Fix: unstage the file (git restore --staged <file>), move data to ${DROPBOX_ROOT} and register it, "
        "or move credentials to .env / ~/.pgpass. If a secret is already in a commit, rotate it and run "
        "`/git-steward history-scan` before pushing. Override only with --no-verify and a stated reason."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # never block on a hook bug

#!/usr/bin/env python3
"""
Path Guard Hook

Fires on PostToolUse for Write/Edit on analysis code (code/**, replication/**,
explorations/**). Scans the written content for hard-coded machine-specific
paths (home directories, Dropbox folders, drive letters) and reminds Claude to
route them through the data registry instead
(code/utils/data_paths.{py,R} → data/registry.json → .env roots).

Non-blocking: prints a reminder and returns additionalContext.

Hook Event: PostToolUse (matcher: "Write|Edit")
"""

from __future__ import annotations

import json
import re
import sys

WATCH_DIRS = ("/code/", "/replication/", "/explorations/")
CODE_EXT = (".py", ".R", ".r", ".do", ".jl", ".qmd", ".Rmd", ".ipynb", ".sh")
PATTERNS = [
    (re.compile(r"/Users/[A-Za-z0-9_.-]+/"), "macOS home directory"),
    (re.compile(r"/home/[A-Za-z0-9_.-]+/"), "Linux home directory"),
    (re.compile(r"[A-Za-z]:\\\\?Users\\\\?"), "Windows user directory"),
    (re.compile(r"[A-Za-z]:[\\/](?!\\)"), "Windows drive letter"),
    (re.compile(r"Dropbox[\\/]"), "Dropbox folder"),
    (re.compile(r"OneDrive[\\/]|Google Drive[\\/]|iCloud"), "cloud-drive folder"),
]


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0
    if hook_input.get("tool_name") not in ("Write", "Edit"):
        return 0
    ti = hook_input.get("tool_input", {}) or {}
    path = (ti.get("file_path") or "").replace("\\", "/")
    if not path.endswith(CODE_EXT) or not any(d in path for d in WATCH_DIRS):
        return 0
    content = ti.get("content") or ti.get("new_string") or ""
    hits = []
    for pat, label in PATTERNS:
        m = pat.search(content)
        if m:
            hits.append(f"{label}: …{content[max(0, m.start()-15):m.end()+25].strip()}…")
    if not hits:
        return 0
    msg = (
        f"[path-guard] {path.rsplit('/', 1)[-1]} contains machine-specific paths — "
        "use the data registry instead (Python: from utils.data_paths import data_path; "
        "R: source('code/utils/data_paths.R'); data_path('name')). Found: " + " | ".join(hits[:3])
    )
    print(msg)
    json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)

#!/usr/bin/env python3
"""
File Protection Hook

Blocks accidental edits to protected files before the tool runs.
Replaces protect-files.sh (which required jq).

Hook Event: PreToolUse (matcher: "Write|Edit")
Exit code 2 = block with message shown to user.
Exit code 0 = allow.
"""

from __future__ import annotations

import json
import sys
import fnmatch
from pathlib import Path

# Files / patterns to protect from accidental overwrite.
# Uses basename matching. Add full path substrings for more precision.
PROTECTED_PATTERNS = [
    "paper/references.bib",         # Centralized bibliography — edit manually
    "settings.json",                 # Claude Code settings — edit manually
    "strategy-memo-*.md",            # Approved strategy memos — immutable after approval
    "referee-report-*.md",           # Real referee reports — never auto-edit
    "quality-score-*.json",          # Audit scores — produced by critics only
]

# Directories where writes are always allowed (generated output)
ALWAYS_ALLOW_DIRS = [
    "quality_reports/",
    "output/",
    "paper/figures/",
    "paper/tables/",
]


def is_always_allowed(file_path: str) -> bool:
    """Check if the file is in a directory that is always writable."""
    normalized = file_path.replace("\\", "/")
    return any(allowed in normalized for allowed in ALWAYS_ALLOW_DIRS)


def is_protected(file_path: str) -> bool:
    """Check if the file matches any protected pattern."""
    normalized = file_path.replace("\\", "/")
    basename = Path(file_path).name

    for pattern in PROTECTED_PATTERNS:
        # Full path substring match
        if pattern in normalized:
            return True
        # Basename glob match
        if fnmatch.fnmatch(basename, pattern):
            return True

    return False


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        return 0

    file_path = hook_input.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0

    if is_always_allowed(file_path):
        return 0

    if is_protected(file_path):
        output = {
            "decision": "block",
            "reason": (
                f"Protected file: {file_path}\n"
                "This file is protected from automatic edits to prevent accidental overwrites. "
                "Edit it manually, or remove the protection in .claude/hooks/protect-files.py "
                "if you intentionally want Claude to modify it."
            ),
        }
        json.dump(output, sys.stdout)
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # Fail open — never block due to hook bug

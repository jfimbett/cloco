#!/usr/bin/env python3
"""
Quality Gate Hook

Fires on PreToolUse when a Bash command contains "git commit".
Checks quality_reports/ for a recent quality report with score >= 80.
Blocks the commit if the score is below threshold.

Falls open (exit 0) if:
  - No quality reports exist yet (new project — don't block)
  - Score cannot be parsed from the report
  - --no-verify flag is present in the commit command (user override)

Hook Event: PreToolUse (matcher: "Bash")
Exit code 0 = allow. Output JSON with decision=block to block.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

COMMIT_THRESHOLD = 80


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    # Only fire on Bash tool
    if hook_input.get("tool_name") != "Bash":
        return 0

    command = hook_input.get("tool_input", {}).get("command", "")

    # Only fire on git commit
    if "git commit" not in command:
        return 0

    # Respect explicit user override
    if "--no-verify" in command:
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    qr_dir = Path(project_dir) / "quality_reports"
    if not qr_dir.exists():
        return 0  # No reports yet — new project, fall open

    # Look for the most recent quality report (merges/ or any scored .md)
    report_files = sorted(
        list(qr_dir.rglob("*.md")),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    if not report_files:
        return 0  # No reports — fall open

    # Score patterns to look for in the report
    score_patterns = [
        r"Aggregate Score[:\s]+(\d+)\s*/\s*100",
        r"Overall Score[:\s]+(\d+)\s*/\s*100",
        r"\*\*Score:\*\*\s*(\d+)\s*/\s*100",
        r"\*\*(\d+)/100\*\*",
        r"Score:\s*(\d+)/100",
    ]

    # Check the 3 most recent reports for a parseable score
    for report in report_files[:3]:
        content = report.read_text(encoding="utf-8", errors="ignore")
        for pattern in score_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                if score < COMMIT_THRESHOLD:
                    output = {
                        "decision": "block",
                        "reason": (
                            f"Quality gate: score {score}/100 is below the commit threshold "
                            f"({COMMIT_THRESHOLD}/100) per quality-gates.md.\n"
                            f"Report: {report.name}\n"
                            f"Fix the blocking issues listed in the report before committing.\n"
                            f"To override: add --no-verify to the git commit command."
                        ),
                    }
                    json.dump(output, sys.stdout)
                return 0  # Score >= 80 or score found and OK

    return 0  # No parseable score found — fall open


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # Always fail open

#!/usr/bin/env python3
"""
Identity Guard Hook

Fires on PreToolUse for Bash. Once a research spec exists this checkout is a
real project, not the `cloco` template. A `git push` whose destination is the
template repository (origin still points at …/cloco.git, or the push names the
`template` remote) is BLOCKED with instructions to run /setup-project, which
renames the template remote, creates cloco-<slug> on GitHub and renames the
folder.

Without a spec (i.e. working on the template itself) the hook does nothing.
Override: append --no-verify to the git command (logged as a user override).

Hook Event: PreToolUse (matcher: "Bash")
Returns: Exit code 0 always; blocks through permissionDecision "deny".
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PUSH_RE = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?push\b(?P<rest>[^|;&]*)")


def block(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))


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
    m = PUSH_RE.search(cmd)
    if not m:
        return 0
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project_dir:
        return 0
    sys.path.insert(0, str(Path(project_dir) / ".claude" / "scripts"))
    from project_setup import identity  # type: ignore

    idn = identity(Path(project_dir))
    if not idn["has_spec"]:
        return 0
    rest = m.group("rest")
    named = [t for t in rest.split() if not t.startswith("-")]
    target_remote = named[0] if named else "origin"
    target_is_template = (target_remote == idn.get("template_remote")) or (target_remote == "origin" and idn["remote_is_template"])
    if not target_is_template:
        return 0
    block(
        "identity-guard: blocked `git push` — this checkout has a research spec "
        f"({idn['spec_file']}: {idn['project_name']}) but the push targets the cloco TEMPLATE repository "
        f"({idn['remotes'].get(target_remote, target_remote)}). Pushing would write your project into the template "
        "and break it for other projects.\n"
        f"Fix: run /setup-project — it renames the template remote to `template`, creates "
        f"`{idn['suggested_repo'] or 'cloco-<slug>'}` on GitHub (private or public, your choice), sets it as origin "
        "and pushes. To push a genuine template improvement from here, use --no-verify and say why."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # never block on a hook bug

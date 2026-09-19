#!/usr/bin/env python3
"""
Session Welcome Hook

Fires on SessionStart (startup / resume / clear — not compact) and prints a
banner: project, phase, last action, next command, gates, git state, data
registry status, lesson count. All state comes from
.claude/scripts/project_state.py so the banner, the status line, and the
shell dashboard never disagree.

Hook Event: SessionStart
Returns: Exit code 0 (informational, never blocks)
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


def get_session_dir() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"
    return Path.home() / ".claude" / "sessions" / hashlib.md5(project_dir.encode()).hexdigest()[:8]


W = 64
BORDER = "─" * (W - 2)


def row(text: str) -> str:
    return f"│  {text[:W - 4]:<{W - 4}}│"


def render(st: dict) -> str:
    lines = [f"┌─ CLOCO {BORDER[8:]}┐"]
    if st.get("has_project"):
        g = st["gates"]
        tick = lambda b: "✓" if b else "○"
        score = f"  (overall: {g['score']}/100)" if g.get("score") is not None else ""
        last = st.get("last")
        last_s = f"{last['agent']} ({last['score'] or '—'}) — {last['verdict']}" if last else "no entries yet"
        lines += [
            row(f"Project  {st['project_name']}"),
            row(f"Type     {st['project_type'].capitalize()} · Phase {st['phase_num']} of 5: {st['phase']}"),
            row(f"Last     {last_s}"),
            row(f"Next     {st['next']}"),
            row(f"Gates    Commit {tick(g['commit'])}  PR {tick(g['pr'])}  Submission {tick(g['submission'])}{score}"),
            f"└{BORDER}┘",
            "  Type /pipeline-status for the full dashboard (or `make status` in the shell).",
        ]
    else:
        lines += [
            row("No active research project."),
            row("Not sure about the idea?   /scout [idea]"),
            row("Committed?                 /interview-me [topic], /discovery"),
            row("Full pipeline:             /new-project [topic]"),
            f"└{BORDER}┘",
            "  Type /pipeline-status for a full list of available commands.",
        ]
    gs = st.get("git")
    if gs:
        hint = "  → work on a branch or worktree (/git-steward)" if gs["on_default"] and gs["dirty"] else ""
        wt = f" · {gs['worktrees']} worktree(s)" if gs["worktrees"] else ""
        lines.append(f"  Git:  branch {gs['branch']} · ↑{gs['ahead']} ↓{gs['behind']} · {gs['dirty'] or 'clean'}{' uncommitted' if gs['dirty'] else ''}{wt}{hint}")
    ds = st.get("data")
    if ds is not None:
        if ds.get("registered") is None:
            lines.append("  Data: registry unreadable — /data-registry check")
        elif ds["registered"] == 0:
            lines.append("  Data: registry empty — /data-registry setup, /wrds search, or /find-data.")
        else:
            miss = ds["missing"]
            tail = f"; {len(miss)} not on this machine ({', '.join(miss[:3])}{'…' if len(miss) > 3 else ''}) → /data-registry check" if miss else "; all present"
            lines.append(f"  Data: {ds['registered']} registered{tail}")
    ls = st.get("lessons")
    if ls is not None:
        if ls["count"]:
            lines.append(f"  Lessons: {ls['count']} recorded — latest {ls['latest_date']} [{ls['latest_category']}]. Read .claude/lessons/LESSONS.md before starting.")
        else:
            lines.append("  Lessons: none yet (.claude/lessons/LESSONS.md).")
    return "\n".join(lines)


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}
    if hook_input.get("type") == "compact" or hook_input.get("source") == "compact":
        return 0
    if (get_session_dir() / "pre-compact-state.json").exists():
        return 0
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0
    sys.path.insert(0, str(Path(project_dir) / ".claude" / "scripts"))
    try:
        from project_state import state  # type: ignore
        print(render(state(Path(project_dir))))
    except Exception as exc:
        print(f"┌─ CLOCO ─┐ (welcome banner unavailable: {exc})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Claude Code status line for cloco — two lines, no session cost.

Line 1  project · type · phase ▸ next command · gates
Line 2  git │ data registry │ context bar │ model

Also sets the terminal tab/window title ("cloco · Strategy · master*") by
writing an OSC 0 sequence straight to /dev/tty, because Claude Code captures
the script's stdout. Disable with CLOCO_NO_TITLE=1.

Configured in .claude/settings.json → "statusLine". Reads the session JSON
Claude Code passes on stdin (model, workspace, context_window); everything
project-related comes from project_state.py. Fails soft: any error yields a
minimal one-line status rather than nothing.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# ANSI
R, B = "\033[0m", "\033[1m"
DIM, CYAN, GREEN, YELLOW, RED, MAGENTA, BLUE = "\033[2m", "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[35m", "\033[34m"


def read_stdin() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def ctx_bar(pct: float | None, width: int = 10) -> str:
    if pct is None:
        return f"{DIM}ctx —{R}"
    filled = int(round(pct / 100 * width))
    color = GREEN if pct < 70 else YELLOW if pct < 85 else RED
    return f"{color}ctx {'▓' * filled}{'░' * (width - filled)} {pct:.0f}%{R}"


def set_title(title: str) -> None:
    if os.environ.get("CLOCO_NO_TITLE"):
        return
    try:
        with open("/dev/tty", "w") as tty:
            tty.write(f"\033]0;{title}\007")
            tty.flush()
    except Exception:
        pass


def truncate(s: str, cols: int) -> str:
    """Trim visible length to the terminal width (ANSI codes don't count)."""
    import re
    visible = re.sub(r"\033\[[0-9;]*m", "", s)
    if len(visible) <= cols:
        return s
    # crude but safe: drop trailing segments until it fits
    parts = s.split(" │ ")
    while len(parts) > 1 and len(re.sub(r"\033\[[0-9;]*m", "", " │ ".join(parts))) > cols:
        parts.pop()
    out = " │ ".join(parts)
    return out if len(re.sub(r"\033\[[0-9;]*m", "", out)) <= cols else visible[: cols - 1] + "…"


def main() -> int:
    data = read_stdin()
    cols = int(os.environ.get("COLUMNS", "120") or 120)
    root = (data.get("workspace") or {}).get("project_dir") or data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR")
    model = (data.get("model") or {}).get("display_name") or ""
    cw = data.get("context_window") or {}
    pct = cw.get("used_percentage")

    try:
        from project_state import state  # type: ignore
        st = state(Path(root) if root else None)
    except Exception:
        st = {"has_project": False, "repo": Path(root).name if root else "cloco", "git": None, "data": None}

    # ---- line 1: project / phase / next / gates
    if st.get("has_project"):
        g = st.get("gates") or {}
        sc = g.get("score")
        gate = lambda ok, label: f"{GREEN}{label} ✓{R}" if ok else f"{DIM}{label} ○{R}"
        gates = f"{gate(g.get('commit'), 'Commit')} {gate(g.get('pr'), 'PR')} {gate(g.get('submission'), 'Submit')}"
        if sc is not None:
            gates += f" {DIM}{sc}{R}"
        name = (st.get("project_name") or "")[:40]
        line1 = (f"{B}{st['repo']}{R} · {name} · {DIM}{st['project_type']}{R} · "
                 f"{CYAN}Phase {st['phase_num']} {st['phase']}{R} ▸ {B}{st['next']}{R}   {gates}")
        if (st.get("identity") or {}).get("needs_detach"):
            line1 += f"  {YELLOW}⚠ template identity → /setup-project{R}"
        title_phase = st["phase"]
    else:
        line1 = f"{B}{st.get('repo', 'cloco')}{R} · {DIM}no research spec{R} ▸ {B}/scout{R} or {B}/interview-me{R}"
        title_phase = "no project"

    # ---- line 2: git │ data │ ctx │ model
    segs = []
    gs = st.get("git")
    if gs:
        dirty_col = YELLOW if gs["dirty"] and gs["on_default"] else (DIM if not gs["dirty"] else R)
        git = f"{MAGENTA}{gs['branch']}{R} ↑{gs['ahead']} ↓{gs['behind']} {dirty_col}{gs['dirty']} dirty{R}"
        if gs["worktrees"]:
            git += f" · {gs['worktrees']} wt"
        segs.append(git)
    ds = st.get("data")
    if ds and ds.get("registered") is not None:
        d = f"data {ds['registered']} reg"
        if ds["missing"]:
            d += f" · {RED}{len(ds['missing'])} missing{R}"
        segs.append(d)
    elif ds is not None:
        segs.append(f"{DIM}data ?{R}")
    segs.append(ctx_bar(pct))
    if model:
        segs.append(f"{BLUE}{model}{R}")
    line2 = " │ ".join(segs)

    print(truncate(line1, cols))
    print(truncate(line2, cols))

    star = "*" if gs and gs["dirty"] else ""
    set_title(f"{st.get('repo', 'cloco')} · {title_phase} · {gs['branch'] + star if gs else ''}".rstrip(" ·"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never leave the bar empty
        print(f"cloco · status error: {exc}")
        sys.exit(0)

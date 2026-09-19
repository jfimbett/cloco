#!/usr/bin/env python3
"""
cloco dashboard — the /pipeline-status box, from the shell, without Claude.

    python3 .claude/scripts/dashboard.py          # or: make status
    python3 .claude/scripts/dashboard.py --watch  # refresh every 30 s (Ctrl-C to stop)

Reads project_state.py (spec, journal scores, gates, git, data registry,
lessons) and the git audit summary. Stdlib only.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_state import PHASES, WEIGHTS, project_root, state  # noqa: E402

W = 66
COMPONENTS = {
    "Discovery": [("Literature", "academic-editor"), ("Data", "data-quality-surveyor")],
    "Strategy": [("Theory", "theory-critic"), ("Identification", "identification-critic"), ("Structural", "structural-critic")],
    "Execution": [("Code", "debugger"), ("Polish", "academic-proofreader")],
    "Peer Review": [("PeerReview", "blind-peer-referee ×2")],
    "Submission": [("Replication", "replication-verifier")],
}


def row(text: str = "") -> str:
    text = text if len(text) <= W - 4 else text[: W - 5] + "…"
    return f"║  {text:<{W - 4}}║"


def bar(title: str) -> list[str]:
    return [f"╠{'═' * (W - 2)}╣", row(title)]


def fmt_score(v):
    return "not started" if v is None else ("PASS" if v == 100 and False else f"{v:.0f}/100")


def render(st: dict) -> str:
    lines = [f"╔{'═' * (W - 2)}╗", row("CLOCO RESEARCH PIPELINE STATUS")]
    if not st.get("has_project"):
        lines += bar("No active research project.")
        lines += [row(), row("Not sure about the idea?   /scout [idea]"), row("Committed?                 /interview-me, then /discovery"),
                  row("Full pipeline:             /new-project [topic]")]
    else:
        ptype = st["project_type"]
        weights = WEIGHTS.get(ptype, WEIGHTS["empirical"])
        lines += bar(f"Project:  {st['project_name'][:50]}")
        lines.append(row(f"Type:     {ptype:<22} Phase {st['phase_num']} of 5 — {st['phase']}"))
        lines += bar("PIPELINE")
        for i, ph in enumerate(PHASES, start=1):
            icon = "✓" if i < st["phase_num"] else ("▶" if i == st["phase_num"] else "○")
            here = "   ← YOU ARE HERE" if i == st["phase_num"] else ""
            lines.append(row(f"{icon} {i} · {ph}{here}"))
            comps = [(c, a) for c, a in COMPONENTS[ph] if c in weights]
            for j, (c, a) in enumerate(comps):
                branch = "└─" if j == len(comps) - 1 else "├─"
                v = st["scores"].get(c)
                lines.append(row(f"    {branch} {c:<16} {a:<24} {fmt_score(v)}"))
        g = st["gates"]
        lines += bar("GATES")
        tick = lambda b: "✓" if b else "○"
        lines.append(row(f"Commit ≥80 {tick(g['commit'])}   PR ≥90 {tick(g['pr'])}   Submit ≥95 {tick(g['submission'])}   Overall: {g['score'] if g['score'] is not None else 'N/A'}"))
        if st.get("last"):
            l = st["last"]
            lines += bar("LAST ACTION")
            lines.append(row(f"{l['agent']} ({l['score'] or '—'}) {l['verdict']}"[: W - 4]))
        lines += bar("NEXT STEP")
        lines.append(row(f"→ {st['next']}"))
    gs, ds, ls = st.get("git"), st.get("data"), st.get("lessons")
    lines += bar("REPO · DATA · LESSONS")
    if gs:
        warn = "  ← branch or worktree?" if gs["on_default"] and gs["dirty"] else ""
        lines.append(row(f"git    {gs['branch']} ↑{gs['ahead']} ↓{gs['behind']} · {gs['dirty']} uncommitted · {gs['worktrees']} wt{warn}"))
    if ds and ds.get("registered") == 0:
        lines.append(row("data   registry empty → /data-registry setup or /wrds search"))
    elif ds and ds.get("registered") is not None:
        miss = f" · missing: {', '.join(ds['missing'][:3])}{'…' if len(ds['missing']) > 3 else ''}" if ds["missing"] else " · all present"
        lines.append(row(f"data   {ds['registered']} registered{miss}"[: W - 4]))
    if ls:
        lines.append(row(f"lessons {ls['count']} recorded" + (f" · latest {ls['latest_date']} [{ls['latest_category']}]" if ls["count"] else "")))
    lines.append(f"╚{'═' * (W - 2)}╝")
    return "\n".join(lines)


def audit_summary(root: Path) -> str:
    tool = root / ".claude" / "scripts" / "git_tools.py"
    if not tool.exists():
        return ""
    try:
        r = subprocess.run([sys.executable, str(tool), "audit"], capture_output=True, text=True, timeout=20, cwd=root)
        import re
        parts = []
        for l in r.stdout.splitlines():
            if l.startswith("Secrets in tree"):
                parts.append("secrets " + re.sub(r"\s+", " ", l.split("tree", 1)[1]).strip())
            elif l.startswith("Large tracked"):
                parts.append("big files " + re.sub(r"\s+", " ", l.split("files", 1)[1]).strip().split(" ≥")[0])
            elif l.startswith("Remote") and "http://" in l:
                parts.append("remote ✗ http://")
        return "  git audit: " + " · ".join(parts) if parts else ""
    except Exception:
        return ""


def main() -> int:
    root = project_root()
    watch = "--watch" in sys.argv
    while True:
        st = state(root)
        out = render(st)
        if watch:
            os.system("clear")
        print(out)
        print(audit_summary(root))
        if not watch:
            return 0
        time.sleep(30)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)

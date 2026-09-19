#!/usr/bin/env python3
"""
Project state — the single source of truth consumed by the session-welcome
hook, the Claude Code status line, the shell dashboard, and anything else
that wants to know "where is this project right now?".

    python3 .claude/scripts/project_state.py            # JSON
    python3 .claude/scripts/project_state.py --brief    # one line

Reads (all optional):
    quality_reports/research_spec_*.md    project_name, project_type, project_slug
    git remotes + folder name             template-vs-project identity (project_setup.py)
    quality_reports/research_journal.md   component scores (highest per component)
    data/registry.json + .env             registered datasets present / missing
    .claude/lessons/LESSONS.md            lesson count
    git                                   branch, ahead/behind, dirty count, worktrees

Stdlib only; every section fails soft (returns None/empty) so consumers can
always render something.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

THRESHOLD = 80.0
PHASES = ["Discovery", "Strategy", "Execution", "Peer Review", "Submission"]

AGENT_COMPONENT = {
    "academic-librarian": "Literature", "academic-editor": "Literature",
    "explorer": "Data", "data-quality-surveyor": "Data",
    "causal-strategist": "Identification", "identification-critic": "Identification", "econometrics-critic": "Identification",
    "econ-finance-theorist": "Theory", "theory-critic": "Theory",
    "structural-estimation-expert": "Structural", "structural-critic": "Structural",
    "coder": "Code", "debugger": "Code",
    "economics-paper-writer": "Paper", "blind-peer-referee": "PeerReview",
    "academic-proofreader": "Polish", "replication-verifier": "Replication",
}
WEIGHTS = {
    "empirical": {"Literature": .10, "Data": .10, "Identification": .25, "Code": .15, "PeerReview": .25, "Polish": .10, "Replication": .05},
    "theory": {"Literature": .15, "Theory": .40, "PeerReview": .30, "Polish": .15},
    "structural": {"Literature": .10, "Data": .10, "Theory": .15, "Structural": .20, "Code": .15, "PeerReview": .20, "Polish": .05, "Replication": .05},
    "empirical+theory": {"Literature": .10, "Data": .10, "Theory": .10, "Identification": .20, "Code": .15, "PeerReview": .25, "Polish": .05, "Replication": .05},
}
NEXT_CMD = {
    1: {t: "/discovery" for t in WEIGHTS},
    2: {"empirical": "/identify", "theory": "/theory-model", "structural": "/theory-model", "empirical+theory": "/theory-model"},
    3: {"empirical": "/data-analysis", "theory": "/draft-paper", "structural": "/data-analysis", "empirical+theory": "/data-analysis"},
    4: {t: "/review-paper" for t in WEIGHTS},
    5: {t: "/submit" for t in WEIGHTS},
}


def project_root(explicit: str | None = None) -> Path:
    for cand in (explicit, os.environ.get("CLAUDE_PROJECT_DIR")):
        if cand:
            return Path(cand)
    here = Path(__file__).resolve()
    for p in (here.parents[2], Path.cwd()):
        if (p / ".claude").is_dir():
            return p
    return Path.cwd()


# --------------------------------------------------------------------------- #
# Spec + journal
# --------------------------------------------------------------------------- #
def read_spec(root: Path) -> dict | None:
    specs = sorted(root.glob("quality_reports/research_spec_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not specs:
        return None
    text = specs[0].read_text(encoding="utf-8", errors="replace")
    info = {"project_name": None, "project_type": "empirical", "spec_file": specs[0].name}
    for line in text.splitlines():
        low = line.lower()
        m = re.search(r":\s*(.+)", line)
        if not m:
            continue
        if "project_name" in low or "project name" in low:
            info["project_name"] = m.group(1).strip().strip("*").strip()
        elif "project_type" in low or "project type" in low:
            pt = m.group(1).strip().strip("*").strip().lower()
            if pt in WEIGHTS:
                info["project_type"] = pt
    if not info["project_name"]:
        m = re.search(r"^#\s*Research Specification:\s*(.+)$", text, re.M)
        if m:
            info["project_name"] = m.group(1).strip()
    if not info["project_name"]:
        info["project_name"] = specs[0].stem.replace("research_spec_", "").replace("_", " ")
    return info


def _score(s: str | None) -> float | None:
    if not s:
        return None
    if "pass" in s.lower():
        return 100.0
    if "fail" in s.lower():
        return 0.0
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def read_journal(root: Path) -> dict:
    path = root / "quality_reports" / "research_journal.md"
    out = {"scores": {}, "last": None, "entries": 0}
    if not path.exists():
        return out
    agent = score = verdict = when = None

    def flush():
        if agent:
            out["entries"] += 1
            comp = next((c for k, c in AGENT_COMPONENT.items() if k in agent.lower()), None)
            val = _score(score)
            if comp and val is not None and out["scores"].get(comp, -1) < val:
                out["scores"][comp] = val
            out["last"] = {"agent": agent, "score": score, "verdict": (verdict or "")[:70], "when": when}

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("### "):
            flush()
            agent = score = verdict = when = None
            m = re.match(r"###\s*(\S+ \S+)?\s*—\s*(.+)$", line)
            if m:
                when, agent = m.group(1), m.group(2).strip()
        elif line.startswith("**Score:**"):
            score = line.split("**Score:**", 1)[1].strip()
        elif line.startswith("**Verdict:**"):
            verdict = line.split("**Verdict:**", 1)[1].strip()
    flush()
    return out


def detect_phase(scores: dict, ptype: str) -> tuple[int, str]:
    done = lambda c: scores.get(c, -1) >= THRESHOLD
    discovery = done("Literature") if ptype == "theory" else done("Literature") and done("Data")
    strategy = {"empirical": done("Identification"), "theory": done("Theory"), "structural": done("Structural")}.get(
        ptype, done("Theory") and done("Identification"))
    # The paper is scored by its critic (academic-proofreader → "Polish"); the writer never self-scores.
    execution = done("Polish") if ptype == "theory" else done("Code") and done("Polish")
    peer = done("PeerReview")
    submission = peer if ptype == "theory" else peer and done("Replication")
    for i, ok in enumerate((discovery, strategy, execution, peer, submission), start=1):
        if not ok:
            return i, PHASES[i - 1]
    return 5, "Submission — complete"


def gates(scores: dict, ptype: str) -> dict:
    w = WEIGHTS.get(ptype, WEIGHTS["empirical"])
    present = {c: s for c, s in scores.items() if c in w}
    if not present:
        return {"score": None, "commit": False, "pr": False, "submission": False}
    tot = sum(w[c] for c in present)
    sc = round(sum(present[c] * w[c] for c in present) / tot, 1)
    return {"score": sc, "commit": sc >= 80, "pr": sc >= 90, "submission": sc >= 95 and all(v >= 80 for v in present.values())}


# --------------------------------------------------------------------------- #
# Git, data, lessons
# --------------------------------------------------------------------------- #
def git_state(root: Path) -> dict | None:
    def g(*a):
        r = subprocess.run(["git", *a], cwd=root, capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    try:
        if not g("rev-parse", "--is-inside-work-tree"):
            return None
        branch = g("branch", "--show-current") or "(detached)"
        up = g("rev-parse", "--abbrev-ref", "@{u}")
        ahead = behind = 0
        if up:
            lr = g("rev-list", "--left-right", "--count", "@{u}...HEAD").split()
            if len(lr) == 2:
                behind, ahead = int(lr[0]), int(lr[1])
        dirty = len([l for l in g("status", "--porcelain").splitlines() if l])
        wts = max(len(g("worktree", "list").splitlines()) - 1, 0)
        return {"branch": branch, "upstream": up or None, "ahead": ahead, "behind": behind, "dirty": dirty, "worktrees": wts,
                "on_default": branch in ("master", "main")}
    except Exception:
        return None


def data_state(root: Path) -> dict | None:
    reg = root / "data" / "registry.json"
    if not reg.exists():
        return None
    try:
        sys.path.insert(0, str(root / ".claude" / "scripts"))
        from data_registry import load_env, load_registry, resolve  # type: ignore
        ds = load_registry().get("datasets", {})
        env = load_env()
        missing = []
        for n, d in ds.items():
            p, unset = resolve(d.get("path", ""), env)
            if unset or not p.exists():
                missing.append(n)
        return {"registered": len(ds), "missing": missing}
    except Exception:
        return {"registered": None, "missing": []}


def identity_state(root: Path) -> dict | None:
    """Template-vs-project identity (folder name, origin remote) — see project_setup.py."""
    try:
        sys.path.insert(0, str(root / ".claude" / "scripts"))
        from project_setup import identity  # type: ignore
        idn = identity(root)
        return {"verdict": idn["verdict"], "needs_detach": idn["needs_detach"], "folder": idn["folder"],
                "origin_repo": idn["origin_repo"], "suggested_repo": idn["suggested_repo"], "problems": idn["problems"]}
    except Exception:
        return None


def lessons_state(root: Path) -> dict | None:
    p = root / ".claude" / "lessons" / "LESSONS.md"
    if not p.exists():
        return None
    entries = re.findall(r"^### (\d{4}-\d{2}-\d{2}) — (.+)$", p.read_text(encoding="utf-8", errors="replace"), re.M)
    return {"count": len(entries), "latest_date": entries[0][0] if entries else None, "latest_category": entries[0][1].strip() if entries else None}


# --------------------------------------------------------------------------- #
# Assemble
# --------------------------------------------------------------------------- #
def state(root: Path | None = None) -> dict:
    root = root or project_root()
    spec = read_spec(root)
    journal = read_journal(root)
    st: dict = {"root": str(root), "repo": root.name, "has_project": spec is not None}
    if spec:
        ptype = spec["project_type"]
        n, name = detect_phase(journal["scores"], ptype)
        st.update({
            "project_name": spec["project_name"], "project_type": ptype,
            "phase_num": n, "phase": name, "next": NEXT_CMD.get(n, {}).get(ptype, "/pipeline-status"),
            "scores": journal["scores"], "gates": gates(journal["scores"], ptype), "last": journal["last"],
            "journal_entries": journal["entries"],
        })
    st["git"] = git_state(root)
    st["data"] = data_state(root)
    st["lessons"] = lessons_state(root)
    st["identity"] = identity_state(root)
    return st


def brief(st: dict) -> str:
    parts = []
    if st.get("has_project"):
        parts.append(f"{st['project_name']} · {st['project_type']} · Phase {st['phase_num']} {st['phase']} ▸ {st['next']}")
    else:
        parts.append(f"{st['repo']} · no research spec ▸ /scout or /interview-me")
    g = st.get("git")
    if g:
        parts.append(f"{g['branch']} ↑{g['ahead']} ↓{g['behind']} {g['dirty']} dirty")
    d = st.get("data")
    if d and d.get("registered") is not None:
        parts.append(f"data {d['registered']} reg" + (f" · {len(d['missing'])} missing" if d["missing"] else ""))
    return " │ ".join(parts)


if __name__ == "__main__":
    st = state()
    print(brief(st) if "--brief" in sys.argv else json.dumps(st, indent=2, default=str))

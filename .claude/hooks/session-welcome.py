#!/usr/bin/env python3
"""
Session Welcome Hook

Fires on every fresh SessionStart (not post-compact restores) and prints a
concise banner showing project name, current phase, last action, and next command.

Hook Event: SessionStart
Returns: Exit code 0 (informational, never blocks)

Skip conditions:
  1. hook_input["type"] == "compact"  → post-compact-restore.py handles it
  2. pre-compact-state.json exists    → compact is in progress
"""

from __future__ import annotations

import json
import os
import re
import sys
import hashlib
from pathlib import Path


def get_session_dir() -> Path:
    """Get the session directory (same hash logic as pre-compact.py)."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def find_research_spec(project_dir: str) -> dict | None:
    """Find and parse the research spec for project_name and project_type."""
    spec_files = sorted(
        Path(project_dir).glob("quality_reports/research_spec_*.md"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not spec_files:
        return None

    content = spec_files[0].read_text(encoding="utf-8", errors="replace")
    info = {"project_name": None, "project_type": "empirical"}

    for line in content.splitlines():
        lower = line.lower()
        if "project_name" in lower or "project name" in lower:
            # e.g. "project_name: Effect of Carbon Taxes"
            m = re.search(r":\s*(.+)", line)
            if m:
                info["project_name"] = m.group(1).strip()
        if "project_type" in lower or "project type" in lower:
            m = re.search(r":\s*(.+)", line)
            if m:
                pt = m.group(1).strip().lower()
                if pt in ("empirical", "theory", "structural", "empirical+theory"):
                    info["project_type"] = pt

    return info


def parse_journal(project_dir: str) -> dict:
    """
    Parse quality_reports/research_journal.md.

    Returns:
        {
            "last_entry": str,       # one-line summary of the most recent entry
            "component_scores": {    # component name -> highest score seen
                "Literature": 87,
                "Data": 72,
                ...
            },
            "overall": float | None  # computed weighted score (simplified)
        }
    """
    journal_path = Path(project_dir) / "quality_reports" / "research_journal.md"
    if not journal_path.exists():
        return {"last_entry": None, "component_scores": {}, "overall": None}

    content = journal_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    component_scores: dict[str, float] = {}
    last_entry: str | None = None
    current_agent: str | None = None
    current_score: str | None = None
    current_verdict: str | None = None

    for line in lines:
        # Detect entry header: ### YYYY-MM-DD HH:MM — Agent Name
        if line.startswith("### "):
            # Save previous entry data
            if current_agent and current_score:
                _update_component_scores(component_scores, current_agent, current_score)
            if current_agent:
                last_entry = _format_last_entry(current_agent, current_score, current_verdict)
            current_agent = None
            current_score = None
            current_verdict = None
            # Extract agent name
            m = re.search(r"—\s*(.+)$", line)
            if m:
                current_agent = m.group(1).strip()
        elif line.startswith("**Score:**"):
            m = re.search(r"\*\*Score:\*\*\s*(.+)", line)
            if m:
                current_score = m.group(1).strip()
        elif line.startswith("**Verdict:**"):
            m = re.search(r"\*\*Verdict:\*\*\s*(.+)", line)
            if m:
                current_verdict = m.group(1).strip()[:60]

    # Handle last entry in file
    if current_agent and current_score:
        _update_component_scores(component_scores, current_agent, current_score)
    if current_agent:
        last_entry = _format_last_entry(current_agent, current_score, current_verdict)

    return {
        "last_entry": last_entry,
        "component_scores": component_scores,
        "overall": None,  # Simplified; full calc in pipeline-status skill
    }


def _parse_score(score_str: str | None) -> float | None:
    """Extract numeric score from strings like '87/100', 'PASS', '72'."""
    if not score_str:
        return None
    if "pass" in score_str.lower():
        return 100.0
    if "fail" in score_str.lower():
        return 0.0
    m = re.search(r"(\d+(?:\.\d+)?)", score_str)
    if m:
        return float(m.group(1))
    return None


def _update_component_scores(scores: dict, agent: str, score_str: str) -> None:
    """Map agent name to a component key and record the score."""
    agent_lower = agent.lower()
    score = _parse_score(score_str)
    if score is None:
        return

    mapping = {
        "academic-librarian": "Literature",
        "academic-editor": "Literature",
        "explorer": "Data",
        "data-quality-surveyor": "Data",
        "causal-strategist": "Identification",
        "identification-critic": "Identification",
        "econometrics-critic": "Identification",
        "econ-finance-theorist": "Theory",
        "theory-critic": "Theory",
        "structural-estimation-expert": "Structural",
        "structural-critic": "Structural",
        "coder": "Code",
        "debugger": "Code",
        "economics-paper-writer": "Paper",
        "blind-peer-referee": "PeerReview",
        "academic-proofreader": "Polish",
        "replication-verifier": "Replication",
    }
    for key, component in mapping.items():
        if key in agent_lower:
            # Keep the highest score seen for each component
            if component not in scores or scores[component] < score:
                scores[component] = score
            break


def _format_last_entry(agent: str, score: str | None, verdict: str | None) -> str:
    """Build a one-line last-action summary."""
    parts = [agent]
    if score:
        parts.append(f"({score})")
    if verdict:
        parts.append(f"— {verdict}")
    return " ".join(parts)[:70]


def detect_current_phase(component_scores: dict, project_type: str) -> tuple[int, str]:
    """
    Determine which pipeline phase is currently active.

    Returns: (phase_number 1-5, phase_name)
    Phase is the first one that is NOT done.
    """

    THRESHOLD = 80.0

    def done(component: str) -> bool:
        s = component_scores.get(component)
        return s is not None and s >= THRESHOLD

    # Discovery requirements by type
    if project_type == "theory":
        discovery_done = done("Literature")
    else:
        discovery_done = done("Literature") and done("Data")

    # Strategy requirements by type
    if project_type == "empirical":
        strategy_done = done("Identification")
    elif project_type == "theory":
        strategy_done = done("Theory")
    elif project_type == "structural":
        strategy_done = done("Structural")
    else:  # empirical+theory
        strategy_done = done("Theory") and done("Identification")

    # Execution: code + paper (theory skips code)
    if project_type == "theory":
        execution_done = done("Paper") and done("Polish")
    else:
        execution_done = done("Code") and done("Paper") and done("Polish")

    # Peer review
    peer_review_done = done("PeerReview")

    # Submission: replication + overall (simplified: just replication for non-theory)
    if project_type == "theory":
        submission_done = peer_review_done  # simplified
    else:
        submission_done = peer_review_done and done("Replication")

    if not discovery_done:
        return (1, "Discovery")
    if not strategy_done:
        return (2, "Strategy")
    if not execution_done:
        return (3, "Execution")
    if not peer_review_done:
        return (4, "Peer Review")
    if not submission_done:
        return (5, "Submission")
    return (5, "Submission — complete")


def next_command(phase_num: int, project_type: str) -> str:
    """Return the recommended next skill command."""
    table = {
        1: {
            "empirical": "/discovery",
            "theory": "/discovery",
            "structural": "/discovery",
            "empirical+theory": "/discovery",
        },
        2: {
            "empirical": "/identify [research question]",
            "theory": "/theory-model [topic]",
            "structural": "/theory-model [topic]",
            "empirical+theory": "/theory-model [topic]",
        },
        3: {
            "empirical": "/data-analysis [dataset]",
            "theory": "/draft-paper [section]",
            "structural": "/data-analysis [dataset]",
            "empirical+theory": "/data-analysis [dataset]",
        },
        4: {
            "empirical": "/review-paper [file]",
            "theory": "/review-paper [file]",
            "structural": "/review-paper [file]",
            "empirical+theory": "/review-paper [file]",
        },
        5: {
            "empirical": "/submit [journal]",
            "theory": "/submit [journal]",
            "structural": "/submit [journal]",
            "empirical+theory": "/submit [journal]",
        },
    }
    return table.get(phase_num, {}).get(project_type, "/pipeline-status")


def compute_gate_status(component_scores: dict, project_type: str) -> dict:
    """Return commit/PR/submission gate status based on a simplified aggregate."""
    if not component_scores:
        return {"commit": False, "pr": False, "submission": False}

    # Weights by project type (from scoring-protocol.md)
    weights: dict[str, dict[str, float]] = {
        "empirical": {
            "Literature": 0.10, "Data": 0.10, "Identification": 0.25,
            "Code": 0.15, "PeerReview": 0.25, "Polish": 0.10, "Replication": 0.05,
        },
        "theory": {
            "Literature": 0.15, "Theory": 0.40, "PeerReview": 0.30, "Polish": 0.15,
        },
        "structural": {
            "Literature": 0.10, "Data": 0.10, "Theory": 0.15, "Structural": 0.20,
            "Code": 0.15, "PeerReview": 0.20, "Polish": 0.05, "Replication": 0.05,
        },
        "empirical+theory": {
            "Literature": 0.10, "Data": 0.10, "Theory": 0.10, "Identification": 0.20,
            "Code": 0.15, "PeerReview": 0.25, "Polish": 0.05, "Replication": 0.05,
        },
    }
    w = weights.get(project_type, weights["empirical"])

    # Only include components that have scores; renormalize
    present = {c: s for c, s in component_scores.items() if c in w}
    if not present:
        return {"commit": False, "pr": False, "submission": False, "score": None}

    total_weight = sum(w[c] for c in present)
    score = sum(present[c] * w[c] for c in present) / total_weight

    return {
        "commit": score >= 80,
        "pr": score >= 90,
        "submission": score >= 95,
        "score": round(score, 1),
    }


def lessons_line() -> str:
    """One-line reminder to read .claude/lessons/LESSONS.md, with count + latest category."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    path = Path(project_dir) / ".claude" / "lessons" / "LESSONS.md"
    if not path.exists():
        return ""
    entries = re.findall(r"^### (\d{4}-\d{2}-\d{2}) — (.+)$", path.read_text(encoding="utf-8", errors="replace"), re.M)
    if not entries:
        return "  Lessons: none yet (.claude/lessons/LESSONS.md)."
    date, cat = entries[0]
    return f"  Lessons: {len(entries)} recorded — latest {date} [{cat.strip()}]. Read .claude/lessons/LESSONS.md before starting."


def registry_line() -> str:
    """One-line data registry status: count + missing on this machine."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    reg = Path(project_dir) / "data" / "registry.json"
    if not reg.exists():
        return ""
    try:
        sys.path.insert(0, str(Path(project_dir) / ".claude" / "scripts"))
        from data_registry import load_env, load_registry, resolve  # type: ignore
        ds = load_registry().get("datasets", {})
        if not ds:
            return "  Data: registry empty — /data-registry setup, /wrds search, or /find-data."
        env = load_env()
        missing = [n for n, d in ds.items() if (lambda r: r[1] or not r[0].exists())(resolve(d.get("path", ""), env))]
        tail = f"; {len(missing)} not on this machine ({', '.join(missing[:3])}{'…' if len(missing) > 3 else ''}) → /data-registry check" if missing else "; all present"
        return f"  Data: {len(ds)} registered{tail}"
    except Exception:
        return "  Data: registry unreadable — /data-registry check"


def format_welcome_with_project(
    project_name: str,
    project_type: str,
    phase_num: int,
    phase_name: str,
    last_entry: str | None,
    next_cmd: str,
    gates: dict,
) -> str:
    """Format the welcome banner for an active project."""
    W = 64
    border = "─" * (W - 2)

    def row(text: str) -> str:
        return f"│  {text:<{W - 4}}│"

    gate_commit = "✅" if gates.get("commit") else "○"
    gate_pr = "✅" if gates.get("pr") else "○"
    gate_sub = "✅" if gates.get("submission") else "○"
    score_str = f"  (overall: {gates['score']}/100)" if gates.get("score") else ""

    name_display = (project_name or "Unnamed project")[:50]
    type_display = f"{project_type.capitalize()} · Phase {phase_num} of 5: {phase_name}"
    last_display = (last_entry or "no entries yet")[:58]

    lines = [
        f"┌─ CLOCO {border[8:]}┐",
        row(f"Project  {name_display}"),
        row(f"Type     {type_display}"),
        row(f"Last     {last_display}"),
        row(f"Next     {next_cmd}"),
        row(f"Gates    Commit {gate_commit}  PR {gate_pr}  Submission {gate_sub}{score_str}"),
        f"└{border}┘",
        "  Type /pipeline-status for the full dashboard.",
        registry_line(),
        lessons_line(),
    ]
    return "\n".join(lines)


def format_welcome_no_project() -> str:
    """Format the welcome banner when no project is found."""
    W = 64
    border = "─" * (W - 2)

    def row(text: str) -> str:
        return f"│  {text:<{W - 4}}│"

    lines = [
        f"┌─ CLOCO {border[8:]}┐",
        row("No active research project."),
        row("Not sure about the idea?   /scout [idea]"),
        row("Committed?                 /interview-me [topic], /discovery"),
        row("Full pipeline:             /new-project [topic]"),
        f"└{border}┘",
        "  Type /pipeline-status for a full list of available commands.",
        registry_line(),
        lessons_line(),
    ]
    return "\n".join(lines)


def main() -> int:
    """Main hook entry point."""
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    # Guard 1: skip post-compact restores (post-compact-restore.py handles those)
    if hook_input.get("type") == "compact":
        return 0

    # Guard 2: skip if a compact is in progress
    session_dir = get_session_dir()
    if (session_dir / "pre-compact-state.json").exists():
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    # Try to find project info
    spec = find_research_spec(project_dir)

    if spec is None:
        print(format_welcome_no_project())
        return 0

    journal = parse_journal(project_dir)
    component_scores = journal["component_scores"]
    project_type = spec.get("project_type", "empirical")
    project_name = spec.get("project_name") or "Unnamed project"

    phase_num, phase_name = detect_current_phase(component_scores, project_type)
    next_cmd = next_command(phase_num, project_type)
    gates = compute_gate_status(component_scores, project_type)

    print(
        format_welcome_with_project(
            project_name=project_name,
            project_type=project_type,
            phase_num=phase_num,
            phase_name=phase_name,
            last_entry=journal.get("last_entry"),
            next_cmd=next_cmd,
            gates=gates,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

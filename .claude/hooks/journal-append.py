#!/usr/bin/env python3
"""
Research Journal Auto-Append Hook

Fires on PostToolUse for the Agent (subagent) tool. Extracts the agent type,
the score (if the agent reported one), a one-line verdict, and any report
path mentioned in the result, then appends an entry to
quality_reports/research_journal.md in the format required by
.claude/rules/research-journal.md.

This automates the "append after every agent report" rule so it no longer
depends on Claude remembering to do it.

Hook Event: PostToolUse (matcher: "Agent|Task")
Returns: Exit code 0, always. Emits additionalContext telling Claude the
         entry was written (or why it was skipped).

Skips silently when:
  - the tool is not Agent/Task
  - the subagent is a non-research agent (Explore, Plan, general-purpose, ...)
  - CLAUDE_PROJECT_DIR is unset
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Agents whose runs belong in the research journal, with their pipeline phase.
RESEARCH_AGENTS: dict[str, str] = {
    "academic-librarian": "Discovery",
    "academic-editor": "Discovery",
    "explorer": "Discovery",
    "data-quality-surveyor": "Discovery",
    "idea-critic": "Discovery",
    "causal-strategist": "Strategy",
    "identification-critic": "Strategy",
    "econ-finance-theorist": "Strategy",
    "theory-critic": "Strategy",
    "structural-estimation-expert": "Strategy",
    "structural-critic": "Strategy",
    "econometrics-critic": "Strategy",
    "debugger": "Execution",
    "economics-paper-writer": "Execution",
    "academic-proofreader": "Execution",
    "replication-verifier": "Execution",
    "blind-peer-referee": "Peer Review",
    "storyteller": "Presentation",
    "discussant": "Presentation",
    "research-orchestrator": "Pipeline",
}

SCORE_PATTERNS = [
    r"\*\*Score:\*\*\s*(\d{1,3})\s*/\s*100",
    r"Verdict:\s*(?:GO|REFRAME|NO-GO)\s*[—-]\s*(\d{1,3})\s*/\s*100",
    r"Final(?: Score)?:\s*\**\s*(\d{1,3})\s*/\s*100",
    r"Overall(?: Score)?:\s*\**\s*(\d{1,3})\s*/\s*100",
    r"Score:\s*(\d{1,3})\s*/\s*100",
    r"\b(\d{1,3})\s*/\s*100\b",
]

PASSFAIL_PATTERN = r"\b(PASS|FAIL)\b"
VERDICT_PATTERNS = [
    r"\*\*Verdict:\*\*\s*(.+)",
    r"##\s*Verdict:\s*(.+)",
    r"\*\*Decision:\*\*\s*(.+)",
    r"##\s*Executive Summary\s*\n+(.+)",
    r"##\s*Summary Judgment\s*\n+(.+)",
]
REPORT_PATH_PATTERN = r"(quality_reports/[A-Za-z0-9_./\-]+\.(?:md|csv|bib))"


def response_text(tool_response) -> str:
    """Flatten whatever shape the Agent tool returned into one string."""
    if tool_response is None:
        return ""
    if isinstance(tool_response, str):
        return tool_response
    if isinstance(tool_response, dict):
        parts = []
        for key in ("content", "result", "output", "text", "message"):
            val = tool_response.get(key)
            if isinstance(val, str):
                parts.append(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        parts.append(item["text"])
                    elif isinstance(item, str):
                        parts.append(item)
        if parts:
            return "\n".join(parts)
        return json.dumps(tool_response)
    if isinstance(tool_response, list):
        return "\n".join(response_text(x) for x in tool_response)
    return str(tool_response)


def extract_score(text: str) -> str:
    for pat in SCORE_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if 0 <= val <= 100:
                return f"{val}/100"
    m = re.search(PASSFAIL_PATTERN, text)
    if m:
        return m.group(1).upper()
    return "N/A"


def extract_verdict(text: str) -> str:
    for pat in VERDICT_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            line = m.group(1).strip().splitlines()[0]
            return re.sub(r"\s+", " ", line)[:160]
    # Fallback: first non-empty, non-heading line
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("|"):
            return re.sub(r"\s+", " ", s)[:160]
    return "(no summary in agent output)"


def extract_report(text: str) -> str:
    m = re.search(REPORT_PATH_PATTERN, text)
    return m.group(1) if m else "—"


def extract_target(prompt: str) -> str:
    """Best-effort target from the dispatch prompt: a path or the first line."""
    m = re.search(REPORT_PATH_PATTERN, prompt or "")
    if m:
        return m.group(1)
    first = (prompt or "").strip().splitlines()[0] if prompt else ""
    first = re.sub(r"^(Prompt:|Task:)\s*", "", first, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", first)[:120] or "—"


def emit_context(msg: str) -> None:
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}},
        sys.stdout,
    )


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    if hook_input.get("tool_name") not in ("Agent", "Task"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or hook_input.get("cwd", "")
    if not project_dir:
        return 0

    tool_input = hook_input.get("tool_input", {}) or {}
    agent = (tool_input.get("subagent_type") or "").strip()
    if agent not in RESEARCH_AGENTS:
        return 0

    text = response_text(hook_input.get("tool_response"))
    score = extract_score(text)
    verdict = extract_verdict(text)
    report = extract_report(text)
    target = extract_target(tool_input.get("prompt", ""))
    phase = RESEARCH_AGENTS[agent]
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    journal = Path(project_dir) / "quality_reports" / "research_journal.md"
    journal.parent.mkdir(parents=True, exist_ok=True)
    if not journal.exists():
        project_name = Path(project_dir).name
        journal.write_text(
            f"# Research Journal — {project_name}\n\n"
            "Append-only, agent-level history. Entries are written automatically by "
            "`.claude/hooks/journal-append.py` after every research-agent dispatch; "
            "add phase transitions, escalations, and user overrides by hand.\n\n",
            encoding="utf-8",
        )

    entry = (
        f"### {stamp} — {agent}\n"
        f"**Phase:** {phase}\n"
        f"**Target:** {target}\n"
        f"**Score:** {score}\n"
        f"**Verdict:** {verdict}\n"
        f"**Report:** {report}\n\n"
    )
    with journal.open("a", encoding="utf-8") as f:
        f.write(entry)

    emit_context(
        f"[journal-append] Logged {agent} ({score}) to quality_reports/research_journal.md. "
        f"If this dispatch completed a phase or triggered an escalation, add that line to the journal by hand."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # never block on a hook bug

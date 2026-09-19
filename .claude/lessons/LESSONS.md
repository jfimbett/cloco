# Lessons Learned

Append-only log of mistakes, corrections, and prevention strategies.
Read this at the start of every session. Never edit or delete past entries.

---

## Format

```
### YYYY-MM-DD — [Category]
**Mistake:** What went wrong or what was done incorrectly.
**Correction:** What the right approach is.
**Prevention:** Concrete rule or check to avoid repeating this.
```

Categories: `workflow` · `tools` · `writing` · `econometrics` · `code` · `latex` · `agents` · `planning`

---

<!-- New lessons go below this line, most recent first -->

### 2026-09-19 — tools
**Mistake:** `.claude/settings.json` invoked hooks through a hard-coded Windows interpreter path (`C:/Users/.../python.exe`), and every hook used PEP 604 unions (`dict | None`) in function signatures. On macOS the hooks were never executed; under the system `python3` (3.9) they crash on import. No banner, no quality gate, no log reminders — silently.
**Correction:** Hooks are invoked as `python3 "$CLAUDE_PROJECT_DIR/..."`, every hook starts with `from __future__ import annotations`, and hooks stay stdlib-only. Machine-specific interpreter paths belong in `.claude/settings.local.json` (gitignored), never in the committed settings.
**Prevention:** After touching any hook, run `echo '{}' | CLAUDE_PROJECT_DIR="$PWD" python3 .claude/hooks/<hook>.py; echo $?` under the oldest Python the team uses. Keep `settings.json` free of absolute paths.

### 2026-09-19 — agents
**Mistake:** The `explorer` agent definition described a codebase cartographer, while `/find-data`, the README, scoring weights, and the orchestrator all dispatched it as a *data-discovery* agent. The pipeline's data lane had no worker that actually searched for datasets.
**Correction:** Rewrote `explorer` as a data-discovery agent (Discovery / Inventory / Quick-Scan modes, nine source categories, variable map, feasibility grades) and kept the name so every cross-reference stays valid.
**Prevention:** When a skill dispatches an agent, open the agent file and confirm its stated role and output paths match the skill's prompt before trusting the pipeline diagram.

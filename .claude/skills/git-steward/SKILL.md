---
name: git-steward
description: Repository hygiene and GitHub workflow — audit that no credentials, data files, or oversized blobs are committed or in history; propose branches and worktrees for parallel tasks (R&R vs new analysis, talk vs paper); clean merged branches and stale worktrees; check state before a push; tag submission versions. Use when the user says "audit the repo", "is it safe to push", "did I commit a secret", "set up a worktree for X", "clean up branches", or "tag the submission".
disable-model-invocation: true
argument-hint: "[audit | secrets | history-scan [N] | worktree NAME [--from BRANCH] | cleanup | tag JOURNAL | pr]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Task"]
---

# Git Steward

Deterministic checks first (`.claude/scripts/git_tools.py`), the `git-steward` agent for judgement and proposals. Nothing state-changing runs unless the subcommand asks for it.

**Input:** `$ARGUMENTS` — subcommand; empty means `audit`.

---

## `audit` (default)

```bash
python3 .claude/scripts/git_tools.py audit
```

Then dispatch `git-steward` in Audit mode with the output: it ranks findings, writes `quality_reports/git_audit_YYYY-MM-DD.md`, and gives a **SAFE TO PUSH / FIX FIRST / DO NOT PUSH** verdict with exact commands. Present the verdict and the top three actions.

## `secrets`

```bash
python3 .claude/scripts/git_tools.py secrets --staged
python3 .claude/scripts/git_tools.py secrets --unpushed
python3 .claude/scripts/git_tools.py secrets --tree
```

Any `critical` → stop, show location (never the value), and follow the agent's remediation: unstage / move to `.env` or `~/.pgpass` / move data to Dropbox and register. The `secrets-guard` hook blocks `git commit` and `git push` on the same findings automatically; this subcommand is for checking *before* you get blocked.

## `history-scan [N]`

```bash
python3 .claude/scripts/git_tools.py secrets --history ${N:-200}
```

Findings here are already in commits. The agent's protocol: **rotate first**, then decide with the user whether to purge (`git filter-repo`) — force-push and re-clone instructions are a separate, explicit confirmation.

## `worktree NAME [--from BRANCH]`

Ask the agent (Worktree-Planning mode) whether a worktree is warranted (parallel streams, long agent runs, overlapping files). If yes and the user confirms:

```bash
python3 .claude/scripts/git_tools.py worktree new NAME --from master
```

Report the path (`../<repo>-wt/NAME`), that `.env` is linked so `data_path()` works there, and that `data/raw` scratch is not shared. Inside Claude Code the `EnterWorktree` tool achieves the same from the current session.

## `cleanup`

`git_tools.py audit` → list merged branches and prunable worktrees. Delete only what the user confirms: `git branch -d <name>` (never `-D` without a separate confirmation), `git_tools.py worktree prune`, `git_tools.py worktree remove NAME --delete-branch` for worktrees with no uncommitted work.

## `tag JOURNAL`

Run `audit` first (must be SAFE TO PUSH), then on confirmation:

```bash
git tag -a submission-<journal>-$(date +%Y-%m-%d) -m "Submitted to <journal>"
git push origin --tags
```

Append a `Tagged submission-…` line to `quality_reports/research_journal.md`.

## `pr`

Dispatch the agent in PR mode with `git diff master...HEAD --stat` and the latest session log; it drafts title + body (summary, what changed, quality scores, verification). Hand the draft to `/commit`, which creates the PR.

---

## Output

```
🛡 GIT STEWARD — [subcommand]
Branch master · ↑0 ↓0 · 3 uncommitted · 1 worktree
Verdict: FIX FIRST
1. [critical] pgpass line (WRDS) — staged diff:14 → move to ~/.pgpass, git restore --staged code/pull.py
2. [high] Data file under data/ — data/raw/crsp.parquet → move to ${DROPBOX_ROOT}, /data-registry add
3. [info] remote is http:// → git remote set-url origin https://github.com/...
Report: quality_reports/git_audit_2026-09-19.md
```

---

## Principles

- **Rotate, don't just delete.** A secret that touched a commit is compromised.
- **Worktrees for parallel work, branches for sequential work, `master` for nothing in progress.**
- **Data is never a git problem** — it is a registry problem (`data-management.md`).
- **The hook is the seatbelt; the steward is the mechanic.**

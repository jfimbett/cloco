# Git Hygiene

**The repository must always be safe to make public and easy to work on in parallel.**

## What never enters git

| Category | Examples | Where it goes instead |
|----------|----------|-----------------------|
| Credentials | `.env`, `~/.pgpass`, API keys, tokens, private keys, `settings.local.json`, `.claude/state/` | `.env` / `~/.pgpass` (gitignored); `.env.example` documents the keys |
| Data | `data/raw/*`, `data/processed/*`, `*.parquet`, `*.dta`, `*.rds`, extracts, zips | `${DROPBOX_ROOT}` + `data/registry.json` (`data-management.md`) |
| Large binaries | anything ≥ 20 MB; GitHub rejects ≥ 100 MB | Dropbox; Git LFS only for versioned paper PDFs/figures if truly needed |
| Build artefacts | `.aux`, `.log`, `.synctex.gz`, `__pycache__`, `paper/**/*.pdf` | gitignored |

Enforcement: the `secrets-guard` hook blocks `git commit` / `git push` (and `git add` of credential files) when the staged or unpushed content matches; `git_tools.py secrets --history N` finds what already slipped in. **A secret that touched a commit is compromised — rotate it; deleting the line is not a fix.**

## Branching model

- `master` holds only reviewed, compiling, score ≥ 80 work. Never accumulate a large dirty tree on it.
- One branch per task: `rr-<journal>-r<n>`, `talk-<venue>`, `robustness-<topic>`, `exp-<idea>`, `fix-<thing>`.
- `/commit` = branch → commit → PR → merge. Direct commits to `master` are for tiny fixes only.

## Worktrees for parallel work

Use a worktree (`python3 .claude/scripts/git_tools.py worktree new NAME`, or `EnterWorktree` inside Claude Code) when two streams run at once and touch overlapping files — a referee response alongside new analysis, a talk alongside paper edits, a long `/data-analysis` run while you keep writing. Worktrees live in `../<repo>-wt/<name>`; `.env` is linked so `data_path()` resolves; `data/raw` scratch is not shared — read from Dropbox via the registry. Remove a worktree only when its branch is merged or explicitly abandoned and it has no uncommitted work.

## Commits and PRs

- Message: imperative title ≤ 72 chars, body says *why*, ends with the attribution line the session provides.
- Do not mix `paper/` prose changes with unrelated `code/` changes in one commit when avoidable.
- PR body: summary · what changed · quality scores (from the research journal) · verification performed.
- Tag submissions: `submission-<journal>-<YYYY-MM-DD>`, pushed with `--tags`, logged in the research journal.

## Session habits

- Session start: the welcome banner shows branch / ahead-behind / dirty count; a dirty `master` is a prompt to branch.
- Before any push after touching credentials or data: `/git-steward audit`.
- Quarterly or before making the repo public: `/git-steward history-scan 500`.

## Never without explicit confirmation of that exact command

`push --force`, `filter-repo` / history rewrites, `reset --hard`, `branch -D`, `worktree remove --force`, deleting remote branches.

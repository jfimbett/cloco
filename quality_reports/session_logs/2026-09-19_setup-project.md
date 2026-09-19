# Session Log — 2026-09-19 — /setup-project

**Goal:** Stop projects from living inside the template identity (folder `cloco`, origin `cloco.git`) once a research spec exists; provide an assistant that checks tooling and sets up the project's own GitHub repository.

**Approach:** `project_setup.py` (status / doctor / slug / detach) + `identity-guard` hook (blocks pushes to the template when a spec exists) + `/setup-project` skill (asks repo name, GitHub create?, private/public, owner, folder rename) + identity surfaced in banner, status line, audit, git-steward.

**Decisions:** interactive flow as a skill; template kept as remote `template`; folder rename last with restart notice; private by default; doctor reports, never installs.

**Verification:** scratch clone with spec (needs-detach, refusal on dirty tree, dry-run, real detach with rename), hook deny/allow matrix, banner/status line/audit, real repo unaffected, python3 3.9 syntax + smoke runs.

**Open:** git identity unset on this machine (`git config --global user.name/email`); `.env` missing; first real `/setup-project` run happens when a spec exists.

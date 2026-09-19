---
name: setup-project
description: Project setup assistant. Checks the machine (git, gh, gh login, python3, latexmk, R, PDF tools, .env) and the project's identity — once a research spec exists the checkout must stop being the `cloco` template: folder `cloco-<slug>`, its own GitHub repository as origin (private or public, your choice), the template kept as a second remote for updates. Asks the questions, then does the work. Use at the start of any new project, when the welcome banner or status line shows "template identity", when a push is blocked by identity-guard, or on a new machine ("is everything installed?").
disable-model-invocation: true
argument-hint: "[doctor | identity | --repo cloco-NAME --private|--public [--owner ORG] [--rename-folder] | --yes]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write", "Edit", "AskUserQuestion"]
---

# Setup Project

The assistant that turns a fresh clone of the template into *this* paper's repository, and confirms the machine can run the pipeline.

**Input:** `$ARGUMENTS` — empty runs the full flow; `doctor` only checks the environment; `identity` only checks names and remotes; explicit flags (`--repo`, `--private`/`--public`, `--owner`, `--rename-folder`) skip the corresponding questions; `--yes` accepts every recommended default.

---

## Why this exists

`cloco` is a template. Every paper starts as a clone of it, and every clone therefore begins with the folder called `cloco` and `origin` pointing at `cloco.git`. If work continues like that, the first push writes the paper into the template and the template can no longer be pulled for the next project. The rule (see `git-hygiene.md`): **the moment a research spec exists, the checkout is a project** — folder `cloco-<slug>`, origin `…/cloco-<slug>.git`, template kept as remote `template`. The `identity-guard` hook blocks pushes to the template once a spec exists; this skill is how you get unblocked.

---

## Workflow

### Step 1: Environment doctor

```bash
python3 .claude/scripts/project_setup.py doctor
```

Report the table. For every ✗ (required) or ○ (optional) item, give the one-line fix the script printed. Offer to run fixes that are safe and local (`gh auth login` must be run by the user — suggest `! gh auth login`; `git config --global user.name/email` you may run once the user gives the values; `cp .env.example .env` then `/data-registry setup`). Do not install software without asking.

If `$ARGUMENTS` is `doctor`, stop here.

### Step 2: Identity check

```bash
python3 .claude/scripts/project_setup.py status
```

Three outcomes:

- **`no-spec`** — the template itself, or a project before `/interview-me`. Say so; nothing to detach yet. If the user is about to start a paper, tell them the identity step will be proposed right after the spec is written. Stop (unless flags were given).
- **`ok`** — folder and origin already belong to this project. Confirm and stop (unless `doctor` findings remain).
- **`needs-detach`** — continue.

If `$ARGUMENTS` is `identity`, stop after reporting.

### Step 3: The questions (one AskUserQuestion, up to four questions)

Skip any question already answered by flags or `--yes`.

1. **Repository name** — recommended: the `Suggested` name from the status output (`cloco-<slug>`, slug from the spec's `project_slug:` or derived from the project name). Options: recommended · shorter variant · "Other".
2. **Create it on GitHub now?** — Yes with `gh` (recommended when `gh auth` is ✓) · No, only detach the remote (I'll create the repo later) .
3. **Visibility** — Private (recommended for a working paper) · Public.
4. **Owner** — your `gh` account (default) · an organisation (ask for the name) — and **rename the folder now?** (Yes, and I'll restart the session · No, I'll rename it later). Renaming while the session runs leaves this session's working directory stale, so a restart is needed either way; say so.

Write the chosen slug back into the spec if it lacks a `project_slug:` line (Edit, directly under `project_type:`).

### Step 4: Detach

Requires a clean tree — if `git status` shows changes, offer `/commit` first (or a quick `git add … && git commit` of the spec) and stop until it is clean.

```bash
python3 .claude/scripts/project_setup.py detach --repo <name> --visibility <private|public> [--owner ORG] [--no-github] [--rename-folder]
```

Run with `--dry-run` first, show the commands, then run for real after the user has confirmed **in this conversation**. The script: renames `origin` → `template`; runs `gh repo create <owner>/<name> --<visibility> --source . --remote origin --push`; renames the folder last if asked.

Never run `git push --force`, never delete the template remote, never use `--no-verify` here.

### Step 5: Personalise the template files

After a successful detach:

1. `CLAUDE.md` header: replace `[Your Project Name]` with the project name from the spec; leave Institution/Authors for the user if still placeholders (ask once).
2. `README.md`: if it still opens with the template's description, add a two-line project banner at the top (title, one-sentence question, "built on the cloco template") — do not delete the template documentation; it is the manual.
3. `.claude/rules/domain-profile.md`: if still placeholders and a spec exists, suggest `/interview-me` filled it — otherwise offer to fill it now from the spec.

Commit these on the new origin: `git add CLAUDE.md README.md quality_reports/research_spec_*.md && git commit -m "Personalise template for <project>"` then `git push`.

### Step 6: Report

```
🧭 SETUP PROJECT — <project name>
Environment: git ✓ · gh ✓ (jfimbett) · python 3.9 ✓ · latexmk ✓ · R ✓ · PDF ✓ · .env ○
Identity:    folder cloco → cloco-<slug> (renamed / rename pending)
             origin  cloco.git → github.com/<owner>/cloco-<slug>.git (private)
             template kept as remote `template`  — update with: git fetch template && git merge template/master
Pushed:      <n> commits
Next:        cd ../cloco-<slug> && claude     (if the folder was renamed)
             /discovery                       (pipeline continues where it was)
```

---

## Pulling template improvements later

`git fetch template && git merge template/master`. Conflicts appear only in files both sides edit (`CLAUDE.md`, `README.md`, `.claude/rules/domain-profile.md`): keep the project's version of the header and profile, take the template's version of skills, agents, hooks and scripts. `/git-steward` can walk through it.

## Principles

- **Ask, then act.** Every state change (remote rename, repo creation, folder rename, config edit) follows an explicit answer in this conversation. Flags and `--yes` count as answers.
- **Keep the template reachable.** The template remote is renamed, never removed.
- **Private by default.** A working paper's repository is private unless the user says otherwise.
- **The doctor never installs.** It reports and gives the command; the user installs.

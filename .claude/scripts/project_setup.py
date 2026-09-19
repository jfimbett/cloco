#!/usr/bin/env python3
"""
Project setup — project identity and environment checks for the /setup-project
assistant, the identity-guard hook, the welcome banner and the status line.

The repository `cloco` is a TEMPLATE. Once a research spec exists the checkout
is a real project and must stop looking like the template: the folder should be
`cloco-<slug>` and `origin` should be `…/cloco-<slug>.git`, with the template
kept as a second remote (`template`) so improvements can still be pulled.

Usage:
    python3 .claude/scripts/project_setup.py status  [--json]   # identity: folder, remotes, spec, verdict
    python3 .claude/scripts/project_setup.py doctor  [--json]   # git, gh, gh auth, python, latexmk, R, pdf tools, .env
    python3 .claude/scripts/project_setup.py slug "Project name" # propose cloco-<slug>
    python3 .claude/scripts/project_setup.py detach --repo cloco-<slug> [--visibility private|public]
            [--owner USER_OR_ORG] [--no-github] [--rename-folder] [--dry-run]

`detach` (state-changing; the skill asks the user first):
    1. renames the template `origin` to `template` (kept, so `git fetch template` works)
    2. creates the GitHub repository with `gh repo create … --source . --remote origin --push`
       (skipped with --no-github: prints the commands to run by hand)
    3. with --rename-folder, renames the checkout folder to the repo name LAST and
       prints the `cd` + restart instructions (the running session keeps a stale cwd)

Exit codes: status → 0 ok / 1 needs detach; doctor → 0 all required ok / 1 something
required is missing; detach → 0 ok / 1 refused / 2 error. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
TEMPLATE_NAMES = {n.strip().lower() for n in os.environ.get("CLOCO_TEMPLATE_NAMES", "cloco").split(",") if n.strip()}
STOPWORDS = {"the", "a", "an", "of", "and", "or", "in", "on", "for", "to", "from", "with", "by", "at", "evidence",
             "effect", "effects", "impact", "role", "does", "do", "how", "why", "what", "when", "using", "based", "via"}
PYTHON_MIN = (3, 9)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def run(*args: str, cwd: Path | None = None, timeout: int = 60) -> tuple[int, str, str]:
    try:
        r = subprocess.run(list(args), cwd=str(cwd or PROJECT_ROOT), capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", str(exc)


def git(*args: str, cwd: Path | None = None) -> str:
    code, out, _ = run("git", *args, cwd=cwd)
    return out if code == 0 else ""


def repo_name_from_url(url: str) -> str:
    """https://github.com/o/cloco.git | git@github.com:o/cloco.git | /path/cloco → 'cloco'."""
    url = url.strip().rstrip("/")
    if not url:
        return ""
    tail = re.split(r"[/:]", url)[-1]
    return re.sub(r"\.git$", "", tail)


def owner_from_url(url: str) -> str:
    m = re.search(r"[/:]([^/:]+)/([^/]+?)(?:\.git)?/?$", url.strip())
    return m.group(1) if m else ""


def slugify(name: str, max_words: int = 3) -> str:
    words = [w for w in re.findall(r"[A-Za-z0-9]+", name.lower()) if w not in STOPWORDS]
    words = [w for w in words if len(w) > 1][:max_words] or re.findall(r"[a-z0-9]+", name.lower())[:max_words]
    return "-".join(words)[:40].strip("-") or "paper"


def read_spec(root: Path) -> dict | None:
    specs = sorted(root.glob("quality_reports/research_spec_*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not specs:
        return None
    text = specs[0].read_text(encoding="utf-8", errors="replace")
    info = {"spec_file": str(specs[0].relative_to(root)), "project_name": None, "project_slug": None}
    for line in text.splitlines():
        low = line.lower()
        m = re.search(r":\s*(.+)", line)
        if not m:
            continue
        val = m.group(1).strip().strip("*`").strip()
        if "project_slug" in low or "project slug" in low:
            info["project_slug"] = slugify(val, max_words=6) if val and "[" not in val else None
        elif ("project_name" in low or "project name" in low) and not info["project_name"]:
            info["project_name"] = val
    if not info["project_name"]:
        m = re.search(r"^#\s*Research Specification:\s*(.+)$", text, re.M)
        info["project_name"] = m.group(1).strip() if m else specs[0].stem.replace("research_spec_", "").replace("_", " ")
    return info


# --------------------------------------------------------------------------- #
# identity
# --------------------------------------------------------------------------- #
def identity(root: Path | None = None) -> dict:
    root = root or PROJECT_ROOT
    folder = root.name
    remotes: dict[str, str] = {}
    for line in git("remote", "-v", cwd=root).splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] not in remotes:
            remotes[parts[0]] = parts[1]
    origin = remotes.get("origin", "")
    origin_name = repo_name_from_url(origin)
    template_remote = next((n for n, u in remotes.items() if repo_name_from_url(u).lower() in TEMPLATE_NAMES), None)
    spec = read_spec(root)
    slug = (spec or {}).get("project_slug") or (slugify(spec["project_name"]) if spec and spec.get("project_name") else None)
    base = sorted(TEMPLATE_NAMES)[0] if TEMPLATE_NAMES else "cloco"
    suggested = f"{base}-{slug}" if slug else None
    folder_is_template = folder.lower() in TEMPLATE_NAMES
    remote_is_template = origin_name.lower() in TEMPLATE_NAMES
    has_spec = spec is not None
    problems = []
    if has_spec and folder_is_template:
        problems.append(f"folder is named '{folder}' (the template) — should be '{suggested or base + '-<slug>'}'")
    if has_spec and remote_is_template:
        problems.append(f"origin is the template repository ({origin}) — pushes would pollute the template")
    if has_spec and not origin:
        problems.append("no origin remote — the project has no GitHub home yet")
    return {
        "root": str(root), "folder": folder, "remotes": remotes, "origin": origin, "origin_repo": origin_name,
        "origin_owner": owner_from_url(origin), "template_remote": template_remote,
        "is_template_checkout": folder_is_template and remote_is_template and not has_spec,
        "has_spec": has_spec, "spec_file": (spec or {}).get("spec_file"),
        "project_name": (spec or {}).get("project_name"), "project_slug": slug, "suggested_repo": suggested,
        "folder_is_template": folder_is_template, "remote_is_template": remote_is_template,
        "needs_detach": bool(problems), "problems": problems,
        "verdict": "no-spec" if not has_spec else ("needs-detach" if problems else "ok"),
    }


def print_identity(idn: dict) -> None:
    mark = {"ok": "✓", "needs-detach": "✗", "no-spec": "·"}[idn["verdict"]]
    print(f"{mark} Identity   {idn['verdict']}")
    print(f"  Folder     {idn['folder']}{'  (template name)' if idn['folder_is_template'] else ''}")
    print(f"  Origin     {idn['origin'] or '— none'}{'  (template repo)' if idn['remote_is_template'] else ''}")
    others = {k: v for k, v in idn["remotes"].items() if k != "origin"}
    if others:
        print("  Remotes    " + ", ".join(f"{k} → {v}" for k, v in others.items()))
    if idn["has_spec"]:
        print(f"  Spec       {idn['spec_file']} — {idn['project_name']}")
        print(f"  Suggested  {idn['suggested_repo']}")
    else:
        print("  Spec       none — this is the template (or a project before /interview-me)")
    for p in idn["problems"]:
        print(f"  ✗ {p}")
    if idn["needs_detach"]:
        print("  → /setup-project  (renames the template remote, creates cloco-<slug> on GitHub, renames the folder)")


# --------------------------------------------------------------------------- #
# doctor
# --------------------------------------------------------------------------- #
def _version(cmd: list[str]) -> str:
    code, out, err = run(*cmd, timeout=20)
    return (out or err).splitlines()[0][:60] if (out or err) else ""


def doctor(root: Path | None = None) -> list[dict]:
    root = root or PROJECT_ROOT
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str, fix: str, required: bool = True) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail, "fix": fix, "required": required})

    py_ok = sys.version_info >= PYTHON_MIN
    add("python3", py_ok, f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "hooks need python3 ≥ 3.9 (brew install python)")
    g = shutil.which("git")
    add("git", bool(g), _version(["git", "--version"]) if g else "not on PATH", "brew install git  (or xcode-select --install)")
    if g:
        name, email = git("config", "user.name"), git("config", "user.email")
        add("git identity", bool(name and email), f"{name} <{email}>" if name and email else "user.name / user.email unset",
            'git config --global user.name "…" && git config --global user.email "…"')
        add("git repository", bool(git("rev-parse", "--is-inside-work-tree", cwd=root)), str(root), "git init")
    gh = shutil.which("gh")
    add("gh (GitHub CLI)", bool(gh), _version(["gh", "--version"]) if gh else "not on PATH", "brew install gh", required=False)
    if gh:
        code, out, err = run("gh", "auth", "status", timeout=30)
        acct = re.search(r"account (\S+)", out + err)
        add("gh auth", code == 0, f"logged in as {acct.group(1)}" if acct else (out or err).splitlines()[0][:70] if (out or err) else "",
            "gh auth login", required=False)
    else:
        add("gh auth", False, "gh not installed", "brew install gh && gh auth login", required=False)
    lm = shutil.which("latexmk")
    add("latexmk", bool(lm), _version(["latexmk", "--version"]) if lm else "not on PATH",
        "install TeX Live / MacTeX (brew install --cask mactex-no-gui)", required=False)
    rs = shutil.which("Rscript")
    add("Rscript", bool(rs), _version(["Rscript", "--version"]) if rs else "not on PATH", "brew install --cask r", required=False)
    pdf_ok = bool(shutil.which("pdftotext"))
    if not pdf_ok:
        try:
            import pypdf  # type: ignore  # noqa: F401
            pdf_ok, pdf_detail = True, "pypdf"
        except Exception:
            pdf_detail = "neither pdftotext nor pypdf"
    else:
        pdf_detail = "pdftotext"
    add("PDF text tool", pdf_ok, pdf_detail, "brew install poppler  (or pip install pypdf) — needed by /revive", required=False)
    env = root / ".env"
    add(".env", env.exists(), "present" if env.exists() else "missing", "cp .env.example .env, then /data-registry setup", required=False)
    if env.exists():
        txt = env.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^DROPBOX_ROOT\s*=\s*(.+)$", txt, re.M)
        val = os.path.expanduser(m.group(1).strip().strip('"').strip("'")) if m else ""
        add("DROPBOX_ROOT", bool(val) and Path(val).is_dir(), val or "unset", "set DROPBOX_ROOT in .env (/data-registry setup)", required=False)
    return checks


def print_doctor(checks: list[dict]) -> None:
    for c in checks:
        mark = "✓" if c["ok"] else ("✗" if c["required"] else "○")
        line = f"{mark} {c['name']:<16} {c['detail']}"
        if not c["ok"]:
            line += f"   → {c['fix']}"
        print(line)
    missing_req = [c["name"] for c in checks if c["required"] and not c["ok"]]
    missing_opt = [c["name"] for c in checks if not c["required"] and not c["ok"]]
    print(f"\nrequired missing: {', '.join(missing_req) or 'none'} · optional missing: {', '.join(missing_opt) or 'none'}")


# --------------------------------------------------------------------------- #
# detach
# --------------------------------------------------------------------------- #
def detach(repo: str, visibility: str, owner: str | None, use_github: bool, rename_folder: bool, dry_run: bool,
           root: Path | None = None) -> int:
    root = root or PROJECT_ROOT
    idn = identity(root)
    repo = re.sub(r"[^A-Za-z0-9._-]+", "-", repo).strip("-")
    if not repo or repo.lower() in TEMPLATE_NAMES:
        print(f"refusing: '{repo}' is the template name; use {sorted(TEMPLATE_NAMES)[0]}-<slug>", file=sys.stderr)
        return 1
    if visibility not in ("private", "public"):
        print("refusing: --visibility must be private or public", file=sys.stderr)
        return 1
    if git("status", "--porcelain", cwd=root):
        print("refusing: uncommitted changes — commit or stash first so the first push is clean", file=sys.stderr)
        return 1
    steps: list[list[str]] = []

    # 1. keep the template as a remote named `template`
    if idn["remote_is_template"]:
        if "template" in idn["remotes"]:
            steps.append(["git", "remote", "remove", "origin"])
        else:
            steps.append(["git", "remote", "rename", "origin", "template"])
    elif idn["origin"] and repo_name_from_url(idn["origin"]) != repo:
        print(f"note: origin already points to {idn['origin']} (not the template); leaving it and adding nothing", file=sys.stderr)

    # 2. GitHub repository
    full = f"{owner}/{repo}" if owner else repo
    gh_cmd = ["gh", "repo", "create", full, f"--{visibility}", "--source", ".", "--remote", "origin", "--push",
              "--description", f"Research project derived from the cloco template ({repo})"]
    if use_github:
        if not shutil.which("gh"):
            print("gh is not installed — run these by hand after `brew install gh && gh auth login`:", file=sys.stderr)
            use_github = False
        else:
            code, _, err = run("gh", "auth", "status", timeout=30)
            if code != 0:
                print(f"gh is not authenticated ({err.splitlines()[0] if err else 'gh auth status failed'}) — run `gh auth login` first", file=sys.stderr)
                use_github = False
    if use_github and not (idn["origin"] and not idn["remote_is_template"]):
        steps.append(gh_cmd)

    # print / run
    for s in steps:
        print("$ " + " ".join(s))
        if dry_run:
            continue
        code, out, err = run(*s, cwd=root, timeout=300)
        if out:
            print(out)
        if code != 0:
            print(err or f"command failed with exit {code}", file=sys.stderr)
            return 2
    if not use_github and not dry_run:
        print("\nManual GitHub step (when ready):")
        print("  " + " ".join(gh_cmd))
        print("  # or create the repo in the browser, then: git remote add origin <url> && git push -u origin master")

    # 3. folder rename — last, because the running session's cwd goes stale
    if rename_folder and root.name != repo:
        target = root.parent / repo
        if target.exists():
            print(f"cannot rename folder: {target} already exists", file=sys.stderr)
            return 2
        print(f"$ mv {root} {target}")
        if not dry_run:
            try:
                os.rename(root, target)
            except OSError as exc:
                print(f"folder rename failed: {exc}", file=sys.stderr)
                return 2
        print(f"\nFolder renamed. Restart your session from the new location:\n  cd {target} && claude")
    elif root.name.lower() in TEMPLATE_NAMES:
        print(f"\nFolder still named '{root.name}'. Rename it when you are done with this session:\n"
              f"  mv {root} {root.parent / repo} && cd {root.parent / repo} && claude")
    if not dry_run:
        print("\nTemplate updates later:  git fetch template && git merge template/master   (resolve conflicts in CLAUDE.md/README by keeping yours)")
    return 0


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("doctor"); s.add_argument("--json", action="store_true")
    s = sub.add_parser("slug"); s.add_argument("name", nargs="+")
    s = sub.add_parser("detach")
    s.add_argument("--repo", required=True, help="new repository / folder name, e.g. cloco-branch-closures")
    s.add_argument("--visibility", default="private", choices=("private", "public"))
    s.add_argument("--owner", help="GitHub user or organisation (default: your gh account)")
    s.add_argument("--no-github", action="store_true", help="only rename the template remote; print the gh command")
    s.add_argument("--rename-folder", action="store_true", help="rename the checkout folder to --repo (last step)")
    s.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.cmd == "status":
        idn = identity()
        print(json.dumps(idn, indent=2) if a.json else "", end="")
        if not a.json:
            print_identity(idn)
        return 1 if idn["needs_detach"] else 0
    if a.cmd == "doctor":
        checks = doctor()
        if a.json:
            print(json.dumps(checks, indent=2))
        else:
            print_doctor(checks)
        return 1 if any(c["required"] and not c["ok"] for c in checks) else 0
    if a.cmd == "slug":
        base = sorted(TEMPLATE_NAMES)[0] if TEMPLATE_NAMES else "cloco"
        print(f"{base}-{slugify(' '.join(a.name))}")
        return 0
    if a.cmd == "detach":
        return detach(a.repo, a.visibility, a.owner, not a.no_github, a.rename_folder, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

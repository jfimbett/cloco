#!/usr/bin/env python3
"""Lean 4 proof verification for the theory lane.

The Lean project lives in `lean/` (library `Cloco`, Lean + Mathlib pinned in lean-toolchain / lakefile.toml).
`lean/ledger.json` maps every formal result in the paper (LaTeX label) to the Lean declarations that prove it.
A result counts as VERIFIED only if every declaration compiles and `#print axioms` shows nothing beyond
the three standard axioms (propext, Classical.choice, Quot.sound) — so `sorry`, `admit`, and custom
`axiom`s are caught even when they hide in a helper lemma.

    python3 .claude/scripts/lean_tools.py doctor [--json]       # elan / lean / lake / Mathlib cache
    python3 .claude/scripts/lean_tools.py setup                 # install elan if missing, toolchain, Mathlib cache, build
    python3 .claude/scripts/lean_tools.py new Topic.Name        # scaffold lean/Cloco/Topic/Name.lean + import it
    python3 .claude/scripts/lean_tools.py verify [--json] [--no-report]
                                                                # build, audit axioms, update ledger + report
    python3 .claude/scripts/lean_tools.py ledger                # print the ledger (no build)

Exit code of `verify`: 0 when the build succeeds and every ledger entry is `verified` or `not_formalized`
(with a reason); 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
LEAN_DIR = PROJECT_ROOT / "lean"
LIB = "Cloco"
LEDGER = LEAN_DIR / "ledger.json"
REPORT = PROJECT_ROOT / "quality_reports" / "lean_verification.md"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ELAN_INIT = "https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
PATH_HINT = 'export PATH="$HOME/.elan/bin:$PATH"   # add to ~/.zshrc or ~/.bashrc'

# Soundness escape hatches that a source scan should surface even before the axiom audit.
SUSPICIOUS = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "axiom": r"^\s*(?:private\s+|protected\s+)?axiom\s",
    "native_decide": r"\bnative_decide\b",
    "implemented_by": r"implemented_by",
    "extern": r"@\[\s*extern",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def find_bin(name: str) -> str | None:
    hit = shutil.which(name)
    if hit:
        return hit
    cand = Path.home() / ".elan" / "bin" / name
    return str(cand) if cand.exists() else None


def env_with_elan() -> dict:
    env = dict(os.environ)
    elan_bin = str(Path.home() / ".elan" / "bin")
    if elan_bin not in env.get("PATH", "").split(os.pathsep):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    return env


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 3600, stream: bool = False) -> tuple[int, str]:
    try:
        if stream:
            p = subprocess.run(cmd, cwd=cwd, env=env_with_elan(), timeout=timeout)
            return p.returncode, ""
        p = subprocess.run(cmd, cwd=cwd, env=env_with_elan(), timeout=timeout,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return p.returncode, p.stdout
    except FileNotFoundError as e:
        return 127, str(e)
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s: {' '.join(cmd)}"


def first_line(s: str) -> str:
    return s.strip().splitlines()[0][:70] if s.strip() else ""


def toolchain() -> str:
    f = LEAN_DIR / "lean-toolchain"
    return f.read_text().strip() if f.exists() else ""


def load_ledger() -> dict:
    if not LEDGER.exists():
        return {"results": []}
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save_ledger(ledger: dict) -> None:
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def lean_files() -> list[Path]:
    root = LEAN_DIR / LIB
    return sorted(p for p in root.rglob("*.lean")) if root.exists() else []


def module_of(path: Path) -> str:
    return ".".join(path.relative_to(LEAN_DIR).with_suffix("").parts)


def strip_comments(src: str) -> str:
    src = re.sub(r"/-.*?-/", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    return re.sub(r"--[^\n]*", "", src)


def declarations(path: Path) -> list[str]:
    """Fully qualified theorem/lemma names, tracking `namespace … end` blocks (good enough for our style)."""
    names, stack = [], []
    for line in strip_comments(path.read_text(encoding="utf-8")).splitlines():
        m = re.match(r"\s*namespace\s+(\S+)", line)
        if m:
            stack.append(m.group(1))
            continue
        m = re.match(r"\s*end\s+(\S+)", line)
        if m and stack and stack[-1] == m.group(1):
            stack.pop()
            continue
        m = re.match(r"\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+)?(?:theorem|lemma)\s+([^\s:({\[]+)", line)
        if m:
            name = m.group(1)
            names.append(name if name.startswith("_root_.") else ".".join(stack + [name]))
    return [n.replace("_root_.", "") for n in names]


# --------------------------------------------------------------------------- #
# doctor
# --------------------------------------------------------------------------- #
def doctor() -> list[dict]:
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str, fix: str, required: bool = False) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail, "fix": fix, "required": required})

    elan = find_bin("elan")
    add("elan", bool(elan), first_line(run([elan, "--version"], timeout=30)[1]) if elan else "not installed",
        "python3 .claude/scripts/lean_tools.py setup")
    if elan and not shutil.which("elan"):
        add("elan on PATH", False, "~/.elan/bin not on PATH (scripts still find it)", PATH_HINT)
    want = toolchain()
    tc_dir = Path.home() / ".elan" / "toolchains" / want.replace("/", "--").replace(":", "---")
    add("Lean toolchain", bool(want) and tc_dir.exists(), want or "lean/lean-toolchain missing",
        "python3 .claude/scripts/lean_tools.py setup")
    lake = find_bin("lake")
    add("lake", bool(lake), "found" if lake else "not installed", "python3 .claude/scripts/lean_tools.py setup")
    ml = LEAN_DIR / ".lake" / "packages" / "mathlib" / ".lake" / "build" / "lib" / "lean" / "Mathlib.olean"
    add("Mathlib cache", ml.exists(), "built oleans present" if ml.exists() else "not downloaded",
        "python3 .claude/scripts/lean_tools.py setup  (≈5 GB, prebuilt cache)")
    return checks


def print_checks(checks: list[dict]) -> None:
    for c in checks:
        mark = "✓" if c["ok"] else ("✗" if c["required"] else "○")
        print(f"{mark} {c['name']:<16} {c['detail']}" + ("" if c["ok"] else f"   → {c['fix']}"))


# --------------------------------------------------------------------------- #
# setup
# --------------------------------------------------------------------------- #
def setup() -> int:
    if not find_bin("elan"):
        if not shutil.which("curl"):
            print("✗ curl not found — install elan manually: https://lean-lang.org/install/")
            return 1
        print("→ installing elan (Lean version manager) into ~/.elan …")
        code, _ = run(["sh", "-c", f"curl -sSfL {ELAN_INIT} | sh -s -- -y --default-toolchain none"], stream=True)
        if code != 0 or not find_bin("elan"):
            print("✗ elan install failed — see https://lean-lang.org/install/")
            return 1
    want = toolchain()
    print(f"→ toolchain {want}")
    if run([find_bin("elan"), "toolchain", "install", want], stream=True)[0] != 0:
        return 1
    lake = find_bin("lake")
    print("→ fetching Mathlib and its prebuilt cache (first time ≈5 GB; later runs are instant)")
    if run([lake, "exe", "cache", "get"], cwd=LEAN_DIR, stream=True)[0] != 0:
        print("✗ `lake exe cache get` failed — retry; on persistent failure run `lake update` in lean/ first")
        return 1
    print(f"→ building {LIB}")
    if run([lake, "build"], cwd=LEAN_DIR, stream=True)[0] != 0:
        print("✗ build failed — the environment is installed; fix the Lean errors above")
        return 1
    print(f"✓ Lean ready. {'' if shutil.which('lean') else 'For a shell: ' + PATH_HINT}")
    return 0


# --------------------------------------------------------------------------- #
# new
# --------------------------------------------------------------------------- #
TEMPLATE = """/-
{title}

Paper results formalised here (one Lean declaration per paper label; record each in lean/ledger.json):
  - <label>: <one-line statement as in the paper>

Fidelity notes: say where the Lean statement is a special case or uses stronger hypotheses than the paper.
-/
import Mathlib

namespace {ns}

-- Primitives (mirror the paper's notation; document every hypothesis).

-- theorem <name> (hyps) : <claim> := by
--   …

end {ns}
"""


def new_module(name: str) -> int:
    parts = [p for p in name.replace("/", ".").split(".") if p]
    if parts and parts[0] == LIB:
        parts = parts[1:]
    if not parts or not all(re.fullmatch(r"[A-Z][A-Za-z0-9_]*", p) for p in parts):
        print("✗ module name must be UpperCamelCase segments, e.g. Contracting.MoralHazard")
        return 1
    path = LEAN_DIR / LIB / Path(*parts).with_suffix(".lean")
    mod = ".".join([LIB] + parts)
    if path.exists():
        print(f"○ {path.relative_to(PROJECT_ROOT)} already exists")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(TEMPLATE.format(title=" ".join(parts), ns=mod), encoding="utf-8")
        print(f"✓ created {path.relative_to(PROJECT_ROOT)}")
    root = LEAN_DIR / f"{LIB}.lean"
    txt = root.read_text(encoding="utf-8") if root.exists() else ""
    if f"import {mod}\n" not in txt + "\n":
        root.write_text(txt.rstrip("\n") + f"\nimport {mod}\n", encoding="utf-8")
        print(f"✓ added `import {mod}` to lean/{LIB}.lean")
    return 0


# --------------------------------------------------------------------------- #
# verify
# --------------------------------------------------------------------------- #
DIAG = re.compile(r"^(error|warning|info): (\S+\.lean):(\d+):(\d+): (.*)$")
BOUNDARY = re.compile(r"^(error|warning|info|trace):|^[✖⚠✔] \[|^Some required targets|^- |^Build completed")


def parse_build(out: str) -> list[dict]:
    diags: list[dict] = []
    cur: dict | None = None
    for line in out.splitlines():
        m = DIAG.match(line)
        if m:
            cur = {"severity": m.group(1), "file": m.group(2), "line": int(m.group(3)), "col": int(m.group(4)),
                   "message": m.group(5)}
            diags.append(cur)
        elif BOUNDARY.match(line):
            cur = None
        elif cur is not None and len(cur["message"]) < 600:
            cur["message"] += "\n" + line
    return diags


AXIOM_LINE = re.compile(r"^'([^']+)' (?:depends on axioms: \[(.*)\]|does not depend on any axioms)")


def audit_axioms(names: list[str], modules: list[str], lake: str) -> dict[str, dict]:
    """`#print axioms` for each name, importing only modules that built (one broken file must not hide the rest)."""
    if not names or not modules:
        return {}
    work = LEAN_DIR / ".lake" / "cloco-verify"
    work.mkdir(parents=True, exist_ok=True)
    probe = work / "Axioms.lean"
    probe.write_text("".join(f"import {m}\n" for m in modules) + "".join(f"#print axioms {n}\n" for n in names), encoding="utf-8")
    _, out = run([lake, "env", "lean", str(probe)], cwd=LEAN_DIR, timeout=1800)
    res: dict[str, dict] = {n: {"status": "missing", "axioms": []} for n in names}
    for line in out.splitlines():
        m = AXIOM_LINE.match(line)
        if not m:
            continue
        ax = [a.strip() for a in (m.group(2) or "").split(",") if a.strip()]
        extra = [a for a in ax if a not in STANDARD_AXIOMS]
        status = "partial" if "sorryAx" in ax else ("unsound" if extra else "verified")
        res[m.group(1)] = {"status": status, "axioms": ax}
    return res


def combine(statuses: list[str]) -> str:
    for s in ("failed", "missing", "unsound", "partial"):
        if s in statuses:
            return s
    return "verified" if statuses else "stated"


def verify(as_json: bool, write_report: bool) -> int:
    lake = find_bin("lake")
    if not lake or not (LEAN_DIR / "lakefile.toml").exists():
        print("✗ Lean not set up — python3 .claude/scripts/lean_tools.py setup")
        return 1
    code, out = run([lake, "build"], cwd=LEAN_DIR)
    diags = parse_build(out)
    errors = [d for d in diags if d["severity"] == "error"]
    bad_files = {d["file"] for d in errors}

    files = lean_files()
    scan: dict[str, dict] = {}
    for f in files:
        src = strip_comments(f.read_text(encoding="utf-8"))
        hits = {k: len(re.findall(p, src, flags=re.M)) for k, p in SUSPICIOUS.items()}
        scan[str(f.relative_to(LEAN_DIR))] = {k: v for k, v in hits.items() if v}

    decl_file: dict[str, str] = {}
    for f in files:
        for n in declarations(f):
            decl_file[n] = str(f.relative_to(LEAN_DIR))
    ledger = load_ledger()
    wanted = sorted(set(decl_file) | {d for r in ledger["results"] for d in r.get("decls", [])})
    ok_decls = [n for n in wanted if decl_file.get(n) not in bad_files]
    good_modules = [module_of(f) for f in files if str(f.relative_to(LEAN_DIR)) not in bad_files]
    axioms = audit_axioms(ok_decls, good_modules, lake)
    for n in wanted:
        if decl_file.get(n) in bad_files:
            axioms[n] = {"status": "failed", "axioms": []}

    for r in ledger["results"]:
        decls = r.get("decls") or []
        if not decls:
            r["status"] = "not_formalized" if r.get("reason") else "stated"
        else:
            r["status"] = combine([axioms.get(d, {"status": "missing"})["status"] for d in decls])
    ledger["last_verified"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    ledger["toolchain"] = toolchain()
    save_ledger(ledger)

    results = ledger["results"]
    n = len(results)
    n_ver = sum(r["status"] == "verified" for r in results)
    n_nf = sum(r["status"] == "not_formalized" for r in results)
    blocking = [r for r in results if r["status"] not in ("verified", "not_formalized")]
    summary = {
        "build_ok": code == 0, "errors": errors, "source_flags": {k: v for k, v in scan.items() if v},
        "declarations": axioms, "ledger": results,
        "coverage": {"results": n, "verified": n_ver, "not_formalized": n_nf,
                     "verified_share": round(n_ver / n, 3) if n else None},
        "pass": code == 0 and not blocking,
    }
    if write_report:
        write_md(summary)
    if as_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print_summary(summary)
    return 0 if summary["pass"] else 1


MARK = {"verified": "✓", "partial": "◐", "stated": "○", "not_formalized": "–",
        "failed": "✗", "missing": "✗", "unsound": "✗"}


def print_summary(s: dict) -> None:
    print(f"{'✓' if s['build_ok'] else '✗'} lake build {'ok' if s['build_ok'] else 'FAILED'}")
    for e in s["errors"][:15]:
        print(f"   {e['file']}:{e['line']}:{e['col']}: {e['message'].splitlines()[0]}")
    for f, flags in s["source_flags"].items():
        print(f"⚠ {f}: " + ", ".join(f"{k}×{v}" for k, v in flags.items()))
    ledgered = {d for r in s["ledger"] for d in r.get("decls", [])}
    for name, a in sorted(s["declarations"].items()):
        if a["status"] != "verified" or name in ledgered:
            print(f"{MARK[a['status']]} {a['status']:<9} {name}" +
                  (f"  [{', '.join(x for x in a['axioms'] if x not in STANDARD_AXIOMS)}]" if a["status"] in ("partial", "unsound") else ""))
    print_ledger(s["ledger"])
    c = s["coverage"]
    if c["results"]:
        print(f"\ncoverage: {c['verified']}/{c['results']} paper results verified"
              f" · {c['not_formalized']} not formalised (with reason)")
    print("PASS" if s["pass"] else "NOT PASSING — see statuses above")


def print_ledger(results: list[dict]) -> None:
    if not results:
        print("ledger: empty (add paper results to lean/ledger.json)")
        return
    print("\nledger:")
    for r in results:
        st = r.get("status", "stated")
        print(f"  {MARK.get(st, '?')} {st:<14} {r.get('label', '?'):<28} {r.get('fidelity', ''):<13} "
              f"{', '.join(r.get('decls') or []) or r.get('reason', '')}")


def write_md(s: dict) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    c = s["coverage"]
    lines = [
        "# Lean Verification Report",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Toolchain:** {toolchain()}  ",
        f"**Build:** {'PASS' if s['build_ok'] else 'FAIL'}  ",
        f"**Coverage:** {c['verified']}/{c['results']} paper results machine-verified; {c['not_formalized']} not formalised  ",
        f"**Overall:** {'PASS' if s['pass'] else 'NOT PASSING'}",
        "",
        "Generated by `python3 .claude/scripts/lean_tools.py verify`. VERIFIED = compiles and depends only on "
        "propext / Classical.choice / Quot.sound. Statement fidelity (does the Lean statement say what the paper "
        "says?) is judged by theory-critic, not by this script.",
        "",
        "## Paper results",
        "| Label | Status | Fidelity | Lean declarations / reason |",
        "|---|---|---|---|",
    ]
    for r in s["ledger"]:
        lines.append(f"| `{r.get('label', '')}` | {r.get('status', '')} | {r.get('fidelity', '')} | "
                     f"{', '.join('`%s`' % d for d in r.get('decls') or []) or r.get('reason', '')} |")
    if s["errors"]:
        lines += ["", "## Build errors"] + [f"- `{e['file']}:{e['line']}` {e['message'].splitlines()[0]}" for e in s["errors"]]
    if s["source_flags"]:
        lines += ["", "## Source flags"] + [f"- `{f}`: " + ", ".join(f"{k}×{v}" for k, v in fl.items())
                                            for f, fl in s["source_flags"].items()]
    lines += ["", "## All declarations", "| Declaration | Status | Axioms |", "|---|---|---|"]
    for n, a in sorted(s["declarations"].items()):
        lines.append(f"| `{n}` | {a['status']} | {', '.join(a['axioms']) or '—'} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("doctor")
    d.add_argument("--json", action="store_true")
    sub.add_parser("setup")
    n = sub.add_parser("new")
    n.add_argument("module")
    v = sub.add_parser("verify")
    v.add_argument("--json", action="store_true")
    v.add_argument("--no-report", action="store_true")
    sub.add_parser("ledger")
    a = ap.parse_args()
    if a.cmd == "doctor":
        checks = doctor()
        print(json.dumps(checks, indent=2)) if a.json else print_checks(checks)
        return 0 if all(c["ok"] for c in checks) else 1
    if a.cmd == "setup":
        return setup()
    if a.cmd == "new":
        return new_module(a.module)
    if a.cmd == "verify":
        return verify(a.json, not a.no_report)
    if a.cmd == "ledger":
        led = load_ledger()
        print_ledger(led["results"])
        if led.get("last_verified"):
            print(f"\nlast verified {led['last_verified']} ({led.get('toolchain', '')})")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

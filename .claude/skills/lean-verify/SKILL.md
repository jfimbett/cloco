---
name: lean-verify
description: Machine-check the paper's formal results in Lean 4 + Mathlib. Sets up Lean if missing, builds lean/, audits axioms (catches sorry and custom axioms), updates lean/ledger.json, and dispatches theory-critic to judge statement fidelity. Use when asked to "verify the proofs", "check the theory in Lean", "formalise proposition X", or before a theory-paper submission.
argument-hint: "[setup | status | <label or Lean module to formalise> | (empty = verify all)]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Lean Verify

Machine-check the project's theory in `lean/` (library `Cloco`, Lean and Mathlib pinned in `lean/lean-toolchain` and `lean/lakefile.toml`).

**Input:** `$ARGUMENTS`

## Step 1: Environment

Run `python3 .claude/scripts/lean_tools.py doctor`.
- Anything other than PATH missing → `python3 .claude/scripts/lean_tools.py setup` (installs elan, the toolchain, Mathlib's prebuilt cache, then builds). First install ≈5 GB and a few minutes; say so before starting. Run it in the background when possible.
- `$ARGUMENTS` = `setup` → stop after this step.

## Step 2: Route

| `$ARGUMENTS` | Action |
|---|---|
| empty / `all` | Step 3 only |
| `status` | `python3 .claude/scripts/lean_tools.py ledger` and stop |
| a LaTeX label (`prop:…`) or module name | Dispatch `econ-finance-theorist` (or `structural-estimation-expert` for structural-model lemmas) with: the LaTeX statement and proof (grep `paper/` and `quality_reports/theory_model_*.md` for the label), the instruction to follow its "Machine-Checked Proofs in Lean 4" protocol, and to record the result in `lean/ledger.json`. Then Step 3. |

## Step 3: Verify

`python3 .claude/scripts/lean_tools.py verify` — builds, runs `#print axioms` on every theorem, updates ledger statuses, writes `quality_reports/lean_verification.md`. Statuses: `verified` · `partial` (sorry in dependency cone) · `failed` (build error) · `missing` (no such declaration) · `unsound` (custom axiom) · `stated` (in ledger, no Lean yet) · `not_formalized` (with reason).

Also check that every `\label{prop:|lem:|thm:|cor:…}` in `paper/` appears in the ledger:
`grep -rhoE '\\label\{(prop|lem|thm|cor|claim):[^}]+\}' paper/ | sort -u`.

## Step 4: Critic

Dispatch `theory-critic` with: "Run Phase 5 (Machine Verification) on lean/ledger.json against [paper/sections/theory.tex or the model file]. Focus on statement fidelity." The script cannot tell whether a verified Lean statement *is* the paper's statement; the critic can.

## Step 5: Report

```
Lean: [verified]/[total] results verified · build PASS/FAIL
Blocking: [label — status]          (partial/failed/missing/unsound/stated)
Fidelity flags: [label — critic finding]
Not formalised: [label — reason]
Report: quality_reports/lean_verification.md · theory-critic score XX/100
```

## Principles

- **A green build is not a verified paper.** Only `#print axioms` showing nothing beyond propext / Classical.choice / Quot.sound counts, and only for a statement that matches the paper.
- **Honest fidelity beats coverage.** A special case labelled `special-case` is worth more than a general claim that quietly assumes more.
- **Pinned toolchain.** Upgrade Lean and Mathlib together, deliberately, on their own branch: bump both, `cd lean && lake update`, re-verify.

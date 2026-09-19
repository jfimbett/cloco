#!/usr/bin/env python3
"""
Automated dataset profiler for the /data-profile skill and the explorer's
Inventory mode.

Usage:
    python3 .claude/scripts/profile_data.py <file> [--quick] [--out DIR]
                                            [--id COL] [--time COL] [--treat COL]

Reads csv / tsv / parquet / dta / xlsx / json (pandas when available; a pure-
Python CSV fallback otherwise) and writes:

    <out>/<stem>_profile.md   human-readable profile
    <out>/<stem>_codebook.csv machine-readable codebook

--quick prints a compact JSON summary to stdout and writes nothing.
Default --out is quality_reports/data/profiles/.

The script never modifies the input file.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

try:  # optional dependency
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None

MAX_ROWS_FALLBACK = 200_000
ID_HINTS = re.compile(r"(^|_)(id|key|code|gvkey|permno|cusip|isin|siren|fips|nuts|cik|ticker)($|_)", re.I)
TIME_HINTS = re.compile(r"(^|_)(year|yr|date|month|quarter|qtr|week|period|time|fyear|datadate)($|_)", re.I)
TREAT_HINTS = re.compile(r"(^|_)(treat|treated|post|policy|adopt|exposure|dose|shock|event|reform)($|_)", re.I)


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_frame(path: Path):
    """Return (pandas.DataFrame | None, list[dict] | None)."""
    suffix = path.suffix.lower()
    if pd is not None:
        try:
            if suffix in (".csv", ".txt"):
                return pd.read_csv(path, low_memory=False), None
            if suffix == ".tsv":
                return pd.read_csv(path, sep="\t", low_memory=False), None
            if suffix == ".parquet":
                return pd.read_parquet(path), None
            if suffix == ".dta":
                return pd.read_stata(path, convert_categoricals=False), None
            if suffix in (".xlsx", ".xls"):
                return pd.read_excel(path), None
            if suffix == ".json":
                return pd.read_json(path), None
            if suffix in (".rds", ".rdata"):
                sys.stderr.write("R binary files: export to csv/parquet first (e.g. arrow::write_parquet).\n")
                return None, None
        except Exception as exc:  # fall through to csv fallback
            sys.stderr.write(f"pandas failed ({exc}); trying csv fallback\n")
    if suffix in (".csv", ".txt", ".tsv"):
        delim = "\t" if suffix == ".tsv" else ","
        rows: list[dict] = []
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh, delimiter=delim)
            for i, row in enumerate(reader):
                if i >= MAX_ROWS_FALLBACK:
                    break
                rows.append(row)
        return None, rows
    sys.stderr.write(f"Cannot read {path.name}: install pandas (and pyarrow for parquet) or convert to csv.\n")
    return None, None


# --------------------------------------------------------------------------- #
# Column profiling
# --------------------------------------------------------------------------- #
def _try_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def profile_columns_pandas(df) -> list[dict]:
    out = []
    n = len(df)
    for col in df.columns:
        s = df[col]
        nonnull = int(s.notna().sum())
        entry = {
            "column": str(col),
            "dtype": str(s.dtype),
            "n_nonnull": nonnull,
            "pct_missing": round(100 * (1 - nonnull / n), 2) if n else 0.0,
            "n_unique": int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            desc = s.describe()
            entry.update(
                {
                    "mean": _fmt(desc.get("mean")),
                    "sd": _fmt(desc.get("std")),
                    "min": _fmt(desc.get("min")),
                    "p50": _fmt(desc.get("50%")),
                    "max": _fmt(desc.get("max")),
                    "n_zero": int((s == 0).sum()),
                    "n_negative": int((s < 0).sum()),
                }
            )
        else:
            top = s.dropna().astype(str).value_counts().head(5)
            entry["top_values"] = "; ".join(f"{k} ({v})" for k, v in top.items())
        entry["role_guess"] = guess_role(entry)
        out.append(entry)
    return out


def profile_columns_rows(rows: list[dict]) -> list[dict]:
    if not rows:
        return []
    cols = list(rows[0].keys())
    n = len(rows)
    out = []
    for col in cols:
        vals = [r.get(col) for r in rows]
        nonnull_vals = [v for v in vals if v not in (None, "", "NA", "NaN", ".", "nan")]
        nums = [f for f in (_try_float(v) for v in nonnull_vals) if f is not None and not math.isnan(f)]
        entry = {
            "column": col,
            "dtype": "numeric" if nonnull_vals and len(nums) == len(nonnull_vals) else "string",
            "n_nonnull": len(nonnull_vals),
            "pct_missing": round(100 * (1 - len(nonnull_vals) / n), 2) if n else 0.0,
            "n_unique": len(set(nonnull_vals)),
        }
        if entry["dtype"] == "numeric" and nums:
            nums_sorted = sorted(nums)
            mean = sum(nums) / len(nums)
            sd = math.sqrt(sum((x - mean) ** 2 for x in nums) / max(len(nums) - 1, 1))
            entry.update(
                {
                    "mean": _fmt(mean),
                    "sd": _fmt(sd),
                    "min": _fmt(nums_sorted[0]),
                    "p50": _fmt(nums_sorted[len(nums_sorted) // 2]),
                    "max": _fmt(nums_sorted[-1]),
                    "n_zero": sum(1 for x in nums if x == 0),
                    "n_negative": sum(1 for x in nums if x < 0),
                }
            )
        else:
            top = Counter(nonnull_vals).most_common(5)
            entry["top_values"] = "; ".join(f"{k} ({v})" for k, v in top)
        entry["role_guess"] = guess_role(entry)
        out.append(entry)
    return out


def _fmt(x):
    if x is None:
        return None
    try:
        if isinstance(x, float) and math.isnan(x):
            return None
        return round(float(x), 4)
    except (TypeError, ValueError):
        return None


def guess_role(entry: dict) -> str:
    name = entry["column"]
    if TIME_HINTS.search(name):
        return "time"
    if ID_HINTS.search(name):
        return "id"
    if TREAT_HINTS.search(name):
        return "treatment?"
    if entry.get("n_unique") == 2 and entry.get("dtype") not in ("string",):
        return "binary"
    if entry.get("n_unique", 0) > 0 and entry["n_unique"] == entry["n_nonnull"] and entry["n_nonnull"] > 50:
        return "id?"
    return ""


# --------------------------------------------------------------------------- #
# Structure detection
# --------------------------------------------------------------------------- #
def detect_structure(df, rows, cols: list[dict], id_col: str | None, time_col: str | None, treat_col: str | None) -> dict:
    info: dict = {"id_col": id_col, "time_col": time_col, "treat_col": treat_col}
    names = [c["column"] for c in cols]

    if id_col is None:
        cands = [c["column"] for c in cols if c["role_guess"] in ("id", "id?")]
        id_col = cands[0] if cands else None
    if time_col is None:
        cands = [c["column"] for c in cols if c["role_guess"] == "time"]
        time_col = cands[0] if cands else None
    if treat_col is None:
        cands = [c["column"] for c in cols if c["role_guess"] in ("treatment?", "binary")]
        treat_col = cands[0] if cands else None
    info.update({"id_col": id_col, "time_col": time_col, "treat_col": treat_col})

    def col_values(name):
        if df is not None:
            return df[name]
        return [r.get(name) for r in rows]

    if id_col in names and time_col in names:
        if df is not None:
            n_units = int(df[id_col].nunique())
            n_periods = int(df[time_col].nunique())
            per_unit = df.groupby(id_col)[time_col].nunique()
            dup = int(df.duplicated(subset=[id_col, time_col]).sum())
            balanced = bool((per_unit == n_periods).all())
            tmin, tmax = df[time_col].min(), df[time_col].max()
        else:
            pairs = [(r.get(id_col), r.get(time_col)) for r in rows]
            n_units = len({p[0] for p in pairs})
            n_periods = len({p[1] for p in pairs})
            per_unit = Counter(p[0] for p in set(pairs))
            dup = len(pairs) - len(set(pairs))
            balanced = all(v == n_periods for v in per_unit.values())
            times = sorted({p[1] for p in pairs if p[1] not in (None, "")})
            tmin, tmax = (times[0], times[-1]) if times else (None, None)
        info["panel"] = {
            "n_units": n_units,
            "n_periods": n_periods,
            "balanced": balanced,
            "duplicate_unit_time_rows": dup,
            "time_range": [str(tmin), str(tmax)],
        }
    else:
        info["panel"] = None

    if treat_col in names:
        vals = col_values(treat_col)
        if df is not None:
            vc = df[treat_col].value_counts(dropna=True).head(6)
            dist = {str(k): int(v) for k, v in vc.items()}
            treated_units = None
            first_treat = None
            if id_col in names and time_col in names:
                try:
                    tr = df[df[treat_col].astype(float) > 0]
                    treated_units = int(tr[id_col].nunique())
                    first = tr.groupby(id_col)[time_col].min()
                    first_treat = {str(k): int(v) for k, v in first.value_counts().sort_index().head(12).items()}
                except Exception:
                    pass
        else:
            dist = dict(Counter(str(v) for v in vals if v not in (None, "")).most_common(6))
            treated_units, first_treat = None, None
            if id_col in names and time_col in names:
                first: dict = {}
                for r in rows:
                    tv = _try_float(r.get(treat_col))
                    if tv is not None and tv > 0:
                        u, t = r.get(id_col), _try_float(r.get(time_col))
                        if t is not None and (u not in first or t < first[u]):
                            first[u] = t
                treated_units = len(first)
                cohorts = Counter(int(t) for t in first.values())
                first_treat = {str(k): v for k, v in sorted(cohorts.items())[:12]}
        info["treatment"] = {
            "value_distribution": dist,
            "treated_units": treated_units,
            "first_treatment_period_counts": first_treat,
            "staggered": (len(first_treat) > 1) if first_treat else None,
        }
    else:
        info["treatment"] = None
    return info


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def flags(cols: list[dict], structure: dict, n_rows: int) -> list[str]:
    out = []
    for c in cols:
        if c["pct_missing"] >= 30:
            out.append(f"`{c['column']}` is {c['pct_missing']}% missing")
        if c.get("n_unique") == 1:
            out.append(f"`{c['column']}` is constant")
    p = structure.get("panel")
    if p:
        if p["duplicate_unit_time_rows"]:
            out.append(f"{p['duplicate_unit_time_rows']} duplicate unit×time rows — panel key is not unique")
        if not p["balanced"]:
            out.append("panel is unbalanced — check attrition/entry before fixed-effects estimation")
    else:
        out.append("no (id, time) pair detected — pass --id/--time if this is a panel")
    t = structure.get("treatment")
    if t and t.get("treated_units") == 0:
        out.append("treatment column has no treated units")
    if t and t.get("staggered"):
        out.append("staggered treatment timing detected — TWFE is biased under heterogeneous effects; plan CS/SA/stacked estimators")
    if n_rows < 200:
        out.append(f"only {n_rows} rows — statistical power is a concern")
    return out


def write_outputs(path: Path, out_dir: Path, n_rows: int, cols: list[dict], structure: dict) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    md = out_dir / f"{stem}_profile.md"
    cb = out_dir / f"{stem}_codebook.csv"

    lines = [
        f"# Data Profile — `{path.name}`",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Source:** `{path}`",
        f"**Rows:** {n_rows:,}   **Columns:** {len(cols)}",
        "",
        "## Structure",
    ]
    p = structure.get("panel")
    if p:
        lines += [
            f"- Panel key: `{structure['id_col']}` × `{structure['time_col']}`",
            f"- Units: {p['n_units']:,}   Periods: {p['n_periods']}   Range: {p['time_range'][0]} → {p['time_range'][1]}",
            f"- Balanced: {p['balanced']}   Duplicate unit×time rows: {p['duplicate_unit_time_rows']}",
        ]
    else:
        lines.append("- No panel key detected (cross-section, or pass `--id`/`--time`).")
    t = structure.get("treatment")
    if t:
        lines += [f"- Treatment column: `{structure['treat_col']}` — distribution {t['value_distribution']}"]
        if t.get("treated_units") is not None:
            lines.append(f"- Treated units: {t['treated_units']}   Staggered: {t['staggered']}")
        if t.get("first_treatment_period_counts"):
            lines.append(f"- First-treatment cohorts: {t['first_treatment_period_counts']}")
    lines += ["", "## Flags"]
    fl = flags(cols, structure, n_rows)
    lines += [f"- {f}" for f in fl] or ["- none"]
    lines += ["", "## Variables", "", "| Column | Type | Missing % | Unique | Mean | SD | Min | Median | Max | Role | Top values |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in cols:
        lines.append(
            f"| `{c['column']}` | {c['dtype']} | {c['pct_missing']} | {c['n_unique']} | "
            f"{c.get('mean', '')} | {c.get('sd', '')} | {c.get('min', '')} | {c.get('p50', '')} | {c.get('max', '')} | "
            f"{c.get('role_guess', '')} | {c.get('top_values', '')} |"
        )
    lines += [
        "",
        "## Next Steps",
        "- Fill the `label`, `source`, and `construction` columns in the codebook CSV.",
        "- Hand this profile to `data-quality-surveyor` (measurement validity) and `causal-strategist` (design fit).",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")

    fields = ["column", "dtype", "pct_missing", "n_unique", "mean", "sd", "min", "p50", "max", "role_guess", "top_values", "label", "source", "construction"]
    with cb.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for c in cols:
            w.writerow({**{k: "" for k in fields}, **c})
    return md, cb


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--quick", action="store_true", help="print JSON summary only")
    ap.add_argument("--out", default="quality_reports/data/profiles")
    ap.add_argument("--id", dest="id_col")
    ap.add_argument("--time", dest="time_col")
    ap.add_argument("--treat", dest="treat_col")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.stderr.write(f"not found: {path}\n")
        return 1

    df, rows = load_frame(path)
    if df is None and rows is None:
        return 1
    n_rows = len(df) if df is not None else len(rows)
    cols = profile_columns_pandas(df) if df is not None else profile_columns_rows(rows)
    structure = detect_structure(df, rows, cols, args.id_col, args.time_col, args.treat_col)

    if args.quick:
        summary = {
            "file": str(path),
            "rows": n_rows,
            "columns": [c["column"] for c in cols],
            "structure": structure,
            "flags": flags(cols, structure, n_rows),
            "backend": "pandas" if df is not None else "csv-fallback",
        }
        print(json.dumps(summary, indent=2, default=str))
        return 0

    md, cb = write_outputs(path, Path(args.out), n_rows, cols, structure)
    print(f"profile:  {md}\ncodebook: {cb}\nbackend:  {'pandas' if df is not None else 'csv-fallback'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

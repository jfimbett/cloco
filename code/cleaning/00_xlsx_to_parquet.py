"""
Script  : 00_xlsx_to_parquet.py
Purpose : Convert raw Excel auction data files to Parquet format.
          This is the first step of the reproducible pipeline.
          The original Excel files are never modified.

Inputs  : (checked in order; first match wins)
          1.  data/raw/Bordeaux Auction Results (Complete).xlsx
          2.  old/in vino veritas/Auction data/Bordeaux Auction Results (Complete).xlsx
          (same logic for Burgundy and Rhone)

Outputs : data/intermediate/bordeaux_raw.parquet
          data/intermediate/burgundy_raw.parquet
          data/intermediate/rhone_raw.parquet

Usage   : Run from project root
          python code/cleaning/00_xlsx_to_parquet.py

Notes   :
  - The xlsx -> parquet conversion was not scripted by any RA; this script
    closes that reproducibility gap.
  - Reading large Excel files is slow (~2-5 min per file on the first run).
  - Parquet files are written with snappy compression by default.
  - If the canonical data/raw/ location does not yet have the Excel files,
    the script reads from old/ and prints a reminder to migrate.
"""

from pathlib import Path
import pandas as pd
import sys

# ---------------------------------------------------------------------------
# Path configuration — all relative to project root
# ---------------------------------------------------------------------------

# Project root is two levels above this file: code/cleaning/ -> code/ -> root
ROOT = Path(__file__).resolve().parent.parent.parent

RAW_DIR = ROOT / "data" / "raw"
INTERMEDIATE_DIR = ROOT / "data" / "intermediate"
FALLBACK_DIR = ROOT / "old" / "in vino veritas" / "Auction data"

INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

# Map each region to its source filename and output parquet name
FILES = {
    "bordeaux": {
        "xlsx": "Bordeaux Auction Results (Complete).xlsx",
        "out":  "bordeaux_raw.parquet",
    },
    "burgundy": {
        "xlsx": "Burgundy Auction Results (Complete).xlsx",
        "out":  "burgundy_raw.parquet",
    },
    "rhone": {
        "xlsx": "Rhone Auction Results (Complete).xlsx",
        "out":  "rhone_raw.parquet",
    },
}


def find_xlsx(filename: str) -> Path:
    """
    Return the path to `filename`, checking data/raw/ first then the
    old/in vino veritas/ fallback. Raises FileNotFoundError if absent.
    """
    canonical = RAW_DIR / filename
    if canonical.exists():
        return canonical

    fallback = FALLBACK_DIR / filename
    if fallback.exists():
        print(
            f"  [NOTE] Reading from fallback location:\n"
            f"         {fallback}\n"
            f"         Copy to {canonical} when possible."
        )
        return fallback

    raise FileNotFoundError(
        f"Could not find '{filename}'.\n"
        f"  Checked: {canonical}\n"
        f"  Checked: {fallback}\n"
        f"Place the raw Excel file in data/raw/ before running this script."
    )


def convert_one(region: str, cfg: dict) -> None:
    """Read one Excel file and write it as parquet to data/intermediate/."""
    out_path = INTERMEDIATE_DIR / cfg["out"]

    if out_path.exists():
        print(f"  [SKIP] {out_path.name} already exists. Delete to re-run.")
        return

    print(f"\n[{region.upper()}] Locating source Excel file ...")
    xlsx_path = find_xlsx(cfg["xlsx"])

    print(f"  Reading {xlsx_path.name}  (this may take several minutes) ...")
    df = pd.read_excel(xlsx_path)

    print(f"  Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"  Columns: {df.columns.tolist()}")

    # Basic dtype check
    for col in df.columns:
        if df[col].dtype == "object":
            non_null = df[col].notna().sum()
            print(f"    {col}: object, {non_null:,} non-null")

    print(f"  Writing to {out_path} ...")
    df.to_parquet(out_path, index=False, compression="snappy")
    print(f"  Done. File size: {out_path.stat().st_size / 1e6:.1f} MB")


def main():
    print("=" * 60)
    print("Step 00: Excel -> Parquet conversion")
    print(f"Project root: {ROOT}")
    print("=" * 60)

    errors = []
    for region, cfg in FILES.items():
        try:
            convert_one(region, cfg)
        except FileNotFoundError as e:
            print(f"\n  [ERROR] {e}")
            errors.append(region)

    if errors:
        print(f"\n[WARNING] Could not convert: {errors}")
        print("Pipeline will continue using existing parquet files in old/.")
        sys.exit(1)
    else:
        print("\n[DONE] All three regions converted to parquet.")


if __name__ == "__main__":
    main()

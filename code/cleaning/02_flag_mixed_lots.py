"""
Script  : 02_flag_mixed_lots.py
Purpose : Identify mixed lots via text-mining of Description_Combi, then use
          consecutive Lot# logic to distinguish true mixed lots from
          mislabelled lots (which should be kept in the sample).

Input   : data/intermediate/clean_data.parquet
          (Falls back to old/RALucie/wine/parquet/clean_data.parquet)

Output  : data/processed/clean_data_final.parquet

Usage   : Run from project root
          python code/cleaning/02_flag_mixed_lots.py

Algorithm (faithful to Lucie's mixed_lots_finding.py):
  1.  Lowercase Description_Combi -> Description_Combi_lower
  2.  Text-mine for 8 mixed-lot keyword patterns:
        - 'lots'        (excluding 'lots of')
        - 'lot'         (>= 2 occurrences, excluding 'lot of', 'per lot')
        - 'mixed lots'
        - 'mixed importers'
        - 'small lots'
        - 'two lots'
        - 'following lots'
        - 'sized lots'
  3.  Merge indicators into Mixed_Lots column (non-null = flagged)
  4.  Compute Excluded_Lots:
        - Flagged as mixed lot AND no consecutive Lot# neighbour
        - These are true mixed lots and should be dropped from price analysis
  5.  Drop intermediary columns; save to processed/

Definition of 'excluded':
  Mixed_Lots = non-null   ->  lot text matched; may or may not be excluded
  Excluded_Lots = 1       ->  mixed lot WITH no consecutive Lot# (drop these)
  Mixed_Lots = non-null AND Excluded_Lots = NaN  ->  keep (consecutive lots)
"""

from pathlib import Path
import sys
import re

import pandas as pd
import numpy as np

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    NLTK_OK = True
except ImportError:
    NLTK_OK = False
    print("[WARN] nltk not installed; 'lot' (>=2 occurrences) pattern skipped.")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT           = Path(__file__).resolve().parent.parent.parent
INTERMEDIATE   = ROOT / "data" / "intermediate"
PROCESSED      = ROOT / "data" / "processed"
FALLBACK_DIR   = ROOT / "old" / "RALucie" / "wine" / "parquet"
INPUT_PATH     = INTERMEDIATE / "clean_data.parquet"
FALLBACK_INPUT = FALLBACK_DIR / "clean_data.parquet"
OUTPUT_PATH    = PROCESSED / "clean_data_final.parquet"

PROCESSED.mkdir(parents=True, exist_ok=True)

MISSING_MARKERS = ["0NA", "nan", "NaN", "n/a", " ", ""]


# ---------------------------------------------------------------------------
# Text-mining helper functions
# ---------------------------------------------------------------------------

def find_lots_keyword(series: pd.Series) -> pd.Series:
    """Find 'lots' but NOT 'lots of'."""
    return (
        series.str.findall(r"\blots(?! of)\b")
        .apply(lambda x: " ".join(x) if isinstance(x, list) and x else np.nan)
    )


def find_lot_twice(text: str):
    """
    Return 'lot, lot' if the word 'lot' appears >= 2 times in `text`,
    excluding 'lot of', 'per lot', 'bottlesper lot', 'par lot'.
    """
    if not NLTK_OK or pd.isna(text):
        return np.nan
    sentences = sent_tokenize(str(text))
    lot_count = 0
    for sentence in sentences:
        words = word_tokenize(sentence)
        i = 0
        while i < len(words):
            if words[i] == "lot":
                if i + 1 < len(words) and words[i + 1] == "of":
                    i += 2
                    continue
                if i - 1 >= 0 and words[i - 1] in ("per", "bottlesper", "par"):
                    i += 1
                    continue
                lot_count += 1
            i += 1
    return "lot, lot" if lot_count >= 2 else np.nan


def find_phrase(series: pd.Series, phrase: str) -> pd.Series:
    """Find an exact phrase in a text series (word-boundary match)."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return (
        series.str.findall(pattern)
        .apply(lambda x: " ".join(x) if isinstance(x, list) and x else np.nan)
    )


# ---------------------------------------------------------------------------
# Consecutive Lot# logic
# ---------------------------------------------------------------------------

def assign_consecutive_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a group number (Lot_Cons_Number) to runs of consecutive Lot#
    values.  Rows in a group of size 1 (i.e., no consecutive neighbour)
    get Lot_Cons_Number = NaN.
    """
    # Fill NaN temporarily so isnumeric() works
    df["Lot#"] = df["Lot#"].fillna("B")
    # Extract numeric Lot# values
    df["Lot#_numeric"] = pd.to_numeric(
        df[df["Lot#"].str.isnumeric()]["Lot#"], errors="coerce"
    )
    diff = df["Lot#_numeric"].diff()
    is_consecutive = diff == 1

    # Assign group IDs
    group_id = 1
    group_ids = []
    for consec in is_consecutive:
        if consec:
            group_ids.append(group_id)
        else:
            group_id += 1
            group_ids.append(group_id)
    df["Lot_Cons_Number"] = group_ids

    # Groups of size 1 -> NaN
    counts = df["Lot_Cons_Number"].value_counts()
    singles = counts[counts == 1].index
    df.loc[df["Lot_Cons_Number"].isin(singles), "Lot_Cons_Number"] = 0
    df.loc[df["Lot_Cons_Number"] == 0, "Lot_Cons_Number"] = np.nan

    # Restore Lot# NaN
    df["Lot#"] = df["Lot#"].replace("B", np.nan)

    return df


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def flag_mixed_lots(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full mixed-lot flagging pipeline."""

    # ------------------------------------------------------------------
    # 1. Prepare lowercase description
    # ------------------------------------------------------------------
    print("[1] Preparing lowercase description ...")
    df["Row#"] = df.index
    df["Description_Combi_lower"] = (
        df["Description_Combi"]
        .str.lower()
        .str.replace(":", "", regex=False)
        .fillna("")
    )
    # Replace remaining NaN representations
    df["Description_Combi_lower"] = df["Description_Combi_lower"].replace(
        MISSING_MARKERS, np.nan
    )
    # Keep as string for regex (NaN rows will return empty match)
    df["Description_Combi_lower"] = df["Description_Combi_lower"].fillna("")

    # ------------------------------------------------------------------
    # 2. Text-mine for mixed-lot keywords
    # ------------------------------------------------------------------
    print("[2] Text-mining for mixed-lot keywords ...")

    df["Identified_Lots"] = find_lots_keyword(df["Description_Combi_lower"])
    print(f"  'lots' keyword: {df['Identified_Lots'].notna().sum():,} matches")

    if NLTK_OK:
        df["Identified_Lot"] = df["Description_Combi_lower"].apply(find_lot_twice)
    else:
        df["Identified_Lot"] = np.nan
    print(f"  'lot' x2 keyword: {df['Identified_Lot'].notna().sum():,} matches")

    df["Identified_Mixed_Lots"] = find_phrase(
        df["Description_Combi_lower"], "mixed lots"
    )
    print(f"  'mixed lots': {df['Identified_Mixed_Lots'].notna().sum():,} matches")

    df["Identified_Mixed_Importers"] = find_phrase(
        df["Description_Combi_lower"], "mixed importers"
    )
    print(f"  'mixed importers': {df['Identified_Mixed_Importers'].notna().sum():,} matches")

    df["Identified_Small_Lots"] = find_phrase(
        df["Description_Combi_lower"], "small lots"
    )
    print(f"  'small lots': {df['Identified_Small_Lots'].notna().sum():,} matches")

    df["Identified_Two_Lots"] = find_phrase(
        df["Description_Combi_lower"], "two lots"
    )
    print(f"  'two lots': {df['Identified_Two_Lots'].notna().sum():,} matches")

    df["Identified_Following_Lots"] = find_phrase(
        df["Description_Combi_lower"], "following lots"
    )
    print(f"  'following lots': {df['Identified_Following_Lots'].notna().sum():,} matches")

    df["Identified_Sized_Lots"] = find_phrase(
        df["Description_Combi_lower"], "sized lots"
    )
    print(f"  'sized lots': {df['Identified_Sized_Lots'].notna().sum():,} matches")

    # ------------------------------------------------------------------
    # 3. Merge keyword indicators into Mixed_Lots
    # ------------------------------------------------------------------
    print("[3] Merging keyword indicators into Mixed_Lots ...")
    keyword_cols = [
        "Identified_Lots",
        "Identified_Lot",
        "Identified_Mixed_Lots",
        "Identified_Mixed_Importers",
        "Identified_Small_Lots",
        "Identified_Two_Lots",
        "Identified_Following_Lots",
        "Identified_Sized_Lots",
    ]

    def _merge_row(row):
        vals = [str(v) for v in row if pd.notna(v)]
        return ", ".join(vals) if vals else np.nan

    df["Mixed_Lots"] = df[keyword_cols].apply(_merge_row, axis=1)
    df["Mixed_Lots"] = df["Mixed_Lots"].replace(MISSING_MARKERS, np.nan)
    print(f"  Mixed_Lots non-null: {df['Mixed_Lots'].notna().sum():,}")

    # ------------------------------------------------------------------
    # 4. Consecutive Lot# grouping for Excluded_Lots
    # ------------------------------------------------------------------
    print("[4] Computing consecutive Lot# groups ...")
    df = assign_consecutive_groups(df)

    # Excluded = flagged as mixed AND no consecutive Lot# neighbour
    df["Excluded_Lots"] = (
        df["Mixed_Lots"].notna() & df["Lot_Cons_Number"].isna()
    ).astype(int)
    # Replace 0 with NaN (only code 1 = excluded)
    df["Excluded_Lots"] = df["Excluded_Lots"].replace(0, np.nan)
    print(f"  Excluded_Lots non-null: {df['Excluded_Lots'].notna().sum():,}")

    # ------------------------------------------------------------------
    # 5. Final missing-value pass and drop intermediary columns
    # ------------------------------------------------------------------
    print("[5] Cleaning up intermediary columns ...")
    df = df.replace(["0", "0NA", "nan", "NaN", "n/a", " "], np.nan)

    drop_cols = [
        "Row#", "Description_Combi_lower",
        "Identified_Lots", "Identified_Lot",
        "Identified_Mixed_Lots", "Identified_Mixed_Importers",
        "Identified_Small_Lots", "Identified_Two_Lots",
        "Identified_Following_Lots", "Identified_Sized_Lots",
        "Lot#_numeric", "Lot_Cons_Number",
    ]
    present = [c for c in drop_cols if c in df.columns]
    df = df.drop(columns=present)

    print(f"  Final columns ({len(df.columns)}): {df.columns.tolist()}")
    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Step 02: Flag mixed lots")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 60)

    if OUTPUT_PATH.exists():
        print("[SKIP] clean_data_final.parquet already exists. Delete to re-run.")
        return

    # Load input
    if INPUT_PATH.exists():
        print(f"\nLoading {INPUT_PATH} ...")
        df = pd.read_parquet(INPUT_PATH)
    elif FALLBACK_INPUT.exists():
        print(
            f"\n[FALLBACK] {INPUT_PATH} not found; "
            f"using {FALLBACK_INPUT}\nRun 01_clean_auction_data.py first."
        )
        df = pd.read_parquet(FALLBACK_INPUT)
    else:
        raise FileNotFoundError(
            f"Input not found:\n  {INPUT_PATH}\n  {FALLBACK_INPUT}"
        )

    print(f"Input shape: {df.shape}")

    df = flag_mixed_lots(df)

    print(f"\nOutput shape: {df.shape}")
    df.to_parquet(OUTPUT_PATH, index=False, compression="snappy")
    print(f"\n[DONE] Written to {OUTPUT_PATH}")
    print(f"       File size: {OUTPUT_PATH.stat().st_size / 1e6:.1f} MB")

    # Summary
    n_mixed = df["Mixed_Lots"].notna().sum()
    n_excl  = df["Excluded_Lots"].notna().sum()
    n_keep  = n_mixed - n_excl
    print(f"\nMixed-lot summary:")
    print(f"  Total rows:            {len(df):,}")
    print(f"  Mixed-lot flagged:     {n_mixed:,} ({100*n_mixed/len(df):.2f}%)")
    print(f"  Excluded (drop these): {n_excl:,} ({100*n_excl/len(df):.2f}%)")
    print(f"  Mixed but kept:        {n_keep:,} (consecutive lots)")


if __name__ == "__main__":
    main()

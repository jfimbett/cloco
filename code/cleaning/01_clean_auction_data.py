"""
Script  : 01_clean_auction_data.py
Purpose : Clean and harmonise the raw auction parquet files produced by
          00_xlsx_to_parquet.py.  This is a clean, portable rewrite of
          Lucie Bourdychova's f1_data_cleaning_final.py.

Input   : data/intermediate/bordeaux_raw.parquet
          data/intermediate/burgundy_raw.parquet
          data/intermediate/rhone_raw.parquet
          (Falls back to old/RALucie/wine/parquet/*complete.parquet if
           intermediate/ files are absent — useful before running step 00.)

Output  : data/intermediate/clean_data.parquet

Usage   : Run from project root
          python code/cleaning/01_clean_auction_data.py

Key transformations (faithful to Lucie's pipeline):
  1.  Standardise missing-value placeholders ('0NA', 'nan', 'n/a', ' ')
  2.  Strip/lowercase selected text columns
  3.  Standardise location fields (country, city abbreviations)
  4.  Combine complementary column pairs into *_Combi columns
  5.  Compute Age = sale year - vintage year
  6.  Convert Size to litres (Size_liter)
  7.  Standardise wine ratings to 100-pt and 20-pt scales
  8.  Drop source columns once combined
  9.  Write clean_data.parquet

Open data questions from data_work.txt (NOT changed by this script):
  - Producer/wine name standardisation (still unstandardised)
  - P_Loc / P_$ conflict with Hammer_Loc_Combi / Hammer_$_Combi (see note §6)
  - Class column standardisation (proposed dict in data_work.txt Q3)
  - Date variable reliability (data_work.txt note §2b)
"""

from pathlib import Path
import pandas as pd
import numpy as np
import sys

# ---------------------------------------------------------------------------
# Utility import — add project root to sys.path so utils/ is importable
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "code" / "utils"))
from bottle_sizes import convert_to_liters  # noqa: E402

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------
INTERMEDIATE_DIR = ROOT / "data" / "intermediate"
FALLBACK_PARQUET  = ROOT / "old" / "RALucie" / "wine" / "parquet"
OUTPUT_PATH       = INTERMEDIATE_DIR / "clean_data.parquet"

INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

# Names used when loading from the old/ fallback
FALLBACK_SUFFIX = "Results complete.parquet"

# ---------------------------------------------------------------------------
# Missing-value placeholders to replace with np.nan everywhere
# ---------------------------------------------------------------------------
MISSING_MARKERS = ["0NA", "nan", "NaN", "n/a", " ", ""]


# ---------------------------------------------------------------------------
# Helper functions (preserved from Lucie's pipeline)
# ---------------------------------------------------------------------------

def standardise_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace known missing-value placeholders with np.nan."""
    return df.replace(["0NA", "nan", "NaN", "n/a", " "], np.nan)


def strip_whitespace(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Strip leading/trailing whitespace from object columns."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].str.strip()
    return df


def lower_and_strip(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Convert to lowercase and strip whitespace."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].str.lower().str.strip()
    return df


def combine_columns(
    df: pd.DataFrame, col1: str, col2: str, new_col: str, sep: str = "_"
) -> pd.DataFrame:
    """
    Merge two complementary columns into a single *_Combi column.

    Logic (preserved from Lucie):
      - Fill NaN with '' before concatenating to avoid 'nan' strings
      - Strip the separator from both ends
      - Replace empty/placeholder strings with np.nan
      - Log counts before/after

    Note: col1 and col2 are BOTH kept in the DataFrame here; they are
    dropped in the final cleanup step at the end of the pipeline.
    """
    c1_count = df[col1].count() if col1 in df.columns else 0
    c2_count = df[col2].count() if col2 in df.columns else 0

    c1 = df[col1].fillna("") if col1 in df.columns else pd.Series("", index=df.index)
    c2 = df[col2].fillna("") if col2 in df.columns else pd.Series("", index=df.index)

    combined = c1 + sep + c2
    combined = combined.str.replace(sep * 2, sep, regex=False)
    combined = combined.str.strip(sep)
    combined = combined.replace(MISSING_MARKERS, np.nan)

    df[new_col] = combined
    print(
        f"  combine {col1!r} + {col2!r} -> {new_col!r}: "
        f"{c1_count} + {c2_count} = {df[new_col].count()} non-null"
    )
    return df


# ---------------------------------------------------------------------------
# Rating standardisation functions (preserved from Lucie)
# ---------------------------------------------------------------------------

# Lists of 100-pt rating strings mapped to each category
_RATING_95_100 = {
    "95", "95-96", "95-97", "95-98", "(95-98)", "95-100", "95?", "95+?",
    "95(+?)", "95+", "96", "96+", "96-97", "96-98", "96-99", "96-100",
    "96(+?)", "97", "97+", "97(+?)", "97-98", "97-99", "97-100", "98",
    "98+", "98(+?)", "99", "99+", "99(+?)", "100",
}
_RATING_90_94 = {
    "(90-91)", "(90-93)", "(90-92)", "(90-94)", "90", "90+", "90+?",
    "90(+?)", "90?", "90-91", "90-92", "90-93", "91", "91?", "91+?",
    "(91-92)", "91-92", "(91-92+)", "91-93", "(91-93)", "91-94", "91+",
    "91(+?)", "92", "92-94", "(92-94)", "92-93", "92-95", "92+", "92(+?)",
    "92?", "92+?", "93", "93?", "93+?", "93-94", "(93-94)", "93+",
    "93(+?)", "(93-95)", "93-95", "94", "94+?", "94?", "94+", "94(?)",
    "94(+?)", "(94-97)", "(94-95+)", "94-97", "93-96", "(93-96)", "94-96",
    "94-95", "91-95",
}
_RATING_80_89 = {
    "80", "81", "82", "83", "84", "85", "85-88", "(85-88)", "86",
    "(86-88)", "(86-89)", "87", "87-89", "(87-89)", "88", "88?",
    "(88-89)", "89", "89+", "89(+?)", "(87-90)", "(89-92)", "89-91",
    "87-90", "88-91", "88-90", "89-92", "(88-90)", "89-90",
    "(89-91+?)", "(89-91)",
}
_RATING_70_79 = {"70", "74", "75", "76", "77", "78", "79"}
_RATING_60_69 = {"64", "65"}
_RATING_50_59 = {"50"}


def convert_to_scale100(points) -> str:
    """Map a raw 100-pt score string to a standardised range bucket."""
    pts = str(points).lower().replace(" ", "")
    if pts in _RATING_95_100:
        return "95-100"
    elif pts in _RATING_90_94:
        return "90-94"
    elif pts in _RATING_80_89:
        return "80-89"
    elif pts in _RATING_70_79:
        return "70-79"
    elif pts in _RATING_60_69:
        return "60-69"
    elif pts in _RATING_50_59:
        return "50-59"
    else:
        return np.nan


# 20-pt JR rating -> 100-pt bucket
_JR_95_100 = {"19", "19.5", "19-", "20", "19+", "20++", "19?"}
_JR_90_94  = {
    "18.5", "18.5+", "18", "18+", "18.5-", "18++", "18?",
    "18-", "18--", "18.5++", "18+++",
}
_JR_80_89  = {
    "17", "17.5+", "16.5", "17.5", "16", "17--", "17+", "17.5++",
    "17-", "17.5-", "16-", "16+", "16.5+", "17++", "17?", "17+++",
}


def convert_jr_to_100(points) -> str:
    """Map Jancis Robinson 20-pt score to standardised 100-pt bucket."""
    pts = str(points).lower().replace(" ", "")
    if pts in _JR_95_100:
        return "95-100"
    elif pts in _JR_90_94:
        return "90-94"
    elif pts in _JR_80_89:
        return "80-89"
    else:
        return np.nan


def convert_jr_to_20(points) -> str:
    """Standardise Jancis Robinson 20-pt score to integer-like string."""
    pts = str(points).lower().replace(" ", "")
    if pts in {"20", "20++"}:
        return "20"
    elif pts in {"19.5", "19", "19-", "19+", "19?"}:
        return "19"
    elif pts in {"18.5", "18.5+", "18.5-", "18.5++"}:
        return "18"
    elif pts in {"18", "18+", "18++", "18?", "18-", "18--", "18+++"}:
        return "18"
    elif pts in {"17.5+", "17.5", "17.5++", "17.5-"}:
        return "17"
    elif pts in {"17", "17--", "17+", "17-", "17++", "17?", "17+++"}:
        return "17"
    elif pts in {"16.5", "16.5+"}:
        return "16"
    elif pts in {"16", "16-", "16+"}:
        return "16"
    else:
        return np.nan


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_raw_parquets() -> pd.DataFrame:
    """
    Load the three regional raw parquets and concatenate.
    Tries data/intermediate/ first, falls back to old/RALucie/wine/parquet/.
    """
    region_map = {
        "bordeaux": "bordeaux_raw.parquet",
        "burgundy": "burgundy_raw.parquet",
        "rhone":    "rhone_raw.parquet",
    }
    fallback_map = {
        "bordeaux": "Bordeaux Auction Results complete.parquet",
        "burgundy": "Burgundy Auction Results complete.parquet",
        "rhone":    "Rhone Auction Results complete.parquet",
    }

    frames = []
    for region, fname in region_map.items():
        primary = INTERMEDIATE_DIR / fname
        if primary.exists():
            print(f"  Loading {primary.name} ...")
            frames.append(pd.read_parquet(primary))
        else:
            fallback = FALLBACK_PARQUET / fallback_map[region]
            if fallback.exists():
                print(
                    f"  [FALLBACK] {primary.name} not found; "
                    f"using {fallback} (run 00_xlsx_to_parquet.py to fix)"
                )
                frames.append(pd.read_parquet(fallback))
            else:
                raise FileNotFoundError(
                    f"Cannot find raw parquet for {region}.\n"
                    f"  Checked: {primary}\n"
                    f"  Checked: {fallback}\n"
                    "Run 00_xlsx_to_parquet.py first."
                )

    df = pd.concat(frames, ignore_index=True)
    print(f"  Concatenated shape: {df.shape}")
    return df


# ---------------------------------------------------------------------------
# Main cleaning pipeline
# ---------------------------------------------------------------------------

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the full cleaning pipeline and return the cleaned DataFrame."""

    # ------------------------------------------------------------------
    # 1. Standardise missing values
    # ------------------------------------------------------------------
    print("\n[1] Standardising missing values ...")
    df = df.replace(["0NA", "nan", "NaN", "n/a", " "], np.nan)

    # ------------------------------------------------------------------
    # 2. Strip whitespace from text columns
    # ------------------------------------------------------------------
    print("[2] Stripping whitespace ...")
    strip_cols = ["Lot Mark", "Lot_Mark", "AucHouse", "AH", "Old Vins", "Old Vine", "Old Tree"]
    df = strip_whitespace(df, strip_cols)

    # ------------------------------------------------------------------
    # 3. Lowercase selected columns
    # ------------------------------------------------------------------
    print("[3] Lowercasing type/region/variety columns ...")
    lower_cols = [
        "Ty", "Type", "Sub_Region", "Sub Region", "Sub Region Dummy",
        "Area", "Sub-Area", "Special", "Grapes", "Variety",
    ]
    df = lower_and_strip(df, lower_cols)

    # ------------------------------------------------------------------
    # 4. Standardise specific values
    # ------------------------------------------------------------------
    print("[4] Standardising location and classification values ...")

    # Auction house
    if "AH" in df.columns:
        df["AH"] = df["AH"].replace("HDH", "Hart Davis Hart")

    # Country
    if "Loc_Country" in df.columns:
        df["Loc_Country"] = (
            df["Loc_Country"]
            .replace("Britain", "UK")
            .replace("NL", "Netherlands")
            .replace("Netherland", "Netherlands")
            .replace("Swiss", "Switzerland")
        )

    # City abbreviations
    if "Loc_City" in df.columns:
        import re
        abbrevs = {
            r"\bLDN\b":            "London",
            r"\bNY\b":             "New York",
            r"\bLA\b":             "Los Angeles",
            r"\bHK\b":             "Hong Kong",
            r"\bOnline Auction\b": "Online",
        }
        for pattern, replacement in abbrevs.items():
            df["Loc_City"] = df["Loc_City"].str.replace(pattern, replacement, regex=True)

        df["Loc_City"] = df["Loc_City"].str.replace(
            "Wood Dale, Illinois U.S.A.", "Wood Dale", regex=False
        )
        df["Loc_City"] = df["Loc_City"].str.replace(
            "Niles, Illinois U.S.A.", "Niles", regex=False
        )
        df["Loc_City"] = df["Loc_City"].str.replace(
            "Ashurst, Kent", "Kent", regex=False
        )
        # Illinois rows with known city in Loc column
        if "Loc" in df.columns:
            replace_map = {
                "Niles, Illinois U.S.A.": "Niles",
                "Wood Dale, Illinois":    "Wood Dale",
            }
            mask = df["Loc_City"] == "Illinois"
            df.loc[mask, "Loc_City"] = df.loc[mask, "Loc"].map(replace_map).fillna(
                df.loc[mask, "Loc_City"]
            )

        # Split multi-city strings and keep first city only
        def _first_city(val):
            if pd.isna(val):
                return val
            if " and " in str(val) or ", " in str(val):
                parts = re.split(r",\s*| and ", str(val))
                return parts[0].strip()
            return str(val)

        df["Loc_City"] = df["Loc_City"].apply(_first_city)
        df["Loc_City"] = df["Loc_City"].replace(MISSING_MARKERS, np.nan)

    # Sub-region typos
    if "Sub Region Dummy" in df.columns:
        df["Sub Region Dummy"] = df["Sub Region Dummy"].str.replace(
            r"\bermitage\b", "hermitage", regex=True
        )
    if "Area" in df.columns:
        df["Area"] = df["Area"].str.replace(r"\bermitage\b", "hermitage", regex=True)
        df["Area"] = df["Area"].str.replace("-", " ", regex=False)
        df["Area"] = df["Area"].str.replace("volany", "volnay", regex=False)

    if "Sub-Area" in df.columns:
        df["Sub-Area"] = df["Sub-Area"].str.replace("-", " ", regex=False)

    # Special: normalise alternate spellings
    if "Special" in df.columns:
        df["Special"] = (
            df["Special"]
            .replace("special", "speciale")
            .replace("especial", "speciale")
            .replace("special reserve", "reserve speciale")
            .replace("speciale reserve", "reserve speciale")
        )

    # ------------------------------------------------------------------
    # 5. Combine complementary column pairs into *_Combi columns
    # ------------------------------------------------------------------
    print("[5] Combining complementary column pairs ...")

    # Each tuple: (col1, col2, new_name)
    combis = [
        ("Ty",            "Type",           "Type_Combi"),
        ("Lot Mark",      "Lot_Mark",       "Lot_Mark_Combi"),
        ("AucHouse",      "AH",             "Auc_House_Combi"),
        ("Sub_Region",    "Sub Region",     "Sub_Region_Combi"),
        ("Sub Region Dummy", "Sub_Region_Combi", "Sub_Region_Combi"),  # overwrite
        ("Old Vins",      "Old Vine",       "Old_Combi"),
        ("Old Tree",      "Old_Combi",      "Old_Combi"),
        ("Grapes",        "Variety",        "Grapes_Combi"),
        ("Hammer_Loc",    "Ham_Loc",        "Hammer_Loc_Combi"),
        ("Hammer_$",      "Ham_$",          "Hammer_$_Combi"),
        ("Esti_Loc_Low",  "Esti_Loc_L",     "Esti_Loc_Low_Combi"),
        ("Esti_$_Low",    "Esti_$_L",       "Esti_$_Low_Combi"),
        ("Esti_Loc_High", "Esti_Loc_H",     "Esti_Loc_High_Combi"),
        ("Esti_$_High",   "Esti_$_H",       "Esti_$_High_Combi"),
        ("Dec",           "Desc",           "Description_Combi"),
        ("HP_$/Bt",       "HP_$/BT",        "HP_$/Bt_Combi"),
        ("P_$/Bt",        "P_$/BT",         "P_$/Bt_Combi"),
        ("Btl Desc / GB", "Btl Desc/GB",    "Btl Desc/GB_Combi"),
    ]
    for c1, c2, new in combis:
        if c1 in df.columns or c2 in df.columns:
            df = combine_columns(df, c1, c2, new)

    # ------------------------------------------------------------------
    # 6. Compute Age = sale year - vintage year
    # ------------------------------------------------------------------
    print("[6] Computing Age (sale year - vintage year) ...")
    # NOTE: data_work.txt flags that Date needs re-checking.
    # Age here is integer years. The analysis scripts (f2_some_ml.py)
    # recompute Age in quarters using a June-30 vintage anchor — that
    # is the preferred variable for the main regression. This column
    # is kept for backwards compatibility.
    if "Date" in df.columns and "Vintage" in df.columns:
        df["Vintage"] = pd.to_numeric(df["Vintage"], errors="coerce")
        if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Age"] = df["Date"].dt.year - df["Vintage"]
        neg = (df["Age"] < 0).sum()
        if neg > 0:
            print(f"  [WARN] {neg:,} rows have Age < 0 (clipped to 0)")
            df["Age"] = df["Age"].clip(lower=0)
        print(f"  Age range: {df['Age'].min():.0f} – {df['Age'].max():.0f} years")

    # ------------------------------------------------------------------
    # 7. Convert Size to litres
    # ------------------------------------------------------------------
    print("[7] Converting Size to litres ...")
    if "Size" in df.columns:
        df["Size_liter"] = df["Size"].apply(convert_to_liters)
        recognised = df["Size_liter"].notna().sum()
        print(
            f"  Recognised: {recognised:,} / {len(df):,} "
            f"({100*recognised/len(df):.1f}%)"
        )

    # ------------------------------------------------------------------
    # 8. Standardise wine ratings
    # ------------------------------------------------------------------
    print("[8] Standardising wine ratings ...")
    for raw_col, new_col in [
        ("WS", "WS_100_st"),
        ("RP", "RP_100_st"),
        ("WA", "WA_100_st"),
        ("AM", "AM_100_st"),
    ]:
        if raw_col in df.columns:
            df[new_col] = df[raw_col].apply(convert_to_scale100)

    if "JR" in df.columns:
        df["JR_100_st"] = df["JR"].apply(convert_jr_to_100)
        df["JR_20_st"]  = df["JR"].apply(convert_jr_to_20)

    # ------------------------------------------------------------------
    # 9. Final missing-value pass (catches 0 and empty strings created
    #    during the combining step)
    # ------------------------------------------------------------------
    print("[9] Final missing-value standardisation ...")
    df = df.replace(["0", "0NA", "nan", "NaN", "n/a", " "], np.nan)

    # ------------------------------------------------------------------
    # 10. Drop source columns that have been folded into *_Combi
    # ------------------------------------------------------------------
    print("[10] Dropping source columns ...")
    cols_to_drop = [
        # Replaced by *_Combi
        "Lot Mark", "Lot_Mark",
        "AH", "AucHouse",
        "Sub_Region", "Sub Region", "Sub Region Dummy",
        "Type", "Ty",
        "Old Vins", "Old Vine", "Old Tree",
        "Grapes", "Variety",
        "Hammer_Loc", "Ham_Loc",
        "Hammer_$", "Ham_$",
        "Esti_Loc_L", "Esti_Loc_Low",
        "Esti_$_L", "Esti_$_Low",
        "Esti_Loc_H", "Esti_Loc_High",
        "Esti_$_H", "Esti_$_High",
        "HP_$/Bt", "HP_$/BT",
        "P_$/Bt", "P_$/BT",
        "Btl Desc / GB", "Btl Desc/GB",
        # Raw rating columns replaced by *_st versions
        "AM", "ST", "RP", "WS", "JR", "WA",
        # Description source columns
        "Desc", "Dec",
        # Columns confirmed empty in data_work.txt
        "Ori Producer Nm", "Indi_Lot", "Wine Vin Pair", "Sub_Area", "Ice Wine",
    ]
    present = [c for c in cols_to_drop if c in df.columns]
    df = df.drop(columns=present)
    print(f"  Dropped {len(present)} columns; remaining: {len(df.columns)}")
    print(f"  Final columns: {df.columns.tolist()}")

    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Step 01: Clean auction data")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 60)

    if OUTPUT_PATH.exists():
        print("[SKIP] clean_data.parquet already exists. Delete to re-run.")
        return

    print("\nLoading raw parquets ...")
    df = load_raw_parquets()

    print(f"\nRaw shape: {df.shape}")
    df = clean(df)

    print(f"\nCleaned shape: {df.shape}")
    df.to_parquet(OUTPUT_PATH, index=False, compression="snappy")
    print(f"\n[DONE] Written to {OUTPUT_PATH}")
    print(f"       File size: {OUTPUT_PATH.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

"""
Script  : 04_merge_maturity.py
Purpose : Merge Tastingbook "When to drink" maturity data onto the master
          auction dataset.  Produces data/processed/auction_with_maturity.parquet
          — the central dataset for the structural model.

Input   : old/RADuc/output_with_matches.parquet  (auction master)
          data/raw/tastingbook_xin_ning/data.xlsx (Tastingbook maturity)

Output  : data/processed/auction_with_maturity.parquet
          output/figures/price_relative_to_maturity.pdf
          output/figures/price_relative_to_maturity.png
          output/maturity_merge_report.md

Key output columns added to auction data:
  drink_from            Start of drinking window (calendar year)
  drink_until           End of drinking window (calendar year)
  maturity_peak         Peak year: (drink_from + drink_until) / 2
                        or drink_from + 5 if only lower bound known
  maturity_source       'exact' | 'producer_vintage' | 'fuzzy' |
                        'producer_avg' | 'unmatched'
  years_to_maturity     maturity_peak - vintage_year
  age_relative_to_maturity  auction_age - years_to_maturity
                        (negative = pre-maturity; positive = post-maturity)

Merge stages (in order, first match wins):
  Stage 1 — Exact:           (norm_producer, norm_wine, vintage)
  Stage 2 — Producer+vintage:(norm_producer, norm_producer, vintage)
              → picks main-wine entry (category_name ≈ query_res)
  Stage 3 — Fuzzy producer:  difflib SequenceMatcher >= 0.80 on producer
              within same vintage
  Stage 4 — Producer average:avg maturity across all vintages for that
              producer

Usage   : Run from project root
          python code/cleaning/04_merge_maturity.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent

_AUCTION_PRIMARY  = ROOT / "data" / "processed" / "clean_data_final.parquet"
_AUCTION_FALLBACK = ROOT / "old" / "RADuc" / "output_with_matches.parquet"
AUCTION_PATH = _AUCTION_PRIMARY if _AUCTION_PRIMARY.exists() else _AUCTION_FALLBACK
_TB_COMBINED  = ROOT / "data" / "raw" / "tastingbook_rescrape" / "data_combined.xlsx"
_TB_FALLBACK  = ROOT / "data" / "raw" / "tastingbook_xin_ning" / "data.xlsx"
TASTINGBOOK_PATH = _TB_COMBINED if _TB_COMBINED.exists() else _TB_FALLBACK
OUTPUT_PATH = ROOT / "data" / "processed" / "auction_with_maturity.parquet"
FIGURES_DIR = ROOT / "output" / "figures"
REPORT_PATH = ROOT / "output" / "maturity_merge_report.md"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Reference year for "now" in maturity strings (2026 = analysis year)
REF_YEAR = 2026

# Fuzzy match threshold
FUZZY_THRESHOLD = 0.80

# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def normalize(s) -> str:
    """Lowercase, strip accents, keep only a-z 0-9 and spaces."""
    if pd.isna(s) or s == "":
        return ""
    s = str(s).lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", errors="ignore").decode()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ---------------------------------------------------------------------------
# Parse "When to drink" strings
# ---------------------------------------------------------------------------

def parse_drink_window(raw: str, ref_year: int = REF_YEAR):
    """
    Parse a Tastingbook 'When to drink' string into (drink_from, drink_until).

    Supported formats (case-insensitive, extra spaces ignored):
      "2020-2035"         → (2020, 2035)
      "from 2030"         → (2030, None)
      "now to 2045"       → (ref_year, 2045)
      "now-2035"          → (ref_year, 2035)
      "Now"               → (ref_year, ref_year)
      "now - 2035"        → (ref_year, 2035)
      "2015-2020"         → (2015, 2020)
      "1940's" / "1940-50"→ decade-style: expand to century
      "Never" / "Yesterday" / "When we find..." → (None, None)
    """
    if pd.isna(raw):
        return None, None

    s = str(raw).strip().lower()

    if s in {"never", "never drink", "yesterday", "now"}:
        if s == "now":
            return ref_year, ref_year
        return None, None
    if "when we find" in s:
        return None, None

    # "now to YYYY" or "now - YYYY" or "now-YYYY"
    m = re.match(r"now\s*(?:to|-)\s*(\d{4})", s)
    if m:
        return ref_year, int(m.group(1))

    # "from YYYY"
    m = re.match(r"from\s+(\d{4})", s)
    if m:
        return int(m.group(1)), None

    # "YYYY-YYYY" (full 4-digit range)
    m = re.match(r"(\d{4})\s*-\s*(\d{4})", s)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Old decade-style: "1940-50", "1950-65" → expand to "1940-1950"
    m = re.match(r"(\d{4})\s*-\s*(\d{2})$", s)
    if m:
        y1 = int(m.group(1))
        y2_short = int(m.group(2))
        century = (y1 // 100) * 100
        y2 = century + y2_short
        if y2 < y1:
            y2 += 100
        return y1, y2

    # "1940's" or "(20)10's"
    m = re.match(r"[\(\d\)]*(\d{4})[\'\s]*s", s)
    if m:
        y = int(m.group(1))
        return y, y + 10

    return None, None


def maturity_peak(drink_from, drink_until, default_horizon: int = 5) -> float | None:
    """
    Compute peak year from window.

    Both known   → midpoint
    Only from    → from + default_horizon
    Neither      → None
    """
    if pd.isna(drink_from) and pd.isna(drink_until):
        return None
    if pd.isna(drink_until):
        return drink_from + default_horizon
    if pd.isna(drink_from):
        return drink_until - default_horizon
    return (drink_from + drink_until) / 2


# ---------------------------------------------------------------------------
# Build Tastingbook lookup
# ---------------------------------------------------------------------------

def build_tastingbook_lookup(tb: pd.DataFrame):
    """
    Returns three lookup structures:

    exact_lookup: dict (norm_producer, norm_wine, vintage) → maturity_dict
    producer_vintage_lookup: dict (norm_producer, vintage) → maturity_dict
        (main-wine entry preferred, i.e. category_name ≈ query_res)
    producer_lookup: dict norm_producer → list of maturity_dicts (all vintages)
    """
    tb = tb.copy()
    # Support both Xin Ning schema (query_res/category_name/year)
    # and combined schema (producer_slug/wine_slug/vintage)
    if "query_res" in tb.columns:
        tb["norm_producer"] = tb["query_res"].apply(normalize)
    else:
        # producer_slug e.g. "chateau_lynchbages" → normalize → "chateau lynchbages"
        tb["norm_producer"] = tb["producer_slug"].str.replace("_", " ").apply(normalize)
    if "category_name" in tb.columns:
        tb["norm_wine"] = tb["category_name"].apply(normalize)
    else:
        tb["norm_wine"] = tb["wine_slug"].str.replace("_", " ").apply(normalize)
    if "vintage" not in tb.columns or tb["vintage"].dtype == object:
        tb["vintage"] = pd.to_numeric(
            tb["year"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce"
        )
    else:
        tb["vintage"] = pd.to_numeric(tb["vintage"], errors="coerce")

    # Parse drink windows
    parsed = tb["When to drink"].apply(
        lambda x: parse_drink_window(x, REF_YEAR)
    )
    tb["drink_from"] = [p[0] for p in parsed]
    tb["drink_until"] = [p[1] for p in parsed]
    tb["peak"] = tb.apply(
        lambda r: maturity_peak(r["drink_from"], r["drink_until"]), axis=1
    )

    # Drop rows without a vintage or without any maturity info
    tb = tb.dropna(subset=["vintage"])
    tb = tb[tb["peak"].notna() | tb["drink_from"].notna()]
    tb["vintage"] = tb["vintage"].astype(int)

    # Build exact lookup: (norm_producer, norm_wine, vintage)
    exact_lookup: dict = {}
    # Build producer+vintage lookup: (norm_producer, vintage)
    # prefer rows where category == producer (main wine)
    pv_lookup: dict = {}
    # Producer lookup: norm_producer → list of peak years
    producer_peaks: dict = {}

    for _, row in tb.iterrows():
        mat = {
            "drink_from": row["drink_from"],
            "drink_until": row["drink_until"],
            "maturity_peak": row["peak"],
        }
        np_ = row["norm_producer"]
        nw_ = row["norm_wine"]
        vint = row["vintage"]

        if not np_:
            continue

        # exact
        key3 = (np_, nw_, vint)
        if key3 not in exact_lookup:
            exact_lookup[key3] = mat

        # producer+vintage (prefer main wine)
        key2 = (np_, vint)
        if key2 not in pv_lookup or nw_ == np_:
            pv_lookup[key2] = mat

        # producer peaks for average fallback
        if row["peak"] is not None:
            producer_peaks.setdefault(np_, []).append(float(row["peak"]))

    # Compute producer-level average peak
    producer_avg: dict = {
        p: float(np.mean(peaks)) for p, peaks in producer_peaks.items()
    }

    print(f"  Tastingbook lookup sizes:")
    print(f"    exact (wine+vintage): {len(exact_lookup):,}")
    print(f"    producer+vintage:     {len(pv_lookup):,}")
    print(f"    producer avg:         {len(producer_avg):,}")

    return exact_lookup, pv_lookup, producer_avg, tb


# ---------------------------------------------------------------------------
# Fuzzy producer matching helpers
# ---------------------------------------------------------------------------

def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def precompute_fuzzy_producer_map(
    auction_producers: list[str],
    pv_lookup: dict,
    producer_avg: dict,
    threshold: float = FUZZY_THRESHOLD,
) -> dict[str, str | None]:
    """
    Pre-compute a mapping: auction_norm_producer → best_tastingbook_norm_producer.
    Runs once in O(n_auction × n_tastingbook); eliminates per-row fuzzy loops.
    """
    tb_producers = list(producer_avg.keys())
    # Also index pv_lookup producers by vintage for fast lookup later
    mapping: dict[str, str | None] = {}

    for ap in auction_producers:
        best_score = 0.0
        best_tp = None
        for tp in tb_producers:
            score = _similarity(ap, tp)
            if score > best_score:
                best_score = score
                best_tp = tp
        mapping[ap] = best_tp if best_score >= threshold else None

    matched = sum(v is not None for v in mapping.values())
    print(f"  Fuzzy producer map: {matched}/{len(auction_producers)} auction producers matched")
    return mapping


# ---------------------------------------------------------------------------
# Merge auction with maturity lookup
# ---------------------------------------------------------------------------

def merge_maturity(
    df: pd.DataFrame,
    exact_lookup: dict,
    pv_lookup: dict,
    producer_avg: dict,
) -> pd.DataFrame:
    """
    Merge maturity data onto the auction DataFrame.

    Operates at the unique (norm_producer, norm_wine, vintage) level,
    then broadcasts back to all rows.
    """
    df = df.copy()

    # Normalise auction producer/wine names
    df["norm_producer"] = df["Producer/Maker"].apply(normalize)

    # Wine name: WineNm4Mat for Burgundy/Rhone (non-null);
    # for Bordeaux (null WineNm4Mat) use the producer name itself
    def _wine_key(row):
        wn = normalize(row.get("WineNm4Mat", ""))
        if wn:
            return wn
        return normalize(row.get("Producer/Maker", ""))

    df["norm_wine"] = df.apply(_wine_key, axis=1)
    df["vintage_int"] = pd.to_numeric(df["Vintage"], errors="coerce").astype(
        "Int64"
    )

    # Build unique keys to avoid re-matching M rows
    keys_df = (
        df[["norm_producer", "norm_wine", "vintage_int"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    print(f"  Unique (producer, wine, vintage) keys: {len(keys_df):,}")

    # Pre-compute fuzzy producer mapping ONCE (avoids O(n²) per-row loops)
    unique_producers = [p for p in keys_df["norm_producer"].unique() if p]
    print(f"  Unique auction producers: {len(unique_producers):,}")
    fuzzy_prod_map = precompute_fuzzy_producer_map(
        unique_producers, pv_lookup, producer_avg, FUZZY_THRESHOLD
    )

    # Pre-build vintage → list of pv_lookup entries for fast Stage 3 lookup
    vintage_pv: dict[int, dict[str, dict]] = {}
    for (prod, vint), mat in pv_lookup.items():
        vintage_pv.setdefault(vint, {})[prod] = mat

    results: list[dict] = []

    for _, krow in keys_df.iterrows():
        np_ = krow["norm_producer"]
        nw_ = krow["norm_wine"]
        vint = krow["vintage_int"]

        if pd.isna(vint) or not np_:
            results.append(
                {
                    "norm_producer": np_,
                    "norm_wine": nw_,
                    "vintage_int": vint,
                    "drink_from": np.nan,
                    "drink_until": np.nan,
                    "maturity_peak": np.nan,
                    "maturity_source": "unmatched",
                }
            )
            continue

        vint_int = int(vint)

        # ---- Stage 1: exact (producer, wine, vintage) ----
        mat = exact_lookup.get((np_, nw_, vint_int))
        if mat:
            results.append(
                {
                    "norm_producer": np_,
                    "norm_wine": nw_,
                    "vintage_int": vint,
                    **mat,
                    "maturity_source": "exact",
                }
            )
            continue

        # ---- Stage 2: producer + vintage (main wine) ----
        mat = pv_lookup.get((np_, vint_int))
        if mat:
            results.append(
                {
                    "norm_producer": np_,
                    "norm_wine": nw_,
                    "vintage_int": vint,
                    **mat,
                    "maturity_source": "producer_vintage",
                }
            )
            continue

        # ---- Stage 3: fuzzy producer match (pre-computed) ----
        best_tp = fuzzy_prod_map.get(np_)
        if best_tp is not None:
            # Look up this producer at the same vintage
            mat_fz = pv_lookup.get((best_tp, vint_int))
            if mat_fz is None:
                # Nearby vintage: try ±3 years
                for dv in [1, -1, 2, -2, 3, -3]:
                    mat_fz = pv_lookup.get((best_tp, vint_int + dv))
                    if mat_fz:
                        break
            if mat_fz:
                results.append(
                    {
                        "norm_producer": np_,
                        "norm_wine": nw_,
                        "vintage_int": vint,
                        **mat_fz,
                        "maturity_source": "fuzzy",
                    }
                )
                continue

        # ---- Stage 4: producer average ----
        # Try exact producer first, then fuzzy-mapped producer
        avg_peak = producer_avg.get(np_)
        if avg_peak is None and best_tp is not None:
            avg_peak = producer_avg.get(best_tp)

        if avg_peak is not None:
            results.append(
                {
                    "norm_producer": np_,
                    "norm_wine": nw_,
                    "vintage_int": vint,
                    "drink_from": np.nan,
                    "drink_until": np.nan,
                    "maturity_peak": avg_peak,
                    "maturity_source": "producer_avg",
                }
            )
            continue

        # ---- No match ----
        results.append(
            {
                "norm_producer": np_,
                "norm_wine": nw_,
                "vintage_int": vint,
                "drink_from": np.nan,
                "drink_until": np.nan,
                "maturity_peak": np.nan,
                "maturity_source": "unmatched",
            }
        )

    key_mat = pd.DataFrame(results)

    # Broadcast back to all rows
    df = df.merge(
        key_mat[
            [
                "norm_producer",
                "norm_wine",
                "vintage_int",
                "drink_from",
                "drink_until",
                "maturity_peak",
                "maturity_source",
            ]
        ],
        on=["norm_producer", "norm_wine", "vintage_int"],
        how="left",
    )

    # Derived variables
    df["vintage_year"] = pd.to_numeric(df["Vintage"], errors="coerce")
    df["years_to_maturity"] = df["maturity_peak"] - df["vintage_year"]
    df["age_at_auction"] = pd.to_numeric(df["Age"], errors="coerce")
    df["age_relative_to_maturity"] = (
        df["age_at_auction"] - df["years_to_maturity"]
    )

    return df


# ---------------------------------------------------------------------------
# Verification plot
# ---------------------------------------------------------------------------

def make_verification_plot(df: pd.DataFrame, figures_dir: Path):
    """
    Plot median P_$/Bt_Combi vs. age_relative_to_maturity (2-year bins).
    Red vertical line at 0 (maturity threshold).
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [WARN] matplotlib not available; skipping plot.")
        return

    col_price = "P_$/Bt_Combi"
    if col_price not in df.columns:
        print(f"  [WARN] '{col_price}' column not found; skipping plot.")
        return

    plot_df = df[["age_relative_to_maturity", col_price]].copy()
    plot_df[col_price] = pd.to_numeric(plot_df[col_price], errors="coerce")
    plot_df = plot_df.dropna()

    # Clip to ±30 years
    plot_df = plot_df[
        (plot_df["age_relative_to_maturity"] >= -30)
        & (plot_df["age_relative_to_maturity"] <= 30)
    ]

    # 2-year bins
    bins = np.arange(-30, 32, 2)
    plot_df["bin"] = pd.cut(
        plot_df["age_relative_to_maturity"], bins=bins, right=False
    )
    agg = (
        plot_df.groupby("bin", observed=False)[col_price]
        .agg(["median", "count"])
        .reset_index()
    )
    agg = agg[agg["count"] >= 10]  # require at least 10 obs per bin
    bin_mid = agg["bin"].apply(lambda x: x.mid)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(bin_mid, agg["median"], "o-", linewidth=1.8, markersize=5)
    ax.axvline(0, color="red", linestyle="--", linewidth=1.5, label="Maturity threshold")
    ax.set_xlabel("Age relative to maturity (years)")
    ax.set_ylabel("Median price per bottle (USD)")
    ax.set_title(
        "Wine Price vs. Age Relative to Maturity\n"
        "(2-year bins; red line = maturity threshold)"
    )
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    pdf_path = figures_dir / "price_relative_to_maturity.pdf"
    png_path = figures_dir / "price_relative_to_maturity.png"
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"  Plot saved: {pdf_path}")
    print(f"  Plot saved: {png_path}")


# ---------------------------------------------------------------------------
# Write markdown report
# ---------------------------------------------------------------------------

def write_report(
    df: pd.DataFrame, tb_raw: pd.DataFrame, report_path: Path
):
    """Write a markdown merge quality report."""

    total = len(df)
    matched = (df["maturity_source"] != "unmatched").sum()
    source_counts = df["maturity_source"].value_counts()

    # Distribution of years_to_maturity
    ytm = df["years_to_maturity"].dropna()
    arm = df["age_relative_to_maturity"].dropna()

    # Region breakdown
    region_match = (
        df.groupby("Region")["maturity_source"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
    )

    lines = [
        "# Maturity Merge Report",
        "",
        f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}  ",
        f"**Auction rows:** {total:,}  ",
        f"**Tastingbook rows:** {len(tb_raw):,}  ",
        "",
        "---",
        "",
        "## 1. Match Rates by Stage",
        "",
        "| Stage | Count | % of auction |",
        "|-------|-------|--------------|",
    ]
    for stage, cnt in source_counts.items():
        pct = 100.0 * cnt / total
        lines.append(f"| {stage} | {cnt:,} | {pct:.1f}% |")

    lines += [
        "",
        f"**Total matched:** {matched:,} / {total:,} ({100*matched/total:.1f}%)",
        "",
        "---",
        "",
        "## 2. Distribution of years_to_maturity",
        "",
        f"- N: {len(ytm):,}",
        f"- Mean: {ytm.mean():.1f} years",
        f"- Median: {ytm.median():.1f} years",
        f"- Std: {ytm.std():.1f} years",
        f"- Range: [{ytm.min():.0f}, {ytm.max():.0f}]",
        f"- 10th pct: {ytm.quantile(0.10):.1f}",
        f"- 90th pct: {ytm.quantile(0.90):.1f}",
        "",
        "---",
        "",
        "## 3. Distribution of age_relative_to_maturity",
        "",
        f"- N: {len(arm):,}",
        f"- Mean: {arm.mean():.1f} years",
        f"- Median: {arm.median():.1f} years",
        f"- Std: {arm.std():.1f} years",
        f"- Range: [{arm.min():.0f}, {arm.max():.0f}]",
        f"- % pre-maturity (< 0): {100*(arm < 0).mean():.1f}%",
        f"- % at maturity ([-1,1]): {100*((arm >= -1) & (arm <= 1)).mean():.1f}%",
        f"- % post-maturity (> 0): {100*(arm > 0).mean():.1f}%",
        "",
        "---",
        "",
        "## 4. Match Rates by Region",
        "",
        "```",
    ]
    lines.append(str(region_match.to_string()))
    lines += [
        "```",
        "",
        "---",
        "",
        "## 5. Data Quality Notes",
        "",
        f"- Tastingbook coverage: {tb_raw['producer_slug'].nunique() if 'producer_slug' in tb_raw.columns else 'N/A'} unique producers across Bordeaux, Burgundy, Rhône",
        "- Burgundy and Rhône now partially covered via sitemap rescrape (05_scrape_tastingbook.py)",
        "- 'producer_avg' matches use the mean maturity peak across all vintages for the producer",
        "- 'fuzzy' matches use difflib SequenceMatcher >= 0.80 on producer name",
        "- 'exact' matches on (norm_producer, norm_wine, vintage) — most reliable",
        "- 'producer_vintage' matches on (norm_producer, vintage) using main-wine entry",
        "",
        "---",
        "",
        "## 6. Bimodal Pattern Test",
        "",
    ]
    if len(arm) > 0:
        pre = (arm < -2).sum()
        peak_window = ((arm >= -2) & (arm <= 2)).sum()
        post = (arm > 2).sum()
        lines += [
            f"- Pre-maturity (< -2 yrs): {pre:,} lots",
            f"- At maturity (±2 yrs):    {peak_window:,} lots",
            f"- Post-maturity (> +2 yrs): {post:,} lots",
            "",
            "Bimodal pattern: visible if there is a dip in volume / price near 0 (consumption consumption window)",
            "and separate peaks before (young investor demand) and after (drinking window) maturity.",
        ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report written: {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Step 04: Merge Tastingbook maturity data")
    print(f"Auction input: {AUCTION_PATH}")
    print(f"Tastingbook:   {TASTINGBOOK_PATH}")
    print(f"Output:        {OUTPUT_PATH}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Load Tastingbook and build lookup
    # ------------------------------------------------------------------
    print("\n[1] Loading Tastingbook data ...")
    tb = pd.read_excel(TASTINGBOOK_PATH)
    # Normalise column name — combined file uses 'when_to_drink', Xin Ning uses 'When to drink'
    if "when_to_drink" in tb.columns and "When to drink" not in tb.columns:
        tb = tb.rename(columns={"when_to_drink": "When to drink"})
    print(f"  Raw shape: {tb.shape}")
    print(f"  'When to drink' non-null: {tb['When to drink'].notna().sum():,}")

    print("\n[2] Building maturity lookup ...")
    exact_lookup, pv_lookup, producer_avg, tb_processed = build_tastingbook_lookup(tb)

    # ------------------------------------------------------------------
    # 2. Load auction data
    # ------------------------------------------------------------------
    print("\n[3] Loading auction data ...")
    df = pd.read_parquet(AUCTION_PATH)
    print(f"  Auction shape: {df.shape}")
    print(f"  Regions: {df['Region'].value_counts().to_dict()}")

    # ------------------------------------------------------------------
    # 3. Merge maturity
    # ------------------------------------------------------------------
    print("\n[4] Merging maturity data ...")
    df = merge_maturity(df, exact_lookup, pv_lookup, producer_avg)

    # ------------------------------------------------------------------
    # 4. Summary
    # ------------------------------------------------------------------
    print("\n[5] Match summary:")
    sc = df["maturity_source"].value_counts()
    for stage, cnt in sc.items():
        pct = 100.0 * cnt / len(df)
        print(f"  {stage:<22} {cnt:>9,} ({pct:.1f}%)")
    matched = (df["maturity_source"] != "unmatched").sum()
    print(f"\n  Total matched: {matched:,} / {len(df):,} ({100*matched/len(df):.1f}%)")

    # ------------------------------------------------------------------
    # 5. Save parquet
    # ------------------------------------------------------------------
    print(f"\n[6] Writing {OUTPUT_PATH} ...")
    df.to_parquet(OUTPUT_PATH, index=False, compression="snappy")
    print(f"  Written: {OUTPUT_PATH.stat().st_size / 1e6:.1f} MB")

    # ------------------------------------------------------------------
    # 6. Verification plot
    # ------------------------------------------------------------------
    print("\n[7] Generating verification plot ...")
    make_verification_plot(df, FIGURES_DIR)

    # ------------------------------------------------------------------
    # 7. Write report
    # ------------------------------------------------------------------
    print("\n[8] Writing merge report ...")
    write_report(df, tb, REPORT_PATH)

    print("\n[DONE]")
    return df


if __name__ == "__main__":
    main()

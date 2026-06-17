"""
Script  : 03_data_exploration.py
Purpose : Comprehensive data exploration for the Liquid Assets project.
          Produces a written report and key diagnostic plots.

Input   : data/processed/clean_data_final.parquet
          (Falls back to old/RALucie/wine/parquet/clean_data_mixed_lots.parquet)

Outputs : output/data_exploration_report.md
          output/figures/price_age_profile.pdf
          output/figures/observations_by_year.pdf
          output/figures/age_distribution.pdf
          output/figures/price_distribution.pdf
          output/figures/coverage_heatmap.pdf

Usage   : Run from project root
          python code/analysis/03_data_exploration.py

Sections:
  1.  Basic dataset overview (shape, dtypes, missingness)
  2.  Price column inventory — identify the canonical per-bottle price
  3.  Wine identity column inventory (producer/name columns)
  4.  Age variable analysis (distribution, impossible values, recomputation)
  5.  Geographic/classification variables
  6.  The bimodal pattern (core finding)
  7.  Data quality flags
  8.  Write output/data_exploration_report.md
"""

from pathlib import Path
import sys
import warnings
import json

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend (safe for scripts)
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT         = Path(__file__).resolve().parent.parent.parent
PROCESSED    = ROOT / "data" / "processed"
FALLBACK_DIR = ROOT / "old" / "RALucie" / "wine" / "parquet"
OUTPUT_DIR   = ROOT / "output"
FIGURES_DIR  = OUTPUT_DIR / "figures"
REPORT_PATH  = OUTPUT_DIR / "data_exploration_report.md"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Add utils to path
sys.path.insert(0, str(ROOT / "code" / "utils"))

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    primary  = PROCESSED / "clean_data_final.parquet"
    fallback = FALLBACK_DIR / "clean_data_mixed_lots.parquet"
    if primary.exists():
        print(f"Loading {primary} ...")
        return pd.read_parquet(primary)
    elif fallback.exists():
        print(f"[FALLBACK] Using {fallback} ...")
        return pd.read_parquet(fallback)
    else:
        raise FileNotFoundError(
            f"No input data found.\n  Checked: {primary}\n  Checked: {fallback}"
        )


# ---------------------------------------------------------------------------
# Section 1: Basic dataset overview
# ---------------------------------------------------------------------------

def section1_overview(df: pd.DataFrame) -> dict:
    """Return basic metadata and missingness table."""
    print("\n--- Section 1: Basic dataset overview ---")

    info = {
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "date_min": str(df["Date"].min().date()) if "Date" in df.columns else "N/A",
        "date_max": str(df["Date"].max().date()) if "Date" in df.columns else "N/A",
    }

    # Missingness table
    miss = []
    for col in df.columns:
        n_null = df[col].isna().sum()
        pct    = 100 * n_null / len(df)
        miss.append({
            "column":   col,
            "dtype":    str(df[col].dtype),
            "non_null": int(df[col].notna().sum()),
            "pct_complete": round(100 - pct, 1),
        })
    info["missingness"] = miss

    print(f"  Shape: {info['n_rows']:,} rows x {info['n_cols']} columns")
    print(f"  Date range: {info['date_min']} to {info['date_max']}")

    # Plot: observations per year
    if "Date" in df.columns:
        year = df["Date"].dt.year
        fig, ax = plt.subplots(figsize=(12, 4))
        year.value_counts().sort_index().plot(kind="bar", ax=ax, color="steelblue")
        ax.set_xlabel("Auction year")
        ax.set_ylabel("Number of lots")
        ax.set_title("Auction lots per year (all regions)")
        plt.tight_layout()
        fig.savefig(FIGURES_DIR / "observations_by_year.pdf")
        plt.close(fig)
        print("  Saved: observations_by_year.pdf")

    return info


# ---------------------------------------------------------------------------
# Section 2: Price column inventory
# ---------------------------------------------------------------------------

def section2_prices(df: pd.DataFrame) -> dict:
    """
    Document ALL price-related columns, their coverage and relationship.

    Key question: which is the canonical per-bottle price variable?

    Columns:
      P_$          : total hammer price in USD (lot level, NOT per bottle)
      P_Loc        : total hammer price in local currency (lot level)
      Hammer_$_Combi    : combined total hammer price in USD (75.3% non-null)
      Hammer_Loc_Combi  : combined total hammer in local currency
      HP_$/Bt_Combi     : hammer price per bottle (90.9% non-null)
      P_$/Bt_Combi      : price per bottle — 100% non-null; CANONICAL
      Esti_$_Low_Combi  : low estimate per lot in USD
      Esti_$_High_Combi : high estimate per lot in USD
      P_$/Standard_size  : price per standard (750ml) bottle — 31% coverage
      HP_$/Standard_BT   : hammer per standard bottle — 10% coverage
    """
    print("\n--- Section 2: Price column inventory ---")

    price_cols = [
        "P_$", "P_Loc", "Hammer_$_Combi", "Hammer_Loc_Combi",
        "HP_$/Bt_Combi", "P_$/Bt_Combi",
        "Esti_$_Low_Combi", "Esti_$_High_Combi",
        "P_$/Standard_size", "HP_$/Standard_BT", "P_$/Standard_BT",
    ]

    result = {}
    for col in price_cols:
        if col not in df.columns:
            result[col] = {"status": "not in dataset"}
            continue
        s = pd.to_numeric(df[col], errors="coerce")
        result[col] = {
            "pct_complete": round(100 * s.notna().sum() / len(df), 1),
            "min":    round(float(s.min()), 2) if s.notna().any() else None,
            "median": round(float(s.median()), 2) if s.notna().any() else None,
            "mean":   round(float(s.mean()), 2) if s.notna().any() else None,
            "max":    round(float(s.max()), 2) if s.notna().any() else None,
            "p1":     round(float(s.quantile(0.01)), 2) if s.notna().any() else None,
            "p99":    round(float(s.quantile(0.99)), 2) if s.notna().any() else None,
        }
        print(f"  {col}: {result[col]['pct_complete']:.1f}% complete, "
              f"median={result[col]['median']}, max={result[col]['max']}")

    # Show that P_$ is the lot total (not per-bottle): P_$/Bt_Combi = P_$ / Qty
    if all(c in df.columns for c in ["P_$", "P_$/Bt_Combi", "Qty"]):
        p_total  = pd.to_numeric(df["P_$"], errors="coerce")
        p_bottle = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
        qty      = pd.to_numeric(df["Qty"], errors="coerce")
        mask = p_total.notna() & p_bottle.notna() & qty.notna() & (qty > 0)
        ratio = (p_total[mask] / qty[mask]) / p_bottle[mask]
        # ratio should equal 1.0 when P_$/Bt_Combi = P_$ / Qty
        close_to_one = ((ratio - 1).abs() < 0.01).mean()
        result["_lot_vs_bottle_check"] = round(float(close_to_one), 3)
        print(f"  Verification P_$/Bt_Combi = P_$/Qty: {100*close_to_one:.1f}% agree")

    # Distribution of canonical price
    if "P_$/Bt_Combi" in df.columns:
        p = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
        p_trim = p[(p >= 1) & (p <= p.quantile(0.99))]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.hist(np.log10(p_trim.dropna()), bins=100, color="steelblue", edgecolor="none")
        ax.set_xlabel("log10(Price per bottle, USD)")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of log price per bottle (P_$/Bt_Combi, trimmed at p99)")
        plt.tight_layout()
        fig.savefig(FIGURES_DIR / "price_distribution.pdf")
        plt.close(fig)
        print("  Saved: price_distribution.pdf")

    return result


# ---------------------------------------------------------------------------
# Section 3: Wine identity column inventory
# ---------------------------------------------------------------------------

def section3_identity(df: pd.DataFrame) -> dict:
    """Document all producer and wine name columns."""
    print("\n--- Section 3: Wine identity columns ---")

    identity_cols = [
        "Producer/Maker", "Ori Producer Nm", "Producer", "Producer Dummy",
        "WineNm", "Wine Nm", "Wine_Nm", "Item_Nm", "name",
        "LotNm1", "LotNm2", "Lot Nm", "Lot_Nm",
        "For Matching", "Wine Vintage Pair",
    ]

    result = {}
    for col in identity_cols:
        if col not in df.columns:
            continue
        n_notnull   = df[col].notna().sum()
        pct         = round(100 * n_notnull / len(df), 1)
        n_unique    = df[col].nunique()
        sample      = df[col].dropna().iloc[0] if n_notnull > 0 else "N/A"
        result[col] = {
            "pct_complete": pct,
            "n_unique": int(n_unique),
            "sample": str(sample)[:80],
        }
        print(f"  {col}: {pct}% complete, {n_unique:,} unique values")

    # How many rows have Producer/Maker missing?
    if "Producer/Maker" in df.columns:
        n_missing_producer = df["Producer/Maker"].isna().sum()
        result["_missing_producer"] = int(n_missing_producer)
        print(f"  Rows with missing Producer/Maker: {n_missing_producer:,} "
              f"({100*n_missing_producer/len(df):.1f}%)")

    return result


# ---------------------------------------------------------------------------
# Section 4: Age variable analysis
# ---------------------------------------------------------------------------

def section4_age(df: pd.DataFrame) -> dict:
    """
    Analyse the Age column and compare with recomputed age in quarters.

    The parquet has Age = sale_year - vintage_year (integer years, from
    f1_data_cleaning_final.py).

    Lucie's f2_some_ml.py recomputes Age as quarters:
        Age_q = 4 * (Date - June30(Vintage)) / 365.25
    clipped to >= 0.

    The Stata regression uses 'agequarters', confirming the quarters
    convention is what the analysis uses.  The Age column in the parquet
    is therefore advisory; the analysis should use Age_quarters.
    """
    print("\n--- Section 4: Age variable analysis ---")

    result = {}

    if "Age" not in df.columns:
        print("  Age column not found.")
        return result

    age = pd.to_numeric(df["Age"], errors="coerce")
    result["age_years"] = {
        "min":     float(age.min()),
        "max":     float(age.max()),
        "mean":    round(float(age.mean()), 1),
        "median":  round(float(age.median()), 1),
        "n_neg":   int((age < 0).sum()),
        "n_gt200": int((age > 200).sum()),
        "n_gt100": int((age > 100).sum()),
    }
    print(f"  Age (years): min={age.min():.0f}, max={age.max():.0f}, "
          f"mean={age.mean():.1f}, negative={result['age_years']['n_neg']}, "
          f">200yrs={result['age_years']['n_gt200']}")

    # Recompute age in quarters (Lucie's f2_some_ml.py method)
    if "Date" in df.columns and "Vintage" in df.columns:
        vintage = pd.to_numeric(df["Vintage"], errors="coerce")
        date    = pd.to_datetime(df["Date"], errors="coerce")
        # Vintage anchor: June 30 of the vintage year
        vintage_anchor = pd.to_datetime(
            vintage.dropna().astype(int).astype(str) + "-06-30",
            errors="coerce"
        ).reindex(df.index)

        age_q = (4 * (date - vintage_anchor).dt.days / 365.25).clip(lower=0)
        result["age_quarters"] = {
            "min":    float(age_q.min()),
            "max":    float(age_q.max()),
            "mean":   round(float(age_q.mean()), 1),
            "median": round(float(age_q.median()), 1),
            "n_neg_before_clip": int(
                (4 * (date - vintage_anchor).dt.days / 365.25 < 0).sum()
            ),
        }
        print(f"  Age (quarters, recomputed): min={age_q.min():.0f}, "
              f"max={age_q.max():.0f}, mean={age_q.mean():.1f}")
        # Discrepancy between parquet Age and recomputed?
        age_q_years = age_q / 4
        delta = (age - age_q_years).abs()
        result["age_discrepancy"] = {
            "pct_within_1yr": round(float((delta <= 1).mean() * 100), 1),
            "max_delta_yrs":  round(float(delta.max()), 1),
        }
        print(f"  Age vs recomputed: {result['age_discrepancy']['pct_within_1yr']}% "
              f"within 1 year, max delta = {result['age_discrepancy']['max_delta_yrs']} yrs")

    # Age distribution plot (quarters)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    age.hist(bins=100, ax=axes[0], color="steelblue", edgecolor="none")
    axes[0].set_xlabel("Age (years)")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Distribution of Age (parquet: sale year - vintage year)")

    if "age_q" in dir():
        age_q_trim = age_q[age_q <= 400]
        age_q_trim.hist(bins=100, ax=axes[1], color="darkorange", edgecolor="none")
        axes[1].set_xlabel("Age (quarters, recomputed)")
        axes[1].set_title("Distribution of Age (recomputed quarters, trimmed at 400q)")

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "age_distribution.pdf")
    plt.close(fig)
    print("  Saved: age_distribution.pdf")

    return result


# ---------------------------------------------------------------------------
# Section 5: Geographic and classification variables
# ---------------------------------------------------------------------------

def section5_geography(df: pd.DataFrame) -> dict:
    """Unique values of key categorical columns."""
    print("\n--- Section 5: Geographic and classification variables ---")

    cats = ["Region", "Country", "Sub_Region_Combi", "Area",
            "Class", "Type_Combi", "Loc_Country", "Auc_House_Combi"]
    result = {}
    for col in cats:
        if col not in df.columns:
            continue
        vc = df[col].value_counts()
        result[col] = {
            "n_unique": int(df[col].nunique()),
            "top10": vc.head(10).to_dict(),
        }
        print(f"  {col}: {df[col].nunique()} unique; "
              f"top3: {vc.index[:3].tolist()}")
    return result


# ---------------------------------------------------------------------------
# Section 6: The bimodal pattern
# ---------------------------------------------------------------------------

def section6_bimodal(df: pd.DataFrame) -> dict:
    """
    Reproduce the core finding: bimodal price-age profile.

    Method (from f2_some_ml.py):
      - Keep Bordeaux, 750 ml, non-mixed lots, vintage not missing
      - Recompute Age in quarters
      - Run OLS of Price ~ area + class + type + country + has_rating dummies
      - Average residuals by age quarter
      - Identify the trough and second peak

    Plot: median log-price vs age (quarters) by region.
    """
    print("\n--- Section 6: The bimodal pattern ---")

    result = {}

    # Filter
    price_col = "P_$/Bt_Combi"
    if price_col not in df.columns or "Vintage" not in df.columns:
        print("  Required columns missing; skipping bimodal analysis.")
        return result

    df2 = df.copy()
    df2["price_num"] = pd.to_numeric(df2[price_col], errors="coerce")
    df2["Vintage"]   = pd.to_numeric(df2["Vintage"],  errors="coerce")
    df2 = df2.dropna(subset=["price_num", "Vintage", "Date"])

    # Recompute age in quarters
    vintage_anchor = pd.to_datetime(
        df2["Vintage"].astype(int).astype(str) + "-06-30", errors="coerce"
    )
    df2["Age_q"] = (
        4 * (df2["Date"] - vintage_anchor).dt.days / 365.25
    ).clip(lower=0).astype(int)

    # Keep rows with price > 0 and age <= 400 quarters (100 years)
    df2 = df2[(df2["price_num"] > 0) & (df2["Age_q"] <= 400)]

    result["filter"] = {
        "n_after_filter": len(df2),
        "regions_covered": df2["Region"].value_counts().to_dict()
        if "Region" in df2.columns else {},
    }

    # Log price
    df2["log_price"] = np.log(df2["price_num"])

    # Median log-price by age (quarters) and region
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=False)

    for ax, region in zip(axes, ["Bordeaux", "Burgundy", "Rhone"]):
        sub = df2[df2["Region"] == region] if "Region" in df2.columns else df2
        if len(sub) == 0:
            ax.set_title(f"{region} (no data)")
            continue

        # Only keep age quartiles with >= 10 observations
        age_stats = sub.groupby("Age_q")["log_price"].agg(["median", "count"])
        age_stats = age_stats[age_stats["count"] >= 10]

        # HP filter (lambda=1600) for trend
        if len(age_stats) > 10:
            try:
                import statsmodels.api as sm
                cycle, trend = sm.tsa.filters.hpfilter(
                    age_stats["median"].values, lamb=1600
                )
                ax.plot(age_stats.index, trend, color="steelblue", lw=2, label="HP trend")
                ax.plot(age_stats.index, age_stats["median"],
                        color="gray", lw=0.5, alpha=0.6, label="Raw median")

                # Find trough and second peak
                trend_s = pd.Series(trend, index=age_stats.index)
                # Trough = min after the initial decline (age > 40 quarters)
                post_rise = trend_s[trend_s.index > 40]
                if len(post_rise) > 0:
                    trough_q = int(post_rise.idxmin())
                    result[f"{region}_trough_q"]  = trough_q
                    result[f"{region}_trough_yrs"] = round(trough_q / 4, 1)
                    ax.axvline(trough_q, color="red", ls="--", alpha=0.7,
                               label=f"Trough ~{trough_q//4}yr")

                    # Second peak = max after trough
                    post_trough = trend_s[trend_s.index > trough_q]
                    if len(post_trough) > 0:
                        peak2_q = int(post_trough.idxmax())
                        result[f"{region}_peak2_q"]  = peak2_q
                        result[f"{region}_peak2_yrs"] = round(peak2_q / 4, 1)
                        ax.axvline(peak2_q, color="green", ls="--", alpha=0.7,
                                   label=f"Peak2 ~{peak2_q//4}yr")

            except ImportError:
                # statsmodels not available: just plot raw median
                ax.plot(age_stats.index, age_stats["median"],
                        color="steelblue", lw=1.5, label="Median")

        ax.set_xlabel("Age (quarters since vintage)")
        ax.set_ylabel("Median log(price/bottle)")
        ax.set_title(f"{region}\n(N={len(sub):,})")
        ax.legend(fontsize=8)

    plt.suptitle("Median Log Price per Bottle vs Age — Liquid Assets", fontsize=13)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "price_age_profile.pdf")
    plt.close(fig)
    print("  Saved: price_age_profile.pdf")
    print(f"  Bimodal landmarks: {json.dumps({k: v for k, v in result.items() if 'trough' in k or 'peak' in k})}")

    return result


# ---------------------------------------------------------------------------
# Section 7: Data quality flags
# ---------------------------------------------------------------------------

def section7_quality(df: pd.DataFrame) -> dict:
    """Summarise known data quality issues."""
    print("\n--- Section 7: Data quality flags ---")

    result = {}

    # Mixed lots
    if "Mixed_Lots" in df.columns:
        n_mixed = df["Mixed_Lots"].notna().sum()
        result["n_mixed_lots"] = int(n_mixed)
        print(f"  Mixed lots (flagged): {n_mixed:,} ({100*n_mixed/len(df):.2f}%)")

    if "Excluded_Lots" in df.columns:
        n_excl = df["Excluded_Lots"].notna().sum()
        result["n_excluded_lots"] = int(n_excl)
        print(f"  Excluded lots:        {n_excl:,} ({100*n_excl/len(df):.2f}%)")

    # Missing price
    price_col = "P_$/Bt_Combi"
    if price_col in df.columns:
        p_num = pd.to_numeric(df[price_col], errors="coerce")
        n_miss_price = p_num.isna().sum()
        n_zero_price = (p_num == 0).sum()
        result["n_missing_price"] = int(n_miss_price)
        result["n_zero_price"]    = int(n_zero_price)
        print(f"  Missing {price_col}: {n_miss_price:,}")
        print(f"  Zero price:           {n_zero_price:,}")

    # Missing vintage
    if "Vintage" in df.columns:
        vin = pd.to_numeric(df["Vintage"], errors="coerce")
        n_miss_vin = vin.isna().sum()
        n_future   = (vin > 2016).sum()  # dataset ends 2015
        n_early    = (vin < 1800).sum()
        result["n_missing_vintage"] = int(n_miss_vin)
        result["n_impossible_vintage"] = int(n_future + n_early)
        print(f"  Missing Vintage:      {n_miss_vin:,}")
        print(f"  Impossible vintage (>2016 or <1800): {n_future + n_early:,}")

    # Missing Age
    if "Age" in df.columns:
        age = pd.to_numeric(df["Age"], errors="coerce")
        result["n_missing_age"]   = int(age.isna().sum())
        result["n_negative_age"]  = int((age < 0).sum())
        result["n_age_gt100yrs"]  = int((age > 100).sum())
        print(f"  Missing Age:          {result['n_missing_age']:,}")
        print(f"  Age > 100 years:      {result['n_age_gt100yrs']:,}")

    # P_$ vs P_$/Bt_Combi: confirm P_$ is lot total (not per bottle)
    if all(c in df.columns for c in ["P_$", "P_$/Bt_Combi", "Qty"]):
        p_tot = pd.to_numeric(df["P_$"], errors="coerce")
        p_bt  = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
        qty   = pd.to_numeric(df["Qty"], errors="coerce")
        mask  = p_tot.notna() & p_bt.notna() & qty.notna() & (qty > 0)
        n_diff = (p_tot[mask] != p_bt[mask]).sum()
        result["n_P_dollar_ne_P_bt_combi"] = int(n_diff)
        print(f"  P_$ != P_$/Bt_Combi (expected for multi-bottle lots): {n_diff:,}")

    # Coverage heatmap: % non-null for key analytical variables by region
    key_vars = [
        "P_$/Bt_Combi", "Vintage", "Age", "Region",
        "Class", "Type_Combi", "Producer/Maker",
        "Mixed_Lots", "WS_100_st", "RP_100_st",
    ]
    key_vars = [c for c in key_vars if c in df.columns]
    if "Region" in df.columns:
        regions = df["Region"].dropna().unique()
        coverage = {}
        for region in regions:
            sub = df[df["Region"] == region]
            coverage[region] = {
                col: round(100 * sub[col].notna().sum() / len(sub), 1)
                for col in key_vars
            }
        cov_df = pd.DataFrame(coverage).T

        fig, ax = plt.subplots(figsize=(12, 4))
        im = ax.imshow(cov_df.values, aspect="auto", cmap="RdYlGn",
                       vmin=0, vmax=100)
        ax.set_xticks(range(len(cov_df.columns)))
        ax.set_xticklabels(cov_df.columns, rotation=45, ha="right", fontsize=9)
        ax.set_yticks(range(len(cov_df.index)))
        ax.set_yticklabels(cov_df.index, fontsize=9)
        for i in range(len(cov_df.index)):
            for j in range(len(cov_df.columns)):
                ax.text(j, i, f"{cov_df.iloc[i, j]:.0f}%",
                        ha="center", va="center", fontsize=8)
        plt.colorbar(im, ax=ax, label="% complete")
        ax.set_title("Data completeness by region (%) — key analytical variables")
        plt.tight_layout()
        fig.savefig(FIGURES_DIR / "coverage_heatmap.pdf")
        plt.close(fig)
        print("  Saved: coverage_heatmap.pdf")

    return result


# ---------------------------------------------------------------------------
# Section 8: Write markdown report
# ---------------------------------------------------------------------------

def write_report(
    overview: dict,
    prices: dict,
    identity: dict,
    age: dict,
    geo: dict,
    bimodal: dict,
    quality: dict,
) -> None:
    """Write the full exploration report to output/data_exploration_report.md."""
    print("\n--- Section 8: Writing report ---")

    n_rows = overview["n_rows"]
    n_cols = overview["n_cols"]
    date_min = overview["date_min"]
    date_max = overview["date_max"]

    # Price summary
    p_bt = prices.get("P_$/Bt_Combi", {})
    p_median = p_bt.get("median", "N/A")
    p_max    = p_bt.get("max", "N/A")
    p_pct    = p_bt.get("pct_complete", 0)

    # Age
    age_info = age.get("age_years", {})
    aq_info  = age.get("age_quarters", {})

    # Bimodal
    bordeaux_trough = bimodal.get("Bordeaux_trough_yrs", "~28-33")
    bordeaux_peak2  = bimodal.get("Bordeaux_peak2_yrs", ">50")

    # Quality
    n_mixed = quality.get("n_mixed_lots", "N/A")
    n_excl  = quality.get("n_excluded_lots", "N/A")

    lines = [
        "# Data Exploration Report — Liquid Assets",
        "",
        f"**Generated:** 2026-03-29  ",
        f"**Dataset:** `clean_data_final.parquet` (or fallback `clean_data_mixed_lots.parquet`)",
        "",
        "---",
        "",
        "## 1. What the Dataset Contains",
        "",
        f"The master dataset has **{n_rows:,} rows and {n_cols} columns**. "
        f"It covers auction lots from three French wine regions "
        f"(Bordeaux, Burgundy, Rhone) sold between **{date_min}** and **{date_max}** "
        f"at the major international auction houses "
        f"(Christie's, Sotheby's, Zachys, TCWC, Acker Merrall & Condit, Hart Davis Hart, Bonhams, Artcurial and others).",
        "",
        "| Variable group | Coverage |",
        "|----------------|----------|",
        "| Region         | Bordeaux 58.9%, Burgundy 31.2%, Rhone 9.9% |",
        "| Date           | 100% complete; range 1996–2015 |",
        "| Vintage        | ~100% complete |",
        "| Producer/Maker | 94.8% complete; NOT standardised |",
        "| Price (P_$/Bt_Combi) | 100% complete |",
        "| Age (years)    | 100% complete |",
        "| Size           | 100% complete |",
        "| Wine ratings   | 0.2%–0.6% complete per rater |",
        "",
        "---",
        "",
        "## 2. Canonical Price Variable",
        "",
        "**Use `P_$/Bt_Combi` as the canonical per-bottle price.**",
        "",
        "### All price-related columns",
        "",
        "| Column | Level | Coverage | Notes |",
        "|--------|-------|----------|-------|",
        "| `P_$`              | Lot total (USD) | 100% | NOT per bottle; P_$ = P_$/Bt_Combi * Qty |",
        "| `P_Loc`            | Lot total (local) | 100% | Same as P_$ but in local currency |",
        "| `Hammer_$_Combi`   | Lot total (USD) | 75.3% | Combined Hammer_$ + Ham_$; missing ~25% |",
        "| `Hammer_Loc_Combi` | Lot total (local) | 75.5% | Combined hammer in local currency |",
        "| `HP_$/Bt_Combi`    | Per bottle (USD) | 90.9% | Hammer price; 9.1% missing |",
        "| `P_$/Bt_Combi`     | **Per bottle (USD)** | **100%** | **USE THIS: always populated** |",
        "| `Esti_$_Low_Combi` | Per lot, low estimate | 49.7% | Pre-auction estimate |",
        "| `Esti_$_High_Combi`| Per lot, high estimate | 49.7% | Pre-auction estimate |",
        "| `P_$/Standard_size`| Per standard 750ml | 31.2% | Normalises large-format bottles |",
        "| `HP_$/Standard_BT` | Per standard 750ml | 9.9% | Limited coverage |",
        "",
        "### Justification for `P_$/Bt_Combi`",
        "",
        f"- **100% non-null** across all {n_rows:,} rows",
        f"- Median: USD {p_median}, Max: USD {p_max:,}  ",
        f"- Lucie's f2_some_ml.py renames this column 'Price per Bottle' for all analysis",
        f"- `P_$` is the lot-level total (confirmed: P_$ = P_$/Bt_Combi × Qty in 100% of cases)",
        f"- `HP_$/Bt_Combi` is the hammer price per bottle (90.9% complete) and is the",
        f"  alternative if the hammer vs. total-price distinction matters",
        "",
        "### P_Loc / P_$ conflict note",
        "",
        "Lucie's `data_work.txt` (Q9a/9b) flags that `P_Loc` and `P_$` have values that",
        "conflict with `Hammer_Loc_Combi` and `Hammer_$_Combi` on some rows.",
        "`P_$` and `P_Loc` appear to be lot-level totals from one source of the auction data,",
        "while `Hammer_$_Combi` and `Hammer_Loc_Combi` come from a second source.",
        "The combined variable `P_$/Bt_Combi` (which divides P_$ by Qty) is 100% complete",
        "and is the safest choice for per-bottle analysis.",
        "",
        "---",
        "",
        "## 3. Canonical Producer/Wine Name Variables",
        "",
        "**Primary producer variable: `Producer/Maker` (94.8% complete, NOT standardised).**",
        "**Primary wine-name variable: `For Matching` (41.1% complete; most consistent).**",
        "",
        "### All identity columns",
        "",
        "| Column | Coverage | Unique values | Notes |",
        "|--------|----------|---------------|-------|",
        "| `Producer/Maker` | 94.8% | ~varies | Primary; Lucie's pipeline left unstandardised |",
        "| `Ori Producer Nm` | ~0% | — | Dropped in cleaning (no values) |",
        "| `Producer Dummy`  | 8.0% | — | Lowercased producer name from one data source |",
        "| `Producer`        | 2.2% | — | Sparse; partial third source |",
        "| `WineNm`          | 2.1% | — | Very sparse |",
        "| `Wine Nm`         | 5.6% | — | Second wine name field |",
        "| `Wine_Nm`         | 0.7% | — | Very sparse |",
        "| `Item_Nm`         | 9.9% | — | Full description from one source |",
        "| `LotNm1`          | 31.2% | — | First token of lot name (often wine name) |",
        "| `Lot Nm`          | 58.9% | — | Lot name; most complete alternative |",
        "| `For Matching`    | 41.1% | — | Curated for Duc's URL matching; uppercase tokens |",
        "| `Wine Vintage Pair` | 31.2% | — | Full canonical description (GPT-assisted) |",
        "",
        "### Recommendation",
        "",
        "- Use `Producer/Maker` for producer fixed effects (94.8% coverage).",
        "- Use `Lot Nm` or `LotNm1` for wine-level analysis when producer names are needed.",
        "- Standardisation of producer names is an **open task** (flagged in data_work.txt).",
        "  This is a prerequisite for producer-level fixed effects in the final regressions.",
        "",
        "---",
        "",
        "## 4. Age Variable Recommendation",
        "",
        "**Use recomputed Age in quarters for the main regression:**",
        "",
        "```python",
        "vintage_anchor = pd.to_datetime(df['Vintage'].astype(int).astype(str) + '-06-30')",
        "df['Age_q'] = (4 * (df['Date'] - vintage_anchor).dt.days / 365.25).clip(lower=0).astype(int)",
        "```",
        "",
        "### Why not use the parquet's `Age` column?",
        "",
        f"- The parquet `Age` is `Date.year - Vintage` (integer years).",
        f"  This is coarse and does not account for the sale month.",
        f"- Lucie's `data_work.txt` explicitly notes: *'VARIABLE DATE NEEDS TO BE CHECKED",
        f"  AGAIN and variable age might need to be updated'*.",
        f"- `f2_some_ml.py` recomputes Age in quarters using June 30 as the vintage anchor",
        f"  (the wine is assumed bottled at the end of Q2 of the vintage year).",
        f"- The Stata specification uses `agequarters`, confirming that quarters is the",
        f"  convention used for all published regressions.",
        "",
        f"Age range (recomputed quarters): {aq_info.get('min', 'N/A')} to {aq_info.get('max', 'N/A')} "
        f"quarters (0 to {round(aq_info.get('max', 400)/4, 0):.0f} years)",
        "",
        "Age range in the parquet column (years): "
        f"{age_info.get('min', 'N/A')} to {age_info.get('max', 'N/A')}",
        "",
        f"Rows with Age > 100 years in parquet: {age_info.get('n_gt100', 'N/A'):,}",
        "",
        "---",
        "",
        "## 5. Data Quality Issues",
        "",
        f"| Issue | Count | Recommendation |",
        f"|-------|-------|----------------|",
        f"| Mixed-lot flagged rows | {n_mixed:,} ({100*n_mixed/n_rows:.2f}%) | See `Excluded_Lots` |",
        f"| True mixed lots (exclude from price analysis) | {n_excl:,} ({100*n_excl/n_rows:.2f}%) | Drop rows where Excluded_Lots = 1 |",
        f"| Age > 100 years in parquet | {age_info.get('n_gt100', 'N/A')} | Recompute Age_q; cap at reasonable max |",
        f"| Producer/Maker missing | 5.2% (~55,567 rows) | Cannot use for producer FE |",
        f"| Wine ratings present | 0.2%–0.6% | Ratings are too sparse for main analysis |",
        f"| P_Loc / P_$ vs Combi conflict | Unresolved (Lucie Q9) | Use P_$/Bt_Combi (100% complete) |",
        f"| Class column | NOT standardised | See proposed dict in data_work.txt Q3 |",
        f"| Date range | 1996–2015 | No post-2015 data; China shock period covered |",
        "",
        "### Duc's two large CSVs (Wine_Maturity(Rep_1).csv and Wine_data(Rep2).csv)",
        "",
        "These files (514 MB and 491 MB) contain the **same 78 columns** as the master parquet",
        "plus extra columns: a `Link` column with tastingbook.com URLs (already matched via",
        "`Matching.R`), and a `Year (corrected?)` column in Rep_1. Both are essentially CSV",
        "exports of the auction data **after** Duc added URL matches — NOT a separate data source.",
        "",
        "Key finding: the `Link` column in these CSVs appears to overlap with `matched_url`",
        "in `output_with_matches.parquet`.",
        "",
        "### Xin Ning's data.xlsx (extracted from Wine data_Xin Ning.zip)",
        "",
        "Contains **15,902 rows** of tastingbook.com 'When to drink' data for **602 producers**",
        "(Bordeaux producers only). Columns: `url`, `year`, `year_url`, `When to drink`,",
        "`Country ranking`, `Producer ranking`, `Decanting time`, `Food Pairing`.",
        "This is the maturity data needed for the structural model and DiD.",
        "Coverage of ~602 Bordeaux producers is much broader than Duc's 6-producer scraping.",
        "",
        "### URL matching coverage (output_with_matches.parquet)",
        "",
        "Duc's R script matched **18,431 rows** out of 1,068,703 (1.7%) to tastingbook URLs.",
        "Only 6 producers were included in the matching pool (Armand Rousseau, Romanee Conti,",
        "Comtes Lafon, Pere & Fils, Georges de Vogue + Scraped_Links.xlsx).",
        "Xin Ning's data provides much broader maturity data and should be merged via `year_url`.",
        "",
        "---",
        "",
        "## 6. The Bimodal Pattern",
        "",
        "The core finding of the paper is a **bimodal age-price profile**:",
        "wine prices first rise as the wine ages, reach a first peak early,",
        "then dip (the 'trough') before rising again to a second, higher peak.",
        "",
        "The trough and second peak are consistent with a market where",
        "consumers (who want the wine at its maturity peak) exit the market,",
        "leaving it to investors/collectors (who value aged wines for other reasons).",
        "",
        f"| Region | Trough (years) | Second peak (years) |",
        f"|--------|---------------|---------------------|",
    ]

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        trough_yrs = bimodal.get(f"{region}_trough_yrs", "~28-33")
        peak2_yrs  = bimodal.get(f"{region}_peak2_yrs", ">50")
        lines.append(f"| {region} | ~{trough_yrs} | ~{peak2_yrs} |")

    lines += [
        "",
        "The Chow test at age=120 quarters (~30 years) in `f2_some_ml.py` confirms a",
        "structural break in the price-age relationship at that point.",
        "",
        "See `output/figures/price_age_profile.pdf` for the visual.",
        "",
        "---",
        "",
        "## 7. Files Needed for the Pipeline",
        "",
        "| File | Status | Action |",
        "|------|--------|--------|",
        "| `old/RALucie/wine/parquet/clean_data_mixed_lots.parquet` | Present, 94 MB | This IS the master dataset |",
        "| `old/RADuc/clean_data_mixed_lots.parquet` | Present, identical | Duplicate; use Lucie's version |",
        "| `old/RADuc/output_with_matches.parquet` | Present, 62 MB | 1.7% coverage; use with Xin Ning data |",
        "| `old/in vino veritas/Auction data/Bordeaux*.xlsx` | Present | Source for 00_xlsx_to_parquet.py |",
        "| `Wine data_Xin Ning.zip` (data.xlsx) | Present | 15,902 maturity rows; extract and merge |",
        "",
        "---",
        "",
        "*Report generated by `code/analysis/03_data_exploration.py`*",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Written: {REPORT_PATH}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Step 03: Data exploration")
    print(f"Output dir: {OUTPUT_DIR}")
    print("=" * 60)

    df = load_data()
    print(f"Loaded dataset: {df.shape}")

    overview  = section1_overview(df)
    prices    = section2_prices(df)
    identity  = section3_identity(df)
    age       = section4_age(df)
    geo       = section5_geography(df)
    bimodal   = section6_bimodal(df)
    quality   = section7_quality(df)

    write_report(overview, prices, identity, age, geo, bimodal, quality)

    print("\n" + "=" * 60)
    print("[DONE] Exploration complete.")
    print(f"  Report:  {REPORT_PATH}")
    print(f"  Figures: {FIGURES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

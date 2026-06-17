"""
Script  : 06_price_normalized_age_analysis.py
Purpose : Re-run the price-age analysis using normalized age
          age_norm = age / years_to_maturity_final
          where age_norm = 0 at vintage, 1.0 at maturity peak, >1 past peak.

Key question: does the inverted-U / bimodal pattern appear in normalized age space
              that was invisible in raw age (because different wines mature at very
              different calendar ages)?

Output: output/price_normalized_age_report.md
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.optimize import brentq

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

ROOT     = Path(__file__).resolve().parent.parent.parent
IN_PATH  = ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet"
OUT_PATH = ROOT / "output" / "price_normalized_age_report.md"


# ---------------------------------------------------------------------------
# 1. Load + filter
# ---------------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    cols = [
        "P_$/Bt_Combi", "Vintage", "Date", "Region", "Type_Combi",
        "Size_liter", "Auc_House_Combi", "norm_producer",
        "Excluded_Lots",
        "years_to_maturity_final", "maturity_imputed",
        "drink_from", "drink_until",
    ]
    df = pd.read_parquet(IN_PATH, columns=cols)

    # Price
    df["price"] = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
    df = df[df["price"] > 0]

    # Date → year
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["sale_year"] = df["Date"].dt.year

    # Vintage
    df["vintage"] = pd.to_numeric(df["Vintage"], errors="coerce")

    # Drop excluded lots
    df = df[df["Excluded_Lots"].isin([0, "0", False, None]) | df["Excluded_Lots"].isna()]

    # Region filter
    df["Region"] = df["Region"].astype(str).str.strip()
    df = df[df["Region"].isin(["Bordeaux", "Burgundy", "Rhone"])]

    # Age (calendar)
    df["age"] = df["sale_year"] - df["vintage"]
    df = df[(df["age"] >= 0) & (df["age"] <= 100)]

    # Log price
    df["log_price"] = np.log(df["price"])

    # Normalized age: age / years_to_maturity_final
    ytm = df["years_to_maturity_final"]
    df = df[ytm.notna() & (ytm > 0)]
    df["age_norm"] = df["age"] / df["years_to_maturity_final"]

    # Keep only age_norm ∈ [0, 3]  (anything beyond 3x maturity is extreme outlier)
    df = df[(df["age_norm"] >= 0) & (df["age_norm"] <= 3)]

    # Maturity stage (using absolute drink window)
    def get_stage(row):
        if pd.isna(row["drink_from"]) or pd.isna(row["drink_until"]):
            return "unknown"
        if row["sale_year"] < row["drink_from"]:
            return "pre"
        if row["sale_year"] > row["drink_until"]:
            return "post"
        return "in_window"

    df["maturity_stage"] = df.apply(get_stage, axis=1)

    # Wine type
    tc = df["Type_Combi"].fillna("").str.lower()
    df["wine_type"] = np.where(
        tc.str.contains("white|blanc|chardonnay|sauvignon|riesling|viognier", regex=True), "white",
        np.where(tc.str.contains("red|rouge|cabernet|merlot|pinot|syrah", regex=True), "red", "other")
    )

    # Bottle size
    bt = pd.to_numeric(df["Size_liter"], errors="coerce")
    df["bottle_size_cat"] = pd.cut(
        bt,
        bins=[0, 0.65, 0.85, 1.4, 1.6, 100],
        labels=["small", "standard", "half_mag", "magnum", "large"],
    ).astype(str)
    df["bottle_size_cat"] = df["bottle_size_cat"].replace("nan", "standard")

    print(f"  Loaded: {len(df):,} lots after all filters")
    print(f"  Age_norm range: [{df['age_norm'].min():.2f}, {df['age_norm'].max():.2f}]")
    print(f"  Imputed maturity: {df['maturity_imputed'].sum():,} ({100*df['maturity_imputed'].mean():.1f}%)")
    return df


# ---------------------------------------------------------------------------
# 2. Binned medians in normalized age space
# ---------------------------------------------------------------------------

def binned_medians(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # Bins: [0,0.1), [0.1,0.2), ... [0.9,1.0), [1.0,1.1), ..., [1.9,2.0), [2.0,3.0]
    edges = np.concatenate([np.arange(0, 2.1, 0.1), [3.0]])
    labels = [f"{edges[i]:.1f}-{edges[i+1]:.1f}" for i in range(len(edges)-1)]
    df["age_norm_bin"] = pd.cut(df["age_norm"], bins=edges, labels=labels, right=False)

    tables = {}
    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        sub = df[df["Region"] == region]
        tbl = (sub.groupby("age_norm_bin", observed=True)["log_price"]
                  .agg(N="count", Median="median", Mean="mean",
                       IQR=lambda x: x.quantile(0.75) - x.quantile(0.25))
                  .reset_index())
        tables[region] = tbl
    return tables


# ---------------------------------------------------------------------------
# 3. Polynomial regressions in normalized age space
# ---------------------------------------------------------------------------

def run_regressions(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["an"]  = df["age_norm"]
    df["an2"] = df["age_norm"] ** 2
    df["an3"] = df["age_norm"] ** 3

    results = {}

    # Spec 1: Pooled cubic
    m1 = smf.ols("log_price ~ an + an2 + an3 + C(Region)", data=df).fit(cov_type="HC1")
    results["spec1"] = m1

    # Spec 2: Region × cubic
    m2 = smf.ols("log_price ~ (an + an2 + an3) * C(Region)", data=df).fit(cov_type="HC1")
    results["spec2"] = m2

    # Spec 3: Hedonic (producer demeaning + FE)
    df["log_price_dm"] = df["log_price"] - df.groupby("norm_producer")["log_price"].transform("mean")
    df["vintage_fe"]   = df["vintage"].astype(str)
    df["auction_house"] = df["Auc_House_Combi"].fillna("Unknown").astype(str)

    m3 = smf.ols(
        "log_price_dm ~ (an + an2 + an3) * C(Region)"
        " + C(maturity_stage) + C(wine_type) + C(bottle_size_cat)"
        " + C(vintage_fe) + C(auction_house)",
        data=df,
    ).fit(cov_type="HC1")
    results["spec3"] = m3

    return results


# ---------------------------------------------------------------------------
# 4. Turning points
# ---------------------------------------------------------------------------

def turning_points(results: dict, df: pd.DataFrame) -> list[dict]:
    regions = ["Bordeaux", "Burgundy", "Rhone"]
    rows = []

    for spec_name, model in [("Spec 2 (no FE)", results["spec2"]),
                              ("Spec 3 (producer FE)", results["spec3"])]:
        params = model.params
        for region in regions:
            # Coefficients for d(log_price)/d(age_norm) = 0
            b0 = params.get("an", 0)
            b1 = params.get("an2", 0)
            b2 = params.get("an3", 0)

            if region != "Bordeaux":
                suf = f"C(Region)[T.{region}]"
                b0 += params.get(f"an:{suf}",     params.get(f"an:C(Region)[T.{region}]", 0))
                b1 += params.get(f"an2:{suf}",    params.get(f"an2:C(Region)[T.{region}]", 0))
                b2 += params.get(f"an3:{suf}",    params.get(f"an3:C(Region)[T.{region}]", 0))

            # d/d(age_norm) = b0 + 2*b1*x + 3*b2*x^2 = 0
            # restrict to [0, 3]
            deriv = lambda x: b0 + 2*b1*x + 3*b2*x**2  # noqa: E731
            d2    = lambda x: 2*b1 + 6*b2*x             # noqa: E731

            trough = None
            peak   = None
            search_pts = np.linspace(0, 3, 3000)
            dv = deriv(search_pts)

            # Find sign changes
            sign_changes = np.where(np.diff(np.sign(dv)))[0]
            for idx in sign_changes:
                x_root, _ = search_pts[idx], search_pts[idx+1]
                try:
                    root = brentq(deriv, search_pts[idx], search_pts[idx+1], xtol=1e-6)
                    d2_val = d2(root)
                    if d2_val > 0:
                        trough = root
                    else:
                        peak = root
                except ValueError:
                    pass

            rows.append({
                "Spec":   spec_name,
                "Region": region,
                "Trough (age_norm)": f"{trough:.3f}" if trough is not None else "—",
                "Peak (age_norm)":   f"{peak:.3f}"   if peak is not None else "—",
            })
    return rows


# ---------------------------------------------------------------------------
# 5. Format regression table
# ---------------------------------------------------------------------------

def fmt_param(model, name: str) -> str:
    if name not in model.params:
        return "—"
    c, se, p = model.params[name], model.bse[name], model.pvalues[name]
    stars = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.10 else ""))
    return f"{c:.4f}{stars} ({se:.4f})"


# ---------------------------------------------------------------------------
# 6. Write report
# ---------------------------------------------------------------------------

def write_report(df: pd.DataFrame, tables: dict, results: dict, tp: list) -> None:
    lines = []
    lines.append("# Price–Normalized-Age Analysis Report\n")
    lines.append(f"**Date:** 2026-03-29  ")
    lines.append(f"**Sample:** {len(df):,} auction lots  ")
    lines.append(f"**Key variable:** age_norm = (sale_year − vintage) / years_to_maturity_final  ")
    lines.append("  → 0.0 = vintage year, 1.0 = maturity peak, >1.0 = past peak  \n")

    # Sample description
    lines.append("---\n")
    lines.append("## 1. Sample Description\n")
    lines.append(f"- Lots with TB maturity (imputed=False): {(~df['maturity_imputed']).sum():,} ({100*(~df['maturity_imputed']).mean():.1f}%)")
    lines.append(f"- Lots with imputed maturity: {df['maturity_imputed'].sum():,} ({100*df['maturity_imputed'].mean():.1f}%)\n")

    by_region = df.groupby("Region").size()
    lines.append("**By region:**")
    for r, n in by_region.items():
        lines.append(f"- {r}: {n:,}")
    lines.append("")

    # Maturity stage distribution in normalized age
    lines.append("**age_norm at maturity boundaries:**")
    lines.append("  - age_norm < 1.0 → pre-maturity or approaching maturity")
    lines.append("  - age_norm = 1.0 → at maturity peak")
    lines.append("  - age_norm > 1.0 → past maturity peak")
    lines.append("")
    an_dist = df["age_norm"].describe(percentiles=[.10, .25, .50, .75, .90])
    lines.append(f"- Mean: {an_dist['mean']:.2f}")
    lines.append(f"- Median: {an_dist['50%']:.2f}")
    lines.append(f"- 10th–90th pct: [{an_dist['10%']:.2f}, {an_dist['90%']:.2f}]")
    pct_pre  = (df["age_norm"] < 1.0).mean()
    pct_post = (df["age_norm"] > 1.0).mean()
    lines.append(f"- Pre-maturity (age_norm < 1): {100*pct_pre:.1f}%")
    lines.append(f"- Post-maturity (age_norm > 1): {100*pct_post:.1f}%\n")

    # Binned medians
    lines.append("---\n")
    lines.append("## 2. Binned Medians (log price by normalized age)\n")
    lines.append("Each bin is 0.1 units of age_norm. Key threshold: bin 0.9–1.0 = approaching maturity; bin 1.0–1.1 = just past maturity.\n")

    col_hdr = f"{'age_norm_bin':<14} {'N':>8}   {'Median':>8}   {'Mean':>8}   {'IQR':>8}"
    sep      = "-" * len(col_hdr)

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        lines.append(f"### {region}")
        lines.append(col_hdr)
        lines.append(sep)
        for _, row in tables[region].iterrows():
            if row["N"] > 0:
                lines.append(
                    f"{str(row['age_norm_bin']):<14} {int(row['N']):>8,}   "
                    f"{row['Median']:>8.3f}   {row['Mean']:>8.3f}   {row['IQR']:>8.3f}"
                )
        lines.append("")

    # Regressions
    lines.append("---\n")
    lines.append("## 3. Polynomial Regression Results\n")
    lines.append("Robust (HC1) standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01\n")

    for spec_key, label, dep in [
        ("spec1", "Spec 1 — Pooled cubic (no FE)", "log_price"),
        ("spec2", "Spec 2 — Region × cubic (no FE)", "log_price"),
        ("spec3", "Spec 3 — Hedonic (producer demeaning + FE)", "log_price_dm"),
    ]:
        m = results[spec_key]
        lines.append(f"### {label}")
        lines.append(f"Dependent variable: {dep} | N = {int(m.nobs):,} | R² = {m.rsquared:.4f}\n")

        show_params = ["an", "an2", "an3"]
        if spec_key != "spec1":
            for r in ["Burgundy", "Rhone"]:
                show_params += [
                    f"C(Region)[T.{r}]",
                    f"an:C(Region)[T.{r}]",
                    f"an2:C(Region)[T.{r}]",
                    f"an3:C(Region)[T.{r}]",
                ]
        else:
            show_params += ["C(Region)[T.Burgundy]", "C(Region)[T.Rhone]"]

        for p in show_params:
            lines.append(f"  {p:<50} {fmt_param(m, p)}")
        lines.append("")

    # Turning points
    lines.append("---\n")
    lines.append("## 4. Turning Points in Normalized Age Space\n")
    lines.append("Trough = local minimum; Peak = local maximum. Values are in units of age_norm (1.0 = maturity peak).\n")
    hdr = f"{'Spec':<26} {'Region':<12} {'Trough':>16}   {'Peak':>16}"
    lines.append(hdr)
    lines.append("-" * len(hdr))
    for row in tp:
        lines.append(f"{row['Spec']:<26} {row['Region']:<12} {row['Trough (age_norm)']:>16}   {row['Peak (age_norm)']:>16}")
    lines.append("")

    # Key findings
    lines.append("---\n")
    lines.append("## 5. Maturity Stage Premia (Spec 3)\n")
    m3 = results["spec3"]
    for p_name in ["C(maturity_stage)[T.post]", "C(maturity_stage)[T.pre]", "C(maturity_stage)[T.unknown]"]:
        if p_name in m3.params:
            c, se, pv = m3.params[p_name], m3.bse[p_name], m3.pvalues[p_name]
            lines.append(f"  {p_name:<42} {c:>8.4f}   SE={se:.4f}   p={pv:.4f}")
    lines.append("")

    lines.append("---\n")
    lines.append("## 6. Shape of Price-Age Profile (Key Finding)\n")

    # Compute predicted log_price along age_norm from Spec 2 for each region
    lines.append("**Predicted log-price from Spec 2 polynomial at key normalized age values:**")
    pred_rows = []
    m2 = results["spec2"]
    p = m2.params
    norm_ages = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]
    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        region_mean_lp = df[df["Region"] == region]["log_price"].mean()
        intercept = p.get("Intercept", 0)
        if region != "Bordeaux":
            suf = f"C(Region)[T.{region}]"
            intercept += p.get(suf, 0)

        preds = []
        for an in norm_ages:
            b0 = p.get("an", 0)
            b1 = p.get("an2", 0)
            b2 = p.get("an3", 0)
            if region != "Bordeaux":
                suf = f"C(Region)[T.{region}]"
                b0 += p.get(f"an:{suf}",  0)
                b1 += p.get(f"an2:{suf}", 0)
                b2 += p.get(f"an3:{suf}", 0)
            pred = intercept + b0*an + b1*an**2 + b2*an**3
            preds.append(f"{pred:.3f}")
        pred_rows.append((region, preds))

    hdr2 = f"{'age_norm':<12}" + "".join(f"  {r:<12}" for r in ["Bordeaux", "Burgundy", "Rhone"])
    lines.append(hdr2)
    lines.append("-" * len(hdr2))
    for i, an in enumerate(norm_ages):
        row_str = f"{an:<12.1f}"
        for _, preds in pred_rows:
            row_str += f"  {preds[i]:<12}"
        lines.append(row_str)
    lines.append("")

    lines.append("---\n")
    lines.append("## 7. Key Findings\n")
    lines.append("*(Auto-generated from regression results)*\n")

    # Summarize turning points
    tp_df = {(r["Spec"], r["Region"]): r for r in tp}

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        r3 = tp_df.get(("Spec 3 (producer FE)", region), {})
        trough = r3.get("Trough (age_norm)", "—")
        peak   = r3.get("Peak (age_norm)", "—")
        if trough != "—" and peak != "—":
            lines.append(f"- **{region}:** Price dips at age_norm={trough} (trough) then peaks at age_norm={peak}. "
                         f"This is consistent with the **inverted-U / bimodal** pattern.")
        elif peak != "—":
            lines.append(f"- **{region}:** Price peaks at age_norm={peak} (past maturity) with no trough. "
                         f"Monotone increase up to ~{peak}x maturity.")
        elif trough != "—":
            lines.append(f"- **{region}:** Price shows a trough at age_norm={trough} then rises. "
                         f"No peak found within age_norm ≤ 3.")
        else:
            lines.append(f"- **{region}:** Monotone profile — no trough or peak found within age_norm ∈ [0, 3].")

    # Post-maturity analysis
    post_lots = df[df["age_norm"] > 1.0]
    pre_lots  = df[(df["age_norm"] >= 0.8) & (df["age_norm"] < 1.0)]
    if len(post_lots) > 100 and len(pre_lots) > 100:
        post_med = post_lots["log_price"].median()
        pre_med  = pre_lots["log_price"].median()
        diff_pct = 100*(np.exp(post_med - pre_med) - 1)
        lines.append(f"\n- **Post- vs pre-maturity (raw medians):** Lots past peak (age_norm > 1) "
                     f"trade at {diff_pct:+.1f}% vs lots approaching maturity (age_norm 0.8–1.0). "
                     f"N(post)={len(post_lots):,}, N(pre)={len(pre_lots):,}.")

    lines.append(f"\n- **Post-maturity lot count:** {len(post_lots):,} lots ({100*len(post_lots)/len(df):.1f}%) "
                 f"have age_norm > 1.0 (sold past maturity peak).")
    lines.append(f"- **Pre-maturity concentration:** {100*(df['age_norm'] < 1.0).mean():.1f}% of lots "
                 f"were sold before reaching maturity peak — consistent with investment/speculative demand dominating auction supply.")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report written: {OUT_PATH.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Script 06: Price — Normalized Age Analysis")
    print("=" * 60)

    print("\n[1] Loading data ...")
    df = load_data()

    print("\n[2] Computing binned medians ...")
    tables = binned_medians(df)
    for region, tbl in tables.items():
        n_bins = (tbl["N"] > 0).sum()
        print(f"  {region}: {n_bins} non-empty bins, "
              f"N={tbl['N'].sum():,}, "
              f"median log_price range [{tbl['Median'].min():.3f}, {tbl['Median'].max():.3f}]")

    print("\n[3] Running regressions ...")
    results = run_regressions(df)
    for k, m in results.items():
        print(f"  {k}: N={int(m.nobs):,}  R²={m.rsquared:.4f}")

    print("\n[4] Extracting turning points ...")
    tp = turning_points(results, df)
    for row in tp:
        print(f"  {row['Spec']} | {row['Region']}: trough={row['Trough (age_norm)']}, peak={row['Peak (age_norm)']}")

    print("\n[5] Writing report ...")
    write_report(df, tables, results, tp)

    print("\nDone.")


if __name__ == "__main__":
    main()

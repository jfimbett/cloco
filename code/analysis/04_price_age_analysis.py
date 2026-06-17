"""
Script  : 04_price_age_analysis.py
Purpose : Characterise how log price per bottle depends on wine age.
          Produces a text report with:
            1. Sample description
            2. Binned medians table (Region × age bin)
            3. Three polynomial regression specs
            4. Turning points by region
            5. Maturity stage, wine type, and bottle size premia

Output  : output/price_age_report.md
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.tools.sm_exceptions import ConvergenceWarning

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH   = ROOT / "data" / "processed" / "auction_with_maturity.parquet"
REPORT_PATH = ROOT / "output" / "price_age_report.md"


# ---------------------------------------------------------------------------
# 1. Load & filter
# ---------------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    print("Loading data ...", flush=True)
    cols = [
        "P_$/Bt_Combi", "Date", "Vintage", "Region",
        "Type_Combi", "Size_liter", "norm_producer",
        "Auc_House_Combi", "drink_from", "drink_until",
        "maturity_source", "Excluded_Lots",
    ]
    df = pd.read_parquet(DATA_PATH, columns=cols)

    # Filters
    df = df[df["Excluded_Lots"] != 1]
    df["P_$/Bt_Combi"] = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
    df = df[df["P_$/Bt_Combi"] > 0]
    df = df[df["Region"].isin(["Bordeaux", "Burgundy", "Rhone"])]

    # Core variables
    df["log_price"] = np.log(df["P_$/Bt_Combi"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["sale_year"] = df["Date"].dt.year
    df["Vintage"] = pd.to_numeric(df["Vintage"], errors="coerce")
    df = df.dropna(subset=["sale_year", "Vintage", "log_price"])
    df["age"] = (df["sale_year"] - df["Vintage"]).astype(int)
    df = df[(df["age"] >= 0) & (df["age"] <= 100)]

    df["age2"] = df["age"] ** 2
    df["age3"] = df["age"] ** 3

    # Maturity stage
    df["drink_from"]  = pd.to_numeric(df["drink_from"],  errors="coerce")
    df["drink_until"] = pd.to_numeric(df["drink_until"], errors="coerce")
    conditions = [
        df["drink_from"].isna() | df["drink_until"].isna(),
        df["sale_year"] < df["drink_from"],
        (df["sale_year"] >= df["drink_from"]) & (df["sale_year"] <= df["drink_until"]),
        df["sale_year"] > df["drink_until"],
    ]
    choices = ["unknown", "pre", "in_window", "post"]
    df["maturity_stage"] = np.select(conditions, choices, default="unknown")

    # Wine type
    tc = df["Type_Combi"].fillna("").str.lower()
    df["wine_type"] = np.where(
        tc.str.contains("white|blanc|chardonnay|sauvignon|riesling", regex=True), "white",
        np.where(tc.str.contains("red|rouge|cabernet|pinot|merlot|syrah|grenache", regex=True), "red",
                 "other")
    )

    # Bottle size category
    sz = df["Size_liter"].fillna(0.75)
    df["bottle_size_cat"] = pd.cut(
        sz,
        bins=[0, 0.65, 0.85, 1.4, 1.6, 100],
        labels=["small", "standard", "half_mag", "magnum", "large"],
        right=True,
    ).astype(str)
    df["bottle_size_cat"] = df["bottle_size_cat"].replace("nan", "standard")

    # Vintage FE (string)
    df["vintage_fe"] = df["Vintage"].astype(int).astype(str)

    # Auction house (clean)
    df["auction_house"] = df["Auc_House_Combi"].fillna("Unknown")

    print(f"  Final sample: {len(df):,} rows")
    return df


# ---------------------------------------------------------------------------
# 2. Descriptive: binned medians
# ---------------------------------------------------------------------------

def binned_medians(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df["age_bin"] = pd.cut(df["age"], bins=list(range(0, 62, 2)) + [100],
                           labels=[f"{i}-{i+2}" for i in range(0, 60, 2)] + ["60+"],
                           right=False)

    # Table 1: Region × age_bin
    t1 = (df.groupby(["Region", "age_bin"], observed=True)["log_price"]
          .agg(N="count", median="median", mean="mean",
               p25=lambda x: x.quantile(0.25), p75=lambda x: x.quantile(0.75))
          .reset_index())
    t1["IQR"] = t1["p75"] - t1["p25"]

    # Table 2: Region × maturity_stage
    t2 = (df.groupby(["Region", "maturity_stage"], observed=True)["log_price"]
          .agg(N="count", median="median", mean="mean").reset_index())

    # Table 3: Region × wine_type (aggregate, not by age)
    t3 = (df.groupby(["Region", "wine_type"], observed=True)["log_price"]
          .agg(N="count", median="median", mean="mean").reset_index())

    return t1, t2, t3


# ---------------------------------------------------------------------------
# 3. Polynomial regressions
# ---------------------------------------------------------------------------

def fit_regressions(df: pd.DataFrame) -> dict:
    results = {}

    # --- Spec 1: Pooled cubic, region dummies ---
    print("  Fitting Spec 1 (pooled cubic) ...", flush=True)
    m1 = smf.ols("log_price ~ age + age2 + age3 + C(Region)", data=df).fit(cov_type="HC1")
    results["spec1"] = m1

    # --- Spec 2: Region × cubic interactions ---
    print("  Fitting Spec 2 (region × cubic) ...", flush=True)
    m2 = smf.ols("log_price ~ (age + age2 + age3) * C(Region)", data=df).fit(cov_type="HC1")
    results["spec2"] = m2

    # --- Spec 3: Producer within-demeaned + controls ---
    print("  Demeaning for producer FE ...", flush=True)
    df = df.copy()
    producer_means = df.groupby("norm_producer")["log_price"].transform("mean")
    df["log_price_dm"] = df["log_price"] - producer_means

    print("  Fitting Spec 3 (hedonic + producer FE via demeaning) ...", flush=True)
    # Limit vintage FEs to vintages with >= 50 observations
    vc = df["vintage_fe"].value_counts()
    valid_vintages = vc[vc >= 50].index
    df["vintage_fe_"] = df["vintage_fe"].where(df["vintage_fe"].isin(valid_vintages), "other")

    m3 = smf.ols(
        "log_price_dm ~ (age + age2 + age3) * C(Region)"
        " + C(maturity_stage) + C(wine_type) + C(bottle_size_cat)"
        " + C(vintage_fe_) + C(auction_house)",
        data=df,
    ).fit(cov_type="HC1")
    results["spec3"] = m3
    results["df_spec3"] = df  # save demeaned df for later use

    return results


# ---------------------------------------------------------------------------
# 4. Turning point extraction
# ---------------------------------------------------------------------------

def turning_points(coefs: dict[str, float], label: str) -> dict:
    """
    Given β1 (age), β2 (age²), β3 (age³), solve dP/dage = β1 + 2β2*age + 3β3*age² = 0.
    Returns real roots in [0, 100].
    """
    b1 = coefs.get("b1", 0)
    b2 = coefs.get("b2", 0)
    b3 = coefs.get("b3", 0)

    if abs(b3) < 1e-12:
        # Quadratic case
        if abs(b2) < 1e-12:
            return {"label": label, "roots": [], "trough": None, "peak": None}
        root = -b1 / (2 * b2)
        roots = [root] if 0 <= root <= 100 else []
    else:
        # Cubic derivative is quadratic
        # 3β3·x² + 2β2·x + β1 = 0
        a, b, c = 3 * b3, 2 * b2, b1
        disc = b ** 2 - 4 * a * c
        if disc < 0:
            roots = []
        else:
            r1 = (-b + np.sqrt(disc)) / (2 * a)
            r2 = (-b - np.sqrt(disc)) / (2 * a)
            roots = sorted([r for r in [r1, r2] if 0 <= r <= 100])

    # Classify as trough (2nd deriv > 0) or peak (2nd deriv < 0)
    trough, peak = None, None
    for r in roots:
        second_deriv = 2 * b2 + 6 * b3 * r
        if second_deriv > 0:
            trough = round(r, 1)
        else:
            peak = round(r, 1)

    return {"label": label, "roots": [round(r, 1) for r in roots],
            "trough": trough, "peak": peak}


def extract_turning_points(results: dict) -> list[dict]:
    rows = []

    # Spec 2: region-specific polynomials
    m2 = results["spec2"]
    params = m2.params

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        if region == "Bordeaux":
            # Bordeaux is the base category in C(Region)
            b1 = params.get("age", 0)
            b2 = params.get("age2", 0)
            b3 = params.get("age3", 0)
        else:
            b1 = params.get("age", 0) + params.get(f"age:C(Region)[T.{region}]", 0)
            b2 = params.get("age2", 0) + params.get(f"age2:C(Region)[T.{region}]", 0)
            b3 = params.get("age3", 0) + params.get(f"age3:C(Region)[T.{region}]", 0)

        tp = turning_points({"b1": b1, "b2": b2, "b3": b3}, f"Spec2 {region}")
        rows.append({"spec": "Spec 2 (no FE)", "region": region,
                     "trough_age": tp["trough"], "peak_age": tp["peak"]})

    # Spec 3: same structure on demeaned outcome
    m3 = results["spec3"]
    params3 = m3.params

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        if region == "Bordeaux":
            b1 = params3.get("age", 0)
            b2 = params3.get("age2", 0)
            b3 = params3.get("age3", 0)
        else:
            b1 = params3.get("age", 0) + params3.get(f"age:C(Region)[T.{region}]", 0)
            b2 = params3.get("age2", 0) + params3.get(f"age2:C(Region)[T.{region}]", 0)
            b3 = params3.get("age3", 0) + params3.get(f"age3:C(Region)[T.{region}]", 0)

        tp = turning_points({"b1": b1, "b2": b2, "b3": b3}, f"Spec3 {region}")
        rows.append({"spec": "Spec 3 (producer FE)", "region": region,
                     "trough_age": tp["trough"], "peak_age": tp["peak"]})

    return rows


# ---------------------------------------------------------------------------
# 5. Format helpers
# ---------------------------------------------------------------------------

def fmt_coef(val: float, se: float, pval: float) -> str:
    stars = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.10 else ""
    return f"{val:.4f}{stars} ({se:.4f})"


def coef_table_lines(model, params_of_interest: list[str]) -> list[str]:
    lines = []
    for p in params_of_interest:
        if p in model.params:
            lines.append(f"  {p:<55} {fmt_coef(model.params[p], model.bse[p], model.pvalues[p])}")
    return lines


def predicted_at_ages(model, region: str, ages: list[int],
                      extra_params: dict | None = None) -> list[float]:
    """Evaluate the cubic polynomial at given ages for a region."""
    pars = model.params
    base = region == "Bordeaux"
    preds = []
    for a in ages:
        a2, a3 = a ** 2, a ** 3
        if base:
            val = (pars.get("Intercept", 0)
                   + pars.get("age", 0) * a
                   + pars.get("age2", 0) * a2
                   + pars.get("age3", 0) * a3)
        else:
            val = (pars.get("Intercept", 0)
                   + pars.get(f"C(Region)[T.{region}]", 0)
                   + (pars.get("age", 0) + pars.get(f"age:C(Region)[T.{region}]", 0)) * a
                   + (pars.get("age2", 0) + pars.get(f"age2:C(Region)[T.{region}]", 0)) * a2
                   + (pars.get("age3", 0) + pars.get(f"age3:C(Region)[T.{region}]", 0)) * a3)
        preds.append(round(val, 3))
    return preds


# ---------------------------------------------------------------------------
# 6. Write report
# ---------------------------------------------------------------------------

def write_report(df: pd.DataFrame, t1: pd.DataFrame, t2: pd.DataFrame,
                 t3: pd.DataFrame, results: dict, tp_rows: list[dict]) -> None:

    m1, m2, m3 = results["spec1"], results["spec2"], results["spec3"]
    lines = []

    # ---- Header ----
    lines += [
        "# Price-Age Analysis Report",
        "",
        f"**Date:** 2026-03-29  ",
        f"**Sample:** {len(df):,} auction lots (after filters)  ",
        f"**Price variable:** log(P_$/Bt_Combi)  ",
        f"**Age variable:** sale_year − vintage (integer years, 0–100)  ",
        "",
        "---",
        "",
    ]

    # ---- 1. Sample description ----
    lines += ["## 1. Sample Description", ""]
    region_counts = df.groupby("Region").size().reset_index(name="N")
    lines.append("**By region:**")
    for _, r in region_counts.iterrows():
        lines.append(f"- {r['Region']}: {r['N']:,}")
    lines.append("")

    type_counts = df.groupby(["Region", "wine_type"]).size().unstack(fill_value=0)
    lines.append("**By region × wine type:**")
    lines.append(f"{'Region':<12} {'red':>10} {'white':>10} {'other':>10}")
    for reg in ["Bordeaux", "Burgundy", "Rhone"]:
        row = type_counts.loc[reg] if reg in type_counts.index else {}
        lines.append(f"{reg:<12} {row.get('red', 0):>10,} {row.get('white', 0):>10,} {row.get('other', 0):>10,}")
    lines.append("")

    stage_counts = df.groupby(["Region", "maturity_stage"]).size().unstack(fill_value=0)
    lines.append("**By region × maturity stage (lots with maturity data only):**")
    stages = ["pre", "in_window", "post", "unknown"]
    header = f"{'Region':<12}" + "".join(f"{s:>12}" for s in stages)
    lines.append(header)
    for reg in ["Bordeaux", "Burgundy", "Rhone"]:
        row = stage_counts.loc[reg] if reg in stage_counts.index else {}
        line = f"{reg:<12}" + "".join(f"{row.get(s, 0):>12,}" for s in stages)
        lines.append(line)
    lines.append("")

    size_counts = df.groupby("bottle_size_cat").size().sort_values(ascending=False)
    lines.append("**By bottle size:**")
    for cat, n in size_counts.items():
        lines.append(f"- {cat}: {n:,} ({100*n/len(df):.1f}%)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 2. Binned medians ----
    lines += ["## 2. Binned Medians (log price per bottle)", ""]
    lines.append("Median log-price by region and 2-year age bin. "
                 "Log-price is log(USD per bottle).")
    lines.append("")

    for region in ["Bordeaux", "Burgundy", "Rhone"]:
        sub = t1[t1["Region"] == region].copy()
        lines.append(f"### {region}")
        lines.append(f"{'Age bin':<10} {'N':>8} {'Median':>8} {'Mean':>8} {'IQR':>8}")
        lines.append("-" * 46)
        for _, row in sub.iterrows():
            if row["N"] >= 10:
                lines.append(
                    f"{str(row['age_bin']):<10} {row['N']:>8,} "
                    f"{row['median']:>8.3f} {row['mean']:>8.3f} {row['IQR']:>8.3f}"
                )
        lines.append("")

    # Predicted log-price at key ages from Spec 2 (for narrative context)
    key_ages = [2, 5, 10, 15, 20, 30, 40, 50, 60]
    lines.append("**Predicted log-price from Spec 2 polynomial at key ages:**")
    lines.append(f"{'Age':<6}" + "".join(f"{r:>12}" for r in ["Bordeaux", "Burgundy", "Rhone"]))
    lines.append("-" * 42)
    for a in key_ages:
        preds = {r: predicted_at_ages(m2, r, [a])[0] for r in ["Bordeaux", "Burgundy", "Rhone"]}
        lines.append(f"{a:<6}" + "".join(f"{preds[r]:>12.3f}" for r in ["Bordeaux", "Burgundy", "Rhone"]))
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 3. Regression results ----
    lines += ["## 3. Polynomial Regression Results", ""]
    lines.append("Robust (HC1) standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01")
    lines.append("")

    # Spec 1
    lines.append("### Spec 1 — Pooled cubic (no fixed effects)")
    lines.append(f"Dependent variable: log_price | N = {int(m1.nobs):,} | R² = {m1.rsquared:.4f}")
    lines.append("")
    spec1_params = ["age", "age2", "age3", "C(Region)[T.Burgundy]", "C(Region)[T.Rhone]"]
    lines += coef_table_lines(m1, spec1_params)
    lines.append("")

    # Spec 2
    lines.append("### Spec 2 — Region × cubic interactions (no fixed effects)")
    lines.append(f"Dependent variable: log_price | N = {int(m2.nobs):,} | R² = {m2.rsquared:.4f}")
    lines.append("")
    spec2_params = [
        "age", "age2", "age3",
        "C(Region)[T.Burgundy]", "C(Region)[T.Rhone]",
        "age:C(Region)[T.Burgundy]", "age:C(Region)[T.Rhone]",
        "age2:C(Region)[T.Burgundy]", "age2:C(Region)[T.Rhone]",
        "age3:C(Region)[T.Burgundy]", "age3:C(Region)[T.Rhone]",
    ]
    lines += coef_table_lines(m2, spec2_params)
    lines.append("")

    # Spec 3
    lines.append("### Spec 3 — Hedonic: producer within-demeaning + vintage + auction house FE")
    lines.append(f"Dependent variable: log_price (producer-demeaned) | N = {int(m3.nobs):,} | R² = {m3.rsquared:.4f}")
    lines.append("")
    spec3_core = [
        "age", "age2", "age3",
        "C(Region)[T.Burgundy]", "C(Region)[T.Rhone]",
        "age:C(Region)[T.Burgundy]", "age:C(Region)[T.Rhone]",
        "age2:C(Region)[T.Burgundy]", "age2:C(Region)[T.Rhone]",
        "age3:C(Region)[T.Burgundy]", "age3:C(Region)[T.Rhone]",
    ]
    lines += coef_table_lines(m3, spec3_core)
    lines.append("")
    lines.append("*Maturity stage, wine type, bottle size, vintage FE, and auction house FE included but not shown above.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 4. Turning points ----
    lines += ["## 4. Turning Points by Region", ""]
    lines.append("Price trough = age where d(log_price)/d(age) = 0 and 2nd derivative > 0 (local minimum).")
    lines.append("Price peak = age where d(log_price)/d(age) = 0 and 2nd derivative < 0 (local maximum).")
    lines.append("All roots restricted to age ∈ [0, 100].")
    lines.append("")
    lines.append(f"{'Spec':<25} {'Region':<12} {'Trough (yrs)':>14} {'Peak (yrs)':>12}")
    lines.append("-" * 66)
    for row in tp_rows:
        t = str(row["trough_age"]) if row["trough_age"] is not None else "—"
        p = str(row["peak_age"]) if row["peak_age"] is not None else "—"
        lines.append(f"{row['spec']:<25} {row['region']:<12} {t:>14} {p:>12}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 5. Maturity stage premia ----
    lines += ["## 5. Maturity Stage Premia (Spec 3)", ""]
    lines.append("Coefficients relative to baseline stage (pre-maturity).")
    lines.append("")
    maturity_params = [k for k in m3.params.index if "maturity_stage" in k]
    if maturity_params:
        lines.append(f"{'Parameter':<50} {'Coef':>10} {'SE':>10} {'p-val':>10}")
        lines.append("-" * 82)
        for p in maturity_params:
            lines.append(
                f"{p:<50} {m3.params[p]:>10.4f} {m3.bse[p]:>10.4f} {m3.pvalues[p]:>10.4f}"
            )
    else:
        lines.append("*(No maturity stage coefficients — all lots may be pre-maturity)*")
    lines.append("")

    # ---- 6. Wine type and bottle size premia ----
    lines += ["## 6. Wine Type and Bottle Size Premia (Spec 3)", ""]
    lines.append("**Wine type** (relative to 'other'):")
    type_params = [k for k in m3.params.index if "wine_type" in k]
    for p in type_params:
        lines.append(f"  {p:<50} {fmt_coef(m3.params[p], m3.bse[p], m3.pvalues[p])}")
    lines.append("")
    lines.append("**Bottle size** (relative to 'half_mag' or first category):")
    size_params = [k for k in m3.params.index if "bottle_size_cat" in k]
    for p in size_params:
        lines.append(f"  {p:<50} {fmt_coef(m3.params[p], m3.bse[p], m3.pvalues[p])}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ---- 7. Key findings ----
    lines += ["## 7. Key Findings", ""]
    lines.append("*(Auto-generated from regression results)*")
    lines.append("")

    # Find Bordeaux trough and peak from Spec 3
    spec3_tp = {r["region"]: r for r in tp_rows if "Spec 3" in r["spec"]}
    for reg in ["Bordeaux", "Burgundy", "Rhone"]:
        tp = spec3_tp.get(reg, {})
        trough = tp.get("trough_age")
        peak   = tp.get("peak_age")
        if trough and peak:
            lines.append(
                f"- **{reg}:** Price reaches a local minimum at ~{trough} years "
                f"and a local maximum at ~{peak} years of age (Spec 3)."
            )
        elif trough:
            lines.append(f"- **{reg}:** Price reaches a local minimum at ~{trough} years (no second peak within age 0–100).")
        elif peak:
            lines.append(f"- **{reg}:** Price reaches a local maximum at ~{peak} years (no trough within age 0–100).")
        else:
            lines.append(f"- **{reg}:** No turning points found within age 0–100 (monotone profile).")

    lines.append("")

    # Maturity stage finding
    in_window = m3.params.get("C(maturity_stage)[T.in_window]")
    post      = m3.params.get("C(maturity_stage)[T.post]")
    if in_window is not None:
        direction = "premium" if in_window > 0 else "discount"
        lines.append(
            f"- **Maturity stage:** Lots sold in their drinking window command a "
            f"{abs(in_window)*100:.1f}% {direction} vs pre-maturity lots "
            f"(exp(coef)={np.exp(in_window):.3f}), after controlling for age and producer."
        )
    if post is not None:
        direction = "premium" if post > 0 else "discount"
        lines.append(
            f"- **Post-maturity:** Lots sold past their peak drinking window trade at a "
            f"{abs(post)*100:.1f}% {direction} vs pre-maturity lots."
        )

    # Wine type
    red_coef = m3.params.get("C(wine_type)[T.red]")
    white_coef = m3.params.get("C(wine_type)[T.white]")
    if red_coef is not None and white_coef is not None:
        lines.append(
            f"- **Wine type:** Red wines trade at exp({red_coef:.3f})={np.exp(red_coef):.3f}x "
            f"relative to other; white at exp({white_coef:.3f})={np.exp(white_coef):.3f}x."
        )

    # Magnum premium
    mag_coef = m3.params.get("C(bottle_size_cat)[T.magnum]")
    if mag_coef is not None:
        lines.append(
            f"- **Magnum premium:** Magnums trade at a {abs(mag_coef)*100:.1f}% "
            f"{'premium' if mag_coef > 0 else 'discount'} per bottle vs standard (exp={np.exp(mag_coef):.3f})."
        )

    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report written → {REPORT_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Script 04: Price-Age Analysis")
    print("=" * 60)

    df = load_data()

    print("\n[1] Computing binned medians ...")
    t1, t2, t3 = binned_medians(df)

    print("\n[2] Fitting regressions ...")
    results = fit_regressions(df)

    print("\n[3] Extracting turning points ...")
    tp_rows = extract_turning_points(results)

    print("\n[4] Writing report ...")
    df_spec3 = results.pop("df_spec3")
    write_report(df_spec3, t1, t2, t3, results, tp_rows)

    print("\nDone.")


if __name__ == "__main__":
    main()

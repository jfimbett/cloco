"""
Script  : 10_structural_moments.py
Purpose : Extract fine-grained (8-bin) moment conditions and full 7x7 HC1
          covariance matrix from the auction data for structural estimation.

          Replaces the 5-segment coarse moments used in initial estimation
          with 7 non-baseline moments (8 bins, young as baseline), giving
          7 moments vs 5 free parameters in fix_lambda spec → 2 df overidentification.

Output  : output/structural_moments_fine.json
          {category: {moments, vcov, bin_midpoints, bin_labels, bin_n, N}}
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent.parent
PARQUET = ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet"
OUT = ROOT / "output" / "structural_moments_fine.json"

# ---------------------------------------------------------------------------
# Bin definitions: 8 bins, "young" is Treatment baseline
# ---------------------------------------------------------------------------

BINS = [
    ("young",    0.0,  0.4, 0.20),
    ("pre1",     0.4,  0.8, 0.60),
    ("pre2",     0.8,  1.0, 0.90),
    ("peak1",    1.0,  1.4, 1.20),
    ("peak2",    1.4,  1.6, 1.50),
    ("trough",   1.6,  2.0, 1.80),
    ("antique1", 2.0,  2.5, 2.25),
    ("antique2", 2.5,  3.1, 2.75),  # upper bound 3.1 to include a*<=3.0
]

BIN_LABELS    = [b[0] for b in BINS]
BIN_MIDPOINTS = {b[0]: b[3] for b in BINS}
NON_BASELINE  = [b[0] for b in BINS if b[0] != "young"]  # 7 labels


def assign_bin(age_norm: pd.Series) -> pd.Series:
    """Assign each observation to a bin label."""
    bins_lo  = [b[1] for b in BINS]
    bins_hi  = [b[2] for b in BINS]
    labels   = [b[0] for b in BINS]
    result   = pd.Series("other", index=age_norm.index, dtype=object)
    for lo, hi, lab in zip(bins_lo, bins_hi, labels):
        mask = (age_norm >= lo) & (age_norm < hi)
        result[mask] = lab
    return result


# ---------------------------------------------------------------------------
# Load and filter data
# ---------------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET)
    df["price"]    = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
    df             = df[df["price"] > 0]
    df["Date"]     = pd.to_datetime(df["Date"], errors="coerce")
    df["sale_year"]= df["Date"].dt.year
    df["vintage"]  = pd.to_numeric(df["Vintage"], errors="coerce")
    df             = df[df["Excluded_Lots"].isin([0, "0", False, None]) | df["Excluded_Lots"].isna()]
    df["Region"]   = df["Region"].astype(str).str.strip()
    df             = df[df["Region"].isin(["Bordeaux", "Burgundy"])]
    df["age"]      = df["sale_year"] - df["vintage"]
    df             = df[(df["age"] >= 0) & (df["age"] <= 100)]
    df["log_price"]= np.log(df["price"])
    df             = df[df["years_to_maturity_final"].notna() & (df["years_to_maturity_final"] > 0)]
    df["age_norm"] = df["age"] / df["years_to_maturity_final"]
    df             = df[(df["age_norm"] >= 0) & (df["age_norm"] <= 3)]

    # Wine type
    tc = df["Type_Combi"].fillna("").str.lower()
    df["wine_type"] = np.where(
        tc.str.contains("white|blanc|chardonnay|sauvignon|riesling|viognier", regex=True),
        "white", "red"
    )
    return df


def build_masks(df: pd.DataFrame) -> dict:
    gcc_kw = ["Premier Cru Class", "Deuxi", "Troisi", "Quatri", "Cinqui",
              "Cru Class", "grands cru"]
    return {
        "Bordeaux Grand Cru (red)": (
            df["Region"].eq("Bordeaux") &
            df["Class"].apply(lambda c: any(k in str(c) for k in gcc_kw)) &
            df["wine_type"].eq("red")
        ),
        "Burgundy Grand Cru": (
            df["Region"].eq("Burgundy") &
            df["Class"].astype(str).str.contains("Grand Cru_Burgundy", na=False)
        ),
        "Burgundy Premier Cru": (
            df["Region"].eq("Burgundy") &
            df["Class"].astype(str).str.contains("Premier Cru_Burgundy", na=False)
        ),
    }


# ---------------------------------------------------------------------------
# Extract moments and HC1 VCV for one group
# ---------------------------------------------------------------------------

def extract_moments(sub: pd.DataFrame, group_name: str) -> dict:
    """Run 8-bin segment regression, return moments + full VCV."""
    sub = sub.copy()
    sub["bin8"] = assign_bin(sub["age_norm"])
    # Keep only observations in defined bins
    sub = sub[sub["bin8"].isin(BIN_LABELS)]

    bin_n = sub.groupby("bin8")["log_price"].count().to_dict()

    # Drop bins with fewer than 30 observations (not enough for inference)
    active_bins = [b for b in BIN_LABELS if bin_n.get(b, 0) >= 30]
    sub = sub[sub["bin8"].isin(active_bins)]
    non_baseline_active = [b for b in NON_BASELINE if b in active_bins]

    if len(non_baseline_active) < 4:
        raise ValueError(f"{group_name}: only {len(non_baseline_active)} non-baseline bins have N>=30")

    print(f"  {group_name}: N={len(sub):,}  active bins: {active_bins}")
    for b in active_bins:
        print(f"    {b:<12}: N={bin_n.get(b,0):>7,}")

    # OLS with HC1
    formula = 'log_price ~ C(bin8, Treatment("young"))'
    m = smf.ols(formula, data=sub).fit(cov_type="HC1")

    # Extract coefficients and VCV for non-baseline bins
    coef = np.array([
        m.params[f'C(bin8, Treatment("young"))[T.{b}]']
        for b in non_baseline_active
    ])

    # Full VCV submatrix for non-baseline bins
    param_names = [f'C(bin8, Treatment("young"))[T.{b}]' for b in non_baseline_active]
    vcov = m.cov_params().loc[param_names, param_names].values

    # Midpoints for non-baseline active bins
    midpoints = [BIN_MIDPOINTS[b] for b in non_baseline_active]

    # Effective N for J-test scaling (use harmonic mean of bin Ns)
    ns = [bin_n.get(b, 0) for b in non_baseline_active]
    n_eff = len(ns) / sum(1.0 / n for n in ns if n > 0)

    return {
        "moments":       coef.tolist(),
        "vcov":          vcov.tolist(),
        "bin_labels":    non_baseline_active,
        "bin_midpoints": midpoints,
        "bin_n":         {b: int(bin_n.get(b, 0)) for b in active_bins},
        "N":             int(len(sub)),
        "N_eff":         float(n_eff),
        "n_moments":     len(non_baseline_active),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Script 10: Structural Moments Extraction (8-bin fine)")
    print("=" * 60)

    print("\nLoading data ...")
    df = load_data()
    masks = build_masks(df)

    results = {}
    for group_name, mask in masks.items():
        print(f"\n[{group_name}]")
        sub = df[mask].copy()
        results[group_name] = extract_moments(sub, group_name)

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {OUT}")

    # Sanity: print moment values vs SEs
    print("\nMoment summary:")
    for cat, res in results.items():
        print(f"\n  {cat}")
        print(f"  {'Bin':<12}  {'Coef':>8}  {'SE':>8}  {'t-stat':>8}")
        vcov = np.array(res["vcov"])
        ses  = np.sqrt(np.diag(vcov))
        for i, (lab, coef, se) in enumerate(zip(res["bin_labels"], res["moments"], ses)):
            t = coef / se if se > 0 else float("nan")
            print(f"  {lab:<12}  {coef:8.4f}  {se:8.4f}  {t:8.2f}")


if __name__ == "__main__":
    main()

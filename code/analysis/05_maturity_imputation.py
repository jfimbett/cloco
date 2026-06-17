"""
Script  : 05_maturity_imputation.py
Purpose : Predict years_to_maturity for auction lots without Tastingbook coverage.

Strategy:
  1. Train a GradientBoostingRegressor on all 17k Tastingbook observations
     Features: producer (target-encoded), wine_type, region, vintage
  2. Cross-validate → report OOS R²
  3. Impute for the 24% of auction lots with maturity_source == 'unmatched'
  4. Cap years_to_maturity_final at YTM_CAP for all lots (TB and imputed)
     Rationale: TB recommendations for very old/obscure vintages anchor to the
     current year (2026), inflating YTM to implausible values.  A cap of 20 yrs
     is a conservative, defensible upper bound for this auction sample.
  5. Write augmented parquet: data/processed/auction_with_maturity_imputed.parquet

Output columns added:
  years_to_maturity_imputed  — model prediction (all lots), capped at YTM_CAP
  years_to_maturity_final    — TB value if matched, model if unmatched; capped at YTM_CAP
  maturity_imputed           — True if this lot used the model
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

ROOT       = Path(__file__).resolve().parent.parent.parent
TB_PATH    = ROOT / "data" / "raw" / "tastingbook_rescrape" / "data_combined.xlsx"
AUCTION_IN = ROOT / "data" / "processed" / "auction_with_maturity.parquet"
OUT_PATH   = ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet"

# Conservative cap on years_to_maturity (applied to both TB values and model predictions).
# TB recommendations for old vintages anchor to the current year, inflating YTM.
# 20 years is a defensible upper bound for peak maturity across this auction sample.
YTM_CAP = 20


# ---------------------------------------------------------------------------
# 1. Load and prepare Tastingbook training data
# ---------------------------------------------------------------------------

def load_tb() -> pd.DataFrame:
    tb = pd.read_excel(TB_PATH)

    # Parse producer slug from URL
    tb["producer_slug"] = tb["url"].str.extract(r"tastingbook\.com/wine/([^/]+)/")
    tb["vintage"]       = pd.to_numeric(
        tb["url"].str.extract(r"_(\d{4})$")[0], errors="coerce"
    )

    # Normalise drink window columns
    for col in ["drink_from", "drink_until"]:
        tb[col] = pd.to_numeric(tb[col], errors="coerce")

    tb["maturity_peak"]    = (tb["drink_from"] + tb["drink_until"]) / 2
    tb["years_to_maturity"] = tb["maturity_peak"] - tb["vintage"]

    # Filter: need vintage + maturity
    tb = tb.dropna(subset=["years_to_maturity", "vintage"])
    tb = tb[tb["vintage"] > 1800]

    # Cap extremes
    tb = tb[(tb["years_to_maturity"] >= 2) & (tb["years_to_maturity"] <= 100)]

    # Region: derive from producer slug prefix patterns
    tb["region"] = np.select(
        [
            tb["producer_slug"].str.contains("chateau|bord|medoc|sauternes|pomerol|st_emilion|margaux|pauillac|stestephe|graves|entre|cotes|blaye|bourg|fronsac|moulis|listrac", na=False),
            tb["producer_slug"].str.contains("domaine|bourgogne|chablis|beaune|gevrey|nuits|vosne|chambolle|morey|pommard|volnay|meursault|puligny|chassagne|cote_de|maranges|ladoix|auxey|monthelie|saint_aubin|santenay|marsannay|fixin|aloxe|savigny|chorey|rully|mercurey|givry|montagny", na=False),
            tb["producer_slug"].str.contains("hermitage|chateauneuf|crozeshermitage|cornas|saintjoseph|vacqueyras|gigondas|lirac|tavel|coteaux|luberon|ventoux|grenache|mourvedre|rhone", na=False),
        ],
        ["Bordeaux", "Burgundy", "Rhone"],
        default="Other",
    )

    # Wine type: from wine_slug
    ws = tb["wine_slug"].fillna("").str.lower()
    tb["wine_type"] = np.where(
        ws.str.contains("blanc|chardonnay|riesling|white|montrachet|meursault|chablis|sauvignon|viognier|marsanne|roussanne|muscat", regex=True), "white",
        np.where(ws.str.contains("rouge|red|cabernet|merlot|pinot|syrah|grenache|mourvèdre|mourvedre|tempranillo", regex=True), "red",
                 "red")   # default to red (most fine wine is red)
    )

    print(f"  TB training rows: {len(tb):,}  "
          f"(producers: {tb['producer_slug'].nunique():,}, "
          f"YTM mean: {tb['years_to_maturity'].mean():.1f} yrs, "
          f"std: {tb['years_to_maturity'].std():.1f})")
    return tb


# ---------------------------------------------------------------------------
# 2. Feature engineering: target-encode producer + wine_slug
# ---------------------------------------------------------------------------

def build_features(tb: pd.DataFrame) -> pd.DataFrame:
    """Add target-encoded producer and wine features to TB data."""
    # Producer-level mean YTM (target encoding with global smoothing)
    global_mean = tb["years_to_maturity"].mean()
    k = 5  # smoothing parameter

    prod_stats = (tb.groupby("producer_slug")["years_to_maturity"]
                  .agg(["mean", "count"]).rename(columns={"mean": "prod_ytm_mean", "count": "prod_n"}))
    prod_stats["prod_ytm_enc"] = (
        (prod_stats["prod_ytm_mean"] * prod_stats["prod_n"] + global_mean * k)
        / (prod_stats["prod_n"] + k)
    )

    # Wine-slug-level mean YTM
    wine_stats = (tb.groupby("wine_slug")["years_to_maturity"]
                  .agg(["mean", "count"]).rename(columns={"mean": "wine_ytm_mean", "count": "wine_n"}))
    wine_stats["wine_ytm_enc"] = (
        (wine_stats["wine_ytm_mean"] * wine_stats["wine_n"] + global_mean * k)
        / (wine_stats["wine_n"] + k)
    )

    tb = tb.join(prod_stats[["prod_ytm_enc"]], on="producer_slug")
    tb = tb.join(wine_stats[["wine_ytm_enc"]], on="wine_slug")

    # Fill any remaining NaN in encodings with global mean
    tb["prod_ytm_enc"] = tb["prod_ytm_enc"].fillna(global_mean)
    tb["wine_ytm_enc"] = tb["wine_ytm_enc"].fillna(global_mean)

    # Region and wine_type as ordinal integers
    tb["region_enc"]    = OrdinalEncoder().fit_transform(tb[["region"]])[:, 0]
    tb["wine_type_enc"] = OrdinalEncoder().fit_transform(tb[["wine_type"]])[:, 0]

    return tb, prod_stats["prod_ytm_enc"], wine_stats["wine_ytm_enc"], global_mean


# ---------------------------------------------------------------------------
# 3. Train and cross-validate
# ---------------------------------------------------------------------------

FEATURES = ["prod_ytm_enc", "wine_ytm_enc", "vintage", "region_enc", "wine_type_enc"]

def train_model(tb: pd.DataFrame) -> GradientBoostingRegressor:
    X = tb[FEATURES].values
    y = tb["years_to_maturity"].values

    model = GradientBoostingRegressor(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        subsample=0.8, min_samples_leaf=10, random_state=42
    )

    print("  Cross-validating (5-fold) ...", flush=True)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
    print(f"  CV R²: {scores.mean():.3f} ± {scores.std():.3f}  (folds: {scores.round(3)})")

    rmse_scores = np.sqrt(-cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error"))
    print(f"  CV RMSE: {rmse_scores.mean():.2f} ± {rmse_scores.std():.2f} years")

    model.fit(X, y)
    print(f"  Train R²: {model.score(X, y):.3f}")

    # Save CV stats for downstream scripts (e.g. 09_paper_tables_figures.py)
    import json
    stats_path = ROOT / "output" / "05_imputation_stats.json"
    stats_path.parent.mkdir(exist_ok=True)
    cv_stats = {
        "n_training": int(len(y)),
        "cv_r2_mean": round(float(scores.mean()), 4),
        "cv_r2_std":  round(float(scores.std()),  4),
        "cv_rmse_mean": round(float(rmse_scores.mean()), 3),
        "cv_rmse_std":  round(float(rmse_scores.std()),  3),
        "train_r2": round(float(model.score(X, y)), 4),
        "feature_importances": {
            feat: round(float(imp), 4)
            for feat, imp in zip(FEATURES, model.feature_importances_)
        },
    }
    with open(stats_path, "w") as fh:
        json.dump(cv_stats, fh, indent=2)
    print(f"  CV stats saved: {stats_path.name}")
    return model


# ---------------------------------------------------------------------------
# 4. Impute for auction data
# ---------------------------------------------------------------------------

def impute_auction(
    model: GradientBoostingRegressor,
    prod_enc: pd.Series,
    wine_enc: pd.Series,
    global_mean: float,
) -> pd.DataFrame:
    print("  Loading auction data ...", flush=True)
    df = pd.read_parquet(AUCTION_IN, columns=[
        "norm_producer", "norm_wine", "Region", "Type_Combi",
        "Vintage", "years_to_maturity", "maturity_source",
    ])

    # Wine type from auction data
    tc = df["Type_Combi"].fillna("").str.lower()
    df["wine_type"] = np.where(
        tc.str.contains("white|blanc|chardonnay|sauvignon|riesling|viognier", regex=True), "white",
        "red"
    )

    # Region encoding (auction Region column)
    df["region"] = df["Region"].fillna("Other")

    # Vintage
    df["vintage"] = pd.to_numeric(df["Vintage"], errors="coerce")

    # Map auction norm_producer → TB prod_ytm_enc
    # First: try direct match via norm of producer slug
    def slug_to_norm(slug: str) -> str:
        return slug.replace("_", " ").lower() if isinstance(slug, str) else ""

    prod_enc_norm = {slug_to_norm(s): v for s, v in prod_enc.items()}

    def get_prod_enc(norm_producer: str) -> float:
        # Try direct lookup
        if norm_producer in prod_enc_norm:
            return prod_enc_norm[norm_producer]
        # Try partial match: find producer slug that contains the auction producer name
        for slug_norm, v in prod_enc_norm.items():
            if norm_producer and norm_producer in slug_norm:
                return v
        return global_mean

    print("  Encoding producers ...", flush=True)
    df["prod_ytm_enc"] = df["norm_producer"].apply(get_prod_enc)

    # Wine encoding: use norm_wine → look up in wine_enc
    wine_enc_norm = {w.replace("_", " ").lower(): v for w, v in wine_enc.items()}

    def get_wine_enc(norm_wine: str) -> float:
        if norm_wine in wine_enc_norm:
            return wine_enc_norm[norm_wine]
        return global_mean

    df["wine_ytm_enc"] = df["norm_wine"].apply(get_wine_enc)

    # Region and wine_type encoding (must match training encoding)
    region_map   = {"Bordeaux": 0.0, "Burgundy": 1.0, "Other": 2.0, "Rhone": 3.0}
    wine_type_map = {"red": 0.0, "white": 1.0}
    df["region_enc"]    = df["region"].map(region_map).fillna(2.0)
    df["wine_type_enc"] = df["wine_type"].map(wine_type_map).fillna(0.0)

    # Predict for ALL rows
    print("  Predicting ...", flush=True)
    X_pred = df[FEATURES].fillna(global_mean).values
    df["years_to_maturity_imputed"] = np.clip(model.predict(X_pred), 2, YTM_CAP)

    # Final: TB value if matched, model otherwise; cap both at YTM_CAP
    df["years_to_maturity_final"] = np.where(
        df["maturity_source"] != "unmatched",
        df["years_to_maturity"].clip(upper=YTM_CAP),
        df["years_to_maturity_imputed"],
    )
    df["maturity_imputed"] = df["maturity_source"] == "unmatched"

    n_imputed = df["maturity_imputed"].sum()
    n_tb      = (~df["maturity_imputed"]).sum()
    print(f"  TB-sourced:  {n_tb:,} ({100*n_tb/len(df):.1f}%)")
    print(f"  Imputed:     {n_imputed:,} ({100*n_imputed/len(df):.1f}%)")
    print(f"  YTM final — mean: {df['years_to_maturity_final'].mean():.1f}  "
          f"std: {df['years_to_maturity_final'].std():.1f}")

    return df[["years_to_maturity_imputed", "years_to_maturity_final", "maturity_imputed"]]


# ---------------------------------------------------------------------------
# 5. Write augmented parquet
# ---------------------------------------------------------------------------

def write_output(imputed_cols: pd.DataFrame) -> None:
    df = pd.read_parquet(AUCTION_IN)
    for col in ["years_to_maturity_imputed", "years_to_maturity_final", "maturity_imputed"]:
        df[col] = imputed_cols[col].values
    df.to_parquet(OUT_PATH, index=False)
    size_mb = OUT_PATH.stat().st_size / 1e6
    print(f"  Written: {OUT_PATH.name}  ({size_mb:.1f} MB, {len(df):,} rows)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Script 05: Maturity Imputation")
    print("=" * 60)

    print("\n[1] Loading Tastingbook training data ...")
    tb = load_tb()

    print("\n[2] Building features ...")
    tb, prod_enc, wine_enc, global_mean = build_features(tb)

    print("\n[3] Training GradientBoostingRegressor ...")
    model = train_model(tb)

    # Feature importance
    fi = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    print("\n  Feature importances:")
    for feat, imp in fi.items():
        print(f"    {feat:<25} {imp:.3f}")

    print("\n[4] Imputing auction lots ...")
    imputed = impute_auction(model, prod_enc, wine_enc, global_mean)

    print("\n[5] Writing output ...")
    write_output(imputed)

    print("\nDone.")


if __name__ == "__main__":
    main()

"""
Script  : 07_dip_significance_test.py
Purpose : Test whether the price dip at age 32-40 (age_norm 1.6-2.0) for
          grand cru Bordeaux reds is statistically significant.
          Also fits degree-5 polynomial and natural cubic spline.
"""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
from scipy.optimize import brentq
import patsy, warnings, json
from pathlib import Path
warnings.filterwarnings("ignore")
import sys; sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
OUT  = ROOT / "output"
OUT.mkdir(exist_ok=True)

# ── Load grand cru Bordeaux red ──────────────────────────────────────────────
df = pd.read_parquet(ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet")
df["price"] = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
df = df[df["price"] > 0]
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["sale_year"] = df["Date"].dt.year
df["vintage"] = pd.to_numeric(df["Vintage"], errors="coerce")
df = df[df["Excluded_Lots"].isin([0, "0", False, None]) | df["Excluded_Lots"].isna()]
df = df[df["Region"].astype(str).str.strip() == "Bordeaux"]
df["age"] = df["sale_year"] - df["vintage"]
df = df[(df["age"] >= 0) & (df["age"] <= 100)]
df["log_price"] = np.log(df["price"])
df = df[df["years_to_maturity_final"].notna() & (df["years_to_maturity_final"] > 0)]
df["age_norm"] = df["age"] / df["years_to_maturity_final"]
df = df[(df["age_norm"] >= 0) & (df["age_norm"] <= 3)]
tc = df["Type_Combi"].fillna("").str.lower()
df["wine_type"] = np.where(
    tc.str.contains("white|blanc|chardonnay|sauvignon|riesling|viognier", regex=True), "white", "red"
)
bt = pd.to_numeric(df["Size_liter"], errors="coerce")
df["bottle_size_cat"] = pd.cut(
    bt, bins=[0, 0.65, 0.85, 1.4, 1.6, 100],
    labels=["small", "standard", "half_mag", "magnum", "large"]
).astype(str).replace("nan", "standard")
gcc_kw = ["Premier Cru Class", "Deuxi", "Troisi", "Quatri", "Cinqui", "Cru Class", "grands cru"]
df = df[
    df["Class"].apply(lambda c: any(k in str(c) for k in gcc_kw)) &
    (df["wine_type"] == "red")
].copy()
df["vintage_fe"]    = df["vintage"].astype(str)
df["auction_house"] = df["Auc_House_Combi"].fillna("Unknown").astype(str)
df["log_price_dm"]  = df["log_price"] - df.groupby("norm_producer")["log_price"].transform("mean")
print(f"N = {len(df):,}")

# ── Degree-5 polynomial ──────────────────────────────────────────────────────
print("\n=== Degree-5 polynomial ===")
for d in range(1, 6):
    df[f"an{d}"] = df["age_norm"] ** d

m5_nofe = smf.ols("log_price ~ an1+an2+an3+an4+an5", data=df).fit(cov_type="HC1")
m5_fe   = smf.ols(
    "log_price_dm ~ an1+an2+an3+an4+an5 + C(bottle_size_cat) + C(vintage_fe) + C(auction_house)",
    data=df
).fit(cov_type="HC1")

def poly5_turning_points(m, label):
    coefs = [m.params[f"an{d}"] for d in range(1, 6)]
    c1, c2, c3, c4, c5 = coefs
    deriv_poly = np.poly1d([5*c5, 4*c4, 3*c3, 2*c2, c1])
    x = np.linspace(0.01, 3, 10000)
    y = deriv_poly(x)
    sc = np.where(np.diff(np.sign(y)))[0]
    f2 = np.polyder(deriv_poly)
    extrema = []
    for idx in sc:
        try:
            r = brentq(deriv_poly, x[idx], x[idx + 1])
            kind = "peak" if f2(r) < 0 else "trough"
            extrema.append((r, kind))
        except Exception:
            pass
    print(f"  [{label}]  R2={m.rsquared:.4f}")
    for d in range(1, 6):
        p = f"an{d}"
        c, se, pv = m.params[p], m.bse[p], m.pvalues[p]
        s = "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.1 else ""
        print(f"    an^{d}: {c:+.4f}{s} ({se:.4f})")
    if extrema:
        for r, kind in sorted(extrema):
            print(f"    --> {kind} at age_norm={r:.3f}  (~{r*20:.0f} yrs)")
    else:
        print("    --> no turning points in [0, 3]")

poly5_turning_points(m5_nofe, "No FE")
print()
poly5_turning_points(m5_fe,   "Producer FE")

# ── Natural cubic spline ─────────────────────────────────────────────────────
print("\n=== Natural cubic spline (knots: 0.4, 0.8, 1.2, 1.6, 2.2) ===")
knots = [0.4, 0.8, 1.2, 1.6, 2.2]
sp_mat = patsy.dmatrix(
    f"cr(an, knots={knots}, constraints='center') - 1",
    data={"an": df["age_norm"]}, return_type="dataframe"
)
sp_mat.columns = [f"sp{i}" for i in range(sp_mat.shape[1])]
sp_df = pd.concat([
    df[["log_price", "log_price_dm", "vintage_fe", "auction_house", "bottle_size_cat"]].reset_index(drop=True),
    sp_mat.reset_index(drop=True)
], axis=1)
sp_cols = " + ".join(sp_mat.columns)

m_sp_nofe = smf.ols(f"log_price ~ {sp_cols}", data=sp_df).fit(cov_type="HC1")
m_sp_fe   = smf.ols(
    f"log_price_dm ~ {sp_cols} + C(bottle_size_cat) + C(vintage_fe) + C(auction_house)",
    data=sp_df
).fit(cov_type="HC1")
print(f"  No FE:       R2={m_sp_nofe.rsquared:.4f}  AIC={m_sp_nofe.aic:.1f}")
print(f"  Producer FE: R2={m_sp_fe.rsquared:.4f}")

# Spline curve on fine grid
x_grid = np.linspace(0.05, 2.9, 500)
sp_grid = patsy.dmatrix(
    f"cr(an, knots={knots}, constraints='center') - 1",
    data={"an": x_grid}, return_type="dataframe"
)
sp_grid.columns = [f"sp{i}" for i in range(sp_grid.shape[1])]
sp_coef_names = [c for c in m_sp_nofe.params.index if c.startswith("sp")]
y_nofe = m_sp_nofe.params["Intercept"] + sp_grid.values @ m_sp_nofe.params[sp_coef_names].values
sp_coef_names_fe = [c for c in m_sp_fe.params.index if c.startswith("sp")]
y_fe   = m_sp_fe.params["Intercept"]   + sp_grid.values @ m_sp_fe.params[sp_coef_names_fe].values
slope_nofe = np.gradient(y_nofe, x_grid)
slope_fe   = np.gradient(y_fe,   x_grid)

print(f"\n  {'age_norm':<10}  {'~age':>6}  {'spline(no FE)':>14}  {'slope':>8}  direction")
print("  " + "-" * 55)
targets = np.arange(0.2, 2.9, 0.2)
for xv in targets:
    idx = np.argmin(np.abs(x_grid - xv))
    direction = "rising" if slope_nofe[idx] > 0 else "FALLING"
    print(f"  {xv:<10.1f}  {xv*20:>6.1f}  {y_nofe[idx]:>14.4f}  {slope_nofe[idx]:>8.4f}  {direction}")

# ── Segment dummies — dip significance ───────────────────────────────────────
print("\n=== Segment dummy tests ===")
bins   = [0.0, 0.6, 1.0, 1.6, 2.0, 3.01]
labels_seg = ["young", "approach", "peak", "trough", "antique"]
df["segment"] = pd.cut(df["age_norm"], bins=bins, labels=labels_seg, right=False).astype(str)

print("\nSegment composition:")
seg_stats = df.groupby("segment")["log_price"].agg(["count", "mean", "median"]).reindex(labels_seg)
for s, r in seg_stats.iterrows():
    print(f"  {s:<10}  N={int(r['count']):>7,}  mean={r['mean']:.4f}  median={r['median']:.4f}")

print("\nRegression (baseline = young):")
m_seg_nofe = smf.ols(
    'log_price ~ C(segment, Treatment("young"))', data=df
).fit(cov_type="HC1")
m_seg_fe = smf.ols(
    'log_price_dm ~ C(segment, Treatment("young")) + C(bottle_size_cat) + C(vintage_fe) + C(auction_house)',
    data=df
).fit(cov_type="HC1")

for label, m in [("No FE", m_seg_nofe), ("Producer FE", m_seg_fe)]:
    print(f"\n  [{label}]  R2={m.rsquared:.4f}")
    for seg_name in ["approach", "peak", "trough", "antique"]:
        p = f'C(segment, Treatment("young"))[T.{seg_name}]'
        c, se, pv = m.params[p], m.bse[p], m.pvalues[p]
        s = "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.1 else ""
        pct = (np.exp(c) - 1) * 100
        print(f"    {seg_name:<10}: {c:+.4f}{s} ({se:.4f})  p={pv:.4f}  effect={pct:+.1f}%")

print("\nDirect contrasts:")
for label, m in [("No FE", m_seg_nofe), ("Producer FE", m_seg_fe)]:
    print(f"\n  [{label}]")
    for (a, b, direction) in [
        ("peak",    "trough", "trough < peak (dip)"),
        ("trough",  "antique","antique > trough (recovery)"),
        ("peak",    "antique","antique > peak (net collector premium)"),
    ]:
        pa = f'C(segment, Treatment("young"))[T.{a}]'
        pb = f'C(segment, Treatment("young"))[T.{b}]'
        diff  = m.params[pb] - m.params[pa]
        var   = (m.cov_params().loc[pb, pb] + m.cov_params().loc[pa, pa]
                 - 2 * m.cov_params().loc[pb, pa])
        se_d  = np.sqrt(var)
        t_val = diff / se_d
        # one-sided p-value (testing in the expected direction)
        pv1   = stats.t.cdf(t_val, df=m.df_resid) if diff < 0 else 1 - stats.t.cdf(t_val, df=m.df_resid)
        sig   = "***" if pv1 < 0.001 else "**" if pv1 < 0.01 else "*" if pv1 < 0.05 else "n.s."
        pct   = (np.exp(diff) - 1) * 100
        print(f"    {direction}: diff={diff:+.4f}  SE={se_d:.4f}  t={t_val:.2f}  p={pv1:.6f} {sig}  ({pct:+.1f}%)")

# ── Save structured results ──────────────────────────────────────────────────
def _contrast(m, a, b):
    pa = f'C(segment, Treatment("young"))[T.{a}]'
    pb = f'C(segment, Treatment("young"))[T.{b}]'
    diff = m.params[pb] - m.params[pa]
    var  = (m.cov_params().loc[pb, pb] + m.cov_params().loc[pa, pa]
            - 2 * m.cov_params().loc[pb, pa])
    t_val = diff / np.sqrt(var)
    pv1 = stats.t.cdf(t_val, df=m.df_resid) if diff < 0 else 1 - stats.t.cdf(t_val, df=m.df_resid)
    return {"diff": round(diff, 6), "t": round(t_val, 4),
            "p_onesided": round(pv1, 6), "pct_effect": round((np.exp(diff)-1)*100, 2)}

results = {
    "group": "Bordeaux GCC red",
    "N": int(len(df)),
    "no_fe": {
        "r2": round(m_seg_nofe.rsquared, 4),
        "segments": {
            seg: {
                "coef": round(m_seg_nofe.params[f'C(segment, Treatment("young"))[T.{seg}]'], 6),
                "se":   round(m_seg_nofe.bse[f'C(segment, Treatment("young"))[T.{seg}]'], 6),
                "pv":   round(m_seg_nofe.pvalues[f'C(segment, Treatment("young"))[T.{seg}]'], 6),
            }
            for seg in ["approach", "peak", "trough", "antique"]
        },
        "trough_vs_peak":   _contrast(m_seg_nofe, "peak", "trough"),
        "antique_vs_trough": _contrast(m_seg_nofe, "trough", "antique"),
    },
}
out_path = OUT / "07_dip_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved: {out_path}")

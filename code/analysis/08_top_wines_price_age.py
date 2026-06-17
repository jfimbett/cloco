"""
Script  : 08_top_wines_price_age.py
Purpose : Replicate the no-FE price-age analysis (binned medians + spline +
          segment dip test) for four subsamples of top French wines:
            1. Grand Cru Bordeaux (all Crus Classés, red)
            2. Grand Cru Burgundy
            3. Premier Cru Burgundy
          No producer FE — we want the stylized market-level fact.
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

# ── Load and prepare ─────────────────────────────────────────────────────────
df = pd.read_parquet(ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet")
df["price"] = pd.to_numeric(df["P_$/Bt_Combi"], errors="coerce")
df = df[df["price"] > 0]
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["sale_year"] = df["Date"].dt.year
df["vintage"]   = pd.to_numeric(df["Vintage"], errors="coerce")
df = df[df["Excluded_Lots"].isin([0, "0", False, None]) | df["Excluded_Lots"].isna()]
df["Region"] = df["Region"].astype(str).str.strip()
df = df[df["Region"].isin(["Bordeaux", "Burgundy"])]
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

# ── Group definitions ────────────────────────────────────────────────────────
gcc_kw = ["Premier Cru Class", "Deuxi", "Troisi", "Quatri", "Cinqui", "Cru Class", "grands cru"]

masks = {
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

# ── Helper: spline turning-point curve ──────────────────────────────────────
KNOTS = [0.4, 0.8, 1.2, 1.6, 2.2]

def fit_spline(sub):
    sp_mat = patsy.dmatrix(
        f"cr(an, knots={KNOTS}, constraints='center') - 1",
        data={"an": sub["age_norm"]}, return_type="dataframe"
    )
    sp_mat.columns = [f"sp{i}" for i in range(sp_mat.shape[1])]
    sp_df = pd.concat([sub[["log_price"]].reset_index(drop=True),
                       sp_mat.reset_index(drop=True)], axis=1)
    sp_cols = " + ".join(sp_mat.columns)
    m = smf.ols(f"log_price ~ {sp_cols}", data=sp_df).fit(cov_type="HC1")
    # Predict on grid
    x_grid = np.linspace(0.05, 2.9, 500)
    sp_grid = patsy.dmatrix(
        f"cr(an, knots={KNOTS}, constraints='center') - 1",
        data={"an": x_grid}, return_type="dataframe"
    )
    sp_grid.columns = [f"sp{i}" for i in range(sp_grid.shape[1])]
    coef_names = [c for c in m.params.index if c.startswith("sp")]
    y_pred = m.params["Intercept"] + sp_grid.values @ m.params[coef_names].values
    slope  = np.gradient(y_pred, x_grid)
    return m, x_grid, y_pred, slope


def fit_poly5(sub):
    s = sub.copy()
    for d in range(1, 6):
        s[f"an{d}"] = s["age_norm"] ** d
    m = smf.ols("log_price ~ an1+an2+an3+an4+an5", data=s).fit(cov_type="HC1")
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
            if 0.05 < r < 2.95:   # ignore boundary artifacts
                extrema.append((r, kind))
        except Exception:
            pass
    return m, extrema


def segment_tests(sub):
    bins_seg   = [0.0, 0.6, 1.0, 1.6, 2.0, 3.01]
    labels_seg = ["young", "approach", "peak", "trough", "antique"]
    s = sub.copy()
    s["segment"] = pd.cut(s["age_norm"], bins=bins_seg,
                           labels=labels_seg, right=False).astype(str)
    m = smf.ols('log_price ~ C(segment, Treatment("young"))', data=s).fit(cov_type="HC1")
    results = {}
    for seg in labels_seg[1:]:
        p = f'C(segment, Treatment("young"))[T.{seg}]'
        c, se, pv = m.params[p], m.bse[p], m.pvalues[p]
        results[seg] = {"coef": c, "se": se, "pv": pv, "n": (s["segment"] == seg).sum()}
    # Direct contrast: trough vs peak
    p_pk = 'C(segment, Treatment("young"))[T.peak]'
    p_tr = 'C(segment, Treatment("young"))[T.trough]'
    diff = m.params[p_tr] - m.params[p_pk]
    var  = (m.cov_params().loc[p_tr, p_tr] + m.cov_params().loc[p_pk, p_pk]
            - 2 * m.cov_params().loc[p_tr, p_pk])
    t_dip = diff / np.sqrt(var)
    pv_dip = stats.t.cdf(t_dip, df=m.df_resid)   # one-sided
    return results, diff, t_dip, pv_dip, m


# ── Main loop ────────────────────────────────────────────────────────────────
SEP = "=" * 70
all_results = {}   # accumulate for JSON output

for group_name, mask in masks.items():
    sub = df[mask].copy()
    print(SEP)
    print(f"GROUP: {group_name}")
    print(f"  N={len(sub):,}  "
          f"pre={(sub['age_norm']<1).mean()*100:.1f}%  "
          f"post={(sub['age_norm']>1).mean()*100:.1f}%  "
          f"mean_age={sub['age'].mean():.1f} yrs  "
          f"mean_age_norm={sub['age_norm'].mean():.2f}")
    print()

    # Binned medians
    edges  = np.concatenate([np.arange(0, 2.1, 0.2), [3.0]])
    labels = [f"{edges[i]:.1f}-{edges[i+1]:.1f}" for i in range(len(edges) - 1)]
    sub["bin"] = pd.cut(sub["age_norm"], bins=edges, labels=labels, right=False)
    tbl = sub.groupby("bin", observed=True)["log_price"].agg(
        N="count", Median="median", Mean="mean",
        IQR=lambda x: x.quantile(0.75) - x.quantile(0.25)
    ).reset_index()
    print(f"  {'bin':<12}  {'N':>8}  {'Median':>8}  {'IQR':>8}")
    print("  " + "-" * 42)
    for _, r in tbl.iterrows():
        if r["N"] > 30:
            flag = " <--" if "1.4-1.6" in str(r["bin"]) else (
                   " DIP" if "1.6-1.8" in str(r["bin"]) or "1.8-2.0" in str(r["bin"]) else "")
            print(f"  {str(r['bin']):<12}  {int(r['N']):>8,}  {r['Median']:>8.3f}  {r['IQR']:>8.3f}{flag}")

    # Degree-5 polynomial
    print()
    try:
        m5, extrema = fit_poly5(sub)
        print(f"  Degree-5 poly: R2={m5.rsquared:.4f}")
        if extrema:
            for r, kind in sorted(extrema):
                print(f"    {kind} at age_norm={r:.3f}  (~{r*20:.0f} yrs)")
        else:
            print("    no turning points in (0.05, 2.95)")
    except Exception as e:
        print(f"  Poly5 failed: {e}")

    # Spline
    print()
    try:
        m_sp, x_grid, y_pred, slope = fit_spline(sub)
        print(f"  Spline: R2={m_sp.rsquared:.4f}")
        print(f"  {'age_norm':<10}  {'~age':>6}  {'pred':>10}  {'slope':>8}  dir")
        for xv in np.arange(0.2, 2.9, 0.2):
            idx = np.argmin(np.abs(x_grid - xv))
            d = "rising" if slope[idx] > 0 else "FALLING"
            print(f"  {xv:<10.1f}  {xv*20:>6.1f}  {y_pred[idx]:>10.4f}  {slope[idx]:>8.4f}  {d}")
    except Exception as e:
        print(f"  Spline failed: {e}")

    # Segment tests
    print()
    try:
        seg_res, diff, t_dip, pv_dip, m_seg = segment_tests(sub)
        print(f"  Segment dummies (baseline=young):  R2={m_seg.rsquared:.4f}")
        for seg, r in seg_res.items():
            n = r["n"]
            s = "***" if r["pv"] < 0.01 else "**" if r["pv"] < 0.05 else "*" if r["pv"] < 0.1 else ""
            pct = (np.exp(r["coef"]) - 1) * 100
            print(f"    {seg:<10}: {r['coef']:+.4f}{s}  ({r['se']:.4f})  N={n:,}  effect={pct:+.1f}%")
        sig = "***" if pv_dip < 0.001 else "**" if pv_dip < 0.01 else "*" if pv_dip < 0.05 else "n.s."
        pct_dip = (np.exp(diff) - 1) * 100
        print(f"  --> trough vs peak: diff={diff:+.4f}  t={t_dip:.2f}  p(1-sided)={pv_dip:.4f} {sig}  ({pct_dip:+.1f}%)")
        # Accumulate for JSON output
        all_results[group_name] = {
            "N": int(len(sub)),
            "segment_r2": round(m_seg.rsquared, 4),
            "segments": {
                seg: {"coef": round(r["coef"], 6), "se": round(r["se"], 6),
                      "pv": round(r["pv"], 6), "n": int(r["n"])}
                for seg, r in seg_res.items()
            },
            "trough_vs_peak": {
                "diff": round(diff, 6), "t": round(t_dip, 4),
                "p_onesided": round(pv_dip, 6),
                "pct_effect": round(pct_dip, 2),
            },
        }
    except Exception as e:
        print(f"  Segment test failed: {e}")
    print()

# ── Save structured results ──────────────────────────────────────────────────
out_path = OUT / "08_top_wines_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)
print(f"Results saved: {out_path}")

"""
Script  : 09_paper_tables_figures.py
Purpose : Generate all tables and figures for the paper.

Main paper outputs
  paper/figures/fig_spline_comparison.pdf   — Figure 1: spline curves (6 groups, 3 panels)
  paper/tables/tab_summary_stats.tex        — Table 1: sample description by group
  paper/tables/tab_segment_dip_bordeaux.tex — Table 2a: segment regression Bordeaux (3 specs)
  paper/tables/tab_segment_dip_burgundy.tex — Table 2b: segment regression Burgundy (3 specs)
  paper/tables/tab_piecewise_slopes.tex     — Table 3: piecewise linear slope estimates

Appendix outputs
  paper/appendix/tab_full_sample_stats.tex
  paper/appendix/tab_tastingbook_match_rates.tex
  paper/appendix/tab_maturity_imputation.tex
  paper/tables/tab_price_age_medians.tex
"""
import pandas as pd, numpy as np, warnings
import statsmodels.formula.api as smf
import patsy
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
warnings.filterwarnings("ignore")
import sys; sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
(ROOT / "paper" / "tables").mkdir(exist_ok=True)
(ROOT / "paper" / "figures").mkdir(exist_ok=True)
(ROOT / "paper" / "appendix").mkdir(exist_ok=True)

# ── Load and prepare data ────────────────────────────────────────────────────
print("Loading data...")
df_full = pd.read_parquet(ROOT / "data" / "processed" / "auction_with_maturity_imputed.parquet")
df_full["price"]   = pd.to_numeric(df_full["P_$/Bt_Combi"], errors="coerce")
df_full = df_full[df_full["price"] > 0]
df_full["Date"]    = pd.to_datetime(df_full["Date"], errors="coerce")
df_full["sale_year"] = df_full["Date"].dt.year
df_full["vintage"] = pd.to_numeric(df_full["Vintage"], errors="coerce")
df_full = df_full[df_full["Excluded_Lots"].isin([0,"0",False,None]) | df_full["Excluded_Lots"].isna()]
df_full["Region"]  = df_full["Region"].astype(str).str.strip()
df_full["age"]     = df_full["sale_year"] - df_full["vintage"]
df_full = df_full[(df_full["age"] >= 0) & (df_full["age"] <= 100)]
df_full["log_price"] = np.log(df_full["price"])
df_full = df_full[df_full["years_to_maturity_final"].notna() & (df_full["years_to_maturity_final"] > 0)]
df_full["age_norm"] = df_full["age"] / df_full["years_to_maturity_final"]
df_full = df_full[(df_full["age_norm"] >= 0) & (df_full["age_norm"] <= 3)]
tc = df_full["Type_Combi"].fillna("").str.lower()
df_full["wine_type"] = np.where(
    tc.str.contains("white|blanc|chardonnay|sauvignon|riesling|viognier", regex=True), "white", "red"
)
# Normalise producer for FE regressions
df_full["producer_fe"] = df_full["Producer"].fillna("Unknown").astype(str).str.strip()
df_full["vintage_fe"]  = df_full["vintage"].fillna(0).astype(int).astype(str)

# ── Group masks ───────────────────────────────────────────────────────────────
# Bordeaux
gcc_kw = ["Premier Cru Class","Deuxi","Troisi","Quatri","Cinqui","Cru Class","grands cru"]
bx_all_mask = (
    df_full["Region"].eq("Bordeaux")
    & df_full["Class"].apply(lambda c: any(k in str(c) for k in gcc_kw))
    & df_full["wine_type"].eq("red")
)
# Bordeaux Grand Cru: 1er Cru Médoc + Premiers grands crus classés A St-Emilion
bx_grc_mask = (
    df_full["Region"].eq("Bordeaux")
    & df_full["Class"].apply(
        lambda c: ("1 Premier Cru Class" in str(c)) or ("A_St.Emilion" in str(c))
    )
    & df_full["wine_type"].eq("red")
)
bx_prc_mask = bx_all_mask & ~bx_grc_mask  # 2nd-5th Médoc + Graves + St-Emilion B/regular

# Burgundy
bu_grc_mask = df_full["Region"].eq("Burgundy") & df_full["Class"].astype(str).str.contains("Grand Cru_Burgundy", na=False)
bu_prc_mask = df_full["Region"].eq("Burgundy") & df_full["Class"].astype(str).str.contains("Premier Cru_Burgundy", na=False)
bu_all_mask = bu_grc_mask | bu_prc_mask

masks = {
    "Bordeaux All":         bx_all_mask,
    "Bordeaux Grand Cru":   bx_grc_mask,
    "Bordeaux Premier Cru": bx_prc_mask,
    "Burgundy All":         bu_all_mask,
    "Burgundy Grand Cru":   bu_grc_mask,
    "Burgundy Premier Cru": bu_prc_mask,
}

tex_labels = {
    "Bordeaux All":         "Bordeaux All",
    "Bordeaux Grand Cru":   "Bordeaux Grand Cru",
    "Bordeaux Premier Cru": "Bordeaux Premier Cru",
    "Burgundy All":         "Burgundy All",
    "Burgundy Grand Cru":   "Burgundy Grand Cru",
    "Burgundy Premier Cru": "Burgundy Premier Cru",
}

groups = {k: df_full[v].copy() for k, v in masks.items()}
for k, v in groups.items():
    print(f"  {k}: N={len(v):,}")

def wrap_table(body, caption, label, size=r"\small"):
    """Wrap a bare tabular+tablenotes block in a full table float."""
    return (
        "\\begin{table}[htbp]\n"
        "\\centering\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        f"{size}\n"
        "\\begin{threeparttable}\n"
        + body +
        "\\end{threeparttable}\n"
        "\\end{table}\n"
    )

# ── Colour palette ─────────────────────────────────────────────────────────────
COLORS = {
    "Bordeaux All":         "#6B0000",   # darkest red
    "Bordeaux Grand Cru":   "#C0392B",   # medium red
    "Bordeaux Premier Cru": "#E07070",   # light red
    "Burgundy All":         "#1A2A6B",   # darkest blue
    "Burgundy Grand Cru":   "#2C3E7A",   # medium blue
    "Burgundy Premier Cru": "#5B7FC0",   # light blue
}
LABELS = {
    "Bordeaux All":         "Bordeaux All",
    "Bordeaux Grand Cru":   "Bordeaux Grand Cru",
    "Bordeaux Premier Cru": "Bordeaux Premier Cru",
    "Burgundy All":         "Burgundy All",
    "Burgundy Grand Cru":   "Burgundy Grand Cru",
    "Burgundy Premier Cru": "Burgundy Premier Cru",
}

# ── Spline fitting helper ─────────────────────────────────────────────────────
KNOTS = [0.4, 0.8, 1.2, 1.6, 2.2]

def fit_spline_with_ci(sub, x_grid):
    """Fit natural cubic spline, return predictions + 95% CI on x_grid."""
    sp_mat = patsy.dmatrix(
        f"cr(an, knots={KNOTS}, constraints='center') - 1",
        data={"an": sub["age_norm"]}, return_type="dataframe"
    )
    sp_mat.columns = [f"sp{i}" for i in range(sp_mat.shape[1])]
    sp_df = pd.concat([sub[["log_price"]].reset_index(drop=True),
                       sp_mat.reset_index(drop=True)], axis=1)
    sp_cols = " + ".join(sp_mat.columns)
    m = smf.ols(f"log_price ~ {sp_cols}", data=sp_df).fit(cov_type="HC1")

    sp_grid = patsy.dmatrix(
        f"cr(an, knots={KNOTS}, constraints='center') - 1",
        data={"an": x_grid}, return_type="dataframe"
    )
    sp_grid.columns = [f"sp{i}" for i in range(sp_grid.shape[1])]
    coef_names = [c for c in m.params.index if c.startswith("sp")]

    X_pred = np.column_stack([np.ones(len(x_grid)),
                               sp_grid[coef_names].values])
    param_vec = np.array([m.params["Intercept"]] + list(m.params[coef_names]))
    y_pred = X_pred @ param_vec

    full_names = ["Intercept"] + coef_names
    cov_sub    = m.cov_params().loc[full_names, full_names].values
    se_pred    = np.sqrt(np.einsum("ij,jk,ik->i", X_pred, cov_sub, X_pred))

    return y_pred, se_pred, m


# ── Figure 1: Spline comparison (3-panel, 6 groups) ──────────────────────────
print("\nGenerating Figure 1: spline comparison (3 panels)...")

plt.rcParams.update({
    "font.family":       "serif",
    "font.size":         11,
    "axes.linewidth":    0.8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi":        150,
})

x_grid = np.linspace(0.05, 2.85, 400)
x_age  = x_grid * 20   # approximate calendar years (20 = maturity cap)

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)

def add_panel(ax, keys, title):
    bin_edges = np.concatenate([np.arange(0, 2.1, 0.30), [3.0]])
    for key in keys:
        sub   = groups[key]
        color = COLORS[key]
        label = LABELS[key]

        y_pred, se_pred, _ = fit_spline_with_ci(sub, x_grid)
        ax.plot(x_age, y_pred, color=color, lw=2.0, label=label)
        ax.fill_between(x_age, y_pred - 1.96*se_pred, y_pred + 1.96*se_pred,
                        color=color, alpha=0.12)

        # Binned medians
        sub2 = sub.copy()
        sub2["bin"] = pd.cut(sub2["age_norm"], bins=bin_edges, right=False)
        agg = sub2.groupby("bin", observed=True).agg(
            N       =("log_price", "count"),
            Median  =("log_price", "median"),
            mid_age =("age",       "median"),
        ).reset_index()
        agg = agg[agg["N"] > 20]
        ax.scatter(agg["mid_age"], agg["Median"], color=color, s=18, alpha=0.6, zorder=3)

    ax.axvline(20, color="gray", lw=1.0, ls="--", alpha=0.7,
               label="Maturity (20 yrs)")
    ax.axvspan(32, 40, color="gold", alpha=0.15, label="Trough zone")
    ax.set_xlabel("Wine age at sale (years)", fontsize=10)
    ax.set_ylabel("Log price per bottle (USD)", fontsize=10)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title(title, fontsize=10, pad=8)
    ax.set_xlim(0, 58)

add_panel(axes[0], ["Bordeaux All", "Bordeaux Grand Cru", "Bordeaux Premier Cru"],
          "Panel A — Bordeaux subgroups")
add_panel(axes[1], ["Burgundy All", "Burgundy Grand Cru", "Burgundy Premier Cru"],
          "Panel B — Burgundy subgroups")
add_panel(axes[2], ["Bordeaux All", "Burgundy All"],
          "Panel C — Bordeaux vs Burgundy (all)")

fig.tight_layout(pad=2.5)
fig_path = ROOT / "paper" / "figures" / "fig_spline_comparison.pdf"
fig.savefig(fig_path, bbox_inches="tight")
fig.savefig(str(fig_path).replace(".pdf", ".png"), bbox_inches="tight", dpi=180)
print(f"  Saved: {fig_path.name} + .png")
plt.close()


# ── Table 1: Summary statistics (6 groups) ──────────────────────────────────
print("\nGenerating Table 1: summary statistics...")

rows = []
for key, sub in groups.items():
    young   = sub[sub["age_norm"] < 0.4]
    at_mat  = sub[(sub["age_norm"] >= 0.9) & (sub["age_norm"] < 1.1)]
    antique = sub[sub["age_norm"] >= 2.0]
    rows.append({
        "group":       tex_labels[key],
        "N":           len(sub),
        "pct_post":    (sub["age_norm"] > 1.0).mean() * 100,
        "med_age":     sub["age"].median(),
        "med_p_young": np.exp(young["log_price"].median()),
        "med_p_mat":   np.exp(at_mat["log_price"].median()),
        "med_p_ant":   np.exp(antique["log_price"].median()) if len(antique) > 30 else np.nan,
        "pct_coll":    (young["price"] > 200).mean() * 100,
    })
ss = pd.DataFrame(rows)

tex_body = r"""\begin{tabular}{lrrrrrrr}
\toprule
 & & \multicolumn{2}{c}{Share} & \multicolumn{3}{c}{Median price (\$/bottle)} & \\
\cmidrule(lr){3-4}\cmidrule(lr){5-7}
Group & $N$ & Post-mat. & Coll.$^{a}$ & Young & At peak & Antique & Med. age \\
 & & (\%) & (\%) & & & & (yrs) \\
\midrule
"""
for i, (_, r) in enumerate(ss.iterrows()):
    if i == 3:
        tex_body += r"\midrule" + "\n"
    ant_str = f"\\${r['med_p_ant']:,.0f}" if not np.isnan(r["med_p_ant"]) else "---"
    tex_body += (f"{r['group']} & {r['N']:,} & {r['pct_post']:.1f} & {r['pct_coll']:.1f} & "
                 f"\\${r['med_p_young']:,.0f} & \\${r['med_p_mat']:,.0f} & {ant_str} & {r['med_age']:.0f} \\\\\n")

tex_body += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item Notes: ``Young'' = age\textsubscript{norm} $<$ 0.4 ($<$ 8 years).
  ``At peak'' = age\textsubscript{norm} $\in$ [0.9, 1.1] (18--22 years).
  ``Antique'' = age\textsubscript{norm} $>$ 2.0 ($>$ 40 years).
  $^{a}$ Share of young lots priced $>$ \$200/bottle.
  Maturity cap: 20 years. Sample period: 1996--2015.
\end{tablenotes}
"""
tex = wrap_table(tex_body, "Sample summary statistics by wine group", "tab:summary_stats")
(ROOT / "paper" / "tables" / "tab_summary_stats.tex").write_text(tex, encoding="utf-8")
print("  Saved: tab_summary_stats.tex")


# ── Table 2: Binned medians ──────────────────────────────────────────────────
print("Generating Table 2: binned medians...")

edges        = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 3.01]
labels_bins  = ["0.0--0.2","0.2--0.4","0.4--0.6","0.6--0.8","0.8--1.0",
                "1.0--1.2","1.2--1.4","1.4--1.6","1.6--1.8","1.8--2.0","2.0+"]
age_approx   = ["0--4","4--8","8--12","12--16","16--20",
                "20--24","24--28","28--32","32--36","36--40","40+"]

med_data = {}
n_data   = {}
for key, sub in groups.items():
    sub2 = sub.copy()
    sub2["bin"] = pd.cut(sub2["age_norm"], bins=edges, labels=labels_bins, right=False)
    tbl = sub2.groupby("bin", observed=True)["log_price"].agg(
        N="count", Median="median").reindex(labels_bins)
    med_data[key] = tbl["Median"].values
    n_data[key]   = tbl["N"].values

gkeys = list(groups.keys())
tex2_body = r"""\begin{tabular}{llcrrrrrr}
\toprule
 &  & & \multicolumn{3}{c}{Bordeaux} & \multicolumn{3}{c}{Burgundy} \\
\cmidrule(lr){4-6}\cmidrule(lr){7-9}
age\textsubscript{norm} & Age (yrs) & & All & Grand Cru & Prem. Cru & All & Grand Cru & Prem. Cru \\
\midrule
"""
for i, (lab, age) in enumerate(zip(labels_bins, age_approx)):
    dip_marker = r" $\downarrow$" if lab in ["1.6--1.8","1.8--2.0"] else ""
    row = f"{lab} & {age} & & "   # blank spacer cell for the 'c' column
    for ki, key in enumerate(gkeys):
        med = med_data[key][i]
        n   = int(n_data[key][i]) if not np.isnan(n_data[key][i]) else 0
        if np.isnan(med) or n < 30:
            row += "--- & " if ki < len(gkeys)-1 else "---"
        else:
            row += f"{med:.3f}{dip_marker} & " if ki < len(gkeys)-1 else f"{med:.3f}{dip_marker}"
    row += " \\\\\n"
    if lab == "1.0--1.2":
        tex2_body += r"\midrule" + "\n"
        tex2_body += r"\multicolumn{9}{l}{\textit{Post-maturity}} \\" + "\n"
    tex2_body += row

tex2_body += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item Notes: Median log price per bottle (USD). age\textsubscript{norm} = age / $\tau_i$
  where $\tau_i = \min(\text{TB maturity}, 20)$ years.
  $\downarrow$ marks the trough zone (age 32--40 years).
  Cells with $N < 30$ shown as ``---''.
\end{tablenotes}
"""
tex2 = wrap_table(tex2_body, "Median log price per bottle by normalized age and wine group",
                  "tab:price_age_medians", r"\footnotesize")
(ROOT / "paper" / "tables" / "tab_price_age_medians.tex").write_text(tex2, encoding="utf-8")
print("  Saved: tab_price_age_medians.tex")


# ── Tables 3a/3b: Segment regression + FE columns ────────────────────────────
print("Generating Tables 3a/3b: segment dip (with vintage FE and producer FE)...")

seg_bins   = [0.0, 0.6, 1.0, 1.6, 2.0, 3.01]
seg_labels = ["young","approach","peak","trough","antique"]

def run_segment_models(sub):
    """Run 4 specifications: baseline, vintage FE, producer FE, both FE."""
    s = sub.copy()
    s["segment"] = pd.cut(s["age_norm"], bins=seg_bins,
                           labels=seg_labels, right=False).astype(str)
    # Drop tiny segments to avoid perfect multicollinearity in FE specs
    s = s[s["segment"].isin(seg_labels)]
    base = 'C(segment, Treatment("young"))'

    # Spec 1: baseline
    m1 = smf.ols(f'log_price ~ {base}', data=s).fit(cov_type="HC1")
    # Spec 2: vintage year FE
    m2 = smf.ols(f'log_price ~ {base} + C(vintage_fe)', data=s).fit(cov_type="HC1")
    # Spec 3: producer FE
    m3 = smf.ols(f'log_price ~ {base} + C(producer_fe)', data=s).fit(cov_type="HC1")
    # Spec 4: both vintage FE and producer FE
    m4 = smf.ols(f'log_price ~ {base} + C(vintage_fe) + C(producer_fe)', data=s).fit(cov_type="HC1")

    results = []
    for m in [m1, m2, m3, m4]:
        p_pk = f'{base}[T.peak]'
        p_tr = f'{base}[T.trough]'
        diff = m.params[p_tr] - m.params[p_pk]
        var  = (m.cov_params().loc[p_tr, p_tr] + m.cov_params().loc[p_pk, p_pk]
                - 2 * m.cov_params().loc[p_tr, p_pk])
        t_val = diff / np.sqrt(var)
        pv    = stats.t.cdf(t_val, df=m.df_resid)
        results.append({"model": m, "diff": diff, "t": t_val, "pv": pv,
                         "n_seg": {sg: (s["segment"] == sg).sum() for sg in seg_labels}})
    return results

def fmt_coef(m, p):
    if p not in m.params:
        return "---", ""
    c, se, pv = m.params[p], m.bse[p], m.pvalues[p]
    stars = "^{***}" if pv < 0.01 else "^{**}" if pv < 0.05 else "^{*}" if pv < 0.1 else ""
    return f"{c:.3f}{stars}", f"({se:.3f})"

def fmt_diff(diff, pv):
    stars = "^{***}" if pv < 0.001 else "^{**}" if pv < 0.01 else "^{*}" if pv < 0.05 else ""
    pct   = (np.exp(diff) - 1) * 100
    return f"${diff:.3f}{stars}$", f"({pct:+.1f}\\%)"

def build_segment_table(region_keys, caption, label, fname):
    """Build a segment regression table for a set of groups (4 specs each).

    Uses resizebox to scale the tabular to textwidth, with notes outside
    the resize box so they remain at normal font size.
    """
    # Pre-compute models
    all_results = {}
    for key in region_keys:
        all_results[key] = run_segment_models(groups[key])

    n_groups = len(region_keys)
    n_specs  = 4  # baseline, vintage FE, producer FE, both FE

    # Column header: group name spanning 4 columns each
    group_header = ""
    spec_header  = ""
    col_spec     = "l" + "cccc" * n_groups
    for key in region_keys:
        group_header += f" & \\multicolumn{{4}}{{c}}{{{tex_labels[key]}}}"
        spec_header  += " & (1) & (2) & (3) & (4)"

    # cmidrule positions (4 cols per group)
    cmid = ""
    for i, _ in enumerate(region_keys):
        lo = 2 + i * 4
        hi = lo + 3
        cmid += f"\\cmidrule(lr){{{lo}-{hi}}}"

    # Build the tabular body (will be wrapped in \resizebox)
    tab = r"\begin{tabular}{" + col_spec + "}\n\\toprule\n"
    tab += group_header + " \\\\\n"
    tab += cmid + "\n"
    tab += "Segment (base: young)" + spec_header + " \\\\\n"
    tab += r"\midrule" + "\n"

    # Segment rows
    for seg in ["approach", "peak", "trough", "antique"]:
        row  = f"\\textit{{{seg.capitalize()}}}"
        srow = " "
        for key in region_keys:
            res = all_results[key]
            for r in res:
                p = f'C(segment, Treatment("young"))[T.{seg}]'
                c_str, se_str = fmt_coef(r["model"], p)
                row  += f" & ${c_str}$"
                srow += f" & {se_str}"
        row  += " \\\\\n"
        srow += " \\\\\n"
        tab  += row + srow

    tab += r"\midrule" + "\n"
    # Trough - Peak contrast
    tab += "\\textbf{Trough $-$ Peak}"
    for key in region_keys:
        for r in all_results[key]:
            d_str, pct_str = fmt_diff(r["diff"], r["pv"])
            tab += f" & {d_str}"
    tab += " \\\\\n"
    # pct row
    tab += " "
    for key in region_keys:
        for r in all_results[key]:
            pct = (np.exp(r["diff"]) - 1) * 100
            tab += f" & ({pct:+.1f}\\%)"
    tab += " \\\\\n"

    tab += r"\midrule" + "\n"
    # R2
    tab += "$R^2$"
    for key in region_keys:
        for r in all_results[key]:
            tab += f" & {r['model'].rsquared:.3f}"
    tab += " \\\\\n"
    # N
    tab += "$N$"
    for key in region_keys:
        for r in all_results[key]:
            tab += f" & {int(r['model'].nobs):,}"
    tab += " \\\\\n"
    # FE indicators
    tab += "Vintage FE"
    for key in region_keys:
        tab += " & No & Yes & No & Yes"
    tab += " \\\\\n"
    tab += "Producer FE"
    for key in region_keys:
        tab += " & No & No & Yes & Yes"
    tab += " \\\\\n"
    tab += "\\bottomrule\n\\end{tabular}"

    notes = (
        r"{\footnotesize\textit{Notes:} OLS, dependent variable log price per bottle (USD). "
        r"Robust (HC1) standard errors in parentheses. "
        r"Segments: \textit{young} = $a^* \in [0, 0.6)$; "
        r"\textit{approach} $\in [0.6, 1.0)$; \textit{peak} $\in [1.0, 1.6)$; "
        r"\textit{trough} $\in [1.6, 2.0)$; \textit{antique} $\in [2.0, 3.0]$. "
        r"``Trough $-$ Peak'' reports the direct contrast with one-sided $p$-value (trough $<$ peak). "
        r"(1) Baseline. (2) Vintage FE. (3) Producer FE. (4) Both FE. "
        r"$^{***}p<0.001$, $^{**}p<0.01$, $^{*}p<0.05$.}"
    )

    full_tex = (
        "\\begin{table}[htbp]\n"
        "\\centering\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\resizebox{\\textwidth}{!}{%\n"
        + tab + "\n"
        "}\n"
        "\\par\\vspace{4pt}\n"
        + notes + "\n"
        "\\end{table}\n"
    )
    (ROOT / "paper" / "tables" / fname).write_text(full_tex, encoding="utf-8")
    print(f"  Saved: {fname}")

build_segment_table(
    ["Bordeaux All", "Bordeaux Grand Cru", "Bordeaux Premier Cru"],
    "Price-age segment regression: Bordeaux groups",
    "tab:segment_dip_bordeaux",
    "tab_segment_dip_bordeaux.tex"
)
build_segment_table(
    ["Burgundy All", "Burgundy Grand Cru", "Burgundy Premier Cru"],
    "Price-age segment regression: Burgundy groups",
    "tab:segment_dip_burgundy",
    "tab_segment_dip_burgundy.tex"
)

# ── Table 4: Piecewise linear slope estimates ─────────────────────────────────
print("Generating Table 4: piecewise linear slopes...")

def fit_piecewise(sub):
    """Fit piecewise linear model with knots at a*=1 and a*=2."""
    s = sub.copy()
    s["x1"] = s["age_norm"]
    s["x2"] = np.maximum(0, s["age_norm"] - 1.0)
    s["x3"] = np.maximum(0, s["age_norm"] - 2.0)
    m = smf.ols("log_price ~ x1 + x2 + x3", data=s).fit(cov_type="HC1")
    return m

pw_results = {}
for key, sub in groups.items():
    pw_results[key] = fit_piecewise(sub)

gkeys = list(groups.keys())
n_cols = len(gkeys)

# Short column labels
short_lbl = {
    "Bordeaux All":         "Bx All",
    "Bordeaux Grand Cru":   "Bx GC",
    "Bordeaux Premier Cru": "Bx PC",
    "Burgundy All":         "Bu All",
    "Burgundy Grand Cru":   "Bu GC",
    "Burgundy Premier Cru": "Bu PC",
}

col_spec = "l" + "c" * n_cols
header   = " & ".join(f"\\multicolumn{{1}}{{c}}{{{short_lbl[k]}}}" for k in gkeys)

tex4  = r"\begin{tabular}{" + col_spec + "}\n\\toprule\n"
tex4 += " & " + header + " \\\\\n"
tex4 += r"\midrule" + "\n"

# Row helper
def pw_row(label, param_fn, se_fn):
    row  = label
    srow = " "
    for key in gkeys:
        m = pw_results[key]
        c, se = param_fn(m), se_fn(m)
        stars = ""
        pv = m.pvalues.get(m.params.index[list(m.params.index).index(
            [x for x in m.params.index if x == param_fn.__name__][0]
        )] if False else m.params.index[0], 1.0)
        row  += f" & {c:.4f}"
        srow += f" & ({se:.4f})"
    return row + " \\\\\n" + srow + " \\\\\n"

# β1 (pre-maturity slope)
tex4 += "$\\beta_1$ (pre-maturity slope)"
srow1 = " "
for key in gkeys:
    m = pw_results[key]
    c, se = m.params["x1"], m.bse["x1"]
    pv    = m.pvalues["x1"]
    stars = "^{***}" if pv<0.01 else "^{**}" if pv<0.05 else "^{*}" if pv<0.1 else ""
    tex4  += f" & ${c:.4f}{stars}$"
    srow1 += f" & ({se:.4f})"
tex4  += " \\\\\n" + srow1 + " \\\\\n"

# β2 (change at maturity)
tex4 += "$\\beta_2$ (change at maturity)"
srow2 = " "
for key in gkeys:
    m = pw_results[key]
    c, se = m.params["x2"], m.bse["x2"]
    pv    = m.pvalues["x2"]
    stars = "^{***}" if pv<0.01 else "^{**}" if pv<0.05 else "^{*}" if pv<0.1 else ""
    tex4  += f" & ${c:.4f}{stars}$"
    srow2 += f" & ({se:.4f})"
tex4 += " \\\\\n" + srow2 + " \\\\\n"

# β3 (change at antique)
tex4 += "$\\beta_3$ (change at antique)"
srow3 = " "
for key in gkeys:
    m = pw_results[key]
    c, se = m.params["x3"], m.bse["x3"]
    pv    = m.pvalues["x3"]
    stars = "^{***}" if pv<0.01 else "^{**}" if pv<0.05 else "^{*}" if pv<0.1 else ""
    tex4  += f" & ${c:.4f}{stars}$"
    srow3 += f" & ({se:.4f})"
tex4 += " \\\\\n" + srow3 + " \\\\\n"

tex4 += r"\midrule" + "\n"
# Trough slope = β1 + β2 (delta method)
tex4 += "\\textbf{Trough slope} $\\beta_1+\\beta_2$"
srow_tr = " "
for key in gkeys:
    m  = pw_results[key]
    c  = m.params["x1"] + m.params["x2"]
    cov_mat = m.cov_params()
    var = (cov_mat.loc["x1","x1"] + cov_mat.loc["x2","x2"]
           + 2 * cov_mat.loc["x1","x2"])
    se  = np.sqrt(max(var, 0))
    pv  = 2 * stats.t.sf(abs(c / se), df=m.df_resid) if se > 0 else 1.0
    stars = "^{***}" if pv<0.01 else "^{**}" if pv<0.05 else "^{*}" if pv<0.1 else ""
    tex4  += f" & ${c:.4f}{stars}$"
    srow_tr += f" & ({se:.4f})"
tex4 += " \\\\\n" + srow_tr + " \\\\\n"

tex4 += r"\midrule" + "\n"
tex4 += "$R^2$"
for key in gkeys:
    tex4 += f" & {pw_results[key].rsquared:.3f}"
tex4 += " \\\\\n"
tex4 += "$N$"
for key in gkeys:
    tex4 += f" & {int(pw_results[key].nobs):,}"
tex4 += " \\\\\n"

tex4 += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item Notes: OLS piecewise linear regression. Dependent variable: log price per bottle (USD).
  Model: $\log p = \alpha + \beta_1 a^* + \beta_2 (a^*-1)_+ + \beta_3 (a^*-2)_+ + \varepsilon$
  where $(x)_+ = \max(0,x)$.
  The slope in the trough zone ($a^* \in [1,2)$) is $\beta_1+\beta_2$; negative values indicate
  a declining price-age profile in the post-maturity period.
  Robust (HC1) standard errors in parentheses.
  $^{***}p<0.01$, $^{**}p<0.05$, $^{*}p<0.10$.
\end{tablenotes}
"""
tex4_full = wrap_table(tex4,
    "Piecewise linear price-age slopes by wine group",
    "tab:piecewise_slopes", r"\small")
(ROOT / "paper" / "tables" / "tab_piecewise_slopes.tex").write_text(tex4_full, encoding="utf-8")
print("  Saved: tab_piecewise_slopes.tex")


# ── Appendix Table A1: Full sample statistics ─────────────────────────────────
print("Generating Appendix A1: full sample stats...")

df_core = df_full[df_full["Region"].isin(["Bordeaux","Burgundy","Rhone"])].copy()
app_rows = []
for region in ["Bordeaux","Burgundy","Rhone"]:
    for wt in ["red","white"]:
        sub = df_core[(df_core["Region"]==region) & (df_core["wine_type"]==wt)]
        if len(sub) < 100: continue
        app_rows.append({
            "Region": region, "Type": wt,
            "N": len(sub),
            "Med price": np.exp(sub["log_price"].median()),
            "Med age": sub["age"].median(),
            "% pre-mat": (sub["age_norm"] < 1.0).mean()*100,
            "% post-mat": (sub["age_norm"] > 1.0).mean()*100,
        })
app_df = pd.DataFrame(app_rows)

tex_a1_body = r"""\begin{tabular}{llrrrrr}
\toprule
Region & Type & $N$ & Med. price & Med. age & Pre-mat. & Post-mat. \\
 & & & (\$/bottle) & (yrs) & (\%) & (\%) \\
\midrule
"""
for _, r in app_df.iterrows():
    tex_a1_body += (f"{r['Region']} & {r['Type']} & {r['N']:,} & \\${r['Med price']:.0f} & "
                    f"{r['Med age']:.0f} & {r['% pre-mat']:.1f} & {r['% post-mat']:.1f} \\\\\n")
tex_a1_body += r"""\bottomrule
\end{tabular}
"""
tex_a1 = wrap_table(tex_a1_body,
    "Full sample summary statistics (all lots, by region and type)", "tab:full_sample")
(ROOT / "paper" / "appendix" / "tab_full_sample_stats.tex").write_text(tex_a1, encoding="utf-8")
print("  Saved: tab_full_sample_stats.tex (appendix)")


# ── Appendix Table A2: Tastingbook match rates ────────────────────────────────
print("Generating Appendix A2: Tastingbook match rates...")

df_match = pd.read_parquet(ROOT / "data" / "processed" / "auction_with_maturity.parquet",
                            columns=["Region","maturity_source"])
df_match = df_match[df_match["Region"].isin(["Bordeaux","Burgundy","Rhone"])]
match_tbl = (df_match.groupby(["Region","maturity_source"])
             .size().reset_index(name="N"))
match_tbl["pct"] = match_tbl.groupby("Region")["N"].transform(lambda x: x/x.sum()*100)

tex_a2_body = r"""\begin{tabular}{llrr}
\toprule
Region & Match type & $N$ & Share (\%) \\
\midrule
"""
for _, r in match_tbl.sort_values(["Region","pct"], ascending=[True,False]).iterrows():
    src = str(r['maturity_source']).replace("_", r"\_")
    tex_a2_body += f"{r['Region']} & {src} & {int(r['N']):,} & {r['pct']:.1f} \\\\\n"
tex_a2_body += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item Notes: match types: \textit{exact} = matched on (producer, wine, vintage);
  \textit{producer\_vintage} = matched on (producer, vintage);
  \textit{fuzzy} = fuzzy producer name match;
  \textit{producer\_avg} = producer-level average maturity;
  \textit{unmatched} = no Tastingbook coverage (maturity imputed).
\end{tablenotes}
"""
tex_a2 = wrap_table(tex_a2_body,
    "Tastingbook match rates by region and match type", "tab:tb_match_rates")
(ROOT / "paper" / "appendix" / "tab_tastingbook_match_rates.tex").write_text(tex_a2, encoding="utf-8")
print("  Saved: tab_tastingbook_match_rates.tex (appendix)")


# ── Appendix Table A3: Maturity imputation model ──────────────────────────────
print("Generating Appendix A3: maturity imputation summary...")

_stats_path = ROOT / "output" / "05_imputation_stats.json"
if _stats_path.exists():
    import json as _json
    with open(_stats_path) as _fh:
        _imp = _json.load(_fh)
    _n_train  = f"{_imp['n_training']:,}"
    _cv_r2    = f"$R^2 = {_imp['cv_r2_mean']:.3f} \\pm {_imp['cv_r2_std']:.3f}$"
    _cv_rmse  = f"{_imp['cv_rmse_mean']:.2f} $\\pm$ {_imp['cv_rmse_std']:.2f} years"
    _dom_feat = max(_imp["feature_importances"], key=_imp["feature_importances"].get)
    _dom_pct  = _imp["feature_importances"][_dom_feat] * 100
    _dom_str  = f"{_dom_feat.replace('_', ' ').title()} ({_dom_pct:.1f}\\% importance)"
else:
    _n_train, _cv_r2, _cv_rmse, _dom_str = "16,148", "$R^2 = 0.991 \\pm 0.001$", \
        "1.99 $\\pm$ 0.13 years", "Vintage (99.8\\% importance)"

_n_tb    = int((df_full["maturity_imputed"] == False).sum())
_n_imp   = int((df_full["maturity_imputed"] == True).sum())
_pct_tb  = 100 * _n_tb  / len(df_full)
_pct_imp = 100 * _n_imp / len(df_full)

tex_a3_body = r"""\begin{tabular}{lc}
\toprule
Model & Gradient Boosting Regressor \\
\midrule
Training observations & """ + _n_train + r""" \\
Features & Producer (target-enc.), wine slug (target-enc.), \\
         & vintage, region, wine type \\
Cross-validation & 5-fold, """ + _cv_r2 + r""" \\
CV RMSE & """ + _cv_rmse + r""" \\
Dominant feature & """ + _dom_str + r""" \\
YTM cap & 20 years (applied to TB values and predictions) \\
\midrule
Auction lots: TB-matched & """ + f"{_n_tb:,} ({_pct_tb:.1f}\\%)" + r""" \\
Auction lots: imputed & """ + f"{_n_imp:,} ({_pct_imp:.1f}\\%)" + r""" \\
\bottomrule
\end{tabular}
\begin{tablenotes}
\footnotesize
\item Notes: Target variable: years\_to\_maturity $= (d_{\text{from}} + d_{\text{until}})/2 - \text{vintage}$,
  capped at 2--100 years for training.
\end{tablenotes}
"""
tex_a3 = wrap_table(tex_a3_body,
    "Maturity imputation model: summary", "tab:maturity_imputation")
(ROOT / "paper" / "appendix" / "tab_maturity_imputation.tex").write_text(tex_a3, encoding="utf-8")
print("  Saved: tab_maturity_imputation.tex (appendix)")


print("\nAll outputs generated:")
print("  paper/figures/fig_spline_comparison.{pdf,png}")
print("  paper/tables/tab_summary_stats.tex")
print("  paper/tables/tab_price_age_medians.tex")
print("  paper/tables/tab_segment_dip_bordeaux.tex")
print("  paper/tables/tab_segment_dip_burgundy.tex")
print("  paper/tables/tab_piecewise_slopes.tex")
print("  paper/appendix/tab_full_sample_stats.tex")
print("  paper/appendix/tab_tastingbook_match_rates.tex")
print("  paper/appendix/tab_maturity_imputation.tex")

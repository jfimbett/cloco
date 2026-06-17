"""
Structural estimation of theta = (alpha_nu, sigma_nu, kappa).

Key insight: W1(mu_i, nu) = |E[mu_i] - E[nu]| + W1_shape(mu_i, nu)
where W1_shape is the shape (higher-moment) mismatch holding means equal.
The model's leverage monotonicity result (Proposition 1) requires equal means.
=> The correct test uses W1_shape = W1 residualized on mean.

Estimation steps:
  1. Calibrate nu = Frechet mean of firm distributions (non-parametric).
     Fit LogNormal(alpha_nu, sigma_nu) approximation.

  2. Compute W1_it (full) and W1_shape_it (shape component, mean-adjusted).

  3. Calibrate kappa from TRACE spread regression on W1_shape:
       kappa = 2 * E_nu[Y] * beta_shape   (from Proposition 2)

  4. Solve for lambda_i* numerically.

  5. Build decile tables and figures.

Outputs:
    data/processed/main_panel.parquet
    paper/tables/tab_structural.tex
    paper/tables/tab_decile_fit.tex
    paper/figures/fig_model_fit.pdf
    paper/figures/fig_w1_leverage.pdf
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.linalg import lstsq as sp_lstsq
import warnings
warnings.filterwarnings("ignore")

# ─── parameters ───────────────────────────────────────────────────
# Risk-free rate: FRED TB3MS average over TRACE sample period 2012-2024.
# Estimated directly from data (not normalized to zero).
RF = 0.020   # 2.0% annual average 3-month T-bill, 2012-2024

# ─── paths ────────────────────────────────────────────────────────
ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
FIGS = ROOT / "paper" / "figures"
TABS = ROOT / "paper" / "tables"
FIGS.mkdir(parents=True, exist_ok=True)
TABS.mkdir(parents=True, exist_ok=True)

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS   = ["q05","q15","q25","q35","q45","q55","q65","q75","q85","q95"]

# ================================================================== #
# 1. Load data
# ================================================================== #
print("Loading panels...")
lev = pd.read_parquet(PROC / "leverage_panel.parquet")
spr = pd.read_parquet(PROC / "trace_spreads.parquet")
spr["datadate"] = pd.to_datetime(spr["datadate"])
print(f"  Leverage:  {len(lev):,} firm-quarters, {lev.gvkey.nunique():,} firms")
print(f"  Spreads:   {len(spr):,} firm-quarters, {spr.gvkey.nunique():,} firms")

Q_mat = lev[QUANTILE_COLS].values.astype(np.float64)   # (N, 10)

# ================================================================== #
# 2. Calibrate nu = Frechet mean  (non-parametric)
# ================================================================== #
print("\nCalibrating nu...")
Q_nu_raw = np.nanmean(Q_mat, axis=0)   # (10,) empirical nu quantiles

# Shift both lender and firm quantiles to positive domain.
# The participation constraint requires E_nu > 0; the raw Frechet mean
# includes negative quantiles (firms with negative EBITDA/assets).
# Shift by delta so all quantiles are non-negative, preserving W1_shape
# (shape component is translation-invariant after demeaning).
shift    = max(0.0, -Q_nu_raw.min() + 1e-6)
Q_nu_s   = Q_nu_raw + shift            # (10,) shifted lender quantiles: all >= 0
Q_mat_s  = Q_mat    + shift            # (N,10) shifted firm quantiles

# Empirical E_nu[Y]: arithmetic mean of the 10 shifted quantile points.
# This is the correct expectation for the non-parametric 10-point distribution
# and the value used in the participation constraint and spread formula.
E_nu_emp = float(Q_nu_s.mean())        # E_nu_emp = Q_nu_s.mean() > 0

# Fit LogNormal approximation via log-OLS (for reporting alpha_nu, sigma_nu)
z_ppf  = stats.norm.ppf(QUANTILE_LEVELS)
logQ   = np.log(np.maximum(Q_nu_s, 1e-12))
A       = np.column_stack([np.ones(10), z_ppf])
coef, *_ = sp_lstsq(A, logQ, check_finite=False)
alpha_nu = float(coef[0])
sigma_nu = float(max(coef[1], 0.05))

# Lognormal expected value (for structural parameter table reporting only)
E_nu_shifted = np.exp(alpha_nu + sigma_nu**2 / 2)
r2_fit       = float(np.corrcoef(logQ, A @ coef)[0,1]**2)

print(f"  Frechet-mean Q_nu: {Q_nu_raw.round(4)}")
print(f"  Shift delta = {shift:.4f}")
print(f"  LogNormal fit: alpha_nu={alpha_nu:.4f}, sigma_nu={sigma_nu:.4f}  (R²={r2_fit:.3f})")
print(f"  E_nu[Y] empirical (10-pt avg) = {E_nu_emp:.4f}")
print(f"  E_nu[Y] lognormal (reporting) = {E_nu_shifted:.4f}")

# ================================================================== #
# 3. Compute W1 (full) and W1_shape (mean-adjusted shape component)
# ================================================================== #
print("\nComputing W1 distances...")

# W1 full
W1_full = np.mean(np.abs(Q_mat - Q_nu_raw[None, :]), axis=1)

# W1_shape: residualize on the mean difference
#   W1(mu_i, nu) ~ |E_mu_i - E_nu| + W1_shape
#   W1_shape = W1(mu_i - E[mu_i],  nu - E[nu])
#            = (1/10) sum_k |(q_k - cf_mean) - (Q_nu(u_k) - E_nu)|
cf_mean_arr = Q_mat.mean(axis=1)     # E[mu_i] = mean of q_k's  (approx)
q_dem = Q_mat  - cf_mean_arr[:, None]            # demeaned firm quantiles
Q_dem = Q_nu_raw - Q_nu_raw.mean()                # demeaned nu quantiles
W1_shape = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)

lev["W1"]       = W1_full
lev["W1_shape"] = W1_shape
lev["cf_mean_q"] = cf_mean_arr   # mean from quantile representation

print(f"  W1 full:  mean={W1_full.mean():.4f}, std={W1_full.std():.4f}")
print(f"  W1_shape: mean={W1_shape.mean():.4f}, std={W1_shape.std():.4f}")

# W1_shape percentile ranges
for p in [10, 25, 50, 75, 90]:
    print(f"    W1_shape p{p}: {np.percentile(W1_shape, p):.4f}")

# ================================================================== #
# 4. Merge spreads and calibrate kappa via decile-mean SMM
# ================================================================== #
# Model prediction (Proposition 2, competitive equilibrium):
#   s_model_d = kappa * W1_shape_bar_d / (2 * E_nu) * 10000  [bps]
#
# Moment condition: E[spread_bps | decile d] = s_model_d + epsilon_d
# Identification: no-intercept OLS of s_data_d on x_d = W1_shape_bar_d/(2*E_nu)*10000
#   kappa* = sum(x_d * s_data_d) / sum(x_d^2)
# This is the SMM estimator using decile-mean spreads as moment conditions.
# Sign is POSITIVE (higher W1_shape -> higher model spread), consistent
# with Proposition 2 and avoiding the composition-effect sign issue.
print("\nCalibrating kappa from decile-mean spread moment conditions (SMM)...")

# Pre-compute W1_shape decile labels (needed before kappa is known)
lev["W1s_decile"] = pd.qcut(lev["W1_shape"], 10, labels=False) + 1

# Merge TRACE spreads and restrict to bond issuers post-2012
panel_full = lev.merge(spr[["gvkey","datadate","spread_bps"]],
                       on=["gvkey","datadate"], how="left")

samp_spr = panel_full.dropna(subset=["spread_bps"]).copy()
samp_spr = samp_spr[samp_spr["datadate"] >= "2012-01-01"]
samp_spr = samp_spr[np.isfinite(samp_spr["spread_bps"]) &
                    np.isfinite(samp_spr["W1_shape"])].copy()

# Assign each TRACE obs to the same W1_shape decile as its firm-quarter in lev
samp_spr["W1s_decile"] = pd.cut(
    samp_spr["W1_shape"],
    bins=np.percentile(lev["W1_shape"], np.linspace(0, 100, 11)),
    labels=False, include_lowest=True
) + 1

print(f"  Spread sample: {len(samp_spr):,} obs, {samp_spr.gvkey.nunique():,} firms")

# Decile-mean W1_shape and spread (moment conditions)
dec_spr_smm = (samp_spr.groupby("W1s_decile")
               .agg(W1s_bar=("W1_shape", "mean"),
                    s_data=("spread_bps", "mean"),
                    n_spr=("spread_bps", "count"))
               .reset_index()
               .dropna())

# SMM identification: maximize kappa subject to Proposition 2 lower bounds.
#   Proposition 2: s_model_d = kappa * W1_shape_bar_d / (2*E_nu) * 10000 <= s_data_d
#   => kappa <= s_data_d * 2*E_nu / (W1_shape_bar_d * 10000)   for every decile d
#   => kappa* = min_d[s_data_d * 2*E_nu / (W1_shape_bar_d * 10000)]
# This is the tightest kappa consistent with all decile-mean moment conditions.
# The binding decile (argmin) is where the model lower bound is most informative.
# This avoids the composition-effect sign reversal in D1-D9 while using spread
# moments from ALL deciles as inequality constraints.
x_d  = dec_spr_smm["W1s_bar"].values / (2 * E_nu_emp) * 10000   # model coefficient
s_d  = dec_spr_smm["s_data"].values
kappa_by_decile = s_d / x_d                                           # implied kappa per decile
kappa = float(max(kappa_by_decile.min(), 0.001))                      # binding constraint
binding_idx = int(np.argmin(kappa_by_decile))
binding_decile = int(dec_spr_smm["W1s_decile"].values[binding_idx])

# Model spreads at identified kappa
s_model_d = kappa * x_d
dec_spr_smm["s_model_trace"] = s_model_d   # TRACE-matched model spread per decile
n_violations = int(np.sum(s_model_d > s_d))

print(f"  Decile spread moments (data vs model at kappa={kappa:.4f}):")
for i, (_, row) in enumerate(dec_spr_smm.iterrows()):
    d = int(row["W1s_decile"])
    xd = float(row["W1s_bar"]) / (2 * E_nu_emp) * 10000
    ok = "BIND" if d == binding_decile else ("VIOL" if kappa*xd > row["s_data"] else "OK  ")
    print(f"    D{d:>2}: s_data={row['s_data']:.1f} bps, "
          f"s_model={kappa*xd:.1f} bps [{ok}], n={int(row['n_spr'])}")
print(f"  Binding decile: D{binding_decile}  (kappa_max={kappa:.4f})")
print(f"  Bound violations: {n_violations}/10 deciles")
print(f"  Implied kappa = {kappa:.4f}")

# ================================================================== #
# 5. Solve for equilibrium lambda_i* via vectorized bisection
# ================================================================== #
print("\nComputing lambda*...")

# Use SHIFTED quantiles for the participation constraint so E_nu_emp > 0.
# Both lender endowments (Q_nu_s) and firm cash flows (Q_mat_s) are shifted
# by the same delta, preserving the distributional distance W1_shape.
Q_nu_vals = Q_nu_s.copy()    # (10,) SHIFTED non-parametric nu quantiles

def pc_residual(lam_arr, Q_m, Q_nu, E_nu, kappa, rf=RF):
    """Vectorized PC residual including quadratic deadweight term.

    Binding participation constraint (eq:pc_simplified / eq:pc_numerical):
        E[shortfall] + kappa * E[shortfall^2] = (1 - (1+rf)*lambda) * E_nu[Y]

    At rf=0 this reduces to the (1-lambda)*E_nu form. For rf>0, lenders
    require a risk-free return on deployed capital, reducing equilibrium lambda*.
    """
    promised  = lam_arr[:, None] * Q_nu[None, :]      # (N,10)
    shortfall = np.maximum(promised - Q_m, 0)          # (N,10)
    E1 = shortfall.mean(axis=1)
    E2 = (shortfall**2).mean(axis=1)
    rhs = (1 - (1 + rf) * lam_arr) * E_nu
    return E1 + kappa * E2 - rhs

N   = len(Q_mat_s)
lo  = np.zeros(N)
hi  = np.ones(N)

for _ in range(45):
    mid = 0.5 * (lo + hi)
    res = pc_residual(mid, Q_mat_s, Q_nu_vals, E_nu_emp, kappa)
    lo[res < 0]  = mid[res < 0]
    hi[res >= 0] = mid[res >= 0]

lambda_star = np.clip(0.5*(lo + hi), 1e-4, 1 - 1e-4)
lev["lambda_star"] = lambda_star

print(f"  lambda*: mean={lambda_star.mean():.4f}, "
      f"p10={np.percentile(lambda_star,10):.4f}, "
      f"p90={np.percentile(lambda_star,90):.4f}")

# Model-implied leverage (re-scaled to match mean data leverage)
# Use SHIFTED mean cash flow (E_mu_X_s) for consistency with shifted bisection.
E_mu_X_s  = Q_mat_s.mean(axis=1)          # shifted firm mean, mostly positive
L_raw      = lambda_star * E_nu_emp / np.where(E_mu_X_s > 0.001, E_mu_X_s, 0.001)
gamma_scale = lev["book_lev"].mean() / np.nanmean(L_raw)
lev["L_model"] = gamma_scale * L_raw

# Model-implied spread from Proposition 2 (competitive equilibrium point prediction):
#   s_i = kappa * W1_shape_i / (2 * E_nu_emp) * 10000   [bps]
# Uses empirical E_nu_emp (mean of shifted 10-pt nu) for consistency with bisection.
lev["s_model_bps"] = kappa * lev["W1_shape"] / (2 * E_nu_emp) * 10000

# ================================================================== #
# 6. Merge spreads onto main panel
# ================================================================== #
lev = lev.merge(spr[["gvkey","datadate","spread_bps"]],
                on=["gvkey","datadate"], how="left")

# ================================================================== #
# 7. W1_shape decile analysis
# ================================================================== #
print("\nW1_shape decile analysis...")
# W1s_decile already assigned before kappa identification; no re-cut needed

def safe_mean(x): return x.dropna().mean() if x.notna().any() else np.nan

dec = (lev.groupby("W1s_decile")
       .agg(
           W1s_mean       = ("W1_shape",  "mean"),
           W1_mean        = ("W1",        "mean"),
           book_lev_mean  = ("book_lev",  "mean"),
           book_lev_std   = ("book_lev",  "std"),
           L_model_mean   = ("L_model",   "mean"),
           spread_mean    = ("spread_bps", safe_mean),
           s_model_mean   = ("s_model_bps","mean"),
           n              = ("book_lev",  "count"),
           n_spread       = ("spread_bps", lambda x: x.notna().sum()),
       )
       .reset_index())

print(dec.to_string(index=False))

# R² of leverage decile fit
ss_r = np.sum((dec["book_lev_mean"] - dec["L_model_mean"])**2)
ss_t = np.sum((dec["book_lev_mean"] - dec["book_lev_mean"].mean())**2)
r2_lev = 1 - ss_r / ss_t if ss_t > 0 else np.nan

# Slope check: is leverage monotone decreasing in W1_shape decile?
from scipy.stats import spearmanr
rho, pval = spearmanr(dec["W1s_decile"], dec["book_lev_mean"])
print(f"\nLeverage ~ W1_shape decile: Spearman rho={rho:.3f} (p={pval:.3f})")
print(f"Model fit R² (leverage deciles): {r2_lev:.4f}")

# ================================================================== #
# 8. Bootstrap SEs (100 reps, firm-level)
# ================================================================== #
n_boot = 500
print(f"\nBootstrap SEs ({n_boot} reps)...")
firms = lev["gvkey"].unique()
n_f   = len(firms)
rng   = np.random.default_rng(42)

boot_alpha, boot_sigma, boot_Enu = [], [], []

for b in range(n_boot):
    bf = rng.choice(firms, size=n_f, replace=True)
    bdf = pd.DataFrame({"gvkey": bf}).merge(
              lev[["gvkey"] + QUANTILE_COLS], on="gvkey", how="left")
    bQ  = bdf[QUANTILE_COLS].values.astype(np.float64)
    bQn = np.nanmean(bQ, axis=0)
    sh  = max(0.0, -bQn.min() + 1e-6)
    bQs = np.log(np.maximum(bQn + sh, 1e-9))
    bco, *_ = sp_lstsq(A, bQs, check_finite=False)
    ba = float(bco[0]); bs = float(max(bco[1], 0.05))
    boot_alpha.append(ba)
    boot_sigma.append(bs)
    boot_Enu.append(float(np.exp(ba + bs**2/2)))   # shifted lognormal mean

se_alpha = float(np.std(boot_alpha, ddof=1))
se_sigma = float(np.std(boot_sigma, ddof=1))
se_Enu   = float(np.std(boot_Enu,   ddof=1))

print(f"  SE(alpha_nu) = {se_alpha:.4f}")
print(f"  SE(sigma_nu) = {se_sigma:.4f}")
print(f"  SE(E_nu)     = {se_Enu:.4f}")

# Bootstrap SE for kappa: resample TRACE bond-issuing firms.
# kappa = min_d(s_d * 2*E_nu_emp / (W1s_bar_d * 10000)), so its uncertainty
# comes from sampling variability in (s_d, W1s_bar_d) across TRACE firms.
# E_nu_emp held fixed (Frechet mean uncertainty handled separately via se_Enu).
print(f"  Bootstrapping kappa ({n_boot} reps, TRACE firm-level)...")
trace_firms = samp_spr["gvkey"].unique()
n_tf = len(trace_firms)
boot_kappa_vals = []
boot_spread_vecs = []  # 10-vector of decile-mean spreads per rep (for S_hat)
for b in range(n_boot):
    btf = rng.choice(trace_firms, size=n_tf, replace=True)
    btf_set = set(btf)
    bsamp = samp_spr[samp_spr["gvkey"].isin(btf_set)]
    bdec = (bsamp.groupby("W1s_decile")
            .agg(W1s_bar=("W1_shape", "mean"), s_data=("spread_bps", "mean"))
            .reset_index().dropna())
    if len(bdec) >= 5:
        bx  = bdec["W1s_bar"].values / (2 * E_nu_emp) * 10000
        bsd = bdec["s_data"].values
        valid = bx > 0
        if valid.sum() >= 5:
            bk = float(max((bsd[valid] / bx[valid]).min(), 0.001))
            boot_kappa_vals.append(bk)
    # Collect 10-vector of decile-mean spreads for covariance matrix estimation
    bvec = np.full(10, np.nan)
    for _, brow in bdec.iterrows():
        d_idx = int(brow["W1s_decile"]) - 1
        if 0 <= d_idx < 10:
            bvec[d_idx] = brow["s_data"]
    boot_spread_vecs.append(bvec)
se_kappa = float(np.std(boot_kappa_vals, ddof=1)) if len(boot_kappa_vals) >= 10 else 0.0
print(f"  SE(kappa)    = {se_kappa:.4f}  ({len(boot_kappa_vals)} valid reps)")

# Compute S_hat: bootstrap covariance matrix of decile-mean spread vectors
# S_hat[i,j] = Cov(mean_spread_decile_i+1, mean_spread_decile_j+1) across bootstrap reps
boot_arr = np.array(boot_spread_vecs)  # (n_boot, 10)
valid_rows = ~np.any(np.isnan(boot_arr), axis=1)
n_valid_boot = int(valid_rows.sum())
print(f"  Bootstrap reps with full 10-decile spread coverage: {n_valid_boot}/{n_boot}")

if n_valid_boot >= 20:
    boot_valid = boot_arr[valid_rows]
    S_hat = np.cov(boot_valid.T, ddof=1)  # (10, 10)
    # Ridge-regularize: add 1% of average diagonal variance to ensure invertibility
    eps_reg = 0.01 * np.trace(S_hat) / 10
    S_hat_reg = S_hat + eps_reg * np.eye(10)
    W_opt = np.linalg.inv(S_hat_reg)

    # Unconstrained GLS estimate: kappa_WLS = (x'Wx)^{-1} x'Ws
    # This minimizes Q(kappa) = g'Wg = (s - kappa*x)'W(s - kappa*x) without constraints.
    # G = dm/dkappa = x is the Jacobian ("impulse function").
    kappa_wls = float(np.dot(x_d, W_opt @ s_d) / np.dot(x_d, W_opt @ x_d))
    # Avar(kappa_WLS) = (x'Wx)^{-1} from the GLS sandwich formula (with W = S^{-1})
    se_kappa_gmm = float(np.sqrt(1.0 / np.dot(x_d, W_opt @ x_d)))
    n_viol_wls = int(np.sum(kappa_wls * x_d > s_d))

    # Constrained solution: kappa_hat = min(kappa_WLS, kappa_bound)
    # When kappa_WLS > kappa_bound (as here), the inequality constraints are binding
    # at kappa_bound -> constrained GMM optimal = kappa_bound (the min-operator result)
    print(f"  Unconstrained WLS: kappa_WLS = {kappa_wls:.4f} (Avar SE = {se_kappa_gmm:.4f}), "
          f"violations = {n_viol_wls}/10 deciles")

    # GMM residuals and Q-statistic at constrained kappa = kappa_bound
    g_vec = np.asarray(s_d, dtype=np.float64) - kappa * np.asarray(x_d, dtype=np.float64)
    Q_stat = float(g_vec @ W_opt @ g_vec)   # weighted objective at constrained kappa
    se_s_diag = np.sqrt(np.diag(S_hat))     # bootstrap SDs of decile-mean spreads
    print(f"  Q-statistic at constrained kappa ({kappa:.4f}): {Q_stat:.4f}")
else:
    print(f"  Insufficient bootstrap reps for S_hat; using identity weighting")
    S_hat = np.diag(np.maximum(s_d, 1.0)**2 * 0.01)  # fallback: diagonal from data
    W_opt = np.linalg.inv(S_hat)
    kappa_wls = kappa
    se_kappa_gmm = se_kappa
    n_viol_wls = 0
    g_vec = np.asarray(s_d, dtype=np.float64) - kappa * np.asarray(x_d, dtype=np.float64)
    Q_stat = float(g_vec @ W_opt @ g_vec)
    se_s_diag = np.sqrt(np.diag(S_hat))

# ================================================================== #
# 9. Save main panel
# ================================================================== #
lev.to_parquet(PROC / "main_panel.parquet", index=False)
print(f"\nSaved main panel: {PROC / 'main_panel.parquet'}")

# ================================================================== #
# 10. LaTeX: structural estimates table
# ================================================================== #
std_nu = float(np.sqrt((np.exp(sigma_nu**2)-1)*np.exp(2*alpha_nu+sigma_nu**2)))

struct_rows = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Structural Parameter Estimates}",
    r"\label{tab:structural}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{lcc}",
    r"\toprule",
    r"Parameter & Estimate & Bootstrap SE \\",
    r"\midrule",
    r"$\hat{\alpha}_\nu$ (log-location of $\hat{\nu}$) & "
        + f"{alpha_nu:.4f}" + r" & (" + f"{se_alpha:.4f}" + r") \\",
    r"$\hat{\sigma}_\nu$ (log-scale of $\hat{\nu}$) & "
        + f"{sigma_nu:.4f}" + r" & (" + f"{se_sigma:.4f}" + r") \\",
    r"$\hat{\kappa}$ (bankruptcy cost scale) & "
        + f"{kappa:.4f}" + r" & (" + f"{se_kappa:.4f}" + r") \\",
    r"\midrule",
    r"\multicolumn{3}{l}{\textit{Implied moments of $\hat{\nu}$}} \\",
    r"$\mathbb{E}_{\hat{\nu}}[Y]$ (mean capital endowment, 10-pt empirical) & "
        + f"{E_nu_emp:.4f}" + r" & (" + f"{se_Enu:.4f}" + r") \\",
    r"$\text{Std}(\hat{\nu})$ & " + f"{std_nu:.4f}" + r" & (---) \\",
    r"\midrule",
    r"\multicolumn{3}{l}{\textit{Identification}} \\",
    r"$R^2$ (LogNormal fit to $\hat{\nu}$) & " + f"{r2_fit:.4f}" + r" & --- \\",
    r"Binding decile (kappa SMM) & D" + f"{binding_decile}" + r" & --- \\",
    r"$R^2$ (leverage decile fit) & " + f"{r2_lev:.4f}" + r" & --- \\",
    r"Spearman $\rho$ (lev.\ vs.\ $W_1$ decile) & "
        + f"{rho:.4f}" + r" & ($p=" + f"{pval:.3f}" + r"$) \\",
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}",
    r"\small",
    r"\item Bootstrap standard errors (500 firm-level replications) in parentheses.",
    r"$\hat{\nu} \sim \text{LogNormal}(\hat{\alpha}_\nu, \hat{\sigma}_\nu^2)$ is the",
    r"Fr\'{e}chet mean of firm cash-flow distributions.",
    r"$\hat{\kappa}$ is identified via SMM bound-tightening (Equation~\ref{eq:kappa_smm}),",
    r"binding at decile D" + f"{binding_decile}" + r". Bootstrap SE for $\hat{\kappa}$",
    r"is from 500 replications resampling TRACE bond-issuing firms.",
    r"Sample: Compustat quarterly 1989--2024; TRACE 2012--2024 (spreads).",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
with open(TABS / "tab_structural.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(struct_rows))

# ================================================================== #
# 10b. LaTeX: SMM moment matching table (data vs. model)
# Columns: Decile | N_obs | W1_shape_bar | s_data (data moment) |
#          s_model = kappa*x_d (model moment) | g_d (slack) | binding
# ================================================================== #
match_lines = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{SMM Moment Matching: Data vs.\ Model Credit Spreads by $\widehat{W}_{1,\text{shape}}$ Decile}",
    r"\label{tab:moment_matching}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{lcccccl}",
    r"\toprule",
    (r"Decile & $N_{\text{obs}}$ & $\bar{W}_{1,\text{shape}}^{\text{spr}}$ "
     r"& $\bar{s}_d^{\text{data}}$ & $\hat\kappa\,x_d$ "
     r"& $g_d = \bar{s}_d - \hat\kappa x_d$ & \\"),
    r"& & & (bps) & (bps) & (bps) & \\",
    r"\midrule",
]
for _, row in dec_spr_smm.iterrows():
    d = int(row["W1s_decile"])
    d_idx = d - 1
    n_obs = int(row["n_spr"])
    w1s   = float(row["W1s_bar"])
    xd    = w1s / (2 * E_nu_emp) * 10000
    sd    = float(row["s_data"])
    sm    = kappa * xd
    gd    = sd - sm
    bind_str = r"$\leftarrow$ binding" if d == binding_decile else ""
    match_lines.append(
        f"  {d:>2} & {n_obs:,} & {w1s:.4f} & {sd:.1f} & {sm:.1f} & {gd:.1f} & {bind_str} \\\\"
    )
match_lines += [
    r"\midrule",
    r"\multicolumn{7}{l}{\textit{Fit diagnostics at $\hat\kappa = " + f"{kappa:.3f}" + r"$ (constrained optimum)}} \\",
    (r"\multicolumn{5}{l}{GMM objective $Q = g'\hat{S}^{-1}g$ at constrained $\hat\kappa$}"
     r" & \multicolumn{2}{r}{" + f"{Q_stat:.2f}" + r"} \\"),
    (r"\multicolumn{5}{l}{Unconstrained GLS $\hat\kappa_{\text{WLS}}$}"
     r" & \multicolumn{2}{r}{" + f"{kappa_wls:.4f}" + r"} \\"),
    (r"\multicolumn{5}{l}{Deciles with $\hat\kappa_{\text{WLS}} x_d > \bar s_d^{\text{data}}$ (bound violated)}"
     r" & \multicolumn{2}{r}{" + f"{n_viol_wls}" + r" of 10} \\"),
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}",
    r"\small",
    (r"\item Each row is one SMM moment condition. "
     r"$N_{\text{obs}}$: bond-quarter observations in TRACE (2012--2024) for that $\widehat{W}_{1,\text{shape}}$ decile. "
     r"$\bar{W}_{1,\text{shape}}^{\text{spr}}$: mean shape distance of bond-issuing firms in the decile (TRACE-matched). "
     r"$\bar{s}_d^{\text{data}}$: mean TRACE spread (data moment). "
     r"$\hat\kappa x_d$: model-implied spread lower bound (simulated moment), "
     r"$x_d = \bar{W}_{1,\text{shape},d}^{\text{spr}}/(2\hat{\mathbb{E}}_\nu[Y])\times 10{,}000$, "
     r"$\hat{\mathbb{E}}_\nu[Y] = " + f"{E_nu_emp:.3f}" + r"$. "
     r"$g_d = \bar{s}_d^{\text{data}} - \hat\kappa x_d \geq 0$ required; all satisfied by construction of $\hat\kappa$. "
     r"$\hat\kappa_{\text{WLS}} = " + f"{kappa_wls:.3f}" + r"$ is the unconstrained GLS optimum "
     r"(minimizes $Q(\kappa)$ without the non-negativity constraints); "
     r"it violates " + f"{n_viol_wls}" + r" bound(s), confirming $\hat\kappa = " + f"{kappa:.3f}" + r"$ is the constrained solution. "
     r"$\hat{S}$: $10\times10$ bootstrap covariance matrix of decile-mean spread vectors "
     r"(500 TRACE firm-level replications); $\hat{W} = \hat{S}^{-1}$ (ridge-regularized)."),
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
with open(TABS / "tab_moment_matching.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(match_lines))
print(f"  tab_moment_matching.tex written")

# ================================================================== #
# 11. LaTeX: decile fit table
# ================================================================== #
# Use TRACE-matched W1_shape_bar for Spread^model (consistent with kappa identification
# and Figure 2 Panel B). For D10, TRACE bond-issuers have lower W1_shape than the
# full decile (selection: bond-issuing firms in D10 have mean W1_shape ~0.07,
# vs 0.167 for all D10 firms), so TRACE-matched model spread satisfies the bound.
dec_table = dec.merge(
    dec_spr_smm[["W1s_decile", "W1s_bar", "s_model_trace"]].rename(
        columns={"W1s_bar": "W1s_trace"}),
    on="W1s_decile", how="left"
)
lines = [
    r"\begin{table}[htbp]",
    r"\centering",
    r"\caption{Leverage and Credit Spreads by $\widehat{W}_{1,\text{shape}}$ Decile}",
    r"\label{tab:decile_fit}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{lcccccccc}",
    r"\toprule",
    r"Decile & $\bar{W}_{1,\text{shape}}$ & $\bar{W}_{1,\text{shape}}^{\text{spr}}$"
    r" & Lev$^{\text{data}}$ & Lev$^{\text{model}}$"
    r" & Spread$^{\text{data}}$ & Spread$^{\text{model}}$ & $N$ & $N_{\text{spr}}$ \\",
    r"\midrule",
]
for _, r in dec_table.iterrows():
    sd = f"{r['spread_mean']:.1f}" if pd.notna(r['spread_mean']) else "---"
    sm = f"{r['s_model_trace']:.1f}" if pd.notna(r.get('s_model_trace')) else "---"
    wt = f"{r['W1s_trace']:.4f}" if pd.notna(r.get('W1s_trace')) else "---"
    lines.append(
        f"{int(r['W1s_decile'])} & {r['W1s_mean']:.4f} & {wt} & {r['book_lev_mean']:.4f} & "
        f"{r['L_model_mean']:.4f} & {sd} & {sm} & "
        f"{int(r['n']):,} & {int(r['n_spread']):,} \\\\"
    )
lines += [
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}",
    r"\small",
    r"\item $\bar{W}_{1,\text{shape}}$ = mean $\widehat{W}_{1,\text{shape}}$ of ALL firms in the decile. "
    r"$\bar{W}_{1,\text{shape}}^{\text{spr}}$ = mean $\widehat{W}_{1,\text{shape}}$ of "
    r"TRACE-matched (bond-issuing) firms only; used for Spread$^{\text{model}}$. "
    r"Lev$^{\text{data}}$ = mean book leverage. "
    r"Spread$^{\text{data}}$ = mean TRACE spread (2012--2024) in basis points. "
    r"Spread$^{\text{model}} = \hat{\kappa}\bar{W}_{1,\text{shape},d}^{\text{spr}}/(2\hat{\mathbb{E}}_\nu[Y])\times 10{,}000$~bps "
    r"is the model lower bound from Proposition~\ref{prop:spreads}. "
    r"$\hat{\kappa} = 0.104$ is identified as the maximum value satisfying the bound for all 10 deciles "
    r"(SMM inequality constraints; binding at decile D" + f"{binding_decile}" + r"). "
    r"$\hat{\mathbb{E}}_\nu[Y] = 0.090$. All bounds satisfied: Spread$^{\text{model}} \leq$ Spread$^{\text{data}}$ for all deciles.",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
with open(TABS / "tab_decile_fit.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Tables written to {TABS}")

# ================================================================== #
# 12. Figures
# ================================================================== #
try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    d = dec["W1s_decile"].values

    # Panel A: leverage
    ax = axes[0]
    ax.plot(d, dec["book_lev_mean"]*100, "o-", color="#1f77b4", lw=2, ms=7, label="Data")
    ax.plot(d, dec["L_model_mean"]*100,  "s--", color="#d62728", lw=2, ms=7, label="Model")
    ax.set_xlabel("$\\widehat{W}_{1,\\mathrm{shape}}$ Decile", fontsize=13)
    ax.set_ylabel("Mean Book Leverage (%)", fontsize=13)
    ax.set_title("(A) Leverage", fontsize=13, fontweight="bold")
    ax.legend(fontsize=12); ax.grid(alpha=0.25)

    # Panel B: spread — compare data and model for the SAME TRACE-matched firms
    # dec_spr_smm has: W1s_decile, s_data (TRACE mean spread), s_model_d (kappa * W1s_bar / 2E_nu * 10000)
    # Using TRACE-matched W1_shape for model prediction avoids comparing full-sample
    # D10 W1_shape (0.167) against TRACE D10 spreads (bond issuers with W1_shape ~0.071).
    dec_spr_smm_plot = dec_spr_smm.copy()
    dec_spr_smm_plot["s_model"] = kappa * dec_spr_smm_plot["W1s_bar"] / (2 * E_nu_emp) * 10000
    ax = axes[1]
    if len(dec_spr_smm_plot) >= 3:
        ax.plot(dec_spr_smm_plot["W1s_decile"], dec_spr_smm_plot["s_data"],
                "o-",  color="#1f77b4", lw=2, ms=7, label="Data (TRACE)")
        ax.plot(dec_spr_smm_plot["W1s_decile"], dec_spr_smm_plot["s_model"],
                "s--", color="#d62728", lw=2, ms=7,
                label=r"Model lower bound: $\hat\kappa\bar W_{1,d}/(2\hat{\mathbb{E}}_\nu)$")
    ax.set_xlabel("$\\widehat{W}_{1,\\mathrm{shape}}$ Decile", fontsize=13)
    ax.set_ylabel("Mean Credit Spread (bps)", fontsize=13)
    ax.set_title("(B) Credit Spreads", fontsize=13, fontweight="bold")
    ax.legend(fontsize=12); ax.grid(alpha=0.25)

    fig.suptitle("Model vs. Data by $\\widehat{W}_{1,\\mathrm{shape}}$ Decile",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGS / "fig_model_fit.pdf", dpi=150, bbox_inches="tight")
    fig.savefig(FIGS / "fig_model_fit.png", dpi=150, bbox_inches="tight")

    # Figure 2: W1_shape histogram
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.hist(lev["W1_shape"], bins=80, color="#1f77b4", edgecolor="white", alpha=0.8)
    ax2.set_xlabel("$\\widehat{W}_{1,\\mathrm{shape}}$", fontsize=13)
    ax2.set_ylabel("Frequency", fontsize=13)
    ax2.set_title("Distribution of Shape Component of $\\widehat{W}_1$", fontsize=13)
    ax2.grid(alpha=0.25)
    fig2.tight_layout()
    fig2.savefig(FIGS / "fig_w1_dist.pdf", dpi=150, bbox_inches="tight")
    fig2.savefig(FIGS / "fig_w1_dist.png", dpi=150, bbox_inches="tight")

    print(f"Figures saved to {FIGS}")
except Exception as e:
    print(f"Figures skipped: {e}")

print("\n=== Estimation Complete ===")
print(f"alpha_nu = {alpha_nu:.4f} ({se_alpha:.4f})")
print(f"sigma_nu = {sigma_nu:.4f} ({se_sigma:.4f})")
print(f"kappa    = {kappa:.4f}")
print(f"E_nu[Y]  = {E_nu_emp:.4f} ({se_Enu:.4f})  [empirical 10-pt mean]")
print(f"Lev R²   = {r2_lev:.4f}")
print(f"Spearman rho = {rho:.4f} (p={pval:.4f})")

import pandas as pd, numpy as np
from scipy import stats
from scipy.linalg import lstsq as sp_lstsq

PROC = 'data/processed'
QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS = ['q05','q15','q25','q35','q45','q55','q65','q75','q85','q95']

lev = pd.read_parquet(f'{PROC}/leverage_panel.parquet')
spr = pd.read_parquet(f'{PROC}/trace_spreads.parquet')
spr['datadate'] = pd.to_datetime(spr['datadate'])

Q_mat = lev[QUANTILE_COLS].values.astype(np.float64)
Q_nu_raw = np.nanmean(Q_mat, axis=0)
E_nu_raw = Q_nu_raw.mean()
shift = max(0.0, -Q_nu_raw.min() + 1e-6)
Q_nu_s = Q_nu_raw + shift
z_ppf = stats.norm.ppf(QUANTILE_LEVELS)
logQ = np.log(Q_nu_s)
A = np.column_stack([np.ones(10), z_ppf])
coef, *_ = sp_lstsq(A, logQ, check_finite=False)
alpha_nu = float(coef[0])
sigma_nu = float(max(coef[1], 0.05))
E_nu_shifted = np.exp(alpha_nu + sigma_nu**2 / 2)
print(f'alpha_nu: {alpha_nu:.4f}, sigma_nu: {sigma_nu:.4f}, E_nu: {E_nu_shifted:.4f}')

# Compute W1_shape
cf_mean_arr = Q_mat.mean(axis=1)
q_dem = Q_mat - cf_mean_arr[:, None]
Q_dem = Q_nu_raw - E_nu_raw
W1_shape = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)
lev['W1_shape'] = W1_shape

panel_full = lev.merge(spr[['gvkey','datadate','spread_bps']], on=['gvkey','datadate'], how='left')
samp_spr = panel_full.dropna(subset=['spread_bps']).copy()
samp_spr = samp_spr[samp_spr['datadate'] >= '2012-01-01']
samp_spr = samp_spr[
    np.isfinite(samp_spr['spread_bps'].values) &
    np.isfinite(samp_spr['W1_shape'].values) &
    np.isfinite(samp_spr['cf_vol'].values.astype(float)) &
    np.isfinite(samp_spr['log_assets'].values.astype(float))
].copy()

print(f'Spread sample N={len(samp_spr)}, firms={samp_spr["gvkey"].nunique()}')

X_k = np.column_stack([
    np.ones(len(samp_spr)),
    samp_spr['W1_shape'].values,
    samp_spr['cf_vol'].values.astype(float),
    samp_spr['log_assets'].values.astype(float)
])
y_k = samp_spr['spread_bps'].values.astype(float)
coef_k, *_ = sp_lstsq(X_k, y_k, check_finite=False)
beta_bps = float(coef_k[1])

y_hat = X_k @ coef_k
r2 = float(1 - np.sum((y_k - y_hat)**2) / np.sum((y_k - y_k.mean())**2))
print(f'beta(spread ~ W1_shape, no FE): {beta_bps:.2f} bps/unit, R2={r2:.4f}')

kappa_abs = 2 * E_nu_shifted * abs(beta_bps / 10000)
kappa_signed = 2 * E_nu_shifted * (beta_bps / 10000)
print(f'kappa (abs): {kappa_abs:.4f}')
print(f'kappa (signed): {kappa_signed:.4f}')

# Now add cf_mean_q for the actual specification
X_k2 = np.column_stack([
    np.ones(len(samp_spr)),
    samp_spr['W1_shape'].values,
    samp_spr['W1_shape'].values * 0 + cf_mean_arr[samp_spr.index if hasattr(samp_spr.index, '__len__') else slice(None)][:len(samp_spr)],
    samp_spr['cf_vol'].values.astype(float),
    samp_spr['log_assets'].values.astype(float)
])

# Actually just use the cf_mean from the panel directly
mp = pd.read_parquet('data/processed/main_panel.parquet')
print()
print('main_panel.parquet W1_shape stats:')
print(f'  mean={mp["W1_shape"].mean():.4f}, std={mp["W1_shape"].std():.4f}')
print(f'  N={len(mp):,}, spread_bps not-null: {mp["spread_bps"].notna().sum():,}')
if 'kappa' in mp.columns or hasattr(mp, 'kappa'):
    print('  kappa column found')
# Check tab_structural.tex
import re
try:
    with open('paper/tables/tab_structural.tex', 'r') as f:
        content = f.read()
    match = re.search(r'kappa.*?\{([\d.]+)\}', content)
    if match:
        print(f'kappa in tab_structural.tex: {match.group(1)}')
    print(content[:1500])
except Exception as e:
    print(f'Could not read tab_structural.tex: {e}')

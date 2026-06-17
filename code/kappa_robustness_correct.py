"""
Correct kappa robustness: using the ACTUAL specification (with cf_mean_q).
Baseline beta = -4243 bps. Check sensitivity to additional controls.
"""
import pandas as pd, numpy as np
from scipy.linalg import lstsq as sp_lstsq
from scipy import stats

QUANTILE_LEVELS = np.array([(2*k-1)/20 for k in range(1, 11)])
QUANTILE_COLS = ['q05','q15','q25','q35','q45','q55','q65','q75','q85','q95']
E_nu = 0.5316

lev = pd.read_parquet('data/processed/leverage_panel.parquet')
lev['datadate'] = pd.to_datetime(lev['datadate'])
Q_mat = lev[QUANTILE_COLS].values.astype(np.float64)
Q_nu_raw = np.nanmean(Q_mat, axis=0)
E_nu_raw = Q_nu_raw.mean()

# W1_shape (exact same as in estimation code)
cf_mean_q = Q_mat.mean(axis=1)
q_dem = Q_mat - cf_mean_q[:, None]
Q_dem = Q_nu_raw - E_nu_raw
W1_shape = np.mean(np.abs(q_dem - Q_dem[None, :]), axis=1)
lev['W1_shape'] = W1_shape
lev['cf_mean_q'] = cf_mean_q

spr = pd.read_parquet('data/processed/trace_spreads.parquet')
spr['datadate'] = pd.to_datetime(spr['datadate'])

panel = lev.merge(spr[['gvkey','datadate','spread_bps']], on=['gvkey','datadate'], how='left')
samp = panel.dropna(subset=['spread_bps']).copy()
samp = samp[samp['datadate'] >= '2012-01-01']
samp = samp[
    np.isfinite(samp['spread_bps'].values) &
    np.isfinite(samp['W1_shape'].values) &
    np.isfinite(samp['cf_mean_q'].values) &
    np.isfinite(samp['cf_vol'].values.astype(float)) &
    np.isfinite(samp['log_assets'].values.astype(float))
].copy()

print(f'Spread sample: N={len(samp)}, firms={samp["gvkey"].nunique()}')

def run_spread_reg(samp_in, extra_cols=[]):
    X = np.column_stack([
        np.ones(len(samp_in)),
        samp_in['W1_shape'].values.astype(float),
        samp_in['cf_mean_q'].values.astype(float),
        samp_in['cf_vol'].values.astype(float),
        samp_in['log_assets'].values.astype(float),
    ] + [samp_in[c].values.astype(float) for c in extra_cols])
    y = samp_in['spread_bps'].values.astype(float)
    coef, *_ = sp_lstsq(X, y, cond=None)
    yhat = X @ coef
    r2 = float(1 - np.sum((y-yhat)**2) / np.sum((y-y.mean())**2))
    beta = float(coef[1])
    kappa = 2 * E_nu * abs(beta / 10000)
    return beta, r2, kappa

beta_base, r2_base, kappa_base = run_spread_reg(samp)
print(f'\nBaseline (W1_shape, cf_mean_q, cf_vol, log_assets):')
print(f'  beta = {beta_base:.2f} bps, R2={r2_base:.4f}, kappa = {kappa_base:.4f}')

# With profitability and tangibility
s2 = samp[np.isfinite(samp['profitability'].values.astype(float)) & np.isfinite(samp['tangibility'].values.astype(float))].copy()
beta_pt, r2_pt, kappa_pt = run_spread_reg(s2, ['profitability','tangibility'])
print(f'\nWith profitability + tangibility:')
print(f'  beta = {beta_pt:.2f} bps, change = {(beta_pt-beta_base)/abs(beta_base)*100:.1f}%, kappa = {kappa_pt:.4f}')

# With SIC2 industry FE (using dummies)
if any(c in samp.columns for c in ['sic2', 'sich', 'sic']):
    sic_col = 'sic2' if 'sic2' in samp.columns else ('sich' if 'sich' in samp.columns else 'sic')
    samp['sic2_code'] = (samp[sic_col].fillna(-1).astype(float) // 10).astype(int)
    sics = np.sort(samp['sic2_code'].unique())
    sic_dummies = np.zeros((len(samp), len(sics)-1), dtype=float)  # omit first
    for j, s in enumerate(sics[1:]):
        sic_dummies[:, j] = (samp['sic2_code'] == s).values.astype(float)

    X_sic = np.column_stack([
        np.ones(len(samp)),
        samp['W1_shape'].values.astype(float),
        samp['cf_mean_q'].values.astype(float),
        samp['cf_vol'].values.astype(float),
        samp['log_assets'].values.astype(float),
        sic_dummies
    ])
    y = samp['spread_bps'].values.astype(float)
    coef_sic, *_ = sp_lstsq(X_sic, y, cond=None)
    yhat_sic = X_sic @ coef_sic
    r2_sic = float(1 - np.sum((y-yhat_sic)**2) / np.sum((y-y.mean())**2))
    beta_sic = float(coef_sic[1])
    kappa_sic = 2 * E_nu * abs(beta_sic / 10000)
    print(f'\nWith SIC2 industry FE:')
    print(f'  beta = {beta_sic:.2f} bps, change = {(beta_sic-beta_base)/abs(beta_base)*100:.1f}%, kappa = {kappa_sic:.4f}')
else:
    print('\nSIC column not found - checking available columns...')
    print([c for c in samp.columns if 'sic' in c.lower()])

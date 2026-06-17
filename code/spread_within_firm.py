"""
Within-firm spread regression on W1_shape.
Tests whether within-firm increases in W1_shape are associated with higher spreads.
If beta_FE > 0, the sign is consistent with the structural model.
"""
import pandas as pd, numpy as np
from scipy.linalg import lstsq as sp_lstsq

df = pd.read_parquet('data/processed/main_panel.parquet')

# TRACE subsample
samp = df[df['spread_bps'].notna() & df['W1_shape'].notna() &
          df['cf_mean'].notna() & df['cf_vol'].notna() & df['log_assets'].notna()].copy()
samp['yt'] = samp['year'].astype(str) + '_' + samp['quarter'].astype(str) if ('year' in samp.columns and 'quarter' in samp.columns) else samp['datadate'].dt.to_period('Q').astype(str)

print(f'TRACE sample: N={len(samp):,}, firms={samp["gvkey"].nunique()}')
print(f'Spread bps: mean={samp["spread_bps"].mean():.1f}, std={samp["spread_bps"].std():.1f}')
print(f'W1_shape: mean={samp["W1_shape"].mean():.4f}, std={samp["W1_shape"].std():.4f}')

COLS = ['spread_bps', 'W1_shape', 'cf_mean', 'cf_vol', 'log_assets']

# Demean by firm and year-quarter
def demean(sub, cols):
    sub = sub.copy()
    for col in cols:
        fm = sub.groupby('gvkey')[col].transform('mean').values
        tm = sub.groupby('yt')[col].transform('mean').values
        gm = float(sub[col].mean())
        sub[col+'_dm'] = sub[col].values.astype(float) - fm - tm + gm
    return sub

samp = demean(samp, COLS)

X_cols = ['W1_shape', 'cf_mean', 'cf_vol', 'log_assets']
X = np.column_stack([np.ones(len(samp))] + [samp[c+'_dm'].values.astype(float) for c in X_cols])
y = samp['spread_bps_dm'].values.astype(float)

coef, *_ = sp_lstsq(X, y, cond=None)
beta_FE = coef[1]
resid = y - X @ coef
r2 = float(1 - np.sum(resid**2) / np.sum((y - y.mean())**2))

# Cluster SE at firm level
firms = samp['gvkey'].values
ufirms = np.unique(firms)
scores = np.zeros((len(ufirms), X.shape[1]))
for i, f in enumerate(ufirms):
    idx = np.where(firms == f)[0]
    scores[i] = (X[idx] * resid[idx, None]).sum(axis=0)
XtX_inv = np.linalg.pinv(X.T @ X)
G, n, k = len(ufirms), len(samp), X.shape[1]
adj = (G/(G-1)) * ((n-1)/(n-k))
cov = adj * XtX_inv @ (scores.T @ scores) @ XtX_inv
se = np.sqrt(np.diag(cov))

print(f'\n--- Within-firm spread regression (firm + year-quarter FE) ---')
print(f'beta(W1_shape): {beta_FE:.2f} bps/unit  (SE={se[1]:.2f}, t={beta_FE/se[1]:.2f})')
print(f'R2: {r2:.4f}')
print(f'')
print(f'Implied kappa from within-firm: {abs(2 * 0.5316 * beta_FE/10000):.4f}')
print(f'Sign: {"POSITIVE (consistent with model)" if beta_FE > 0 else "NEGATIVE (opposite to model)"}')

# OLS comparison (no FE)
X_ols = np.column_stack([np.ones(len(samp))] + [samp[c].values.astype(float) for c in X_cols])
y_ols = samp['spread_bps'].values.astype(float)
coef_ols, *_ = sp_lstsq(X_ols, y_ols, cond=None)
beta_ols = coef_ols[1]
r2_ols = float(1 - np.sum((y_ols - X_ols@coef_ols)**2) / np.sum((y_ols - y_ols.mean())**2))
print(f'\n--- OLS (no FE, TRACE subsample) ---')
print(f'beta(W1_shape): {beta_ols:.2f} bps/unit')
print(f'R2: {r2_ols:.4f}')

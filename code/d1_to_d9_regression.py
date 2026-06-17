"""
Within-firm leverage regression on D1-D9 subsample (excluding extreme right tail, W1_shape decile 10).
Also reports within-firm spread regression for the TRACE subsample.
"""
import pandas as pd, numpy as np
from scipy.linalg import lstsq as sp_lstsq

df = pd.read_parquet('data/processed/main_panel.parquet')
LCOLS = ['book_lev', 'W1_shape', 'cf_mean', 'cf_vol', 'log_assets', 'mtb', 'profitability', 'tangibility']

mask = np.ones(len(df), dtype=bool)
for c in LCOLS:
    mask &= df[c].notna().values
dfa = df[mask].copy().reset_index(drop=True)
for c in LCOLS:
    dfa[c] = dfa[c].astype(float)
if 'yt' not in dfa.columns:
    dfa['yt'] = pd.PeriodIndex(dfa['datadate'], freq='Q').astype(str)

# Exclude decile 10 (top 10% of W1_shape)
p90 = float(dfa['W1_shape'].quantile(0.90))
d1to9 = dfa[dfa['W1_shape'] <= p90].copy().reset_index(drop=True)

print(f'Full sample: N={len(dfa):,}, firms={dfa["gvkey"].nunique()}, p90(W1_shape)={p90:.4f}')
print(f'D1-D9 (excl top 10%): N={len(d1to9):,}, firms={d1to9["gvkey"].nunique()}')

def within_coef(sub, ycol, xcols):
    sub = sub.copy().reset_index(drop=True)
    allcols = [ycol] + xcols
    for col in allcols:
        fm = sub.groupby('gvkey')[col].transform('mean').values
        tm = sub.groupby('yt')[col].transform('mean').values
        gm = float(sub[col].mean())
        sub[col+'_dm'] = sub[col].values - fm - tm + gm
    X = np.column_stack([np.ones(len(sub))] + [sub[c+'_dm'].values for c in xcols])
    y = sub[ycol+'_dm'].values
    coef, *_ = sp_lstsq(X, y, cond=None)
    resid = y - X @ coef
    firms = sub['gvkey'].values
    ufirms = np.unique(firms)
    scores = np.zeros((len(ufirms), X.shape[1]))
    for i, f in enumerate(ufirms):
        idx = np.where(firms == f)[0]
        scores[i] = (X[idx] * resid[idx, None]).sum(axis=0)
    XtX_inv = np.linalg.pinv(X.T @ X)
    G, n, k = len(ufirms), len(sub), X.shape[1]
    cov = (G/(G-1)) * ((n-1)/(n-k)) * XtX_inv @ (scores.T @ scores) @ XtX_inv
    se = np.sqrt(np.diag(cov))
    return float(coef[1]), float(se[1]), float(coef[1]/se[1]), len(sub), int(sub['gvkey'].nunique())

# Leverage regression: D1-D9
xcols_lev = ['W1_shape', 'cf_mean', 'cf_vol', 'log_assets', 'mtb', 'profitability', 'tangibility']
b_all, se_all, t_all, n_all, g_all = within_coef(dfa, 'book_lev', xcols_lev)
b_d1to9, se_d1to9, t_d1to9, n_d1to9, g_d1to9 = within_coef(d1to9, 'book_lev', xcols_lev)

print(f'\n=== Leverage regression ===')
print(f'Full sample (D1-D10): beta={b_all:.4f}, SE={se_all:.4f}, t={t_all:.2f}, N={n_all:,}, G={g_all}')
print(f'D1-D9 only:           beta={b_d1to9:.4f}, SE={se_d1to9:.4f}, t={t_d1to9:.2f}, N={n_d1to9:,}, G={g_d1to9}')
print(f'')
wfsd = float(dfa.groupby('gvkey')['book_lev'].std().mean())
print(f'Within-firm SD of book leverage: ~{wfsd:.4f}')
print(f'1 SD (0.075) effect in D1-D9: {abs(b_d1to9)*0.075:.4f} pp = {abs(b_d1to9)*0.075/wfsd*100:.1f}% of within-firm SD')

# Within-firm spread regression (TRACE subsample)
SCOLS = ['spread_bps', 'W1_shape', 'cf_mean', 'cf_vol', 'log_assets']
smask = np.ones(len(df), dtype=bool)
for c in SCOLS:
    smask &= df[c].notna().values
sdf = df[smask].copy().reset_index(drop=True)
for c in SCOLS:
    sdf[c] = sdf[c].astype(float)
if 'yt' not in sdf.columns:
    sdf['yt'] = pd.PeriodIndex(sdf['datadate'], freq='Q').astype(str)

xcols_spr = ['W1_shape', 'cf_mean', 'cf_vol', 'log_assets']
b_spr, se_spr, t_spr, n_spr, g_spr = within_coef(sdf, 'spread_bps', xcols_spr)
print(f'\n=== Within-firm spread regression (TRACE, firm+year FE) ===')
print(f'beta(W1_shape): {b_spr:.2f} bps/unit, SE={se_spr:.2f}, t={t_spr:.2f}')
print(f'N={n_spr:,}, firms={g_spr}')
print(f'W1_shape SD within TRACE sample: {sdf["W1_shape"].std():.4f}')
print(f'W1_shape within-firm variation: {float(sdf.groupby("gvkey")["W1_shape"].std().mean()):.4f}')

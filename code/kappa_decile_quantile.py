"""
Identify kappa from the 10th percentile of TRACE spreads by W1_shape decile.
The model says: s_i >= kappa * W1_shape_i / (2 * E_nu[Y])
=> The minimum spread (10th percentile) should be proportional to W1_shape mean.
This is a direct test of the lower-bound prediction.
"""
import pandas as pd, numpy as np
from scipy.linalg import lstsq as sp_lstsq

df = pd.read_parquet('data/processed/main_panel.parquet')
samp = df[df['spread_bps'].notna() & df['W1_shape'].notna()].copy()
E_nu = 0.5316

# Use the full-sample W1_shape deciles (same as main decile table)
samp['decile'] = pd.qcut(samp['W1_shape'], 10, labels=False) + 1

# By decile: mean W1_shape and 10th/25th/50th percentile of spread
result = samp.groupby('decile').agg(
    W1_mean=('W1_shape', 'mean'),
    spread_p10=('spread_bps', lambda x: x.quantile(0.10)),
    spread_p25=('spread_bps', lambda x: x.quantile(0.25)),
    spread_p50=('spread_bps', lambda x: x.quantile(0.50)),
    spread_mean=('spread_bps', 'mean'),
    N=('spread_bps', 'count'),
    N_trace=('spread_bps', lambda x: x.notna().sum())
).reset_index()

print('Decile | W1_mean | p10-spread | p25-spread | mean-spread | N | N_trace')
for _, r in result.iterrows():
    print(f"  {int(r['decile'])}   | {r['W1_mean']:.4f}  | {r['spread_p10']:.1f} bps     | {r['spread_p25']:.1f} bps    | {r['spread_mean']:.1f} bps    | {int(r['N'])} | {int(r['N_trace'])}")

# Identify kappa from 10th percentile: p10 = kappa * W1_mean / (2*E_nu) * 10000
# => kappa = p10 * 2 * E_nu / (W1_mean * 10000)  per decile
# => or run OLS: p10 = beta * W1_mean, then kappa = beta * 2 * E_nu / 10000

trace_only = result[result['N_trace'] > 10].copy()

# OLS through origin: p10_spread = beta * W1_mean
X = trace_only['W1_mean'].values[:, None]
y_p10 = trace_only['spread_p10'].values
coef_p10, *_ = sp_lstsq(X, y_p10, cond=None)
beta_p10 = float(coef_p10[0])
kappa_p10 = 2 * E_nu * beta_p10 / 10000

y_p25 = trace_only['spread_p25'].values
coef_p25, *_ = sp_lstsq(X, y_p25, cond=None)
beta_p25 = float(coef_p25[0])
kappa_p25 = 2 * E_nu * beta_p25 / 10000

print(f'\n--- kappa from 10th percentile (OLS through origin) ---')
print(f'beta: {beta_p10:.2f} bps/unit')
print(f'kappa_p10 = {kappa_p10:.4f}')

print(f'\n--- kappa from 25th percentile (OLS through origin) ---')
print(f'beta: {beta_p25:.2f} bps/unit')
print(f'kappa_p25 = {kappa_p25:.4f}')

# Per-decile kappa implied by p10 bound
print('\nPer-decile kappa implied by 10th pctile bound:')
for _, r in trace_only.iterrows():
    k_dec = r['spread_p10'] * 2 * E_nu / (r['W1_mean'] * 10000)
    print(f"  D{int(r['decile'])}: W1={r['W1_mean']:.4f}, p10={r['spread_p10']:.1f} bps, kappa_implied={k_dec:.4f}")

# What does the MODEL predict for decile-specific lower bounds with kappa=0.4511?
kappa_paper = 0.4511
print(f'\nModel lower bounds with kappa={kappa_paper}:')
for _, r in result.iterrows():
    lb = kappa_paper * r['W1_mean'] / (2 * E_nu) * 10000
    print(f"  D{int(r['decile'])}: bound={lb:.1f} bps, actual p10={r['spread_p10']:.1f} bps, above_floor={'YES' if r['spread_p10'] > lb else 'NO'}")

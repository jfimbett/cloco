import pandas as pd, numpy as np

df = pd.read_parquet('data/processed/main_panel.parquet')
trace = df[df['spread_bps'].notna() & df['W1_shape'].notna()].copy()
print(f'TRACE-matched N={len(trace):,}, firms={trace["gvkey"].nunique()}')

trace['decile'] = pd.qcut(trace['W1_shape'], 10, labels=False) + 1
kappa = 0.4511; Enu = 0.5316

result = trace.groupby('decile').agg(
    W1_mean=('W1_shape','mean'),
    spread_mean=('spread_bps','mean'),
    N=('spread_bps','size')
).reset_index()
result['spread_bound'] = kappa * result['W1_mean'] / (2*Enu) * 10000
result['bound_over_actual'] = result['spread_bound'] / result['spread_mean']

print()
print('Decile | W1_shape | Spread_data | Spread_bound | Bound/Data | N')
for _, r in result.iterrows():
    d = int(r['decile'])
    w = r['W1_mean']
    sd = r['spread_mean']
    sb = r['spread_bound']
    bo = r['bound_over_actual']
    n = int(r['N'])
    print(f'  {d}   | {w:.4f}   | {sd:.1f} bps   | {sb:.1f} bps  | {bo:.2f}  | {n}')

# Also check if bound < actual for all deciles
all_below = (result['spread_bound'] < result['spread_mean']).all()
print(f'\nAll model bounds below actual TRACE spreads: {all_below}')
print(f'Max bound/actual ratio: {result["bound_over_actual"].max():.3f}')

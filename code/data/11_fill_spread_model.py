"""
Fill model-implied spread column in tab_decile_fit.tex.
Model lower bound: s_model = kappa * W1_shape / (2 * E_nu[Y]) * 10000  [in bps]
Output: updates paper/tables/tab_decile_fit.tex
"""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np

# Structural parameters from estimation
kappa = 0.2119
E_nu = 1.4984  # mean capital endowment (shifted scale)

# Decile data (from tab_decile_fit.tex)
deciles = [
    {'decile': 1,  'W1_shape': 0.0161, 'lev_data': 0.1625, 'spread_data': 326.4, 'N': 69847, 'N_spr': 902},
    {'decile': 2,  'W1_shape': 0.0240, 'lev_data': 0.1743, 'spread_data': 252.4, 'N': 69847, 'N_spr': 1379},
    {'decile': 3,  'W1_shape': 0.0295, 'lev_data': 0.1859, 'spread_data': 246.0, 'N': 69846, 'N_spr': 1773},
    {'decile': 4,  'W1_shape': 0.0341, 'lev_data': 0.2040, 'spread_data': 237.4, 'N': 69847, 'N_spr': 2522},
    {'decile': 5,  'W1_shape': 0.0383, 'lev_data': 0.2196, 'spread_data': 214.6, 'N': 69846, 'N_spr': 2995},
    {'decile': 6,  'W1_shape': 0.0423, 'lev_data': 0.2367, 'spread_data': 224.7, 'N': 69847, 'N_spr': 3475},
    {'decile': 7,  'W1_shape': 0.0465, 'lev_data': 0.2518, 'spread_data': 241.5, 'N': 69846, 'N_spr': 3832},
    {'decile': 8,  'W1_shape': 0.0512, 'lev_data': 0.2727, 'spread_data': 281.4, 'N': 69847, 'N_spr': 4199},
    {'decile': 9,  'W1_shape': 0.0593, 'lev_data': 0.2530, 'spread_data': 295.7, 'N': 69846, 'N_spr': 2852},
    {'decile': 10, 'W1_shape': 0.2696, 'lev_data': 0.1134, 'spread_data': 557.7, 'N': 69847, 'N_spr': 126},
]

df = pd.DataFrame(deciles)

# Model lower bound on spread: s_min = kappa * W1_shape / (2 * E_nu) * 10000 bps
df['spread_model_lb'] = kappa * df['W1_shape'] / (2 * E_nu) * 10000

print("Decile  W1_shape  Spread_data  Spread_model_lb")
for _, r in df.iterrows():
    print(f"  {int(r['decile']):2d}    {r['W1_shape']:.4f}     {r['spread_data']:.1f}          {r['spread_model_lb']:.1f}")

# Write updated table
lines = [
    r'\begin{table}[htbp]',
    r'\centering',
    r'\caption{Leverage and Credit Spreads by $\widehat{W}_{1,\text{shape}}$ Decile}',
    r'\label{tab:decile_fit}',
    r'\begin{threeparttable}',
    r'\begin{tabular}{lccccccc}',
    r'\toprule',
    r'Decile & $\bar{W}_{1,\text{shape}}$ & Lev$^{\text{data}}$ & Lev$^{\text{model}}$ & Spread$^{\text{data}}$ & Spread$^{\text{lb}}$ & $N$ & $N_{\text{spr}}$ \\',
    r'\midrule',
]

# From estimation script, these are the model-implied leverage values:
lev_model = [0.1711, 0.1835, 0.1907, 0.1901, 0.2012, 0.2136, 0.2366, 0.2804, 0.3655, 0.0413]

for i, r in df.iterrows():
    lm = lev_model[i]
    lines.append(
        f"{int(r['decile'])} & {r['W1_shape']:.4f} & {r['lev_data']:.4f} & {lm:.4f} & "
        f"{r['spread_data']:.1f} & {r['spread_model_lb']:.1f} & "
        f"{int(r['N']):,} & {int(r['N_spr']):,} \\\\"
    )

lines += [
    r'\bottomrule',
    r'\end{tabular}',
    r'\begin{tablenotes}[flushleft]',
    r'\small',
    (r'\item $\widehat{W}_{1,\text{shape}}$ is the mean-adjusted shape component of the Wasserstein-1 '
     r'distance. Lev$^{\text{data}}$ = mean book leverage. Spread$^{\text{data}}$ = mean TRACE spread '
     r'(2012--2024) in bps. Spread$^{\text{lb}} = \hat{\kappa}\bar{W}_{1,\text{shape}} / '
     r'(2\hat{\mathbb{E}}_\nu[Y]) \times 10{,}000$ is the model-implied lower bound on equilibrium spreads '
     r'from Proposition~\ref{prop:spreads}. Lev$^{\text{model}}$ = model-implied book leverage '
     r'from calibrated structural parameters.'),
    r'\end{tablenotes}',
    r'\end{threeparttable}',
    r'\end{table}',
]

with open('paper/tables/tab_decile_fit.tex', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("\nUpdated paper/tables/tab_decile_fit.tex")

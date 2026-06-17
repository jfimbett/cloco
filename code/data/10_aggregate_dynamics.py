"""
Aggregate distributional dynamics figure.
Plots cross-sectional W1_shape distribution over time vs. aggregate leverage.
Output: paper/figures/fig_aggregate_w1.pdf
"""
import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

print("Loading main panel...")
df = pd.read_parquet('data/processed/main_panel.parquet')
df = df.dropna(subset=['W1_shape', 'book_lev'])

# Parse date from year and quarter
if 'datadate' in df.columns:
    df['date'] = pd.to_datetime(df['datadate'], errors='coerce')
elif 'year' in df.columns and 'quarter' in df.columns:
    df['date'] = pd.to_datetime(df['year'].astype(str) + 'Q' + df['quarter'].astype(str))
else:
    # Fallback: try to infer from columns
    print("Available columns:", df.columns.tolist()[:20])
    raise ValueError("Cannot find date column")

df = df.dropna(subset=['date'])
df['yrqtr'] = df['date'].dt.to_period('Q')
print(f"Panel: {len(df):,} obs, {df['yrqtr'].nunique()} quarters")

# Aggregate by quarter
grp = df.groupby('yrqtr')
qtr_median_w1 = grp['W1_shape'].median()
qtr_q25_w1 = grp['W1_shape'].quantile(0.25)
qtr_q75_w1 = grp['W1_shape'].quantile(0.75)
qtr_lev = grp['book_lev'].median()

# Convert period index to timestamps for plotting
idx = qtr_median_w1.index.to_timestamp()

# NBER recession dates (approximate quarter boundaries)
recessions = [
    ('1990-07', '1991-03'),
    ('2001-03', '2001-11'),
    ('2007-12', '2009-06'),
    ('2020-02', '2020-04'),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
fig.suptitle('', fontsize=1)

# --- Left panel: W1_shape distribution over time ---
ax1.fill_between(idx, qtr_q25_w1.values, qtr_q75_w1.values,
                 alpha=0.25, color='steelblue', label='IQR')
ax1.plot(idx, qtr_median_w1.values, color='steelblue', linewidth=1.6, label='Median')

for r_start, r_end in recessions:
    try:
        ts = pd.Timestamp(r_start)
        te = pd.Timestamp(r_end)
        if ts >= idx.min() and te <= idx.max():
            ax1.axvspan(ts, te, alpha=0.12, color='gray')
    except Exception:
        pass

ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel(r'$\widehat{W}_{1,\mathrm{shape}}$', fontsize=11)
ax1.set_title('Cross-sectional Distribution of Distributional Mismatch', fontsize=9)
ax1.legend(fontsize=9, frameon=False)
ax1.tick_params(labelsize=9)

# --- Right panel: median W1_shape vs. aggregate book leverage ---
color_w1 = 'steelblue'
color_lev = 'firebrick'

ax2b = ax2.twinx()

for r_start, r_end in recessions:
    try:
        ts = pd.Timestamp(r_start)
        te = pd.Timestamp(r_end)
        if ts >= idx.min() and te <= idx.max():
            ax2.axvspan(ts, te, alpha=0.12, color='gray')
    except Exception:
        pass

lw1, = ax2.plot(idx, qtr_median_w1.values, color=color_w1, linewidth=1.6,
                label=r'Median $\widehat{W}_{1,\mathrm{shape}}$ (left)')
llev, = ax2b.plot(idx, qtr_lev.values, color=color_lev, linewidth=1.4,
                  linestyle='--', label='Median book leverage (right)')

ax2.set_xlabel('Year', fontsize=10)
ax2.set_ylabel(r'$\widehat{W}_{1,\mathrm{shape}}$', color=color_w1, fontsize=11)
ax2b.set_ylabel('Book leverage', color=color_lev, fontsize=11)
ax2.tick_params(axis='y', labelcolor=color_w1, labelsize=9)
ax2b.tick_params(axis='y', labelcolor=color_lev, labelsize=9)
ax2.tick_params(axis='x', labelsize=9)
ax2.set_title('Distributional Mismatch vs. Aggregate Leverage', fontsize=9)

handles = [lw1, llev]
labels = [h.get_label() for h in handles]
ax2.legend(handles, labels, fontsize=8, frameon=False, loc='upper left')

plt.tight_layout()
fig.savefig('paper/figures/fig_aggregate_w1.pdf', bbox_inches='tight', dpi=200)
fig.savefig('paper/figures/fig_aggregate_w1.png', bbox_inches='tight', dpi=150)
print("Saved: paper/figures/fig_aggregate_w1.pdf")

# Print a few summary stats for the text
print("\nAggregate dynamics summary:")
crisis = {'2001': ('2001-01', '2001-12'),
          '2008-09': ('2008-01', '2010-06'),
          '2020': ('2020-01', '2021-01')}
for label, (s, e) in crisis.items():
    mask = (idx >= s) & (idx <= e)
    if mask.sum() > 0:
        pre_mask = (idx >= pd.Timestamp(s) - pd.DateOffset(years=2)) & (idx < s)
        pre_val = qtr_median_w1.values[pre_mask].mean() if pre_mask.sum() > 0 else np.nan
        crisis_val = qtr_median_w1.values[mask].max()
        print(f"  {label}: pre-crisis W1_shape={pre_val:.4f}, peak={crisis_val:.4f}, "
              f"change={crisis_val - pre_val:.4f}")

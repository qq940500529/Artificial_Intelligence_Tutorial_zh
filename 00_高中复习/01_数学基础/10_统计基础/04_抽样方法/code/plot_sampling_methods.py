# 文件：code/plot_sampling_methods.py
# 用途：可视化四种抽样方法的直观对比
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------- 输出路径 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'sampling_methods.png')

# ---------- 全局样式 ----------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)
N = 60  # population size

fig, axes = plt.subplots(2, 2, figsize=(11, 10))

def setup_ax(ax, title):
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Generate grid positions for dots
xs = np.repeat(np.arange(10), 6)[:N]
ys = np.tile(np.arange(6), 10)[:N]
# Add small jitter
xs_j = xs + np.random.uniform(-0.15, 0.15, N)
ys_j = ys + np.random.uniform(-0.15, 0.15, N)

# ========== Top-left: Simple Random Sampling ==========
ax = axes[0, 0]
setup_ax(ax, 'Simple Random Sampling')
sample_idx = np.random.choice(N, size=15, replace=False)
mask = np.zeros(N, dtype=bool)
mask[sample_idx] = True
ax.scatter(xs_j[~mask], ys_j[~mask], s=60, c='#BDC3C7', edgecolors='#95A5A6',
           linewidth=0.5, zorder=2, label='Population')
ax.scatter(xs_j[mask], ys_j[mask], s=80, c='#E74C3C', edgecolors='#C0392B',
           linewidth=1, zorder=3, label='Sample (random)')
ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.text(4.5, -0.3, f'Selected {mask.sum()} / {N} at random', ha='center',
        fontsize=9, color='#555555')

# ========== Top-right: Systematic Sampling ==========
ax = axes[0, 1]
setup_ax(ax, 'Systematic Sampling')
k = 4
start = 1
sys_idx = np.arange(start, N, k)
mask_sys = np.zeros(N, dtype=bool)
mask_sys[sys_idx] = True
ax.scatter(xs_j[~mask_sys], ys_j[~mask_sys], s=60, c='#BDC3C7',
           edgecolors='#95A5A6', linewidth=0.5, zorder=2, label='Population')
ax.scatter(xs_j[mask_sys], ys_j[mask_sys], s=80, c='#3498DB',
           edgecolors='#2471A3', linewidth=1, zorder=3,
           label=f'Every {k}th (start={start})')
ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.text(4.5, -0.3, f'Selected {mask_sys.sum()} / {N} with interval k={k}',
        ha='center', fontsize=9, color='#555555')

# ========== Bottom-left: Stratified Sampling ==========
ax = axes[1, 0]
setup_ax(ax, 'Stratified Sampling')
strata_colors_pop = ['#F5B7B1', '#AED6F1', '#A9DFBF']
strata_colors_sel = ['#E74C3C', '#2980B9', '#27AE60']
strata_labels = ['Stratum A', 'Stratum B', 'Stratum C']
strata_assign = np.array([0] * 20 + [1] * 20 + [2] * 20)[:N]

for s in range(3):
    s_mask = strata_assign == s
    s_idx = np.where(s_mask)[0]
    # Select proportional sample from each stratum
    n_sel = 5
    sel = np.random.choice(s_idx, size=n_sel, replace=False)
    not_sel = np.setdiff1d(s_idx, sel)
    ax.scatter(xs_j[not_sel], ys_j[not_sel], s=60, c=strata_colors_pop[s],
               edgecolors='#95A5A6', linewidth=0.5, zorder=2)
    ax.scatter(xs_j[sel], ys_j[sel], s=80, c=strata_colors_sel[s],
               edgecolors='black', linewidth=1, zorder=3, label=strata_labels[s])

ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.text(4.5, -0.3, 'Proportional selection from each stratum', ha='center',
        fontsize=9, color='#555555')

# ========== Bottom-right: Cluster Sampling ==========
ax = axes[1, 1]
setup_ax(ax, 'Cluster Sampling')

# Assign dots into 4 clusters based on spatial regions
cluster_assign = np.zeros(N, dtype=int)
for i in range(N):
    if xs[i] < 5 and ys[i] < 3:
        cluster_assign[i] = 0
    elif xs[i] >= 5 and ys[i] < 3:
        cluster_assign[i] = 1
    elif xs[i] < 5 and ys[i] >= 3:
        cluster_assign[i] = 2
    else:
        cluster_assign[i] = 3

selected_cluster = 2  # randomly select cluster 2
cluster_colors_pop = ['#D5DBDB', '#D5DBDB', '#D5DBDB', '#D5DBDB']
cluster_colors_sel = ['#D5DBDB', '#D5DBDB', '#F39C12', '#D5DBDB']

# Draw cluster boundaries
for c, (xmin, xmax, ymin, ymax, lbl) in enumerate([
    (-0.4, 4.4, -0.4, 2.4, 'Cluster 1'),
    (4.6, 9.4, -0.4, 2.4, 'Cluster 2'),
    (-0.4, 4.4, 2.6, 5.4, 'Cluster 3'),
    (4.6, 9.4, 2.6, 5.4, 'Cluster 4'),
]):
    color = '#F39C12' if c == selected_cluster else '#CCCCCC'
    lw = 2.5 if c == selected_cluster else 1
    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                          fill=False, edgecolor=color, linewidth=lw,
                          linestyle='--' if c != selected_cluster else '-',
                          zorder=1)
    ax.add_patch(rect)
    tx = (xmin + xmax) / 2
    ty = ymax + 0.15 if ymax < 5 else ymin - 0.15
    va = 'bottom' if ymax < 5 else 'top'
    ax.text(tx, ty, lbl, ha='center', va=va, fontsize=8, color='#555555')

for c in range(4):
    c_mask = cluster_assign == c
    if c == selected_cluster:
        ax.scatter(xs_j[c_mask], ys_j[c_mask], s=80, c='#F39C12',
                   edgecolors='#D68910', linewidth=1, zorder=3,
                   label='Selected cluster')
    else:
        ax.scatter(xs_j[c_mask], ys_j[c_mask], s=60, c='#BDC3C7',
                   edgecolors='#95A5A6', linewidth=0.5, zorder=2)

ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.text(4.5, -0.3, 'Entire cluster selected at random', ha='center',
        fontsize=9, color='#555555')

plt.tight_layout(h_pad=2.0)
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}')

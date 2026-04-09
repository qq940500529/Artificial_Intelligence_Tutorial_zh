# 文件：code/plot_central_tendency.py
# 用途：对比对称分布与右偏分布中平均数、中位数、众数的位置差异
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------- 输出路径 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'central_tendency.png')

# ---------- 全局样式 ----------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ========== 左图：对称分布 ==========
ax = axes[0]
data_sym = np.random.normal(loc=50, scale=8, size=100)
data_sym = np.round(data_sym).astype(int)

mean_val = np.mean(data_sym)
median_val = np.median(data_sym)
# Mode: most frequent value
values, counts = np.unique(data_sym, return_counts=True)
mode_val = values[np.argmax(counts)]

ax.hist(data_sym, bins=15, color='#5B9BD5', edgecolor='white', alpha=0.8, zorder=2)
ax.axvline(mean_val, color='#E74C3C', linewidth=2.5, linestyle='-', label=f'Mean = {mean_val:.1f}', zorder=3)
ax.axvline(median_val, color='#2ECC71', linewidth=2.5, linestyle='--', label=f'Median = {median_val:.1f}', zorder=3)
ax.axvline(mode_val, color='#F39C12', linewidth=2.5, linestyle=':', label=f'Mode = {mode_val}', zorder=3)

ax.set_title('Symmetric Distribution', fontsize=14, fontweight='bold', pad=10)
ax.set_xlabel('Value', fontsize=11)
ax.set_ylabel('Frequency', fontsize=11)
ax.legend(fontsize=10, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# ========== 右图：右偏分布（含异常值） ==========
ax = axes[1]
data_skew = np.random.exponential(scale=10, size=85)
data_skew = np.clip(data_skew, 1, 40)
outliers = np.array([65, 72, 80, 85, 90, 95, 78, 70, 88, 75,
                     82, 92, 68, 77, 83])
data_skew = np.concatenate([data_skew, outliers])
data_skew = np.round(data_skew, 1)

mean_val2 = np.mean(data_skew)
median_val2 = np.median(data_skew)
values2, counts2 = np.unique(np.round(data_skew).astype(int), return_counts=True)
mode_val2 = values2[np.argmax(counts2)]

ax.hist(data_skew, bins=20, color='#C8A2C8', edgecolor='white', alpha=0.8, zorder=2)
ax.axvline(mean_val2, color='#E74C3C', linewidth=2.5, linestyle='-', label=f'Mean = {mean_val2:.1f}', zorder=3)
ax.axvline(median_val2, color='#2ECC71', linewidth=2.5, linestyle='--', label=f'Median = {median_val2:.1f}', zorder=3)
ax.axvline(mode_val2, color='#F39C12', linewidth=2.5, linestyle=':', label=f'Mode $\\approx$ {mode_val2}', zorder=3)

ax.annotate('Mean pulled\nby outliers',
            xy=(mean_val2, 0), xytext=(mean_val2 + 8, ax.get_ylim()[1] * 0.5 if ax.get_ylim()[1] > 0 else 8),
            fontsize=9, color='#E74C3C', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5))

ax.set_title('Right-Skewed Distribution (with outliers)', fontsize=14, fontweight='bold', pad=10)
ax.set_xlabel('Value', fontsize=11)
ax.set_ylabel('Frequency', fontsize=11)
ax.legend(fontsize=10, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}')

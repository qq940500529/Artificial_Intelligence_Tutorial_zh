"""
文件：code/plot_lines.py
用途：绘制直线方程的多种表示形式对比图
依赖：matplotlib>=3.5, numpy>=1.21
运行：python code/plot_lines.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

# === 图1：四种直线形式 ===
fig, axes = plt.subplots(2, 2, figsize=(10, 9))

x = np.linspace(-2, 6, 300)

# 点斜式：过 (1,2)，斜率 k=2
ax = axes[0, 0]
y1 = 2 * (x - 1) + 2
ax.plot(x, y1, 'b-', linewidth=2, label='$y - 2 = 2(x - 1)$')
ax.plot(1, 2, 'ro', markersize=8, zorder=5)
ax.annotate('$(1, 2)$', xy=(1, 2), xytext=(1.5, 1), fontsize=11,
            arrowprops=dict(arrowstyle='->', color='red'))
ax.set_title('Point-Slope Form', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(-2, 5)
ax.set_ylim(-3, 10)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 斜截式：y = 2x + 1
ax = axes[0, 1]
y2 = 2 * x + 1
ax.plot(x, y2, 'g-', linewidth=2, label='$y = 2x + 1$')
ax.plot(0, 1, 'ro', markersize=8, zorder=5)
ax.annotate('intercept $(0, 1)$', xy=(0, 1), xytext=(1.5, 0), fontsize=11,
            arrowprops=dict(arrowstyle='->', color='red'))
ax.set_title('Slope-Intercept Form', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(-2, 5)
ax.set_ylim(-3, 10)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 一般式：2x - y + 1 = 0
ax = axes[1, 0]
y3 = 2 * x + 1
ax.plot(x, y3, 'm-', linewidth=2, label='$2x - y + 1 = 0$')
ax.fill_between(x, y3, 10, alpha=0.1, color='magenta')
ax.set_title('General Form', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(-2, 5)
ax.set_ylim(-3, 10)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 两点式：过 (1,2) 和 (3,6)
ax = axes[1, 1]
y4 = 2 * (x - 1) + 2
ax.plot(x, y4, 'r-', linewidth=2, label='Through $(1,2)$ and $(3,6)$')
ax.plot([1, 3], [2, 6], 'ko', markersize=8, zorder=5)
ax.annotate('$(1, 2)$', xy=(1, 2), xytext=(0, 3.5), fontsize=11,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.annotate('$(3, 6)$', xy=(3, 6), xytext=(3.5, 4.5), fontsize=11,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('Two-Point Form', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_xlim(-2, 5)
ax.set_ylim(-3, 10)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(assets_dir, 'line_forms.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

# === 图2：斜率的几何含义 ===
fig, ax = plt.subplots(figsize=(8, 6))
slopes = [-2, -1, -0.5, 0, 0.5, 1, 2]
colors = plt.cm.coolwarm(np.linspace(0, 1, len(slopes)))

for k, c in zip(slopes, colors):
    y = k * x
    ax.plot(x, y, color=c, linewidth=2, label=f'$k = {k}$')

ax.set_title('Slope: Geometric Meaning', fontsize=14, fontweight='bold')
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.set_xlim(-3, 5)
ax.set_ylim(-6, 8)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.8)
ax.axvline(x=0, color='k', linewidth=0.8)
ax.legend(fontsize=9, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(assets_dir, 'slope_meaning.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

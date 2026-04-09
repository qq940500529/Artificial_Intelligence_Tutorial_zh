# 文件：code/plot_power_growth.py
# 用途：对比幂函数与根式函数的增长速度
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------- 输出路径 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'power_growth.png')

# ---------- 全局样式 ----------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(0, 4, 500)
# Avoid division warnings at x=0 for roots
x_pos = np.where(x > 0, x, np.nan)

fig, ax = plt.subplots(figsize=(8, 6))

# Baseline
ax.plot(x, x, color='gray', linewidth=1.5, linestyle='--', label='$y = x$', zorder=2)

# Power functions
ax.plot(x, x ** 2, color='#2980B9', linewidth=2.5, label='$y = x^2$', zorder=3)
ax.plot(x, x ** 3, color='#E74C3C', linewidth=2.5, label='$y = x^3$', zorder=3)

# Root functions
ax.plot(x_pos, np.sqrt(x_pos), color='#27AE60', linewidth=2.5,
        label='$y = \\sqrt{x}$', zorder=3)
ax.plot(x_pos, np.cbrt(x_pos), color='#8E44AD', linewidth=2.5,
        label='$y = \\sqrt[3]{x}$', zorder=3)

# Mark intersection at (1, 1)
ax.plot(1, 1, 'ko', markersize=9, zorder=5)
ax.annotate('All pass through $(1, 1)$',
            xy=(1, 1), xytext=(1.8, 1.8),
            fontsize=11, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFACD', edgecolor='gray'))

# Mark (0, 0)
ax.plot(0, 0, 'ko', markersize=7, zorder=5)

# Annotations for growth direction
ax.annotate('Higher powers\ngrow faster',
            xy=(2.5, 2.5 ** 2), xytext=(3.0, 7.2),
            fontsize=10, color='#2980B9', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#2980B9', lw=1.3))

ax.annotate('Higher roots\ngrow slower',
            xy=(3.5, np.sqrt(3.5)), xytext=(2.8, 0.5),
            fontsize=10, color='#27AE60', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=1.3))

ax.set_xlim(0, 4)
ax.set_ylim(0, 8)
ax.set_xlabel('$x$', fontsize=13)
ax.set_ylabel('$y$', fontsize=13)
ax.set_title('Power Functions vs. Root Functions', fontsize=14, fontweight='bold', pad=12)
ax.legend(fontsize=11, loc='upper left', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}')

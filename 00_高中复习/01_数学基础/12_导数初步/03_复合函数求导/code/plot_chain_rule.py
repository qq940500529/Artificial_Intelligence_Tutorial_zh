# 文件：code/plot_chain_rule.py
# 用途：可视化链式法则——分别展示内函数、外函数、复合函数及其导数
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------- 输出路径 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'chain_rule.png')

# ---------- 全局样式 ----------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(-2, 2, 500)
u = x ** 2                    # inner function
y_outer = np.sin(np.linspace(0, 4, 500))  # outer over u-range
y_comp = np.sin(x ** 2)       # composite
dy_dx = np.cos(x ** 2) * 2 * x  # derivative

# Tangent line at x0 = 1
x0 = 1.0
y0 = np.sin(x0 ** 2)
slope = np.cos(x0 ** 2) * 2 * x0
x_tan = np.linspace(x0 - 0.6, x0 + 0.6, 100)
y_tan = y0 + slope * (x_tan - x0)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# ========== 左图：内函数 u = x² ==========
ax = axes[0]
ax.plot(x, u, color='#2980B9', linewidth=2.5, label='$u = x^2$')
ax.axvline(x0, color='gray', linewidth=0.8, linestyle=':', alpha=0.5)
ax.plot(x0, x0 ** 2, 'o', color='#2980B9', markersize=8, zorder=5)
ax.annotate(f'$x={x0:.0f},\\; u={x0**2:.0f}$',
            xy=(x0, x0 ** 2), xytext=(x0 + 0.4, x0 ** 2 + 0.6),
            fontsize=10, color='#2980B9',
            arrowprops=dict(arrowstyle='->', color='#2980B9', lw=1.2))
ax.set_title('Inner function: $u = x^2$', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$u$', fontsize=12)
ax.legend(fontsize=11, loc='upper center')
ax.set_ylim(-0.5, 4.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# ========== 中图：外函数 y = sin(u) ==========
ax = axes[1]
u_range = np.linspace(0, 4, 500)
ax.plot(u_range, np.sin(u_range), color='#E74C3C', linewidth=2.5, label='$y = \\sin(u)$')
u0 = x0 ** 2
ax.plot(u0, np.sin(u0), 'o', color='#E74C3C', markersize=8, zorder=5)
ax.annotate(f'$u={u0:.0f},\\; y={np.sin(u0):.2f}$',
            xy=(u0, np.sin(u0)), xytext=(u0 + 0.8, np.sin(u0) + 0.3),
            fontsize=10, color='#E74C3C',
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))
ax.set_title('Outer function: $y = \\sin(u)$', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('$u$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.set_ylim(-1.3, 1.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# ========== 右图：复合函数 y = sin(x²) 及其导数 ==========
ax = axes[2]
ax.plot(x, y_comp, color='#8E44AD', linewidth=2.5, label='$y = \\sin(x^2)$')
ax.plot(x, dy_dx, color='#27AE60', linewidth=2, linestyle='--',
        label="$y' = \\cos(x^2) \\cdot 2x$")
ax.plot(x_tan, y_tan, color='#F39C12', linewidth=2, linestyle='-',
        label=f'Tangent at $x={x0:.0f}$')
ax.plot(x0, y0, 'o', color='#8E44AD', markersize=8, zorder=5)
ax.annotate(f'slope = {slope:.2f}',
            xy=(x0, y0), xytext=(x0 + 0.5, y0 - 0.6),
            fontsize=10, color='#F39C12', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#F39C12', lw=1.2))
ax.set_title('Composite: $y = \\sin(x^2)$', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.legend(fontsize=9.5, loc='lower left')
ax.set_ylim(-2.5, 2.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}')

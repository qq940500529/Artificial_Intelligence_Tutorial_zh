# plot_tangent.py
# 用途：绘制曲线 y = x^2 在某一点的切线，以及逐渐逼近的割线
# 依赖：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ---- 全局设置 ----
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ---- 参数 ----
a = 1.0  # 切点的 x 坐标
f = lambda x: x ** 2
f_prime = lambda x: 2 * x

x = np.linspace(-0.5, 3.0, 300)
y = f(x)

fig, ax = plt.subplots(figsize=(8, 6))

# 绘制曲线
ax.plot(x, y, 'b-', linewidth=2, label=r'$y = x^2$')

# 绘制逐渐逼近的割线
delta_values = [1.5, 1.0, 0.5]
colors = ['#cccccc', '#999999', '#666666']
for delta, color in zip(delta_values, colors):
    x2 = a + delta
    slope = (f(x2) - f(a)) / (x2 - a)
    y_secant = f(a) + slope * (x - a)
    ax.plot(x, y_secant, '--', color=color, linewidth=1,
            label=rf'Secant ($\Delta x = {delta}$)')
    ax.plot(x2, f(x2), 'o', color=color, markersize=5)

# 绘制切线
slope_tangent = f_prime(a)
y_tangent = f(a) + slope_tangent * (x - a)
ax.plot(x, y_tangent, 'r-', linewidth=2,
        label=rf'Tangent at $x={a:.0f}$ (slope = {slope_tangent:.0f})')

# 标注切点
ax.plot(a, f(a), 'ro', markersize=8, zorder=5)
ax.annotate(f'({a:.0f}, {f(a):.0f})', xy=(a, f(a)),
            xytext=(a + 0.3, f(a) - 0.8),
            fontsize=12, color='red',
            arrowprops=dict(arrowstyle='->', color='red'))

# 美化
ax.set_xlim(-0.5, 3.0)
ax.set_ylim(-1.0, 6.0)
ax.set_xlabel(r'$x$', fontsize=14)
ax.set_ylabel(r'$y$', fontsize=14)
ax.set_title('Secant Lines Approaching the Tangent Line', fontsize=14)
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# ---- 保存图片 ----
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'tangent_line.png')
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved to {output_path}")

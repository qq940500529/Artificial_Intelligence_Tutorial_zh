"""
文件：code/plot_conics.py
用途：绘制圆与二次曲线（椭圆、抛物线、双曲线）的图像
依赖：matplotlib>=3.5, numpy>=1.21
运行：python code/plot_conics.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

# === 图1：四种圆锥曲线概览 ===
fig, axes = plt.subplots(2, 2, figsize=(10, 9))

theta = np.linspace(0, 2 * np.pi, 500)

# 圆：x^2 + y^2 = 4
ax = axes[0, 0]
cx, cy = 2 * np.cos(theta), 2 * np.sin(theta)
ax.plot(cx, cy, 'b-', linewidth=2)
ax.plot(0, 0, 'ro', markersize=6, zorder=5)
ax.annotate('center $(0,0)$', xy=(0, 0), xytext=(0.5, -1.5), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='red'))
ax.plot([0, 2], [0, 0], 'r--', linewidth=1.5)
ax.text(1, 0.2, '$r=2$', fontsize=11, color='red')
ax.set_title('Circle: $x^2 + y^2 = 4$', fontsize=13, fontweight='bold')
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 椭圆：x^2/9 + y^2/4 = 1
ax = axes[0, 1]
ex, ey = 3 * np.cos(theta), 2 * np.sin(theta)
ax.plot(ex, ey, 'g-', linewidth=2)
c_val = np.sqrt(9 - 4)
ax.plot([-c_val, c_val], [0, 0], 'r^', markersize=8, zorder=5)
ax.text(c_val + 0.2, 0.3, '$F_2$', fontsize=11, color='red')
ax.text(-c_val - 0.7, 0.3, '$F_1$', fontsize=11, color='red')
ax.plot([3, 0, -3, 0], [0, 2, 0, -2], 'g.', markersize=8)
ax.set_title(r'Ellipse: $\frac{x^2}{9}+\frac{y^2}{4}=1$',
             fontsize=13, fontweight='bold')
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 抛物线：y^2 = 4x
ax = axes[1, 0]
t_para = np.linspace(-3, 3, 500)
px = t_para ** 2 / 4
py = t_para
ax.plot(px, py, 'm-', linewidth=2)
ax.plot(1, 0, 'r^', markersize=8, zorder=5)
ax.text(1.2, 0.3, 'focus $(1,0)$', fontsize=10, color='red')
ax.axvline(x=-1, color='orange', linestyle='--', linewidth=1.5, label='directrix $x=-1$')
ax.set_title('Parabola: $y^2 = 4x$', fontsize=13, fontweight='bold')
ax.set_xlim(-3, 5)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 双曲线：x^2/4 - y^2/1 = 1
ax = axes[1, 1]
t_hyp = np.linspace(-2.5, 2.5, 500)
# 右支
hx_r = 2 * np.cosh(t_hyp)
hy_r = 1 * np.sinh(t_hyp)
# 左支
hx_l = -2 * np.cosh(t_hyp)
hy_l = 1 * np.sinh(t_hyp)
ax.plot(hx_r, hy_r, 'c-', linewidth=2)
ax.plot(hx_l, hy_l, 'c-', linewidth=2)
# 渐近线
x_asym = np.linspace(-6, 6, 100)
ax.plot(x_asym, x_asym / 2, 'r--', linewidth=1, alpha=0.7, label='asymptotes $y=\\pm x/2$')
ax.plot(x_asym, -x_asym / 2, 'r--', linewidth=1, alpha=0.7)
ax.set_title(r'Hyperbola: $\frac{x^2}{4}-y^2=1$',
             fontsize=13, fontweight='bold')
ax.set_xlim(-6, 6)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(assets_dir, 'conic_sections.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

# === 图2：圆的标准方程与一般方程对比 ===
fig, ax = plt.subplots(figsize=(7, 7))
# 圆1：标准式 (x-1)^2 + (y-2)^2 = 4
c1x, c1y = 1 + 2 * np.cos(theta), 2 + 2 * np.sin(theta)
ax.plot(c1x, c1y, 'b-', linewidth=2, label='$(x-1)^2+(y-2)^2=4$')
ax.plot(1, 2, 'bo', markersize=6, zorder=5)

# 圆2：一般式 x^2+y^2-4x+2y-4=0 => (x-2)^2+(y+1)^2=9
c2x, c2y = 2 + 3 * np.cos(theta), -1 + 3 * np.sin(theta)
ax.plot(c2x, c2y, 'r-', linewidth=2, label='$x^2+y^2-4x+2y-4=0$')
ax.plot(2, -1, 'ro', markersize=6, zorder=5)

ax.set_title('Standard Form vs General Form', fontsize=14, fontweight='bold')
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.set_xlim(-3, 7)
ax.set_ylim(-5, 6)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend(fontsize=10, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
output_path = os.path.join(assets_dir, 'circle_forms.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

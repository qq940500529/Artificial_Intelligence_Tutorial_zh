# plot_monotonicity.py
# 绘制递增函数与递减函数的对比图
# 依赖：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ── 字体与样式设置 ──
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ── 输出路径（基于脚本自身位置） ──
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'monotonicity_examples.png')

# ── 数据 ──
x_linear = np.linspace(-3, 3, 300)
y_linear = 2 * x_linear + 1

x_quad = np.linspace(-3, 3, 300)
y_quad = -x_quad ** 2

# ── 绘图 ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')

# --- 左图：递增函数 f(x) = 2x + 1 ---
ax1 = axes[0]
ax1.plot(x_linear, y_linear, color='#2196F3', linewidth=2.5, label=r'$f(x) = 2x + 1$')

# 标注两个点并用箭头说明递增
x1, x2 = -1.5, 1.5
y1, y2 = 2 * x1 + 1, 2 * x2 + 1
ax1.scatter([x1, x2], [y1, y2], color='#E53935', s=80, zorder=5)
ax1.annotate(f'$x_1={x1}$\n$f(x_1)={y1:.0f}$', xy=(x1, y1),
             xytext=(x1 - 1.2, y1 + 1.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='center')
ax1.annotate(f'$x_2={x2}$\n$f(x_2)={y2:.0f}$', xy=(x2, y2),
             xytext=(x2 + 1.2, y2 - 1.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='center')

# 添加递增标注
ax1.annotate('', xy=(2.2, 2 * 2.2 + 1), xytext=(-2.2, 2 * (-2.2) + 1),
             arrowprops=dict(arrowstyle='->', color='green', lw=2, ls='--'))
ax1.text(0, -4, 'Increasing: $x_1 < x_2 \\Rightarrow f(x_1) < f(x_2)$',
         fontsize=11, ha='center', color='green', style='italic')

ax1.set_title(r'Increasing Function: $f(x) = 2x + 1$', fontsize=13, fontweight='bold')
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$f(x)$', fontsize=12)
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.axvline(x=0, color='black', linewidth=0.5)
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11, loc='upper left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# --- 右图：递减函数 f(x) = -x^2（在 [0, +∞) 上递减） ---
ax2 = axes[1]
# 画完整曲线（灰色）
ax2.plot(x_quad, y_quad, color='#BDBDBD', linewidth=1.5, linestyle='--', alpha=0.6)
# 高亮 [0, +∞) 部分
x_right = x_quad[x_quad >= 0]
y_right = -x_right ** 2
ax2.plot(x_right, y_right, color='#FF9800', linewidth=2.5, label=r'$f(x) = -x^2$, $x \in [0, +\infty)$')

# 标注两个点
p1, p2 = 0.8, 2.2
q1, q2 = -p1 ** 2, -p2 ** 2
ax2.scatter([p1, p2], [q1, q2], color='#E53935', s=80, zorder=5)
ax2.annotate(f'$x_1={p1}$\n$f(x_1)={q1:.2f}$', xy=(p1, q1),
             xytext=(p1 + 1.0, q1 + 1.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='center')
ax2.annotate(f'$x_2={p2}$\n$f(x_2)={q2:.2f}$', xy=(p2, q2),
             xytext=(p2 + 0.5, q2 - 1.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='center')

# 添加递减标注
ax2.text(1.5, -7.5, 'Decreasing: $x_1 < x_2 \\Rightarrow f(x_1) > f(x_2)$',
         fontsize=11, ha='center', color='#E65100', style='italic')

ax2.set_title(r'Decreasing on $[0, +\infty)$: $f(x) = -x^2$', fontsize=13, fontweight='bold')
ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$f(x)$', fontsize=12)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.axvline(x=0, color='black', linewidth=0.5)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10, loc='lower left')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到：{output_path}")

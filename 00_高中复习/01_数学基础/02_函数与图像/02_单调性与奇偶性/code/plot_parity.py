# plot_parity.py
# 绘制奇函数（x^3）和偶函数（x^2）的对称性示意图
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
output_path = os.path.join(assets_dir, 'parity_examples.png')

# ── 数据 ──
x = np.linspace(-2, 2, 300)
y_odd = x ** 3    # 奇函数
y_even = x ** 2   # 偶函数

# ── 绘图 ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')

# --- 左图：奇函数 f(x) = x^3（关于原点对称） ---
ax1 = axes[0]
ax1.plot(x, y_odd, color='#9C27B0', linewidth=2.5, label=r'$f(x) = x^3$')

# 标注对称点对
pts = [1.3, -1.3]
for p in pts:
    ax1.scatter(p, p ** 3, color='#E53935', s=80, zorder=5)

# 画虚线连接对称点
ax1.plot([pts[0], pts[1]], [pts[0] ** 3, pts[1] ** 3],
         linestyle='--', color='#E53935', linewidth=1.5, alpha=0.7)

# 标注原点
ax1.scatter(0, 0, color='#FF9800', s=100, zorder=5, marker='D')
ax1.annotate('Origin (0, 0)', xy=(0, 0), xytext=(0.5, 3),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='#FF9800', lw=1.5),
             color='#FF9800', fontweight='bold')

# 标注对称点
ax1.annotate(f'$(a, a^3)$', xy=(pts[0], pts[0] ** 3),
             xytext=(pts[0] + 0.3, pts[0] ** 3 + 2), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935')
ax1.annotate(f'$(-a, -a^3)$', xy=(pts[1], pts[1] ** 3),
             xytext=(pts[1] - 0.3, pts[1] ** 3 - 2), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='right')

ax1.text(0, -7, 'Odd: $f(-x) = -f(x)$\nSymmetric about origin',
         fontsize=11, ha='center', color='#7B1FA2',
         style='italic', bbox=dict(boxstyle='round,pad=0.4',
                                    facecolor='#F3E5F5', alpha=0.8))

ax1.set_title(r'Odd Function: $f(x) = x^3$', fontsize=13, fontweight='bold')
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$f(x)$', fontsize=12)
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.axvline(x=0, color='black', linewidth=0.5)
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11, loc='upper left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_ylim(-9, 9)

# --- 右图：偶函数 f(x) = x^2（关于 y 轴对称） ---
ax2 = axes[1]
ax2.plot(x, y_even, color='#0288D1', linewidth=2.5, label=r'$f(x) = x^2$')

# 标注对称点对
for sign in [1, -1]:
    px = sign * 1.5
    py = px ** 2
    ax2.scatter(px, py, color='#E53935', s=80, zorder=5)

# 画水平虚线连接对称点
px_val = 1.5
py_val = px_val ** 2
ax2.plot([-px_val, px_val], [py_val, py_val],
         linestyle='--', color='#E53935', linewidth=1.5, alpha=0.7)

# 画 y 轴对称线（加粗）
ax2.axvline(x=0, color='#FF9800', linewidth=2, linestyle='-.',
            alpha=0.7, label='$y$-axis (symmetry axis)')

# 标注对称点
ax2.annotate(f'$(a, a^2)$', xy=(px_val, py_val),
             xytext=(px_val + 0.3, py_val + 0.8), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935')
ax2.annotate(f'$(-a, a^2)$', xy=(-px_val, py_val),
             xytext=(-px_val - 0.3, py_val + 0.8), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.5),
             color='#E53935', ha='right')

# 标注顶点
ax2.scatter(0, 0, color='#FF9800', s=100, zorder=5, marker='D')

ax2.text(0, -0.8, 'Even: $f(-x) = f(x)$\nSymmetric about $y$-axis',
         fontsize=11, ha='center', color='#01579B',
         style='italic', bbox=dict(boxstyle='round,pad=0.4',
                                    facecolor='#E1F5FE', alpha=0.8))

ax2.set_title(r'Even Function: $f(x) = x^2$', fontsize=13, fontweight='bold')
ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$f(x)$', fontsize=12)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10, loc='upper center')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylim(-1.5, 5)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到：{output_path}")

# 文件：code/plot_domain_range.py
# 用途：绘制三个常见函数（y=1/x, y=sqrt(x), y=x^2）的图像，
#       直观展示定义域和值域的概念。
# 依赖：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

# ── 字体与样式设置 ──
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ── 输出路径（基于脚本自身位置） ──
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'domain_range_examples.png')

# ── 创建画布：三个子图 ──
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='white')

# ────────────────────────────────
# 子图 1：y = 1/x
# 定义域：x != 0 ；值域：y != 0
# ────────────────────────────────
ax1 = axes[0]
x_neg = np.linspace(-5, -0.15, 300)
x_pos = np.linspace(0.15, 5, 300)
ax1.plot(x_neg, 1 / x_neg, color='#2196F3', linewidth=2, label=r'$y = 1/x$')
ax1.plot(x_pos, 1 / x_pos, color='#2196F3', linewidth=2)
# 标注 x=0 处不可取
ax1.axvline(x=0, color='red', linestyle='--', alpha=0.5, label='$x = 0$ (excluded)')
ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax1.set_xlim(-5, 5)
ax1.set_ylim(-6, 6)
ax1.set_xlabel(r'$x$', fontsize=12)
ax1.set_ylabel(r'$y$', fontsize=12)
ax1.set_title(r'$y = 1/x$' + '\nDomain: $x \\neq 0$, Range: $y \\neq 0$', fontsize=11)
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ────────────────────────────────
# 子图 2：y = sqrt(x)
# 定义域：x >= 0 ；值域：y >= 0
# ────────────────────────────────
ax2 = axes[1]
x_sqrt = np.linspace(0, 10, 400)
ax2.plot(x_sqrt, np.sqrt(x_sqrt), color='#4CAF50', linewidth=2, label=r'$y = \sqrt{x}$')
# 标注端点
ax2.plot(0, 0, 'o', color='#4CAF50', markersize=8, zorder=5)
ax2.annotate('$(0, 0)$', xy=(0, 0), xytext=(1.2, -0.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='gray'))
# 标注定义域从 0 开始
ax2.axvspan(-2, 0, color='red', alpha=0.08, label='Undefined ($x < 0$)')
ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax2.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
ax2.set_xlim(-2, 10)
ax2.set_ylim(-1, 4)
ax2.set_xlabel(r'$x$', fontsize=12)
ax2.set_ylabel(r'$y$', fontsize=12)
ax2.set_title(r'$y = \sqrt{x}$' + '\nDomain: $x \\geq 0$, Range: $y \\geq 0$', fontsize=11)
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ────────────────────────────────
# 子图 3：y = x^2
# 定义域：全体实数 ；值域：y >= 0
# ────────────────────────────────
ax3 = axes[2]
x_sq = np.linspace(-4, 4, 400)
ax3.plot(x_sq, x_sq ** 2, color='#FF9800', linewidth=2, label=r'$y = x^2$')
# 标注顶点
ax3.plot(0, 0, 'o', color='#FF9800', markersize=8, zorder=5)
ax3.annotate('Vertex $(0, 0)$\nMinimum $y = 0$', xy=(0, 0), xytext=(1.5, 8),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
# 标注值域
ax3.axhspan(-2, 0, color='red', alpha=0.08, label='No output ($y < 0$)')
ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax3.set_xlim(-4, 4)
ax3.set_ylim(-2, 16)
ax3.set_xlabel(r'$x$', fontsize=12)
ax3.set_ylabel(r'$y$', fontsize=12)
ax3.set_title(r'$y = x^2$' + '\nDomain: all reals, Range: $y \\geq 0$', fontsize=11)
ax3.legend(loc='upper center', fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Plot saved to: {output_path}")

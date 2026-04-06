# 文件：code/activation_functions.py
# 用途：绘制 Sigmoid 和 ReLU 两个常见激活函数的图像，
#       展示定义域与值域概念在人工智能中的应用。
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
output_path = os.path.join(output_dir, 'activation_functions.png')

# ── 创建画布：两个子图 ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')

# ────────────────────────────────
# 子图 1：Sigmoid 函数
# 定义域：全体实数 ；值域：(0, 1)
# ────────────────────────────────
ax1 = axes[0]
x_sigmoid = np.linspace(-8, 8, 500)
y_sigmoid = 1 / (1 + np.exp(-x_sigmoid))

ax1.plot(x_sigmoid, y_sigmoid, color='#E91E63', linewidth=2.5, label=r'$\sigma(x) = \frac{1}{1 + e^{-x}}$')
# 标注值域边界
ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='$y = 1$ (asymptote)')
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5, label='$y = 0$ (asymptote)')
ax1.axhline(y=0.5, color='#E91E63', linestyle=':', alpha=0.4)
# 标注关键点
ax1.plot(0, 0.5, 'o', color='#E91E63', markersize=8, zorder=5)
ax1.annotate('$(0, 0.5)$', xy=(0, 0.5), xytext=(1.5, 0.35), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='gray'))
# 用半透明色块标注值域
ax1.axhspan(0, 1, color='#E91E63', alpha=0.05)
ax1.fill_between(x_sigmoid, 0, y_sigmoid, alpha=0.1, color='#E91E63')
ax1.set_xlim(-8, 8)
ax1.set_ylim(-0.15, 1.15)
ax1.set_xlabel(r'$x$', fontsize=13)
ax1.set_ylabel(r'$\sigma(x)$', fontsize=13)
ax1.set_title('Sigmoid Function\nDomain: $(-\\infty, +\\infty)$, Range: $(0, 1)$', fontsize=12)
ax1.legend(loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ────────────────────────────────
# 子图 2：ReLU 函数
# 定义域：全体实数 ；值域：[0, +∞)
# ────────────────────────────────
ax2 = axes[1]
x_relu = np.linspace(-6, 6, 500)
y_relu = np.maximum(0, x_relu)

ax2.plot(x_relu, y_relu, color='#2196F3', linewidth=2.5, label=r'$\mathrm{ReLU}(x) = \max(0, x)$')
# 标注拐点
ax2.plot(0, 0, 'o', color='#2196F3', markersize=8, zorder=5)
ax2.annotate('$(0, 0)$ turning point', xy=(0, 0), xytext=(1.5, 2.5), fontsize=11,
             arrowprops=dict(arrowstyle='->', color='gray'))
# 标注 x<0 部分为零
ax2.fill_between(x_relu[x_relu <= 0], 0, 0, alpha=0.1, color='red')
ax2.axhspan(-1, 0, color='red', alpha=0.05, label='No output ($y < 0$)')
ax2.set_xlim(-6, 6)
ax2.set_ylim(-1, 6)
ax2.set_xlabel(r'$x$', fontsize=13)
ax2.set_ylabel(r'$\mathrm{ReLU}(x)$', fontsize=13)
ax2.set_title('ReLU Function\nDomain: $(-\\infty, +\\infty)$, Range: $[0, +\\infty)$', fontsize=12)
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Plot saved to: {output_path}")

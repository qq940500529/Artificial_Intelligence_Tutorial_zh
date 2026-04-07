# 文件：plot_translation.py
# 用途：绘制函数平移变换示例图
# 环境要求：Python 3.10+, numpy, matplotlib

import os
import numpy as np
import matplotlib.pyplot as plt

# ── 配置 ──
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ── 输出路径 ──
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'translation_examples.png')

# ── 绘图 ──
x = np.linspace(-6, 8, 500)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图：上下平移
ax1 = axes[0]
ax1.plot(x, x**2, 'k--', linewidth=1.5, label='$y = x^2$', alpha=0.6)
ax1.plot(x, x**2 + 3, 'r-', linewidth=2, label='$y = x^2 + 3$ (up 3)')
ax1.plot(x, x**2 - 2, 'b-', linewidth=2, label='$y = x^2 - 2$ (down 2)')

# 标注顶点
ax1.plot(0, 0, 'ko', markersize=6)
ax1.plot(0, 3, 'ro', markersize=6)
ax1.plot(0, -2, 'bo', markersize=6)

# 绘制平移箭头
ax1.annotate('', xy=(0, 3), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5, ls='--'))
ax1.annotate('', xy=(0, -2), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='blue', lw=1.5, ls='--'))

ax1.set_xlim(-4, 4)
ax1.set_ylim(-4, 12)
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_title('Vertical Translation', fontsize=14)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# 右图：左右平移
ax2 = axes[1]
ax2.plot(x, x**2, 'k--', linewidth=1.5, label='$y = x^2$', alpha=0.6)
ax2.plot(x, (x - 3)**2, 'r-', linewidth=2, label='$y = (x-3)^2$ (right 3)')
ax2.plot(x, (x + 2)**2, 'b-', linewidth=2, label='$y = (x+2)^2$ (left 2)')

# 标注顶点
ax2.plot(0, 0, 'ko', markersize=6)
ax2.plot(3, 0, 'ro', markersize=6)
ax2.plot(-2, 0, 'bo', markersize=6)

# 绘制平移箭头
ax2.annotate('', xy=(3, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5, ls='--'))
ax2.annotate('', xy=(-2, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='blue', lw=1.5, ls='--'))

ax2.set_xlim(-5, 7)
ax2.set_ylim(-2, 12)
ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_title('Horizontal Translation', fontsize=14)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Plot saved to: {output_path}")

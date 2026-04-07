# 文件：plot_scaling.py
# 用途：绘制函数伸缩变换示例图
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
output_path = os.path.join(assets_dir, 'scaling_examples.png')

# ── 绘图 ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图：垂直伸缩（抛物线）
ax1 = axes[0]
x = np.linspace(-3, 3, 500)

ax1.plot(x, x**2, 'k--', linewidth=1.5, label='$y = x^2$', alpha=0.6)
ax1.plot(x, 2 * x**2, 'r-', linewidth=2, label='$y = 2x^2$ (stretch)')
ax1.plot(x, 0.5 * x**2, 'b-', linewidth=2, label='$y = 0.5x^2$ (compress)')

# 标注关键点 x=1
ax1.plot(1, 1, 'ko', markersize=5)
ax1.plot(1, 2, 'ro', markersize=5)
ax1.plot(1, 0.5, 'bo', markersize=5)
ax1.annotate('$(1, 1)$', xy=(1, 1), xytext=(1.3, 1.3), fontsize=9)
ax1.annotate('$(1, 2)$', xy=(1, 2), xytext=(1.3, 2.3), fontsize=9, color='red')
ax1.annotate('$(1, 0.5)$', xy=(1, 0.5), xytext=(1.3, 0.2), fontsize=9, color='blue')

ax1.set_xlim(-3, 3)
ax1.set_ylim(-1, 8)
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_title('Vertical Scaling: $y = a \\cdot x^2$', fontsize=14)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# 右图：水平伸缩（正弦函数）
ax2 = axes[1]
x = np.linspace(-2 * np.pi, 4 * np.pi, 1000)

ax2.plot(x, np.sin(x), 'k--', linewidth=1.5, label='$y = \\sin(x)$', alpha=0.6)
ax2.plot(x, np.sin(2 * x), 'r-', linewidth=2, label='$y = \\sin(2x)$ (compress)')
ax2.plot(x, np.sin(0.5 * x), 'b-', linewidth=2, label='$y = \\sin(0.5x)$ (stretch)')

# 标注周期
ax2.annotate('', xy=(2 * np.pi, -0.15), xytext=(0, -0.15),
             arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
ax2.text(np.pi, -0.35, '$T = 2\\pi$', ha='center', fontsize=9, color='gray')

ax2.annotate('', xy=(np.pi, -0.5), xytext=(0, -0.5),
             arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax2.text(np.pi / 2, -0.7, '$T = \\pi$', ha='center', fontsize=9, color='red')

ax2.set_xlim(-2, 4 * np.pi)
ax2.set_ylim(-1.3, 1.3)
ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_title('Horizontal Scaling: $y = \\sin(bx)$', fontsize=14)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# 设置 x 轴刻度为 pi 的倍数
ax2.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
ax2.set_xticklabels(['$0$', '$\\pi$', '$2\\pi$', '$3\\pi$', '$4\\pi$'])

plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Plot saved to: {output_path}")

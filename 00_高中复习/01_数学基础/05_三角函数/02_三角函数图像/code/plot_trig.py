# 文件：code/plot_trig.py
# 绘制三角函数图像及参数变换效果
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

x = np.linspace(-2 * np.pi, 2 * np.pi, 500)

# 左上：sin, cos
ax = axes[0, 0]
ax.plot(x, np.sin(x), color='#2196f3', linewidth=2, label='$y = \\sin x$')
ax.plot(x, np.cos(x), color='#f44336', linewidth=2, label='$y = \\cos x$')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$'])
ax.set_title('$y = \\sin x$ and $y = \\cos x$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 右上：tan
ax = axes[0, 1]
for k in range(-2, 3):
    x_seg = np.linspace(-np.pi/2 + k*np.pi + 0.05, np.pi/2 + k*np.pi - 0.05, 200)
    ax.plot(x_seg, np.tan(x_seg), color='#4caf50', linewidth=2)
    ax.axvline(x=np.pi/2 + k*np.pi, color='gray', linewidth=0.5, linestyle=':')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-5, 5)
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$'])
ax.set_title('$y = \\tan x$', fontsize=12)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 左下：振幅变换
ax = axes[1, 0]
ax.plot(x, np.sin(x), color='gray', linewidth=1, linestyle='--', label='$y = \\sin x$')
ax.plot(x, 2*np.sin(x), color='#2196f3', linewidth=2, label='$y = 2\\sin x$')
ax.plot(x, 0.5*np.sin(x), color='#ff9800', linewidth=2, label='$y = 0.5\\sin x$')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-2.5, 2.5)
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$'])
ax.set_title('Amplitude $A$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 右下：频率变换
ax = axes[1, 1]
ax.plot(x, np.sin(x), color='gray', linewidth=1, linestyle='--', label='$y = \\sin x$')
ax.plot(x, np.sin(2*x), color='#9c27b0', linewidth=2, label='$y = \\sin 2x$')
ax.plot(x, np.sin(0.5*x), color='#4caf50', linewidth=2, label='$y = \\sin 0.5x$')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$'])
ax.set_title('Angular Frequency $\\omega$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'assets', 'trig_functions.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"图片已保存到 {output_path}")

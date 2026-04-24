# plot_lp_balls.py
# Visualize the unit balls of L1, L2, L_inf norms in 2D
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

theta = np.linspace(0, 2 * np.pi, 400)

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect('equal')
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
ax.set_title(r'Unit balls of $L_1$, $L_2$, $L_\infty$ norms in $\mathbb{R}^2$',
             fontsize=13, fontweight='bold')

# L2 ball: x^2 + y^2 = 1
x_l2 = np.cos(theta)
y_l2 = np.sin(theta)
ax.plot(x_l2, y_l2, color='#27ae60', lw=2.5, label=r'$L_2$ (circle)')
ax.fill(x_l2, y_l2, color='#27ae60', alpha=0.10)

# L1 ball: |x| + |y| = 1   (rotated square = diamond)
diamond_x = [1, 0, -1, 0, 1]
diamond_y = [0, 1, 0, -1, 0]
ax.plot(diamond_x, diamond_y, color='#e67e22', lw=2.5, label=r'$L_1$ (diamond)')
ax.fill(diamond_x, diamond_y, color='#e67e22', alpha=0.10)

# L_inf ball: max(|x|, |y|) = 1   (axis-aligned square)
square_x = [1, 1, -1, -1, 1]
square_y = [1, -1, -1, 1, 1]
ax.plot(square_x, square_y, color='#2980b9', lw=2.5, label=r'$L_\infty$ (square)')
ax.fill(square_x, square_y, color='#2980b9', alpha=0.10)

# Annotate the corners of L1 (sparsity!)
for (px, py) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    ax.plot(px, py, 'o', color='#e67e22', markersize=9, zorder=5)
ax.annotate('Corners of $L_1$\nlie on axes\n=> sparse solutions',
            xy=(1, 0), xytext=(0.55, -1.2),
            fontsize=9, color='#e67e22', ha='center',
            arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.2))

ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax.set_xlabel('$x_1$', fontsize=12)
ax.set_ylabel('$x_2$', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'lp_balls.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

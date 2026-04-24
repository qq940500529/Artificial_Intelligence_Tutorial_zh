# plot_composition_order.py
# Visualize that AB != BA: shear-then-rotate vs rotate-then-shear
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Unit square
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

theta = np.pi / 4  # 45 deg
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
H = np.array([[1.0, 1.0],
              [0.0, 1.0]])


def apply(M, pts):
    return pts @ M.T


def setup_ax(ax, title, xlim=(-1.6, 2.5), ylim=(-0.5, 2.5)):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.tick_params(labelsize=8)


def draw(ax, pts, color, alpha=0.5, lw=2, label=None):
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, label=label)
    ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=alpha * 0.5)


fig, axes = plt.subplots(2, 3, figsize=(13, 8.5))

# Top row: shear then rotate (R H)
draw(axes[0, 0], square, '#2980b9'); setup_ax(axes[0, 0], 'Start')
sheared = apply(H, square)
draw(axes[0, 1], sheared, '#e67e22'); setup_ax(axes[0, 1], 'After shear H')
rh = apply(R, sheared)
draw(axes[0, 2], rh, '#27ae60'); setup_ax(axes[0, 2], 'Then rotate R\n=> R H @ x')

# Bottom row: rotate then shear (H R)
draw(axes[1, 0], square, '#2980b9'); setup_ax(axes[1, 0], 'Start')
rotated = apply(R, square)
draw(axes[1, 1], rotated, '#9b59b6'); setup_ax(axes[1, 1], 'After rotate R')
hr = apply(H, rotated)
draw(axes[1, 2], hr, '#c0392b'); setup_ax(axes[1, 2], 'Then shear H\n=> H R @ x')

# Big title
fig.suptitle('Order matters: R H  vs  H R   (the two final shapes differ)',
             fontsize=13, fontweight='bold', y=1.0)

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'composition_order.png')
plt.savefig(output_path, dpi=140, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

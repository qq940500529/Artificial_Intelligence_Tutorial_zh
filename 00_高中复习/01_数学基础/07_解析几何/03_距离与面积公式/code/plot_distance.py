# plot_distance.py
# Visualize point-to-point and point-to-line distance formulas
# Requirements: Python 3.10+, matplotlib >= 3.7, numpy >= 1.24

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'distance_formulas.png')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

# ========== Left: Point-to-Point Distance ==========
ax = ax1

P1 = np.array([1, 2])
P2 = np.array([4, 6])

# Grid and axes
ax.set_xlim(-0.5, 6)
ax.set_ylim(-0.5, 8)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Right triangle: horizontal and vertical legs
# Horizontal leg P1 -> (P2[0], P1[1])
corner = np.array([P2[0], P1[1]])
ax.plot([P1[0], corner[0]], [P1[1], corner[1]], color='#55A868',
        linewidth=2, linestyle='--', zorder=2)
# Vertical leg (P2[0], P1[1]) -> P2
ax.plot([corner[0], P2[0]], [corner[1], P2[1]], color='#C44E52',
        linewidth=2, linestyle='--', zorder=2)

# Right angle marker
marker_size = 0.25
ax.plot([corner[0] - marker_size, corner[0] - marker_size, corner[0]],
        [corner[1], corner[1] + marker_size, corner[1] + marker_size],
        color='#666666', linewidth=1.5, zorder=2)

# Hypotenuse (distance line)
ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color='#4C72B0',
        linewidth=2.5, zorder=3)

# Points
ax.plot(*P1, 'o', color='#4C72B0', markersize=10, zorder=5)
ax.plot(*P2, 'o', color='#4C72B0', markersize=10, zorder=5)

# Labels for points
ax.annotate(r'$P_1(1, 2)$', xy=P1, xytext=(P1[0] - 0.3, P1[1] - 0.7),
            fontsize=13, fontweight='bold', color='#4C72B0', zorder=5)
ax.annotate(r'$P_2(4, 6)$', xy=P2, xytext=(P2[0] + 0.2, P2[1] + 0.3),
            fontsize=13, fontweight='bold', color='#4C72B0', zorder=5)

# Delta labels
dx = P2[0] - P1[0]
dy = P2[1] - P1[1]
ax.text((P1[0] + corner[0]) / 2, P1[1] - 0.45,
        r'$\Delta x = %d$' % dx, fontsize=12, ha='center',
        color='#55A868', fontweight='bold')
ax.text(corner[0] + 0.35, (corner[1] + P2[1]) / 2,
        r'$\Delta y = %d$' % dy, fontsize=12, ha='left',
        color='#C44E52', fontweight='bold')

# Distance label on hypotenuse
mid = (P1 + P2) / 2
d_val = np.sqrt(dx**2 + dy**2)
ax.text(mid[0] - 0.9, mid[1] + 0.3,
        r'$d = \sqrt{\Delta x^2 + \Delta y^2} = %.0f$' % d_val,
        fontsize=12, fontweight='bold', color='#4C72B0',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE',
                  edgecolor='#4C72B0', alpha=0.9))

ax.set_xlabel('$x$', fontsize=13)
ax.set_ylabel('$y$', fontsize=13)
ax.set_title('Point-to-Point Distance', fontsize=14, fontweight='bold', pad=12)


# ========== Right: Point-to-Line Distance ==========
ax = ax2

# Line: 3x + 4y - 12 = 0 => y = (12 - 3x)/4
A_coeff, B_coeff, C_coeff = 3, 4, -12
x_line = np.linspace(-0.5, 6.5, 200)
y_line = (- A_coeff * x_line - C_coeff) / B_coeff  # y = (12 - 3x)/4

# Point P0
P0 = np.array([5, 5])

# Foot of perpendicular from P0 to the line
# foot = P0 - ((A*x0 + B*y0 + C) / (A^2 + B^2)) * (A, B)
t = (A_coeff * P0[0] + B_coeff * P0[1] + C_coeff) / (A_coeff**2 + B_coeff**2)
foot = P0 - t * np.array([A_coeff, B_coeff])

ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Plot line
mask = (y_line >= -1) & (y_line <= 7)
ax.plot(x_line[mask], y_line[mask], color='#8172B2', linewidth=2.5, zorder=2,
        label=r'$3x + 4y - 12 = 0$')

# Perpendicular segment
ax.plot([P0[0], foot[0]], [P0[1], foot[1]], color='#C44E52',
        linewidth=2.5, linestyle='-', zorder=3)

# Right angle marker at foot
# Compute perpendicular directions
along_line = np.array([-B_coeff, A_coeff])
along_line = along_line / np.linalg.norm(along_line)
perp_dir = np.array([A_coeff, B_coeff])
perp_dir = perp_dir / np.linalg.norm(perp_dir)
ms = 0.25
corner1 = foot + ms * along_line
corner2 = corner1 + ms * perp_dir
corner3 = foot + ms * perp_dir
ax.plot([corner1[0], corner2[0], corner3[0]],
        [corner1[1], corner2[1], corner3[1]],
        color='#666666', linewidth=1.5, zorder=3)

# Points
ax.plot(*P0, 'o', color='#C44E52', markersize=10, zorder=5)
ax.plot(*foot, 's', color='#55A868', markersize=8, zorder=5)

# Point labels
ax.annotate(r'$P_0(5, 5)$', xy=P0, xytext=(P0[0] + 0.2, P0[1] + 0.4),
            fontsize=13, fontweight='bold', color='#C44E52', zorder=5)
ax.annotate('Foot', xy=foot, xytext=(foot[0] - 1.2, foot[1] - 0.7),
            fontsize=11, color='#55A868', fontweight='bold', zorder=5)

# Distance label
d_val = abs(A_coeff * P0[0] + B_coeff * P0[1] + C_coeff) / np.sqrt(A_coeff**2 + B_coeff**2)
mid_perp = (P0 + foot) / 2
ax.text(mid_perp[0] + 0.3, mid_perp[1] + 0.1,
        r'$d = %.1f$' % d_val,
        fontsize=13, fontweight='bold', color='#C44E52',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDEDEC',
                  edgecolor='#C44E52', alpha=0.9))

# Formula annotation box
ax.text(3, -0.5,
        r'$d = \dfrac{|Ax_0 + By_0 + C|}{\sqrt{A^2 + B^2}}$',
        fontsize=14, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFDE7',
                  edgecolor='#F9A825', linewidth=1.5))

# Line label
ax.text(0.8, 2.6, r'$3x + 4y - 12 = 0$', fontsize=11, color='#8172B2',
        rotation=-37, fontweight='bold')

ax.set_xlabel('$x$', fontsize=13)
ax.set_ylabel('$y$', fontsize=13)
ax.set_title('Point-to-Line Distance', fontsize=14, fontweight='bold', pad=12)

plt.tight_layout(pad=2.0)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Chart saved to {output_path}")

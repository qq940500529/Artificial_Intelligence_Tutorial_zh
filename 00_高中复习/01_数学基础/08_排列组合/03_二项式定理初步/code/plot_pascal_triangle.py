# plot_pascal_triangle.py
# Visualize Pascal's Triangle with symmetry coloring and row sums
# Environment: Python 3.10+, matplotlib

import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

n_rows = 6  # rows n=0 to n=5

fig, ax = plt.subplots(figsize=(10, 7))

# Color scheme
color_left = '#3498db'    # blue for left half
color_right = '#e74c3c'   # red for right half
color_center = '#f39c12'  # orange for center (when n is even, the middle element)
color_bg_left = '#d6eaf8'
color_bg_right = '#fadbd8'
color_bg_center = '#fdebd0'

circle_radius = 0.38

for n in range(n_rows):
    row = [math.comb(n, k) for k in range(n + 1)]
    row_sum = sum(row)
    y = (n_rows - 1) - n  # top row at top

    for k, val in enumerate(row):
        # Center the row: x offset
        x = k - n / 2.0

        # Determine left/right/center
        if k < n / 2:
            fc = color_bg_left
            ec = color_left
            tc = color_left
        elif k > n / 2:
            fc = color_bg_right
            ec = color_right
            tc = color_right
        else:
            fc = color_bg_center
            ec = color_center
            tc = color_center

        # Draw circle
        circle = plt.Circle((x, y), circle_radius, facecolor=fc,
                             edgecolor=ec, linewidth=1.8, zorder=2)
        ax.add_patch(circle)

        # Draw value
        ax.text(x, y, str(val), ha='center', va='center',
                fontsize=13, fontweight='bold', color=tc, zorder=3)

    # Draw row label on the left
    x_label = -n / 2.0 - 0.9
    ax.text(x_label, y, f'$n={n}$', ha='center', va='center',
            fontsize=10, color='gray')

    # Draw row sum on the right
    x_sum = n / 2.0 + 0.9
    ax.text(x_sum, y, f'$\\Sigma = {row_sum} = 2^{n}$', ha='left', va='center',
            fontsize=10, color='#2c3e50', fontweight='bold')

    # Draw connecting lines to next row
    if n < n_rows - 1:
        next_y = y - 1
        for k in range(n + 1):
            x_curr = k - n / 2.0
            # Connect to left child
            x_left = k - (n + 1) / 2.0
            ax.plot([x_curr, x_left], [y - circle_radius, next_y + circle_radius],
                    '-', color='lightgray', linewidth=0.8, zorder=1)
            # Connect to right child
            x_right = (k + 1) - (n + 1) / 2.0
            ax.plot([x_curr, x_right], [y - circle_radius, next_y + circle_radius],
                    '-', color='lightgray', linewidth=0.8, zorder=1)

ax.set_xlim(-4.5, 6.5)
ax.set_ylim(-1.0, n_rows)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Pascal's Triangle (Rows $n=0$ to $n=5$)",
             fontsize=16, fontweight='bold', pad=15)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=color_bg_left, edgecolor=color_left,
                   linewidth=1.5, label='Left half'),
    mpatches.Patch(facecolor=color_bg_center, edgecolor=color_center,
                   linewidth=1.5, label='Center'),
    mpatches.Patch(facecolor=color_bg_right, edgecolor=color_right,
                   linewidth=1.5, label='Right half (symmetric)'),
]
ax.legend(handles=legend_elements, loc='lower center', ncol=3,
          fontsize=10, frameon=True, edgecolor='lightgray')

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'pascal_triangle.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

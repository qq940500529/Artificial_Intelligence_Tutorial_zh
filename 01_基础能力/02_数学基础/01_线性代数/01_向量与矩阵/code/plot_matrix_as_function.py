# plot_matrix_as_function.py
# Visualize a matrix as a function from R^3 to R^2
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_xlim(-0.5, 11)
ax.set_ylim(-0.5, 6)
ax.set_aspect('equal')
ax.axis('off')

# ── Left box: Input space R^3 ──
left = patches.FancyBboxPatch((0.2, 0.5), 3.8, 4.5,
                              boxstyle="round,pad=0.1",
                              facecolor='#eaf2f8', edgecolor='#2980b9', linewidth=2)
ax.add_patch(left)
ax.text(2.1, 4.6, r'Input space $\mathbb{R}^3$',
        fontsize=13, fontweight='bold', color='#2980b9', ha='center')

# Draw a 3-element column vector in left box
ax.text(2.1, 3.5, r'$\mathbf{x} = $', fontsize=14, ha='right', va='center')
vec_x = patches.FancyBboxPatch((2.15, 1.5), 1.3, 2.5,
                                boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='#2980b9', linewidth=1.5)
ax.add_patch(vec_x)
for i, val in enumerate([1, 2, 3]):
    ax.text(2.8, 3.5 - 0.7 * i, str(val), fontsize=13, ha='center', va='center', color='#2980b9')

# ── Middle: matrix A as the "machine" ──
mid = patches.FancyBboxPatch((4.7, 1.7), 2.3, 2.6,
                             boxstyle="round,pad=0.1",
                             facecolor='#fdf2e9', edgecolor='#e67e22', linewidth=2.5)
ax.add_patch(mid)
ax.text(5.85, 4.0, 'Matrix A', fontsize=13, fontweight='bold', color='#e67e22', ha='center')
ax.text(5.85, 3.5, r'shape $2 \times 3$', fontsize=10, color='#e67e22', ha='center', style='italic')

# 2x3 matrix display
matrix_vals = [[1, 2, 3], [4, 5, 6]]
for i in range(2):
    for j in range(3):
        ax.text(5.0 + 0.55 * j, 2.6 - 0.5 * i, str(matrix_vals[i][j]),
                fontsize=11, ha='center', va='center', color='#e67e22')
# brackets
ax.plot([4.85, 4.85, 4.95], [2.85, 2.05, 2.05], 'k-', linewidth=1.2)
ax.plot([4.85, 4.85, 4.95], [2.85, 2.85, 2.85], 'k-', linewidth=1.2)
ax.plot([6.85, 6.85, 6.75], [2.85, 2.05, 2.05], 'k-', linewidth=1.2)
ax.plot([6.85, 6.85, 6.75], [2.85, 2.85, 2.85], 'k-', linewidth=1.2)

# Arrow from x to A
ax.annotate('', xy=(4.65, 3.0), xytext=(3.55, 3.0),
            arrowprops=dict(arrowstyle='->', color='gray', lw=2))

# Arrow from A to y
ax.annotate('', xy=(7.85, 3.0), xytext=(7.05, 3.0),
            arrowprops=dict(arrowstyle='->', color='gray', lw=2))
ax.text(7.45, 3.25, r'$A\mathbf{x}$', fontsize=11, color='gray', ha='center')

# ── Right box: Output space R^2 ──
right = patches.FancyBboxPatch((7.95, 0.5), 2.8, 4.5,
                               boxstyle="round,pad=0.1",
                               facecolor='#eafaf1', edgecolor='#27ae60', linewidth=2)
ax.add_patch(right)
ax.text(9.35, 4.6, r'Output space $\mathbb{R}^2$',
        fontsize=13, fontweight='bold', color='#27ae60', ha='center')

# 2-element column vector in right box
ax.text(9.0, 3.0, r'$\mathbf{y} = $', fontsize=14, ha='right', va='center')
vec_y = patches.FancyBboxPatch((9.05, 2.0), 1.3, 2.0,
                                boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='#27ae60', linewidth=1.5)
ax.add_patch(vec_y)
for i, val in enumerate([14, 32]):
    ax.text(9.7, 3.5 - 0.7 * i, str(val), fontsize=13, ha='center', va='center', color='#27ae60')

# Caption
ax.text(5.5, 0.1,
        r'A matrix $A \in \mathbb{R}^{m \times n}$ acts as a function: it takes an n-d input and produces an m-d output.',
        fontsize=10, ha='center', style='italic', color='#555')

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'matrix_as_function.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

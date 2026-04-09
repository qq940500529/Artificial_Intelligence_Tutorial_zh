# plot_3d_vectors.py
# Visualize two 3D vectors and their cross product with parallelogram
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')

# Vectors
a = np.array([2, 1, 0])
b = np.array([0, 1, 2])
cross = np.cross(a, b)  # a × b = (1*2 - 0*1, 0*0 - 2*2, 2*1 - 1*0) = (2, -4, 2)

origin = np.array([0, 0, 0])

# Draw vectors as arrows using quiver
arrow_kwargs = dict(arrow_length_ratio=0.08, linewidth=2.5)

# Vector a
ax.quiver(*origin, *a, color='#2980b9', **arrow_kwargs, label=r'$\vec{a}=(2,1,0)$')
# Vector b
ax.quiver(*origin, *b, color='#e74c3c', **arrow_kwargs, label=r'$\vec{b}=(0,1,2)$')
# Cross product
ax.quiver(*origin, *cross, color='#27ae60', **arrow_kwargs,
          label=r'$\vec{a}\times\vec{b}=(2,-4,2)$')

# Draw the parallelogram formed by a and b
parallelogram_verts = [
    origin,
    a,
    a + b,
    b
]
para = Poly3DCollection([parallelogram_verts], alpha=0.2,
                         facecolor='#9b59b6', edgecolor='#8e44ad', linewidth=1.5)
ax.add_collection3d(para)

# Draw parallelogram edges
for i in range(4):
    p1 = parallelogram_verts[i]
    p2 = parallelogram_verts[(i + 1) % 4]
    ax.plot(*zip(p1, p2), color='#8e44ad', linewidth=1.2, linestyle='--')

# Label the vectors at their tips
offset = 0.15
ax.text(a[0] + offset, a[1] + offset, a[2] - 0.3,
        r'$\vec{a}=(2,1,0)$', fontsize=11, color='#2980b9', fontweight='bold')
ax.text(b[0] - 0.8, b[1] + offset, b[2] + offset,
        r'$\vec{b}=(0,1,2)$', fontsize=11, color='#e74c3c', fontweight='bold')
ax.text(cross[0] + offset, cross[1] - 0.3, cross[2] + 0.2,
        r'$\vec{a}\times\vec{b}=(2,-4,2)$', fontsize=11, color='#27ae60', fontweight='bold')

# Mark the origin
ax.scatter(*origin, color='black', s=40, zorder=5)
ax.text(-0.3, -0.3, -0.3, '$O$', fontsize=12, fontweight='bold')

# Draw dashed lines showing perpendicularity hint
# Right angle markers are hard in 3D, so just add text annotation
mid_para = (a + b) / 2
ax.plot([0, cross[0] * 0.3], [0, cross[1] * 0.3], [0, cross[2] * 0.3],
        ':', color='#27ae60', linewidth=1, alpha=0.5)

# Add annotation for perpendicularity
ax.text(0.3, -2.5, 3.5,
        r'$\vec{a}\times\vec{b} \perp \vec{a}$' + '\n' +
        r'$\vec{a}\times\vec{b} \perp \vec{b}$' + '\n' +
        r'$|\vec{a}\times\vec{b}|$ = parallelogram area',
        fontsize=10, color='#2c3e50',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#eafaf1', alpha=0.9))

# Style
ax.set_xlabel('$x$', fontsize=12, labelpad=8)
ax.set_ylabel('$y$', fontsize=12, labelpad=8)
ax.set_zlabel('$z$', fontsize=12, labelpad=8)
ax.set_title('Cross Product: $\\vec{a} \\times \\vec{b}$', fontsize=15, fontweight='bold', pad=15)

# Set limits
max_val = 5
ax.set_xlim(-1, max_val)
ax.set_ylim(-max_val, max_val)
ax.set_zlim(-1, max_val)

# Grid
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('lightgray')
ax.yaxis.pane.set_edgecolor('lightgray')
ax.zaxis.pane.set_edgecolor('lightgray')
ax.grid(True, alpha=0.3)

# Set a good viewing angle
ax.view_init(elev=20, azim=-55)

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, '3d_vectors.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

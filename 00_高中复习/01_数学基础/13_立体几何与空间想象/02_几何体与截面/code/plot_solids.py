# plot_solids.py
# Visualize four basic 3D geometric solids
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(12, 10))

# ── Helper ──
def set_ax_style(ax, title):
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel('$x$', fontsize=10)
    ax.set_ylabel('$y$', fontsize=10)
    ax.set_zlabel('$z$', fontsize=10)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.grid(True, alpha=0.3)

# ── 1. Rectangular Prism (Cube) ──
ax1 = fig.add_subplot(221, projection='3d')

# Vertices of a unit cube
v = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],
              [0,0,1],[1,0,1],[1,1,1],[0,1,1]])
faces = [
    [v[0],v[1],v[2],v[3]],  # bottom
    [v[4],v[5],v[6],v[7]],  # top
    [v[0],v[1],v[5],v[4]],  # front
    [v[2],v[3],v[7],v[6]],  # back
    [v[0],v[3],v[7],v[4]],  # left
    [v[1],v[2],v[6],v[5]],  # right
]
ax1.add_collection3d(Poly3DCollection(
    faces, alpha=0.15, facecolor='#3498db', edgecolor='#2c3e50', linewidth=1.2))

# Draw wireframe edges more prominently
edges = [
    (0,1),(1,2),(2,3),(3,0),  # bottom
    (4,5),(5,6),(6,7),(7,4),  # top
    (0,4),(1,5),(2,6),(3,7),  # verticals
]
for i, j in edges:
    ax1.plot3D(*zip(v[i], v[j]), color='#2c3e50', linewidth=1.0)

# Mark vertices
for vi in v:
    ax1.scatter(*vi, color='#2c3e50', s=15, zorder=5)

set_ax_style(ax1, 'Cube (Rectangular Prism)')
ax1.set_xlim(-0.2, 1.3)
ax1.set_ylim(-0.2, 1.3)
ax1.set_zlim(-0.2, 1.3)

# ── 2. Triangular Pyramid (Tetrahedron) ──
ax2 = fig.add_subplot(222, projection='3d')

# Regular tetrahedron vertices
t = np.array([
    [1, 1, 1],
    [1, -1, -1],
    [-1, 1, -1],
    [-1, -1, 1]
], dtype=float)

# Scale to unit-ish size
t = t * 0.5

tri_faces = [
    [t[0], t[1], t[2]],
    [t[0], t[1], t[3]],
    [t[0], t[2], t[3]],
    [t[1], t[2], t[3]],
]
colors = ['#e74c3c', '#f39c12', '#27ae60', '#9b59b6']
for face, c in zip(tri_faces, colors):
    ax2.add_collection3d(Poly3DCollection(
        [face], alpha=0.2, facecolor=c, edgecolor='#2c3e50', linewidth=1.2))

# Edges
tri_edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
for i, j in tri_edges:
    ax2.plot3D(*zip(t[i], t[j]), color='#2c3e50', linewidth=1.0)
for vi in t:
    ax2.scatter(*vi, color='#2c3e50', s=20, zorder=5)

set_ax_style(ax2, 'Tetrahedron (Triangular Pyramid)')
ax2.set_xlim(-1, 1)
ax2.set_ylim(-1, 1)
ax2.set_zlim(-1, 1)

# ── 3. Cylinder ──
ax3 = fig.add_subplot(223, projection='3d')

theta = np.linspace(0, 2 * np.pi, 60)
z_cyl = np.linspace(0, 1.5, 2)
Theta, Z = np.meshgrid(theta, z_cyl)
X = 0.6 * np.cos(Theta)
Y = 0.6 * np.sin(Theta)

# Surface
ax3.plot_surface(X, Y, Z, alpha=0.15, color='#f39c12', edgecolor='none')

# Wireframe circles top and bottom
for z_val in [0, 1.5]:
    ax3.plot(0.6 * np.cos(theta), 0.6 * np.sin(theta),
             np.full_like(theta, z_val), color='#d35400', linewidth=1.2)

# Vertical lines
for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    x_line = 0.6 * np.cos(angle)
    y_line = 0.6 * np.sin(angle)
    ax3.plot([x_line, x_line], [y_line, y_line], [0, 1.5],
             color='#d35400', linewidth=0.5, alpha=0.5)

set_ax_style(ax3, 'Cylinder')
ax3.set_xlim(-1, 1)
ax3.set_ylim(-1, 1)
ax3.set_zlim(-0.2, 1.8)

# ── 4. Cone ──
ax4 = fig.add_subplot(224, projection='3d')

# Parametric cone
r_cone = np.linspace(0, 0.6, 20)
theta_cone = np.linspace(0, 2 * np.pi, 60)
R, Theta_c = np.meshgrid(r_cone, theta_cone)
X_cone = R * np.cos(Theta_c)
Y_cone = R * np.sin(Theta_c)
Z_cone = 1.5 * (1 - R / 0.6)  # apex at z=1.5, base at z=0

ax4.plot_surface(X_cone, Y_cone, Z_cone, alpha=0.15, color='#27ae60', edgecolor='none')

# Base circle
ax4.plot(0.6 * np.cos(theta), 0.6 * np.sin(theta),
         np.zeros_like(theta), color='#1e8449', linewidth=1.2)

# Slant lines
for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    x_base = 0.6 * np.cos(angle)
    y_base = 0.6 * np.sin(angle)
    ax4.plot([x_base, 0], [y_base, 0], [0, 1.5],
             color='#1e8449', linewidth=0.6, alpha=0.5)

# Apex point
ax4.scatter(0, 0, 1.5, color='#c0392b', s=30, zorder=5)
ax4.text(0.05, 0.05, 1.6, 'Apex', fontsize=9, color='#c0392b')

set_ax_style(ax4, 'Cone')
ax4.set_xlim(-1, 1)
ax4.set_ylim(-1, 1)
ax4.set_zlim(-0.2, 1.8)

fig.suptitle('Basic 3D Geometric Solids', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'geometric_solids.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

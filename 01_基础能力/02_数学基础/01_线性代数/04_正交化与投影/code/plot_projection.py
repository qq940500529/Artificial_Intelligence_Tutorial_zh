# plot_projection.py
# Visualize orthogonal projection of a vector onto a direction
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

v = np.array([3.0, 2.0])
u = np.array([4.0, 0.5])
proj = (v @ u) / (u @ u) * u
res = v - proj

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-0.5, 5)
ax.set_ylim(-0.5, 3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)

# Direction line (extended)
t = np.linspace(-0.5, 1.5, 100)
line_x = t * u[0]
line_y = t * u[1]
ax.plot(line_x, line_y, '--', color='black', lw=1.2, alpha=0.7,
        label=r'Direction line spanned by $\mathbf{u}$')

# v vector (blue)
ax.annotate('', xy=v, xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2.5))
ax.text(v[0] + 0.05, v[1] + 0.1, r'$\mathbf{v}$',
        fontsize=15, color='#2980b9', fontweight='bold')

# u vector (gray, on the direction line)
ax.annotate('', xy=u, xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
ax.text(u[0] - 0.1, u[1] - 0.25, r'$\mathbf{u}$',
        fontsize=14, color='#7f8c8d', fontweight='bold')

# Projection (green)
ax.annotate('', xy=proj, xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.8))
ax.text(proj[0] - 0.7, proj[1] - 0.35, r'$\mathrm{proj}_{\mathbf{u}}(\mathbf{v})$',
        fontsize=12, color='#27ae60', fontweight='bold')

# Residual (red): from proj to v
ax.annotate('', xy=v, xytext=proj,
            arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5))
ax.text((proj[0] + v[0]) / 2 + 0.1, (proj[1] + v[1]) / 2,
        r'residual = $\mathbf{v} - \mathrm{proj}_{\mathbf{u}}(\mathbf{v})$',
        fontsize=11, color='#e74c3c')

# Right-angle marker at the foot of the projection
size = 0.15
u_dir = u / np.linalg.norm(u)
n_dir = np.array([-u_dir[1], u_dir[0]])  # perpendicular
p1 = proj
p2 = proj + size * u_dir
p3 = proj + size * u_dir + size * n_dir
p4 = proj + size * n_dir
ax.plot([p1[0], p2[0], p3[0], p4[0], p1[0]],
        [p1[1], p2[1], p3[1], p4[1], p1[1]],
        color='#e74c3c', lw=1.2)

ax.set_title('Orthogonal projection of $\\mathbf{v}$ onto $\\mathbf{u}$\n'
             r'Residual is perpendicular to $\mathbf{u}$',
             fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlabel('$x_1$', fontsize=11)
ax.set_ylabel('$x_2$', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'projection.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

# plot_svd_geometry.py
# Visualize SVD = rotate -> scale -> rotate
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# A 2x2 matrix
A = np.array([[2.0, 1.0],
              [0.5, 1.5]])
U, s, Vt = np.linalg.svd(A)
Sigma = np.diag(s)

# Unit circle and the right-singular vectors as basis arrows
theta = np.linspace(0, 2 * np.pi, 200)
circle = np.array([np.cos(theta), np.sin(theta)])
e1 = np.array([1.0, 0.0]); e2 = np.array([0.0, 1.0])

# Step results
after_Vt = Vt @ circle
after_Sigma = Sigma @ after_Vt
after_U = U @ after_Sigma  # = A @ circle

fig, axes = plt.subplots(2, 2, figsize=(12, 11))


def draw_basis(ax, b1, b2, color1='#e74c3c', color2='#27ae60'):
    ax.annotate('', xy=b1, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color1, lw=2.5))
    ax.annotate('', xy=b2, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color2, lw=2.5))


def setup(ax, title, lim=2.5):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=9)


# (0) Original
setup(axes[0, 0], 'Step 0: unit circle\n+ right-singular vectors $\\mathbf{v}_1, \\mathbf{v}_2$')
axes[0, 0].plot(circle[0], circle[1], color='gray', lw=1.5)
draw_basis(axes[0, 0], Vt[0], Vt[1])  # show v1, v2

# (1) After V^T (rotation)
setup(axes[0, 1], r'Step 1: $V^\top$ rotates so $\mathbf{v}_i \to \mathbf{e}_i$',)
axes[0, 1].plot(after_Vt[0], after_Vt[1], color='gray', lw=1.5)
draw_basis(axes[0, 1], e1, e2)

# (2) After Sigma (scaling)
setup(axes[1, 0], f'Step 2: $\\Sigma$ stretches axes\nby singular values {s[0]:.2f}, {s[1]:.2f}', lim=4)
axes[1, 0].plot(after_Sigma[0], after_Sigma[1], color='gray', lw=1.5)
draw_basis(axes[1, 0], s[0] * e1, s[1] * e2)

# (3) After U (rotation): final = A @ circle
setup(axes[1, 1], r'Step 3: $U$ rotates ellipse to final position'
      '\n= $A\\mathbf{x}$ for $\\mathbf{x}$ on unit circle', lim=4)
axes[1, 1].plot(after_U[0], after_U[1], color='gray', lw=1.5)
# Show U columns (the left-singular vectors), scaled by sigmas
draw_basis(axes[1, 1], s[0] * U[:, 0], s[1] * U[:, 1])

fig.suptitle(r'SVD $A = U\,\Sigma\,V^\top$ : rotate $\to$ scale $\to$ rotate',
             fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'svd_geometry.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

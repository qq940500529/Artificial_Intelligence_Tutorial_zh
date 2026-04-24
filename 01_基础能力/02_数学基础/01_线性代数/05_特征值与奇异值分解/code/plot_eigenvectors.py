# plot_eigenvectors.py
# Visualize eigenvectors of a 2x2 matrix
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

A = np.array([[4, 1],
              [2, 3]], dtype=float)
eigvals, eigvecs = np.linalg.eig(A)

# Sort by descending eigenvalue for clarity
order = np.argsort(-eigvals)
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]
v1 = eigvecs[:, 0]; v2 = eigvecs[:, 1]
lam1 = eigvals[0]; lam2 = eigvals[1]

# A non-eigen direction for contrast
w = np.array([1.0, 0.0])

# Unit circle and its image under A (an ellipse)
theta = np.linspace(0, 2 * np.pi, 200)
circle = np.array([np.cos(theta), np.sin(theta)])  # 2 x 200
image = A @ circle

fig, axes = plt.subplots(1, 2, figsize=(12, 6))


def setup(ax, xlim, ylim, title):
    ax.set_xlim(xlim); ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# Left: before
setup(axes[0], (-2, 2), (-2, 2), 'Before transform: unit circle\n+ eigen-directions (red, green)')
axes[0].plot(circle[0], circle[1], color='gray', lw=1.5, alpha=0.6)

axes[0].annotate('', xy=v1, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5))
axes[0].text(v1[0] + 0.05, v1[1] + 0.1, r'$\mathbf{v}_1$', fontsize=13,
             color='#e74c3c', fontweight='bold')

axes[0].annotate('', xy=v2, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5))
axes[0].text(v2[0] + 0.05, v2[1] - 0.18, r'$\mathbf{v}_2$', fontsize=13,
             color='#27ae60', fontweight='bold')

axes[0].annotate('', xy=w, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2.0))
axes[0].text(w[0] + 0.05, w[1] - 0.2, r'$\mathbf{w}$ (non-eigen)', fontsize=10,
             color='#2980b9')

# Right: after
setup(axes[1], (-7, 7), (-6, 6),
      f'After transform $A$: ellipse\n$\\mathbf{{v}}_1$ x{lam1:.1f},  $\\mathbf{{v}}_2$ x{lam2:.1f}')
axes[1].plot(image[0], image[1], color='gray', lw=1.5, alpha=0.6)

Av1 = A @ v1
Av2 = A @ v2
Aw = A @ w

# eigen-directions only stretch
axes[1].annotate('', xy=Av1, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.8))
axes[1].text(Av1[0] + 0.1, Av1[1] + 0.2,
             r'$A\mathbf{v}_1=' + f'{lam1:.1f}' + r'\mathbf{v}_1$',
             fontsize=11, color='#e74c3c', fontweight='bold')

axes[1].annotate('', xy=Av2, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.8))
axes[1].text(Av2[0] - 1.5, Av2[1] - 0.6,
             r'$A\mathbf{v}_2=' + f'{lam2:.1f}' + r'\mathbf{v}_2$',
             fontsize=11, color='#27ae60', fontweight='bold')

# w changes both length and direction
axes[1].annotate('', xy=Aw, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2.0))
axes[1].text(Aw[0] + 0.1, Aw[1] + 0.1,
             r'$A\mathbf{w}$ (direction changed!)',
             fontsize=10, color='#2980b9')
# show original w lightly
axes[1].annotate('', xy=w, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#2980b9', lw=1.0, alpha=0.4))

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'eigenvectors.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

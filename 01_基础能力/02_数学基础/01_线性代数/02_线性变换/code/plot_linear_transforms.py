# plot_linear_transforms.py
# Visualize four basic linear transformations
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def make_cat():
    """Return a set of 2D points forming a stylized cat shape."""
    # body (rectangle outline)
    body = np.array([[-0.5, 0], [0.5, 0], [0.5, 0.6], [-0.5, 0.6], [-0.5, 0]])
    # left ear
    ear_l = np.array([[-0.5, 0.6], [-0.4, 0.9], [-0.2, 0.6]])
    # right ear
    ear_r = np.array([[0.2, 0.6], [0.4, 0.9], [0.5, 0.6]])
    return [body, ear_l, ear_r]


def draw_shape(ax, shapes, color, alpha=0.7, lw=2):
    for s in shapes:
        ax.plot(s[:, 0], s[:, 1], color=color, alpha=alpha, lw=lw)
        ax.fill(s[:, 0], s[:, 1], color=color, alpha=alpha * 0.3)


def draw_basis(ax, A=np.eye(2), color='black'):
    """Draw the basis vectors after applying matrix A."""
    e1 = A @ np.array([1, 0])
    e2 = A @ np.array([0, 1])
    ax.annotate('', xy=e1, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.0))
    ax.annotate('', xy=e2, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.0))


def setup_ax(ax, title, xlim=(-1.6, 1.6), ylim=(-1.0, 1.6)):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.tick_params(labelsize=8)


# Define four transformations
theta = np.pi / 4  # 45 deg
transforms = [
    ('(a) Rotation 45°',
     np.array([[np.cos(theta), -np.sin(theta)],
               [np.sin(theta),  np.cos(theta)]])),
    ('(b) Scaling diag(1.5, 0.6)',
     np.array([[1.5, 0.0],
               [0.0, 0.6]])),
    ('(c) Shear k=0.7 along x',
     np.array([[1.0, 0.7],
               [0.0, 1.0]])),
    ('(d) Projection onto x-axis',
     np.array([[1.0, 0.0],
               [0.0, 0.0]])),
]

fig, axes = plt.subplots(4, 2, figsize=(10, 14))
cat = make_cat()

for row, (label, M) in enumerate(transforms):
    # Original (left)
    ax_l = axes[row, 0]
    setup_ax(ax_l, 'Before')
    draw_shape(ax_l, cat, color='#2980b9')
    draw_basis(ax_l, np.eye(2), color='#2980b9')

    # After transformation (right)
    ax_r = axes[row, 1]
    transformed = [s @ M.T for s in cat]   # apply M to each point (row vectors)
    setup_ax(ax_r, label)
    draw_shape(ax_r, transformed, color='#e74c3c')
    draw_basis(ax_r, M, color='#e74c3c')

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'linear_transforms.png')
plt.savefig(output_path, dpi=140, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

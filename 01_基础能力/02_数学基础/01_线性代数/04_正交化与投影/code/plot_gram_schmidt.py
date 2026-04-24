# plot_gram_schmidt.py
# Visualize a 2D Gram-Schmidt procedure step by step
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

a1 = np.array([3.0, 1.0])
a2 = np.array([1.5, 2.5])

# Step 1: u1 = a1
u1 = a1.copy()
# Step 2: u2 = a2 - proj_u1(a2)
proj = (a2 @ u1) / (u1 @ u1) * u1
u2 = a2 - proj
# Normalize
q1 = u1 / np.linalg.norm(u1)
q2 = u2 / np.linalg.norm(u2)


def setup_ax(ax, title):
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 3.2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=9)


def arrow(ax, vec, color, label, offset=(0.05, 0.1), lw=2.5, fontsize=13):
    ax.annotate('', xy=vec, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    ax.text(vec[0] + offset[0], vec[1] + offset[1], label,
            fontsize=fontsize, color=color, fontweight='bold')


fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: original a1, a2 (not orthogonal)
setup_ax(axes[0], 'Step 0: original $\\mathbf{a}_1, \\mathbf{a}_2$\n(not orthogonal)')
arrow(axes[0], a1, '#2980b9', r'$\mathbf{a}_1$')
arrow(axes[0], a2, '#e67e22', r'$\mathbf{a}_2$')

# Panel 2: subtract projection
setup_ax(axes[1], r'Step 1-2: $\mathbf{u}_2 = \mathbf{a}_2 - \mathrm{proj}_{\mathbf{u}_1}(\mathbf{a}_2)$')
arrow(axes[1], u1, '#2980b9', r'$\mathbf{u}_1=\mathbf{a}_1$')
# show a2 lightly
axes[1].annotate('', xy=a2, xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5, alpha=0.4))
axes[1].text(a2[0] + 0.05, a2[1] + 0.1, r'$\mathbf{a}_2$',
             fontsize=11, color='#e67e22', alpha=0.6)
# projection vector (from origin to proj)
arrow(axes[1], proj, '#27ae60', r'$\mathrm{proj}_{\mathbf{u}_1}(\mathbf{a}_2)$',
      offset=(-0.6, -0.35), lw=1.8, fontsize=10)
# residual u2 (from proj to a2)
axes[1].annotate('', xy=a2, xytext=proj,
                 arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2.5))
axes[1].text((proj[0] + a2[0]) / 2 - 0.4, (proj[1] + a2[1]) / 2 + 0.1,
             r'$\mathbf{u}_2$ (perp. to $\mathbf{u}_1$)',
             fontsize=10, color='#c0392b')
# small right-angle marker at proj
size = 0.12
ud = u1 / np.linalg.norm(u1)
nd = np.array([-ud[1], ud[0]])
pts = np.array([proj, proj + size * ud, proj + size * ud + size * nd, proj + size * nd, proj])
axes[1].plot(pts[:, 0], pts[:, 1], color='#c0392b', lw=1)

# Panel 3: normalized q1, q2
setup_ax(axes[2], 'Step 3: normalize -> $\\mathbf{q}_1, \\mathbf{q}_2$\n(orthonormal)')
arrow(axes[2], q1, '#2980b9', r'$\mathbf{q}_1$', lw=3)
arrow(axes[2], q2, '#c0392b', r'$\mathbf{q}_2$', lw=3)
# unit circle for reference
theta = np.linspace(0, 2 * np.pi, 200)
axes[2].plot(np.cos(theta), np.sin(theta), '--', color='gray', lw=0.8, alpha=0.5)
axes[2].text(0.95, -0.35, 'unit circle', color='gray', fontsize=9, alpha=0.7)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'gram_schmidt.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

# plot_conditional_prob.py
# Venn diagram illustrating conditional probability P(A|B) = P(A∩B)/P(B)
# Requirements: Python 3.10+, matplotlib >= 3.7

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from matplotlib.collections import PatchCollection

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'conditional_probability.png')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


def draw_venn_base(ax):
    """Draw the sample space rectangle and two overlapping circles."""
    rect = Rectangle((-3.2, -2.5), 6.4, 5.0, linewidth=2,
                     edgecolor='#333333', facecolor='#f8f8f8', zorder=0)
    ax.add_patch(rect)
    ax.text(2.8, 2.2, r'$\Omega$', fontsize=18, fontweight='bold', color='#333333')
    return rect


# ========== Left subplot: Standard Venn with A∩B highlighted ==========
ax = ax1
draw_venn_base(ax)

# Draw circles A and B
circle_a = Circle((-0.7, 0), 1.6, linewidth=2, edgecolor='#2166AC',
                  facecolor='#2166AC', alpha=0.15, zorder=1)
circle_b = Circle((0.7, 0), 1.6, linewidth=2, edgecolor='#B2182B',
                  facecolor='#B2182B', alpha=0.15, zorder=1)
ax.add_patch(circle_a)
ax.add_patch(circle_b)

# Highlight intersection A∩B using a filled region
theta = np.linspace(0, 2 * np.pi, 300)
ax_c = -0.7 + 1.6 * np.cos(theta)
ay_c = 0 + 1.6 * np.sin(theta)
bx_c = 0.7 + 1.6 * np.cos(theta)
by_c = 0 + 1.6 * np.sin(theta)

# Fill intersection via clip paths
circle_a_fill = Circle((-0.7, 0), 1.6, facecolor='#7B2D8E', alpha=0.45,
                       edgecolor='none', zorder=2)
ax.add_patch(circle_a_fill)
circle_b_clip = Circle((0.7, 0), 1.6, transform=ax.transData)
circle_a_fill.set_clip_path(circle_b_clip)

# Circle outlines on top
circle_a_outline = Circle((-0.7, 0), 1.6, linewidth=2.5, edgecolor='#2166AC',
                          facecolor='none', zorder=3)
circle_b_outline = Circle((0.7, 0), 1.6, linewidth=2.5, edgecolor='#B2182B',
                          facecolor='none', zorder=3)
ax.add_patch(circle_a_outline)
ax.add_patch(circle_b_outline)

# Labels
ax.text(-1.6, 0, r'$A$', fontsize=22, fontweight='bold', color='#2166AC',
        ha='center', va='center', zorder=4)
ax.text(1.6, 0, r'$B$', fontsize=22, fontweight='bold', color='#B2182B',
        ha='center', va='center', zorder=4)
ax.text(0, 0, r'$A \cap B$', fontsize=14, fontweight='bold', color='white',
        ha='center', va='center', zorder=4)

ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.7, 2.7)
ax.set_aspect('equal')
ax.set_title('Events A and B in Sample Space $\\Omega$',
             fontsize=14, fontweight='bold', pad=12)
ax.axis('off')


# ========== Right subplot: Conditional — "Given B" ==========
ax = ax2
draw_venn_base(ax)

# Dimmed circle A (outside B)
circle_a_dim = Circle((-0.7, 0), 1.6, linewidth=2, edgecolor='#2166AC',
                      facecolor='#2166AC', alpha=0.06, zorder=1)
ax.add_patch(circle_a_dim)

# Highlighted circle B
circle_b_highlight = Circle((0.7, 0), 1.6, linewidth=2.5, edgecolor='#B2182B',
                            facecolor='#B2182B', alpha=0.20, zorder=1)
ax.add_patch(circle_b_highlight)

# Strongly highlighted intersection
circle_ab_fill = Circle((-0.7, 0), 1.6, facecolor='#D6604D', alpha=0.55,
                        edgecolor='none', zorder=2)
ax.add_patch(circle_ab_fill)
circle_b_clip2 = Circle((0.7, 0), 1.6, transform=ax.transData)
circle_ab_fill.set_clip_path(circle_b_clip2)

# Outlines
circle_a_out2 = Circle((-0.7, 0), 1.6, linewidth=2, edgecolor='#2166AC',
                       facecolor='none', linestyle='--', alpha=0.5, zorder=3)
circle_b_out2 = Circle((0.7, 0), 1.6, linewidth=3, edgecolor='#B2182B',
                       facecolor='none', zorder=3)
ax.add_patch(circle_a_out2)
ax.add_patch(circle_b_out2)

# Labels
ax.text(-1.6, 0, r'$A$', fontsize=22, fontweight='bold', color='#2166AC',
        alpha=0.4, ha='center', va='center', zorder=4)
ax.text(1.6, 0, r'$B$', fontsize=22, fontweight='bold', color='#B2182B',
        ha='center', va='center', zorder=4)
ax.text(0, 0, r'$A \cap B$', fontsize=14, fontweight='bold', color='white',
        ha='center', va='center', zorder=4)

# Formula annotation
ax.text(0, -2.0,
        r'$P(A \mid B) = \dfrac{P(A \cap B)}{P(B)}$',
        fontsize=16, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFDE7',
                  edgecolor='#F9A825', linewidth=1.5),
        zorder=5)

# Arrow pointing to the highlighted region
ax.annotate('', xy=(0.15, -0.5), xytext=(0.15, -1.5),
            arrowprops=dict(arrowstyle='->', color='#F9A825', lw=2),
            zorder=5)

ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.7, 2.7)
ax.set_aspect('equal')
ax.set_title('Conditional: Given B occurred',
             fontsize=14, fontweight='bold', pad=12)
ax.axis('off')

plt.tight_layout(pad=1.5)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Chart saved to {output_path}")

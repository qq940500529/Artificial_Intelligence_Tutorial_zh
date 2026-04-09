# plot_set_operations.py
# Visualize 4 set operations using Venn diagrams
# Requirements: Python 3.10+, matplotlib >= 3.7

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'set_operations.png')

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Circle centers and radius
cA = (-0.5, 0)
cB = (0.5, 0)
radius = 1.3


def draw_frame(ax, title):
    """Draw the sample space rectangle and base circle outlines."""
    rect = Rectangle((-2.5, -2.0), 5.0, 4.0, linewidth=2,
                     edgecolor='#333333', facecolor='#f0f0f0', zorder=0)
    ax.add_patch(rect)
    ax.text(2.1, 1.7, r'$\Omega$', fontsize=16, fontweight='bold', color='#333333')
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.axis('off')


def add_circle_outlines(ax):
    """Add circle outlines for A and B."""
    cA_patch = Circle(cA, radius, linewidth=2.5, edgecolor='#2166AC',
                      facecolor='none', zorder=4)
    cB_patch = Circle(cB, radius, linewidth=2.5, edgecolor='#B2182B',
                      facecolor='none', zorder=4)
    ax.add_patch(cA_patch)
    ax.add_patch(cB_patch)
    ax.text(cA[0] - 0.6, cA[1] + 0.1, r'$A$', fontsize=18,
            fontweight='bold', color='#2166AC', zorder=5)
    ax.text(cB[0] + 0.6, cB[1] + 0.1, r'$B$', fontsize=18,
            fontweight='bold', color='#B2182B', zorder=5)


# ========== Top-left: Union A ∪ B ==========
ax = axes[0, 0]
draw_frame(ax, r'Union: $A \cup B$')

# Fill both circles
fill_a = Circle(cA, radius, facecolor='#4393C3', alpha=0.45,
                edgecolor='none', zorder=1)
fill_b = Circle(cB, radius, facecolor='#4393C3', alpha=0.45,
                edgecolor='none', zorder=1)
ax.add_patch(fill_a)
ax.add_patch(fill_b)
add_circle_outlines(ax)


# ========== Top-right: Intersection A ∩ B ==========
ax = axes[0, 1]
draw_frame(ax, r'Intersection: $A \cap B$')

# Fill A, then clip to B to get only the intersection
fill_intersection = Circle(cA, radius, facecolor='#D6604D', alpha=0.55,
                           edgecolor='none', zorder=2)
ax.add_patch(fill_intersection)
clip_circle = Circle(cB, radius, transform=ax.transData)
fill_intersection.set_clip_path(clip_circle)
add_circle_outlines(ax)


# ========== Bottom-left: Difference A \ B ==========
ax = axes[1, 0]
draw_frame(ax, r'Difference: $A \setminus B$')

# Fill all of A first
fill_a_diff = Circle(cA, radius, facecolor='#4393C3', alpha=0.45,
                     edgecolor='none', zorder=1)
ax.add_patch(fill_a_diff)

# Cover the intersection part with the background color
# We use a circle B filled with the background color, but clipped to A
cover_ab = Circle(cA, radius, facecolor='#f0f0f0',
                  edgecolor='none', zorder=2)
ax.add_patch(cover_ab)
clip_b = Circle(cB, radius, transform=ax.transData)
cover_ab.set_clip_path(clip_b)
add_circle_outlines(ax)


# ========== Bottom-right: Complement Ā ==========
ax = axes[1, 1]
draw_frame(ax, r'Complement: $\overline{A}$')

# Fill entire rectangle
rect_fill = Rectangle((-2.5, -2.0), 5.0, 4.0,
                       facecolor='#B2ABD2', alpha=0.5, edgecolor='none', zorder=1)
ax.add_patch(rect_fill)

# "Erase" circle A by drawing it with background color
erase_a = Circle(cA, radius, facecolor='#f0f0f0',
                 edgecolor='none', zorder=2)
ax.add_patch(erase_a)

# Only show circle A outline (no B needed for complement)
cA_outline = Circle(cA, radius, linewidth=2.5, edgecolor='#2166AC',
                    facecolor='none', zorder=4)
ax.add_patch(cA_outline)
ax.text(cA[0] - 0.1, cA[1], r'$A$', fontsize=18, fontweight='bold',
        color='#2166AC', ha='center', zorder=5)
ax.text(1.6, -1.3, r'$\overline{A}$', fontsize=16, fontweight='bold',
        color='#6A51A3', zorder=5)

plt.tight_layout(pad=2.0)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Chart saved to {output_path}")

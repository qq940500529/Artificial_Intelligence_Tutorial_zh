# plot_linear_combination.py
# Visualize linearly independent vs linearly dependent vectors
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# ── Left subplot: Linearly Independent ──
ax1.set_title('Linearly Independent', fontsize=14, fontweight='bold')

# Vectors a=(1,0) and b=(0,1)
a = np.array([1, 0])
b = np.array([0, 1])
target = 3 * a + 2 * b  # (3, 2)

# Draw parallelogram: 0 -> 3a -> 3a+2b -> 2b -> 0
parallelogram = plt.Polygon(
    [[0, 0], [3, 0], [3, 2], [0, 2]],
    closed=True, fill=True, facecolor='#d4e6f1', edgecolor='gray',
    linewidth=1, linestyle='--', alpha=0.5, zorder=1
)
ax1.add_patch(parallelogram)

# Draw basis vectors (thick)
ax1.annotate('', xy=a, xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2.5), zorder=3)
ax1.annotate('', xy=b, xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5), zorder=3)

# Draw scaled vectors 3a and 2b (thinner)
ax1.annotate('', xy=(3, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#2980b9', lw=1.2, linestyle='--'), zorder=2)
ax1.annotate('', xy=(0, 2), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.2, linestyle='--'), zorder=2)

# Draw resultant vector to (3,2)
ax1.annotate('', xy=target, xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5), zorder=4)

# Labels
ax1.text(0.55, -0.3, r'$\vec{a}=(1,0)$', color='#2980b9', fontsize=11, fontweight='bold')
ax1.text(-0.9, 0.45, r'$\vec{b}=(0,1)$', color='#e74c3c', fontsize=11, fontweight='bold')
ax1.text(1.5, -0.45, r'$3\vec{a}$', color='#2980b9', fontsize=10, style='italic')
ax1.text(-0.7, 1.1, r'$2\vec{b}$', color='#e74c3c', fontsize=10, style='italic')
ax1.text(3.1, 2.1, r'$3\vec{a}+2\vec{b}=(3,2)$', color='#27ae60', fontsize=11, fontweight='bold')

# Mark the target point
ax1.plot(*target, 'o', color='#27ae60', markersize=8, zorder=5)

# Add a span hint: light gray arrows showing coverage
for xi in np.arange(-0.5, 4.5, 1.0):
    for yi in np.arange(-0.5, 3.5, 1.0):
        if (xi, yi) != (0, 0):
            ax1.plot(xi, yi, '.', color='lightgray', markersize=3, zorder=0)

ax1.set_xlim(-1.5, 5)
ax1.set_ylim(-1, 3.5)
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.axvline(0, color='black', linewidth=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.text(0.5, 3.0, 'Can reach ANY point\nin the plane',
         fontsize=10, color='#27ae60', style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#eafaf1', alpha=0.8))

# ── Right subplot: Linearly Dependent ──
ax2.set_title('Linearly Dependent', fontsize=14, fontweight='bold')

# Vectors a=(1,2) and b=(2,4) — collinear
a2 = np.array([1, 2])
b2 = np.array([2, 4])

# Draw the line they span
t_vals = np.linspace(-1.2, 2.8, 100)
line_x = t_vals * 1
line_y = t_vals * 2
ax2.plot(line_x, line_y, '--', color='gray', linewidth=1.5, alpha=0.6, zorder=1,
         label='Span: 1D line only')

# Draw vector a
ax2.annotate('', xy=a2, xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#2980b9', lw=2.5), zorder=3)
# Draw vector b
ax2.annotate('', xy=b2, xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5), zorder=3)

# Labels
ax2.text(1.15, 1.7, r'$\vec{a}=(1,2)$', color='#2980b9', fontsize=11, fontweight='bold')
ax2.text(2.15, 3.7, r'$\vec{b}=(2,4)=2\vec{a}$', color='#e74c3c', fontsize=11, fontweight='bold')

# Mark an unreachable point
unreachable = np.array([1, -1])
ax2.plot(*unreachable, 'x', color='#95a5a6', markersize=12, markeredgewidth=2.5, zorder=5)
ax2.text(1.2, -1.2, 'Unreachable!', color='#95a5a6', fontsize=10, fontweight='bold')

ax2.set_xlim(-2, 4)
ax2.set_ylim(-2.5, 5.5)
ax2.set_xlabel('$x$', fontsize=12)
ax2.set_ylabel('$y$', fontsize=12)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.axvline(0, color='black', linewidth=0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.text(0.5, -2.0, 'Can only reach points\non ONE line',
         fontsize=10, color='#e74c3c', style='italic',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdedec', alpha=0.8))

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'linear_combination.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

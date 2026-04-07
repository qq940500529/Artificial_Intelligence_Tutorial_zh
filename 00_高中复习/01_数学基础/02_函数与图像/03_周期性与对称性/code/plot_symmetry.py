"""
plot_symmetry.py
Generate plots showing general axis of symmetry and center of symmetry.
Dependencies: matplotlib, numpy
"""
import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- Left: Axis of symmetry at x = 2 ---
ax = axes[0]
x = np.linspace(-1, 5, 500)
y = (x - 2) ** 2 + 1  # parabola with axis of symmetry at x=2

ax.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = (x-2)^2 + 1$')
ax.axvline(x=2, color='red', linestyle='--', linewidth=2, label='Axis of symmetry: $x = 2$')

# Symmetric point pair
x1, x2 = 0.5, 3.5
y1 = (x1 - 2) ** 2 + 1
y2 = (x2 - 2) ** 2 + 1
ax.plot([x1, x2], [y1, y2], 'go', markersize=9, zorder=5)
ax.plot([x1, x2], [y1, y2], 'g--', linewidth=1.5, alpha=0.7)
ax.annotate(f'({x1}, {y1:.1f})', xy=(x1, y1), xytext=(x1 - 0.8, y1 + 1),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))
ax.annotate(f'({x2}, {y2:.1f})', xy=(x2, y2), xytext=(x2 + 0.2, y2 + 1),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xlabel(r'$x$', fontsize=12)
ax.set_ylabel(r'$f(x)$', fontsize=12)
ax.set_title('Axis of Symmetry at $x = 2$', fontsize=13)
ax.legend(fontsize=10, loc='upper right')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-0.5, 10)

# --- Right: Center of symmetry at (1, 0) ---
ax = axes[1]
x = np.linspace(-2, 4, 500)
y = (x - 1) ** 3  # cubic with center of symmetry at (1, 0)

ax.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = (x-1)^3$')
ax.plot(1, 0, 'r*', markersize=18, zorder=5, label='Center of symmetry: $(1, 0)$')

# Symmetric point pair about (1, 0)
x1, x2 = 0, 2
y1 = (x1 - 1) ** 3
y2 = (x2 - 1) ** 3
ax.plot([x1, x2], [y1, y2], 'go', markersize=9, zorder=5)
ax.plot([x1, x2], [y1, y2], 'g--', linewidth=1.5, alpha=0.7)
# Midpoint annotation
ax.annotate('Midpoint = $(1, 0)$', xy=(1, 0), xytext=(2.2, -4),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

ax.annotate(f'$({x1}, {y1})$', xy=(x1, y1), xytext=(x1 - 1.2, y1 - 2),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))
ax.annotate(f'$({x2}, {y2})$', xy=(x2, y2), xytext=(x2 + 0.5, y2 + 2),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1.2))

ax.axhline(y=0, color='black', linewidth=0.8)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel(r'$x$', fontsize=12)
ax.set_ylabel(r'$f(x)$', fontsize=12)
ax.set_title('Center of Symmetry at $(1, 0)$', fontsize=13)
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'symmetry_examples.png'),
            dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("Generated: assets/symmetry_examples.png")

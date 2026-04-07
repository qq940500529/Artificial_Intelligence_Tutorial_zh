"""
plot_periodic_function.py
Generate a plot showing a periodic function with period annotation.
Dependencies: matplotlib, numpy
"""
import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Output path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)

x = np.linspace(-1, 5, 1000)
y = np.sin(2 * np.pi * x)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = \sin(2\pi x)$')

# Annotate the period T = 1
ax.annotate('', xy=(2, -1.3), xytext=(1, -1.3),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax.text(1.5, -1.45, r'$T = 1$', ha='center', va='top', fontsize=14, color='red',
        fontweight='bold')

# Mark repeated points
for xi in [0.25, 1.25, 2.25, 3.25]:
    ax.plot(xi, np.sin(2 * np.pi * xi), 'ro', markersize=7, zorder=5)

# Dashed vertical lines showing period alignment
for xi in [0.25, 1.25, 2.25, 3.25]:
    ax.axvline(x=xi, color='gray', linestyle=':', alpha=0.5, linewidth=1)

ax.axhline(y=0, color='black', linewidth=0.8)
ax.axvline(x=0, color='black', linewidth=0.8)
ax.set_xlabel(r'$x$', fontsize=13)
ax.set_ylabel(r'$f(x)$', fontsize=13)
ax.set_title('Periodic Function: $f(x) = \\sin(2\\pi x)$, Period $T = 1$', fontsize=14)
ax.legend(fontsize=12, loc='upper right')
ax.set_ylim(-1.7, 1.5)
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'periodic_function.png'),
            dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print("Generated: assets/periodic_function.png")

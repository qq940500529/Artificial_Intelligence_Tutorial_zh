# plot_bayes.py
# Visualize Bayesian reasoning with a medical test probability area diagram
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Probabilities
p_sick = 0.001
p_healthy = 0.999
p_pos_sick = 0.99
p_neg_sick = 0.01
p_pos_healthy = 0.01
p_neg_healthy = 0.99

# Area calculation (total width = 1)
# Heights represent sub-populations within each group
fig, ax = plt.subplots(figsize=(11, 6.5))

# Use a proportional area mosaic
# X-axis: Sick (width = p_sick) | Healthy (width = p_healthy)
# But p_sick = 0.001 is too small to see, so use a schematic with exaggerated sick width
# We'll use a log-like scaling: sick gets width 0.15 for visibility, healthy gets 0.85

w_sick = 0.15   # exaggerated for visibility
w_healthy = 0.85
total_h = 1.0

# Sick column
# Positive portion
h_sick_pos = p_pos_sick * total_h  # 0.99
h_sick_neg = p_neg_sick * total_h  # 0.01

# Healthy column
h_healthy_pos = p_pos_healthy * total_h  # 0.01
h_healthy_neg = p_neg_healthy * total_h  # 0.99

x_sick = 0
x_healthy = w_sick + 0.02  # small gap

# Draw rectangles
# Sick + Positive (TRUE POSITIVE)
rect_sp = plt.Rectangle((x_sick, 0), w_sick, h_sick_pos,
                         facecolor='#e74c3c', edgecolor='white', linewidth=1.5, alpha=0.85)
ax.add_patch(rect_sp)
ax.text(x_sick + w_sick / 2, h_sick_pos / 2,
        f'True\nPositive\n{p_sick * p_pos_sick:.5f}',
        ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Sick + Negative (FALSE NEGATIVE)
rect_sn = plt.Rectangle((x_sick, h_sick_pos), w_sick, h_sick_neg,
                         facecolor='#f1948a', edgecolor='white', linewidth=1.5, alpha=0.7)
ax.add_patch(rect_sn)
ax.text(x_sick + w_sick / 2, h_sick_pos + h_sick_neg / 2,
        f'False\nNeg', ha='center', va='center', fontsize=8, color='#922b21')

# Healthy + Positive (FALSE POSITIVE)
rect_hp = plt.Rectangle((x_healthy, 0), w_healthy, h_healthy_pos,
                         facecolor='#f39c12', edgecolor='white', linewidth=1.5, alpha=0.85)
ax.add_patch(rect_hp)
ax.text(x_healthy + w_healthy / 2, h_healthy_pos / 2,
        f'False Positive\n{p_healthy * p_pos_healthy:.5f}',
        ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Healthy + Negative (TRUE NEGATIVE)
rect_hn = plt.Rectangle((x_healthy, h_healthy_pos), w_healthy, h_healthy_neg,
                         facecolor='#3498db', edgecolor='white', linewidth=1.5, alpha=0.75)
ax.add_patch(rect_hn)
ax.text(x_healthy + w_healthy / 2, h_healthy_pos + h_healthy_neg / 2,
        f'True Negative\n{p_healthy * p_neg_healthy:.4f}',
        ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Highlight the "Positive test" band with a bracket
# Draw a horizontal bracket at the bottom spanning both positive regions
bracket_y = -0.08
ax.annotate('', xy=(x_sick, bracket_y), xytext=(x_healthy + w_healthy, bracket_y),
            arrowprops=dict(arrowstyle='|-|', color='#e74c3c', lw=2))
ax.plot([x_sick, x_healthy + w_healthy], [bracket_y, bracket_y],
        '-', color='#c0392b', lw=2)
ax.text((x_sick + x_healthy + w_healthy) / 2, bracket_y - 0.05,
        'All Positive Results', ha='center', va='top',
        fontsize=11, color='#c0392b', fontweight='bold')

# Column headers
ax.text(x_sick + w_sick / 2, 1.06, f'Sick\nP = {p_sick}',
        ha='center', va='bottom', fontsize=11, fontweight='bold', color='#c0392b')
ax.text(x_healthy + w_healthy / 2, 1.06, f'Healthy\nP = {p_healthy}',
        ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2980b9')

# Right-side annotations
# P(sick | positive)
p_positive = p_sick * p_pos_sick + p_healthy * p_pos_healthy
p_sick_given_pos = (p_sick * p_pos_sick) / p_positive

ax.text(1.12, 0.55,
        'Bayesian Result:',
        ha='left', va='center', fontsize=12, fontweight='bold',
        color='#2c3e50', transform=ax.transAxes)
ax.text(1.12, 0.45,
        f'P(Sick | Positive)',
        ha='left', va='center', fontsize=11,
        color='#2c3e50', transform=ax.transAxes)
ax.text(1.12, 0.36,
        f'= {p_sick * p_pos_sick:.5f} / {p_positive:.5f}',
        ha='left', va='center', fontsize=10,
        color='#7f8c8d', transform=ax.transAxes)
ax.text(1.12, 0.26,
        f'$\\approx$ {p_sick_given_pos:.1%}',
        ha='left', va='center', fontsize=14, fontweight='bold',
        color='#e74c3c', transform=ax.transAxes)
ax.text(1.12, 0.16,
        f'NOT 99% !',
        ha='left', va='center', fontsize=11,
        color='#e74c3c', style='italic', transform=ax.transAxes)

# Note about exaggerated width
ax.text(x_sick + w_sick / 2, -0.19,
        '(width exaggerated\nfor visibility)',
        ha='center', va='top', fontsize=8, color='gray', style='italic')

ax.set_xlim(-0.05, 1.08)
ax.set_ylim(-0.25, 1.2)
ax.set_aspect('auto')
ax.axis('off')
ax.set_title('Medical Test: Why 99% Accuracy $\\neq$ 99% Certainty',
             fontsize=14, fontweight='bold', pad=20)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#e74c3c', alpha=0.85, label='True Positive (sick + positive)'),
    mpatches.Patch(facecolor='#f39c12', alpha=0.85, label='False Positive (healthy + positive)'),
    mpatches.Patch(facecolor='#3498db', alpha=0.75, label='True Negative (healthy + negative)'),
    mpatches.Patch(facecolor='#f1948a', alpha=0.7, label='False Negative (sick + negative)'),
]
ax.legend(handles=legend_elements, loc='upper left',
          bbox_to_anchor=(0.0, -0.02), ncol=2, fontsize=9,
          frameon=True, edgecolor='lightgray')

plt.tight_layout()

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'bayes_reasoning.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

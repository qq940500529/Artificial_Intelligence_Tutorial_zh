# plot_chart_types.py
# Generate a 2x2 subplot showing 4 common chart types
# Requirements: Python 3.10+, matplotlib >= 3.7, numpy >= 1.24

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Output path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'chart_types.png')

np.random.seed(42)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# --- Top-left: Bar chart (exam scores by subject) ---
ax = axes[0, 0]
subjects = ['Math', 'Physics', 'Chemistry', 'English', 'Biology']
scores = [88, 76, 82, 91, 70]
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974']
bars = ax.bar(subjects, scores, color=colors, edgecolor='white', linewidth=1.2)
for bar, score in zip(bars, scores):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            str(score), ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('Bar Chart: Exam Scores by Subject', fontsize=13, fontweight='bold', pad=10)
ax.set_ylabel('Score', fontsize=11)
ax.set_ylim(0, 105)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# --- Top-right: Histogram (student height distribution) ---
ax = axes[0, 1]
heights = np.random.normal(loc=168, scale=8, size=300)
n, bins, patches = ax.hist(heights, bins=20, color='#55A868', edgecolor='white',
                           alpha=0.85, density=True)
# Overlay a smooth normal curve (using numpy, no scipy needed)
x_smooth = np.linspace(heights.min(), heights.max(), 200)
mu, std = heights.mean(), heights.std()
normal_pdf = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_smooth - mu) / std) ** 2)
ax.plot(x_smooth, normal_pdf, color='#C44E52',
        linewidth=2.5, label=f'Normal fit ($\\mu$={mu:.1f}, $\\sigma$={std:.1f})')
ax.axvline(mu, color='#C44E52', linestyle='--', alpha=0.7, linewidth=1.5)
ax.set_title('Histogram: Student Height Distribution', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Height (cm)', fontsize=11)
ax.set_ylabel('Density', fontsize=11)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# --- Bottom-left: Pie chart (time allocation) ---
ax = axes[1, 0]
activities = ['Study', 'Sleep', 'Exercise', 'Social', 'Other']
hours = [6, 8, 2, 3, 5]
pie_colors = ['#4C72B0', '#8172B2', '#55A868', '#CCB974', '#C44E52']
explode = (0.05, 0, 0, 0, 0)
wedges, texts, autotexts = ax.pie(
    hours, labels=activities, autopct='%1.1f%%', startangle=90,
    colors=pie_colors, explode=explode, pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2))
for t in autotexts:
    t.set_fontsize(10)
    t.set_fontweight('bold')
ax.set_title('Pie Chart: Daily Time Allocation', fontsize=13, fontweight='bold', pad=10)

# --- Bottom-right: Box plot (comparing 3 groups) ---
ax = axes[1, 1]
group_a = np.random.normal(78, 6, 60)
group_b = np.random.normal(85, 10, 60)
group_c = np.concatenate([np.random.normal(72, 7, 55), [40, 42, 100, 102, 105]])
data = [group_a, group_b, group_c]
bp = ax.boxplot(data, tick_labels=['Group A', 'Group B', 'Group C'],
                patch_artist=True, widths=0.5,
                medianprops=dict(color='black', linewidth=2),
                flierprops=dict(marker='o', markersize=5, markerfacecolor='#C44E52'))
box_colors = ['#4C72B0', '#55A868', '#CCB974']
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
ax.set_title('Box Plot: Score Comparison', fontsize=13, fontweight='bold', pad=10)
ax.set_ylabel('Score', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout(pad=2.0)
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Chart saved to {output_path}")

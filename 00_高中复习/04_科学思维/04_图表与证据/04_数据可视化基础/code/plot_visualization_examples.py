# 文件：code/plot_visualization_examples.py
# 用途：生成数据可视化基础课程的示例图表（柱状图、折线图、散点图、好图vs差图对比）
# 环境要求：Python 3.10+, matplotlib>=3.7, numpy>=1.24

import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

# ============================================================
# Figure 1: Bar Chart — Model Accuracy Comparison
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')

models = ['Logistic\nRegression', 'SVM', 'Random\nForest', 'ResNet-18', 'BERT']
accuracy = [72.3, 78.1, 83.5, 91.2, 94.7]
colors = ['#64b5f6', '#64b5f6', '#64b5f6', '#ef5350', '#ef5350']

bars = ax.bar(models, accuracy, color=colors, width=0.6, edgecolor='white')
for bar, acc in zip(bars, accuracy):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f'{acc}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylim(0, 105)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('Model Accuracy Comparison on CIFAR-10', fontsize=14, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

legend_elements = [Patch(facecolor='#64b5f6', label='Traditional ML'),
                   Patch(facecolor='#ef5350', label='Deep Learning')]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.tight_layout()
save_path = os.path.join(assets_dir, 'model_comparison.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

# ============================================================
# Figure 2: Line Chart — Training Loss Curve
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')

epochs = np.arange(1, 51)
np.random.seed(42)
train_loss = 2.5 * np.exp(-0.08 * epochs) + 0.1 + np.random.normal(0, 0.03, 50)
val_loss = 2.5 * np.exp(-0.06 * epochs) + 0.3 + np.random.normal(0, 0.05, 50)
val_loss[35:] += np.linspace(0, 0.4, 15)

ax.plot(epochs, train_loss, color='#1976d2', linewidth=2, label='Training Loss')
ax.plot(epochs, val_loss, color='#e53935', linewidth=2, label='Validation Loss',
        linestyle='--')

ax.axvspan(35, 50, alpha=0.1, color='red')
ax.annotate('Overfitting\nzone', xy=(42, val_loss[41]), fontsize=10,
            color='#c62828', ha='center',
            arrowprops=dict(arrowstyle='->', color='#c62828'),
            xytext=(42, val_loss[41] + 0.4))

ax.set_xlabel('Epoch', fontsize=12)
ax.set_ylabel('Loss', fontsize=12)
ax.set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
save_path = os.path.join(assets_dir, 'training_loss.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

# ============================================================
# Figure 3: Scatter Plot — Study Hours vs Score
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6), facecolor='white')

np.random.seed(123)
study_hours = np.random.uniform(1, 10, 80)
scores = 50 + 4 * study_hours + np.random.normal(0, 5, 80)
scores = np.clip(scores, 0, 100)

ax.scatter(study_hours, scores, color='#42a5f5', alpha=0.6, edgecolors='white', s=60)

z = np.polyfit(study_hours, scores, 1)
p = np.poly1d(z)
x_line = np.linspace(1, 10, 100)
ax.plot(x_line, p(x_line), color='#e53935', linewidth=2, linestyle='--',
        label=f'Trend: y = {z[0]:.1f}x + {z[1]:.1f}')

ax.set_xlabel('Study Hours per Day', fontsize=12)
ax.set_ylabel('Test Score', fontsize=12)
ax.set_title('Study Hours vs Test Score (Simulated)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
save_path = os.path.join(assets_dir, 'scatter_study.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

# ============================================================
# Figure 4: Bad Chart vs Good Chart Comparison
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='white')

categories = ['Model A', 'Model B', 'Model C', 'Model D']
values = [88, 92, 85, 90]

# --- Bad chart ---
ax = axes[0]
bars = ax.bar(categories, values,
              color=['red', 'green', 'blue', 'yellow'],
              edgecolor='grey', linewidth=1.5)
ax.set_ylim(80, 95)
ax.set_facecolor('#e8e8e8')
ax.set_title('Bad Chart', fontsize=13, fontweight='bold', color='#c62828')

# Add "X" marks for problems
problems = [
    (0.05, 0.92, 'Y-axis starts at 80'),
    (0.05, 0.82, 'No axis labels'),
    (0.05, 0.72, 'Random colors'),
    (0.05, 0.62, 'Grey background'),
]
for x, y, text in problems:
    ax.text(x, y, f'  \u2718 {text}', transform=ax.transAxes, fontsize=9,
            color='#c62828', fontweight='bold')

# --- Good chart ---
ax = axes[1]
bars = ax.bar(categories, values, color='#42a5f5', width=0.6, edgecolor='white')
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f'{val}%', ha='center', fontsize=11, fontweight='bold')

ax.set_ylim(0, 105)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('Good Chart', fontsize=13, fontweight='bold', color='#2e7d32')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

checks = [
    (0.55, 0.92, 'Y-axis from 0'),
    (0.55, 0.82, 'Clear labels'),
    (0.55, 0.72, 'Consistent color'),
    (0.55, 0.62, 'White background'),
]
for x, y, text in checks:
    ax.text(x, y, f'  \u2714 {text}', transform=ax.transAxes, fontsize=9,
            color='#2e7d32', fontweight='bold')

plt.tight_layout(pad=2.0)
save_path = os.path.join(assets_dir, 'bad_vs_good_chart.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

# ============================================================
# Figure 5: Chart Type Selection Guide (visual)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(15, 10), facecolor='white')

# (a) Bar Chart
ax = axes[0, 0]
cats = ['A', 'B', 'C', 'D', 'E']
vals = [23, 45, 12, 38, 30]
ax.bar(cats, vals, color='#42a5f5', edgecolor='white')
ax.set_title('Bar Chart\nCompare categories', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# (b) Line Chart
ax = axes[0, 1]
x = np.arange(1, 11)
y = [3, 5, 4, 7, 6, 8, 9, 8, 10, 11]
ax.plot(x, y, color='#ff9800', linewidth=2.5, marker='o', markersize=5,
        markerfacecolor='white', markeredgecolor='#ff9800', markeredgewidth=2)
ax.set_title('Line Chart\nShow trends over time', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# (c) Pie Chart
ax = axes[0, 2]
sizes = [40, 30, 20, 10]
labels = ['40%', '30%', '20%', '10%']
colors_pie = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350']
ax.pie(sizes, labels=labels, colors=colors_pie, startangle=90,
       textprops={'fontsize': 10, 'fontweight': 'bold'})
ax.set_title('Pie Chart\nShow proportions', fontsize=11, fontweight='bold')

# (d) Scatter Plot
ax = axes[1, 0]
np.random.seed(7)
sx = np.random.normal(5, 1.5, 40)
sy = 0.8 * sx + np.random.normal(0, 1, 40)
ax.scatter(sx, sy, color='#ab47bc', alpha=0.6, edgecolors='white', s=50)
ax.set_title('Scatter Plot\nExplore relationships', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# (e) Histogram
ax = axes[1, 1]
np.random.seed(42)
data = np.random.normal(70, 10, 200)
ax.hist(data, bins=20, color='#26a69a', edgecolor='white', alpha=0.8)
ax.set_title('Histogram\nShow distribution', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# (f) Box Plot
ax = axes[1, 2]
np.random.seed(42)
data_box = [np.random.normal(m, 5, 30) for m in [60, 70, 75, 68]]
bp = ax.boxplot(data_box, tick_labels=['G1', 'G2', 'G3', 'G4'],
                patch_artist=True)
box_colors = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350']
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title('Box Plot\nCompare distributions', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout(pad=2.0)
save_path = os.path.join(assets_dir, 'chart_type_guide.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

print("\n🎉 所有图表已生成！")

# 文件：code/plot_chart_types.py
# 用途：生成四种基本图表类型的示例图（柱状图、折线图、饼图、散点图）
# 环境要求：Python 3.10+, matplotlib>=3.7, numpy>=1.24

import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='white')

# --- (a) Bar Chart ---
ax = axes[0, 0]
cities = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu']
temps = [12.3, 16.1, 22.4, 23.0, 16.5]
colors_bar = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350', '#ab47bc']
bars = ax.bar(cities, temps, color=colors_bar, width=0.6, edgecolor='white')
for bar, t in zip(bars, temps):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f'{t}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_ylabel('Temperature ($\\degree$C)', fontsize=11)
ax.set_title('(a) Bar Chart\nAverage Temperature by City', fontsize=12, fontweight='bold')
ax.set_ylim(0, 28)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# --- (b) Line Chart ---
ax = axes[0, 1]
months = np.arange(1, 13)
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sales = [45, 52, 48, 61, 55, 67, 72, 68, 74, 80, 85, 92]
ax.plot(months, sales, color='#1976d2', linewidth=2.5, marker='o', markersize=5,
        markerfacecolor='white', markeredgecolor='#1976d2', markeredgewidth=2)
ax.fill_between(months, sales, alpha=0.1, color='#1976d2')
ax.set_xticks(months)
ax.set_xticklabels(month_labels, fontsize=8)
ax.set_ylabel('Sales (units)', fontsize=11)
ax.set_title('(b) Line Chart\nMonthly Sales Trend', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# --- (c) Pie Chart ---
ax = axes[1, 0]
labels = ['Type A\n35%', 'Type B\n28%', 'Type C\n22%', 'Type O\n15%']
sizes = [35, 28, 22, 15]
colors_pie = ['#42a5f5', '#66bb6a', '#ffa726', '#ef5350']
explode = (0.03, 0.03, 0.03, 0.03)
wedges, texts = ax.pie(sizes, labels=labels, colors=colors_pie,
                       explode=explode, startangle=90,
                       textprops={'fontsize': 10})
ax.set_title('(c) Pie Chart\nBlood Type Distribution', fontsize=12, fontweight='bold')

# --- (d) Scatter Plot ---
ax = axes[1, 1]
np.random.seed(42)
heights = np.random.normal(170, 8, 60)
weights = 0.6 * heights - 32 + np.random.normal(0, 5, 60)
ax.scatter(heights, weights, color='#ab47bc', alpha=0.6, edgecolors='white', s=50)
z = np.polyfit(heights, weights, 1)
p = np.poly1d(z)
x_line = np.linspace(heights.min(), heights.max(), 100)
ax.plot(x_line, p(x_line), color='#e53935', linewidth=2, linestyle='--',
        label=f'Trend: y={z[0]:.1f}x+{z[1]:.0f}')
ax.set_xlabel('Height (cm)', fontsize=11)
ax.set_ylabel('Weight (kg)', fontsize=11)
ax.set_title('(d) Scatter Plot\nHeight vs Weight', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout(pad=2.0)
save_path = os.path.join(assets_dir, 'four_chart_types.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

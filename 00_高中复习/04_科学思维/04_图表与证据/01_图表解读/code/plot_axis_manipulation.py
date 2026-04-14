# 文件：code/plot_axis_manipulation.py
# 用途：生成截断坐标轴对比图，演示同一数据如何因坐标轴设置不同而产生不同视觉印象
# 环境要求：Python 3.10+, matplotlib>=3.7

import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

companies = ['Company A', 'Company B']
sales = [1020, 980]

fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')

# --- Left: Honest chart (y starts at 0) ---
ax = axes[0]
bars = ax.bar(companies, sales, color=['#42a5f5', '#66bb6a'], width=0.5,
              edgecolor='white')
for bar, val in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
            f'{val}', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylim(0, 1200)
ax.set_ylabel('Sales (10k CNY)', fontsize=12)
ax.set_title('Honest Chart\n(Y-axis starts at 0)', fontsize=13, fontweight='bold',
             color='#2e7d32')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

diff_pct = abs(sales[0] - sales[1]) / sales[1] * 100
ax.text(0.5, 0.02, f'Actual difference: {abs(sales[0]-sales[1])} ({diff_pct:.1f}%)',
        transform=ax.transAxes, ha='center', fontsize=10, style='italic',
        color='#555555')

# --- Right: Misleading chart (y starts at 950) ---
ax = axes[1]
bars = ax.bar(companies, sales, color=['#42a5f5', '#66bb6a'], width=0.5,
              edgecolor='white')
for bar, val in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f'{val}', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylim(950, 1050)
ax.set_ylabel('Sales (10k CNY)', fontsize=12)
ax.set_title('Misleading Chart\n(Y-axis starts at 950)', fontsize=13, fontweight='bold',
             color='#c62828')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# Warning annotation
ax.annotate('Same data,\nvery different\nvisual impression!',
            xy=(0.5, 990), fontsize=10, color='#c62828', fontweight='bold',
            ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffebee', edgecolor='#c62828'))

plt.tight_layout(pad=2.0)
save_path = os.path.join(assets_dir, 'axis_manipulation_comparison.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

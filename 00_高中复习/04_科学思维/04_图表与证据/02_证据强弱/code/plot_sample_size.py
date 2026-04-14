# 文件：code/plot_sample_size.py
# 用途：可视化样本量对结论可靠性的影响（大数定律演示）
# 环境要求：Python 3.10+, matplotlib>=3.7, numpy>=1.24

import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

np.random.seed(42)

# ============================================================
# Figure 1: Sample size effect — spread of results
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 5), facecolor='white')

sample_sizes = [10, 100, 1000]
titles = ['n = 10\n(Very Small)', 'n = 100\n(Medium)', 'n = 1,000\n(Large)']
n_experiments = 50

for idx, (n, title) in enumerate(zip(sample_sizes, titles)):
    ax = axes[idx]
    results = [np.random.binomial(n, 0.5) / n for _ in range(n_experiments)]

    ax.hist(results, bins=15, color='#42a5f5', edgecolor='white', alpha=0.8,
            density=True)
    ax.axvline(x=0.5, color='#e53935', linewidth=2, linestyle='--', label='True p=0.50')

    mean_r = np.mean(results)
    std_r = np.std(results)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Heads Ratio', fontsize=10)
    if idx == 0:
        ax.set_ylabel('Density', fontsize=10)
    ax.set_xlim(0.1, 0.9)
    ax.legend(fontsize=9, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.3)

    ax.text(0.5, 0.95, f'Std = {std_r:.3f}',
            transform=ax.transAxes, ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4', edgecolor='#f9a825'))

fig.suptitle('Law of Large Numbers: More Samples → More Stable Results',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
save_path = os.path.join(assets_dir, 'sample_size_effect.png')
plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path}")
plt.close()

# ============================================================
# Figure 2: Convergence to true value with increasing n
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')

max_n = 2000
flips = np.random.binomial(1, 0.5, max_n)
cumulative_ratio = np.cumsum(flips) / np.arange(1, max_n + 1)

ax.plot(range(1, max_n + 1), cumulative_ratio, color='#1976d2', linewidth=1.5,
        alpha=0.8)
ax.axhline(y=0.5, color='#e53935', linewidth=2, linestyle='--', label='True p = 0.50')
ax.fill_between(range(1, max_n + 1), 0.45, 0.55, alpha=0.1, color='#4caf50',
                label='$\\pm$0.05 range')

ax.set_xlabel('Number of Flips', fontsize=12)
ax.set_ylabel('Cumulative Heads Ratio', fontsize=12)
ax.set_title('Coin Flip: Cumulative Ratio Converges to True Probability',
             fontsize=13, fontweight='bold')
ax.set_ylim(0.2, 0.8)
ax.set_xlim(1, max_n)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

# Annotate early volatility
ax.annotate('High volatility\n(small n)', xy=(20, cumulative_ratio[19]),
            xytext=(150, 0.72), fontsize=10, color='#c62828',
            arrowprops=dict(arrowstyle='->', color='#c62828'))
ax.annotate('Converged\n(large n)', xy=(1800, cumulative_ratio[1799]),
            xytext=(1500, 0.35), fontsize=10, color='#2e7d32',
            arrowprops=dict(arrowstyle='->', color='#2e7d32'))

plt.tight_layout()
save_path2 = os.path.join(assets_dir, 'convergence_to_true_value.png')
plt.savefig(save_path2, dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 已保存：{save_path2}")
plt.close()

# 文件：code/plot_conditions.py
# 用途：用集合包含关系图解充分条件、必要条件、充要条件和既非充分也非必要条件
# 环境要求：Python 3.10+, matplotlib

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------- 输出路径 ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'conditions.png')

# ---------- 全局样式 ----------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(2, 2, figsize=(10, 9))

# Helper: draw circle
def draw_circle(ax, center, radius, label, color, fontsize=16):
    circle = plt.Circle(center, radius, facecolor=color, edgecolor='black',
                        linewidth=2, alpha=0.3, zorder=2)
    ax.add_patch(circle)
    ax.text(center[0], center[1], label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', zorder=3)

def setup_ax(ax, title, subtitle):
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.text(0, -2.2, subtitle, ha='center', va='center', fontsize=11,
            style='italic', color='#555555')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

# ========== Top-left: P ⊂ Q (P sufficient for Q) ==========
ax = axes[0, 0]
setup_ax(ax, '$P \\subset Q$', '$P$ is sufficient for $Q$')
draw_circle(ax, (0, 0), 1.8, '', '#5DADE2', fontsize=14)
ax.text(1.1, 1.2, '$Q$', fontsize=18, fontweight='bold', color='#2471A3')
draw_circle(ax, (0, 0), 0.8, '$P$', '#E74C3C', fontsize=16)
ax.annotate('$P \\Rightarrow Q$ ✓', xy=(0.3, -1.5), fontsize=12,
            color='#27AE60', fontweight='bold', ha='center')

# ========== Top-right: P ⊃ Q (P necessary for Q) ==========
ax = axes[0, 1]
setup_ax(ax, '$P \\supset Q$', '$P$ is necessary for $Q$')
draw_circle(ax, (0, 0), 1.8, '', '#E74C3C', fontsize=14)
ax.text(1.1, 1.2, '$P$', fontsize=18, fontweight='bold', color='#C0392B')
draw_circle(ax, (0, 0), 0.8, '$Q$', '#5DADE2', fontsize=16)
ax.annotate('$Q \\Rightarrow P$ ✓', xy=(0.3, -1.5), fontsize=12,
            color='#27AE60', fontweight='bold', ha='center')

# ========== Bottom-left: P = Q (P iff Q) ==========
ax = axes[1, 0]
setup_ax(ax, '$P = Q$', '$P$ iff $Q$ (necessary & sufficient)')
circle_p = plt.Circle((0, 0), 1.3, facecolor='#E74C3C', edgecolor='black',
                       linewidth=2, alpha=0.25, zorder=2)
circle_q = plt.Circle((0, 0), 1.3, facecolor='#5DADE2', edgecolor='black',
                       linewidth=2, alpha=0.25, zorder=2)
ax.add_patch(circle_p)
ax.add_patch(circle_q)
ax.text(0, 0, '$P = Q$', ha='center', va='center', fontsize=18,
        fontweight='bold', zorder=3)
ax.annotate('$P \\Leftrightarrow Q$ ✓', xy=(0.3, -1.5), fontsize=12,
            color='#27AE60', fontweight='bold', ha='center')

# ========== Bottom-right: partial overlap (neither) ==========
ax = axes[1, 1]
setup_ax(ax, '$P \\cap Q \\neq \\emptyset,\\; P \\not\\subset Q,\\; Q \\not\\subset P$',
         'Neither sufficient nor necessary')
draw_circle(ax, (-0.6, 0), 1.2, '$P$', '#E74C3C', fontsize=16)
draw_circle(ax, (0.6, 0), 1.2, '$Q$', '#5DADE2', fontsize=16)
ax.annotate('$P \\Rightarrow Q$ ✗\n$Q \\Rightarrow P$ ✗',
            xy=(0.3, -1.5), fontsize=12,
            color='#E74C3C', fontweight='bold', ha='center')

plt.tight_layout(h_pad=2.0)
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {output_path}')

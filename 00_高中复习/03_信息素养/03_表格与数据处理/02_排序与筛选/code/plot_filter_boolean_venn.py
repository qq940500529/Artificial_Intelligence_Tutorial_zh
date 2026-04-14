# 文件：code/plot_filter_boolean_venn.py
# 用途：用韦恩图（几何图形）展示数据筛选中 AND 和 OR 的含义
# 环境要求：Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, '..', 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)


def draw_venn(ax, highlight='none', title='',
              label_left='A', label_right='B',
              example_text=''):
    """Draw a Venn diagram and highlight a region.

    highlight: 'and' / 'or'
    """
    theta = np.linspace(0, 2 * np.pi, 200)
    r = 1.0
    cx_left, cx_right = -0.5, 0.5
    cy = 0.0

    # Universal set rectangle
    rect = FancyBboxPatch(
        (-2.2, -1.6), 4.4, 3.2,
        boxstyle="round,pad=0.05",
        linewidth=1.5, edgecolor='#555555',
        facecolor='#f8f8f8', zorder=0,
    )
    ax.add_patch(rect)
    ax.text(1.85, 1.25, 'All rows', fontsize=9,
            color='#555555', style='italic')

    # Circle coordinates
    x_left = cx_left + r * np.cos(theta)
    y_left = cy + r * np.sin(theta)
    x_right = cx_right + r * np.cos(theta)
    y_right = cy + r * np.sin(theta)

    # Grid for filling
    x_grid = np.linspace(-2.2, 2.2, 500)
    y_grid = np.linspace(-1.6, 1.6, 500)
    X, Y = np.meshgrid(x_grid, y_grid)
    in_left = (X - cx_left) ** 2 + (Y - cy) ** 2 <= r ** 2
    in_right = (X - cx_right) ** 2 + (Y - cy) ** 2 <= r ** 2

    if highlight == 'and':
        mask = in_left & in_right
        color = '#FF6B6B'
    elif highlight == 'or':
        mask = in_left | in_right
        color = '#4ECDC4'
    else:
        mask = np.zeros_like(X, dtype=bool)
        color = '#CCCCCC'

    if mask.any():
        ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5],
                    colors=[color], alpha=0.5, zorder=1)

    ax.plot(x_left, y_left, color='#2C3E50', linewidth=2, zorder=3)
    ax.plot(x_right, y_right, color='#2C3E50', linewidth=2, zorder=3)

    ax.text(cx_left - 0.35, cy, label_left, fontsize=12,
            fontweight='bold', ha='center', va='center',
            color='#2C3E50', zorder=4)
    ax.text(cx_right + 0.35, cy, label_right, fontsize=12,
            fontweight='bold', ha='center', va='center',
            color='#2C3E50', zorder=4)

    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    if example_text:
        ax.text(0, -1.45, example_text, fontsize=9, ha='center',
                va='center', color='#666666', style='italic', zorder=5)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.8, 1.8)
    ax.set_aspect('equal')
    ax.axis('off')


def main():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    draw_venn(axes[0], highlight='and',
              title='AND: Intersection\n(both conditions met)',
              label_left='Class=1', label_right='Math>=85',
              example_text='Only rows satisfying BOTH conditions')
    draw_venn(axes[1], highlight='or',
              title='OR: Union\n(either condition met)',
              label_left='Math>=95', label_right='Eng>=90',
              example_text='Rows satisfying ANY condition')

    fig.suptitle('Data Filtering — AND vs OR (Venn Diagram)',
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()

    save_path = os.path.join(ASSETS_DIR, 'filter_boolean_venn.png')
    fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved: {save_path}')


if __name__ == '__main__':
    main()

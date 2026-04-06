# 文件：code/plot_number_lines.py
# 数轴图生成脚本
# 环境要求：Python 3.10+, matplotlib, numpy
# 用途：为"不等式与绝对值"课程生成数轴示意图

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置字体，避免中文字体缺失问题
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 输出目录：基于脚本位置定位 assets/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, '..', 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)


def plot_number_line_geq(value, filename, title=""):
    """
    绘制 x >= value 的数轴图（实心点 + 向右箭头）
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 1.5))

    # 数轴范围
    x_min, x_max = value - 4, value + 5
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.5, 0.8)

    # 画数轴
    ax.annotate('', xy=(x_max, 0), xytext=(x_min, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.plot([x_min, x_max], [0, 0], color='black', lw=1.5)

    # 画刻度
    for i in range(int(x_min) + 1, int(x_max)):
        ax.plot([i, i], [-0.08, 0.08], color='gray', lw=0.8)
        ax.text(i, -0.25, str(i), ha='center', va='top', fontsize=10, color='gray')

    # 高亮解集区域（向右的射线）
    ax.fill_between([value, x_max], -0.15, 0.15, color='#4CAF50', alpha=0.3)

    # 画实心点（包含端点）
    ax.plot(value, 0, 'o', color='#4CAF50', markersize=12, zorder=5)

    # 标注
    ax.text(value, 0.45, f'x = {value}', ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='#2E7D32')
    ax.text(value + 2.5, 0.45, r'$x \geq ' + str(value) + r'$',
            ha='center', va='bottom', fontsize=13, color='#1B5E20',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50'))

    if title:
        ax.set_title(title, fontsize=12, pad=10)

    ax.axis('off')
    plt.tight_layout()
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")


def plot_number_line_abs_lt(center, radius, filename, title=""):
    """
    绘制 |x - center| < radius 的数轴图（空心点 + 中间区域高亮）
    解集: (center - radius, center + radius)
    """
    left = center - radius
    right = center + radius

    fig, ax = plt.subplots(1, 1, figsize=(8, 1.8))

    x_min = left - 3
    x_max = right + 3
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.6, 1.0)

    # 画数轴
    ax.annotate('', xy=(x_max, 0), xytext=(x_min, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.plot([x_min, x_max], [0, 0], color='black', lw=1.5)

    # 画刻度
    for i in range(int(x_min) + 1, int(x_max)):
        ax.plot([i, i], [-0.08, 0.08], color='gray', lw=0.8)
        ax.text(i, -0.3, str(i), ha='center', va='top', fontsize=10, color='gray')

    # 高亮解集区域（中间区域）
    ax.fill_between([left, right], -0.15, 0.15, color='#FF9800', alpha=0.3)

    # 画空心点（不包含端点）
    ax.plot(left, 0, 'o', color='#FF9800', markersize=12, zorder=5,
            markerfacecolor='white', markeredgewidth=2.5)
    ax.plot(right, 0, 'o', color='#FF9800', markersize=12, zorder=5,
            markerfacecolor='white', markeredgewidth=2.5)

    # 标注中心点
    ax.plot(center, 0, 'o', color='#4CAF50', markersize=8, zorder=5)
    ax.text(center, -0.3, str(center), ha='center', va='top',
            fontsize=10, fontweight='bold', color='#2E7D32')

    # 标注端点
    ax.text(left, 0.45, str(left), ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='#E65100')
    ax.text(right, 0.45, str(right), ha='center', va='bottom',
            fontsize=11, fontweight='bold', color='#E65100')

    # 标注距离
    ax.annotate('', xy=(left, 0.75), xytext=(center, 0.75),
                arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=1.5))
    ax.text((left + center) / 2, 0.85, str(radius), ha='center', va='bottom',
            fontsize=10, color='#1565C0')
    ax.annotate('', xy=(center, 0.75), xytext=(right, 0.75),
                arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=1.5))
    ax.text((center + right) / 2, 0.85, str(radius), ha='center', va='bottom',
            fontsize=10, color='#1565C0')

    # 解集标注
    solution_text = f'$|x - {center}| < {radius}$' + r'$\;\Rightarrow\;$' + f'${left} < x < {right}$'
    ax.text((left + right) / 2, -0.55, solution_text,
            ha='center', va='top', fontsize=12, color='#BF360C',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', edgecolor='#FF9800'))

    if title:
        ax.set_title(title, fontsize=12, pad=10)

    ax.axis('off')
    plt.tight_layout()
    filepath = os.path.join(ASSETS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {filepath}")


if __name__ == "__main__":
    # 图 1：x >= 3 的数轴表示
    plot_number_line_geq(
        value=3,
        filename="number_line_geq_3.png",
        title=r"Solution: $x \geq 3$"
    )

    # 图 2：|x - 3| < 2 的数轴表示（解集 1 < x < 5）
    plot_number_line_abs_lt(
        center=3,
        radius=2,
        filename="number_line_abs_lt.png",
        title=r"Solution: $|x - 3| < 2$"
    )

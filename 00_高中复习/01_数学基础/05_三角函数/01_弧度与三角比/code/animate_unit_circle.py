# 文件：code/animate_unit_circle.py
# 用途：生成单位圆动态 GIF，展示角度变化时 sin/cos 值的对应变化
# 环境要求：Python 3.10+, matplotlib, numpy, Pillow

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os
from PIL import Image
import io

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)


def draw_frame(theta_deg):
    """绘制单位圆的一帧，角度为 theta_deg 度"""
    fig, (ax_circle, ax_wave) = plt.subplots(1, 2, figsize=(12, 5.5),
                                              gridspec_kw={'width_ratios': [1, 1.2]})

    theta = np.radians(theta_deg)
    x = np.cos(theta)
    y = np.sin(theta)

    # ===== 左图：单位圆 =====
    # 画单位圆
    circle_t = np.linspace(0, 2 * np.pi, 200)
    ax_circle.plot(np.cos(circle_t), np.sin(circle_t), 'b-', linewidth=1.5, alpha=0.4)

    # 坐标轴
    ax_circle.axhline(y=0, color='k', linewidth=0.8)
    ax_circle.axvline(x=0, color='k', linewidth=0.8)

    # 扫过的弧（从 0 到当前角度）
    arc_t = np.linspace(0, theta, 100)
    ax_circle.plot(np.cos(arc_t), np.sin(arc_t), 'b-', linewidth=3, alpha=0.6)

    # 半径线
    ax_circle.plot([0, x], [0, y], 'r-', linewidth=2.5, zorder=5)
    ax_circle.plot(x, y, 'ro', markersize=8, zorder=6)

    # cos θ 投影（水平）
    ax_circle.plot([0, x], [0, 0], color='#9C27B0', linewidth=4, alpha=0.7, zorder=4)
    ax_circle.plot([x, x], [0, y], color='#4CAF50', linewidth=2.5, linestyle='--',
                   alpha=0.8, zorder=4)

    # 标注
    ax_circle.text(x / 2, -0.12, r'$\cos\theta$', fontsize=12, ha='center',
                   color='#9C27B0', fontweight='bold')
    if abs(y) > 0.15:
        ax_circle.text(x + 0.08, y / 2, r'$\sin\theta$', fontsize=12, ha='left',
                       color='#4CAF50', fontweight='bold')

    # 角度弧
    if theta_deg > 5:
        arc_angle = np.linspace(0, theta, 50)
        r_arc = 0.2
        ax_circle.plot(r_arc * np.cos(arc_angle), r_arc * np.sin(arc_angle),
                       'orange', linewidth=1.5)
        mid_angle = theta / 2
        ax_circle.text(0.3 * np.cos(mid_angle), 0.3 * np.sin(mid_angle),
                       r'$\theta$', fontsize=11, color='orange', ha='center', va='center')

    # 坐标标注
    ax_circle.annotate(f'$P$({x:.2f}, {y:.2f})',
                       xy=(x, y), xytext=(x + 0.15, y + 0.15),
                       fontsize=10, color='red',
                       arrowprops=dict(arrowstyle='->', color='red', lw=1))

    # 当前角度显示
    ax_circle.text(0, 1.35, f'$\\theta = {theta_deg:.0f}°$',
                   fontsize=14, ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                             edgecolor='orange'))

    ax_circle.set_xlim(-1.4, 1.6)
    ax_circle.set_ylim(-1.4, 1.5)
    ax_circle.set_aspect('equal')
    ax_circle.set_title('Unit Circle', fontsize=13, pad=5)
    ax_circle.grid(True, alpha=0.2)
    ax_circle.spines['top'].set_visible(False)
    ax_circle.spines['right'].set_visible(False)

    # ===== 右图：sin 和 cos 随角度变化的曲线 =====
    all_t = np.linspace(0, 360, 500)
    ax_wave.plot(all_t, np.sin(np.radians(all_t)), 'g-', linewidth=1.5, alpha=0.3,
                 label=r'$\sin\theta$')
    ax_wave.plot(all_t, np.cos(np.radians(all_t)), color='#9C27B0', linewidth=1.5,
                 alpha=0.3, label=r'$\cos\theta$')

    # 已扫过部分（高亮）
    past_t = np.linspace(0, theta_deg, max(2, int(theta_deg)))
    if len(past_t) >= 2:
        ax_wave.plot(past_t, np.sin(np.radians(past_t)), 'g-', linewidth=3, alpha=0.8)
        ax_wave.plot(past_t, np.cos(np.radians(past_t)), color='#9C27B0',
                     linewidth=3, alpha=0.8)

    # 当前点
    ax_wave.plot(theta_deg, np.sin(theta), 'go', markersize=10, zorder=5)
    ax_wave.plot(theta_deg, np.cos(theta), 'o', color='#9C27B0', markersize=10, zorder=5)

    # 水平连接线（连接单位圆和波形图）
    ax_wave.axhline(y=y, color='g', linewidth=0.8, linestyle=':', alpha=0.5)
    ax_wave.axhline(y=x, color='#9C27B0', linewidth=0.8, linestyle=':', alpha=0.5)

    # 数值标注
    ax_wave.text(theta_deg + 8, y + 0.05, f'sin = {y:.2f}', fontsize=10,
                 color='g', fontweight='bold')
    ax_wave.text(theta_deg + 8, x - 0.12, f'cos = {x:.2f}', fontsize=10,
                 color='#9C27B0', fontweight='bold')

    ax_wave.set_xlim(-10, 380)
    ax_wave.set_ylim(-1.4, 1.4)
    ax_wave.set_xlabel('Angle (degrees)', fontsize=11)
    ax_wave.set_ylabel('Value', fontsize=11)
    ax_wave.set_title(r'$\sin\theta$ and $\cos\theta$ vs Angle', fontsize=13, pad=5)
    ax_wave.legend(loc='upper right', fontsize=11)
    ax_wave.grid(True, alpha=0.3)
    ax_wave.set_xticks([0, 90, 180, 270, 360])
    ax_wave.spines['top'].set_visible(False)
    ax_wave.spines['right'].set_visible(False)

    plt.tight_layout()

    # 转为 PIL Image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf).copy()
    buf.close()
    plt.close(fig)
    return img


# 生成帧
print("Generating unit circle animation frames...")
frames = []
# 0° → 360°, 每 5° 一帧
for deg in range(0, 365, 5):
    frames.append(draw_frame(deg))
    if deg % 45 == 0:
        print(f"  Frame {deg}°...")

# 保存 GIF
output_path = os.path.join(assets_dir, 'unit_circle_anim.gif')
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=80,  # 每帧 80ms
    loop=0  # 无限循环
)

print(f"Generated: unit_circle_anim.gif ({len(frames)} frames)")

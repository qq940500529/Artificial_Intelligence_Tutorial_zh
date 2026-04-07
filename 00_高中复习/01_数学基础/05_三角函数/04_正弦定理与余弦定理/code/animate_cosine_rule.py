# 文件：code/animate_cosine_rule.py
# 用途：生成余弦定理动态 GIF，展示夹角 C 变化时对边 c 的长度变化
#       直觉理解：当 C=90° 退化为勾股定理，C<90° 对边缩短，C>90° 对边变长
# 环境要求：Python 3.10+, matplotlib, numpy, Pillow

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import io

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

# 固定两边 a=4, b=3
a_len = 4.0
b_len = 3.0


def draw_frame(C_deg):
    """绘制余弦定理的一帧：固定 a, b，变化角 C"""
    fig, (ax_tri, ax_plot) = plt.subplots(1, 2, figsize=(13, 5.5),
                                           gridspec_kw={'width_ratios': [1, 1]})

    C_rad = np.radians(C_deg)

    # 计算三角形顶点
    # C 在原点，a 边沿 x 轴正方向，b 边与 a 夹角 C
    C_pt = np.array([0, 0])
    B_pt = np.array([a_len, 0])  # B 在 a 方向
    A_pt = np.array([b_len * np.cos(C_rad), b_len * np.sin(C_rad)])  # A 在 b 方向

    # 计算对边 c
    c_val = np.sqrt(a_len**2 + b_len**2 - 2 * a_len * b_len * np.cos(C_rad))
    # 勾股定理参考值
    c_pyth = np.sqrt(a_len**2 + b_len**2)
    # 修正项
    correction = -2 * a_len * b_len * np.cos(C_rad)

    # ===== 左图：三角形 =====
    # 画三角形
    triangle = plt.Polygon([A_pt, B_pt, C_pt], fill=True, facecolor='#e3f2fd',
                           edgecolor='blue', linewidth=2, alpha=0.5)
    ax_tri.add_patch(triangle)

    # 边的颜色：a 和 b 固定（蓝色），c 变化（红色）
    ax_tri.plot([C_pt[0], B_pt[0]], [C_pt[1], B_pt[1]], 'b-', linewidth=2.5)
    ax_tri.plot([C_pt[0], A_pt[0]], [C_pt[1], A_pt[1]], 'b-', linewidth=2.5)
    ax_tri.plot([A_pt[0], B_pt[0]], [A_pt[1], B_pt[1]], 'r-', linewidth=3)

    # 标注边
    mid_a = (C_pt + B_pt) / 2
    mid_b = (C_pt + A_pt) / 2
    mid_c = (A_pt + B_pt) / 2
    ax_tri.text(mid_a[0], mid_a[1] - 0.35, f'$a = {a_len:.0f}$', fontsize=12,
                ha='center', color='blue', fontweight='bold')
    offset_b = np.array([-0.3, 0.1]) if C_deg < 150 else np.array([0.1, 0.2])
    ax_tri.text(mid_b[0] + offset_b[0], mid_b[1] + offset_b[1],
                f'$b = {b_len:.0f}$', fontsize=12, color='blue', fontweight='bold')
    ax_tri.text(mid_c[0] + 0.1, mid_c[1] + 0.15, f'$c = {c_val:.2f}$', fontsize=13,
                color='red', fontweight='bold')

    # 标注角 C
    arc_t = np.linspace(0, C_rad, 50)
    arc_r = 0.6
    ax_tri.plot(C_pt[0] + arc_r * np.cos(arc_t), C_pt[1] + arc_r * np.sin(arc_t),
                'orange', linewidth=2)
    mid_arc = C_rad / 2
    ax_tri.text(C_pt[0] + 0.8 * np.cos(mid_arc), C_pt[1] + 0.8 * np.sin(mid_arc),
                f'$C={C_deg:.0f}°$', fontsize=12, color='orange', fontweight='bold',
                ha='center', va='center')

    # 顶点标注
    ax_tri.text(C_pt[0] - 0.3, C_pt[1] - 0.3, r'$C$', fontsize=14, fontweight='bold')
    ax_tri.text(B_pt[0] + 0.15, B_pt[1] - 0.3, r'$B$', fontsize=14, fontweight='bold')
    ax_tri.text(A_pt[0] - 0.1, A_pt[1] + 0.2, r'$A$', fontsize=14, fontweight='bold')

    # 如果 C=90°，显示直角符号
    if abs(C_deg - 90) < 2:
        sq = 0.25
        # C在原点，a沿x轴，b沿y轴
        ax_tri.plot([sq, sq, 0], [0, sq, sq], 'orange', linewidth=1.5)

    # 公式框
    if C_deg < 88:
        status = r'$C < 90° \Rightarrow c^2 < a^2 + b^2$'
        status_color = '#4CAF50'
    elif C_deg > 92:
        status = r'$C > 90° \Rightarrow c^2 > a^2 + b^2$'
        status_color = '#f44336'
    else:
        status = r'$C = 90° \Rightarrow c^2 = a^2 + b^2$  (Pythagorean!)'
        status_color = '#FF9800'

    formula = r'$c^2 = a^2 + b^2 - 2ab\cos C = %.1f$' % (c_val ** 2)
    ax_tri.text(0.5, -1.2, formula + '\n' + status, fontsize=11, ha='left',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                          edgecolor=status_color, linewidth=2))

    ax_tri.set_xlim(-2, 5.5)
    ax_tri.set_ylim(-2, 4.5)
    ax_tri.set_aspect('equal')
    ax_tri.set_title('Law of Cosines: Triangle', fontsize=13, pad=5)
    ax_tri.grid(True, alpha=0.15)
    ax_tri.axis('off')

    # ===== 右图：c 随 C 变化的曲线 =====
    all_C = np.linspace(10, 170, 300)
    all_c = np.sqrt(a_len**2 + b_len**2 - 2 * a_len * b_len * np.cos(np.radians(all_C)))

    ax_plot.fill_between(all_C, all_c, where=(all_C < 90), alpha=0.15, color='green',
                         label=r'$C < 90°$: acute')
    ax_plot.fill_between(all_C, all_c, where=(all_C > 90), alpha=0.15, color='red',
                         label=r'$C > 90°$: obtuse')

    ax_plot.plot(all_C, all_c, 'b-', linewidth=2, alpha=0.5)

    # 已扫过的部分高亮
    past_C = np.linspace(10, C_deg, max(2, int(C_deg - 9)))
    past_c = np.sqrt(a_len**2 + b_len**2 - 2 * a_len * b_len * np.cos(np.radians(past_C)))
    ax_plot.plot(past_C, past_c, 'b-', linewidth=3)

    # 当前点
    ax_plot.plot(C_deg, c_val, 'ro', markersize=12, zorder=5)
    ax_plot.annotate(f'$c = {c_val:.2f}$', xy=(C_deg, c_val),
                     xytext=(C_deg + 8, c_val + 0.3), fontsize=11, color='red',
                     fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='red'))

    # 勾股定理参考线
    ax_plot.axhline(y=c_pyth, color='orange', linewidth=1.5, linestyle='--', alpha=0.7)
    ax_plot.text(15, c_pyth + 0.1, f'$\\sqrt{{a^2+b^2}} = {c_pyth:.2f}$ (Pythagorean)',
                 fontsize=10, color='orange')

    # C=90° 竖线
    ax_plot.axvline(x=90, color='gray', linewidth=1, linestyle=':', alpha=0.5)
    ax_plot.text(91, 1.2, '$90°$', fontsize=10, color='gray')

    ax_plot.set_xlim(5, 175)
    ax_plot.set_ylim(0.5, 7.5)
    ax_plot.set_xlabel('Angle $C$ (degrees)', fontsize=12)
    ax_plot.set_ylabel('Side $c$', fontsize=12)
    ax_plot.set_title(r'$c$ vs Angle $C$ ($a=4, b=3$)', fontsize=13, pad=5)
    ax_plot.legend(loc='upper left', fontsize=10)
    ax_plot.grid(True, alpha=0.3)
    ax_plot.spines['top'].set_visible(False)
    ax_plot.spines['right'].set_visible(False)

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
print("Generating cosine rule animation frames...")
frames = []
# 角 C 从 20° 到 160°，每 2° 一帧
for deg in range(20, 162, 2):
    frames.append(draw_frame(deg))
    if deg % 20 == 0:
        print(f"  Frame C={deg}°...")

# 保存 GIF
output_path = os.path.join(assets_dir, 'cosine_rule_anim.gif')
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=100,  # 每帧 100ms
    loop=0
)

print(f"Generated: cosine_rule_anim.gif ({len(frames)} frames)")

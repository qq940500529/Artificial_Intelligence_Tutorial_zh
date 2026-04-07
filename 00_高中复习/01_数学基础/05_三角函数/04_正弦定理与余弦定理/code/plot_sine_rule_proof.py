# 文件：code/plot_sine_rule_proof.py
# 用途：绘制正弦定理推导过程的三角形图（从C向AB作高 + 外接圆证明2R）
# 环境要求：Python 3.10+, matplotlib, numpy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)

# ========== 图1：正弦定理推导图（作高法） ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# --- 左图：从C向AB作高 ---
ax = axes[0]

# 三角形顶点
A = np.array([0, 0])
B = np.array([6, 0])
C = np.array([2, 4])

# 画三角形
triangle = plt.Polygon([A, B, C], fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(triangle)

# 从 C 向 AB 作高 h
# AB 在 x 轴上，所以高的垂足 D 就是 (C[0], 0)
D = np.array([C[0], 0])

# 画高 h (虚线)
ax.plot([C[0], D[0]], [C[1], D[1]], 'r--', linewidth=2, zorder=3)

# 直角符号（正确的小正方形标记）
# 标准右角标记：从 CD 方向偏移一点，水平转折，再沿 AB 方向回来
# 即 (D[0], D[1]+sq) → (D[0]+sq, D[1]+sq) → (D[0]+sq, D[1])
# 这是一个不经过 D 点的折线，形成直角标记
sq = 0.25
ax.plot([D[0], D[0] + sq, D[0] + sq],
        [D[1] + sq, D[1] + sq, D[1]], 'r-', linewidth=1.2)

# 标注顶点
ax.text(A[0] - 0.3, A[1] - 0.35, r'$A$', fontsize=16, fontweight='bold', color='blue')
ax.text(B[0] + 0.15, B[1] - 0.35, r'$B$', fontsize=16, fontweight='bold', color='blue')
ax.text(C[0] - 0.1, C[1] + 0.2, r'$C$', fontsize=16, fontweight='bold', color='blue')
ax.text(D[0] + 0.15, D[1] - 0.35, r'$D$', fontsize=14, color='red')

# 标注边
mid_BC = (B + C) / 2
mid_AC = (A + C) / 2
mid_AB = (A + B) / 2

ax.text(mid_BC[0] + 0.25, mid_BC[1] + 0.1, r'$a$', fontsize=16, color='darkgreen', fontweight='bold')
ax.text(mid_AC[0] - 0.45, mid_AC[1] + 0.1, r'$b$', fontsize=16, color='darkgreen', fontweight='bold')
ax.text(mid_AB[0], mid_AB[1] - 0.4, r'$c$', fontsize=16, color='darkgreen', fontweight='bold')

# 标注高 h
ax.text(C[0] + 0.2, C[1] / 2, r'$h$', fontsize=16, color='red', fontweight='bold')

# 标注角 A
angle_A = np.arctan2(C[1] - A[1], C[0] - A[0])
arc_theta_A = np.linspace(0, angle_A, 50)
arc_r_A = 0.7
ax.plot(A[0] + arc_r_A * np.cos(arc_theta_A), A[1] + arc_r_A * np.sin(arc_theta_A),
        'orange', linewidth=1.5)
ax.text(A[0] + 0.8, A[1] + 0.25, r'$A$', fontsize=14, color='orange')

# 标注角 B
angle_B_start = np.pi - np.arctan2(C[1] - B[1], B[0] - C[0])
angle_B_end = np.pi
arc_theta_B = np.linspace(angle_B_start, angle_B_end, 50)
arc_r_B = 0.7
ax.plot(B[0] + arc_r_B * np.cos(arc_theta_B), B[1] + arc_r_B * np.sin(arc_theta_B),
        'purple', linewidth=1.5)
ax.text(B[0] - 0.95, B[1] + 0.3, r'$B$', fontsize=14, color='purple')

# 关键等式标注
eq_text = (r'$h = b \sin A = a \sin B$' + '\n'
           + r'$\Rightarrow \dfrac{a}{\sin A} = \dfrac{b}{\sin B}$')
ax.text(4.0, 3.5, eq_text, fontsize=12,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='orange', alpha=0.9))

ax.set_xlim(-0.8, 7.5)
ax.set_ylim(-0.8, 5)
ax.set_aspect('equal')
ax.set_title('Step 1: Altitude Proof', fontsize=13, pad=10)
ax.axis('off')

# --- 右图：外接圆证明 a/sinA = 2R ---
ax2 = axes[1]

# 外接圆参数：选三角形 A, B, C 并计算外接圆
# 使用预设的三角形在外接圆上
R = 3.0  # 外接圆半径
O = np.array([3, 2.5])  # 圆心

# 三角形三个顶点在圆上
angle_B2 = np.radians(200)
angle_C2 = np.radians(320)
angle_A2 = np.radians(80)

A2 = O + R * np.array([np.cos(angle_A2), np.sin(angle_A2)])
B2 = O + R * np.array([np.cos(angle_B2), np.sin(angle_B2)])
C2 = O + R * np.array([np.cos(angle_C2), np.sin(angle_C2)])

# 画外接圆
circle_theta = np.linspace(0, 2 * np.pi, 200)
ax2.plot(O[0] + R * np.cos(circle_theta), O[1] + R * np.sin(circle_theta),
         'gray', linewidth=1.5, alpha=0.6)

# 画三角形
triangle2 = plt.Polygon([A2, B2, C2], fill=False, edgecolor='blue', linewidth=2)
ax2.add_patch(triangle2)

# 直径 BD'：从 B 穿过圆心 O 到对面的点 B'
angle_B2_opposite = angle_B2 + np.pi
B_prime = O + R * np.array([np.cos(angle_B2_opposite), np.sin(angle_B2_opposite)])

# 画直径
ax2.plot([B2[0], B_prime[0]], [B2[1], B_prime[1]], 'r-', linewidth=1.5, zorder=2)

# 连接 B' 到 C
ax2.plot([B_prime[0], C2[0]], [B_prime[1], C2[1]], 'r--', linewidth=1.5, alpha=0.7)

# 标注圆心和半径
ax2.plot(*O, 'ko', markersize=4, zorder=5)
ax2.text(O[0] + 0.15, O[1] - 0.3, r'$O$', fontsize=13, color='black')

# 标注半径 R
mid_OB = (O + B2) / 2
ax2.text(mid_OB[0] - 0.6, mid_OB[1] + 0.1, r'$R$', fontsize=14, color='gray', fontstyle='italic')

# 标注直径 2R
mid_diameter = (B2 + B_prime) / 2
ax2.annotate(r'$2R$', xy=(mid_diameter[0] + 0.15, mid_diameter[1] + 0.2),
             fontsize=14, color='red', fontweight='bold')

# 标注顶点
ax2.text(A2[0] - 0.1, A2[1] + 0.25, r'$A$', fontsize=16, fontweight='bold', color='blue')
ax2.text(B2[0] - 0.45, B2[1] - 0.15, r'$B$', fontsize=16, fontweight='bold', color='blue')
ax2.text(C2[0] + 0.15, C2[1] - 0.25, r'$C$', fontsize=16, fontweight='bold', color='blue')
ax2.text(B_prime[0] + 0.15, B_prime[1] + 0.15, r"$B'$", fontsize=14, fontweight='bold', color='red')

# 标注边 a = BC
mid_a2 = (B2 + C2) / 2
ax2.text(mid_a2[0] - 0.5, mid_a2[1] - 0.3, r'$a$', fontsize=15, color='darkgreen', fontweight='bold')

# 标注角 A（圆周角）
vec_AB = B2 - A2
vec_AC = C2 - A2
angle_start = np.arctan2(vec_AB[1], vec_AB[0])
angle_end = np.arctan2(vec_AC[1], vec_AC[0])
if angle_end < angle_start:
    angle_end += 2 * np.pi
arc_A2 = np.linspace(angle_start, angle_end, 50)
arc_r2 = 0.6
ax2.plot(A2[0] + arc_r2 * np.cos(arc_A2), A2[1] + arc_r2 * np.sin(arc_A2),
         'orange', linewidth=1.5)
ax2.text(A2[0] + 0.35, A2[1] - 0.55, r'$A$', fontsize=13, color='orange')

# B'C 处标注直角（直径所对圆周角=90°）
# 计算 B'C 和 B'B 的方向
vec_BpC = C2 - B_prime
vec_BpB = B2 - B_prime
# 角平分线方向
dir1 = vec_BpC / np.linalg.norm(vec_BpC)
dir2 = vec_BpB / np.linalg.norm(vec_BpB)
sq2 = 0.25
corner1 = B_prime + sq2 * dir1
corner3 = B_prime + sq2 * dir2
corner2 = B_prime + sq2 * dir1 + sq2 * dir2
ax2.plot([corner1[0], corner2[0], corner3[0]],
         [corner1[1], corner2[1], corner3[1]], 'r-', linewidth=1.2)

# 关键推导框
proof_text = (
    r"$BB'$ is diameter $\Rightarrow \angle B'CB = 90°$" + "\n"
    + r"Inscribed angle: $\angle B'BC = \angle A$" + "\n"
    + r"$\sin A = \dfrac{a}{2R} \Rightarrow \dfrac{a}{\sin A} = 2R$"
)
ax2.text(0.3, -0.8, proof_text, fontsize=11,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f5e9', edgecolor='#4caf50', alpha=0.9))

ax2.set_xlim(-0.8, 7.5)
ax2.set_ylim(-1.5, 6.5)
ax2.set_aspect('equal')
ax2.set_title('Step 2: Why $= 2R$ (Circumscribed Circle)', fontsize=13, pad=10)
ax2.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(assets_dir, 'sine_rule_proof.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("Generated: sine_rule_proof.png")

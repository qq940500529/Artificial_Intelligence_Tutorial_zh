# 文件：code/inequality_proof_demo.py
# 用途：数值验证 AM-GM 不等式与柯西-施瓦茨不等式，可视化 f(a) = a + 1/a
# 环境要求：Python 3.10+, numpy>=1.24, matplotlib>=3.7

import numpy as np

# ========== 1. 验证 AM-GM 不等式 ==========
print("=" * 50)
print("1. AM-GM 不等式验证：(a+b)/2 >= sqrt(a*b)")
print("=" * 50)

rng = np.random.default_rng(42)
test_pairs = rng.uniform(0, 100, size=(5, 2))

for a, b in test_pairs:
    am = (a + b) / 2          # 算术平均
    gm = np.sqrt(a * b)       # 几何平均
    diff = am - gm
    print(f"  a={a:.4f}, b={b:.4f}  =>  AM={am:.4f}, GM={gm:.4f}, AM-GM={diff:.4f} >= 0 ✓")

# 等号条件：a == b
a_eq = 7.0
am_eq = (a_eq + a_eq) / 2
gm_eq = np.sqrt(a_eq * a_eq)
print(f"\n  等号条件 a=b={a_eq}: AM={am_eq:.4f}, GM={gm_eq:.4f}, AM-GM={am_eq - gm_eq:.4f}")

# ========== 2. 验证柯西-施瓦茨不等式 ==========
print("\n" + "=" * 50)
print("2. 柯西-施瓦茨不等式验证：")
print("   (a1²+a2²)(b1²+b2²) >= (a1·b1+a2·b2)²")
print("=" * 50)

for _ in range(5):
    a1, a2 = rng.uniform(-10, 10, size=2)
    b1, b2 = rng.uniform(-10, 10, size=2)
    lhs = (a1**2 + a2**2) * (b1**2 + b2**2)
    rhs = (a1 * b1 + a2 * b2) ** 2
    print(f"  a=({a1:.2f},{a2:.2f}), b=({b1:.2f},{b2:.2f})")
    print(f"    LHS={lhs:.4f}, RHS={rhs:.4f}, LHS-RHS={lhs - rhs:.4f} >= 0 ✓")

# ========== 3. 验证 f(a) = a + 1/a 的最小值 ==========
print("\n" + "=" * 50)
print("3. f(a) = a + 1/a 的最小值（a > 0）")
print("=" * 50)

a_values = np.linspace(0.1, 5, 1000)
f_values = a_values + 1 / a_values
min_idx = np.argmin(f_values)
print(f"  数值最小值: f({a_values[min_idx]:.4f}) = {f_values[min_idx]:.4f}")
print(f"  理论最小值: f(1) = 2")

# ========== 4. 生成函数图像 ==========
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import os

    plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        a_values, f_values,
        color="#2196F3", linewidth=2,
        label=r"$f(a) = a + \frac{1}{a}$",
    )
    ax.axhline(y=2, color="#FF5722", linestyle="--", alpha=0.7, label=r"$y = 2$ (minimum)")
    ax.plot(1, 2, "o", color="#FF5722", markersize=10, zorder=5)
    ax.annotate(
        r"min at $a=1,\ f=2$",
        xy=(1, 2),
        xytext=(2.5, 3.5),
        fontsize=12,
        arrowprops=dict(arrowstyle="->", color="#333"),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="#333"),
    )

    ax.set_xlabel(r"$a$", fontsize=13)
    ax.set_ylabel(r"$f(a)$", fontsize=13)
    ax.set_title(
        r"$f(a) = a + \frac{1}{a}$ for $a > 0$ (AM-GM lower bound)",
        fontsize=14,
    )
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 8)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 输出到 assets 目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    output_path = os.path.join(assets_dir, "f_a_plus_inv_a.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\n  图像已保存到: {output_path}")
except ImportError:
    print("\n  [提示] 未安装 matplotlib，跳过图像生成。")

print("\n所有验证通过！")

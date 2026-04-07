# 文件：code/radian_trig.py
# 弧度转换与三角函数计算
# 环境要求：Python 3.10+（仅使用标准库 math）

import math


def deg2rad(degrees: float) -> float:
    """角度转弧度"""
    return degrees * math.pi / 180


def rad2deg(radians: float) -> float:
    """弧度转角度"""
    return radians * 180 / math.pi


if __name__ == "__main__":
    # 角度-弧度互转
    print("=" * 50)
    print("角度与弧度互转")
    print("=" * 50)
    for deg in [0, 30, 45, 60, 90, 180, 360]:
        rad = deg2rad(deg)
        print(f"  {deg:>3d}° = {rad:.4f} rad = {rad/math.pi:.4f}π")

    # 特殊角三角函数值
    print("\n" + "=" * 50)
    print("特殊角三角函数值")
    print("=" * 50)
    print(f"{'角度':>6} | {'弧度':>8} | {'sin':>8} | {'cos':>8} | {'tan':>8}")
    print("-" * 50)
    for deg in [0, 30, 45, 60, 90]:
        rad = deg2rad(deg)
        s = math.sin(rad)
        c = math.cos(rad)
        t = math.tan(rad) if deg != 90 else float('inf')
        t_str = f"{t:>8.4f}" if deg != 90 else "     inf"
        print(f"{deg:>5d}° | {rad:>8.4f} | {s:>8.4f} | {c:>8.4f} | {t_str}")

    # 勾股恒等式验证
    print("\n" + "=" * 50)
    print("勾股恒等式验证：sin²θ + cos²θ = 1")
    print("=" * 50)
    for deg in [0, 17, 45, 73, 90, 135, 200, 300]:
        rad = deg2rad(deg)
        result = math.sin(rad)**2 + math.cos(rad)**2
        print(f"  θ = {deg:>3d}°: sin²θ + cos²θ = {result:.10f}")

    # 常见错误演示：传入角度而非弧度
    print("\n" + "=" * 50)
    print("⚠️ 常见错误：把角度直接传入 sin()")
    print("=" * 50)
    print(f"  sin(90) = {math.sin(90):.4f}  ← 错误！90 被当作弧度")
    print(f"  sin(π/2) = {math.sin(math.pi/2):.4f}  ← 正确！")

# 文件：code/trig_identities.py
# 三角恒等变换的数值验证
# 环境要求：Python 3.10+（仅使用标准库 math）

import math


def verify(name: str, left: float, right: float, tol: float = 1e-10):
    """验证恒等式左右两边是否相等"""
    ok = abs(left - right) < tol
    status = "✓" if ok else "✗"
    print(f"  {status} {name}: 左 = {left:.8f}, 右 = {right:.8f}")
    return ok


if __name__ == "__main__":
    A = math.radians(37)
    B = math.radians(53)

    print("=" * 55)
    print("和差角公式验证（A=37°, B=53°）")
    print("=" * 55)
    verify("sin(A+B) = sinA cosB + cosA sinB",
           math.sin(A + B),
           math.sin(A)*math.cos(B) + math.cos(A)*math.sin(B))
    verify("cos(A+B) = cosA cosB - sinA sinB",
           math.cos(A + B),
           math.cos(A)*math.cos(B) - math.sin(A)*math.sin(B))
    verify("sin(A-B) = sinA cosB - cosA sinB",
           math.sin(A - B),
           math.sin(A)*math.cos(B) - math.cos(A)*math.sin(B))

    print("\n" + "=" * 55)
    print("倍角公式验证（θ=37°）")
    print("=" * 55)
    theta = A
    verify("sin(2θ) = 2sinθ cosθ",
           math.sin(2*theta),
           2*math.sin(theta)*math.cos(theta))
    verify("cos(2θ) = cos²θ - sin²θ",
           math.cos(2*theta),
           math.cos(theta)**2 - math.sin(theta)**2)
    verify("cos(2θ) = 2cos²θ - 1",
           math.cos(2*theta),
           2*math.cos(theta)**2 - 1)

    print("\n" + "=" * 55)
    print("半角（降幂）公式验证")
    print("=" * 55)
    verify("sin²θ = (1-cos2θ)/2",
           math.sin(theta)**2,
           (1 - math.cos(2*theta)) / 2)
    verify("cos²θ = (1+cos2θ)/2",
           math.cos(theta)**2,
           (1 + math.cos(2*theta)) / 2)

    print("\n" + "=" * 55)
    print("辅助角公式验证：sinx + √3·cosx = 2sin(x+π/3)")
    print("=" * 55)
    for deg in [0, 30, 45, 60, 90, 120, 180]:
        x = math.radians(deg)
        left = math.sin(x) + math.sqrt(3) * math.cos(x)
        right = 2 * math.sin(x + math.pi/3)
        verify(f"x = {deg}°", left, right)

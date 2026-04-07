# 文件：code/solve_triangle.py
# 综合解三角形计算器
# 环境要求：Python 3.10+（仅使用标准库 math）

import math


def solve_AAS(A_deg: float, B_deg: float, a: float) -> dict:
    """两角一边（AAS）：已知 A, B, a"""
    A = math.radians(A_deg)
    B = math.radians(B_deg)
    C_deg = 180 - A_deg - B_deg
    C = math.radians(C_deg)
    b = a * math.sin(B) / math.sin(A)
    c = a * math.sin(C) / math.sin(A)
    area = 0.5 * a * b * math.sin(C)
    return {"A": A_deg, "B": B_deg, "C": C_deg, "a": a, "b": b, "c": c, "area": area}


def solve_SAS(a: float, b: float, C_deg: float) -> dict:
    """两边夹角（SAS）：已知 a, b, C"""
    C = math.radians(C_deg)
    c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(C))
    cos_A = (b**2 + c**2 - a**2) / (2*b*c)
    A_deg = math.degrees(math.acos(max(-1, min(1, cos_A))))
    B_deg = 180 - A_deg - C_deg
    area = 0.5 * a * b * math.sin(C)
    return {"A": A_deg, "B": B_deg, "C": C_deg, "a": a, "b": b, "c": c, "area": area}


def solve_SSS(a: float, b: float, c: float) -> dict:
    """三边（SSS）：已知 a, b, c"""
    cos_A = (b**2 + c**2 - a**2) / (2*b*c)
    cos_B = (a**2 + c**2 - b**2) / (2*a*c)
    A_deg = math.degrees(math.acos(max(-1, min(1, cos_A))))
    B_deg = math.degrees(math.acos(max(-1, min(1, cos_B))))
    C_deg = 180 - A_deg - B_deg
    # 海伦公式
    s = (a + b + c) / 2
    area = math.sqrt(s * (s-a) * (s-b) * (s-c))
    return {"A": A_deg, "B": B_deg, "C": C_deg, "a": a, "b": b, "c": c, "area": area}


def print_triangle(result: dict, title: str):
    """打印三角形完整信息"""
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")
    print(f"  边：a = {result['a']:.4f}, b = {result['b']:.4f}, c = {result['c']:.4f}")
    print(f"  角：A = {result['A']:.2f}°, B = {result['B']:.2f}°, C = {result['C']:.2f}°")
    print(f"  面积 S = {result['area']:.4f}")
    print(f"  验证：A + B + C = {result['A'] + result['B'] + result['C']:.2f}°")


if __name__ == "__main__":
    # 类型 1：AAS
    r1 = solve_AAS(50, 70, 10)
    print_triangle(r1, "类型 1（AAS）：A=50°, B=70°, a=10")

    # 类型 2：SAS
    r2 = solve_SAS(8, 6, 75)
    print_triangle(r2, "类型 2（SAS）：a=8, b=6, C=75°")

    # 类型 3：SSS
    r3 = solve_SSS(5, 7, 9)
    print_triangle(r3, "类型 3（SSS）：a=5, b=7, c=9")

    # 类型 3：特殊三角形
    r4 = solve_SSS(3, 4, 5)
    print_triangle(r4, "类型 3（SSS）：a=3, b=4, c=5（直角三角形）")

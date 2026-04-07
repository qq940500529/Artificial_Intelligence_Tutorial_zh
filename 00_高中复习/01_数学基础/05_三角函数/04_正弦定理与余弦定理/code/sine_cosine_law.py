# 文件：code/sine_cosine_law.py
# 正弦定理与余弦定理的数值计算
# 环境要求：Python 3.10+（仅使用标准库 math）

import math


def law_of_cosines_side(a: float, b: float, C_deg: float) -> float:
    """余弦定理求第三边：已知两边和夹角"""
    C = math.radians(C_deg)
    return math.sqrt(a**2 + b**2 - 2*a*b*math.cos(C))


def law_of_cosines_angle(a: float, b: float, c: float) -> float:
    """余弦定理求角 C（度数）：已知三边"""
    cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
    return math.degrees(math.acos(cos_C))


def law_of_sines_side(a: float, A_deg: float, B_deg: float) -> float:
    """正弦定理求边 b：已知 a, A, B"""
    A = math.radians(A_deg)
    B = math.radians(B_deg)
    return a * math.sin(B) / math.sin(A)


if __name__ == "__main__":
    # 示例 1：余弦定理 - 两边夹角求第三边
    print("=" * 55)
    print("示例 1：余弦定理求第三边")
    print("  已知：a=5, b=7, C=60°")
    c = law_of_cosines_side(5, 7, 60)
    print(f"  c = {c:.4f}")

    # 示例 2：余弦定理 - 三边求角
    print("\n" + "=" * 55)
    print("示例 2：余弦定理求角")
    print("  已知：a=3, b=4, c=5")
    C = law_of_cosines_angle(3, 4, 5)
    print(f"  C = {C:.1f}°（验证：这是直角三角形！）")

    # 示例 3：正弦定理 - 两角一边求另一边
    print("\n" + "=" * 55)
    print("示例 3：正弦定理求边")
    print("  已知：a=10, A=30°, B=45°")
    b = law_of_sines_side(10, 30, 45)
    print(f"  b = {b:.4f}")

    # 示例 4：余弦相似度
    print("\n" + "=" * 55)
    print("示例 4：余弦相似度（余弦定理的向量版）")
    vec_a = [1, 2, 3]
    vec_b = [4, 5, 6]
    dot_product = sum(x*y for x, y in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x**2 for x in vec_a))
    mag_b = math.sqrt(sum(x**2 for x in vec_b))
    cos_sim = dot_product / (mag_a * mag_b)
    angle = math.degrees(math.acos(cos_sim))
    print(f"  向量 a = {vec_a}")
    print(f"  向量 b = {vec_b}")
    print(f"  余弦相似度 = {cos_sim:.4f}")
    print(f"  夹角 = {angle:.1f}°")

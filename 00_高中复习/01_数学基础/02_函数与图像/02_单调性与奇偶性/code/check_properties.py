# check_properties.py
# 数值检验函数的单调性与奇偶性
# 环境要求：Python 3.10+, numpy

import numpy as np


def check_monotonicity(f, a, b, n=1000):
    """
    数值检验函数 f 在区间 [a, b] 上的单调性。
    返回 'increasing', 'decreasing' 或 'non-monotonic'。
    """
    x = np.linspace(a, b, n)
    y = f(x)
    diffs = np.diff(y)  # 相邻点的差值

    if np.all(diffs > 0):
        return "strictly increasing（严格递增）"
    elif np.all(diffs < 0):
        return "strictly decreasing（严格递减）"
    elif np.all(diffs >= 0):
        return "non-decreasing（非递减/单调不减）"
    elif np.all(diffs <= 0):
        return "non-increasing（非递增/单调不增）"
    else:
        return "non-monotonic（非单调）"


def check_parity(f, a, b, n=1000, tol=1e-8):
    """
    数值检验函数 f 在关于原点对称的区间 [-b, b] 上的奇偶性。
    返回 'even', 'odd', 'both' 或 'neither'。
    """
    x = np.linspace(0.01, b, n)  # 避免 x=0 的特殊情况
    fx = f(x)
    f_neg_x = f(-x)

    is_even = np.allclose(f_neg_x, fx, atol=tol)
    is_odd = np.allclose(f_neg_x, -fx, atol=tol)

    if is_even and is_odd:
        return "both even and odd（既奇又偶，通常是零函数）"
    elif is_even:
        return "even（偶函数）"
    elif is_odd:
        return "odd（奇函数）"
    else:
        return "neither（非奇非偶）"


# ── 测试函数 ──
print("=" * 50)
print("函数单调性与奇偶性数值检验")
print("=" * 50)

# 函数 1：f(x) = 2x + 1
f1 = lambda x: 2 * x + 1
print(f"\nf(x) = 2x + 1:")
print(f"  在 [-10, 10] 上的单调性：{check_monotonicity(f1, -10, 10)}")
print(f"  奇偶性：{check_parity(f1, -10, 10)}")

# 函数 2：f(x) = -x^2
f2 = lambda x: -x ** 2
print(f"\nf(x) = -x²:")
print(f"  在 [0, 10] 上的单调性：{check_monotonicity(f2, 0, 10)}")
print(f"  奇偶性：{check_parity(f2, -10, 10)}")

# 函数 3：f(x) = x^3
f3 = lambda x: x ** 3
print(f"\nf(x) = x³:")
print(f"  在 [-10, 10] 上的单调性：{check_monotonicity(f3, -10, 10)}")
print(f"  奇偶性：{check_parity(f3, -10, 10)}")

# 函数 4：tanh（AI 中常用的激活函数）
f4 = lambda x: np.tanh(x)
print(f"\nf(x) = tanh(x):")
print(f"  在 [-5, 5] 上的单调性：{check_monotonicity(f4, -5, 5)}")
print(f"  奇偶性：{check_parity(f4, -5, 5)}")

# 函数 5：ReLU
f5 = lambda x: np.maximum(0, x)
print(f"\nf(x) = ReLU(x):")
print(f"  在 [-5, 5] 上的单调性：{check_monotonicity(f5, -5, 5)}")
print(f"  奇偶性：{check_parity(f5, -5, 5)}")

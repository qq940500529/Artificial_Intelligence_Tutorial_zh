# 文件：code/inequality_solver.py
# 不等式与绝对值求解器
# 环境要求：Python 3.10+（无需额外库）

import math


def solve_linear_inequality(a: float, b: float, direction: str = ">") -> str:
    """
    求解一元一次不等式 ax + b > 0（或 <, >=, <=）
    """
    if a == 0:
        # 退化为常数不等式，根据方向判断 b 与 0 的关系
        checks = {
            ">": b > 0,
            "<": b < 0,
            ">=": b >= 0,
            "<=": b <= 0,
        }
        if checks[direction]:
            return "解集为全体实数"
        else:
            return "无解"

    # 解方程 ax + b = 0 得到临界点
    critical = -b / a

    # 根据 a 的正负确定解集方向
    if a > 0:
        final_dir = direction
    else:
        # a 为负数，方向反转
        flip = {">": "<", "<": ">", ">=": "<=", "<=": ">="}
        final_dir = flip[direction]

    print(f"不等式：{a}x + {b} {direction} 0")
    print(f"临界点：x = {critical}")
    print(f"解集：x {final_dir} {critical}")
    return f"x {final_dir} {critical}"


def solve_abs_inequality(a: float, b: float, bound: float, direction: str = "<") -> str:
    """
    求解 |ax + b| < bound 或 |ax + b| > bound 形式的绝对值不等式
    """
    print(f"不等式：|{a}x + {b}| {direction} {bound}")

    if bound < 0:
        if direction in ("<", "<="):
            print("绝对值不可能小于负数，无解")
            return "无解"
        else:
            print("绝对值恒大于等于 0，大于负数恒成立")
            return "解集为全体实数"

    if direction in ("<", "<="):
        # 小于取中间：-bound < ax + b < bound
        left = (-bound - b) / a if a > 0 else (bound - b) / a
        right = (bound - b) / a if a > 0 else (-bound - b) / a
        if left > right:
            left, right = right, left
        eq_sign = "=" if "=" in direction else ""
        print(f"去绝对值（小于取中间）：-{bound} {direction} {a}x + {b} {direction} {bound}")
        print(f"解集：{left} <{eq_sign} x <{eq_sign} {right}")
        return f"{left} <{eq_sign} x <{eq_sign} {right}"
    else:
        # 大于取两边：ax + b < -bound 或 ax + b > bound
        val1 = (-bound - b) / a
        val2 = (bound - b) / a
        left = min(val1, val2)
        right = max(val1, val2)
        eq_sign = "=" if "=" in direction else ""
        print(f"去绝对值（大于取两边）：{a}x + {b} <{eq_sign} -{bound} 或 {a}x + {b} >{eq_sign} {bound}")
        print(f"解集：x <{eq_sign} {left} 或 x >{eq_sign} {right}")
        return f"x <{eq_sign} {left} 或 x >{eq_sign} {right}"


def solve_quadratic_inequality(a: float, b: float, c: float, direction: str = ">") -> str:
    """
    求解一元二次不等式 ax² + bx + c > 0（或 <, >=, <=）
    假设 a ≠ 0
    """
    if a == 0:
        return solve_linear_inequality(b, c, direction)

    # 如果 a < 0，两边乘以 -1，反转方向
    if a < 0:
        a, b, c = -a, -b, -c
        flip = {">": "<", "<": ">", ">=": "<=", "<=": ">="}
        direction = flip[direction]

    delta = b**2 - 4 * a * c
    print(f"二次不等式（标准化后）：{a}x² + {b}x + {c} {direction} 0")
    print(f"判别式 Δ = {delta}")

    if delta < 0:
        # 无实数根
        if direction in (">", ">="):
            print("Δ < 0 且 a > 0，抛物线恒在 x 轴上方")
            print("解集为全体实数")
            return "解集为全体实数"
        else:
            print("Δ < 0 且 a > 0，抛物线恒在 x 轴上方")
            print("无解")
            return "无解"
    elif delta == 0:
        x0 = -b / (2 * a)
        print(f"Δ = 0，重根 x = {x0}")
        if direction in (">",):
            return f"x ≠ {x0}"
        elif direction in (">=",):
            return "解集为全体实数"
        elif direction in ("<",):
            return "无解"
        else:  # "<="
            return f"x = {x0}"
    else:
        x1 = (-b - math.sqrt(delta)) / (2 * a)
        x2 = (-b + math.sqrt(delta)) / (2 * a)
        print(f"两个根：x₁ = {x1}, x₂ = {x2}")
        if direction in (">", ">="):
            eq = "=" if "=" in direction else ""
            print(f"开口向上，两根外侧为正")
            print(f"解集：x <{eq} {x1} 或 x >{eq} {x2}")
            return f"x <{eq} {x1} 或 x >{eq} {x2}"
        else:
            eq = "=" if "=" in direction else ""
            print(f"开口向上，两根之间为负")
            print(f"解集：{x1} <{eq} x <{eq} {x2}")
            return f"{x1} <{eq} x <{eq} {x2}"


if __name__ == "__main__":
    # 示例 1：一元一次不等式 -2x + 6 ≤ 0
    print("=" * 50)
    print("示例 1：一元一次不等式 -2x + 6 ≤ 0")
    solve_linear_inequality(-2, 6, "<=")

    # 示例 2：一元二次不等式 x² - 2x - 3 > 0
    print("\n" + "=" * 50)
    print("示例 2：一元二次不等式 x² - 2x - 3 > 0")
    solve_quadratic_inequality(1, -2, -3, ">")

    # 示例 3：绝对值不等式 |2x - 1| ≤ 5
    print("\n" + "=" * 50)
    print("示例 3：绝对值不等式 |2x - 1| ≤ 5")
    solve_abs_inequality(2, -1, 5, "<=")

    # 示例 4：绝对值不等式 |x - 4| > 1
    print("\n" + "=" * 50)
    print("示例 4：绝对值不等式 |x - 4| > 1")
    solve_abs_inequality(1, -4, 1, ">")

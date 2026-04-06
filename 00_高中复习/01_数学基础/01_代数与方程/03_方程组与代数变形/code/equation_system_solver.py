# 文件：code/equation_system_solver.py
# 二元一次方程组求解器
# 环境要求：Python 3.10+（无需额外库）


def solve_system(a1: float, b1: float, c1: float,
                 a2: float, b2: float, c2: float) -> str:
    """
    用加减消元法求解二元一次方程组：
    a1*x + b1*y = c1
    a2*x + b2*y = c2

    返回解的情况和结果
    """
    print(f"方程组：")
    print(f"  {a1}x + {b1}y = {c1}  ... ①")
    print(f"  {a2}x + {b2}y = {c2}  ... ②")

    # 计算行列式（判断解的情况）
    det = a1 * b2 - a2 * b1

    print(f"\n系数行列式 D = {a1}×{b2} - {a2}×{b1} = {det}")

    if det != 0:
        # 唯一解：使用克拉默法则（本质上就是加减消元法的公式化）
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        print(f"D ≠ 0，方程组有唯一解：")
        print(f"  x = ({c1}×{b2} - {c2}×{b1}) / {det} = {x}")
        print(f"  y = ({a1}×{c2} - {a2}×{c1}) / {det} = {y}")

        # 验证
        check1 = a1 * x + b1 * y
        check2 = a2 * x + b2 * y
        print(f"\n验证：")
        print(f"  ① {a1}×{x} + {b1}×{y} = {check1}（应等于 {c1}）{'✓' if abs(check1 - c1) < 1e-10 else '✗'}")
        print(f"  ② {a2}×{x} + {b2}×{y} = {check2}（应等于 {c2}）{'✓' if abs(check2 - c2) < 1e-10 else '✗'}")
        return f"x = {x}, y = {y}"
    else:
        # det == 0，方程平行或重合
        # 通过比较系数比值来判断是平行（无解）还是重合（无穷多解）
        if a1 != 0:
            ratio = a2 / a1
        elif b1 != 0:
            ratio = b2 / b1
        else:
            if c1 == 0:
                print("第一个方程是 0 = 0（恒成立），解取决于第二个方程")
                return "需要更多信息"
            else:
                print("第一个方程是 0 = 非零（矛盾），无解")
                return "无解"

        if abs(c2 - ratio * c1) < 1e-10:
            print("D = 0 且方程等价（一个是另一个的倍数）")
            print("方程组有无穷多解")
            return "无穷多解"
        else:
            print("D = 0 但方程矛盾（平行线不重合）")
            print("方程组无解")
            return "无解"


if __name__ == "__main__":
    # 示例 1：唯一解
    print("=" * 50)
    print("示例 1：唯一解")
    print("=" * 50)
    solve_system(2, 3, 13, 4, 5, 23)

    # 示例 2：唯一解（苹果和梨问题）
    print("\n" + "=" * 50)
    print("示例 2：唯一解（苹果和梨问题）")
    print("=" * 50)
    # x + y = 20, x - 2y = 0（即 x = 2y）
    solve_system(1, 1, 20, 1, -2, 0)

    # 示例 3：无解（平行线）
    print("\n" + "=" * 50)
    print("示例 3：无解（平行线）")
    print("=" * 50)
    solve_system(1, 1, 5, 1, 1, 8)

    # 示例 4：无穷多解（重合线）
    print("\n" + "=" * 50)
    print("示例 4：无穷多解（重合线）")
    print("=" * 50)
    solve_system(1, 1, 5, 2, 2, 10)

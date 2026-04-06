# 文件：check_domain.py
# 用途：通过数值试探来验证函数的定义域和值域
# 环境要求：Python 3.10+, numpy

import numpy as np

def check_domain(func, x_values, func_name="f"):
    """
    对一组输入值逐一测试函数，
    找出哪些输入合法（定义域内）、函数输出的范围（值域估计）。
    """
    valid_x = []
    valid_y = []
    invalid_x = []

    for x in x_values:
        try:
            y = func(x)
            # 检查结果是否为有限的实数
            if np.isfinite(y):
                valid_x.append(x)
                valid_y.append(y)
            else:
                invalid_x.append(x)
        except (ValueError, ZeroDivisionError):
            invalid_x.append(x)

    print(f"=== 函数 {func_name} 的数值检测 ===")
    print(f"测试范围：[{x_values[0]}, {x_values[-1]}]")
    print(f"合法输入数量：{len(valid_x)}")
    print(f"非法输入数量：{len(invalid_x)}")

    if invalid_x:
        print(f"部分非法输入：{invalid_x[:5]}...")

    if valid_y:
        print(f"输出最小值：{min(valid_y):.6f}")
        print(f"输出最大值：{max(valid_y):.6f}")
    print()


# ── 测试用例 ──
if __name__ == "__main__":
    x_test = np.linspace(-10, 10, 10001)

    # 测试 1：f(x) = 1/(x-2)，定义域应排除 x=2
    check_domain(lambda x: 1 / (x - 2), x_test, "1/(x-2)")

    # 测试 2：f(x) = sqrt(3-x)，定义域应为 x <= 3
    check_domain(lambda x: np.sqrt(3 - x), x_test, "sqrt(3-x)")

    # 测试 3：f(x) = ln(x+1)，定义域应为 x > -1
    check_domain(lambda x: np.log(x + 1), x_test, "ln(x+1)")

    # 测试 4：f(x) = x^2 - 4x + 5，值域应为 [1, +∞)
    check_domain(lambda x: x**2 - 4*x + 5, x_test, "x²-4x+5")

# 文件：transform_demo.py
# 用途：演示函数图像的平移、翻转和伸缩变换
# 环境要求：Python 3.10+, numpy, matplotlib

import numpy as np
import matplotlib.pyplot as plt

# ── 配置 ──
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def apply_transforms(x, f, transforms):
    """
    对函数 f 应用一系列变换。
    transforms 是一个字典，包含可选的变换参数：
      h: 水平平移量（正数向右）
      k: 垂直平移量（正数向上）
      a: 垂直伸缩因子
      b: 水平伸缩因子
      flip_x: 是否关于 y 轴翻转
      flip_y: 是否关于 x 轴翻转
    """
    h = transforms.get('h', 0)
    k = transforms.get('k', 0)
    a = transforms.get('a', 1)
    b = transforms.get('b', 1)
    flip_x = transforms.get('flip_x', False)
    flip_y = transforms.get('flip_y', False)

    # 先处理输入端变换
    x_input = b * ((-x) if flip_x else x) - h * b
    # 再处理输出端变换
    y = a * f(x_input)
    if flip_y:
        y = -y
    y = y + k
    return y


# ── 演示 ──
x = np.linspace(-5, 5, 500)

# 基本函数
f = lambda t: t ** 2

print("=== 函数图像变换演示 ===\n")

# 演示各种变换
demos = [
    ("original",     {},                         "y = x^2 (original)"),
    ("shift_right",  {'h': 2},                   "y = (x-2)^2 (shift right 2)"),
    ("shift_up",     {'k': 3},                   "y = x^2 + 3 (shift up 3)"),
    ("flip_y_axis",  {'flip_x': True},            "y = (-x)^2 = x^2 (y-axis flip)"),
    ("flip_x_axis",  {'flip_y': True},            "y = -x^2 (x-axis flip)"),
    ("stretch_v",    {'a': 2},                   "y = 2x^2 (vertical stretch)"),
    ("compress_v",   {'a': 0.5},                 "y = 0.5x^2 (vertical compress)"),
]

for name, transform, desc in demos:
    y = apply_transforms(x, f, transform)
    # 在 x=1 处计算值作为验证
    idx = np.argmin(np.abs(x - 1.0))
    print(f"  {desc:45s} -> f(1) = {y[idx]:.2f}")

print("\nAll transformations computed successfully.")

# norms_demo.py
# Demonstrate Lp norms, distances, cosine similarity, and matrix norms
# Environment: Python 3.10+, numpy, scipy

import numpy as np
import scipy.optimize as opt

x = np.array([3.0, 4.0])
y = np.array([0.0, 5.0])

# ---- 1. Lp norms ----
print("vector x =", x)
print(f"L1 norm = {np.linalg.norm(x, ord=1):.3f}   (= 3 + 4 = 7)")
print(f"L2 norm = {np.linalg.norm(x, ord=2):.3f}   (= sqrt(9+16) = 5)")
print(f"L_inf norm = {np.linalg.norm(x, ord=np.inf):.3f}   (= max(3, 4) = 4)")

# ---- 2. Distances ----
print("\nvector y =", y)
print(f"L1 distance d(x, y) = {np.linalg.norm(x - y, ord=1):.3f}")
print(f"L2 distance d(x, y) = {np.linalg.norm(x - y, ord=2):.3f}")
print(f"L_inf distance = {np.linalg.norm(x - y, ord=np.inf):.3f}")

# ---- 3. Cosine similarity ----
def cosine_sim(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

v1 = np.array([1.0, 1.0])
v2 = np.array([2.0, 1.5])
v3 = np.array([-1.0, -1.0])
print(f"\ncos(v1, v2) = {cosine_sim(v1, v2):.3f}   (close direction, near 1)")
print(f"cos(v1, v3) = {cosine_sim(v1, v3):.3f}   (opposite, equals -1)")

# ---- 4. L1 vs L2 sparsity ----
res_l2 = opt.minimize(lambda v: np.linalg.norm(v, 2),
                      x0=[0.0, 0.0],
                      constraints={'type': 'eq',
                                   'fun': lambda v: v[0] + 2*v[1] - 4})
res_l1 = opt.minimize(lambda v: np.linalg.norm(v, 1),
                      x0=[0.1, 0.1],
                      constraints={'type': 'eq',
                                   'fun': lambda v: v[0] + 2*v[1] - 4})
print(f"\nUnder a + 2b = 4:")
print(f"  Minimum L2-norm solution: ({res_l2.x[0]:.3f}, {res_l2.x[1]:.3f})  -- both nonzero")
print(f"  Minimum L1-norm solution: ({res_l1.x[0]:.3f}, {res_l1.x[1]:.3f})  -- one zeroed (sparse)")

# ---- 5. Matrix Frobenius vs spectral norm ----
M = np.array([[1, 2],
              [3, 4]], dtype=float)
print(f"\nMatrix M Frobenius norm = {np.linalg.norm(M, 'fro'):.3f}   (= sqrt(30))")
print(f"Matrix M spectral norm = {np.linalg.norm(M, 2):.3f}   (= largest singular value)")

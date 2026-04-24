# linear_transform_demo.py
# Verify properties of linear transformations
# Environment: Python 3.10+, numpy

import numpy as np

# ---- 1. Define a rotation by 90 degrees ----
theta = np.pi / 2
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
print("Rotation matrix R (90 deg):\n", R.round(3))

# Verify that columns of R are images of e1, e2
e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
print("\nR @ e1 =", (R @ e1).round(3), "  (expected [0, 1])")
print("R @ e2 =", (R @ e2).round(3), "  (expected [-1, 0])")
print("Columns of R:", R[:, 0].round(3), "and", R[:, 1].round(3))

# ---- 2. Verify linearity ----
u = np.array([2.0, 3.0])
v = np.array([1.0, -1.0])
c = 5.0

lhs = R @ (u + v)
rhs = R @ u + R @ v
print("\nAdditivity:  T(u+v) =", lhs.round(3), "  T(u)+T(v) =", rhs.round(3))

lhs2 = R @ (c * u)
rhs2 = c * (R @ u)
print("Homogeneity: T(c*u) =", lhs2.round(3), "  c*T(u) =", rhs2.round(3))

# ---- 3. Matrix product = composition of transformations ----
H = np.array([[1, 1],
              [0, 1]])             # shear
x = np.array([1.0, 1.0])

result_A = R @ (H @ x)
result_B = (R @ H) @ x
print("\nComposition: R @ (H @ x) =", result_A.round(3),
      "  (R @ H) @ x =", result_B.round(3))

# ---- 4. Verify AB != BA ----
RH = R @ H
HR = H @ R
print("\nR @ H =\n", RH.round(3))
print("H @ R =\n", HR.round(3))
print("Equal?", np.allclose(RH, HR))

# ---- 5. Determinant tells us about invertibility ----
P = np.array([[1, 0],
              [0, 0]])             # projection onto x-axis
print("\ndet(R) =", round(np.linalg.det(R), 3), "  (=1, area- and orientation-preserving)")
print("det(H) =", round(np.linalg.det(H), 3), "  (=1, area-preserving)")
print("det(P) =", round(np.linalg.det(P), 3), "  (=0, NOT invertible)")

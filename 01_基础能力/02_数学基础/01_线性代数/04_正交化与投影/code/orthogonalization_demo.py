# orthogonalization_demo.py
# Demo: projection, Gram-Schmidt, least squares, orthogonal matrices
# Environment: Python 3.10+, numpy

import numpy as np

# ---- 1. Single-direction projection ----
v = np.array([3.0, 2.0])
u = np.array([1.0, 0.0])
proj = (v @ u) / (u @ u) * u
residual = v - proj
print("v =", v, "  u =", u)
print("proj_u(v) =", proj, "  (should be [3, 0])")
print("residual =", residual, "  inner(residual, u) =", residual @ u, "  (should be 0)")


# ---- 2. Gram-Schmidt ----
def gram_schmidt(A):
    """Apply Gram-Schmidt to columns of A. Returns orthonormal Q."""
    A = A.astype(float)
    n_cols = A.shape[1]
    Q = np.zeros_like(A)
    for k in range(n_cols):
        v_k = A[:, k].copy()
        for j in range(k):
            v_k -= (A[:, k] @ Q[:, j]) * Q[:, j]
        Q[:, k] = v_k / np.linalg.norm(v_k)
    return Q


A = np.array([[1, 1, 0],
              [1, 0, 1],
              [0, 1, 1]], dtype=float)
Q = gram_schmidt(A)
print("\nGram-Schmidt orthonormal Q =\n", Q.round(3))
print("Q^T Q =\n", (Q.T @ Q).round(3), "  (should be identity)")

# ---- 3. Compare with NumPy QR ----
Q_np, R_np = np.linalg.qr(A)
print("\nNumPy QR's Q =\n", Q_np.round(3))
print("Same column directions (allowing sign flip):",
      [bool(np.allclose(np.abs(Q[:, i]), np.abs(Q_np[:, i]))) for i in range(3)])

# ---- 4. Least squares ----
np.random.seed(42)
x_data = np.linspace(0, 10, 30)
y_data = 2 * x_data + 1 + np.random.randn(30) * 0.5
X = np.column_stack([x_data, np.ones_like(x_data)])
w = np.linalg.solve(X.T @ X, X.T @ y_data)
print(f"\nLeast-squares solution: slope={w[0]:.3f}, intercept={w[1]:.3f}   (true: 2, 1)")

y_hat = X @ w
residual_vec = y_data - y_hat
print("X^T @ residual =", (X.T @ residual_vec).round(8),
      "  (should be ~0, residual orthogonal to col(X))")

# ---- 5. Orthogonal matrices preserve length ----
theta = np.pi / 6
Q_rot = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
x = np.array([3.0, 4.0])
print(f"\n||x|| before = {np.linalg.norm(x):.3f}")
print(f"||Qx|| after = {np.linalg.norm(Q_rot @ x):.3f}   (should be equal)")

# matrix_decompositions_demo.py
# Demo of LU / Cholesky / QR / SVD / NMF decompositions
# Environment: Python 3.10+, numpy, scipy, scikit-learn

import time
import numpy as np
from scipy.linalg import lu, cholesky, qr, solve_triangular

np.set_printoptions(precision=4, suppress=True)

# ---- 1. LU decomposition ----
A = np.array([[4, 3, 2],
              [2, 1, 0],
              [1, 0, 3]], dtype=float)
P, L, U = lu(A)
print("LU decomposition (PA = LU):")
print("L =\n", L); print("U =\n", U)
print("Equal P@A == L@U?", np.allclose(P @ A, L @ U))

# ---- 2. Cholesky decomposition ----
np.random.seed(0)
M = np.random.randn(4, 4)
S = M @ M.T + np.eye(4)
L_chol = cholesky(S, lower=True)
print("\nCholesky decomposition:")
print("L @ L^T == S?", np.allclose(L_chol @ L_chol.T, S))

# ---- 3. QR decomposition ----
A2 = np.random.randn(5, 3)
Q, R = qr(A2, mode='economic')
print("\nQR decomposition:")
print("Q shape", Q.shape, "  R shape", R.shape)
print("Q @ R == A2?", np.allclose(Q @ R, A2))
print("Q^T Q approx I?", np.allclose(Q.T @ Q, np.eye(3)))

# ---- 4. Solve least squares with QR ----
b = np.random.randn(5)
x_qr = solve_triangular(R, Q.T @ b)
x_lstsq, *_ = np.linalg.lstsq(A2, b, rcond=None)
print("\nQR-based LS solution =", x_qr)
print("np.linalg.lstsq      =", x_lstsq)
print("Same?", np.allclose(x_qr, x_lstsq))

# ---- 5. Speed comparison: solve SPD system ----
n = 1000
M = np.random.randn(n, n)
A_spd = M @ M.T + n * np.eye(n)
b = np.random.randn(n)

t0 = time.time(); _ = np.linalg.solve(A_spd, b); t_solve = time.time() - t0
t0 = time.time(); L = cholesky(A_spd, lower=True)
y = solve_triangular(L, b, lower=True)
x_chol = solve_triangular(L.T, y, lower=False); t_chol = time.time() - t0
t0 = time.time(); _ = np.linalg.inv(A_spd) @ b; t_inv = time.time() - t0

print(f"\nSolve 1000x1000 SPD system A x = b:")
print(f"  np.linalg.solve (LU): {t_solve*1000:.2f} ms")
print(f"  Cholesky + back-sub:  {t_chol*1000:.2f} ms   (theoretically fastest)")
print(f"  inv(A) @ b (BAD):     {t_inv*1000:.2f} ms")

# ---- 6. NMF ----
try:
    from sklearn.decomposition import NMF
    np.random.seed(42)
    V = np.array([
        [5, 4, 0, 0, 1, 0, 0, 0],
        [4, 5, 0, 0, 0, 1, 0, 0],
        [0, 0, 5, 4, 0, 0, 1, 0],
        [0, 1, 4, 5, 0, 0, 0, 1],
        [1, 0, 0, 1, 5, 4, 4, 5],
    ], dtype=float)
    nmf = NMF(n_components=2, init='nndsvd', max_iter=500, random_state=42)
    W = nmf.fit_transform(V)
    H = nmf.components_
    print(f"\nNMF: V (5x8) -> W ({W.shape}) @ H ({H.shape})")
    print("W =\n", W.round(2))
    print("H =\n", H.round(2))
    err = np.linalg.norm(V - W @ H, 'fro')
    print(f"||V - W H||_F = {err:.3f}")
except ImportError:
    print("\n(scikit-learn not installed, skipping NMF demo)")

# eigen_svd_demo.py
# Demo: eigendecomposition and SVD
# Environment: Python 3.10+, numpy

import numpy as np

# ---- 1. Eigendecomposition ----
A = np.array([[4, 1],
              [2, 3]], dtype=float)
eigvals, eigvecs = np.linalg.eig(A)
print("Matrix A =\n", A)
print("eigenvalues lambda =", eigvals)
print("eigenvectors (as columns) =\n", eigvecs.round(3))

for i in range(2):
    Av = A @ eigvecs[:, i]
    lam_v = eigvals[i] * eigvecs[:, i]
    print(f"A @ v{i+1} =", Av.round(3),
          f"  lambda{i+1} * v{i+1} =", lam_v.round(3))

# ---- 2. Diagonalization reconstruction ----
V = eigvecs
Lambda = np.diag(eigvals)
A_reconstructed = V @ Lambda @ np.linalg.inv(V)
print("\nV Lambda V^-1 =\n", A_reconstructed.round(3))
print("Equal to A?", np.allclose(A, A_reconstructed))

# ---- 3. Symmetric matrix ----
S = np.array([[2, 1],
              [1, 3]], dtype=float)
eigvals_s, eigvecs_s = np.linalg.eigh(S)
print("\nSymmetric S, eigenvalues:", eigvals_s)
print("Eigenvector orthogonality Q^T Q =\n", (eigvecs_s.T @ eigvecs_s).round(8))

# ---- 4. SVD ----
M = np.array([[3, 1, 1],
              [-1, 3, 1]], dtype=float)
U, sigmas, Vt = np.linalg.svd(M)
print("\nMatrix M shape:", M.shape)
print("U shape:", U.shape, "  Sigma:", sigmas, "  V^T shape:", Vt.shape)
print("U^T U =\n", (U.T @ U).round(8), "  (should be identity)")
print("V V^T =\n", (Vt @ Vt.T).round(8), "  (should be identity)")

Sigma_full = np.zeros_like(M)
Sigma_full[:2, :2] = np.diag(sigmas)
M_reconstructed = U @ Sigma_full @ Vt
print("U Sigma V^T =\n", M_reconstructed.round(3))
print("Equal to M?", np.allclose(M, M_reconstructed))

# ---- 5. Low-rank approximation ----
np.random.seed(0)
true_rank = 3
m, n = 100, 50
B = np.random.randn(m, true_rank)
C = np.random.randn(true_rank, n)
A_lowrank = B @ C + 0.01 * np.random.randn(m, n)

U2, s2, Vt2 = np.linalg.svd(A_lowrank, full_matrices=False)
print("\nFirst 6 singular values:", s2[:6].round(3))
k = 3
A_k = U2[:, :k] @ np.diag(s2[:k]) @ Vt2[:k, :]
relative_err = np.linalg.norm(A_lowrank - A_k, 'fro') / np.linalg.norm(A_lowrank, 'fro')
print(f"Reconstruct with top {k} singular values, relative Frobenius error = {relative_err:.4f}")

# ---- 6. SVD-based pseudoinverse ----
A_pinv_svd = Vt2.T @ np.diag([1/s if s > 1e-10 else 0 for s in s2]) @ U2.T
A_pinv_np = np.linalg.pinv(A_lowrank)
print("\nManual pinv == np.linalg.pinv?", np.allclose(A_pinv_svd, A_pinv_np))

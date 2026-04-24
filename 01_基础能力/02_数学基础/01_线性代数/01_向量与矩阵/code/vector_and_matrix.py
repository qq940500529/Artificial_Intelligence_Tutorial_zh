# vector_and_matrix.py
# Demonstrate vector and matrix basic operations
# Environment: Python 3.10+, numpy

import numpy as np

# ---- 1. Create vector and matrix ----
x = np.array([1.0, 2.0, 3.0])           # 1D array, treated as a column vector
A = np.array([[1, 2, 3],
              [4, 5, 6]])                 # 2 x 3 matrix

print("vector x:", x, "  shape:", x.shape)
print("matrix A:\n", A, "  shape:", A.shape)

# ---- 2. Transpose ----
print("\nTranspose A^T:\n", A.T, "  shape:", A.T.shape)

# ---- 3. Matrix-vector product ----
y = A @ x          # @ is the matrix-multiply operator in Python
print("\nA @ x =", y, "  shape:", y.shape)

# ---- 4. Matrix-matrix product ----
B = np.array([[1, 0],
              [0, 1],
              [1, 1]])                    # 3 x 2 matrix
C = A @ B          # (2,3) @ (3,2) -> (2,2)
print("\nA @ B =\n", C, "  shape:", C.shape)

# ---- 5. Verify non-commutativity ----
print("\nB @ A shape:", (B @ A).shape, "  vs  A @ B shape:", C.shape)
print("=> Matrix multiplication is NOT commutative")

# ---- 6. Identity matrix ----
I3 = np.eye(3)
print("\nIdentity I3:\n", I3)
print("I3 @ x =", I3 @ x, "  (same as x)")

# ---- 7. A simplified neural-network layer ----
np.random.seed(0)
W = np.random.randn(4, 3) * 0.1   # weights: 3-d input -> 4-d output
b = np.zeros(4)                    # bias
y_layer = W @ x + b
print("\nNN-layer output y = W x + b:", y_layer, "  shape:", y_layer.shape)

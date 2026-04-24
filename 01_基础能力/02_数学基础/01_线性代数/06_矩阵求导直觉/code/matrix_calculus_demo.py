# matrix_calculus_demo.py
# Verify matrix calculus formulas with PyTorch autograd
# Environment: Python 3.10+, torch>=2.0

import numpy as np
import torch

torch.manual_seed(0)

# ---- Formula 1: f = a^T x ----
a = torch.tensor([1.0, 2.0, 3.0])
x = torch.tensor([4.0, 5.0, 6.0], requires_grad=True)
f = a @ x
f.backward()
print("Formula 1: a^T x")
print("  autograd df/dx =", x.grad.numpy(), "  manual = a =", a.numpy())

# ---- Formula 2: f = x^T A x ----
x = torch.tensor([1.0, 2.0], requires_grad=True)
A = torch.tensor([[2.0, 1.0],
                  [3.0, 4.0]])
f = x @ A @ x
f.backward()
manual = (A + A.T) @ x.detach()
print("\nFormula 2: x^T A x  (A non-symmetric)")
print("  autograd df/dx =", x.grad.numpy(), "  manual (A+A^T)x =", manual.numpy())

# ---- Formula 3: f = ||x||^2 ----
x = torch.tensor([3.0, 4.0], requires_grad=True)
f = (x ** 2).sum()
f.backward()
print("\nFormula 3: ||x||^2")
print("  autograd df/dx =", x.grad.numpy(), "  manual 2x =", (2 * x.detach()).numpy())

# ---- Formula 4: f = ||A x - b||^2 ----
A = torch.tensor([[1.0, 2.0],
                  [3.0, 4.0],
                  [5.0, 6.0]])
b = torch.tensor([1.0, 0.0, -1.0])
x = torch.tensor([0.5, -0.5], requires_grad=True)
f = ((A @ x - b) ** 2).sum()
f.backward()
manual = 2 * A.T @ (A @ x.detach() - b)
print("\nFormula 4: ||A x - b||^2")
print("  autograd df/dx =", x.grad.numpy(), "  manual 2 A^T (Ax - b) =", manual.numpy())

# ---- Formula 5: f = tr(A^T X) ----
A = torch.tensor([[1.0, 2.0],
                  [3.0, 4.0]])
X = torch.tensor([[5.0, 6.0],
                  [7.0, 8.0]], requires_grad=True)
f = (A.T @ X).trace()
f.backward()
print("\nFormula 5: tr(A^T X)")
print("  autograd df/dX =\n", X.grad.numpy())
print("  manual = A =\n", A.numpy())

# ---- Real demo: linear regression ----
print("\n--- Linear regression ---")
torch.manual_seed(42)
X_data = torch.randn(50, 3)
true_w = torch.tensor([2.0, -1.5, 0.7])
y_data = X_data @ true_w + 0.05 * torch.randn(50)

# Method 1: normal equation
w_normal = torch.linalg.solve(X_data.T @ X_data, X_data.T @ y_data)

# Method 2: gradient descent via autograd
w_gd = torch.zeros(3, requires_grad=True)
optimizer = torch.optim.SGD([w_gd], lr=0.05)
for _ in range(2000):
    optimizer.zero_grad()
    loss = ((X_data @ w_gd - y_data) ** 2).mean()
    loss.backward()
    optimizer.step()

print("Normal equation w* =", w_normal.numpy().round(4))
print("Gradient descent w* =", w_gd.detach().numpy().round(4))
print("True w  =", true_w.numpy())

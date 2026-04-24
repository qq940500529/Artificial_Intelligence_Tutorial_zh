# plot_svd_image_compression.py
# Demo SVD-based low-rank approximation on a synthetic grayscale image
# Environment: Python 3.10+, matplotlib, numpy

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def make_synthetic_image(size=128):
    """Build a synthetic grayscale image with a few clear features."""
    img = np.zeros((size, size))
    # Background gradient
    for i in range(size):
        img[i, :] = 0.2 + 0.3 * (i / size)
    # A bright diagonal stripe
    for i in range(size):
        for j in range(size):
            if abs(i - j) < 6:
                img[i, j] = 0.95
    # A circular blob
    cy, cx = size // 3, 2 * size // 3
    for i in range(size):
        for j in range(size):
            if (i - cy) ** 2 + (j - cx) ** 2 < (size // 8) ** 2:
                img[i, j] = 0.05
    # Noise
    img += 0.03 * np.random.RandomState(0).randn(size, size)
    return np.clip(img, 0, 1)


img = make_synthetic_image(128)
U, s, Vt = np.linalg.svd(img, full_matrices=False)


def low_rank(k):
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]


ks = [1, 5, 10, 20, 50]
fig, axes = plt.subplots(1, len(ks) + 1, figsize=(16, 3.6))

axes[0].imshow(img, cmap='gray', vmin=0, vmax=1)
axes[0].set_title(f'Original\nrank={min(img.shape)}', fontsize=10)
axes[0].axis('off')

for ax, k in zip(axes[1:], ks):
    Ak = low_rank(k)
    err = np.linalg.norm(img - Ak, 'fro') / np.linalg.norm(img, 'fro')
    ax.imshow(np.clip(Ak, 0, 1), cmap='gray', vmin=0, vmax=1)
    ax.set_title(f'k = {k}\nrel.err = {err:.3f}', fontsize=10)
    ax.axis('off')

fig.suptitle('SVD low-rank approximation: keep top-$k$ singular values',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '..', 'assets')
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, 'svd_image_compression.png')
plt.savefig(output_path, dpi=140, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {output_path}")

"""
animate_convergence.py
用途：生成收敛 vs 发散序列的动画 GIF，用于「数列极限初步」课程。
依赖：Python 3.10+, matplotlib >= 3.6, Pillow >= 9.0

左图：a_n = 1/n → 0（收敛），带 ε-band 逐步收缩
右图：b_n = (-1)^n（发散），点在 +1 / -1 之间交替

输出：../assets/convergence_anim.gif（相对于本脚本）
"""

import os
import io

import matplotlib
matplotlib.use("Agg")  # headless backend — no display needed for GIF generation
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# ── font / style ──────────────────────────────────────────────
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ── paths ─────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, os.pardir, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "convergence_anim.gif")

# ── sequence data ─────────────────────────────────────────────
N_FRAMES = 40
ns = np.arange(1, N_FRAMES + 1)
a_n = 1.0 / ns          # convergent: 1/n → 0
b_n = (-1.0) ** ns       # divergent: (-1)^n

# epsilon shrinks every 10 frames
EPSILON_SCHEDULE = {0: 0.3, 10: 0.2, 20: 0.1, 30: 0.05}
LIMIT = 0.0


def _current_epsilon(frame: int) -> float:
    """Return the ε value in effect at *frame* (0-indexed)."""
    eps = 0.3
    for boundary in sorted(EPSILON_SCHEDULE):
        if frame >= boundary:
            eps = EPSILON_SCHEDULE[boundary]
    return eps


def _render_frame(frame: int) -> Image.Image:
    """Draw both subplots for the given frame index and return a PIL Image."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(12, 5), facecolor="white")

    k = frame + 1  # number of points visible (1-based count)
    eps = _current_epsilon(frame)

    # ── left subplot: convergence ─────────────────────────────
    visible_n = ns[:k]
    visible_a = a_n[:k]

    inside = np.abs(visible_a - LIMIT) <= eps
    outside = ~inside

    ax_l.axhline(LIMIT, color="steelblue", ls="--", lw=1.5, label="$L = 0$")
    ax_l.axhspan(
        LIMIT - eps, LIMIT + eps,
        color="steelblue", alpha=0.12,
        label=f"$\\epsilon = {eps}$",
    )

    if np.any(outside):
        ax_l.scatter(
            visible_n[outside], visible_a[outside],
            color="crimson", s=40, zorder=5, label="Outside $\\epsilon$-band",
        )
    if np.any(inside):
        ax_l.scatter(
            visible_n[inside], visible_a[inside],
            color="seagreen", s=40, zorder=5, label="Inside $\\epsilon$-band",
        )

    ax_l.set_xlim(0, N_FRAMES + 1)
    ax_l.set_ylim(-0.45, 1.15)
    ax_l.set_xlabel("$n$", fontsize=12)
    ax_l.set_ylabel("$a_n$", fontsize=12)
    ax_l.set_title("Convergence: $a_n = 1/n \\to 0$", fontsize=13)
    ax_l.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax_l.grid(True, alpha=0.3)
    ax_l.spines["top"].set_visible(False)
    ax_l.spines["right"].set_visible(False)

    # ── right subplot: divergence ─────────────────────────────
    visible_b = b_n[:k]

    ax_r.plot(
        visible_n, visible_b,
        ls="--", lw=0.8, color="gray", zorder=3,
    )
    ax_r.scatter(
        visible_n, visible_b,
        color="darkorange", s=40, zorder=5,
    )

    ax_r.set_xlim(0, N_FRAMES + 1)
    ax_r.set_ylim(-1.6, 1.6)
    ax_r.set_xlabel("$n$", fontsize=12)
    ax_r.set_ylabel("$b_n$", fontsize=12)
    ax_r.set_title("Divergence: $b_n = (-1)^n$", fontsize=13)
    ax_r.grid(True, alpha=0.3)
    ax_r.spines["top"].set_visible(False)
    ax_r.spines["right"].set_visible(False)

    plt.tight_layout()

    # render to in-memory PNG then convert to PIL Image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def main() -> None:
    frames = [_render_frame(i) for i in range(N_FRAMES)]

    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=150,
        loop=0,
    )
    print(f"GIF saved to {os.path.abspath(OUTPUT_PATH)}")
    print(f"  frames : {len(frames)}")
    print(f"  size   : {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")


if __name__ == "__main__":
    main()

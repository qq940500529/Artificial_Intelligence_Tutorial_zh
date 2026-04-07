"""
animate_ssa.py — Animated GIF demonstrating the SSA (Side-Side-Angle)
ambiguity case for solving triangles.

Dependencies: Python 3.10+, matplotlib, numpy, Pillow
Usage:        python code/animate_ssa.py
Output:       ../assets/ssa_ambiguity_anim.gif (relative to this script)
"""

import os
import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# ── font / style ──────────────────────────────────────────────────────
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ── output path ───────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, os.pardir, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(ASSETS_DIR, "ssa_ambiguity_anim.gif")

# ── geometric constants ───────────────────────────────────────────────
A_DEG = 30.0                        # angle A in degrees
A_RAD = np.radians(A_DEG)           # angle A in radians
b = 5.0                             # side b (A → C)
h = b * np.sin(A_RAD)               # perpendicular height from C to base
Cx = b * np.cos(A_RAD)              # C coordinates
Cy = b * np.sin(A_RAD)

N_FRAMES = 60
A_MIN, A_MAX = 0.0, 7.0             # side a sweep range
FPS_DELAY = 150                      # ms per frame


def find_intersections(a):
    """Return x-coordinates where the circle centred at C with radius *a*
    intersects the x-axis (y = 0).

    Circle: (x - Cx)^2 + Cy^2 = a^2  →  (x - Cx)^2 = a^2 - Cy^2
    """
    diff = a * a - Cy * Cy
    if diff < -1e-12:
        return []
    if diff < 1e-12:
        return [Cx]
    sq = np.sqrt(diff)
    return sorted([Cx - sq, Cx + sq])


def draw_frame(a):
    """Render one frame for side-length *a* and return a PIL Image."""
    fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(-1.5, 9)
    ax.set_ylim(-2.0, 5.5)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$", fontsize=12)
    ax.set_ylabel("$y$", fontsize=12)
    ax.grid(True, alpha=0.15)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    # ── rays from A ───────────────────────────────────────────────────
    ray_len = 8.5
    # base ray (along x-axis)
    ax.annotate("", xy=(ray_len, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-", color="grey", lw=1.0))
    ax.plot([0, ray_len], [0, 0], color="grey", lw=1.0, zorder=1)
    # upper ray (30° direction)
    ax.plot([0, ray_len * np.cos(A_RAD)],
            [0, ray_len * np.sin(A_RAD)],
            color="grey", lw=1.0, zorder=1)

    # ── angle arc + label ─────────────────────────────────────────────
    arc = patches.Arc((0, 0), 1.6, 1.6, angle=0,
                       theta1=0, theta2=A_DEG,
                       color="purple", lw=1.5)
    ax.add_patch(arc)
    mid_a = A_RAD / 2
    ax.text(1.1 * np.cos(mid_a), 1.1 * np.sin(mid_a),
            r"$A = 30°$", fontsize=10, color="purple",
            ha="left", va="bottom")

    # ── side b  (A → C) ──────────────────────────────────────────────
    ax.plot([0, Cx], [0, Cy], "k-", lw=2.5, zorder=3)
    mid_bx, mid_by = Cx / 2, Cy / 2
    ax.text(mid_bx - 0.55, mid_by + 0.25,
            r"$b = 5$", fontsize=11, color="black",
            ha="center", va="bottom", fontweight="bold")

    # ── point labels  A and C ─────────────────────────────────────────
    ax.plot(0, 0, "ko", ms=6, zorder=5)
    ax.text(-0.35, -0.35, "$A$", fontsize=13, fontweight="bold")
    ax.plot(Cx, Cy, "ko", ms=6, zorder=5)
    ax.text(Cx + 0.15, Cy + 0.25, "$C$", fontsize=13, fontweight="bold")

    # ── perpendicular from C to base (height h) ──────────────────────
    ax.plot([Cx, Cx], [0, Cy], "k--", lw=0.9, alpha=0.5, zorder=2)
    ax.text(Cx + 0.15, Cy / 2,
            f"$h = b\\sin A = {h:.1f}$", fontsize=9,
            color="dimgrey", va="center")
    # small right-angle marker
    sq = 0.2
    ax.plot([Cx - sq, Cx - sq, Cx], [0, sq, sq],
            "k-", lw=0.7, alpha=0.5)

    # ── circle from C with radius a ──────────────────────────────────
    if a > 0.05:
        circle = plt.Circle((Cx, Cy), a, fill=False,
                             linestyle="--", linewidth=1.5,
                             edgecolor="steelblue", alpha=0.7, zorder=2)
        ax.add_patch(circle)
        ax.text(Cx + a * 0.55, Cy + a * 0.65,
                f"$a = {a:.2f}$", fontsize=10,
                color="steelblue", style="italic",
                bbox=dict(boxstyle="round,pad=0.25",
                          fc="white", ec="steelblue", alpha=0.85))

    # ── intersections & case label ────────────────────────────────────
    xs = find_intersections(a)
    # filter to positive x only for the "one solution when a >= b" logic
    xs_pos = [x for x in xs if x > 1e-6]
    xs_neg = [x for x in xs if x <= 1e-6]

    eps = 0.08  # tolerance for tangent detection
    if len(xs) == 0:
        case_text = "No Solution"
        case_color = "red"
    elif len(xs) == 1 or (len(xs) == 2 and abs(xs[1] - xs[0]) < eps):
        case_text = "One Solution (tangent)"
        case_color = "darkorange"
        bx = xs[0]
        ax.plot(bx, 0, "o", color="darkorange", ms=9, zorder=6)
        ax.text(bx, -0.45, "$B$", fontsize=12,
                color="darkorange", ha="center", fontweight="bold")
        # triangle sides
        ax.plot([0, bx], [0, 0], color="darkorange", lw=2.2, zorder=4)
        ax.plot([bx, Cx], [0, Cy], color="darkorange", lw=2.2, zorder=4)
    elif len(xs) == 2:
        if len(xs_pos) == 2:
            case_text = "Two Solutions"
            case_color = "royalblue"
            for idx, bx in enumerate(xs_pos):
                label = f"$B_{idx+1}$"
                clr = "royalblue" if idx == 0 else "dodgerblue"
                ax.plot(bx, 0, "o", color=clr, ms=9, zorder=6)
                ax.text(bx, -0.45, label, fontsize=12,
                        color=clr, ha="center", fontweight="bold")
                ls = "-" if idx == 0 else "--"
                ax.plot([0, bx], [0, 0], color=clr, lw=2.2,
                        linestyle=ls, zorder=4)
                ax.plot([bx, Cx], [0, Cy], color=clr, lw=2.2,
                        linestyle=ls, zorder=4)
        else:
            # one intersection positive → one valid triangle
            case_text = "One Solution"
            case_color = "green"
            bx = xs_pos[0] if xs_pos else xs[1]
            ax.plot(bx, 0, "o", color="green", ms=9, zorder=6)
            ax.text(bx, -0.45, "$B$", fontsize=12,
                    color="green", ha="center", fontweight="bold")
            ax.plot([0, bx], [0, 0], color="green", lw=2.2, zorder=4)
            ax.plot([bx, Cx], [0, Cy], color="green", lw=2.2, zorder=4)

    # ── info box (top-left) ───────────────────────────────────────────
    ax.text(0.02, 0.97, f"$a = {a:.2f}$\n{case_text}",
            transform=ax.transAxes, fontsize=14,
            fontweight="bold", color=case_color,
            va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.4",
                      fc="white", ec=case_color, lw=1.5, alpha=0.92))

    # ── title ─────────────────────────────────────────────────────────
    ax.set_title("SSA Ambiguity: Solving Triangles ($A=30°,\\ b=5$)",
                 fontsize=14, pad=10)

    # ── render to PIL Image ───────────────────────────────────────────
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).copy()


def main():
    a_values = np.linspace(A_MIN, A_MAX, N_FRAMES)
    frames = []
    for i, a in enumerate(a_values):
        print(f"\rRendering frame {i+1}/{N_FRAMES} (a={a:.2f})", end="")
        frames.append(draw_frame(a))
    print()

    # Save as animated GIF
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FPS_DELAY,
        loop=0,
    )
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"Saved: {OUTPUT_PATH}  ({size_kb:.0f} KB, {N_FRAMES} frames)")


if __name__ == "__main__":
    main()

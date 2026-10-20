# Copyright Matthew Armstrong (https://github.com/The-Dorkknight). Code: PolyForm Noncommercial 1.0.0.
"""Draw the paper's figures from the real fin code in code/shark_core.py.

python3 tools/make_figures.py        (needs numpy and matplotlib)

Figures 5-8 are captures (PrusaSlicer G-code, Cura) and are not redrawn here.
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import shark_core as sc  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

FIG = os.path.join(ROOT, "paper", "figures")
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"
FIN, PART, ACCENT, PALE = "#e8741a", "#9aa4b1", "#e8741a", "#f6c79f"

VERSIONS = [
    ("0.1.0  round back", dict(back_curve="ellipse", top_cut=0, tip_length=0, tooth_pitch=6, contact_gap=0.2, anchor_teeth=0)),
    ("0.1.1  triangle", dict(back_curve="vertical", top_cut=0, tip_length=0, tooth_pitch=6, contact_gap=0.2, anchor_teeth=0)),
    ("0.1.2  more teeth, 2 anchors", dict(back_curve="vertical", top_cut=0, tip_length=0)),
    ("0.2.0  cut at 85 %, blunt top", dict()),
]


def middle_fin(settings):
    """(polygons in the (y, z) side plane, volume of all fins) for the 35 degree test box."""
    v, f = sc.tilted_box(tilt_deg=35)
    V, F, _ = sc.make_fins(v, f, sc.FinSettings(brim=False, crossbar=False, **settings))
    tri = V[F]
    sel = np.all(np.abs(tri[:, :, 0] - 75.0) < 2.0, axis=1)
    return tri[sel][:, :, 1:3], sc.mesh_volume(V, F)


def part_underside(ax):
    yy = np.linspace(0, 40 * np.cos(np.radians(35)), 50)
    zz = yy * np.tan(np.radians(35))
    ax.fill_between(yy, zz, zz + 5, color=PART, alpha=0.45, lw=0)
    ax.plot(yy, zz, color="#4b5563", lw=1.2)


def fig_evolution():
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.1), dpi=150, sharey=True)
    for ax, (name, kw) in zip(axes, VERSIONS):
        polys, vol = middle_fin(kw)
        part_underside(ax)
        ax.add_collection(PolyCollection(polys, facecolors=FIN, edgecolors="none"))
        ax.plot([0, 42], [0, 0], color=INK, lw=1)
        ax.set_xlim(0, 42)
        ax.set_ylim(-1, 27)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, fontsize=9.5, color=INK, loc="left")
        ax.text(1, -4.5, "5 fins: %.1f cm³ (no brim or crossbar)" % (vol / 1000), fontsize=8.5, color=MUTED)
    fig.suptitle("Figure 3. Four versions of one fin, side view, under the 35° test box", fontsize=10.5,
                 x=0.01, ha="left", color=INK)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(os.path.join(FIG, "fig03-evolution.png"), facecolor="white")
    plt.close(fig)


def fig_cost():
    # PrusaSlicer 2.7.2, fins alone, 0.2 mm layers, 0.4 mm nozzle, 2 perimeters (section 6)
    names = ["0.1.0", "0.1.1", "0.1.2", "0.2.0\nleaning back", "0.2.0"]
    metres = [2.27, 1.74, 1.76, 1.97, 1.68]
    minutes = [47.8, 42.4, 43.1, 42.3, 40.1]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), dpi=150)
    for ax, vals, unit, title in ((axes[0], metres, "m", "Filament for the fins"),
                                  (axes[1], minutes, "min", "Print time for the fins")):
        colours = [PALE] * (len(vals) - 1) + [ACCENT]
        x = np.arange(len(vals))
        ax.bar(x, vals, width=0.62, color=colours, edgecolor="white", linewidth=2)
        for xi, val in zip(x, vals):
            ax.text(xi, val + max(vals) * 0.02, ("%.2f" if unit == "m" else "%.0f") % val + " " + unit,
                    ha="center", va="bottom", fontsize=8.5, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8.5, color=INK)
        ax.set_ylim(0, max(vals) * 1.18)
        ax.set_title(title, fontsize=10, color=INK, loc="left")
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(axis="y", colors=MUTED, labelsize=8)
        ax.tick_params(axis="x", length=0)
        ax.yaxis.grid(True, color=GRID, lw=0.8)
        ax.set_axisbelow(True)
    fig.suptitle("Figure 4. What each version costs, 35° test box (PrusaSlicer 2.7.2 estimate; current default in orange)",
                 fontsize=10.5, x=0.01, ha="left", color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(FIG, "fig04-cost.png"), facecolor="white")
    plt.close(fig)


def fig_backs():
    kinds = [("vertical (default)", "vertical"), ("leaning out 20°", "slope"),
             ("round", "ellipse"), ("concave “shark”", "concave")]
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.0), dpi=150, sharey=True)
    for ax, (name, kind) in zip(axes, kinds):
        polys, vol = middle_fin(dict(back_curve=kind))
        part_underside(ax)
        ax.add_collection(PolyCollection(polys, facecolors=FIN, edgecolors="none"))
        ax.plot([0, 46], [0, 0], color=INK, lw=1)
        ax.set_xlim(0, 46)
        ax.set_ylim(-1, 25)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(name, fontsize=9.5, color=INK, loc="left")
        ax.text(1, -4.5, "5 fins: %.1f cm³" % (vol / 1000), fontsize=8.5, color=MUTED)
    fig.suptitle("Figure 9. Back-edge variants after the 85 % cut and 5 mm blunt top (all generated by the same code)",
                 fontsize=10.5, x=0.01, ha="left", color=INK)
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(os.path.join(FIG, "fig09-backs.png"), facecolor="white")
    plt.close(fig)


def fig_plan():
    """Plan view of the test box: face outline, fin lines, crossbars and pads."""
    v, f = sc.tilted_box(tilt_deg=35)
    V, F, _ = sc.make_fins(v, f, sc.FinSettings())
    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=150)
    tri = v[f]
    n, _ = sc.face_normals_areas(v, f)
    for t, nn in zip(tri, n):
        if nn[2] < -0.7:          # the base face (55 deg overhang) only
            ax.add_patch(plt.Polygon(t[:, :2], closed=True, fc=PART, ec=PART, lw=0.5, alpha=0.35))
    ftri = V[F]
    low = ftri[:, :, 2].max(axis=1) <= 0.25
    ax.add_collection(PolyCollection(ftri[low][:, :, :2], facecolors="#7c2d12", edgecolors="none", alpha=0.35))
    ax.add_collection(PolyCollection(ftri[~low][:, :, :2], facecolors=FIN, edgecolors="none"))
    ax.text(75, -1.5, "edge the box stands on (on the bed)", ha="center", va="top", fontsize=8.5, color=MUTED)
    ax.text(75, 44.5, "high edge of the face", ha="center", va="bottom", fontsize=8.5, color=MUTED)
    ax.annotate("", xy=(156, 6), xytext=(156, 30), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.text(158, 18, "downhill", rotation=90, va="center", fontsize=8.5, color=MUTED)
    ax.set_xlim(-8, 166)
    ax.set_ylim(-8, 48)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Figure 2. Plan view: the tilted base face (grey), five fins running downhill (orange), crossbar feet and "
                 "one-layer brim pads (brown)", fontsize=9.5, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig02-plan.png"), facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(FIG, exist_ok=True)
    fig_evolution()
    fig_cost()
    fig_backs()
    fig_plan()
    data = os.path.join(ROOT, "data")
    subprocess.run([sys.executable, os.path.join(HERE, "render_preview.py"), os.path.join(data, "tilted_box_35deg.stl"),
                    os.path.join(data, "tilted_box_35deg_fins.stl"), os.path.join(FIG, "fig01-test-box.png"),
                    "--zoom", "1.25"],
                   check=True)
    subprocess.run([sys.executable, os.path.join(HERE, "draw_profile.py"), os.path.join(FIG, "fig10-profile.png")], check=True)
    subprocess.run([sys.executable, os.path.join(HERE, "render_preview.py"), os.path.join(data, "box_on_corner.stl"),
                    os.path.join(data, "box_on_corner_fins.stl"), os.path.join(FIG, "fig11-corner.png"),
                    "--view", "18", "125", "--zoom", "1.35"], check=True)
    try:  # trim the 3D renders' empty margins
        from PIL import Image, ImageChops
        for name in ("fig01-test-box.png", "fig10-profile.png", "fig11-corner.png"):
            path = os.path.join(FIG, name)
            im = Image.open(path).convert("RGB")
            box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
            if box:
                l, t, r, b = box
                im.crop((max(0, l - 24), max(0, t - 24), min(im.width, r + 24), min(im.height, b + 24))).save(path)
    except ImportError:
        pass
    print("figures written to", FIG)


if __name__ == "__main__":
    main()

"""Mac lock screen and Teams backgrounds for JM², mirroring the Hoenle set
(01_Mac_Lockscreen A–E, 02_Teams T1–T5) in black / chrome."""
import math
import os
import random
import re

from build import logo_left, pearl, pearl_defs, shadow

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "wallpaper_svg")
os.makedirs(OUT, exist_ok=True)

LIGHT_BG = ("#f7f7f8", "#e9eaec")   # centre, edge
DARK_BG = ("#24262b", "#060607")


def background(w, h, dark):
    c, e = DARK_BG if dark else LIGHT_BG
    return f"""
  <radialGradient id="bg" cx="0.5" cy="0.4" r="0.75">
    <stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{e}"/>
  </radialGradient>""", f'\n  <rect width="{w}" height="{h}" fill="url(#bg)"/>'


def network(w, h, density, n, dark, seed):
    """Plexus of dots and thin lines. `density(x, y)` in 0..1 weights placement."""
    rnd = random.Random(seed)
    pts = []
    while len(pts) < n:
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        if rnd.random() < density(x / w, y / h):
            pts.append((x, y))
    col = "#c4c8ce" if dark else "#6f747b"
    unit = w / 1920
    lines, dots = [], []
    maxd = 150 * unit
    for i, (x, y) in enumerate(pts):
        near = sorted((math.dist((x, y), q), j) for j, q in enumerate(pts) if j != i)[:2]
        for d, j in near:
            if d < maxd:
                a = 0.10 + 0.25 * (1 - d / maxd)
                lines.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" '
                             f'stroke-opacity="{a:.2f}"/>')
        r = rnd.choice((1.6, 2.2, 2.8, 3.6, 4.4)) * unit
        o = rnd.uniform(0.35, 0.9)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill-opacity="{o:.2f}"/>')
        if rnd.random() < 0.05:
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*3:.1f}" fill="none" '
                        f'stroke="{col}" stroke-opacity="0.45" stroke-width="{unit:.1f}"/>')
    return (f'\n  <g stroke="{col}" stroke-width="{0.9*unit:.2f}">{"".join(lines)}</g>'
            f'\n  <g fill="{col}">{"".join(dots)}</g>')


def nested_logo(x, y, width, dark):
    """Embed the horizontal JM² logo (with tagline) at (x, y), given width."""
    svg = logo_left(dark=dark)
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    inner = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return (f'\n  <svg x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{width*vh/vw:.1f}" '
            f'viewBox="0 0 {vw:.0f} {vh:.0f}">{inner}</svg>'), width * vh / vw


def big_pearl(cx, cy, d, with_shadow):
    s = pearl("w", cx - d / 2, cy - d / 2, d)
    if with_shadow:
        s += shadow("w", cx, cy + d / 2 + d * 0.12, d * 0.44)
    return s


def chip(x, y, w, h):
    """Light rounded plate behind the logo (Teams T5)."""
    return (f'\n  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h*0.26:.0f}" fill="#e2e4e7" '
            f'fill-opacity="0.96"/>')


def page(w, h, dark, parts, extra_defs=""):
    defs, bg = background(w, h, dark)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'\n<defs>{defs}{pearl_defs("w", dark)}{extra_defs}\n</defs>{bg}{"".join(parts)}\n</svg>\n')


# density helpers (x, y normalised 0..1)
def ring_around(cx, cy, r0, r1):
    return lambda x, y: 1.0 if r0 < math.hypot((x - cx) * 1.78, y - cy) < r1 else 0.08


def cloud(cx, cy, r):
    return lambda x, y: max(0.03, 1 - math.hypot((x - cx) * 1.78, y - cy) / r)


def edges(x, y):
    return 1.0 if min(x, 1 - x) < 0.2 or y < 0.12 or y > 0.85 else 0.04


def build():
    out = []
    # --- Mac lock screens (5120×2880) ---
    W, H = 5120, 2880
    out.append(("JM2_Mac_A_Dunkel_Perle_zentral", W, H, True, [
        network(W, H, ring_around(0.5, 0.38, 0.12, 0.62), 380, True, 1),
        big_pearl(W * 0.5, H * 0.36, H * 0.48, False)]))
    out.append(("JM2_Mac_B_Dunkel_Perle_rechts", W, H, True, [
        network(W, H, ring_around(0.62, 0.42, 0.1, 0.62), 380, True, 2),
        big_pearl(W * 0.62, H * 0.36, H * 0.48, False)]))
    out.append(("JM2_Mac_C_Hell_Perle_zentral", W, H, False, [
        network(W, H, ring_around(0.5, 0.4, 0.12, 0.6), 380, False, 3),
        big_pearl(W * 0.5, H * 0.36, H * 0.46, True)]))
    lg, lh = nested_logo(W * 0.5 - W * 0.17, H * 0.28, W * 0.34, False)
    out.append(("JM2_Mac_D_Hell_Logo_klein", W, H, False, [
        network(W, H, cloud(0.5, 0.5, 0.95), 330, False, 4), lg]))
    lg, lh = nested_logo(W * 0.5 - W * 0.13, H * 0.70, W * 0.26, False)
    out.append(("JM2_Mac_E_Hell_Logo_unten", W, H, False, [
        network(W, H, cloud(0.4, 0.38, 0.55), 320, False, 5), lg]))

    # --- Teams backgrounds (1920×1080) ---
    W, H = 1920, 1080
    lg, _ = nested_logo(80, 900, 300, False)
    out.append(("JM2_Teams_T1_Hell_Logo_links", W, H, False, [network(W, H, edges, 150, False, 11), lg]))
    lg, _ = nested_logo(80, 900, 300, False)
    out.append(("JM2_Teams_T2_Hell_Perle_Logo", W, H, False, [
        network(W, H, edges, 150, False, 12), big_pearl(1560, 420, 340, True), lg]))
    lg, _ = nested_logo(W - 380, 900, 300, False)
    out.append(("JM2_Teams_T3_Hell_Logo_rechts", W, H, False, [network(W, H, edges, 150, False, 13), lg]))
    out.append(("JM2_Teams_T4_Dunkel_Perle", W, H, True, [
        network(W, H, edges, 150, True, 14), big_pearl(1520, 410, 420, False)]))
    lg, _ = nested_logo(150, 850, 360, False)
    out.append(("JM2_Teams_T5_Dunkel_Logo_Chip", W, H, True, [
        network(W, H, edges, 150, True, 15), chip(110, 815, 440, 190), lg]))

    for name, w, h, dark, parts in out:
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(page(w, h, dark, parts))
        print("wrote", name)


if __name__ == "__main__":
    build()

"""Generate the JM² logo set (SVG) from the Hoenle Medical layout.

Text is converted to outlines so the SVGs render identically everywhere.
Fonts: Unbounded (wordmark, same family as the hoenle medical logo) and
Newsreader Light (tagline). Both are SIL Open Font License.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "..", "svg")
os.makedirs(OUT, exist_ok=True)

# Palette: black body, chrome / dark silver accents
INK = "#0b0b0d"          # primary black
INK_SOFT = "#1d1f23"     # sphere depth
SILVER_DARK = "#5f646c"  # dark silver
SILVER = "#9aa0a8"
CHROME = "#e4e7eb"
TAGLINE = "#8a8e94"      # same grey role as the hoenle tagline
WHITE = "#f4f5f7"


class Font:
    def __init__(self, file):
        self.tt = TTFont(os.path.join(FONTS, file))
        self.upm = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.hmtx = self.tt["hmtx"]

    def path(self, text, size, x, y, tracking=0):
        """Outline `text` with baseline at (x, y). Returns (d, advance)."""
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        cx = 0
        for ch in text:
            g = self.cmap[ord(ch)]
            tp = TransformPen(pen, (s, 0, 0, -s, x + cx, y))
            self.gs[g].draw(tp)
            cx += self.hmtx[g][0] * s + tracking
        return pen.getCommands(), cx - tracking

    def bounds(self, ch, size):
        bp = BoundsPen(self.gs)
        self.gs[self.cmap[ord(ch)]].draw(bp)
        s = size / self.upm
        return tuple(v * s for v in bp.bounds)


BOLD = Font("unb700.ttf")
REG = Font("unb500.ttf")
SERIF = Font("news300.ttf")
CAP = 0.75  # Unbounded cap height / em


def pearl_defs(p, dark_bg=False):
    """Gradients for the pearl. `p` prefixes ids so several logos can share a page."""
    return f"""
  <linearGradient id="{p}ring" x1="0" y1="0" x2="1" y2="0.25">
    <stop offset="0" stop-color="{CHROME}"/>
    <stop offset="0.45" stop-color="{SILVER}"/>
    <stop offset="1" stop-color="{SILVER_DARK}"/>
  </linearGradient>
  <linearGradient id="{p}wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#c9cdd2"/>
    <stop offset="0.5" stop-color="{SILVER}"/>
    <stop offset="1" stop-color="{SILVER_DARK}"/>
  </linearGradient>
  <radialGradient id="{p}body" cx="0.38" cy="0.32" r="0.8">
    <stop offset="0" stop-color="{INK_SOFT}"/>
    <stop offset="1" stop-color="{INK}"/>
  </radialGradient>
  <radialGradient id="{p}hl">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0.96"/>
    <stop offset="0.45" stop-color="#eef0f2" stop-opacity="0.9"/>
    <stop offset="1" stop-color="#eef0f2" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{p}hl2">
    <stop offset="0" stop-color="{SILVER}" stop-opacity="0.95"/>
    <stop offset="0.5" stop-color="{SILVER}" stop-opacity="0.75"/>
    <stop offset="1" stop-color="{SILVER}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{p}shadow">
    <stop offset="0" stop-color="{SILVER if dark_bg else INK}" stop-opacity="{0.55 if dark_bg else 0.9}"/>
    <stop offset="0.7" stop-color="{SILVER if dark_bg else INK}" stop-opacity="{0.25 if dark_bg else 0.45}"/>
    <stop offset="1" stop-color="{SILVER if dark_bg else INK}" stop-opacity="0"/>
  </radialGradient>"""


def pearl(p, x, y, d):
    """Pearl mark scaled to diameter `d` (incl. ring), top-left at (x, y).
    Drawn in a 1600-unit box; the shadow sits below at ~y=1760."""
    k = d / 1600
    return f"""
  <g transform="translate({x:.2f} {y:.2f}) scale({k:.5f})">
    <circle cx="800" cy="800" r="800" fill="url(#{p}ring)"/>
    <circle cx="788" cy="803" r="760" fill="url(#{p}body)"/>
    <ellipse cx="470" cy="470" rx="245" ry="250" fill="url(#{p}hl)"/>
    <ellipse cx="1215" cy="480" rx="120" ry="330" transform="rotate(-38 1215 480)" fill="url(#{p}hl)"/>
    <ellipse cx="385" cy="975" rx="130" ry="140" fill="url(#{p}hl2)"/>
    <path fill="url(#{p}wave)" d="M240 1330 C 400 1450 640 1480 760 1440 C 880 1400 900 1290 960 1200
      C 1040 1080 1160 1040 1300 1020 C 1400 1005 1450 1000 1500 930 C 1550 860 1560 760 1545 690
      C 1560 760 1555 900 1520 980 C 1440 1160 1250 1300 1050 1400 C 820 1515 560 1500 385 1440 Z"/>
  </g>"""


def shadow(p, cx, cy, rx):
    return f'\n  <ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{rx*0.115:.2f}" fill="url(#{p}shadow)"/>'


def wordmark(x, baseline, cap_h, color, sup_color):
    """'JM' + superscript '2'. Returns (svg, width)."""
    size = cap_h / CAP
    d, w = BOLD.path("JM", size, x, baseline, tracking=size * 0.01)
    sup_size = size * 0.52
    gap = size * 0.05
    # superscript top aligned with the cap height, like m²
    sup_base = baseline - cap_h + sup_size * CAP
    d2, w2 = BOLD.path("2", sup_size, x + w + gap, sup_base)
    svg = f'\n  <path fill="{color}" d="{d}"/>\n  <path fill="{sup_color}" d="{d2}"/>'
    return svg, w + gap + w2


def tagline(x, baseline, size, color, anchor="start"):
    text = "a eurocept homecare company"
    _, w = SERIF.path(text, size, 0, 0)
    if anchor == "middle":
        x -= w / 2
    d, w = SERIF.path(text, size, x, baseline)
    return f'\n  <path fill="{color}" d="{d}"/>', w


def doc(w, h, body, defs, bg=None):
    bgr = f'\n  <rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">\n<defs>{defs}\n</defs>{bgr}{body}\n</svg>\n')


def colors(dark):
    return (WHITE, SILVER) if dark else (INK, SILVER_DARK)


def logo_left(dark=False, with_tagline=True, bg=None):
    p = "d" if dark else "l"
    D = 1000                     # pearl diameter
    cap = 540                    # JM cap height
    tx = D + 200                 # text start
    top = 40
    body = pearl(p, 40, top, D) + shadow(p, 40 + D / 2, top + D + 150, D * 0.46)
    ink, sup = colors(dark)
    baseline = top + D * (0.80 if with_tagline else 0.5) + (0 if with_tagline else cap * 0.5)
    wm, ww = wordmark(tx, baseline, cap, ink, sup)
    body += wm
    width = tx + ww
    h = top + D + 150 + D * 0.46 * 0.115 + 40
    if with_tagline:
        tg, tw = tagline(tx, top + D + 150 + 25, 150, TAGLINE)
        body += tg
        width = max(width, tx + tw)
    return doc(width + 60, h, body, pearl_defs(p, dark), bg)


def logo_center(dark=False, with_tagline=True, bg=None):
    p = "d" if dark else "l"
    D = 1000
    cap = 520
    ink, sup = colors(dark)
    _, ww = wordmark(0, 0, cap, ink, sup)
    _, tw = tagline(0, 0, 150, TAGLINE)
    W = max(D, ww, tw if with_tagline else 0) + 160
    cx = W / 2
    body = pearl(p, cx - D / 2, 60, D) + shadow(p, cx, 60 + D + 150, D * 0.46)
    baseline = 60 + D + 150 + 200 + cap
    wm, _ = wordmark(cx - ww / 2, baseline, cap, ink, sup)
    body += wm
    h = baseline + 80
    if with_tagline:
        tg, _ = tagline(cx, baseline + 260, 150, TAGLINE, anchor="middle")
        body += tg
        h = baseline + 330
    return doc(W, h, body, pearl_defs(p, dark), bg)


def pearl_only(dark=False):
    p = "d" if dark else "l"
    D = 1000
    body = pearl(p, 40, 40, D) + shadow(p, 40 + D / 2, 40 + D + 150, D * 0.46)
    return doc(D + 80, D + 150 + 40 + D * 0.46 * 0.115 + 40, body, pearl_defs(p, dark))


def app_icon(size=1024):
    """Square icon: pearl on black, e.g. for Teams / Slack / favicon."""
    p = "i"
    D = size * 0.74
    body = pearl(p, (size - D) / 2, (size - D) / 2, D)
    return doc(size, size, body, pearl_defs(p, True), INK)


FILES = {
    "JM2_payoff_left_rgb.svg": logo_left(),
    "JM2_left_notagline_rgb.svg": logo_left(with_tagline=False),
    "JM2_center_rgb.svg": logo_center(with_tagline=False),
    "JM2_payoff_center_rgb.svg": logo_center(),
    "JM2_pearl_rgb.svg": pearl_only(),
    "JM2_payoff_left_dark_rgb.svg": logo_left(dark=True),
    "JM2_payoff_center_dark_rgb.svg": logo_center(dark=True),
    "JM2_pearl_dark_rgb.svg": pearl_only(dark=True),
    "JM2_icon_1024.svg": app_icon(),
}

if __name__ == "__main__":
    for name, svg in FILES.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        print("wrote", name)

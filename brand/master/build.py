#!/usr/bin/env python3
"""Build the master logo set (SVG + PNG) for b, bWalletX, bChatX and bMintX.

One geometry, one script. Every file in brand/master/ comes from here, so nobody draws a
rough copy by hand again. Run from anywhere:  python3 brand/master/build.py
Needs rsvg-convert and magick (Homebrew: librsvg, imagemagick).

The b (unchanged from brand/bwalletx-mark.svg, owner-approved, 23 Oct 2026), 120-unit grid:
  stem   x 27..45 (18 wide), top cut at 45 deg from (27,30) to (45,12)
  bowl   circle (60,72) r33, counter r15 -> bowl stroke 18 = stem width
  join   the stem's left edge x=27 is the bowl's leftmost point (cx - r), so the outline
         runs straight into the arc with no step. The stem's right edge x=45 is tangent to
         the counter (cx - 15). Drawn as ONE unioned path with an even-odd counter: no masks,
         no overlapping shapes, nothing to misalign at 4096px.
"""
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# One path for the letter. (45, 42.606) is where x=45 meets the bowl: 72 - sqrt(33^2 - 15^2).
B_PATH = (
    "M27 30L45 12V42.606A33 33 0 1 1 27 72Z"
    "M60 57A15 15 0 1 0 60 87A15 15 0 1 0 60 57Z"
)
LETTER_BOX = "23 8 74 100"   # tight box around the letter, 2-unit margin
TILE_BOX = "-4 4 120 120"    # square box, letter optically centred at (56,64)
CX, CY = 56, 64

# Colour ramps: top, middle (= flat colour), bottom. From brand/ and brand/family/ (23 Oct 2026).
BRANDS = {
    "b":        {"name": "b",        "ramp": ("#FFE58A", "#FFD24D", "#C98F00")},
    "bwalletx": {"name": "bWalletX", "ramp": ("#FFE58A", "#FFD24D", "#C98F00")},
    "bchatx":   {"name": "bChatX",   "ramp": ("#DEE1E7", "#C9CED8", "#898C93")},
    "bmintx":   {"name": "bMintX",   "ramp": ("#76E4C0", "#22D39A", "#178F69")},
}
GROUND_DARK = "#000000"
GROUND_LIGHT = "#F4F4F2"
INK_DARK = "#0A0A0A"

# Scale of the letter inside each container (share of the 120-unit square).
SCALE = {"icon": 0.74, "avatar": 0.68, "maskable": 0.60, "favicon": 0.86}
TILE_RX = 26.4  # 22% of 120


def grad(ramp):
    t, m, b = ramp
    return (
        '<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="12" x2="0" y2="105">'
        f'<stop offset="0" stop-color="{t}"/><stop offset=".55" stop-color="{m}"/>'
        f'<stop offset="1" stop-color="{b}"/></linearGradient>'
    )


def letter(fill, scale=None):
    p = f'<path fill="{fill}" fill-rule="evenodd" d="{B_PATH}"/>'
    if scale is None:
        return p
    return f'<g transform="translate({CX} {CY}) scale({scale}) translate({-CX} {-CY})">{p}</g>'


def svg(box, label, body, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="{label}">{d}{body}</svg>\n'


def variants(slug, spec):
    n, ramp = spec["name"], spec["ramp"]
    g = grad(ramp)
    sq = '<rect x="-4" y="4" width="120" height="120" fill="{}"/>'
    tile = '<rect x="-4" y="4" width="120" height="120" rx="%s" fill="{}"/>' % TILE_RX
    circ = '<circle cx="56" cy="64" r="60" fill="{}"/>'
    return {
        # bare letter (pages, extension icon, anywhere the ground is already dark)
        f"{slug}-mark.svg": svg(LETTER_BOX, n, letter("url(#g)"), g),
        f"{slug}-mark-flat.svg": svg(LETTER_BOX, n, letter(ramp[1])),
        f"{slug}-mark-white.svg": svg(LETTER_BOX, n, letter("#FFFFFF")),
        f"{slug}-mark-black.svg": svg(LETTER_BOX, n, letter(INK_DARK)),
        # tiles
        f"{slug}-icon.svg": svg(TILE_BOX, n, tile.format(GROUND_DARK) + letter("url(#g)", SCALE["icon"]), g),
        f"{slug}-icon-light.svg": svg(TILE_BOX, n, tile.format(GROUND_LIGHT) + letter(INK_DARK, SCALE["icon"])),
        f"{slug}-icon-square.svg": svg(TILE_BOX, n, sq.format(GROUND_DARK) + letter("url(#g)", SCALE["icon"]), g),
        f"{slug}-avatar.svg": svg(TILE_BOX, n, circ.format(GROUND_DARK) + letter("url(#g)", SCALE["avatar"]), g),
        f"{slug}-maskable.svg": svg(TILE_BOX, n, sq.format(GROUND_DARK) + letter("url(#g)", SCALE["maskable"]), g),
        f"{slug}-adaptive-foreground.svg": svg(TILE_BOX, n, letter("url(#g)", SCALE["maskable"]), g),
        f"{slug}-favicon.svg": svg(TILE_BOX, n, tile.format(GROUND_DARK) + letter("url(#g)", SCALE["favicon"]), g),
    }


def render(src, out, size, opaque=False):
    subprocess.run(["rsvg-convert", "-a", "-w", str(size), "-h", str(size), "-o", out, src], check=True)
    if src.endswith("-mark.svg"):  # letter box is 74x100: centre it on a square transparent canvas
        subprocess.run(["magick", out, "-background", "none", "-gravity", "center",
                        "-extent", f"{size}x{size}", out], check=True)
    if opaque:
        subprocess.run(["magick", out, "-background", GROUND_DARK, "-alpha", "remove", "-alpha", "off", out], check=True)


IOS_SIZES = [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024]
SIZES = [1024, 512, 400, 256, 180, 128, 48, 32, 16]


def build(slug, spec):
    d = os.path.join(HERE, slug)
    shutil.rmtree(d, ignore_errors=True)
    png = os.path.join(d, "png")
    os.makedirs(png)
    for fn, body in variants(slug, spec).items():
        with open(os.path.join(d, fn), "w") as f:
            f.write(body)
    p = lambda fn: os.path.join(d, fn)
    for s in SIZES:
        # rounded tile with transparent corners: general app/web icon
        render(p(f"{slug}-icon.svg"), os.path.join(png, f"{slug}-icon-{s}.png"), s)
        # square, opaque: apple-touch (180), X app + profile (400), stores (1024)
        render(p(f"{slug}-icon-square.svg"), os.path.join(png, f"{slug}-square-{s}.png"), s, opaque=True)
        # bare letter on transparent: extension toolbar, overlays
        render(p(f"{slug}-mark.svg"), os.path.join(png, f"{slug}-mark-{s}.png"), s)
        render(p(f"{slug}-avatar.svg"), os.path.join(png, f"{slug}-avatar-{s}.png"), s)
    for s in (16, 32, 48):
        render(p(f"{slug}-favicon.svg"), os.path.join(png, f"{slug}-favicon-{s}.png"), s)
    subprocess.run(["magick"] + [os.path.join(png, f"{slug}-favicon-{s}.png") for s in (16, 32, 48)]
                   + [p(f"{slug}-favicon.ico")], check=True)
    # Android: PWA maskable + adaptive icon layers (108dp at xxxhdpi = 432px)
    for s in (192, 512):
        render(p(f"{slug}-maskable.svg"), os.path.join(png, f"{slug}-maskable-{s}.png"), s, opaque=True)
    render(p(f"{slug}-adaptive-foreground.svg"), os.path.join(png, f"{slug}-adaptive-foreground-432.png"), 432)
    subprocess.run(["magick", "-size", "432x432", f"xc:{GROUND_DARK}", os.path.join(png, f"{slug}-adaptive-background-432.png")], check=True)
    # iOS app icon set: opaque, square (iOS rounds the corners itself)
    ios = os.path.join(d, "ios", "AppIcon.appiconset")
    os.makedirs(ios)
    for s in IOS_SIZES:
        render(p(f"{slug}-icon-square.svg"), os.path.join(ios, f"icon-{s}.png"), s, opaque=True)
    with open(os.path.join(ios, "Contents.json"), "w") as f:
        f.write('{\n  "images" : [\n    { "filename" : "icon-1024.png", "idiom" : "universal", "platform" : "ios", "size" : "1024x1024" }\n'
                '  ],\n  "info" : { "author" : "xcode", "version" : 1 }\n}\n')
    # X / Twitter: the 400x400 to upload for the X developer app and the profile picture
    shutil.copy(os.path.join(png, f"{slug}-square-400.png"), p(f"{slug}-x-app-400.png"))


if __name__ == "__main__":
    for slug, spec in BRANDS.items():
        build(slug, spec)
        print("built", slug)

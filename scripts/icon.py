#!/usr/bin/env python3
"""Metro icon builder + linter. The skill ships a grammar, not an icon set: describe any glyph with a few
primitives on a 20x20 grid and this renders the ring-and-glyph SVG, or lints an SVG you drew yourself.

  icon.py render spec.json out.svg [--size 44] [--no-ring]
  icon.py lint   icon.svg

spec.json:  {"name":"mail","shapes":[
    {"t":"rect","x":2,"y":5,"w":16,"h":10},
    {"t":"poly","pts":[[2,5],[10,11],[18,5]]},
    {"t":"line","x1":3,"y1":4,"x2":17,"y2":4},
    {"t":"arc","cx":10,"cy":10,"r":6,"a0":200,"a1":340},      # degrees, 0 = +x axis, clockwise (SVG y down)
    {"t":"circle","cx":10,"cy":10,"r":2,"fill":true},
    {"t":"path","d":"M2 2L18 18"}]}
Rules enforced: white on transparent, stroke 2 (ring 2.2), round caps/joins, fills only solid white,
every coordinate inside the 0..20 glyph box, no gradients/opacity/filters.
"""
import sys, json, math, re

RING_R, RING_STROKE, STROKE, BOX = 20.9, 2.2, 2.0, 20.0

def _el(s):
    t = s["t"]; fill = "#fff" if s.get("fill") else "none"
    a = f'fill="{fill}" stroke="#fff" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round"'
    if fill != "none": a = 'fill="#fff" stroke="none"'
    if t == "line": return f'<line x1="{s["x1"]}" y1="{s["y1"]}" x2="{s["x2"]}" y2="{s["y2"]}" {a}/>'
    if t == "rect": return f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["w"]}" height="{s["h"]}" {a}/>'
    if t == "circle": return f'<circle cx="{s["cx"]}" cy="{s["cy"]}" r="{s["r"]}" {a}/>'
    if t == "poly":
        pts = " ".join(f"{x},{y}" for x, y in s["pts"]); tag = "polygon" if s.get("close") else "polyline"
        return f'<{tag} points="{pts}" {a}/>'
    if t == "arc":
        cx, cy, r = s["cx"], s["cy"], s["r"]; a0, a1 = math.radians(s["a0"]), math.radians(s["a1"])
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if (s["a1"] - s["a0"]) % 360 > 180 else 0
        return f'<path d="M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}" {a}/>'
    if t == "path": return f'<path d="{s["d"]}" {a}/>'
    raise SystemExit(f"unknown primitive {t}")

def render(spec, size=44, ring=True):
    g = "".join(_el(s) for s in spec["shapes"])
    r = f'<circle r="{RING_R}" fill="none" stroke="#fff" stroke-width="{RING_STROKE}"/>' if ring else ""
    half = 22 if ring else BOX / 2 + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="{-half} {-half} {2*half} {2*half}">'
            f'{r}<g transform="translate({-BOX/2} {-BOX/2})">{g}</g></svg>\n')

def lint(svg):
    bad = []
    for rx, msg in [(r"gradient|filter|opacity|mask", "gradient/filter/opacity not allowed"),
                    (r'(?:fill|stroke)="(?!none|#fff|#ffffff|white|currentColor)[^"]+"', "colour must be white/currentColor"),
                    (r'stroke-linecap="(?!round)', "linecap must be round"),
                    (r'stroke-linejoin="(?!round)', "linejoin must be round")]:
        if re.search(rx, svg, re.I): bad.append(msg)
    for w in re.findall(r'stroke-width="([\d.]+)"', svg):
        if float(w) not in (STROKE, RING_STROKE): bad.append(f"stroke-width {w} (use {STROKE}; ring {RING_STROKE})")
    return sorted(set(bad))

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "render":
        spec = json.load(open(a[1])); size = int(a[a.index("--size") + 1]) if "--size" in a else 44
        svg = render(spec, size, "--no-ring" not in a)
        issues = lint(svg)
        if issues: sys.exit("lint: " + "; ".join(issues))
        open(a[2], "w").write(svg); print("ok", a[2])
    elif len(a) == 2 and a[0] == "lint":
        issues = lint(open(a[1]).read()); print("clean" if not issues else "\n".join(issues)); sys.exit(1 if issues else 0)
    else:
        print(__doc__); sys.exit(2)

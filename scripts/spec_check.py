#!/usr/bin/env python3
"""Check a render against a reference band spec (numbers only, no reference image needed).

usage: spec_check.py render.png evals/specs/<name>.json [--tol 1.0]
Prints, per reference band, the vertical (dy) and horizontal (dx) error in CSS px of the nearest band in your
render, plus a pass/fail verdict: pass = every band within --tol (default 1.0) and none missing/extra.
Exit code 0 pass, 1 fail, 3 wrong image size.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare as C

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 1.0
    if "--tol" in sys.argv: a = [x for x in a if x != str(tol) and x != sys.argv[sys.argv.index("--tol") + 1]]
    if len(a) != 2: print(__doc__); sys.exit(2)
    spec = json.load(open(a[1])); im = C.load(a[0])
    W, H = spec["size_css"]
    if im.size != (W * 4, H * 4):
        print(f"ERROR: render is {im.size[0]}x{im.size[1]}, spec expects {W*4}x{H*4} (capture {W}x{H} CSS px at scale 4)"); sys.exit(3)
    m = C.ink_mask(im); cb = C.bands_from_profile(C.row_profile(m))
    sb = spec["bands"]; bad, rows, used = 0, [], set()
    # a render band that swallows several spec bands (two lines closer than the split gap) is compared by its outer edges
    owner = {}
    for i, b in enumerate(sb):
        tc = (b["y"] + b["h"] / 2) * 4
        inside = [j for j, (c0, c1) in enumerate(cb) if c0 - 8 <= tc <= c1 + 8]
        owner[i] = inside[0] if inside else None
    groups = {}
    for i, j in owner.items(): groups.setdefault(j, []).append(i)
    for i, b in enumerate(sb):
        j = owner[i]
        if j is None:
            rows.append(f"  y={b['y']:>6} h={b['h']:>5}  MISSING"); bad += 1; continue
        used.add(j); c0, c1 = cb[j]; bx = C.band_box(m, c0, c1); g = groups[j]
        top = b["y"] if i == g[0] else None; bot = (b["y"] + b["h"]) if i == g[-1] else None
        if len(g) > 1 and i != g[0] and i != g[-1]:
            rows.append(f"  y={b['y']:>6} h={b['h']:>5}  (merged with neighbours in your render)  ok"); continue
        dy = round(c0 / 4 - b["y"], 1) if top is not None else round((c1 + 1) / 4 - bot, 1)
        dh = round((c1 - c0 + 1) / 4 - b["h"], 1) if len(g) == 1 else 0.0
        dxl = round(bx[0] / 4 - b["x0"], 1) if bx else 0; dxr = round(bx[1] / 4 - b["x1"], 1) if bx else 0
        ok = abs(dy) <= tol and abs(dxl) <= tol + 0.5 and (abs(dxr) <= tol + 0.5 or len(g) > 1)
        bad += 0 if ok else 1
        rows.append(f"  y={b['y']:>6} h={b['h']:>5}  dy={dy:>+5} dh={dh:>+5} dx_l={dxl:>+5} dx_r={dxr:>+5}  {'ok' if ok else 'FIX'}")
    extra = len(cb) - len(used)
    print("\n".join(rows)); print(f"extra bands in render: {extra}")
    print("PASS" if not bad and not extra else f"FAIL ({bad} bands off, {extra} extra)")
    sys.exit(0 if not bad and not extra else 1)
main()

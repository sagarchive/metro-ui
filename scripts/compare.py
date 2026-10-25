#!/usr/bin/env python3
"""Compare a candidate Metro screenshot against ground truth, with ACTIONABLE feedback.

usage: compare.py candidate.png truth.png [--out DIR] [--json]

Both images are expected at the Metro reference geometry (1440x2960 = 360 CSS px x 4.0).
Reports (all positions in CSS px = pixels / 3.2):
  score          0..100 composite (higher is better)
  ssim           structural similarity on a 180px-wide grayscale downsample
  ink_iou        overlap of 'ink' (non-black) regions, 1px tolerance
  colour         Jaccard-ish match of the dominant non-black colours
  bands          every horizontal text/graphic band in the truth, matched to the nearest band
                 in the candidate: dy_top, dy_bottom, height delta, dx_left, dx_right
  drift          best global vertical shift that would align the candidate (+ = candidate is lower)
Writes DIR/compare.png : candidate | truth | difference heat-map (+ bands overlay).
Pure Pillow, no numpy.
"""
import sys, json, os, math, warnings
warnings.filterwarnings("ignore")
from PIL import Image, ImageChops, ImageDraw, ImageFilter

SCALE = 4.0           # px per CSS px (=pt) at the reference geometry: 1440px / 360pt
INK = 40              # luminance above this = ink

def load(p):
    return Image.open(p).convert("RGB")

def ink_mask(im, thr=INK):
    return im.convert("L").point(lambda v: 255 if v > thr else 0)

def row_profile(mask):
    w, h = mask.size
    prof = mask.resize((1, h), Image.BOX)           # average of each row
    return list(prof.tobytes())

def bands_from_profile(prof, min_h=3, gap=6):
    """consecutive rows with any ink -> [(y0,y1)], merging gaps smaller than `gap` px"""
    rows = [i for i, v in enumerate(prof) if v > 0]
    out = []
    for y in rows:
        if out and y - out[-1][1] <= gap:
            out[-1][1] = y
        else:
            out.append([y, y])
    return [(a, b) for a, b in out if b - a + 1 >= min_h]

def band_box(mask, y0, y1):
    box = mask.crop((0, y0, mask.size[0], y1 + 1)).getbbox()
    if not box:
        return None
    return box[0], box[2]       # x0, x1

def ssim(a, b, win=7, step=3):
    """mean SSIM of two equal-size 'L' images (pure python, small images only)"""
    w, h = a.size
    pa, pb = a.load(), b.load()
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    tot, n = 0.0, 0
    for y in range(0, h - win, step):
        for x in range(0, w - win, step):
            sa = sb = saa = sbb = sab = 0
            for j in range(win):
                for i in range(win):
                    va, vb = pa[x + i, y + j], pb[x + i, y + j]
                    sa += va; sb += vb
                    saa += va * va; sbb += vb * vb; sab += va * vb
            N = win * win
            ma, mb = sa / N, sb / N
            va_, vb_ = saa / N - ma * ma, sbb / N - mb * mb
            cov = sab / N - ma * mb
            tot += ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma * ma + mb * mb + c1) * (va_ + vb_ + c2))
            n += 1
    return tot / max(n, 1)

def dominant_colours(im, k=8, q=24):
    small = im.resize((180, int(180 * im.size[1] / im.size[0])), Image.BOX)
    cnt = {}
    for px in small.getdata():
        if max(px) < INK:
            continue
        key = tuple((c // q) * q + q // 2 for c in px)
        cnt[key] = cnt.get(key, 0) + 1
    top = sorted(cnt.items(), key=lambda kv: -kv[1])[:k]
    tot = sum(v for _, v in top) or 1
    return {kk: v / tot for kk, v in top}

def colour_score(ca, cb):
    keys = set(ca) | set(cb)
    if not keys:
        return 1.0
    inter = sum(min(ca.get(k, 0), cb.get(k, 0)) for k in keys)
    return inter / sum(max(ca.get(k, 0), cb.get(k, 0)) for k in keys)

def best_shift(pa, pb, maxs=120):
    best, bs = None, 0
    n = min(len(pa), len(pb))
    for s in range(-maxs, maxs + 1, 2):
        err = 0
        for y in range(max(0, s), min(n, n + s)):
            err += abs(pa[y] - pb[y - s])
        if best is None or err < best:
            best, bs = err, s
    return bs / SCALE

def match_bands(cb, tb, cmask, tmask):
    res = []
    used = set()
    for (t0, t1) in tb:
        tc = (t0 + t1) / 2
        best, bi = None, None
        for i, (c0, c1) in enumerate(cb):
            if i in used:
                continue
            d = abs((c0 + c1) / 2 - tc)
            if best is None or d < best:
                best, bi = d, i
        tx = band_box(tmask, t0, t1)
        if bi is None:
            res.append(dict(truth_y=round(t0 / SCALE, 1), truth_h=round((t1 - t0 + 1) / SCALE, 1), missing=True))
            continue
        used.add(bi)
        c0, c1 = cb[bi]
        cx = band_box(cmask, c0, c1)
        r = dict(truth_y=round(t0 / SCALE, 1), truth_h=round((t1 - t0 + 1) / SCALE, 1),
                 dy_top=round((c0 - t0) / SCALE, 1), dy_bottom=round((c1 - t1) / SCALE, 1),
                 dh=round(((c1 - c0) - (t1 - t0)) / SCALE, 1))
        if tx and cx:
            r["dx_left"] = round((cx[0] - tx[0]) / SCALE, 1)
            r["dx_right"] = round((cx[1] - tx[1]) / SCALE, 1)
        res.append(r)
    extra = [dict(cand_y=round(cb[i][0] / SCALE, 1), cand_h=round((cb[i][1] - cb[i][0] + 1) / SCALE, 1), extra=True)
             for i in range(len(cb)) if i not in used]
    return res, extra

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    out_dir = None
    if "--out" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out") + 1]
        args = [a for a in args if a != out_dir]
    if len(args) < 2:
        print(__doc__); sys.exit(2)
    cand, truth = load(args[0]), load(args[1])
    note = None
    if cand.size != truth.size:
        if "--resize" not in flags:
            print(f"ERROR: candidate is {cand.size[0]}x{cand.size[1]} but truth is {truth.size[0]}x{truth.size[1]}. "
                  "Capture at 360 CSS px wide with device scale factor 4 (scripts/capture.sh), or pass --resize.", file=sys.stderr)
            sys.exit(3)
        note = f"candidate size {cand.size} != truth {truth.size}: resized"
        cand = cand.resize(truth.size, Image.LANCZOS)

    W = 180
    H = int(W * truth.size[1] / truth.size[0])
    cs = cand.resize((W, H), Image.BOX).convert("L")
    ts = truth.resize((W, H), Image.BOX).convert("L")
    s = ssim(cs, ts)

    cm, tm = ink_mask(cand), ink_mask(truth)
    cmd = cm.resize((W, H), Image.BOX).filter(ImageFilter.MaxFilter(3)).point(lambda v: 255 if v > 0 else 0)
    tmd = tm.resize((W, H), Image.BOX).filter(ImageFilter.MaxFilter(3)).point(lambda v: 255 if v > 0 else 0)
    inter = ImageChops.logical_and(cmd.convert("1"), tmd.convert("1")).convert("L")
    union = ImageChops.logical_or(cmd.convert("1"), tmd.convert("1")).convert("L")
    ni = sum(1 for v in inter.getdata() if v); nu = sum(1 for v in union.getdata() if v) or 1
    iou = ni / nu

    col = colour_score(dominant_colours(cand), dominant_colours(truth))

    cprof, tprof = row_profile(cm), row_profile(tm)
    cb, tb = bands_from_profile(cprof), bands_from_profile(tprof)
    matched, extra = match_bands(cb, tb, cm, tm)
    drift = best_shift(cprof, tprof)

    dy = [abs(m["dy_top"]) for m in matched if "dy_top" in m]
    missing = sum(1 for m in matched if m.get("missing"))
    band_pen = (sum(min(d, 12) for d in dy) / max(len(dy), 1)) / 12 if dy else 1.0
    band_pen = min(1.0, band_pen + missing / max(len(tb), 1) * 0.5 + len(extra) / max(len(tb), 1) * 0.25)

    score = 100 * (0.35 * max(s, 0) + 0.25 * iou + 0.15 * col + 0.25 * (1 - band_pen))

    report = dict(score=round(score, 1), ssim=round(s, 3), ink_iou=round(iou, 3), colour=round(col, 3),
                  drift_css_px=round(drift, 1), n_truth_bands=len(tb), n_cand_bands=len(cb),
                  missing_bands=missing, extra_bands=len(extra), bands=matched, extra=extra, note=note)

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        sw = 480; sh = int(sw * truth.size[1] / truth.size[0])
        a = cand.resize((sw, sh), Image.LANCZOS); b = truth.resize((sw, sh), Image.LANCZOS)
        d = ImageChops.difference(a, b).convert("L").point(lambda v: min(255, v * 3))
        heat = Image.merge("RGB", (d, d.point(lambda v: v // 3), d.point(lambda v: v // 3)))
        sheet = Image.new("RGB", (sw * 3 + 20, sh), (50, 50, 50))
        sheet.paste(a, (0, 0)); sheet.paste(b, (sw + 10, 0)); sheet.paste(heat, (2 * sw + 20, 0))
        dr = ImageDraw.Draw(sheet)
        k = sw / truth.size[0]
        for (t0, t1) in tb:
            dr.rectangle([sw + 10, t0 * k, sw + 14, t1 * k], fill=(0, 200, 0))
        for (c0, c1) in cb:
            dr.rectangle([sw - 5, c0 * k, sw - 1, c1 * k], fill=(230, 160, 0))
        sheet.save(os.path.join(out_dir, "compare.png"))
        json.dump(report, open(os.path.join(out_dir, "report.json"), "w"), indent=1)

    if "--json" in flags:
        print(json.dumps(report, indent=1))
    else:
        print(f"SCORE {report['score']}/100   ssim={report['ssim']}  ink_iou={report['ink_iou']}  colour={report['colour']}  drift={report['drift_css_px']}px")
        print(f"bands: truth={len(tb)} cand={len(cb)} missing={missing} extra={len(extra)}   (all deltas in CSS px; + = candidate lower/right)")
        for m in matched:
            if m.get("missing"):
                print(f"  truth y={m['truth_y']:>6} h={m['truth_h']:>5}   MISSING in candidate")
            else:
                print(f"  truth y={m['truth_y']:>6} h={m['truth_h']:>5}   dy={m['dy_top']:>+6} dh={m['dh']:>+5} dx_l={m.get('dx_left','-'):>5} dx_r={m.get('dx_right','-'):>5}")
        for e in extra:
            print(f"  EXTRA band in candidate at y={e['cand_y']} h={e['cand_h']}")
        if note:
            print("note:", note)

if __name__ == "__main__":
    main()

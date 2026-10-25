# Icon design: redesign anything as a Windows Phone 8.1 glyph

The skill does not ship an icon set. It ships a grammar and a tool (`scripts/icon.py`) so you can turn any icon (a Material glyph, a brand mark, a sketch) into Metro style.

## The grammar
| Property | Value |
|---|---|
| Colour | white only (`#fff`) on transparent; tiles/pressed states supply the accent behind it. Never two-tone, never tinted. |
| Style | monoline outline, flat. No gradients, shadows, bevels, inner glows, rounded-rect "app icon" containers. |
| Glyph box | 20 x 20 pt, centred. Keep 1 pt padding inside the box. |
| Stroke | 2 pt, round caps and joins for glyphs inside a ring button. Bare shell/status glyphs use thin square-capped strokes (about 7 % of size, min 1.2 pt, miter joins). |
| Ring button | 44 pt circle, 2.2 pt white stroke (r 20.9), glyph centred, optional 11.5 pt label 3 pt below. Pressed = accent fill. |
| Filled parts | allowed only as small solid white pads (handset ends, dots, play triangle). Use sparingly. |
| Geometry | straight lines, circles, arcs, rectangles, 45 / 90 degree angles. No freehand curves, no perspective, no tiny detail. |
| Tile glyph | on a Start tile the glyph is 56 % of a small tile, 46 % of a medium one, centred slightly above middle, white on the accent. |
| Status bar | 5 signal bars rising 20/40/60/80/100 %, unlit bars at 30 % alpha; wifi = 3 concentric arcs; battery = outline + nub, red below 15 %. |

## Redesign procedure (any source icon)
1. **Name the metaphor** in four words or fewer ("envelope", "handset", "gear", "magnifier"). Drop everything that is not the metaphor (shadows, sparkles, text, badges).
2. **Reduce to primitives**: rect, circle, arc, line, polyline, at most 3 to 5 shapes. If it needs more, simplify the metaphor.
3. **Snap to the 20 x 20 grid**: integer or half-integer coordinates; symmetric about x = 10 unless the object is asymmetric (handset, pencil).
4. **Apply the stroke rules**: 2 pt, round caps and joins, no fills except pads. Gaps between strokes are at least 2 pt so they do not close up at 1x.
5. **Write the spec** (`examples/icons/*.json`) and run `python3 scripts/icon.py render spec.json out.svg`. The renderer rejects off-palette colour, wrong strokes, gradients.
6. **Look at it** at 44 pt on black inside the ring, and at 20 pt without. If it is not recognisable at 20 pt, remove detail.
7. **Lint hand-drawn SVGs** with `python3 scripts/icon.py lint file.svg`.

## Spec primitives
`line`, `rect`, `circle` (`"fill":true` for a pad), `poly` (`"close":true` for a polygon), `arc` (centre, radius, start/end degrees clockwise from +x), `path` (raw SVG path; keep inside 0..20). See `examples/icons/` for two worked specs (envelope, handset); they are demonstrations of the method, not a library.

## Common redesign decisions
- Material "filled" glyph -> outline the outer shape, delete interior detail.
- Rounded corners -> square corners (the ring and dots are the only round shapes).
- Two-tone / badge -> single white; express state with the accent behind or a second stroke.
- Direction (back, next) -> 45-degree chevron or arrow with a 2 pt shaft, no filled head.

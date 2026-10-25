# Windows Phone 8.1 - Start Screen, Tiles and the All-Apps List

An independent measurement specification of the Windows Phone 8.1 Start screen: tile geometry, colours, tile faces, live-tile flipping, press and edit feedback, scrolling physics, and the all-apps list. All numbers are in points on a 360 x 740 pt reference screen (4 px per pt, 1440 x 2960 px). Where a value could not be measured directly it is marked "(inferred)" or "(unverified)".

Conventions: text line heights are the natural line height of Segoe UI (about 1.33 x font size). Durations are nominal; the shell's default animation-speed setting (75) stretches every animation duration by 1.333x relative to the numbers below.

## 1. Coordinate system and scaling

| Fact | Value |
|---|---|
| Reference screen | 360 x 740 pt, 1 pt = 4 px (1440 x 2960 px) |
| Layout units | All layout constants below are in these points |
| Eye distance for 3D effects | 1210 pt at H = 740 (vertical field of view 34 deg) |

Measured cross-checks against a full-resolution reference capture: first tile left edge 14.06 pt (margin 14), medium tile width 105.8 pt (106), first tile top 41.8 pt (status bar 28 + top padding 14 = 42); all-apps icon square spans x = 80 to 124.7 pt; navigation-bar icon centre sits at y = 720 pt (740 - 40/2).

Use 360 x 740 pt as the reference. To render at another width, keep the ratios (gutter = 2% of width) and the fixed point constants, or scale everything by W/360.

Only three things depend on screen width: gutter = round(W x 0.02), margin = 2 x gutter, tile unit derived from them; the status-row cell size round(W x 0.032 x 2)/2; and quick-settings shade tiles (W - 8 - 9)/4. Everything else is absolute points. The number of medium tiles across (2, 3 or 4; default 3) is a user setting and is never derived from width.

Colour note: reference captures were taken with a warm colour-temperature shift (about 5200 K, inferred), so white appears as (255,232,217) and cobalt as (0,73,203). The nominal values (white #FFFFFF, cobalt #0050EF) are the authoritative ones.

Fonts: Light = Segoe UI Light, Semilight = Segoe UI Semilight, Regular = Segoe UI, Semibold = Segoe UI Semibold. Sizes are absolute points at the 360-wide layout (equal to CSS px).

## 2. Start layout constants

| Name | Value (pt) |
|---|---|
| Status bar height | 28 |
| Navigation bar height | 40 |
| Top padding (below status bar, above first tile row) | 14 |
| Gutter | round(W x 0.02) = 7 @360 |
| Side margin | 2 x gutter = 14 @360 |
| Units per row (small tiles) | 6 by default (3 medium columns); 4 or 8 for 2 or 4 medium columns |
| Max units per row / max tiles | 8 / 64 |
| Unit (small tile edge) | (W - 2 x margin - (units - 1) x gutter) / units = 49.5 @360, 6 units |
| Small tile | 1 x 1 unit = 49.5 x 49.5 |
| Medium tile | 2 x 2 units = 2u + g = 106 x 106 |
| Wide tile | 4 x 2 units = 4u + 3g = 219 x 106 |
| Large (4 x 4) tile | does not exist in this measurement; only small, medium, wide |
| Row pitch | unit + gutter = 56.5 |
| Round button (arrow / search) | 31 |

Other unit counts @360 (computed from the formula, inferred numerically): units = 4 gives unit 77.75, medium 162.5, wide = full row 332; units = 8 gives unit 35.375, medium 77.75, wide 162.5.

Width check at units = 6: medium columns sit at x = 14, 127, 240; the last ends at 346 = 360 - 14.

### 2.1 Placement algorithm

Tiles are placed in list order. A small tile occupies one quarter of a "medium slot"; slots are scanned left to right, top to bottom, and quarters fill in the order top-left, top-right, bottom-left, bottom-right. Medium and wide tiles use first-fit over cells, restricted to even columns (and even rows for two-row tiles).

```js
function placeTiles(tiles, W, H, units = 6) {
  const STATUS_H = 28, NAV_H = 40, TOP_PAD = 14, ROUND = 31;
  const gutter = Math.round(W * 0.02), margin = 2 * gutter;
  const unit = (W - 2 * margin - (units - 1) * gutter) / units;
  const taken = new Set();                       // "r,c" cells
  const T = (r, c) => taken.has(r + "," + c);
  let rows = 0;
  for (const t of tiles) {
    const cw = t.size === "small" ? 1 : t.size === "medium" ? 2 : 4;
    const ch = t.size === "small" ? 1 : 2;
    if (t.size === "small") {
      for (let block = 0; ; block++) {
        const br = Math.floor(block / (units / 2)) * 2, bc = (block % (units / 2)) * 2;
        let k = 0;
        while (k < 4 && T(br + (k >> 1), bc + (k & 1))) k++;
        if (k === 4) continue;                   // slot full (or covered by a medium/wide)
        const r = br + (k >> 1), c = bc + (k & 1);
        taken.add(r + "," + c);
        Object.assign(t, { row: r, col: c, x: margin + c * (unit + gutter),
          y: TOP_PAD + r * (unit + gutter), w: unit, h: unit });
        rows = Math.max(rows, r + 1); break;
      }
    } else {
      for (let cell = 0; ; cell++) {
        const r = Math.floor(cell / units), c = cell % units;
        if (c + cw > units || (cw > 1 && c % 2) || (ch > 1 && r % 2)) continue;
        let free = true;
        for (let y = r; y < r + ch; y++) for (let x = c; x < c + cw; x++) free = free && !T(y, x);
        if (!free) continue;
        for (let y = r; y < r + ch; y++) for (let x = c; x < c + cw; x++) taken.add(y + "," + x);
        Object.assign(t, { row: r, col: c, x: margin + c * (unit + gutter),
          y: TOP_PAD + r * (unit + gutter), w: cw * unit + (cw - 1) * gutter,
          h: ch * unit + (ch - 1) * gutter });
        rows = Math.max(rows, r + ch); break;
      }
    }
  }
  const visible = H - STATUS_H - NAV_H;
  const arrowY = TOP_PAD + rows * (unit + gutter) + 10;   // top of the round arrow button
  const startH = Math.max(arrowY + ROUND + 24, visible);  // scroll content height
  return { unit, gutter, margin, arrowY, startH };
}
```

Notes:
- Tile x, y are relative to the Start content; screen y = tile.y + 28 - scroll.
- The round "all apps" arrow button sits at x = W - 2 x round(W x 0.02) - 31 = 315 and y = arrowY + 28 - scroll. In the reference capture its centre is at (330.5, 520) pt: x = 315 + 15.5 = 330.5; with 8 rows, arrowY = 14 + 8 x 56.5 + 10 = 476, and 28 + 476 + 15.5 = 519.5.
- Tile order, size and colour are persistent and re-saved after every rearrangement. A tile's colour is an accent palette entry, an explicit RGB value, or "accent" (follow the system accent).

## 3. Colours

| Item | Value |
|---|---|
| Default accent | cobalt #0050EF |
| Accent palette (20) | lime a4c400, green 60a917, emerald 008a00, teal 00aba9, cyan 1ba1e2, cobalt 0050ef, indigo 6a00ff, violet aa00ff, pink f472d0, magenta d80073, crimson a20025, red e51400, orange fa6800, amber f0a30a, yellow e3c800, brown 825a2c, olive 6d8764, steel 647687, mauve 76608a, taupe 87794e |
| Tile fill | the tile's colour, opaque, full rectangle, no border, no corner radius |
| Tile text / glyph | white #FFFFFF |
| Start background | black #000000 |
| Wallpaper mode | the tile fill is only rgba(0,0,0,0.15) painted over a window onto the wallpaper photo; the tile's own colour is then not shown |

### 3.1 Wallpaper-under-tile ("translucent") tiles

- The wallpaper photo is scaled to cover and centre-cropped into a surface W wide and 1.6 x H tall.
- It is not a full-screen background. Each tile draws, first, the photo sub-rectangle behind it, opaque, using the same transform as the tile (so it tilts and flips with it); then the 15% black tile face over it.
- Parallax: the photo moves at 0.25 of the scroll speed.
```js
const py = clamp(28 + t.y - scroll * 0.75, 0, wallH - t.h);   // pt, inside the 1.6H photo
// sample photo rect (t.x, py, t.w, t.h); then composite rgba(0,0,0,.15) + white glyph/label
```
- The gutters between tiles and all area outside tiles stay black; the photo shows only through tiles.

## 4. Tile faces

Each tile face is w x h pt with a white glyph.

| Size | Glyph centre | Glyph box s | Label | Count badge |
|---|---|---|---|---|
| Small | (w/2, h/2) | h x 0.56 (27.7 @49.5) | none | Light 16 pt, top-right |
| Medium / wide | (w/2, h x 0.44) | h x 0.46 (48.8 @106) | Regular 13 pt, x = 8, top at y = h - 23, width w - 16, ellipsis | Light 22 pt, top-right |

- A glyph derived from the application's own icon is drawn at 0.86 of the box size and tinted pure white regardless of the original icon colours (a 192 x 192 single-channel mask).
- Count (live tile front): right-aligned at x = w - 8 - textwidth, y = 4, white; shown only on live tiles with count > 0.
- Label y is the top of the text box; at 13 pt the natural line height is about 17.3 pt, so the text bottom sits about 6 pt above the tile bottom. In the reference capture the label top is at 41.8 + 106 - 23 = 124.8 pt for the first medium tile.
- Fallback when there is no glyph: the first letter of the label, upper-cased, Light, size s x 0.9, centred in a box 2s x 1.24s.
- Glyphs in captures appear warm cream (about #FFE8D8) rather than white; this is the capture colour shift (inferred), the nominal colour is #FFFFFF.

### 4.1 Icon rendering

Decision order:
1. If the lower-cased label is one of music, phone, people, contacts, messaging, messages, mail, email, calendar, store, camera, maps, map, draw the matching Segoe UI Symbol glyph at absolute size s x 1.1, centred on the glyph's ink extents at the glyph centre. Codepoints: phone U+E13A, people U+E125, message U+E13B, mail U+E119, music U+E142, camera U+E114, calendar U+E163, store U+E14D, map U+E128 (the pairing of codepoints to names was read from a byte sequence; treat as inferred).
2. Otherwise, built-in system icons are monoline vector drawings: stroke width max(1.2, s x 0.07), square caps, miter joins, half-box unit u = s/2. Names: terminal, gear (settings), folder, globe, chart, pencil, store, back, search, shift, shift-on, backspace, enter, smiley, arrow (left/up/right/down), wifi, bluetooth, torch, brightness, rotation, code, phone, people, message, mail, photo, music, calendar, map, camera, airplane, location, close, chevron-up, plug, bolt. An unknown name draws a plain window (rectangle with a title bar). Exact path fractions of u are not reproduced here (unverified).
3. Otherwise, the application-derived white mask described above; fallback to the first letter.

## 5. Live tiles (flip)

Live tiles show up to three text lines, a title and a count on their back face. Small tiles are never live.

### 5.1 Back face layout

| Item | Value |
|---|---|
| Background | same rule as the front (tile colour, or 15% black over the wallpaper) |
| Line font size | 17 pt for wide tiles, 15 pt otherwise |
| Line y (k = 0..2) | 8 + k x (size + 5) |
| Line x / width | 8 / w - 16 |
| Line fonts | line 0 Semibold, lines 1-2 Regular, white |
| Title | tile label if empty; Regular 13 pt at (8, h - 23), width w - 16 |

A line wider than w - 16 is marqueed: rest 1200 ms, slide left at 30 pt/s until the end of the text shows, rest 1200 ms, restart. Cycle = 2 x 1200 + travel / 30 x 1000 ms. It is clipped to a window w - 16 wide. The marquee restarts each time the back face comes round.

### 5.2 Flip state machine

```js
// evaluated once per second; at most ONE tile flips per tick
function liveTick(now) {
  if (startNotInFront || screenOff || locked || editing) return;
  for (const t of tiles) {                    // list order
    if (!t.live || !t.backReady || now < t.nextFlipMs) continue;
    const toBack = t.flip < 90;
    if (toBack) t.sweepSince = now;
    animateSpring(t, 'flip', toBack ? 180 : 0, 520, 0.08);       // ms, overshoot
    t.nextFlipMs = now + (toBack ? 5000 + rand(0, 3000)           // back stays 5-8 s
                                 : 4000 + rand(0, 6000));         // front stays 4-10 s
    break;
  }
}
```
- The first time a tile becomes live: next flip at now + 2000 + rand(0, 4000) ms.
- If the live content disappears while the back is showing: flip back to 0 over 500 ms, ease-out.
- Rotation is about the horizontal axis through the tile centre. For angles above 90 deg the back face is drawn at (angle - 180) so it is never mirrored. No shading or alpha change during the flip.
- Easing is back-ease-out with 8% overshoot: c1 = 1.70158 x 0.08 / 0.1 = 1.3613; c3 = c1 + 1; u = t - 1; e = 1 + c3 x u^3 + c1 x u^2. Duration 520 ms (693 ms at the default animation-speed setting).
- The original device overshoot is closer to -180 -> 35 -> -6 -> 0 deg; the single 8% overshoot above approximates it (inferred).
- CSS approximation (inferred; perspective 1210 px, FOV 34 deg):
```css
.tile{transform-style:preserve-3d}
@keyframes tile-flip-notify{          /* cubic-bezier fit to back-ease-out o=0.08 */
  0%{transform:rotateX(0)} 100%{transform:rotateX(180deg)}}
.tile.flip{animation:tile-flip-notify 520ms cubic-bezier(.2,.7,.3,1.15) both}
```
Prefer the exact formula e = 1 + 2.3613 x u^3 + 1.3613 x u^2, u = t - 1.

## 6. Press feedback (tilt)

Constants: tilt 14 deg, in 70 ms, out 160 ms (the same constants are used by apps; app tilt lift is 40 pt).
```js
function press(t, fx, fy) {     // fx,fy = touch position in tile, -1..1 (x/w*2-1)
  if (Math.abs(fx) < .25 && Math.abs(fy) < .25) fx = fy = 0;   // centre press: only sinks
  anim(t.tiltY, fx * 14, 70);  // rotateY: pressed side goes away
  anim(t.tiltX, fy * 14, 70);  // rotateX
  anim(t.scale, 0.88, 70);     // sinks in
}
// release: tiltX = tiltY = 0, scale = 1 over 160 ms (ease-out)
```
- Transform order: place translate, rotateX(tiltX), rotateY(tiltY), flip rotateX, scale(press x grow), translate(-w/2, -h/2).
- Perspective: vertical FOV 34 deg, eye distance d = (H/2) / tan(17 deg) = 370 / 0.3057 = 1210 pt at H = 740; point scale w' = 1 - z/d. CSS: `perspective: 1210px; perspective-origin: 50% 50%` on the Start container.
- A press is cancelled once the touch moves more than 8 pt (it becomes a scroll).
- All-apps list rows: tiltY = fx x 14 x 0.7, tiltX = fy x 14, scale 0.91.

## 7. Scrolling, fling and overscroll (Start and list)

| Constant | Value |
|---|---|
| Fling decay time constant | 380 ms |
| Overscroll drag resistance | 0.35 |
| Max fling velocity | 7 pt/ms |
| Max velocity while out of range | 1.4 pt/ms |
| Overscroll spring omega | 0.016 /ms |
| Page change duration | 300 ms |
| Page flick velocity threshold | 0.35 pt/ms |

```js
// finger drag: position follows finger 1:1 inside bounds, 0.35x outside
resist = (raw, max) => raw < 0 ? raw*0.35 : raw > max ? max + (raw-max)*0.35 : raw;
scroll = resist(scroll0 - (y - y0), max);                 // max = contentH - (H-28-40)
// release: v = clamp(-fingerVy, ±7) pt/ms  (0 if the finger rested >90 ms before lifting)
// integrate in sub-steps of at most 4 ms:
step(dt): if (pos<0||pos>max) {                           // overscroll: critically damped spring
            x = pos - (pos<0?0:max); v += (-w*w*x - 2*w*v)*dt; w=0.016; pos += v*dt;
            snap when sign flips or |x|<.25&&|v|<.01 }
          else { v *= Math.exp(-dt/380); pos += v*dt;
                 if (pos out of range) v = clamp(v, ±1.4);  else if (|v|<0.012) stop }
```
- Finger velocity filter: v = v x keep + (dx/dt) x (1 - keep), keep = 0.45 (0 if dt > 50 ms); velocity in pt/ms.
- Direction lock: once movement reaches 12 pt, an angle steeper than 20 deg from horizontal locks vertical scrolling; horizontal page change requires being within 20 deg of horizontal and a length of at least 18 pt. A finger landing on a coasting list only stops it (it is not a tap). Tap slop is 8 pt.
- Start <-> all-apps page swipe: page value 0..1; during drag page = page0 - dx/W with 0.3x rubber band outside [0, 1]. On release, a flick faster than 0.35 pt/ms (or a drag past halfway) chooses the target; it settles with a critically damped spring k = 0.018 /ms starting from the finger's speed. The whole Start content translates by -page x W; the list slides in from the right at x = 80 + (1 - page) x W.

## 8. Entrance and exit of Start (turnstile)

When Start appears, each tile swings in around its inner vertical edge, starting 65-70 deg turned and 0.18 x eye-distance behind the screen. Order: bottom rows first, right tile before left. Row step 50 ms; the left tile of a pair +51 ms; small tiles 33 ms earlier; per-tile life 186 ms (small tiles x0.8); start jitter +-6 ms; speed jitter +-5%; overshoot travel jitter +-15%; the top-left tile last (+70 ms). The same clock drives all-apps rows. Full formulas are in the motion-shell chapter.

## 9. Edit mode (long press on a tile)

- Trigger: finger rests on a tile for 450 ms (fires from 420 ms) without moving more than 8 pt. Strong haptic.
- Edit progress goes 0 to 1 over 180 ms, ease-out:
  - held tile: scale 1 + 0.06 x progress, drawn on top;
  - every other tile: scale 1 - 0.08 x progress, alpha 1 - 0.45 x progress;
  - the arrow-to-list button fades with alpha x (1 - progress).
- Two round badges (32 pt, black fill, 2 pt white ring, white glyph) appear after progress > 0.3, alpha (progress - 0.3) / 0.7, at the held tile's right edge: x = min(cx + w/2 x grow - 16 - 4, W - 32 - 2). The unpin badge top is at cy - h/2 x grow - 16 + 4; the size badge bottom at cy + h/2 x grow - 16 - 4. Unpin glyph = pin with a diagonal strike. Size glyph = diagonal arrow pointing down-right (grow) for small and medium tiles, rotated 180 deg (shrink) for wide tiles. Hit radius 25 pt (badge radius + 9).
- Tapping the size badge cycles small -> medium -> wide -> small; tiles re-place; click haptic; layout saved.
- Drag: the held tile follows the finger with the grabbed point preserved. When the centre of the dragged tile is inside another tile (or below all tiles, which means "to the end"), it takes that tile's position in the order. Reorders are debounced to one per 220 ms, with a tick haptic. Other tiles glide to their new places: offset decays by exp(-dt/70) (time constant 70 ms), snapping when below 0.3 pt.
- Auto-scroll while dragging near the top (y < 28 + 56 = 84) or bottom (y > 740 - 40 - 56 = 644): 0.45 pt/ms.
- Exit: tap on empty area, tap on the held tile, Back, or Start; progress returns to 0 in 180 ms. Unpin removes the tile instantly, the rest re-place with the glide, and the layout is saved.
- Live tiles do not flip during editing.

## 10. Pin to Start from the all-apps list

Long press (450 ms) on an app row opens a context menu (section 11.3). "pin to start" adds a medium tile in the accent colour with the app-derived glyph, last on Start. Start scrolls so the new tile's bottom is 24 pt above the visible bottom, the page springs back to Start, and the new tile's press scale animates 0.4 -> 1.0 over 320 ms after a delay of 220 ms (page change 300 ms minus 80 ms), so it grows in as the page arrives.

## 11. All-apps list

### 11.1 Geometry (360 pt basis)

| Item | Value |
|---|---|
| Column left | 80 |
| Icon square | 45 x 45 |
| Row pitch | 55 (10 pt gap) |
| First row top below status bar | 17 |
| Row composition | square + 13 pt gap + name; name x = 80 + 45 + 13 = 138 |
| Row width | min(W - 80 - 8, 45 + 13 + textwidth(name, Semilight 22) + 6) |
| App name | Segoe UI Semilight 22 pt, white, top y = 7 within the 45 pt row, ellipsised at the row width |
| App glyph on square | 25 pt box, centred, white |
| Square | solid accent colour, no corner radius |
| Letter header | outline square 45 x 45: 1.5 pt accent stroke inset 0.75; lower-case letter, Semilight 27 pt, accent colour, at x = 4, y = 45 - 38 = 7 |
| Header letter rule | first character A-Z becomes lower case; anything else becomes "#" |
| Headers | occupy a 55 pt row slot like an app; not tappable |
| Content height | last row y + 55 + 40 |
| Search round button | 31 pt ring (white, 2 pt) centred at x = 51, top at y = 28 + 12 = 40; fixed, does not scroll |
| Round arrow glyph | circle radius c - 1.5, 2 pt white stroke; shaft from c - 7 to c + 7, head 6 |
| Search glyph | lens radius 6 centred at (c + 2, c - 2), handle to (c - 8, c + 8) |

Measured cross-checks (reference capture): header outline spans x = 80 to 124.7 pt, top at 45 pt (28 + 17); row pitch 55 pt; app name x = 138.6 pt; search ring centre (51, 55.5) pt (40 + 15.5).

### 11.2 Searching the list

Tapping the round search button filters the list to apps whose name contains the typed text (case-insensitive), with no headers, starting at y = 40 - 28 + 40 + 14 = 66 pt in list space. The search box is a white rectangle (W - 32) x 40 at x = 16, y = 40; text Regular 19 pt black at box x + 10, y + 8; placeholder "search" in grey (55% white level); caret a 2 pt accent bar; magnifier at the right (grey 20%, 2.2 pt stroke). Rows are clipped below y = 40 + 40 + 4 = 84 pt. The on-screen keyboard appears; Enter launches the first match. Leaving the page ends the search.

### 11.3 Long-press menu

White panel, full width, 62 pt per row. One row ("pin to start" / "unpin from start"); installed third-party apps get a second row "uninstall", which changes to "tap again to uninstall" in the accent colour. Text black Semilight 24 pt at x = 86, y = 14 (+62 for the second row). Placed 6 pt below the row (row top + 45 + 6), or above it if it would overlap the navigation bar. Opening: scaleY 0 -> 1 about its middle plus a 50% black dim over the list, 200 ms ease-out; closing 140 ms.

### 11.4 Jump list / alphabet letter grid

Not measured. Tapping a letter header does nothing in this measurement. The Windows Phone 8.1 letter-grid overlay is (unverified); a plausible form is a 4-column grid of 45 pt outline squares (inferred from the platform, no measured reference).

### 11.5 List scrolling and entrance

Scroll physics are those of section 7, with an independent scroll position and velocity. Row entrance and exit use the tile turnstile rule with each row treated as a small tile at the left (left = 0.5), jitter from a per-row hash, and rows-up = (list bottom - (row y + 45)) / pitch where pitch = 2 x W / units = 120 pt.

## 12. Start screen chrome

The 28 pt status bar and 40 pt navigation bar are separate, opaque black layers drawn on top. The Start content area is y = 28 to 700. Scrolling content passes under the bars.

## Kit-ready constants

```json
{
  "reference": {"width_pt": 360, "height_pt": 740, "px_per_pt": 4, "px": [1440, 2960]},
  "layout": {"statusH": 28, "navH": 40, "topPad": 14, "gutterPctW": 0.02, "marginGutters": 2,
    "units": 6, "mediumCols": [2, 3, 4], "tile": {"small": [1, 1], "medium": [2, 2], "wide": [4, 2]},
    "gutter@360": 7, "margin@360": 14, "unit@360": 49.5, "medium@360": 106, "wide@360": [219, 106],
    "roundBtn": 31, "arrowBelowRows": 10, "contentPadBottom": 24},
  "tileFace": {"smallGlyph": 0.56, "mediumGlyph": 0.46, "glyphCy": 0.44, "labelPt": 13,
    "labelXY": [8, "h-23"], "glyphAtScale": 0.86, "wallTint": 0.15, "wallParallax": 0.25, "wallTall": 1.6,
    "countFont": {"small": 16, "other": 22}, "countRightPad": 8, "countTop": 4},
  "live": {"backLinePt": {"wide": 17, "other": 15}, "lineY": "8+k*(size+5)", "flipMs": 520, "overshoot": 0.08,
    "frontStayMs": [4000, 10000], "backStayMs": [5000, 8000], "firstFlipMs": [2000, 6000], "tickMs": 1000,
    "sweep": {"restMs": 1200, "ptPerSec": 30}},
  "press": {"tiltDeg": 14, "inMs": 70, "outMs": 160, "scale": 0.88, "deadZone": 0.25, "fovDeg": 34, "eye@740": 1210},
  "edit": {"longPressMs": 450, "ms": 180, "heldScale": 0.06, "othersScale": -0.08, "othersDim": 0.45,
    "badge": 32, "reorderDebounceMs": 220, "glideTauMs": 70, "autoScrollPtPerMs": 0.45, "autoScrollEdge": 56},
  "scroll": {"tauMs": 380, "resist": 0.35, "maxV": 7, "edgeV": 1.4, "springW": 0.016, "pageMs": 300,
    "pageFlickV": 0.35, "pageSpringK": 0.018, "axisDeg": 20, "axisLock": [12, 18], "slop": 8},
  "list": {"left": 80, "icon": 45, "row": 55, "top": 17, "gap": 13, "nameFont": ["Semilight", 22],
    "glyph": 25, "headerFont": ["Semilight", 27], "headerStroke": 1.5, "search": {"x": 51, "y": 40, "box": 40},
    "menuH": 62},
  "accent": {"default": "#0050EF"}
}
```

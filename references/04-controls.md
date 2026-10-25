# Windows Phone 8.1 Controls: Measured Specification

This document records the geometry, typography, colour and timing of the core Windows Phone 8.1 style controls: page headers, list entries, toggle switches, sliders, text boxes, pickers, buttons, menus, glyphs, loading dots and the press/tilt effect. All values are measured from a 360 x 740 pt reference screen. Items marked (inferred) were deduced rather than observed; items marked (unverified) could not be determined.

## 0. Units, coordinate system, text conventions

* **Screen = 360 x 740 pt, 4.0 px per pt** (1440 x 2960 px). Status bar 28 pt, navigation bar 40 pt, so an app window is **360 x 672 pt** and its origin sits at screen y = 28. All numbers are in these points (equal to CSS px at a 360 px viewport). To convert a capture: `app_y = px_y/4 - 28`, `x = px_x/4`.
* **Scaling to other widths**: nothing is scaled. Only items defined relative to the screen width stretch (row hit areas, boxes of width `360 - 2*margin`, right-aligned items at `360 - margin - ...`). Left/top offsets and font sizes are absolute. To render at another width W without reflow, apply a uniform `scale = W/360` (e.g. 450 gives x1.25, so margin 16 becomes 20). Do not scale the 4 px/pt to a different physical width.
* **Text origin**: the y coordinate given for text is the **top of the text line box**, not the baseline. Hinting is off, glyph positions are not rounded to whole pixels; text wraps at word boundaries (falling back to characters) when a wrap width is given.
* **Vertical metrics**: measured on about/sensors/networking pages (error <= 0.2 pt), **baseline = y_top + 1.00 x size** (measured with natural line height). Line height is the font's natural height: **natural line height of Segoe UI (about 1.33 x size)**. Layout height of a text block is `H(size, n) = ceil(n x 1.33 x size)` pt (16 pt: 1 line 22, 2 lines 43; 19 pt: 1 line 26). Cap height is about 0.70 em, ascender height about 0.76 em, x-height about 0.5 em.
* **CSS recipe**: for every text, `position:absolute; left:x; top:y; font-size:size px; line-height:normal; white-space:nowrap` (or `width:wrap; overflow-wrap:anywhere`). Use `text-rendering: geometricPrecision; -webkit-font-smoothing: antialiased`, and no letter-spacing (none is ever applied). With Segoe UI metrics (ascent about 1.08, descent about 0.25) the baseline lands where measured; for another font, shift vertically so the baseline is at `top + 1.00 x size`.
* **Flow layout rule**: each text call advances the cursor by the block's line-box height `H(size, n)`.
* **Ellipsis**: single-line text is truncated at the end with a Unicode ellipsis (U+2026) at the given width.
* **Corner radii: 0 everywhere.** Every shape is a rectangle; the only circles are the round buttons, the keypad dots and the Wi-Fi dot. No shadows, gradients or blur. The only translucency: menu scrim 0.72, picker fade, skeleton 0.07.

### Font stack
| Role | CSS font-family (order matters) | weight |
|---|---|---|
| Light | "Segoe UI Light","Selawik Light","Selawik","Open Sans Light",sans-serif | 300 |
| Semilight | "Segoe UI Semilight","Selawik Semilight","Selawik","Open Sans",sans-serif | 350 (Semilight; 300/400 fallback) |
| Regular | "Segoe UI","Selawik","Open Sans",sans-serif | 400 |
| Semibold | "Segoe UI Semibold","Selawik Semibold","Selawik","Open Sans Semibold",sans-serif | 600 |
| Mono | "DejaVu Sans Mono","Liberation Mono",monospace | 400 |

The glyph shapes in the captures look Segoe/Selawik-like; the exact face actually rendered is (unverified).

### Colour tokens
| Token | Value | Notes |
|---|---|---|
| background | #000000 | |
| text primary | #FFFFFF | |
| caption / secondary / disabled-ish grey | #999999 (0.6) | measured pixel (153,153,153) |
| next pivot title | #616161 (0.38) | |
| accent default | #0050EF (cobalt) | |
| slider track | #383838 (0.22, rgb 56) | |
| toggle off fill | #333333 (0.2) | |
| textbox idle / focused | #C7C7C7 (0.78) / #FFFFFF | text #000 |
| picker border, toggle border, button outline | #FFFFFF, 2 pt | |
| dark tile (phone keypad row, speed-dial "plus") | #212121 (0.13) | |
| keypad key / outline button stroke | #333333 / #666666 (0.4), 1.5 pt | |
| red (end call / decline) | #C72121 (0.78,0.13,0.13) | |
| WP red / amber (device states) | #E51400 / #F0A30A | |
| scrim under menu | rgba(0,0,0,0.72) | |
| wallpaper tile placeholder / unchosen button | #333333 / #2E2E2E (0.18) | |

**20 accents** (in order): lime a4c400, green 60a917, emerald 008a00, teal 00aba9, cyan 1ba1e2, cobalt 0050ef, indigo 6a00ff, violet aa00ff, pink f472d0, magenta d80073, crimson a20025, red e51400, orange fa6800, amber f0a30a, yellow e3c800, brown 825a2c, olive 6d8764, steel 647687, mauve 76608a, taupe 87794e.

Accent is used for: ON toggle fill, slider fill, choice value, picker selected option (open), connected/active status text, failed/note text, speed-dial tiles, incoming message bubbles, call timer, app-list tiles/letters, wallpaper chosen frame, "search again" link, caret in the shell search.

**Warm tint**: one capture of the networking page measures (255,232,217) for white and (0,73,203) for accent, a global multiply of about (1.0, 0.91, 0.85) from a system-wide colour-temperature layer. The about and sensors captures are pure (255,255,255). Apply any tint as a separate overlay, not inside the controls.

### Global constants
Margin 16; header height 104; touch slop 8 pt; hold time 500 ms. Tilt: 14 deg maximum, lift 40, press sink 0.045, 70 ms in / 160 ms out (section 12).

## 1. Header family

```
Pivot header (title, next title, optional action)    returns 108
  caps line   : app name in UPPERCASE (e.g. "SETTINGS"), Semibold 11.5, #fff, x=16, top y=14
  title       : Semilight 48, #fff, x=13 (margin-3), top y=24
  next title  : same font, #616161, x = 13 + W(title) + 16, y=24      (W = integer px width of title at 48)
  3rd copy    : title again in #616161 at x = 13 + W(title)+16 + W(next)+16   (so tabs "go round")
  hit BACK    : (0,0,360,90) action back  [registered last, so it loses to the next-title hit]
  hit PIVOT   : (16+W+8, 0, 360-(16+W+8), 90) action pivot, arg = other page   (only if an action exists)
  state       : pivot offset dx = W+16
Plain header (title) = pivot header with no next title (no grey title, no third copy)
```
* Measured (about page): caps cap-top 17.2, baseline 25.5 (predicted 17.5 / 26); title baseline 72.5 (predicted 72.0 = 24+48).
* The caps band spans y 14 to about 32 (band height 32): it does not move while tabs slide; only the title strip (32..104) moves.
* Titles have no letter-spacing and are lowercase by convention ("about", "cellular + SIM", "sensors").
* The header region 0..104 never scrolls; below it content is offset by the scroll amount. Content starts at y=108.
* Long titles (store page): if W(title,48) > 328, caps stay at 14 and the title is set at 30 pt Semilight, wrapped, at x=14, y=32; the header returns `32 + h + 22`.

## 2. Entry (hub row)
```
title  : Semilight 25.5 #fff   x=16 top y
detail : Regular 12 #999       x=16 top y+31
hit    : (0, y-2, 360, 57)
returns y+59      (an empty detail still reserves the pitch)
```
Measured (networking "access point"): title baseline 356.1 vs predicted 330+25.5 = 355.5. Press gives the tilt effect (section 12). Also used as a button-like action row ("save", "delete", "sync now", "call", "text").

**Choice variant**: title Semilight 20 white at y; value Regular 15 **accent** at y+26; hit (0,y-4,360,52); returns y+68.

## 3. Switch and toggle
```
title  : Semilight 21 #fff x=16 y   (wrap width = 360-32-64 = 264)
state  : "On"/"Off" Regular 13 #999 x=16 y+26
toggle : placed at x = 360-16-54 = 290, y+4
hit    : (0, y-4, 360, 52)
returns y+66
```
Toggle (54 x 24 body, thumb 12 x 26), coordinates relative to its (x,y):
| Part | Geometry | Colour |
|---|---|---|
| border | stroke 2 pt, rect(x+1,y+1,52,22), outer 54 x 24 | #fff |
| track fill | rect(x+4,y+4,46,16) | ON accent / OFF #333333 |
| thumb | ON rect(x+41,y-1,12,26); OFF rect(x+1,y-1,12,26) | #fff |

There is **no slide animation**: a state change is an immediate redraw and the thumb jumps. Pixel check (networking page): bbox x 290-344, y 111-137 for a row at y=108, so toggle y = 112 and thumb spans 111..137, an exact match. The hit area is the whole row, not just the control. The devices page uses a bare toggle at `(360-16-56, row_top+12)` with hit width 96.

Page variants: the settings pages use slightly different hand-set offsets: display page title y, "On/Off" y+26, toggle y+6, hit h50, pitch 66; audio/battery pitch 66/72; keyboard page state 13.5 pt, toggle y+4, pitch 68.

CSS:
```css
.toggle{position:absolute;width:54px;height:24px;box-sizing:border-box;border:2px solid #fff}
.toggle::before{content:"";position:absolute;left:2px;top:2px;width:46px;height:16px;background:#333}
.toggle.on::before{background:var(--accent)}
.toggle::after{content:"";position:absolute;top:-3px;left:-1px;width:12px;height:26px;background:#fff}
.toggle.on::after{left:39px}
```
(Thumb x relative to the toggle outer box: OFF at x+1 gives left:-1px inside the border box; ON at x+41 gives 39px. Adjust if the border is drawn as an outline.)

## 4. Field (read-only value)
```
caption: Regular 13 #999 x=16 top y
value  : Regular 16 #fff x=16 top y+18, wrap width 328
returns y + 20 + H(value) + 12      (1 line = 54, 2 lines = 75)
```
With natural line height (Segoe UI: 1.33 x size, rounded up per block), value blocks are 22 pt (1 line) and 43 pt (2 lines) tall, so the pitch is 20 + 22 + 12 = 54 (1 line) and 20 + 43 + 12 = 75 (2 lines). The same rule was verified for the 19 pt label/value pair (56, confirmed against a render); 54 / 75 follow from the identical formula. Earlier 52 / 71 figures assumed a 1.2 x size line height and are superseded.

The settings "about" page uses a variant: caption 13 #999 at y; value Semilight **19** #fff at y+18 (wrap 328); pitch `H(value,19)+30` (53 under an older 1.2 x size assumption; 56 with natural line height, verified against a render).

## 5. Slider
```
hit (slider): (x, y, w, 46)   touch-down accepts x-16 .. x+w+16 horizontally
caption : Regular 13 #999 at (x,y)       [if caption]
percent : "N%" Semibold 14 #fff at (x+w-42, y)
track   : rect(x, y+24, w, 4)  #383838
fill    : rect(x, y+24, w*p/100, 4) accent
thumb   : rect(x+fill-5, y+17, 10, 18) #fff        (y+24-7 .. y+24+11)
```
Typical use: `x=16, w=328`; the caller advances 62 (brightness/audio), 58-76 elsewhere. Dragging: value = round((touch_x - x)/w x 100) clamped 0..100, redrawn live until the finger lifts. Haptic "tick" on touch down and "tick slide" at every 10 % notch crossing. The thumb is square (no rounding).

## 6. Text box
```
caption : Regular 13 #999 x=16 y
y += 22
box     : rect(16, y, 328, 38) fill #C7C7C7 idle, #FFFFFF focused; no border
text    : Regular 17 #000 at (24, y+8); caret = literal "|" appended while focused
hit     : (0, y-24, 360, 68)
returns y + 38 + 16     (caption top to next = 76)
```
Focus raises the app above the on-screen keyboard. The message compose box is the same widget, narrower.

## 7. Picker (list picker)
```
caption : Regular 15 #999 at (16,y), wrap 328;  y += 24
row = 40; closed box h = 40; open h = 40 + ((count-1)*40 + 8)*p        p = open amount 0..1
box     : fill white alpha=p ; stroke 2 pt white (inset 1) ; contents clipped to box
option i: top = y + 4p + i*40p ; text Regular 17 at (26, top+9), wrap 308
          selected: colour lerp(white -> accent, p) ; others: black alpha p (hidden at p~0)
returns y + h + 18
hits    : closed (p<0.999): (0, y-28, 360, h+32) arg -1 (toggles open); open: each option (0, top, 360, 40) arg = index
```
Open: p = 1-(1-t)^3, t = elapsed/250 ms. Close: p = (1-t)^3, t = elapsed/200 ms (closing also follows ease-out-cubic). While 0.001 < p < 0.999 the page redraws every frame. Only one picker animates at a time. Back closes an open picker first.

Settings "theme" accent picker is a different widget: caption Regular 13.5 #999; box stroke 2 pt `rect(17,y+1,326,40)`; colour chip 22x22 at (26,y+10); name Regular 16 at (58,y+10). Chip tile grid on the accents page: 4 across, gap 10, side (328-30)/4 = 74.5, selected = 3 pt white inset stroke.

## 8. Buttons, round button, menu
**Button**: h=40, width given; idle: 2 pt white stroke inset by 1; label Semibold 14.5 centred at (x+w/2, top y+10); returns y+52. Pressed (finger down): **fill white, label black**, no tilt. Pair layout gap 12. Store variant: h46, stroke 2 inset 1 (`rect(x+1,y+1,w-2,44)`), label Semilight 17 at y+11, hit (x,y-4,w,54), returns y+46; full width = 328, pair = (328-12)/2.

**Phone outline buttons**: stroke 1.5 #666 (`rect(x+.75, y+.75, w-1.5, h-1.5)`), h46, w = (328-10)/2 = 159, label Regular 16 #EBEBEB at y+12. **Call pad**: answer/decline rects h54 (accent / #C72121), label Semilight 22 white at y+12; gap 8.

**Round button**: d=44; ring stroke 2.2 pt white, circle centre (cx, y+22), radius 20.9; glyph in a 20-pt box centred at (cx, y+22), line width 2, round caps and joins; label Regular 11.5 centred at (cx, y+47); hit `(cx-34, y-4, 68, 44+26)` with label, else `44+8`. Colour is white. Glyph strokes (box-centre origin):
* add `M-8 0 H8 M0 -8 V8`; cancel `M-7-7 L7 7 M7-7 L-7 7`; back `M8 0 H-8 M-2-6 L-8 0 L-2 6`
* send (closed) `-9,-8 9,0 -9,8 -6,0`; message (closed) `-9,-7 9,-7 9,4 -2,4 -7,9 -7,4 -9,4`; edit (closed) `-8,8 -7,3 4,-8 8,-4 -3,7`
* save: stroke `rect(-8,-8,16,16)`, fill `rect(-4,-8,8,5)`, stroke `rect(-4.5,1,9,7)`
* delete `M-8-5 H8 M-3-5 V-8 H3 V-5 M-6-5 L-5 9 H5 L6-5`
* refresh: arc r8 from -36 deg to 243 deg plus arrowhead `M8-8 L7-2.5 L2-4.5`
* people: filled circle (0,-4.5) r4 plus half-disc (0,9) r8.5
* keypad: 3x3 dots, pitch 7, r1.8
* call: handset made from a -45 deg rotated arc r13 and two 5.5 x 5 pads (exact pad placement (unverified))

**Menu**: appears immediately (no animation). Everything behind is dimmed with `rgba(0,0,0,.72)`; earlier hit areas are cleared. Panel white, full width (0..360), height `count*50+16`, top y clamped so it ends at least 8 above the window bottom. Item i text Semilight 24 #000 at (16, y+8+i*50+8), hit `(0, y+8+i*50, 360, 50)` arg i; a fallthrough hit (0,0,360,100000) cancels. Opened by a hold (500 ms) with a "heavy" haptic. Anchor y: row bottom (`y+52`, `y+56`, `y+44`).

Centred text is placed at `x - W/2`, W = integer px width.

## 9. Wi-Fi glyph and loading dots
**Wi-Fi glyph**: box `size`, origin (x,y). Centre `cx = x+size/2, cy = y+0.86*size`, `r = 0.78*size`, stroke `0.1*size`, butt caps. Three arcs i=0..2 at radius `r*(0.45+0.275*i)` from -135 to -45 deg, alpha 1 if `bars >= i+2` else 0.3; dot `circle(cx, cy-0.03*size, 0.09*size)` alpha 1 if bars >= 1 else 0.3. Signal to bars: >=75: 4, >=55: 3, >=35: 2, >0: 1. Locked network: 9x7 #BFBFBF rect at (margin+19, y+30) with a 1.5 pt arc r3 shackle.

**Loading dots** (same maths in the shell): 5 squares **3 x 3 pt**, accent colour, at y=3 (top edge of the window), no radius. `t = elapsed mod 2600 ms`; dot i: `p = (t - 160 i)/1700`, drawn if 0 < p < 1; `u = 2p-1`; `x_centre = W*(0.5 + 0.5*(0.25u + 0.75u^3))`; rect `(x-1.5, 3, 3, 3)`. Speed profile dx/dt ~ 0.25 + 2.25u^2 (centre slow, edges about 10x faster), 260 ms pause at the end of each cycle. Shown while the app is busy; hidden during a page-change animation. Full-screen "Loading..." variant (shell): text Semilight 20 white at x=20, y = centre of app area, dots 12 pt above it.

## 10. Hit testing and misc
Hit rect = `{x, y, w, h, action, arg, slider, button}`. The **first** matching hit in registration order wins on tap and press, so overlays (menu) register first and background hits last. Minimum sizes in practice: row hits 52-64 high, full width; round button 68 x 70; slider 46; button 40; nothing smaller than 40 except text links ("see all" 40; filter chips 44).
Scrollbars: **none** (no indicator anywhere). Cursor/selection UI: none beyond "|".

## 11. Skeleton placeholders and store rows
Skeleton placeholders `rgba(255,255,255,0.07)` rects: tile 56x56 at x16, name 0.55w x16 at x84, line 0.85w x12 at y+25, badge 54x13 at y+45; row pitch 76. Source badge: 1 pt #999 outline `rect(x+.5, y+43.5, W(badge,9.5 semibold)+8, 14)`, label 9.5 semibold #999 at (x+4, y+44). Row: tile 56 at x16; title Semilight 20 white at (84, y-3); blurb Regular 13 #B8B8B8 at (84,y+23); meta Regular 11.5 #999 at (x+badge_w+8, y+43); pitch 76; hit (0,y-6,360,70).

## 12. Press / tilt effect
Applies to any non-header hit (y >= 104) shorter than the window; not to buttons (they fill instead) nor sliders.
```
press amount p(t): clamp01(dt/ms), then 1-(1-t)^2 ; ms = 70 going in, 160 coming out (from the current amount)
pivot fractions fx,fy = touch position inside the hit (0..1)
ay = min(14deg, asin(min(1, 40 / (w/2))))        // width-limited lean
ax = min(14deg, asin(min(1, 40 / (h/2))))
ry = (fx-0.5)*2*ay*p ;  rx = (fy-0.5)*2*ax*p     // the touched side goes AWAY (sinks)
z0 = -0.045 * eye * p ;  eye = (windowH/2)/tan(17deg)   (about 1099 for 672)
vertex (X,Y) from centre: Z = z0 - X sin(ry) - Y sin(rx); scale s = eye/(eye - Z)
   screen = centre + (X cos(ry) s, Y cos(rx) s)
the row is rendered as a 12 x 4 cell mesh, black behind it (it only shrinks)
```
Full-width 360 row: ay = asin(40/180) = 12.84 deg; any hit narrower than 330 pt gets the full 14 deg; row height 57 gives a full 14 deg vertical component but fy is mostly 0.5, so rx is small. A scroll (>8 pt move) cancels the press instantly (p=0, no ease).

CSS: `transform: perspective(1099px) translateZ(calc(-0.045*1099px*var(--p))) rotateY(calc(var(--ry)*1deg)) rotateX(calc(var(--rx)*-1deg))` with `transform-origin:center` and `perspective-origin:center` per element; finger right gives positive CSS rotateY (right side recedes); finger low gives negative CSS rotateX. Transition 70 ms ease-out-quad in, 160 ms out (`cubic-bezier(.259,.518,.599,1)`, error 0.0001).

**Hold**: finger still (< 8 pt) for 500 ms fires a hold action; if it opened a menu, the later lift is not a tap.

**Haptics**: `"tap"` on every activated hit, `"tick"` on slider touch, `"tick slide"` per slider 10 % notch, `"heavy"` when a hold fires. Haptics on tab changes and list ends are described in the design intent but were not observed (unverified). Kinds, light to strong: tick, tap, click, heavy. Settings can also use grouped kinds such as `tick system`, `tap nav`, `tap tiles`, `tick slide`, `tap apps`, `key keys`.

## 13. Bubble and list one-offs
| Item | Geometry |
|---|---|
| speech bubble in/out | width 0.74 x 360 = 266.4, pad 10, text Regular 15; incoming accent, outgoing #333; tail triangle 12 x 8 at top-left / bottom-right; timestamp Regular 11.5 #8C8C8C |
| letter square (people) | 42x42 accent, letter Semilight 26 white at (22,y+8); row title Semilight 24; pitch 48; letter block +6 above, +52 |
| wallpaper target buttons | 3 across, gap 8, h36, label Regular 13 at +10,+9; chosen accent else #2E2E2E |
| speed-dial tile | 2 across gap 8, h112, name Semilight 20 at (x+12, y+h-50), "mobile" 12.5 #D9D9D9 at y+h-26 |
| keypad key | 3 x 4, gap 2, kw = (360-4)/3, kh 84, fill #333, digit Light 40 centred, letters Semibold 12 #D9D9D9 |
| menu rows | see section 8 |

## Kit-ready constants
```json
{
 "units": {"screen_pt":[360,740],"px_per_pt":4,"status_h":28,"nav_h":40,"app_h":672,"margin":16,"header_h":104,"content_top":108},
 "text": {"baseline_over_top_em":1.0,"line_height_em":1.33,"layout_h":"ceil(lines*1.33*size)"},
 "fonts": {"light":"Segoe UI Light|Selawik Light","semilight":"Segoe UI Semilight|Selawik Semilight","regular":"Segoe UI|Selawik","semibold":"Segoe UI Semibold|Selawik Semibold"},
 "colors": {"bg":"#000000","text":"#FFFFFF","caption":"#999999","nextTitle":"#616161","accent":"#0050EF","track":"#383838","toggleOff":"#333333","textboxIdle":"#C7C7C7","tile":"#212121","key":"#333333","outline":"#666666","danger":"#C72121","wpRed":"#E51400","wpAmber":"#F0A30A","scrim":"rgba(0,0,0,0.72)","skeleton":"rgba(255,255,255,0.07)"},
 "header": {"caps":{"size":11.5,"weight":"semibold","x":16,"y":14},"title":{"size":48,"weight":"semilight","x":13,"y":24},"nextGap":16,"hit_h":90,"returns":108},
 "entry": {"title":25.5,"detail":12,"detailDy":31,"pitch":59,"hit":[0,-2,360,57]},
 "switch": {"title":21,"state":13,"stateDy":26,"toggleDx":-70,"toggleDy":4,"pitch":66,"hit":[0,-4,360,52]},
 "toggle": {"w":54,"h":24,"border":2,"fill":[4,4,46,16],"thumb":[12,26],"thumbOffX":1,"thumbOnX":41,"thumbDy":-1},
 "field": {"caption":13,"value":16,"valueDy":18,"gap":12,"pitch":"20+H+12"},
 "slider": {"caption":13,"pct":14,"trackDy":24,"trackH":4,"thumb":[10,18],"thumbDy":-7,"hitH":46,"notch":10},
 "textbox": {"caption":13,"captionAdv":22,"boxH":38,"text":17,"textDx":8,"textDy":8,"after":16},
 "picker": {"caption":15,"captionAdv":24,"rowH":40,"text":17,"textDx":10,"textDy":9,"openMs":250,"closeMs":200,"after":18,"border":2},
 "button": {"h":40,"stroke":2,"label":14.5,"labelDy":10,"after":12,"storeH":46,"storeLabel":17},
 "round": {"d":44,"ring":2.2,"label":11.5,"labelDy":47,"hit":[68,70]},
 "menu": {"row":50,"pad":16,"text":24,"scrim":0.72},
 "tilt": {"deg":14,"lift":40,"sink":0.045,"inMs":70,"outMs":160,"fovDeg":34,"cells":[12,4]},
 "dots": {"count":5,"size":3,"y":3,"stagger":160,"travel":1700,"period":2600},
 "hold_ms": 500, "slop": 8,
 "hapticKinds": ["tick","tap","click","heavy"]
}
```

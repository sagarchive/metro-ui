# Windows Phone 8.1 Motion Specification, Part B: Shell Motion

Measured and reconstructed shell-level motion: Start and app-list turnstile, tile press and flip, overlays, switcher, lock screen, boot sequence. Units: ms, degrees, points on a **360 x 740 pt** screen (4 px per pt). Related areas: Start/tiles and surfaces, covered in companion specs. Tags: **(inferred)** = reconstructed; **(unverified)** = not confirmed.

## 1. Engine

### 1.1 Global time scale

`effectiveMs = ms * 100 / animationSpeed`. **The default animation speed setting is 75 %** (range 25 to 300 %; 100 % is "as measured on the Lumia reference device"), so every duration **and delay** in this document is stretched by **x1.333** by default. Slow-motion is a further x5. All numbers below are the base (100 %) values; multiply by `100/animationSpeed` for effective time (1.33 at the default). Recommendation for a kit: expose a motion-speed variable where 1.0 equals the 100 % measurement.

### 1.2 Value animation model

- A new animation retargets from the variable's current value; each animated variable has a single slot.
- Default easing is **exponential ease-out**, normalised so it ends exactly at 1:
```js
const easeOutExpo = t => (1 - Math.pow(2, -10 * t)) / (1 - 1 / 1024);
const linear = t => t;
```
CSS approximation: `cubic-bezier(0.19, 1, 0.22, 1)` (standard easeOutExpo); prefer the JS formula for exactness. There is **no ease-in or ease-in-out anywhere** except the linear option.
- Back-ease-out with overshoot (live-tile flip only):
```js
const backOut = (t, o) => { const c1 = 1.70158 * o / 0.1, c3 = c1 + 1, u = t - 1; return 1 + c3*u*u*u + c1*u*u; };
```
(o = 0.08 gives c1 = 1.3613.)
- Time is wall-clock, not frame count. A jump is a 1 ms linear animation.

### 1.3 Spring and physics integrators (sub-step <= 4 ms)

```js
// critically damped spring to target, w = k (per ms): v += (-w*w*x - 2*w*v)*dt; x += v*dt
// page (Start<->list): w = 0.018   switcher row: w = 0.014   scroll overscroll: w = 0.016
// stop when sign of (pos - target) flips, or tiny.   Scroll coast: v *= exp(-dt/380)
// tile glide after reorder: off *= exp(-dt/70)
```

### 1.4 Projection (shared by all 3D motion)

Vertical field of view 34 deg; eye distance `d = (H/2)/tan(17 deg) = 1210 pt` at H = 740; the plane z = 0 is the screen; `w = 1 - z/d` (nearer = bigger); the vanishing point is the screen centre. CSS: `perspective: 1210px; perspective-origin: 50% 50%` on the root; the model transforms below are applied about the stated pivots. Positive `rotateY` carries the **right-hand side away** from the viewer, matching CSS `rotateY(+)`. Positive `rotateX` carries the bottom away, matching CSS `rotateX(+)` (top toward the viewer, bottom away).

## 2. Catalogue of animations

| # | Thing | Trigger | Property | From -> To | Dur ms | Delay | Easing |
|---|---|---|---|---|---|---|---|
| 1 | Tile press | touch down on tile | tiltX/Y, scale | 0 -> (+-14 deg * fx, fy), 1 -> 0.88 | 70 | 0 | expo |
| 2 | Tile release | finger up, or move > 8 pt | same | -> 0, 1 | 160 | 0 | expo |
| 3 | List row press/release | row touch | tiltY = fx*14*.7, tiltX = fy*14, scale .91 | | 70 / 160 | | expo |
| 4 | Quick tile press | shade | tilt 14 deg, scale .97 | | 70 / 160 | | expo |
| 5 | Edit mode in/out | long-press 450 | edit amount 0 <-> 1: held tile scale 1.06, others .92 and dim .55, badges fade after 0.3 | | 180 | 0 | expo |
| 6 | Tile reorder glide | reorder (debounce 220 ms) | offset decays | | tau 70 | | exponential decay |
| 7 | Live tile flip | timer (see Start/tiles spec) | rotateX 0 <-> 180 | | 520 | | back-out o = .08 |
| 8 | Live tile flip back to front (file gone) | | flip -> 0 | | 500 | | expo |
| 9 | Pin arrival | pin | tile scale .4 -> 1 | | 320 | 220 (page duration minus 80) | expo |
| 10 | Start <-> app list page | swipe / arrow / search | page 0 <-> 1 | spring | | | k = .018 |
| 11 | Context menu open / close | long press row | scaleY 0 -> 1 about centre, veil .5 | | 200 / 140 | | expo |
| 12 | Turnstile out/in (Start) | launch / return | see section 3 | | out / return duration | | linear clock + per-tile curve |
| 13 | App swing in | map | angleY 80 -> 0, alpha 0 -> 1 | | 350 | 0, or (out duration - 55) | expo |
| 14 | App swing out | Start tapped / close | angleY 0 -> 80, alpha 1 -> 0 | | 250 | 0 | expo |
| 15 | Black gap | | between out and in | | 110 (forward) / 150 (back) | | |
| 16 | Loading text/dots | pending launch | alpha 0 -> 1 over 150 ms, dots on clock | | | after (start-out duration + 110) + 150 | linear |
| 17 | Switcher open/close | long-press Start | switcher amount 0 <-> 1 | | 260 | | expo |
| 18 | Switcher pick | tap card | position -> i, amount -> 0 | | 260 | | expo |
| 19 | Card removed | forget | position -> last | | 180 | | expo |
| 20 | Card dismiss fly-off | up-swipe / fling | drop -> -H | | clamp((H+drop)/max(-vy, 2.2), 90, 240) | | linear |
| 21 | Card cancel | released short | drop -> 0 | | 260 | | expo |
| 22 | On-screen keyboard slide | show/hide | 0 <-> 1 (y = H - 40 - keyboardHeight * s) | | 200 | | expo |
| 23 | App lift for keyboard | | lift | | 200 | | expo |
| 24 | Shade settle | release / close | shade height -> 700 / 0 | | 260 | | expo |
| 25 | Peek in / out | hold 320 | peek 0 -> 1 / -> 0 | | 180 / 220 | | expo |
| 26 | Status icons | link change | wifi/tech/arrow 0 <-> 1 (scale .25 + .75t, alpha t) | | 150 in / 70 out | tech/arrow in: +70 | expo |
| 27 | Charging-plug blink | 1 s timer | alpha hard toggle | | snap | | none |
| 28 | Toast in | notification | swivel 0 -> 1 (rotX -45*(1-t), alpha t) | | 300 | | expo |
| 29 | Toast out | 4500 ms / tap | -> 0 | | 199 | | expo |
| 30 | Volume in | key | y -H -> 0 | | 140 | | expo |
| 31 | Volume out | 2000 / 4000 ms | -> -bannerHeight | | 180 | | expo |
| 32 | Dialog in / out | dialog | y -h -> 0 / 0 -> -h | | 260 / 170 | | expo |
| 33 | Search overlay in / out | search button | 0 -> 1 (y +40 -> 0, alpha) / -> 0 | | 250 (expo) / 180 (linear) | | |
| 34 | Lock unlock | swipe > H/5 | lock y -> -H | | 200 | | expo |
| 35 | Lock tap-hint | tap | -26 -> 0 | | 320 | | expo |
| 36 | Lock cancel | short swipe | -> 0 | | 220 | | expo |
| 37 | Boot nav icons | boot | y 60 -> 0 each | | 480 | 700 / 1050 / 1400 | expo |
| 38 | Boot lock drop | boot | lock y -H -> 0 | | 750 | 2200 | expo |
| 39 | Marquee on live-tile back | | slide 30 pt/s, rest 1200 ms | | | | linear |
| 40 | Brightness and others | no animation | | | | | |

Haptic pairing: tile tap TAP, nav-key down TAP, long-press HEAVY, reorder TICK, resize/unpin CLICK, toast HEAVY, key press 7 ms. Pulse parameters: TICK 14 ms at 0.385, TAP 18 ms at 0.525, CLICK 24 ms at 0.63, HEAVY 38 ms at 0.7, KEY 7 ms at 0.28; user strength 80 %.

## 3. Turnstile (Start tiles and list rows), exact model

### 3.1 Clock

```js
const TILE_ROW_MS=50, TILE_LEFT_MS=51, TILE_OUT_LIFE_MS=85, TILE_TAPPED_WAIT_MS=80, TILE_TAPPED_LIFE_MS=55,
      TILE_LIFE_MS=186, TILE_LAST_LATE_MS=70, TILE_SMALL_EARLY_MS=33, JIT_START=6, JIT_SPEED=.05, JIT_TRAVEL=.15;
const pitch = 2*W/units;                      // 120 pt @6 units: "one medium row"
// rows = (bottom-top of what is on screen)/pitch, at least visible/pitch + 1, visible = H-28-40 = 672
const startRows = Math.max(spanOnScreen/pitch, 672/pitch + 1);
outMs    = 50*(rows-1 > 0 ? rows-1 : 0) + 51 + 85 + 80 + 55;
returnMs = 50*rows + 51 + 186*1.35 + 6;
// the turnstile clock runs 0->1 (leaving) / 1->0 (returning) LINEARLY over outMs / returnMs (x time scale)
```
The turn bottom is the bottom of the lowest on-screen tile, so with few tiles nothing waits for empty rows. Per tile: `rowsUp = (turnBottom - (t.y + t.h)) / pitch` (>= 0), `cx = (t.x + t.w/2)/W`, `left = clamp((0.75 - cx)/0.5, 0, 1)` (1 = left column, 0 = right column), `small = size == small`, `last = row == 0 && col == 0`, `tapped` = this is the tapped tile.

### 3.2 Per-tile progress `turn` (0 at rest, 1 gone)

Leaving:
```js
let start = 50*rowsUp + 51*left; if (small) start -= 33;
let life = 85, others = outMs - 80 - 55;
if (tapped) { life = 55; start = outMs - life; } else if (start + life > others) start = others - life;
start = Math.max(0, start);
turn = clamp((clock*outMs - start) / life, 0, 1);       // clock*outMs = elapsed ms (pre-scale)
```
Returning:
```js
let start = 50*rowsUp + 51*left, life = 186;
if (small) { start -= 33; life *= 0.8; }
start += 6*jitStart; life *= 1 + 0.05*jitSpeed;           // jit* uniform -1..1, redrawn every return
if (last) start += 70;
if (start + life > returnMs) start = returnMs - life; start = Math.max(0, start);
const elapsed = (1 - clock) * returnMs;
turn = elapsed >= start+life ? 0 : 1 - clamp((elapsed - start)/life, 0, 1);
```
Draw order when returning: tiles with the most remaining turn are drawn first (landed ones overlap). The tile being edited is always on top.

App-list rows use the same function with `rowsUp = (listTurnBottom - (y+45))/pitch`, `left = 0.5`, `small = true`, and per-row jitter derived from a hash.

### 3.3 Geometry per tile

Pivot/hinge: a tile hinges on its **right edge if its centre is left of the screen centre (`cx < W/2 - 1`), otherwise on its left edge** (the edge nearest the centre line; list rows and the arrow button use the left edge). Model: `translate3(hingeX + dx, y + h/2, z) -> rotateY(angle) -> translate(+-w/2, 0)`, then tile lean/flip/scale about the centre.

**Leaving**, with `turn` in [0,1]:
```js
angle = -45 * turn*turn;                       // right edge toward viewer for left-hinged
z     =  0.09 * eye * turn*turn;               // 0.09*1210 = 109 pt toward viewer
dx    = -(0.047 + (0.098-0.047)*rightness) * W * Math.pow(turn, 2.5);   // rightness = (x+span/2)/W clamped 0..1 ; sweeps left 17..35 pt
alpha = turn < 0.7 ? 1 : turn >= 1 ? 0 : (1 - turn)/0.3;                // solid until 70%
```
**Returning** (local `u = 1 - turn`, 0 = just set off, 1 = landed):
```js
angle = 69.8 * Math.exp(-2.649*u) * Math.pow(1-u, 0.165);
z     = -0.182 * eye * Math.exp(-1.656*u) * (1-u);          // starts 220 pt behind the screen
dx    = span * ( -0.476*Math.exp(-7.157*u) + (1 + 0.15*jitTravel)*0.193*Math.exp(-0.849*u) ) * Math.sqrt(1-u);
shade = (0.7 + 0.3*Math.cos(angle*Math.PI/180)) * (u<=0 ? 0 : u<0.08 ? u/0.08 : 1);   // used as alpha (darkens/hides until set off)
```
`span` is the tile width (list rows and the arrow button use 110). A returning tile therefore starts 0.476 x width to the **left** of its place, passes about 0.08 x width beyond it to the right (about 60 ms in), then settles; the fit is least-squares to a 215 px-wide reference tile over 12 frames, 2.9 px rms.

Port notes: per frame compute `turn`, then set `transform: translate3d(dx, 0, z) rotateY(angle)` with `transform-origin` at the hinge edge (right edge for left-half tiles), `opacity = alpha`, and `perspective: 1210px` on the parent.

### 3.4 Which transition where

| Event | Start tiles | App |
|---|---|---|
| Tap tile/row (cold) | out: tiles turn away, tapped tile last | first-party apps: alpha 0 -> 1 at launch time + (outMs + 110) * 100/animationSpeed (1 ms linear), the app plays its own entrance; third-party apps wait until they report ready; others: angle 80 -> 0 plus alpha in over 350 ms after a delay of `outMs - 55` (first show) or 0 (resume) |
| Resume running app | same | app swings in with delay 0 if not the first time |
| Back to Start (nav Start / app closed) | after 250 + 150 ms: turnstile in (returnMs) | app 0 -> 80 deg, alpha -> 0, 250 ms |
| App crashes or closes itself | after 150 ms black: turnstile in | none |
| Launch times out (30 s) | turnstile in | |
| Switcher pick | no turnstile; Start clock snapped to 1 | card grows |

For apps, the turn-out and turn-in angles are both 80 deg; the app turns around the **screen's left edge** (x = 0) in the same projection; app alpha `= min(1, appAlpha*4) * turnAlpha(|angle|/80)` where `turnAlpha(x) = x<.7 ? 1 : x>=1 ? 0 : (1-x)/.3`.

Of the named platform transitions (turnstile, continuum, swivel, readerboard, slide-up-fade), **only turnstile (Start and apps) and swivel (toast) occur at shell level**; continuum, readerboard and slide-up-fade belong to in-app motion (see Part A). The search overlay uses a 40 pt rise plus fade.

### 3.5 Measured reference timings

Reference device (Lumia 820) at 60 fps: tiles out about 270 ms from the bottom row up, tapped tile about 130 ms after, black about 110 ms, app in about 300 ms; closing: app out about 250 ms, black about 150 ms, tiles in about 270 ms. Leaving tile angles 10, 25, 40 deg over three frames, growing about 10 %, swept left about 24 px of 508 (left edge) and 50 px (right).

## 4. Other formulas ready to port

### 4.1 Swivel toast

```css
.toast{transform-origin:50% 0; transform:perspective(1210px) rotateX(calc(-45deg * (1 - var(--t)))); opacity:var(--t);}
/* --t: 0 -> 1 in 300 ms easeOutExpo; hold 4500; 1 -> 0 in 199 ms */
```
Sign note: in the measurement convention a positive rotateX carries the bottom away, so -45 swings the bottom *toward* the viewer first. In CSS use whichever sign makes the banner fall from above toward the viewer; verify visually.

### 4.2 Shade reveal (not a translate)

```js
reveal = shadeHeight;           // 0..700
veilAlpha = 0.6 * reveal/700;                  // black over y 28..700
clip(panel, y: 0 .. max(0, reveal-16));        // panel contents fixed in place
drawBar(y = reveal - 16 .. reveal);            // 16 pt accent bar slides down uncovering it
```

### 4.3 Lock drag

`lockY = Math.min(0, y - y0)`; release beyond H/5 animates to -H in 200 ms.

### 4.4 Switcher card

```js
sc = 1 - 0.4*t; pitch = W*sc + 18;
x = W/2 + (switchX - i)*pitch - sc*W/2; y = 28 + (672 - sc*672)/2 - 10*t;
```
Flick settle target `round(switchX + vx/pitch*170)`.

### 4.5 Edit mode dimming

```js
held: scale = 1 + .06*e; others: scale = 1 - .08*e, opacity *= 1 - .45*e;   // e = edit amount (180 ms)
```

### 4.6 Loading dots

```js
for i in 0..4: k = ((t % 2600) - i*160)/1700; if (0<k<1) { u = 2k-1; x = W*(0.5 + 0.5*(0.25*u + 0.75*u*u*u)); draw 3x3 accent at (x-1.5, mid-12) }
// slow in the middle, fast at the ends (cubic); text alpha = min(1, (since-gone)/150)
```

## 5. Timers that affect motion

| Timer | Value | Use |
|---|---|---|
| Long press | 450 ms | tile edit, row menu, nav-key long press, keyboard trackpad |
| Peek hold | 320 ms | status bar hold |
| Toast | 4500 ms | |
| Volume | 2000 / 4000 ms | |
| Network / Bluetooth / live-tile tick | 1000 ms | plug blink, live flips (at most one per tick) |
| Clock | on the minute (+50 ms) | status and lock text |
| Idle sleep | 60 s | |
| Reorder debounce | 220 ms | |
| Launch wait | 30 000 ms | |
| Third-party app ready fallback | 4000 ms | uncover the app anyway |

## Kit-ready constants

```json
{
  "engine": {"defaultAnimationSpeed": 75, "speedFormula": "ms*100/animationSpeed", "slowMotionX": 5,
    "ease": "(1-2^(-10t))/(1-2^-10)", "backOut": "1+c3*u^3+c1*u^2, c1=1.70158*o/0.1, u=t-1",
    "fovDeg": 34, "eye@740": 1210, "springK": {"page": 0.018, "switcher": 0.014, "overscroll": 0.016}},
  "turnstile": {"rowMs": 50, "leftMs": 51, "smallEarlyMs": 33, "outLifeMs": 85, "tappedWaitMs": 80, "tappedLifeMs": 55,
    "inLifeMs": 186, "inLifeSmallX": 0.8, "lastLateMs": 70, "jitter": {"startMs": 6, "speed": 0.05, "travel": 0.15},
    "returnMsFormula": "50*rows+51+186*1.35+6", "outMsFormula": "50*(rows-1)+51+85+80+55",
    "out": {"degMax": 45, "angleExp": 2, "depthEye": 0.09, "sweepL": 0.047, "sweepR": 0.098, "sweepExp": 2.5, "solidUntil": 0.7},
    "in": {"deg": 69.8, "kAngle": 2.649, "pAngle": 0.165, "depthEye": 0.182, "kZ": 1.656,
      "dx": {"a": -0.476, "ka": 7.157, "b": 0.193, "kb": 0.849}, "shadeBase": 0.7, "shadeRampU": 0.08},
    "gapMs": {"turn": 110, "back": 150}},
  "app": {"inDeg": 80, "outDeg": 80, "inMs": 350, "outMs": 250, "alphaGain": 4, "solidUntil": 0.7},
  "tilt": {"deg": 14, "inMs": 70, "outMs": 160, "press": 0.88, "shadePress": 0.97, "rowPress": 0.91},
  "flip": {"ms": 520, "overshoot": 0.08, "backStayMs": [5000, 8000], "frontStayMs": [4000, 10000], "tickMs": 1000},
  "edit": {"ms": 180, "held": 0.06, "others": -0.08, "dim": 0.45},
  "overlays": {"toastInMs": 300, "toastHoldMs": 4500, "toastOutMs": 199, "volumeInMs": 140, "volumeOutMs": 180,
    "dialogInMs": 260, "dialogOutMs": 170, "shadeMs": 260, "peekInMs": 180, "peekOutMs": 220, "oskMs": 200,
    "switcherMs": 260, "hyperInMs": 250, "hyperOutMs": 180, "menuInMs": 200, "menuOutMs": 140,
    "statusInMs": 150, "statusOutMs": 70, "unlockMs": 200, "lockBounceMs": 320, "bootNavMs": 480, "bootLockMs": 750}
}
```

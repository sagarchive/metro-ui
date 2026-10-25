# Windows Phone 8.1 Motion Specification, Part A: In-App Motion

Measured and reconstructed behaviour of in-app motion: easing primitives, named transitions, page change (turnstile), pivot swipe and spring, scrolling physics, press/tilt, picker, loading dots, haptic timing.

Conventions: all lengths are in points on a 360-pt-wide screen (4 px per pt); all times are in ms. Tags: **(inferred)** = reconstructed from observed behaviour or naming rather than directly measured; **(unverified)** = intent or value not confirmed. Bezier fits were computed offline (grid search plus hill-climb, 200 samples on x, maximum |y error| over 51 sample points). The exact formulas in section 1 are preferable to the beziers wherever script is available (Web Animations `linear()` or requestAnimationFrame).

**Animation speed setting.** The platform's default animation speed setting is 75 %, which stretches every duration and delay listed in the shell part (06b) by 1.33 (100/75). In this document, the entrance animation (section 3.4) is the only motion that follows that setting (rate = 100 / speed percent, range 50 to 200 %, slow-motion adds a further x5); the page-change constants in 3.1 are fixed (inferred). The numbers below are the base (100 %) values.

## 1. Easing primitives

Curves are reconstructed from the weights of the platform's named curves (**inferred**; the shapes are what the shipping system plays and were tuned against a real device). With `k = w/30`, t in [0,1]:

```js
const EXP  = (w,t)=>{const k=w/30; return (Math.exp(k*t)-1)/(Math.exp(k)-1)};            // gathers speed ("things leaving")
const LOG  = (w,t)=>{const k=w/30; return 1-(Math.exp(k*(1-t))-1)/(Math.exp(k)-1)};      // settles ("things arriving")  LOG(w,t)=1-EXP(w,1-t)
const SCURVE=(w,t)=>{const f0=1/(1+Math.exp(w/2)), f1=1/(1+Math.exp(-w/2));              // logistic, normalised; w = steepness (NOT w/30)
                    return (1/(1+Math.exp(-w*(t-.5)))-f0)/(f1-f0)};
const clamp01=v=>Math.min(1,Math.max(0,v));
```

| Curve | cubic-bezier approximation | max error | Sample values at t=.1/.25/.5/.75 |
|---|---|---|---|
| EXP 60 (k=2) | `cubic-bezier(0.468, 0.145, 0.763, 0.454)` | 0.0002 | .035 / .102 / .269 / .545 |
| LOG 60 | `cubic-bezier(0.237, 0.546, 0.532, 0.855)` (mirror of EXP60: (1-c,1-d,1-a,1-b)) | 0.0003 | .210 / .455 / .731 / .898 |
| EXP 150 (k=5) | `cubic-bezier(0.554, 0.024, 0.813, 0.064)` | 0.0004 | |
| LOG 150 | `cubic-bezier(0.183, 0.911, 0.425, 0.979)` | 0.0006 | |
| LOG 200 (k=6.67) | `cubic-bezier(0.153, 1.000, 0.342, 0.996)` | 0.0017 | |
| SCURVE 7.5 | `cubic-bezier(0.534, 0.069, 0.467, 0.931)` | 0.0017 | |
| LOG 10 (tile flip, stage 1) | `cubic-bezier(0.502, 0.588, 0.887, 0.902)` | 0.0005 | |
| SCURVE 10 (tile flip, stage 2) | `cubic-bezier(0.613, -0.019, 0.388, 1.020)` | 0.0043 | |
| t^2 (row out) | `cubic-bezier(0.312, 0, 0.645, 0.290)` | 0.0002 | |
| 1-(1-t)^2 (press, picker (inferred)) | `cubic-bezier(0.259, 0.518, 0.599, 1)` | 0.0001 | |
| 1-(1-t)^3 (row in, picker) | `cubic-bezier(0.194, 0.550, 0.401, 1.048)` (CSS `easeOutCubic` 0.215,0.61,0.355,1 is 0.022 off) | 0.0039 | |

The EXP60/LOG60 fits are essentially exact (a bezier of an exponential at k=2 is near-perfect); weights of 150 and above are steeper than a bezier can follow past the first 5 % (error figures hold for the 51 sampled points).

## 2. Named transitions

Fields: `axis` (Y = rotate about the **vertical** edge, pivot = fraction of width; X = about the **horizontal** edge, pivot = fraction of height; Z = in-plane rotation, pivot at centre), `from/to deg`, `pivot`, `from/to scale` (about the element centre), `from/to dy` (pt, + = down), `from/to alpha`, duration, curve. A single eased value `e = curve(w, t)` drives all channels linearly: `deg = from+(to-from)e`, likewise scale, dy and alpha.

| name | axis | deg | pivot | scale | dy | alpha | ms | curve (w) |
|---|---|---|---|---|---|---|---|---|
| turnstile-in | Y | -80 -> 0 | 0 (left) | 1 | 0 | 0 -> 1 | 350 | LOG 60 |
| turnstile-out | Y | 0 -> 50 | 0 | 1 | 0 | 1 -> 0 | 128 | EXP 60 |
| swivel-in | X | -60 -> 0 | 0.5 | 1 | 0 | 0 -> 1 | 300 | LOG 200 |
| swivel-out | X | 0 -> 60 | 0.5 | 1 | 0 | 1 -> 0 | 199 | EXP 60 |
| continuum-hide | X | 0 -> 80 | 0 (top) | 1 | 0 -> 120 | 1 -> 0 | 120 | EXP 60 |
| continuum-show | X | -50 -> 0 | 0 | 1.5 -> 1 | -60 -> 0 | 0 -> 1 | 350 | LOG 60 |
| readerboard-in | X | -45 -> 0 | 0 | 1 | 0 | 0 -> 1 | 166 | LOG 60 |
| readerboard-out | X | 0 -> 90 | 0 | 1 | 0 | 1 -> 0 | 166 | EXP 60 |
| slide-up-fade-in | none | 0 | - | 1 | 24 -> 0 | 0 -> 1 | 240 | LOG 150 |
| rotate-90 | Z | 90 -> 0 | 0.5 | 1 | 0 | 1 -> 1 | 167 | SCURVE 7.5 |
| fade-in | - | 0 | - | 1 | 0 | 0 -> 1 | 350 | LOG 150 |
| fade-out | - | 0 | - | 1 | 0 | 1 -> 0 | 150 | EXP 150 |
| tile-flip-notify | X | -180 -> 35 -> -6 -> 0 | 0.5 | 1 | 0 | 1 | 520 | 3-stage, below |

Tile flip (three stages over 520 ms):
- `t < .367`: `deg = -180 + 215*LOG(10, t/.367)`
- `.367 <= t < .833`: `deg = 35 - 41*SCURVE(10, (t-.367)/.466)`
- otherwise: `deg = -6 + 6*(t-.833)/.167` (linear)

Notes:
1. For multi-row transitions (turnstile, readerboard) successive rows are offset by a 33 ms feather; single elements have no feather. Two further variants exist: **turnstile backward in** (50 -> 0, 350 ms, LOG 60, last row first) and **turnstile backward out** (0 -> -80, 128 ms, EXP 60, last row first). Fade-in and slide-up are described as "Exp 150" in some descriptions, but the measured behaviour is a LOG (settling) curve; use LOG.
2. Sign convention in this section: positive Y-axis degrees tip the **right side toward the viewer**, the opposite of the row turn in section 3 (positive = away). In CSS: Y-axis entries = `rotateY(calc(var(--deg)*-1deg))` (CSS positive rotateY sends the right side away); X-axis entries = `rotateX(var(--deg)*1deg)` (CSS positive rotateX brings the bottom toward the viewer); Z = `rotate(deg)` (positive = clockwise on a y-down screen, same as CSS) (sign inferred).
3. Geometry for an element (x, y, w, h): corners relative to the centre are rotated about the pivot line, scaled about the centre, then moved by dy; perspective uses the eye distance in 3.3.
4. Reference staging: 4 rows of 46 pt with 8 pt gaps; run time = ms + 3 x feather; 700 ms hold between loops.

CSS skeleton for one transition:
```css
.anim{perspective:1099px;perspective-origin:50% 50%}
.row{transform-origin:calc(var(--pivot)*100%) 50%; /* axis Y: pivot along x */
     transform:translateY(calc(var(--dy)*1px)) scale(var(--s)) rotateY(calc(var(--deg)*-1deg));opacity:var(--a)}
```
Drive `--deg --dy --s --a` from the JS curve each frame. Keyframes between two points need a `linear()` easing sampled from the formula, or the bezier above, because only EXP/LOG 60 are well approximated by a single bezier.

## 3. Page change (the turnstile), in-app

### 3.1 Constants

| Constant | Value | Note |
|---|---|---|
| Row out | 128 ms | matches the platform's forward-turnstile-out duration of 0.128 s |
| Row in | 180 ms | the platform's Settings app measures about 150 ms; 180 is the tuned value |
| Row stagger | 33 ms | one frame of 30 fps video |
| Gap | 120 ms | black screen between the two pages |
| Turn out angle | 50 deg | |
| Turn in angle | 80 deg | |
| Field of view | 34 deg | eye distance `d = (H/2)/tan(17deg)`; H = window height (672 -> d = 1099 pt) |
| Strip slices | 16 | only for a software-rendered fallback |
| Entrance: row stagger / row life / title life / hold | 28 / 190 / 200 / 60 ms | app's first page |

### 3.2 Rows and order

A "row" is a horizontal strip of the page between consecutive **full-width hit targets** (width >= 0.9 x 360, excluding the Back target, spaced more than 8 pt apart, at most 30). The first strip (0 to the first target) is the header plus whatever is above it. Order index = row index top-down; the **tapped row is moved last** (rows after it close up). Going back, or closing, reverses the order (bottom-up). Up to 32 rows. Targets narrower than 90 % of the width (switch toggles, tiles) do not create row boundaries.

Total duration: `out = maxOrder_out*33 + 128`; `total = out + 120 + maxOrder_in*33 + 180`. The destination is rendered during the black gap; if rendering overruns, the clock shifts so the arrival still receives its full duration. Example with 10 rows each side: 425 + 120 + 477 = 1022 ms. Closing plays the out phase only; first launch plays the in phase only (entrance).

### 3.3 Per-row maths

Leaving row, `m = elapsed - order*33`:
```
t = clamp01(m/128);  e = t*t                       // gathering speed
deg = (back ? +50 : -50) * e                       // forward: right edge swings TOWARD viewer; back: away
alpha = e<0.7 ? 1 : (1-e)/0.3                      // solid, gone only in the last ~16 % of time
```
Arriving row (non-entrance), `m = elapsed - in_start - order*33`:
```
t = clamp01(m/180); e = 1-(1-t)^3                  // settling
deg = 80*(1-e)  (positive = right edge AWAY from viewer: new rows arrive from behind the screen)
alpha = e>0.3 ? 1 : e/0.3
```
A row that has not started (t <= 0) is not drawn (black). Rotation is about the **left edge** (x = 0) of the full-width strip; the strip's vertical extent y0..y1 is preserved and scaled in perspective.

Projection: for strip points x in [0,360] with turn angle a, depth offset `z0`, shift `dx`:
`s(x) = d/(d - z0 + x sin a)`; screen x = `180 + (x cos a + dx - 180) s`; vertical scale about the strip's mid line `cy`: `y' = cy + (y-cy) s`.

CSS equivalent per strip: `perspective:1099px; perspective-origin:50% (strip centre); transform-origin:0 50%; transform: translate3d(dx,0,z0) rotateY(a deg)`, where positive `a` takes the right side away (CSS `rotateY(+a)`) and the forward-out turn is CSS `rotateY(-50*e)`.

Row images are the page rendered once and only moved (no per-frame redraw). Strips are drawn at full width with no gutters; between rows there is only the black background.

Relation to the named table: row-out uses `t^2` over 128 ms (named table: EXP 60, 128 ms, same duration); row-in uses cubic-out over 180 ms versus the named LOG 60 over 350 ms from -80 deg. The in-app version trades duration for feel (the platform's Settings app is about 150 ms). **Both are valid: use the in-app values for apps, the table values for dialogs and OS chrome.**

### 3.4 Entrance (an app's first page)

All rows of the first page (and the title strip, `y0 < 1`) arrive once Start has been hidden. Per-row start = `order*28*rate`, life = `190*rate` (title strip `200*rate`), where `rate = 100/animation_speed_percent` (50 to 200 %; slow-motion x5 multiplies rate by 5). A touch more than 60 ms after the start jumps to the end. Per-row shaping uses the same fitted curve as the Start tiles' return:

```js
function entrance(t, eye){ t=clamp01(t); const l=1-t;
  const angle  = 69.8*Math.exp(-2.649*t)*Math.pow(l,0.165);          // deg, + = right edge away
  const depth  = -0.182*eye*Math.exp(-1.656*t)*l;                    // pt along z (negative = farther)
  const travel = 110*(-0.476*Math.exp(-7.157*t)+0.193*Math.exp(-0.849*t))*Math.sqrt(l); // pt in x
  const alpha  = (0.7+0.3*Math.cos(angle*Math.PI/180))*Math.min(1,t/0.08);
  return {angle,depth,travel,alpha}; }
```
Samples (eye = 1099): t=0 -> angle 69.8, depth -200, travel -31.1, alpha 0; t=.08 -> 55.7, -161, -9.3, .87; t=.2 -> 39.6, -115, +4.8, .93; t=.4 -> 22.2, -62, +9.4 (overshoot to the right), .98; t=.6 -> 12.2, -30, 7.6, .99; t=.8 -> 6.4, -10.6, 4.7, 1; t=.95 -> 3.4, -2.1, 2.1, 1; t=1 -> 0.

Rows enter rotating from about 70 deg behind the screen, 31 pt to the left and 200 pt deep, fading in over the first 8 % of their life, overshoot 9 pt to the right at t of about 0.4, and settle at t=1. There is a visible final snap in the last 5 % because of the `(1-t)^0.165` term.

Total entrance duration = `(last*28 + 190)*rate` (or the title's `200*rate` if longer), plus up to 6 s of deferral until the shell reveals the app.

### 3.5 Input during motion

Touch-down during a page change is ignored (hit targets cleared). During a row-by-row entrance a touch after 60 ms ends it. Back/close while animating is ignored.

## 4. Pivot swipe and spring

Setup: when a pivot page has been idle for 150 ms, both tabs are pre-rendered. Tabs lie side by side, **one window width (360) apart**, as an endless strip A B A B ...; `swipe_dx` is the strip offset (negative = moved left to reveal the next tab).

- Under the finger: `swipe_dx = swipe_grab + (x - down_x)`, 1:1 (no resistance, no clamp: the strip is endless). Axis lock: flat movement beyond 18 pt, angle <= 20 deg.
- Titles: strip position `strip = titleAt(k0) + f*(titleAt(k0+1)-titleAt(k0))`, `u = -swipe_dx/360`, `k0 = floor(u)`, `f = u - k0`; `titleAt(k)` is the sum of title widths `a = W(this)+16`, `b = W(next)+16` alternately. So **the title strip moves one title-width per tab (360 pt) of body travel** (parallax). Each title's opacity is `0.38 + 0.62*clamp01((180 + 30 - |u-k|*360)/60)`: fully white when its tab is within +-30 pt of centred, fading to 38 % (grey #616161) by +-90 pt (light = 1 at distance <= 30 pt, 0 at >= 90 pt). The caps line stays (alpha 1, y 0..32). A second threshold constant of 50 pt appears alongside the 60 pt light-ramp divisor; its intent is **unverified** and it has no observable effect.
- Release: filtered velocity `vx` in pt/ms, `vx = 0.4 vx + 0.6 dx/dt`; zero if the finger rested more than 80 ms. Target tab `k`: `vx < -0.3 -> floor(u)+1`; `vx > +0.3 -> ceil(u)-1`; else `round(u)`; `target = -k*360`.
- Spring (critically damped, integrated in steps of <= 4 ms, dt <= 50 ms per frame): with `K = 0.018 /ms`, `v += (-K^2 (x-T) - 2K v) dt;  x += v dt`, starting at the finger's `x` with `v = vx`. It ends when it would cross T, or when `|x-T| < 0.4` and `|v| < 0.02`; it never overshoots. Closed form for v0 = 0: `(x-T)/(x0-T) = (1+Kt)e^{-Kt}`, giving 50 % at 93 ms, 90 % at 216 ms (the "quarter second"), 99 % at 369 ms, and the final snap at about 520 ms (simulated for a full 360 pt move). A touch that catches the slide re-grabs the strip at its current offset.
- Tap on the next title: a full-screen move from rest (`v = 0`) with the same spring, so about 520 ms.
- Landing on the odd tab swaps the pages, resets scroll to 0, and fires the page's "arrived" event (apps start loading). Landing on the same tab does not swap.

CSS: tween `x` with the closed form `x(t) = T + ((x0-T) + ((v0 + K (x0-T))) t) e^{-Kt}` (general critically-damped solution with v0 in pt/ms, K = .018, t in ms); title strip `translateX = -strip`, body tabs at `x + k*360`.

## 5. Scrolling physics (in-app pages)

```js
// finger: v = -(dy/dt); vel = 0.4*vel + 0.6*v   (pt/ms, + = content moves up / scroll increases)
// drag: scroll = down_scroll - dy ; beyond [0,max]: excess *= 0.4 (resistance 0.4, i.e. follows 40 %)
function flingStep(dt){ dt=Math.min(dt,50);
  scroll += vel*dt;
  const bound = clamp(scroll,0,max);
  if(bound!==scroll){ vel*=Math.exp(-dt/35); scroll += (bound-scroll)*(1-Math.exp(-dt/110));   // rubber band, no bounce
     if(Math.abs(vel)<0.05 && Math.abs(bound-scroll)<0.5){scroll=bound; stop();} }
  else { vel*=Math.exp(-dt/350); if(Math.abs(vel)<0.02) stop(); } }
```
Coasting distance = `vel*350 ms` (1 pt/ms -> 350 pt before the 0.02 cutoff stops it, about 3.5 s total). Lift after more than 80 ms of rest: vel = 0. A touch on a moving list only stops it (it is not a tap). The overscroll recovery time constant is 110 ms (95 % in about 330 ms) with velocity decaying at 35 ms. There is no maximum-velocity clamp in-app. (The shell's Start screen and app list use a different set: coast tau 380, resistance 0.35, max velocity 7 pt/ms, edge velocity 1.4, spring 0.016/ms; see the shell part.)

## 6. Press and tilt

`p(t) = 1-(1-t')^2`, `t' = clamp01(elapsed/ms)`, with ms = 70 (in) and 160 (out). An interrupted press restarts from the current amount; the start of scrolling cancels it instantly. Tilt geometry is in the companion geometry spec. Buttons use a **hard fill swap** (white background, black text) on touch-down, restored on lift or cancel; no animation. Sliders: no tilt; the thumb follows the finger 1:1; a haptic "tick slide" fires every 10 %.

## 7. Picker, menu, switch

- Picker open: `p = 1-(1-t)^3` over 250 ms; close: `p = (1-t)^3` (t over 200 ms); both are ease-out-cubic of the open/closed amount. Box height grows `40 -> 40 + (n-1)*40 + 8`; option i slides from the chosen value's place to `4 + 40 i`; box fill fades in as white alpha p, the border stays 2 pt white; selected text lerps white -> accent, other options fade in as black alpha p. The page redraws each frame while 0 < p < 1.
- Context menu: appears instantly (no entrance animation in-app); scrim is 0.72 black. Opened by a 500 ms hold plus a "heavy" haptic. The named table's `swivel-in` (300 ms, LOG 200, -60 -> 0 about X) is for shell dialogs; whether the in-app menu uses it is **unverified**.
- Switch/toggle: no motion (state redraw only).
- Slider live drag: follows the finger each move, no easing.

## 8. Loading dots

Five 3 x 3 pt accent squares at y = 3. `t = (now - since) mod 2600`; dot i: `p = (t - 160 i)/1700`, visible while 0 < p < 1; `u = 2p-1`; `x = W (0.5 + 0.5 (0.25 u + 0.75 u^3))`. Each dot's travel is an odd cubic in u with speed proportional to 0.25 + 2.25 u^2, so the edges are 10x faster than the centre. Cycle: the first dot enters at 0, the last dot (i = 4) leaves at 640 + 1700 = 2340, then a 260 ms pause.

CSS: 5 elements, `animation: dot 2600ms infinite; animation-delay: i*160ms`, with keyframes over 0..65.4 % (1700/2600) of the cycle: `left: calc(50% + 50%*(0.25u+0.75u^3))`, u from -1 to 1, expressed as `left` keyframes at 0/10/20/.../100 % of the 1700 ms window with linear interpolation (sample u in 0.1 steps), then `visibility:hidden` for the rest.

The shell's "Loading..." variant fades in over 150 ms after Start has left (`alpha = min(1,(since-gone)/150)`).

## 9. Haptic timing

- `tap` at tap activation (finger up).
- `tick` at slider touch-down.
- `tick slide` at each 10 % slider notch.
- `heavy` at the 500 ms hold.

Strength and group levels follow the user's settings (default strength 80 %, groups 100 %).

## 10. Frame behaviour

Pages are rendered once and transformed on the GPU; moving pages are drawn at a raised render scale. A frame-driven loop drives everything; the target is 60 fps. The animation speed setting (options 50/75/100/125/150/200 %, default 75 % which stretches shell durations by 1.33) scales the **entrance** only; the page-change constants in 3.1 are fixed (inferred). Slow-motion x5 also affects only the entrance.

## Kit-ready constants

```json
{
 "easing": {
  "formula": {"exp":"(e^(k t)-1)/(e^k-1), k=w/30","log":"1-(e^(k(1-t))-1)/(e^k-1)","scurve":"(1/(1+e^(-w(t-.5)))-f0)/(f1-f0), f0=1/(1+e^(w/2)), f1=1/(1+e^(-w/2))"},
  "bezier": {"exp60":[0.468,0.145,0.763,0.454],"log60":[0.237,0.546,0.532,0.855],"exp150":[0.554,0.024,0.813,0.064],"log150":[0.183,0.911,0.425,0.979],"log200":[0.153,1.0,0.342,0.996],"scurve7_5":[0.534,0.069,0.467,0.931],"easeOutQuad":[0.259,0.518,0.599,1],"easeOutCubic":[0.194,0.55,0.401,1.048],"easeInQuad":[0.312,0,0.645,0.29]}
 },
 "pageChange": {"rowOutMs":128,"rowInMs":180,"staggerMs":33,"gapMs":120,"turnOutDeg":50,"turnInDeg":80,"fovDeg":34,"eyePt":1099,"outEase":"t^2","inEase":"1-(1-t)^3","outAlphaKnee":0.7,"inAlphaKnee":0.3,"tappedRowLast":true,"backBottomUp":true,"maxRows":32},
 "entrance": {"staggerMs":28,"rowMs":190,"titleMs":200,"holdMs":60,"angle":[69.8,-2.649,0.165],"depth":[-0.182,-1.656],"travel":[110,-0.476,-7.157,0.193,-0.849],"alphaRampT":0.08},
 "pivot": {"springK_perMs":0.018,"stepMs":4,"flickPtPerMs":0.3,"tabWidth":"screenW","titleParallax":"1 title width per tab","lightFullPt":30,"lightZeroPt":90,"dimAlpha":0.38,"stopPt":0.4,"stopV":0.02,"axisFlatDeg":20,"axisAcrossPt":18,"axisUndecidedPt":12,"slopPt":8,"velFilter":[0.4,0.6],"restStopMs":80},
 "scroll": {"overscrollK":0.4,"flingTauMs":350,"edgeVelTauMs":35,"edgeSpringTauMs":110,"stopV":0.02,"edgeStopV":0.05,"edgeStopPt":0.5,"dtClampMs":50},
 "press": {"inMs":70,"outMs":160,"curve":"1-(1-t)^2","maxDeg":14,"liftPt":40,"sink":0.045,"holdMs":500},
 "picker": {"openMs":250,"closeMs":200,"curve":"easeOutCubic"},
 "dots": {"count":5,"size":3,"y":3,"staggerMs":160,"travelMs":1700,"periodMs":2600,"profile":"0.5+0.5*(0.25u+0.75u^3)"},
 "namedTransitions": {
  "turnstile-in":{"axis":"Y","deg":[-80,0],"pivot":0,"alpha":[0,1],"ms":350,"curve":["log",60]},
  "turnstile-out":{"axis":"Y","deg":[0,50],"pivot":0,"alpha":[1,0],"ms":128,"curve":["exp",60]},
  "swivel-in":{"axis":"X","deg":[-60,0],"pivot":0.5,"alpha":[0,1],"ms":300,"curve":["log",200]},
  "swivel-out":{"axis":"X","deg":[0,60],"pivot":0.5,"alpha":[1,0],"ms":199,"curve":["exp",60]},
  "continuum-hide":{"axis":"X","deg":[0,80],"pivot":0,"dy":[0,120],"alpha":[1,0],"ms":120,"curve":["exp",60]},
  "continuum-show":{"axis":"X","deg":[-50,0],"pivot":0,"scale":[1.5,1],"dy":[-60,0],"alpha":[0,1],"ms":350,"curve":["log",60]},
  "readerboard-in":{"axis":"X","deg":[-45,0],"pivot":0,"alpha":[0,1],"ms":166,"curve":["log",60],"featherMs":33},
  "readerboard-out":{"axis":"X","deg":[0,90],"pivot":0,"alpha":[1,0],"ms":166,"curve":["exp",60],"featherMs":33},
  "slide-up-fade-in":{"dy":[24,0],"alpha":[0,1],"ms":240,"curve":["log",150]},
  "rotate-90":{"axis":"Z","deg":[90,0],"pivot":0.5,"ms":167,"curve":["scurve",7.5]},
  "fade-in":{"alpha":[0,1],"ms":350,"curve":["log",150]},
  "fade-out":{"alpha":[1,0],"ms":150,"curve":["exp",150]},
  "tile-flip-notify":{"axis":"X","pivot":0.5,"ms":520,"stages":[[0,0.367,-180,35,"log",10],[0.367,0.833,35,-6,"scurve",10],[0.833,1,-6,0,"linear"]]}
 },
 "turnstileFeatherMs": 33
}
```

# 09 - Sound and haptics

Design specification for Windows Phone 8.1 style sound and haptic feedback.
Tags: **(inferred)**, **(unverified)**, **(device-specific)** = depends on particular hardware; treat as a tuning starting point.

## 1. Sound categories

Ten sound categories, indexed 0-9.

| Idx | Category | Role | Target duration |
|---|---|---|---|
| 0 | key | letter / symbol key tap | ~30.5 ms |
| 1 | space | space bar | ~24.1 ms (waveform differs from function; same length) |
| 2 | function | non-character keys (shift, symbols, emoji, enter, backspace) | ~24.1 ms |
| 3 | lock | screen goes off | (unverified) |
| 4 | unlock | unlock gesture completes | (unverified) |
| 5 | notify | new notification; also a chime when the phone finishes starting | (unverified) |
| 6 | copy | copy confirmation; no triggering event defined | (unverified) |
| 7 | menu | menu open; no triggering event defined | (unverified) |
| 8 | battery-low | battery crosses a low threshold | (unverified) |
| 9 | pip | short blip on ringer volume change | (unverified) |

Keyboard sounds are very short clicks: mono, 44.1 kHz, ~1300 samples (key) and ~1060 samples (space, function). Categories 3-9 have no measured reference; synthesise or source them separately, keeping them short and unobtrusive. The stock Windows Phone sound kit is the stylistic reference; its licence is (unverified), so do not redistribute it.

Format guidance: 16-bit PCM, 1-2 channels, 44.1 or 48 kHz; mix at 48 kHz stereo.

## 2. Event map

| Event | Sound category |
|---|---|
| Letter / symbol key | key |
| Space key | space |
| Any non-character key (shift, symbols, emoji, enter, backspace) | function |
| Screen goes off (locked as it goes dark; waking is silent) | lock |
| Swipe-up unlock completes (past 1/5 of screen height) | unlock (+ tap haptic, slide group) |
| New notification | notify |
| Phone finishes starting | notify (a chime) |
| Battery unplugged and crossing down through 15 % or 5 % | battery-low |
| Ringer volume changed while in ring mode (level actually changed) | pip |

Volume rules:
- All UI sounds play at the **ring volume**: default 21 of 30 (70 %); silent when 0.
- Volume keys adjust media volume while media plays, otherwise the ringer. Entering ringer level 0 gives a tap haptic and silences key sounds.
- Key sounds are user-switchable in keyboard settings.

## 3. Playback timing targets

- 4 simultaneous voices; when full, the oldest voice is stolen; after a burst only the newest 4 queued taps are kept.
- Mixing: one voice plays at requested gain; overlapping voices are divided by their count to avoid clipping.
- Output latency target for key taps: ~16 ms end-to-end buffer.
- Output stream idles (is released) after ~500 ms of silence.
- Event/phone-role audio does not count as "media playing" when deciding which volume the volume keys control.
- Key press: sound and haptic fire in the same press handler, same frame, with no deliberate offset (inferred).

## 4. Haptic actuator (device-specific)

- Linear resonant actuator at about 160 Hz (6.25 ms cycle) (device-specific).
- Strength scales drive amplitude between "still" and ~95 % of full drive (device-specific).
- Design rule: a cycle is ~6 ms and two or three cycles are needed before a pulse is felt at all, so no pulse is shorter than ~7 ms.

## 5. Haptic kinds

| Kind | ms | base level | Intended feel | Effective level at default strength 80 % |
|---|---|---|---|---|
| tick | 14 | 0.385 | a tick too short to be more than felt | 0.308 |
| tap | 18 | 0.525 | normal touch / press / navigation | 0.420 |
| click | 24 | 0.63 | toggles, confirmations, commit | 0.504 |
| heavy | 38 | 0.70 | the thud of a long press (hold, nav long-press) | 0.560 |
| key | 7 | 0.28 | the shortest perceptible pulse, light, so fast typing is a row of precise ticks | 0.224 |

Levels were tuned down 30 % after the first pass felt too strong, so the original levels were about 0.55 / 0.75 / 0.9 / 1.0 / 0.4 (inferred, = /0.7). The values are tuning targets (device-specific), not measurements of real Windows Phone hardware.

Final level = `base level * global strength% * group level%`, capped at 1.0. Defaults: haptics on, global strength 80 % (range 10-100), each group 100 %.

Groups (each independently switchable): system, nav bar, tiles and lists, sliding / snapping, inside apps, keyboard.

### Event map

| Event | Kind / group |
|---|---|
| Tile tap / launch | tap / tiles |
| Tile edit-mode grab or drop | click / tiles; tick / tiles for intermediate steps |
| Tile long-press (hold) | heavy / tiles |
| Nav bar tap | tap / nav |
| Nav bar long press (app switcher etc.) | heavy / nav; click / nav on completion |
| Quick-action toggle | click / system (tap for plain presses) |
| Volume key step | tick / system; stepping to zero from above = tap |
| Notification arrives | heavy / system |
| Unlock slide | tap / slide |
| Keyboard key | key / keys; tick / keys for special keys |
| List-slider press | tick |
| Slider notch every 10 % | tick / slide |
| Any hit activation | tap |
| App hold | heavy |
| Install result | click on success, heavy on failure |
| Toggle changed by user | click |
| Slider press | tick |
| Seek bar | press = tick, release = tap |
| Held list row | tap |
| Dialog shown | tap |
| Pivot title tap | tap |

Apps may request any kind by name (tick, tap, click, heavy); the default group for app requests is "apps".

Timing relative to visuals: the pulse is issued at press-down for tilt effects (tilt in 70 ms, out 160 ms, so the 14-38 ms pulse ends before the tilt finishes) and at completion for unlock and slider notches. Real-hardware lag is (unverified).

## 6. Boot splash (adjacent)

Black background, white wordmark in `"Segoe WP Light, Selawik Light, Open Sans Light, sans-serif"` at 56 pt, centred horizontally in a 360-pt column and vertically in the 740-pt height (`y = (740 - text_height)/2`) - consistent with the 360x740 pt reference at 4.0 px/pt. Notification LED blink pattern: (unverified).

## Kit-ready constants

```json
{
 "sounds": {
  "ringVolumeDefault": 21, "volumeMax": 30, "sampleRate": 48000, "voices": 4, "idleReleaseMs": 500,
  "categories": [
   {"i":0,"name":"key","ms":30.5,"event":"letter key"},
   {"i":1,"name":"space","ms":24.1,"event":"space"},
   {"i":2,"name":"function","ms":24.1,"event":"shift/enter/backspace/symbol"},
   {"i":3,"name":"lock","event":"screen off"},
   {"i":4,"name":"unlock","event":"unlock slide"},
   {"i":5,"name":"notify","event":"notification / boot chime"},
   {"i":6,"name":"copy","event":"unused"},
   {"i":7,"name":"menu","event":"unused"},
   {"i":8,"name":"battery-low","event":"15% and 5% falling, unplugged"},
   {"i":9,"name":"pip","event":"ringer volume change"}]
 },
 "haptics": {
  "motorHz": 160, "strengthDefault": 80, "strengthRange": [10,100], "groupDefault": 100,
  "pulses": {"tick":{"ms":14,"level":0.385},"tap":{"ms":18,"level":0.525},"click":{"ms":24,"level":0.63},
             "heavy":{"ms":38,"level":0.70},"key":{"ms":7,"level":0.28}},
  "groups": ["system","nav","tiles","slide","apps","keys"],
  "web": {"navigatorVibrate": {"tick":[14],"tap":[18],"click":[24],"heavy":[38],"key":[7]}, "note":"scale by level; web can only vary duration"}
 }
}
```

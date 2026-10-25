# 11 - Known unknowns and judgement calls

Things this skill cannot state with certainty. Treat them as defaults, not facts.

| Topic | State |
|---|---|
| Font in reference renders | Segoe UI metrics are assumed (win ascent 1.079 em, descent 0.251 em, natural line 1.33 em). `kit/metro.css` forces Selawik to the same metrics so Selawik-only renders land within about 0.5 pt of Segoe ones. |
| Page title size | The official WP8 theme gives 72 XAML px = 54 pt; the measured reference pages use 48 pt. The kit uses 48 so scoring against the measured pages passes; use 54 for a stricter phone replica. |
| Page margin | 16 pt measured. A real 480-wide phone uses 24 px = 18 pt. |
| Large tile size | Not present in the measured shell (small, medium, wide only). |
| Jump list overlay | Not measured. |
| Live-tile flip curve | Approximated (520 ms with 8 % overshoot). |
| Page transitions | Only turnstile and swivel are measured. Continuum, slide-up and readerboard values come from the SDK transition tables (`06c-motion-measured.md`). |
| Row-out duration | 110 ms in the SDK, 128 ms measured. The kit uses 128. |
| Start exit duration | Documentation says 340 ms; the measured value is about 270 ms. |
| Haptic timing | Unmeasured. Kinds (tick, tap, click, heavy) are defined; durations are a guess. |
| System sounds | Seven standard sounds have no measured reference. |
| Animation speed | The default speed setting (75 %) stretches every measured animation by 1.33. Divide measured durations by 0.75 or set speed to 100 %. |
| Light theme | Values exist in the SDK resources but no page was measured in light theme. |

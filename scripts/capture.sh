#!/bin/sh
# Render an HTML file to a PNG with headless Chromium in Docker, at the Metro reference geometry:
#   360 CSS px (= 360 pt) wide, device scale factor 4  ->  1440 px wide
#   default height 740 CSS px  ->  2960 px tall (page-only views use 664 -> 2656)
#
# usage: scripts/capture.sh page.html out.png [width_css=360] [height_css=740] [dsf=4] [wait_ms=1500]
#
# Needs Docker and the image: docker build -t metro-capture harness/
# Paths must be under your home directory when Docker runs in a VM (Colima, Docker Desktop).
# Fonts: kit/metro.css bundles Selawik (OFL). If you own Segoe UI, point SEGOE_DIR at a folder of its TTFs and it is
# mounted read-only so "Segoe UI" resolves exactly as on a phone. Never commit those fonts.
set -eu
HTML="${1:?html file}"; OUT="${2:?out png}"
W="${3:-360}"; H="${4:-740}"; DSF="${5:-4}"; WAIT="${6:-1500}"
if [ -z "${DOCKER_HOST:-}" ] && [ -S "$HOME/.colima/default/docker.sock" ]; then
  DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"; export DOCKER_HOST
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML_ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"
mkdir -p "$(dirname "$OUT")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
MNT="$(dirname "$HTML_ABS")"

SEGOE_MOUNT=""
[ -n "${SEGOE_DIR:-}" ] && [ -d "$SEGOE_DIR" ] && SEGOE_MOUNT="-v $SEGOE_DIR:/usr/local/share/fonts/segoe:ro"

docker run --rm \
  -v "$ROOT":"$ROOT":ro -v "$MNT":"$MNT" -v "$(dirname "$OUT_ABS")":"$(dirname "$OUT_ABS")" \
  $SEGOE_MOUNT metro-capture sh -c "
    fc-cache -f >/dev/null 2>&1
    chromium --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --hide-scrollbars \
      --allow-file-access-from-files --default-background-color=FF000000 \
      --force-device-scale-factor=$DSF --window-size=$W,$H \
      --virtual-time-budget=$WAIT --screenshot='$OUT_ABS' 'file://$HTML_ABS' >/dev/null 2>&1
  "
[ -s "$OUT_ABS" ] && echo "ok: $OUT_ABS" || { echo "capture failed" >&2; exit 1; }

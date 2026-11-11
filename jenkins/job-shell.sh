#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r requirements.txt

SUITE="${SUITE:-all}"
BROWSER="${BROWSER:-chrome}"
BROWSER_VERSION="${BROWSER_VERSION:-156.0}"
WINDOW_SIZE="${WINDOW_SIZE:-1920x1080}"

case "$SUITE" in
  api)
    pytest -m api
    ;;
  ui)
    pytest -m ui \
      --browser="$BROWSER" \
      --browser-version="$BROWSER_VERSION" \
      --window-size="$WINDOW_SIZE"
    ;;
  *)
    pytest \
      --browser="$BROWSER" \
      --browser-version="$BROWSER_VERSION" \
      --window-size="$WINDOW_SIZE"
    ;;
esac

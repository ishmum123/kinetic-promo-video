#!/usr/bin/env bash
# Fetch Poppins woff2 subsets (Latin only, ~8 KB each) next to scene.html so the
# render is offline and reproducible. Poppins is licensed under the SIL OFL 1.1.
#
#   bash fetch-fonts.sh [dest]      # default dest: ./fonts
#
# If this fails (no network), fall back to a geometric system font in the CSS —
# Futura, Avenir Next, or Century Gothic — and tell the user you substituted.
set -euo pipefail
DEST="${1:-fonts}"
mkdir -p "$DEST"

base="https://fonts.gstatic.com/s/poppins/v24"
declare -a f=(
  "200:pxiByp8kv8JHgFVrLFj_Z1xlFd2JQEk.woff2"
  "300:pxiByp8kv8JHgFVrLDz8Z1xlFd2JQEk.woff2"
  "400:pxiEyp8kv8JHgFVrJJfecnFHGPc.woff2"
  "500:pxiByp8kv8JHgFVrLGT9Z1xlFd2JQEk.woff2"
  "600:pxiByp8kv8JHgFVrLEj6Z1xlFd2JQEk.woff2"
)
for e in "${f[@]}"; do
  w="${e%%:*}"; u="${e#*:}"
  curl -fsS -o "$DEST/Poppins-$w.woff2" "$base/$u"
  printf '  Poppins-%s.woff2  %s bytes\n' "$w" "$(wc -c < "$DEST/Poppins-$w.woff2" | tr -d ' ')"
done
echo "fonts -> $DEST"

# If these URLs ever 404, regenerate them with:
#   curl -sA "Mozilla/5.0 ... Chrome/120" \
#     "https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600" | grep -E "src|font-weight"
# and take the src whose unicode-range covers U+0000-00FF (the Latin subset).

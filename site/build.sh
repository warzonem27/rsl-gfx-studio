#!/bin/sh
# Builds the team website from the studio: same page, website mode switched on.
# Usage: PASS_HASH=$(printf '0099' | shasum -a 256 | cut -d' ' -f1) ./site/build.sh
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC="$ROOT/studio"; OUT="$ROOT/site/dist"
rm -rf "$OUT"; mkdir -p "$OUT/data"
cp -r "$SRC/assets" "$OUT/assets"
sed "s#<title>RSL GFX Studio</title>#<title>RSL GFX Studio</title>\n<meta name=\"rsl-site\" content=\"1\">\n<meta name=\"rsl-build\" content=\"$(date +%s)\">\n<meta name=\"rsl-pass\" content=\"$PASS_HASH\">\n<meta name=\"robots\" content=\"noindex,nofollow\">#" "$SRC/index.html" > "$OUT/index.html"
printf 'User-agent: *\nDisallow: /\n' > "$OUT/robots.txt"
touch "$OUT/.nojekyll"
echo "Built $OUT — copy it into the RSL-GFX/rsl-gfx.github.io repo to publish."

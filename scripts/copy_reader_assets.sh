#!/bin/sh
set -eu

mkdir -p public/fonts public/vendor
for font in roboto-latin-wght-normal roboto-latin-wght-italic; do
  cp "node_modules/@fontsource-variable/roboto/files/$font.woff2" public/fonts/
done
cp node_modules/@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2 public/fonts/
cp node_modules/@fontsource-variable/roboto/LICENSE public/fonts/roboto-LICENSE.txt
cp node_modules/@fontsource/ibm-plex-mono/LICENSE public/fonts/ibm-plex-mono-LICENSE.txt
cp node_modules/list.js/dist/list.min.js public/vendor/
cp node_modules/tocbot/dist/tocbot.min.js public/vendor/
cp node_modules/anchor-js/anchor.min.js public/vendor/
for package in list.js tocbot anchor-js; do
  cp "node_modules/$package/LICENSE" "public/vendor/$package-LICENSE.txt"
done

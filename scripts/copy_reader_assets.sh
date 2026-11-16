#!/bin/sh
set -eu

mkdir -p public/fonts public/vendor
rm -f public/fonts/roboto-* public/fonts/ibm-plex-*
for font in geist-latin-wght-normal geist-latin-wght-italic; do
  cp "node_modules/@fontsource-variable/geist/files/$font.woff2" public/fonts/
done
for font in geist-mono-latin-wght-normal geist-mono-latin-wght-italic; do
  cp "node_modules/@fontsource-variable/geist-mono/files/$font.woff2" public/fonts/
done
cp node_modules/@fontsource-variable/geist/LICENSE public/fonts/geist-LICENSE.txt
cp node_modules/@fontsource-variable/geist-mono/LICENSE public/fonts/geist-mono-LICENSE.txt
cp node_modules/list.js/dist/list.min.js public/vendor/
cp node_modules/tocbot/dist/tocbot.min.js public/vendor/
cp node_modules/anchor-js/anchor.min.js public/vendor/
for package in list.js tocbot anchor-js; do
  cp "node_modules/$package/LICENSE" "public/vendor/$package-LICENSE.txt"
done

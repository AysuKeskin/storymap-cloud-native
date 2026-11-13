#!/usr/bin/env bash
# Rebuilds the architecture diagram and the Phase 1 PDF.
# Requires: graphviz (dot), pandoc, Google Chrome.
set -euo pipefail
cd "$(dirname "$0")"

dot -Tsvg architecture.dot -o architecture.svg
dot -Tpng -Gdpi=170 architecture.dot -o architecture.png

tmp_html="$(mktemp -t phase1-report).html"
pandoc phase1-report.md -s --self-contained --css report.css -o "$tmp_html"

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/phase1-report.pdf" "file://$tmp_html" 2>/dev/null
rm -f "$tmp_html"
echo "Wrote $PWD/phase1-report.pdf"

#!/usr/bin/env bash
# Rebuilds the architecture diagram and compiles the Phase 1 LaTeX report.
# Requires: graphviz (dot) and tectonic (https://tectonic-typesetting.github.io).
set -euo pipefail
cd "$(dirname "$0")"

dot -Tpdf architecture.dot -o architecture.pdf
dot -Tsvg architecture.dot -o architecture.svg
dot -Tpng -Gdpi=170 architecture.dot -o architecture.png

tectonic --keep-logs=false phase1-report.tex
echo "Wrote $PWD/phase1-report.pdf"

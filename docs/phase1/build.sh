#!/usr/bin/env bash
# Rebuilds the architecture diagram and compiles the Phase 1 LaTeX report.
# Requires: python3 + matplotlib, and tectonic (https://tectonic-typesetting.github.io).
set -euo pipefail
cd "$(dirname "$0")"

python3 architecture.py   # writes architecture.png / .pdf / .svg

tectonic --keep-logs=false phase1-report.tex
echo "Wrote $PWD/phase1-report.pdf"

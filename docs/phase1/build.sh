#!/usr/bin/env bash
# Rebuilds the architecture diagram and compiles the Phase 1 LaTeX report.
# Requires: python3 with matplotlib, and tectonic.
set -euo pipefail
cd "$(dirname "$0")"

# 1. Draw the diagram (writes architecture.png, .pdf and .svg).
python3 architecture.py

# 2. Compile the report.
tectonic --keep-logs=false phase1-report.tex
echo "Wrote $PWD/phase1-report.pdf"

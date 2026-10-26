#!/usr/bin/env bash
# Rebuilds the TNB site. Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/tools/build_home.py
python3 src/tools/build_pages.py
echo "Built ../site/index.html"

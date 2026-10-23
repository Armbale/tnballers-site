#!/usr/bin/env bash
# Rebuilds site/index.html from src/. Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")"
python3 parts/make_canada.py
python3 parts/make_feed.py
python3 retheme.py
python3 structure.py
python3 script_fix.py
python3 build.py
node --check work-check.js
rm -f work.html work2.html work3.html work-check.js
echo "Built ../site/index.html"

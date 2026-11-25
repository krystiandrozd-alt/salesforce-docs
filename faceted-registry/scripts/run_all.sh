#!/usr/bin/env bash
# Rebuild everything from sources/. Snapshot step needs the live ~/.claude tree; skip it to rebuild from the checked-in sources.
set -e
cd "$(dirname "$0")/.."
[ "$1" = "--snapshot" ] && python3 scripts/snapshot_sources.py
python3 scripts/build_registry.py
python3 scripts/analyze.py > /dev/null
python3 scripts/gen_site.py
python3 scripts/kappa.py > /dev/null   # needs validation/blind_*.json

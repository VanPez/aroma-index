#!/usr/bin/env bash
# Rebuild every derived artifact from data/ — the whole point being that no
# output is ever produced by hand. Three separate drifts (stats2.json, the CSV,
# and the deployed HTML) all traced back to hand-built outputs, so: one command,
# everything regenerated, nothing copied manually.
#
#   ./build.sh
#
# Generators read and write their working directory, so we stage into a temp dir
# and copy the results into place. scentmap.py is NOT run here: it needs
# umap-learn + numpy and recomputes the UMAP projection, which would move every
# dot on the scent map. Run it deliberately when the molecule set changes.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(pwd)
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

cp generators/* "$STAGE"/
cp data/rows2.json data/stats2.json data/scentmap.json "$STAGE"/
cd "$STAGE"

python3 mkstats.py                 # stats2.json  <- rows2.json   (run first: the others read it)
python3 mkhtml2.py                 # aroma-index.html
python3 mkscentmap.py              # scent-map.html
python3 mkcsv.py                   # aroma-index.csv
python3 build_mint.py > /dev/null  # mint/

cp stats2.json          "$ROOT"/data/stats2.json
cp aroma-index.html     "$ROOT"/docs/index.html
cp scent-map.html       "$ROOT"/docs/scent-map.html
cp aroma-index.csv      "$ROOT"/docs/aroma-index.csv
mkdir -p "$ROOT"/mint/metadata "$ROOT"/mint/structures
cp mint/mint-records.json mint/erc721-metadata.json mint/_stats.json "$ROOT"/mint/
cp mint/metadata/*.json     "$ROOT"/mint/metadata/
cp mint/structures/*.smi    "$ROOT"/mint/structures/

cd "$ROOT"
echo
echo "rebuilt: docs/index.html docs/scent-map.html docs/aroma-index.csv data/stats2.json mint/"
echo "note: smiles-3d.html and molnft-resolver.html are hand-maintained, not generated."
git status --short 2>/dev/null || true

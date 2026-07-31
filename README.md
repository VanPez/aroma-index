# Aroma Molecule Index

An open, hand-curated index of common aroma molecules — a DeSci proof-of-concept and proposed public-good extension of GenesisL1's **MOLNFT** protocol.

- **Live site:** https://vanpez.github.io/aroma-index/
- **Repo:** https://github.com/VanPez/aroma-index (MIT)
- **Maintainer:** Ivan (vanpe / vAnPΞ)
- **Companion:** `../INFRA.md` (validator + L1 tooling reference). This folder is the home for all Aroma-index work — previously only an early `aroma-index.html` lived in `../l1-liquidity/` (now superseded).

## What it is

99 fragrance molecules grouped into top / heart / base notes by volatility, each with boiling point and vapor pressure at 25 °C. Click any molecule for its 3D structure and public identifiers (PubChem CID · InChIKey · SMILES). Includes a UMAP "scent map", a SMILES→3D tool, and Joe's MolNFT/IPFS resolver folded into the index page (v3).

## Folder layout

```
aroma-index/
  README.md            this file
  DEVLOG.md            running work log (newest first) — the project narrative
  LICENSE              MIT
  build.sh             rebuilds every derived artifact from data/ — run this, don't hand-edit outputs
  docs/                the deployed pages — GitHub Pages serves this folder directly
    index.html           the current v3 (molecules + resolver)
    scent-map.html
    smiles-3d.html       hand-maintained (not generated)
    molnft-resolver.html standalone resolver, hand-maintained (now redundant; kept for reference)
    aroma-index.csv
  data/                canonical data
    rows2.json           99 molecules, all fields (source of truth)
    stats2.json          per-tier stats
    scentmap.json        UMAP coordinates + odour classes
  generators/          scripts that build the site from data
    mkhtml2.py           builds docs/index.html from rows2.json + stats2.json + res_*.txt
    mkscentmap.py        builds scent-map.html from scentmap.json
    mkstats.py           recomputes stats2.json from rows2.json
    mkcsv.py             rebuilds docs/aroma-index.csv from rows2.json
    scentmap.py          computes scentmap.json (UMAP) from rows2.json
    measure.py           byte-size measurement (Mike's ladder)
    build_mint.py        builds the mint/ pilot data from rows2.json
    res_css.txt/res_js.txt/res_section.txt  resolver snippets injected by mkhtml2.py
  mint/                mint-ready pilot (see mint/SCHEMA.md) — NOT in git until the mint; see .gitignore
    mint-records.json    canonical on-chain fields, 95 molecules
    metadata/0001..0095.json   ERC-721 tokenURI metadata per token
    structures/0001..0095.smi  SMILES structure file per token
    erc721-metadata.json, _stats.json, SCHEMA.md
  reports/
    aroma-index-feasibility.md   deep-research feasibility report
    resolver-review.md           verification of Joe's resolver
  screenshots/         visual records
  archive/             earlier builds, intermediate scripts, v1/v2 data
```

## Regenerating

**Edit `data/rows2.json`, then run `./build.sh`.** Never hand-edit a file under `docs/`,
`mint/` or `data/stats2.json` — they are all derived, and every one of them has drifted
from the source at least once by being touched directly.

```
./build.sh
```

It rebuilds `docs/index.html`, `docs/scent-map.html`, `docs/aroma-index.csv`,
`data/stats2.json` and `mint/`, then prints `git status`. Stdlib only — no dependencies.

Not run by `build.sh`:

- `generators/scentmap.py` recomputes the UMAP projection (`data/scentmap.json`) and needs
  `umap-learn` + `numpy`. It moves every dot on the scent map, so run it deliberately when
  the molecule set changes — not on every build.
- `docs/smiles-3d.html` and `docs/molnft-resolver.html` are hand-maintained.

## Deploying

GitHub Pages serves the `docs/` folder on `main`, so **`git push` deploys** — the working
folder and the repo are the same tree, with no copy step.

## Current status (2026-07-31)

- Site is live at v3; resolver folded into the index page.
- **Pilot mint staged + audited** (`mint/`): 95 molecules with public structures (4 trade-name captives excluded — no public structure). ~277 B/record. No licence needed — own curation over public-domain PubChem structures.
- **Pre-mint audit passed (2026-07-31):** all 95 InChIKeys and formulae recompute from their SMILES; no null/empty value in any record, metadata file or attribute; `formula`/`mw` complete 95/95. Pilot fingerprint `2c160f09b51d22844dfed34d7e07aac3019bc59e3dd1623f53fc6e8dfd5cfc42` (sha256 over the 95 `.smi` + metadata pairs in ID order). NB token IDs were renumbered in the audit, and the fingerprint changed again when the vapour-pressure estimator was recalibrated — see DEVLOG. **Recompute it before minting rather than trusting this line.**
- MolNFTs are **standard tradeable ERC-721s** (confirmed by Mike). Path: deploy own MolNFT contract → mint script (with dry-run) → mint. Deploy/sign/mint is Ivan's (with Mike's help); keys stay on Ivan's side.
- **Waiting on:** Mike's reference MolNFT contract (to base the collection on); Rick Gerkin / Pyrfume re a licence for the Leffingwell scale-up (tradeable tokens + CC-BY-NC clash — expansion needs a commercial-friendly or permissive source).
- Next: pilot-mint the 95, learn real gas + process, then decide on scale.

See `DEVLOG.md` for the full chronological history.

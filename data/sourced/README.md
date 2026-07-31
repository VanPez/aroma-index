# `data/sourced/` — licence-clean molecules from public-domain / CC0 sources

**Status: partial (192 of 382 pulled, 172 new after de-duplication). Resumable.**

## What this is

An expansion set of aroma molecules whose odour data is free for commercial use — so it can back
**tradeable** MOLNFTs, unlike the Leffingwell set (CC-BY-NC, and now access-restricted on Zenodo).

Selection criteria, in order:

1. Carries a **FEMA number** in PubChem (i.e. is a flavour/fragrance substance) — 2,389 molecules
2. Has odour data from a commercially-usable source: **HSDB** odour text (US National Library of
   Medicine → US Government work, public domain) or **Keller & Vosshall 2016** (CC BY 4.0 + CC0 data)
3. Passes a basic odorant screen (organic, MW 60–320, not a salt/amino acid/sugar)
4. Restricted to molecules **present in Keller** — i.e. actually smelled and rated by 61 human
   subjects, so they are odorants by construction. This deliberately excludes the HSDB-only bucket,
   which is contaminated with food additives (parabens, acidulants, humectants).

## Provenance of every field

| Field | Source | Status |
|---|---|---|
| `cid`, `name`, `smiles` | PubChem | public domain |
| `inchikey`, `formula`, `mw` | **computed locally from SMILES with RDKit** | derived, reproducible |
| `sources` | which free source carries odour data for this molecule | — |
| `note`, `family`, `descriptors` | **deliberately null** | to be supplied, see below |

`note` / `family` / `descriptors` are left empty on purpose. They are the curated layer, and filling
them automatically is exactly the mistake that produced the unverifiable descriptors in `rows2.json`.
Note tier in particular cannot be derived — a rule fitted to the existing 99 reproduces them at only
56% under leave-one-out, so it is a judgement, not a computation. See `reports/descriptor-crosscheck.md`.

## Counts so far

- 192 molecules pulled from PubChem
- 20 already present in the curated 99 (skipped, curated entries always win)
- **172 new**, of which **95 have HSDB odour text** available to attach
- Target for the full pull: 382

## Resuming

State lives in the browser session and is lost on reload, but the selection is fully reproducible:

1. `GET /rest/pug_view/annotations/heading/JSON?heading=FEMA%20Number` (3 pages) → FEMA CID set
2. `GET /rest/pug_view/annotations/heading/JSON?heading=Odor` (3 pages) → HSDB odour text by CID
3. Keller CIDs from `raw.githubusercontent.com/pyrfume/pyrfume-data/main/keller_2016/molecules.csv`
4. Intersect per the criteria above, then fetch
   `/rest/pug/compound/cid/<batch>/property/Title,MolecularFormula,MolecularWeight,InChIKey,IsomericSMILES/JSON`

**Note:** PubChem's REST API returns an empty body through the direct fetch tool; it only works from
inside a page on `pubchem.ncbi.nlm.nih.gov` (same-origin). Hence the browser round-trips, ~96 rows at a
time. Raw batches are kept in `data/staging/`.

## Not yet done

- Remaining ~190 molecules
- Attaching the HSDB odour text itself (currently only flagged, not stored) for the 95 + rest
- Boiling point / vapour pressure from PubChem, needed before any tier work
- Merge into `rows2.json` — held back deliberately; the sourced set should stay separate and clearly
  labelled until reviewed

# Aroma Molecule Index — work log

A running record of what got built and why. Project: **VanPez/aroma-index** — an open, hand-curated index of common aroma molecules, proposed as a public-good DeSci proof-of-concept for GenesisL1's **MOLNFT** protocol. Live at https://vanpez.github.io/aroma-index/

Times are UTC. Commit hashes in parentheses. Newest first.

---

## 2026-07-31 — Built a licence-clean expansion set: 218 molecules from public-domain / CC0 sources

Acting on the licence scan: rather than chase Leffingwell, assembled an expansion from sources that permit commercial use, so it can back **tradeable** tokens. Lives in `data/sourced/`, deliberately **separate from `rows2.json`** so the curated and sourced layers stay visibly distinct.

**Selection** (all measured, not estimated): molecules with a **FEMA number** in PubChem (2,389) ∩ having free odour data — **HSDB** odour text (US National Library of Medicine → public domain) or **Keller & Vosshall 2016** (CC BY 4.0 + CC0) → 562. Restricted to those **present in Keller** (i.e. actually smelled and rated by 61 human subjects, so odorants by construction, which excludes the HSDB-only bucket full of parabens and acidulants) → 382. Minus 34 already in the curated 99, minus 10 that **HSDB itself labels odourless** (adipic acid, glycerol, cetyl alcohol…) → 338.

**Then filtered to perfumery relevance** (Ivan's call — "keep it in the spirit of what it was born in"): 338 → **218**. Removed 120 with a stated reason each, kept in `data/sourced/excluded.json` so any category can be reinstated by changing one rule: 48 savoury/roasted heterocycles (pyrazines, thiazoles, furans), 26 solvents/industrial/plasticisers, 25 sulfurous, 15 straight-chain fatty acids, 4 amines, 2 preservatives.

- **48 are flagged `borderline`, not decided** — short-chain fruity esters, fusel alcohols, simple aldehydes/ketones. Genuine perfumery judgement, explicitly left to Ivan rather than guessed.
- **`note`, `family`, `descriptors` are null on every sourced molecule, on purpose.** Auto-filling them is exactly the mistake that produced the unverifiable descriptors in `rows2.json`.
- Provenance per field: structures/CIDs from PubChem; **formula, MW and InChIKey recomputed locally with RDKit**; odour text from HSDB (64 of the 218); Keller CC0 ratings for all.
- **Verified, 0 problems:** all SMILES parse, all InChIKeys/formulae recompute from structure, no duplicates, no collision with the curated set, `rows2.json` untouched at 99 rows.
- **Two of my own filter rules misfired and were caught on review** — bornyl acetate binned by an `^acetic acid` regex matching its IUPAC name, and thioguaiacol *rescued* by the `guaiacol` keep-rule despite being a sulfur compound. Lesson: keyword filters over chemical names fail in both directions; always audit both the kept and removed lists.

**Index now: 99 curated + 170 sourced = 269**, plus 48 pending. Honest about what it is — the sourced material is well-documented commodity flavour/fragrance chemistry, not the modern perfumery palette. Iso E Super, Hedione, Ambroxan and the musks are not in any free source and never will be.

**Pipeline note:** PubChem's REST API returns an empty body through the direct fetch tool; it only works same-origin from a page on `pubchem.ncbi.nlm.nih.gov`, so everything came through the browser ~96 rows at a time. Raw batches kept in `data/staging/` (`k1`–`k4`). Full method in `data/sourced/README.md`.

## 2026-07-31 — Licence scan for the scale-up: no permissive Leffingwell exists; PubChem supplies the molecules but not the words

Full scan of 15 odour/aroma datasets, licences read at source, written up in `reports/license-scan.md`. Driven by the constraint that **tradeable ERC-721s = commercial use**, so anything NonCommercial is out.

**Result: the scale-up premise was wrong.** There is no permissive equivalent of Leffingwell. Every large expert-labelled odour table is NC, proprietary, or a copyrighted book.

- **Leffingwell is worse than CC-BY-NC** — the Zenodo files are now **Restricted**, released only on request under a stated non-commercial condition.
- **Only clean descriptor set found: Keller & Vosshall 2016** — **CC BY 4.0 + CC0 for the data** (verified on the publisher's rights statement, `oa=CC BY + CC0`). 480 molecules, 61 subjects, 19 semantic descriptors. Perceptual ratings, not perfumer vocabulary.
- **FlavorDB2 = CC BY-NC-SA 3.0** (site footer) — fails twice: NC blocks tokens, SA would force copyleft on the collection.
- **Two traps that look like green lights:** `pyrfume-data` has an **MIT LICENSE at its root** that covers Pyrfume's *code* and cannot relicense the third-party archives inside it (Good Scents manifest: *"Pyrfume developers make no claims concerning copyright"*). And **OpenPOM is MIT but trained on Leffingwell + Good Scents** — the badge doesn't launder the data.
- **Wikidata ruled out with numbers** (SPARQL, not impression): 363 items classed as aroma compounds, 699 uses of `smells of` across all of Wikidata, and only **31** chemicals having both a SMILES and an odour statement.

**PubChem measured directly (PUG View API):** **2,389** molecules carry a FEMA number — a licence-clean flavour/fragrance molecule list, 24× the current index, one API call away. **2,261** molecules have an `Odor` annotation, **2,356 of 2,358 sourced from HSDB** (US National Library of Medicine → public domain) — but only **308** overlap the FEMA set, and the prose is toxicological ("Sweetish smell" for vanillin; geraniol absent).

**The reframe that matters:** the descriptors are the only encumbered layer, and they are *not* what makes this index work. Its organising principle — top/heart/base from vapor pressure — is **computed from physics**. So a ~2,389-molecule index can be built today with zero licence exposure: PD structures, computed formula/MW, PubChem BP/VP with the existing Clausius–Clapeyron fallback, tiers computed. Descriptors would cover only a few hundred (308 HSDB + 480 Keller). Explicit trade: thousands correctly tiered, hundreds described.

**Open lead, not yet assessed:** US patents — patent text isn't copyrightable in the US, and fragrance patents describe compound odours in detail beside their structures. The only plausible route to free descriptors at scale. Needs extraction, not download.

Does not affect the 95-molecule pilot, which needs no licence.

## 2026-07-31 — Project put under version control; sources published; deploys are now `git push` · `8109e86`

The repo held only the built HTML — every source, generator and note lived on one machine with no history. Fixed the structure rather than the symptom, because the day's three separate bugs (`stats2.json` drift, the stale CSV, the site being a hand-copied duplicate) all had the same cause: **derived artifacts built by hand, with no generator and no single source**.

- **Adopted the real git history** into `~/Documents/GenesisL1/aroma-index/` (cloned the 14 existing commits rather than `git init`, so nothing was orphaned). Ivan pushed; the assistant never handles credentials.
- **Published** `data/`, `generators/`, `reports/`, `README.md`, `DEVLOG.md`, `build.sh` — 45 files. Reproducibility is the scientific claim, so the generators belong in public alongside the output.
- **`mint/` deliberately untracked** (`.gitignore`, with the reasoning written in so it isn't silently reverted). Not secrecy — the structures are public-domain and the curation is now public in `data/`. It's that token IDs stay volatile until a contract fixes them (today's fix renumbered 56 of 95), and `mint/` regenerates exactly from `rows2.json` + `build_mint.py`, so the git history still dates the curation. It gets published at mint time with the contract address and tx hashes.
- **`build.sh`** — one command regenerates all five derived artifacts. Verified it reproduces every current one **byte-for-byte** before committing, so the committed outputs provably match their sources. `scentmap.py` is deliberately excluded (recomputing UMAP would move every dot).
- **New `generators/mkcsv.py`** — `docs/aroma-index.csv` was a hand export and still carried the three empty formula/mw cells after the site was fixed. It now regenerates, and reproduces the old export byte-for-byte apart from those three rows.
- **`site/` → `docs/`, GitHub Pages source switched to `main /docs`.** The working folder and the repo are now one tree: **`git push` deploys**, no copy step, no web-UI uploads. Verified live afterwards — index, scent map and SMILES→3D all serve correctly and the corrected `138 → 169 → 210` header is up.
  - **Gotcha:** between the push and the Pages settings change the site rendered `README.md` instead — the standard Pages fallback when there's no `index.html` at the publishing source. Harmless and self-correcting, but it means **the two steps should be done back-to-back**; the Pages build also takes ~2 min, so don't judge it from the first reload.
- **Left for Ivan, deliberately not decided:** the local `LICENSE` said a legal name where the published one says `vanpe` — reverted to the pseudonym rather than publish a legal name irreversibly. `screenshots/` is 2.2 MB of the 2.8 MB repo and git keeps it forever; kept for now.

## 2026-07-31 — Pre-mint data audit: 3 empty fields fixed at source; token IDs renumbered

Audit of the staged pilot before anything goes on-chain. Found **three records carrying empty `formula` and null `mw`** — Mayol (CID 83763), Aurantiol (CID 98118), Norlimbanol (CID 116699) — which the ERC-721 builder was rendering as literal `"value": ""` / `"value": null` attributes. Immutable tokens, so worth catching now.

- **Fixed at source, not in the builder.** The gap lived in `data/rows2.json`, which feeds both the mint *and* the live site — patching `build_mint.py` alone would have fixed the tokens while leaving the website table showing "—", and the gap would recur on any rebuild. Filled `formula`/`mw` for the three in `rows2.json`, then regenerated both.
- **Values** (RDKit from the SMILES already on file, **average** MW to match the PubChem convention of the other 92; only the three gaps filled, the other 92 untouched — no churn/drift): Mayol `C10H20O` 156.27 · Aurantiol `C18H27NO3` 305.42 · Norlimbanol `C15H30O` 226.40.
- **Cross-check.** PubChem REST is unreachable from the build container (same as the Rung-1 enrichment), so used a stronger offline proof instead: **recomputed the InChIKey from each SMILES and compared it to the stored PubChem InChIKey**. All **95/95 round-trip exactly** — so each SMILES *is* the PubChem record it claims to be, and a formula derived from it is PubChem's formula. (Aurantiol also checks by hand: methyl anthranilate C8H9NO2 + hydroxycitronellal C10H20O2 − H2O = C18H27NO3, correct for a Schiff base.)
- **`build_mint.py` hardened** with `prune()`/`prune_attrs()` — absent fields are now **omitted rather than encoded as null/""**, in both the canonical records and the ERC-721 attributes. Kept as a defensive net even though the source is now complete: on an immutable token, an omitted field reads "not recorded", a null field reads sloppy. Side effects: CAS dropped from 2 tokens (Mayol, Norlimbanol — genuinely unknown), BP/VP dropped from the 23 molecules with no experimental value, record size **284 → 277 B** avg, collection gzip 7395 → 7372 B.
- **New `generators/mkstats.py`** — `data/stats2.json` (the site's "Avg MW rises with tier" header) had no generator and was computed over the incomplete set, so it silently drifted. Now regenerable. Filling the three moved base `mw_max` 270.37 → **305.42** (Aurantiol is the heaviest base note) and base mean 206.79 → 209.67; heart mean 169.84 → 169.47.
- **⚠️ Token IDs renumbered — 56 of 95 changed.** `build_mint.py` sorts by `(tier, mw)`, and the three null-MW records had been sorting as `mw=0` to the front of their tier. With real MWs they take their proper place: Mayol 20 → **35**, Norlimbanol 57 → **80**, Aurantiol 56 → **95**, shifting everything after them. Harmless (nothing is minted) and now correct, but **any earlier note mapping a token ID to a molecule is stale** — regenerate from `mint-records.json`.
- **Re-verified, 0 failures:** 95 records; formula+mw populated 95/95; no null/empty in any record, metadata file or attribute; IDs contiguous 1–95; InChIKey/name/CID unique; every `.smi` byte-matches its record and its metadata name; all 95 InChIKeys and formulae recompute from SMILES; no stray files. Site table confirmed showing real values for all three (remaining "—" are genuine BP/VP unknowns).
- **Pilot fingerprint** (sha256 over all 95 `.smi` + metadata pairs, in ID order): `f66365fd5dd953fd05ca7dab309b9f9887705c3ff8480039c38855ceb0528c62` — pre-mint content hash to check against at mint time. (Previous, pre-fix: `d78bac2f…`.)

Still waiting only on Mike's reference MolNFT contract.

## 2026-07-31 — Saved to disk + continuity wired in; ready to mint the 95

Session work saved to `~/Documents/GenesisL1/aroma-index/` (236 files); INFRA.md updated with an Aroma-index pointer.

**RESUME HERE — the 95-molecule pilot mint is the next action.** Sequence: (1) get Mike's reference MolNFT contract; (2) draft the mint script around it, with a dry-run that prints every record before any transaction; (3) Ivan + Mike deploy the collection contract and mint the 95 — keys stay with Ivan, the assistant never signs/mints; (4) read the real gas cost, then decide on scale. Outstanding waits: Mike's reference contract; Rick/Pyrfume licence (needed for the Leffingwell scale-up only, not the pilot).

## 2026-07-31 — Plan set: pilot-mint the 95, decide scale from real numbers

Decision (Ivan): don't chase the Leffingwell expansion yet. **Test-mint the 95 we have**, learn the actual gas cost and mint process end-to-end, then decide whether/how much to scale from evidence. Considered and set aside a "relabel Leffingwell descriptors to dodge CC-BY-NC" idea — database rights also cover the *selection* of molecules (not just labels), and a workaround would undercut the good-faith permission ask already sent to Rick. If we ever scale, the clean routes are a permissive (CC0/CC-BY) odour dataset or an independently-sourced molecule list — not relabeled Leffingwell.

- Mike: no testnet needed; sequence is prepare collection contract → mint script that securely mints → go. Clarified the 95-vs-99 to Mike: not a rights issue — 4 are trade-name captives with no publicly disclosed structure (nothing to encode); Leffingwell-style sets are structure-based so wouldn't have that gap.
- Waiting on Mike's **reference MolNFT contract** so the collection matches his standard (future UI/client compatibility). Then I draft the mint script around it (with a dry-run that prints every record before anything goes on-chain).
- Pilot data staged and ready (`mint/`: 95 SMILES structure files + paired ERC-721 JSON, ~284 B/record).

## 2026-07-31 — Mike's answers: mint path clear, tokens ARE tradeable

Mike answered the three questions:

1. **Tokens are tradeable** — MolNFTs are standard, transferable/sellable ERC-721s, *not* a locked one-address registry (Joe's guess was wrong). Mike is himself selling neuroscience-atlas collections.
2. **Any field can be added** — MolNFT is ERC-721 holding molecular data+metadata instead of an image. The path: **deploy your own MolNFT contract (a "collection")** and mint your molecules into it. Mike will build a UI/client later; will help manually meanwhile.
3. **Permissionless** — deploy + mint yourself; Mike offers hands-on help.

Ivan's homework (Mike): decide exactly what per-molecule data to record (he suggests generous, since small), and have it locally as a folder of molecular files + matching JSON that a mint script assembles.

- **Consequence for licensing:** tradeable makes the **Leffingwell scale-up harder, not easier** — CC-BY-NC forbids commercial use and a sellable token is commercial. So the expansion would need a commercial licence, a permissive (CC0/CC-BY, non-NC) odour source, or descriptors kept off the tradeable tokens. The **95 pilot is unaffected** (own curation + public-domain structures, no licence needed even when tradeable). Also: the Pyrfume email framed things as "public-good/non-commercial" — must stay straight with Rick that tokens are tradeable if he replies.
- **Repackaged the pilot** to Mike's suggested layout: added `structures/NNNN.smi` (molecular file per token) paired 1:1 with `metadata/NNNN.json`; corrected `SCHEMA.md` for the tradeable reality and the deploy-your-own-contract path. 95 pairs, ~284 B/record.

## 2026-07-31 — Pilot is license-clean; mint-ready data built for the 95

Key realisation: the current index needs **no third-party licence to mint**. Its structures/identifiers are public-domain (PubChem); its note tiers, families and descriptors are original hand-curation, not the Leffingwell dataset. Copyright protects a *compiled database*, not individual factual data points — so original curation over public-domain structures is clean. (Not legal advice.) The CC-BY-NC Leffingwell licence only matters for the ~3,500 scale-up. So the current set can be the **pilot mint now**, proving the pipeline end-to-end while Rick's answer gates only the expansion.

- **Built the mint-ready artifact** (`mint/`, `build_mint.py`): 95 mintable molecules (4 proprietary captives excluded — no public structure). Two forms: `mint-records.json` (canonical on-chain fields, avg **284 B**/token, 27 KB total) and `metadata/*.json` (ERC-721 render, one per token). Whole collection gzips to 7.4 KB. No base64/gzip needed at token level.
- Schema documented in `mint/SCHEMA.md`: InChIKey (canonical small-molecule key) + SMILES + core properties; 3D regenerates in-browser; JSON rendered on the fly. Attribution: PubChem (public domain) + vanpe curation.
- **Drafted a consolidated question to Mike:** confirm tokens are non-transferable / one-address (Joe thinks so — strengthens the licensing case); how/who adds the small-molecule field; the mint path (contract, permissions, interface vs dev).
- **Answered Joe** on SMILES completeness: complete/canonical for covalent organics; his d/f-orbital concern applies only to organometallics/coordination compounds (out of scope for fragrance); InChI is the stricter standard if full generality is ever needed.

## 2026-07-29 — Byte-size measurement (Mike's ladder) + on-chain format decision

Mike (GenesisL1) asked for a concrete measurement before deciding on-chain vs off-chain: smallest format that preserves metadata, then raw → gzip → gzip+base64 at every step, plus an invented NFT metadata schema. Ran it on the 99-molecule set (`measure.py`).

- **Framing that resolves half the checklist:** the data is text (SMILES + JSON), never binary, so base64 has no role — it only inflates text +33%. SMILES (~24 B) regenerates the 3D in-browser (Joe's point), so no 3D model is ever stored; base64 is reserved for genuinely binary payloads (e.g. Joe's focus-stacked species images).
- **Measured (compact JSON, all metadata preserved):** raw ~228 B/molecule (22 KB for 99); whole-collection gzip 7.3 KB (~75 B/molecule); base64 of that 9.7 KB (larger than the gzip → counterproductive). Verbose ERC-721 record 642 B/molecule (62 KB for 99). Per-record gzip is wasteful (per-stream overhead exceeds the gain on a ~200 B record); compression only pays as a single collection blob.
- **Extrapolation:** Leffingwell (~3,500) ≈ 256 KB gzipped; 1M molecules ≈ 72 MB. Confirmed tiny → on-chain is reasonable (matches Mike's instinct).
- **Format decision:** per token, store canonical fields on-chain (InChIKey + SMILES + core properties, ~200 B) and render the ERC-721 `tokenURI` JSON on the fly — no IPFS, no gzip, no base64 at this size. Same conclusion sent to Joe, so the story is consistent across both.
- **Metadata schema:** identifiers (inchikey = canonical key, smiles, pubchem_cid, cas, formula); properties (mw, bp_c, vp_pa_25c, note_tier, odor_family, descriptors[]); ERC-721 name/description/attributes.
- **Mike's protein point (acknowledged):** InChIKey works only for small molecules (small, enumerable); proteins stay sequence-identified (alignment/E-value; identical sequence ≠ identical fold). So InChIKey is the *additive* small-molecule field Mike said MolNFT can include easily — not a universal key.
- Replied to Mike (numbers + format decision) and Joe (SMILES-over-base64 confirmed).

## 2026-07-29 — Leffingwell scale-up: licensing gate identified + outreach sent

Decision to scale from the 99-molecule "play" toward the full **Leffingwell odour dataset** (~3,500 molecules) to make it a serious reference, then mint. Did the diligence before committing to that path.

- **Licensing finding:** the Leffingwell odour dataset (via Pyrfume/Zenodo) is **CC-BY-NC** — free for research use with attribution, but **NonCommercial**. That gates the *mint* step: minting is permanent/immutable and creates tradeable tokens, which is hard to square with NonCommercial. The molecular *structures* (SMILES/InChIKey/CID) are public-domain and safe to mint; the *odour descriptors* are the encumbered, value-add layer.
- **Verdict split:** scaling the *display site* to full Leffingwell is license-clean (non-commercial research use, attributed) and a real step up — the UMAP scent map especially gains meaning at 3,500 points, and Pyrfume ships SMILES+CIDs so enrichment is mostly a join. **Minting** the descriptors is blocked until the license is cleared; structures + our own volatility-derived curation remain mintable today.
- **Outreach — Pyrfume:** emailed **Rick Gerkin** (rgerkin@asu.edu, Pyrfume lead; now also Head of Neuroscience at Osmo) asking permission to record an attributed, public-good on-chain version, and flagging that the rights may trace to Leffingwell & Associates. Introduced GenesisL1/MOLNFT with a self-serve link (molnft.org) rather than a call. Sent from the Formentera Essence address for in-field credibility. Fallbacks noted: GitHub/LinkedIn, or Joel Mainland (Monell, paper's corresponding author).
- **Outreach — Joe (DM):** answered his SMILES-DB questions — the DB is tiny (our molecules avg ~24 B of SMILES; all of ChEMBL ~120 MB; Leffingwell < 200 KB), so gas is the only real variable; proposed storing InChIKey+SMILES as on-chain fields and rendering the tokenURI JSON as a view (no IPFS file for small molecules). Asked the pivotal question: can MOLNFTs be minted **non-transferable / registry-only (soulbound-style)**, or are they always tradeable — because non-tradeable would strengthen the NonCommercial licensing case.

## 2026-07-29 — Joe's resolver folded into the index (v3) · `1eff9e9`

Joe asked to share the whole thing with the community and to include the MolNFT resolver framework he'd layered on top ("his gift"). Rather than ship it as a separate tab that duplicated the 99-molecule table, we folded his resolver **into the Molecule Index page itself** — where he'd originally placed it, above the table — so there's a single source of truth again and nothing drifts as molecules get added.

- Extracted Joe's resolver CSS, the `<section>`, and its ~270-line read-only JS verbatim and merged them into the page generator (`mkhtml2.py`) via placeholder injection, keeping his "Prepare MolNFT link" button wired into each 3D panel.
- Dropped the standalone **Resolver** nav tab; nav is back to three (Molecule index · Scent map · SMILES→3D). Bumped the badge to **v3 · MolNFT resolver** and credited Joe in the footer.
- Verified live: 99 molecules intact, both resolver panes render, mock links generate correctly against the GenesisL1 IPFS gateway, ethers + 3Dmol load. The old `molnft-resolver.html` is now redundant (unlinked) and pending a decision on removal.
- Drafted a community announcement for the group, crediting Joe's framework.

## 2026-07-29 — SMILES → 3D prototype + wired in as a tab · `f4b70f9`, `9238912`, `a4556c9`

Prototyped Joe's efficiency idea: regenerate a molecule's 3D structure **client-side from its SMILES string alone**, no stored structure file needed. This is the argument for putting small molecules on-chain as SMILES (compact, canonical) and rebuilding geometry in the browser, reserving IPFS for things you genuinely can't regenerate (proteins/receptors).

- RDKit.js MinimalLib turned out to be 2D-only (no 3D embed), so switched to **OpenChemLib** (`ConformerGenerator` → real V2000 3D) rendered by **3Dmol.js**.
- Fixed a heavy-atom count bug: the conformer generator adds hydrogens in-place, so the count had to be captured *before* generation (limonene now correctly reports 10 heavy atoms, not 26).
- Added it as a nav tab across the pages. (A cache-of-canonical-URL hiccup made the tab look like it vanished on the index; proved the server was serving the right file and it was browser HTTP cache — cleared, confirmed working.)

## 2026-07-29 — Scent map (UMAP) · `83d88a6`, `1d7e30d`

Built a "map of smell" — molecules projected into 2D by their odour descriptors, a nod to the Turin/MacKay Kohonen-map idea. Prototyped both SOM and UMAP; chose **UMAP only** and wired it in as a nav tab.

- Descriptors → binary vectors; `umap-learn` with cosine metric, `n_neighbors=15`, `min_dist=0.2`. A few disconnected points were blowing up min-max normalization and rendering an empty map — fixed with robust 2nd–98th-percentile normalization.
- Nine odour groups (kept distinct, not merged) with a palette validated against the dataviz skill's colorblind checks. Nine categories can't fully pass CVD separation, so identity is reinforced by hover/isolate/table, not colour alone.
- Deferred polish (agreed "for later"): shrink dots as the set scales; an outline-only style for a single highlighted group.

## 2026-07-29 — MolNFT / IPFS resolver verified + on-chain read proven · `c0be5bf`

Reviewed Joe's `AromaIndexMolNFT.html` end-to-end and hosted it as a preview.

- **Security:** read-only — `eth_call`/`eth_chainId` only, no wallet, no signing, no key requests; values HTML-escaped, links protocol-checked, payload capped at 12 MB. Clean.
- **Correctness:** unit-tested the hand-rolled ABI encode/decode against ethers 6 — **7/7 pass** (calldata byte-identical, `tokenURI` selector matches canonical `0xc87b56dd`, string tuples round-trip).
- **Live proof:** ran the actual on-chain read against real GenesisL1 endpoints (RPC `api.lcserve.net`, MolNFT `0xDE37…37Eba`). Token **16277 = "1nu3" = limonene-1,2-epoxide hydrolase** → resolved owner + tokenURI → IPFS metadata → 260 KB PDB rendered in 3D. Thematically perfect: the chain already holds the *receptor* for limonene; the index holds the *ligand*.

## 2026-07-28 — Boiling point + vapor pressure (25°C) columns · `6f046c7`

Added Joe's suggested columns: normal boiling point and vapor pressure at 25°C — the real physical measures of volatility behind the top/heart/base tiers (VP falls, BP and MW climb as you go down). Experimental values from PubChem where available; estimated ones (grey italic) from BP via Clausius–Clapeyron with a Kistiakowsky enthalpy.

- Caught a bad vanillin reading (a high-temperature VP defaulted to 25°C, ~133 Pa); re-fetched requiring an explicit ~25°C measurement → corrected to ~15.7 mPa.

## 2026-07-28 — Rung 1: PubChem enrichment + 3D structure viewer · `0fd95fc`, `fc02302`

Enriched all 99 molecules with **PubChem CID · SMILES · InChIKey** and added a click-to-view **3D structure viewer** (lazy-loads the PubChem conformer by CID). PubChem isn't reachable from the build container, so fetches went through the browser.

- Six hand-typed formulas disagreed with PubChem; all six CAS-resolved and IUPAC-confirmed (PubChem was right) → corrected formula + MW, re-sorted, refreshed stats.

## 2026-07-28 — Live search · `f2c9898`

Added an instant client-side search over molecule name, family, and odour descriptors (and formula), with a live count and empty state.

## 2026-07-27/28 — Repo + hosting + feasibility report · `a2008df`, `50e3f62`

Migrated the 99-molecule index into its own repo (**VanPez/aroma-index**, MIT) and hosted it on GitHub Pages. Delivered the deep-research **feasibility report** (`aroma-index-feasibility.md`) on the MOLNFT-extension concept.

- Established the storage architecture that guides everything since: **small molecules → on-chain SMILES + client-side 3D regeneration** (~1M molecules ≈ 3 GB, never threatens the 1 TB concern); **proteins/receptors → IPFS PDB** (can't be folded from identifiers). The 1 TB worry is a protein problem, not a ligand problem.

---

### Still open / next

- **Waiting on Pyrfume (Rick Gerkin):** permission / license path to mint the Leffingwell descriptors on-chain (or a pointer to Leffingwell & Associates as the rights holder).
- **Deploy own MolNFT contract + mint the 95:** permissionless; Mike offers manual help until his UI lands. Deploy/sign/mint is yours (I only prep data). Decide chain (mainnet vs testnet first) and collection name.
- **Leffingwell now needs a commercial-friendly path** (tradeable + CC-BY-NC clash): a commercial licence from Pyrfume/Leffingwell, or a CC0/CC-BY odour source, or descriptors off-token.
- **Leffingwell display scale-up (green-lit, license-clean):** join Pyrfume's ~3,500-molecule set, derive note tiers from volatility programmatically, tune the scent map (smaller dots finally needed), check table/search hold at 3,500. I prep; nothing minted.
- **MolNFT small-molecule field:** Mike says a new field for small molecules is easy to add; the spec is ready (InChIKey canonical + SMILES + core props, ~200 B/token, JSON rendered on the fly).
- **Rung 2 — minting:** mint-ready data for the 95 is **built and staged** (`mint/`); needs no licence. The actual sign + gas is yours/Joe's (I never touch keys or send transactions). Gated only on Mike's mint-path + non-transferable confirmation.
- Scent-map polish: smaller dots at scale; outline-only single-group style.
- Decide whether to delete the now-redundant `molnft-resolver.html`.

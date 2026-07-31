# An on-chain aroma-molecule index for GenesisL1 — feasibility brief

*A DeSci proof-of-concept assessment for the MOLNFT / GL1F stack. Prepared for Ivan (Vanpez), July 2026. Written for a domain-expert (perfumer) reader with a technical appendix for founder "M".*

---

## The one-paragraph answer

The idea is sound, genuinely novel, and buildable — with one commercial caveat you have to design around. The perfumery intuition you started from (smaller/lighter molecules evaporate faster and read as top notes; heavy ones linger as base notes) is not just folklore: it is a well-established structure–property relationship, and the underlying driver (vapor pressure) is predictable from molecular structure alone with very high accuracy. Open odor datasets exist and are large, but almost all of the good ones carry **non-commercial** licenses, so the redistributable on-chain layer has to be built on public-domain identifiers (PubChem/CAS/SMILES) plus your own curation rather than by re-hosting those datasets wholesale. No one has built a *structured, verifiable, on-chain index of aroma molecules* — the existing "fragrance blockchain" projects are art NFTs, consumer tokens, or IP-rights tokenization, none of which put molecular structure on-chain — so MOLNFT would be occupying open ground. And the note-tier prediction task is a good fit for GenesisL1's deterministic gradient-boosted-tree inference (GL1F): it is an *easier* problem than full odor-descriptor prediction, and even for the harder odor task, compact-feature tree models land within reach of the graph-neural-network state of the art while being deterministic and cheap enough to run on-chain.

---

## 1. The science holds up: structure → note tier is real and computable

The note pyramid is an evaporation-rate phenomenon. The most volatile species leave the headspace first (top notes, minutes), the least volatile persist for hours to days (base notes). This is standard and well-sourced. The quantity that actually governs it is **saturated vapor pressure**, not molecular weight per se — the peer-reviewed headspace relationship combines several properties into a single "who dominates the smell right now" constant:

> K = (P_sat × M_w) / (Threshold × RT)

— i.e. vapor pressure, molecular weight, odor-detection threshold and temperature together (Chemical Engineering Science, perfume-diffusion studies).

**Why this matters for the index, and an important honesty caveat.** Molecular weight is a *useful proxy* for volatility (it's cheap, it's in every record, and it trends the right way — the v2 prototype's average MW climbs cleanly 139 → 170 → 208 Da across top → heart → base). But MW alone is imperfect: within base notes, vanillin (the lightest) actually diffuses more than heavier base molecules, so real behavior depends on more than mass. During verification, two draft claims that leaned on "odorants cluster around ~187 Da, therefore MW is a volatility proxy" were **refuted** — the source they came from measures volatility directly via vapor pressure and explicitly does *not* endorse MW as the proxy. The defensible framing, which the prototype already uses, is: **MW is the display-friendly proxy; a production index should compute the tier from measured or QSPR-estimated vapor pressure.**

And vapor pressure *is* computable from structure. A QSPR model on ~45,000 vapor-pressure values (≈1,500 compounds, DIPPR 801) using 29 structure-derived descriptors reached **R² = 0.990** with ~7% average deviation across a very wide temperature range — so an on-chain predictor could derive volatility (hence note tier) from a molecule's structure rather than needing a lab measurement for every entry. That is the single most encouraging technical finding in the brief: the physical quantity your index is organized around is exactly the kind of thing a structure-in / number-out model does well.

---

## 2. Data exists — but licensing is the real constraint

There is plenty of structured odor data. The catch is that the best datasets are **non-commercial**, which matters the moment you talk about redistributing them on a public, potentially commercial chain. The landscape, from most-open to most-restricted:

| Source | What it gives you | Size | License / reuse reality |
|---|---|---|---|
| **PubChem** | Structures, SMILES, InChI, MW, CAS mapping | Millions | **Public domain** — the clean base layer for the redistributable index |
| **IFRA Transparency List (2025)** | The perfumer's palette: CAS + names | 3,691 ingredients (1,021 natural complex substances) | **No structures/SMILES, no odor descriptors, no stated license** — great as a *selection* reference, not a redistributable dataset |
| **Pyrfume** (Nature Sci Data, 2024) | Structure + descriptors + perceptual ratings, tidy schema | 20,000+ odorants, 40+ datasets | **CC BY-NC-(ND/SA)** — non-commercial; a direct blocker for commercial on-chain redistribution |
| **Leffingwell Odor Dataset** | ML-ready: structures, fingerprints, Mordred descriptors, train/test splits | 3,523 molecules | **CC BY-NC** — excellent for *training/research*, non-commercial for redistribution |
| **GS-LF (Good Scents + Leffingwell)** | SMILES + ~100 binary odor-percept labels | ~3,300–4,000 | Underlying Good Scents is **proprietary**; benchmark doc states **no explicit license** |
| **The Good Scents Company** | Per-ingredient CAS, formula, MW, odor descriptors | Large | **Copyrighted, no open license** — cross-reference only, scraping is legally risky |

**The practical route this points to:** build the redistributable, on-chain layer from **public-domain identifiers (PubChem: SMILES, formula, MW, CAS)** plus **your own hand-curated note-tier and descriptor annotations** (which is exactly what the prototype already does — the descriptors are short, human-written, and attributed). Use the NC datasets (Pyrfume, Leffingwell) *only* as private training data for a model or as a research cross-check, never re-hosted verbatim in the commercial index. For anything that would ship commercially, IFRA/RIFM and Good Scents reuse rights should be confirmed with the source directly — do not assume.

---

## 3. Novelty: nobody has built this

This is where the concept is strongest. Two adjacent fields are busy, but neither occupies your niche.

**AI olfaction is a hot, credible frontier — and it's closed.** Osmo (Alex Wiltschko's team, out of Google Research's 2019 "Learning to Smell" work) published the **Principal Odor Map** in *Science* (2023): a graph neural network that predicts odor descriptors from structure and, on 400 novel odorants, matched a trained human panel's mean better than the median individual panelist. Osmo raised a **$70M Series B (Feb 2026)**. But their map and data are proprietary and closed. An **open, verifiable** structure→odor index is precisely the public-good gap that a closed leader leaves on the table.

**"Fragrance blockchain" projects exist — but none put molecules on-chain.** Look Labs' 2021 "world's first digital fragrance" NFT was a *spectral scan of one perfume sold as art* (10 ETH on Rarible), not a structural index. Smell Token digitizes *device parameters* (cartridge/duration/intensity) for a "smell-to-earn" consumer token, not chemistry. Even the flagship DeSci project **Molecule Protocol** tokenizes *IP rights* to research assets (IP-NFTs on Ethereum) — it does **not** commit molecular structure on-chain. So GenesisL1's MOLNFT (on-chain structure commitments) is architecturally distinct from all of them, and a queryable aroma-molecule index built on it would be, as far as this research found, **the first of its kind**. That's a clean positioning line for M: *complementary to Molecule Protocol, not duplicative; open where Osmo is closed.*

---

## 4. GL1F / GBDT technical fit: pragmatic, deterministic, cheap

GenesisL1's on-chain inference engine runs gradient-boosted decision trees (GL1F). Is that a good engine for this? The nuanced, honest answer:

- **For molecular property prediction generally, gradient boosting is competitive with deep learning** and often the practical SOTA (Journal of Cheminformatics, 2023). XGBoost tends to edge LightGBM/CatBoost; algorithm choice scales with dataset size.
- **For full odor-descriptor prediction specifically, GNNs currently win.** The POM and multiple benchmarks show graph models beat classical/tree methods (e.g. GCN +24.1% relative over the best traditional model; macro-F1 ~0.52 vs ~0.47). Trees can't see graph topology the way a GNN can.
- **But among non-graph methods, GBDT is the strongest class, and it closes most of the gap with compact features.** A Morgan-fingerprint XGBoost model hit AUROC 0.828 for odor prediction; with feature selection down to just **12–33 descriptors per label**, tree models reached near-competitive macro-F1 while *slashing computation* — which is exactly what you want when every inference costs gas.

**The synthesis for on-chain use:** the deterministic, reproducible, verifiable requirement of on-chain inference actually *favors* GBDT over a GNN — a tree ensemble over a fixed, small descriptor vector gives the same answer every time and is auditable, whereas a large GNN is heavier and harder to make bit-reproducible. And critically, **your headline feature — note tier from volatility — is an easier task than full odor prediction**: it's essentially a regression/low-cardinality classification off vapor pressure and a handful of descriptors (MW, logP, H-bond counts, functional groups), which is squarely in GBDT's sweet spot. Full odor-family tags can be the "v2 model" ambition; note tier is the "v1, ships now" model.

---

## 5. Recommended v1 scope, schema, and risks

**Scope (v1 — deliberately small and honest).** A curated open index of ~100–300 widely-used, single-molecule aroma chemicals (the prototype's 99 is a good start), each committed on-chain via MOLNFT with a public structure hash, organized by note tier. Ship the *note-tier predictor* (volatility-driven) as the first GL1F model. Defer full structure→odor-descriptor prediction to v2. Explicitly label it a proof-of-concept, exclude captive/proprietary molecules (as the prototype does), and represent naturals by their signature molecule with a source note (black pepper → rotundone, vetiver → khusimol) rather than pretending a natural is one compound.

**Suggested per-molecule schema:**

- `name`, `cas`, `iupac` — identity (CAS from public sources)
- `smiles`, `inchikey` — structure (PubChem, public domain); the InChIKey is the natural on-chain commitment / dedup key
- `formula`, `mw` — from structure
- `vapor_pressure_est`, `logp` — computed descriptors (the volatility basis)
- `note_tier` — {top, heart, base}, model output + rationale
- `odor_descriptors[]` — short curated tags, **with source attribution per row**
- `family` — floral / woody / citrus / etc. (display grouping)
- `provenance` — data source + license tag for every field (so the index is self-documenting about what's public-domain vs. curated)

**Top risks, and mitigations:**

1. **Licensing contamination** (highest). *Mitigation:* public-domain identifiers + own curation only in the shipped layer; NC datasets stay in the private training corpus; confirm IFRA/Good Scents terms before any commercial use.
2. **Over-claiming the science.** MW-as-proxy was refuted in verification; don't build marketing on it. *Mitigation:* frame tier on vapor pressure, MW as display proxy — the prototype's wording already does this.
3. **Odor prediction being oversold vs. Osmo.** *Mitigation:* position v1 as *open + verifiable + note-tier*, not "we beat the POM." Odor tags are curated, not model-claimed, in v1.
4. **Naturals vs. single molecules confusion** for a perfumer audience. *Mitigation:* the signature-molecule mapping with source notes (already in the prototype).
5. **On-chain cost / reproducibility of inference.** *Mitigation:* compact 12–33 descriptor feature vector, deterministic GBDT, tier task first.

**Bottom line.** Green light for a proof-of-concept. It's scientifically defensible, it's novel, it fits the MOLNFT + GL1F architecture unusually well, and the one serious constraint (data licensing) is fully navigable by building on public-domain structure data plus your own curation — which is the path the live prototype is already on.

---

## Sources

Structure → note tier / volatility: Chemical Engineering Science, "The diffusion of perfume mixtures and odor performance" (sciencedirect.com/science/article/abs/pii/S0009250909000700); "QSPR for a very large vapor-pressure dataset" (sciencedirect.com/science/article/abs/pii/S0009250912002035); McClelland & Jurs, *J. Chem. Inf. Comput. Sci.* 2000, 40(4):967–975 (pubs.acs.org/doi/abs/10.1021/ci990137c); "In silico prediction of fragrance retention grades (QSPR)" (sciencedirect.com/science/article/abs/pii/S0169743921001921).

Open data & licensing: Pyrfume, *Nature Scientific Data* 2024 (pmc.ncbi.nlm.nih.gov/articles/PMC11557823/) and Zenodo v1.0.0 (zenodo.org/records/13820408); Leffingwell Odor Dataset, Zenodo 10.5281/zenodo.4085097; GS-LF dataset docs (deepwiki.com/microsoft/olfaction/4.2-gs_lf-dataset); IFRA Transparency List (ifrafragrance.org/transparency-list/about-the-ifra-transparency-list); The Good Scents Company (thegoodscentscompany.com).

AI-olfaction prior art: Lee/Wiltschko et al., "A principal odor map unifies diverse tasks in olfactory perception," *Science* 2023 (science.org/doi/10.1126/science.ade4401); Google Research, "Learning to Smell" (research.google/blog/learning-to-smell-...); Osmo $70M Series B, BusinessWire Feb 2026; "QSAR-guided generative framework for odorants," arXiv 2512.23080.

Blockchain/molecular prior art: Look Labs fragrance NFT, Dezeen 2021 (dezeen.com/2021/04/08/look-labs-digital-fragrance-nft/); Smell Token litepaper (smelltoken.com/litepaper); Molecule Protocol IP-NFT (github.com/moleculeprotocol/IPNFT).

GBDT / on-chain ML fit: "Practical guidelines for gradient boosting for molecular property prediction," *J. Cheminformatics* 2023 (link.springer.com/article/10.1186/s13321-023-00743-7); "ML models on molecular fingerprints for odor decoding," *Nature Comms Chemistry* 2025 (nature.com/articles/s42004-025-01651-7); "GNNs vs. traditional QSAR for multi-label odor prediction," *Molecules* 2025 (mdpi.com/1420-3049/30/23/4605); "Predicting odor from molecular structure: multi-label classification," *Sci. Reports* 2022 (nature.com/articles/s41598-022-18086-y).

*Method note: findings were produced by a multi-agent research fan-out across five dimensions, with each claim independently verified; 55 of 57 verification checks upheld, 2 refuted (both the MW-as-volatility-proxy overreach flagged in §1).*

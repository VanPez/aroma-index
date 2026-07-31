# Odour-dataset licence scan — which sources can back *tradeable* MOLNFTs

**Date:** 2026-07-31 · **For:** Aroma Molecule Index scale-up (not the 95-molecule pilot) · **Author:** prepared for vanpe

## Why this scan exists

The pilot mint of 95 molecules needs **no third-party licence**: its structures are public-domain PubChem
facts and its note tiers, families and descriptors are original curation. This scan only concerns the
**scale-up** — going from 99 to a few thousand molecules by adopting an existing odour dataset.

The constraint that drives everything: **MOLNFTs are standard, transferable ERC-721s** (confirmed by
Mike). A sellable token is a commercial use. So any source under a **NonCommercial** licence is
unusable, regardless of how good the data is.

**What is and isn't at issue.** Molecular structures and identifiers (SMILES, InChIKey, formula, CAS,
PubChem CID) are *facts*, not creative works — under *Feist v. Rural* (US) and equivalents, individual
facts aren't copyrightable, and PubChem is public domain. The encumbered layer is:

1. the **odour descriptors** ("rose, honey, powdery") — expert judgements someone authored, and
2. the **compilation** — the selection and arrangement of *which* molecules form the set, which in the
   EU can attract a *sui generis* database right even where each datum is free.

Point 2 is the one people miss. Re-typing Leffingwell's descriptors in your own words does not launder
the set, because the *choice of 3,523 molecules* is itself the protected compilation.

> Not legal advice. Licences were read at source on 2026-07-31; verification status is marked per row.

---

## Comparison table

| Dataset | # molecules | Structures? | Odour descriptors? | Licence | Commercial OK | Source | Redistribution / attribution notes |
|---|---|---|---|---|---|---|---|
| **Keller & Vosshall 2016** (Pyrfume `keller_2016`) | 480 | Yes (CID) | Yes — 19 semantic descriptors + intensity/pleasantness, rated by 61 subjects | **CC BY 4.0** article + **CC0 1.0** for the data | ✅ **YES** | [BMC Neurosci 10.1186/s12868-016-0287-2](https://bmcneurosci.biomedcentral.com/articles/10.1186/s12868-016-0287-2) | Rights statement reads *CC BY + CC0* — CC0 waiver applies to the data. Attribute the paper anyway (norm, and CC BY covers the text). Cleanest licence found. |
| **Wikidata** (chemical items) | Not quantified here | Yes (SMILES/InChI/CID) | Partial, uneven | **CC0 1.0** (all structured data) | ✅ **YES** | [Wikidata:Licensing](https://www.wikidata.org/wiki/Wikidata:Licensing) | *"All structured data in the main, property and lexeme namespaces is made available under the Creative Commons CC0 License."* No attribution required. Coverage of odour descriptors is sparse and unsystematic — good as a **supplement or cross-check**, weak as a primary descriptor source. |
| **Mainland et al. 2015** (Pyrfume `mainland_2015`) | ~*not counted* | Yes | ❌ No — olfactory *receptor* responses, not odour words | Sci Data (open access) — **not verified in this scan** | ⚠️ n/a | [Sci Data 10.1038/sdata.2015.2](https://doi.org/10.1038/sdata.2015.2) | No use-restriction note in the Pyrfume manifest. Irrelevant for descriptors — listed so it isn't re-checked later. |
| **Abraham et al. 2012** (Pyrfume `abraham_2012`) | 353 | Yes | ❌ No — detection *thresholds* | Chemical Senses (OUP, subscription) — **not verified** | ⚠️ CAUTION | [Chem Senses 10.1093/chemse/bjr094](https://doi.org/10.1093/chemse/bjr094) | Pyrfume notes data was *"scraped from in-line tables"* of a subscription journal. No descriptors anyway. |
| **Leffingwell PMP 2001** (via Pyrfume/Zenodo) | 3,523 | Yes | Yes — 113 expert labels | **CC BY-NC 4.0**, files **Restricted** | ❌ **NO** | [Zenodo 4085098](https://zenodo.org/records/4085098) | Zenodo record now gates the files behind an access request whose stated condition is *"free non-commercial use"*. Pyrfume manifest: *"see LICENSE for use restrictions … terms of John Leffingwell and Google."* Unusable for tradeable tokens without a negotiated commercial licence. |
| **Good Scents Company** (Pyrfume `goodscents`) | ~thousands | Yes | Yes | **Proprietary / unclear** | ❌ **NO** | [manifest.toml](https://github.com/pyrfume/pyrfume-data/blob/main/goodscents/manifest.toml) | Manifest: *"see LICENSE for use restrictions according to the terms of The Goodscents Company"* and — decisively — *"Pyrfume developers make no claims concerning copyright."* Upstream rights unresolved. |
| **Arctander 1960** (Pyrfume `arctander_1960`) | ~3,000 | Yes | Yes — labels + prose descriptions | **Copyrighted book** | ❌ **NO** | [manifest.toml](https://github.com/pyrfume/pyrfume-data/blob/main/arctander_1960/manifest.toml) | *Perfume and Flavor Materials of Natural Origin*, ISBN 978-0931710360. Manifest: *"see LICENSE for use restrictions."* Prose descriptions are plainly creative authorship. |
| **Dravnieks 1985** (Pyrfume `dravnieks_1985`) | ~140 | Yes | Yes — 146-descriptor profiles | **ASTM copyrighted** (DS61) | ❌ **NO** / CAUTION | [manifest.toml](https://github.com/pyrfume/pyrfume-data/blob/main/dravnieks_1985/manifest.toml) | Source is ASTM *Atlas of Odor Character Profiles* (DOI 10.1520/DS61-EB) — a sold standards publication. Manifest lists no LICENSE file, but absence of a licence is not a grant. |
| **FlavorDB / FlavorDB2** | 25,595 | Yes | Yes (taste + odour) | **CC BY-NC-SA 3.0** | ❌ **NO** | [cosylab.iiitd.edu.in/flavordb2](https://cosylab.iiitd.edu.in/flavordb2/) | Licence stated in the site footer. Fails twice: **NC** blocks tradeable tokens, and **SA** would force a copyleft licence onto the derived collection. |
| **SuperScent** | ~2,100 | Yes (2D/3D) | Yes | **CC BY-NC 2.0** — *reported, not verified at source* | ❌ **NO** (as reported) | [NAR 10.1093/nar/gkn695](https://academic.oup.com/nar/article/37/suppl_1/D291/1005806) | Original host appears defunct; licence taken from secondary description, so treat as unconfirmed. NC either way per available information. |
| **Flavornet** | ~700 | Partial | Yes (GC-O odour descriptions) | **No explicit licence found** | ⚠️ CAUTION | [flavornet.org](http://www.flavornet.org/) | Site did not return content when fetched. No licence grant located → default "all rights reserved". |
| **OpenPOM / Principal Odor Map** | *code only* | n/a | n/a | **MIT** (the *code*) | ⚠️ CAUTION — see note | [github.com/BioMachineLearning/openpom](https://github.com/BioMachineLearning/openpom) | **The trap:** MIT covers the model code, not training data. OpenPOM is trained on **Leffingwell + Good Scents**, so its *outputs and any redistributed training set inherit those restrictions*. An MIT badge here does not launder NC data. |
| **FEMA GRAS / Flavor Ingredient Library** | ~2,900 | Partial | ❌ Not odour descriptors (safety/GRAS status) | **Proprietary**, © FEMA, partly login-gated | ❌ **NO** | [femaflavor.org/flavor-library](https://www.femaflavor.org/flavor-library) | Industry association content under its own Terms of Use. FEMA numbers themselves are identifiers/facts. |
| **FDA Substances Added to Food (EAFUS)** | ~4,000 | Partial | ❌ No | **US Government — public domain** | ✅ YES (but no descriptors) | [FDA inventory](https://www.hfpappexternal.fda.gov/scripts/fdcc/index.cfm?set=FoodSubstances) | Useful as a **licence-clean molecule list** to *select* a set independently — which solves the compilation problem, not the descriptor problem. |
| **PubChem** | — | Yes | Some organoleptic annotations | Public domain *as an archive*; **individual annotations inherit their upstream source licence** | ⚠️ CAUTION | [pubchem.ncbi.nlm.nih.gov](https://pubchem.ncbi.nlm.nih.gov/) | Safe for structures/identifiers/properties (what the pilot already uses). Do **not** assume its *odour* annotation blocks are free — many are re-served from third-party databases with their own terms. |

Legend: ✅ usable for tradeable tokens · ⚠️ conditional or unverified · ❌ ruled out.

### On SA, ND and ODbL specifically

- **ShareAlike (SA)** — not a hard block on selling, but viral: the derived collection must be released
  under the same licence. For an on-chain collection that means committing every future token's metadata
  to CC-BY-SA, and it conflicts with the MIT posture of the rest of this project. Treat as a no.
- **NoDerivatives (ND)** — fatal in practice. Re-encoding descriptors into a new schema, joining them to
  our tiers, and rendering an ERC-721 `tokenURI` is by definition a derivative.
- **ODbL** — share-alike for databases *plus* a "keep it open" obligation on any publicly-used derived
  database. Compatible with selling in principle, but it would require licensing the resulting on-chain
  database under ODbL, which is a bigger commitment than it looks. None of the datasets scanned use it.
- **ODC-BY** — would be fine (attribution only). None found.

---

## Recommendation, ranked

### 1. Keller & Vosshall 2016 as the licensed descriptor core — *the only clean, ready-made option found*

480 molecules with **CC BY 4.0 + CC0 data**, verified at the publisher's own rights statement. It is the
only descriptor-bearing set in this scan that permits commercial use outright. Trade-offs to accept:

- **480 molecules, not 3,500.** Roughly 5× the current index, not 35×.
- **Descriptors are perceptual ratings from untrained subjects**, not perfumer vocabulary — 19 semantic
  scales, numeric rather than the evocative labels the index uses now. Different in kind from
  Leffingwell's expert tags, and arguably *more* scientifically defensible for a DeSci artifact: they are
  measurements with subjects and replicates, not opinions.
- The molecule set was chosen for *chemical diversity*, so it includes many compounds no perfumer uses.
  Expect to filter.

### 2. Independent molecule list + our own descriptors — *the strategically better path, and the one I'd actually take*

Select the molecule set from a licence-clean list (FDA/EAFUS, FEMA numbers as identifiers, PubChem, or
simply perfumery domain knowledge as already done for the 99), then write the odour descriptors as
original curation — exactly the method that makes the 95-molecule pilot licence-free today.

Why this beats option 1 despite being more work:

- **It scales without ever re-opening the licence question.** Every future addition stays clean.
- **It's the honest version of the project's own claim.** The index is already positioned as *hand-curated*;
  its value is the curation, not a re-hosted third-party table.
- **It sidesteps the compilation right**, because the selection is ours.
- It keeps faith with the Pyrfume outreach — no workaround that would embarrass the good-faith ask to Rick.

The realistic shape: use **option 1 as a validation set** (Keller's CC0 ratings are a free, legitimate way
to sanity-check our tiers and descriptors against measured human data) while growing the curated index
under option 2. That combination is both licence-clean and scientifically stronger than adopting
Leffingwell would have been.

### 3. Negotiate a commercial licence for Leffingwell — *only if 3,500 expert-labelled molecules is the actual goal*

Rick Gerkin is already contacted. If he replies, the ask must now be explicit that **tokens are tradeable**,
which is a commercial licence request, not a public-good one — and the rights may sit with Leffingwell &
Associates / Google rather than Pyrfume. Low probability, and the Zenodo record moving to *Restricted*
suggests tightening rather than loosening. Do not plan around it.

**Conclusion:** the scale-up is *not* blocked, but it is blocked on the assumption that it would come from
a big existing table. No permissive equivalent of Leffingwell exists. Grow the curated index ourselves,
and use Keller & Vosshall's CC0 data as free external validation.

---

## Verification status

Read directly at source on 2026-07-31: Leffingwell (Zenodo record), Keller & Vosshall (publisher rights
statement, `CC BY + CC0`), FlavorDB2 (site footer), Wikidata (official licensing policy), Good Scents /
Arctander / Dravnieks / Mainland / Abraham (Pyrfume `manifest.toml` for each), FEMA (site + footer),
OpenPOM (repo).

**Not verified at source — do not rely on without checking:** SuperScent (host appears defunct; licence
from secondary source), Flavornet (site returned no content), Mainland 2015 and Abraham 2012 publisher
licences (not needed — neither carries odour descriptors), per-archive molecule counts marked *~*.

One structural caveat: the `pyrfume-data` repository carries an **MIT LICENSE at its root**, which covers
the Pyrfume project's own code and packaging — **it does not and cannot relicense third-party data** held
in the archives, several of which carry their own explicit restrictions. Judge each archive by its
`manifest.toml` and its upstream source, never by the repo badge.

## Sources

- [Leffingwell Odor Dataset — Zenodo 10.5281/zenodo.4085098](https://zenodo.org/records/4085098)
- [Keller & Vosshall 2016, BMC Neuroscience](https://bmcneurosci.biomedcentral.com/articles/10.1186/s12868-016-0287-2)
- [Pyrfume data archives (manifests)](https://github.com/pyrfume/pyrfume-data)
- [FlavorDB2](https://cosylab.iiitd.edu.in/flavordb2/)
- [Wikidata:Licensing](https://www.wikidata.org/wiki/Wikidata:Licensing)
- [FEMA Flavor Ingredient Library](https://www.femaflavor.org/flavor-library)
- [OpenPOM](https://github.com/BioMachineLearning/openpom)
- [SuperScent, Nucleic Acids Research](https://academic.oup.com/nar/article/37/suppl_1/D291/1005806)

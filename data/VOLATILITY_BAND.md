# `volatility_band` — a declared convention, not a measurement

## Definition

```
volatility_band = light   if MW <  150
                  medium  if MW <  200
                  heavy   otherwise
```

That is the whole rule. It is applied mechanically to every molecule with a known molecular weight.

## Why round numbers

Best-fit thresholds against the 99 curated molecules are 146.14 / 206.33, giving 67% agreement.
The round convention 150 / 200 gives 66%. **The extra 1% is not worth pretending the numbers were
derived from anything.** Round thresholds make it obvious this is a stated convention that anyone can
apply, disagree with, or re-cut.

## What it is not

It is **not** a note tier. It agrees with the curated `note` field on only **67%** of molecules, and the
disagreement cannot be tuned away, because the information is not in molecular weight:

| Molecule | Formula | MW | `volatility_band` | curated `note` |
|---|---|---|---|---|
| Linalool | C10H18O | 154.25 | medium | **top** |
| Geraniol | C10H18O | 154.25 | medium | **heart** |
| Menthol | C10H20O | 156.27 | medium | **top** |
| Citronellol | C10H20O | 156.27 | medium | **heart** |

Identical formula, identical mass — different perfumery behaviour, because the –OH sits on a tertiary
or ring carbon in the top notes and on an exposed primary carbon in the heart notes. Primary alcohols
hydrogen-bond strongly, evaporate slowly and linger. No threshold on MW can separate these; a band
assigns all four to `medium`.

## Why both fields exist

- **`volatility_band`** — computed, reproducible, present on every molecule with an MW, scales to any
  molecule ever added, safe to publish or mint without qualification.
- **`note`** — the maintainer's perfumery judgement. Present only where that judgement has actually been
  made. Cannot be sourced (patents assert tiers for accords, never for individual compounds — 0 direct
  assertions across 60 patents) and cannot be computed (a fitted rule reproduces it at 56% under
  leave-one-out).

**The ~33% where they disagree is precisely the information the curation contributes.** If the band
reproduced the tier, the curation would be redundant. It doesn't, so it isn't.

## Coverage (2026-08-01)

| set | banded | light | medium | heavy |
|---|---|---|---|---|
| curated (99) | 96 | 22 | 42 | 32 |
| sourced (218) | 218 | 99 | 89 | 30 |

Three curated molecules have no MW (trade-name captives with no public structure) and no band.

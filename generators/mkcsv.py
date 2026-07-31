# -*- coding: utf-8 -*-
# Rebuild aroma-index.csv from rows2.json.
# The CSV is the machine-readable download people actually build on, so it
# must never be a hand export — it was, and it silently kept three empty
# formula/mw cells after the source was fixed. Regenerate it with everything else.
import csv, json

COLS = ["name","cas","cid","inchikey","smiles","formula","mw",
        "bp_c","bp_est","vp_pa","vp_src","note","family","descriptors"]

rows = json.load(open("rows2.json"))
with open("aroma-index.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for r in rows:
        w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in COLS})

filled = sum(1 for r in rows if r.get("formula") and r.get("mw") is not None)
print(f"wrote aroma-index.csv — {len(rows)} rows, {filled} with formula+mw")

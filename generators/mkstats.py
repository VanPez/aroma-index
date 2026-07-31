# -*- coding: utf-8 -*-
# Recompute data/stats2.json from rows2.json.
# stats2.json feeds the site's per-tier summary ("Avg MW rises with tier"),
# so it must be regenerated whenever rows2.json changes — otherwise the
# headline numbers silently drift from the table below them.
# Means/min/max are over molecules that HAVE an mw; n is the full tier count.
import json

rows = json.load(open("rows2.json"))
stats = {}
for t in ("top", "heart", "base"):
    grp = [r for r in rows if r["note"] == t]
    mws = [r["mw"] for r in grp if r.get("mw") is not None]
    stats[t] = {
        "n": len(grp),
        "mw_min": min(mws),
        "mw_max": max(mws),
        "mw_mean": sum(mws) / len(mws),
    }
    print(f"{t:6} n={len(grp):3}  mw known={len(mws):3}  "
          f"min={stats[t]['mw_min']:.2f} max={stats[t]['mw_max']:.2f} "
          f"mean={stats[t]['mw_mean']:.2f}")

json.dump({"stats": stats}, open("stats2.json", "w"), indent=1)

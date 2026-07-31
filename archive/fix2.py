import json,re
AW={"C":12.011,"H":1.008,"O":15.999,"N":14.007,"S":32.06}
def mw(f):
    if not f: return None
    tot=0.0
    for el,ct in re.findall(r'([A-Z][a-z]?)(\d*)',f):
        if not el: continue
        tot+=AW.get(el,0)*(int(ct) if ct else 1)
    return round(tot,2)

# PubChem-authoritative formula corrections (all CAS-resolved, IUPAC-confirmed)
fix={"Melonal":"C9H16O","Bourgeonal":"C13H18O","Calone":"C10H10O3","Helional":"C11H12O3","Ebanol":"C14H24O","Cedramber":"C16H28O"}

rows=json.load(open("rows2.json"))
changed=[]
for r in rows:
    if r["name"] in fix:
        old=(r["formula"],r["mw"])
        r["formula"]=fix[r["name"]]
        r["mw"]=mw(fix[r["name"]])
        changed.append((r["name"],old,(r["formula"],r["mw"])))

# re-sort within each note tier by mw (None last), then recompute stats
order={"top":0,"heart":1,"base":2}
rows.sort(key=lambda r:(order[r["note"]], r["mw"] if r["mw"] is not None else 9e9, r["name"]))

stats={}
for t in ("top","heart","base"):
    ms=[r["mw"] for r in rows if r["note"]==t and r["mw"] is not None]
    stats[t]={"n":sum(1 for r in rows if r["note"]==t),
              "mw_min":min(ms),"mw_max":max(ms),"mw_mean":sum(ms)/len(ms)}

json.dump(rows, open("rows2.json","w"), ensure_ascii=False, indent=0)
json.dump({"stats":stats}, open("stats2.json","w"), indent=0)
print("corrected formulas/MW:")
for c in changed: print("  ",c)
print("\nnew tier means:", {t:round(stats[t]['mw_mean'],1) for t in stats})

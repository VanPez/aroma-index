import json, math, statistics
rows=json.load(open("rows2.json"))
PAIRS=[[i,r["cid"]] for i,r in enumerate(rows) if r.get("cid")]
strictvp=[12425.6104,None,169.31894,79.9932,746.6032,199.983,206.6491,633.2795,None,None,86.6593,None,None,253.3118,21.198198,None,None,None,8.492611,None,None,None,3.853006,4.386294,None,1.33322,23.597994,3.613026,None,None,266.644,None,5.639521,2.66644,2.946416,None,None,None,None,None,None,None,None,None,None,2.533118,None,7.199388,None,14.798742,None,None,None,None,None,0.043463,1.066576,None,None,None,None,0.015732,None,0.001387,None,None,None,None,None,None,None,None,0.029864,None,None,None,None,None,None,0.010399,None,None,None,None,None,None,None,None,None,0.07266,None,None,None,None,None]
exp={PAIRS[k][0]: strictvp[k] for k in range(len(PAIRS))}
R=8.314
def dHvap(Tb): return Tb*(36.6+8.31*math.log(Tb))
def vp_at(T,Tb): return 101325.0*math.exp(-(dHvap(Tb)/R)*(1.0/T-1.0/Tb))
def fmt(pa):
    if pa is None: return ""
    if pa>=1000: return f"{pa/1000:.2f} kPa"
    if pa>=1: return f"{pa:.1f} Pa"
    if pa>=1e-3: return f"{pa*1000:.1f} mPa"
    return f"{pa:.1e} Pa"

nexp=nest=0
for i,r in enumerate(rows):
    est=None
    if r.get("bp_c") is not None:
        est=vp_at(298.15, r["bp_c"]+273.15)
    e=exp.get(i)
    if e is not None:
        r["vp_pa"]=e; r["vp_src"]="exp"; nexp+=1
    elif est is not None:
        r["vp_pa"]=est; r["vp_src"]="est"; nest+=1
    else:
        r["vp_pa"]=None; r["vp_src"]=None
    r["vp_disp"]=fmt(r.get("vp_pa"))

json.dump(rows, open("rows2.json","w"), ensure_ascii=False, indent=0)
print(f"VP: experimental={nexp}, estimated={nest}, blank={sum(1 for r in rows if r.get('vp_pa') is None and r.get('cid'))}, captives(no cid)={sum(1 for r in rows if not r.get('cid'))}")
print("BP: experimental={}, est(from reduced)={}, none={}".format(
    sum(1 for r in rows if r.get('bp_c') is not None and not r.get('bp_est')),
    sum(1 for r in rows if r.get('bp_est')),
    sum(1 for r in rows if r.get('bp_c') is None)))
print("\n=== tier gradient ===")
for t in ("top","heart","base"):
    vs=[r['vp_pa'] for r in rows if r['note']==t and r.get('vp_pa') is not None]
    print(f"  {t}: n={len(vs)} median={fmt(statistics.median(vs))}  ({fmt(min(vs))} .. {fmt(max(vs))})")
print("\n=== spot checks ===")
for nm in ["Ethyl acetate","Limonene","Linalool","Vanillin","Coumarin","Eugenol","2-Phenylethanol","Muscone","Galaxolide (HHCB)"]:
    r=next((x for x in rows if x['name']==nm),None)
    if r: print(f"  {nm:22} BP={str(r.get('bp_c'))+('~' if r.get('bp_est') else ''):8} VP={r['vp_disp']:10} [{r.get('vp_src')}]")

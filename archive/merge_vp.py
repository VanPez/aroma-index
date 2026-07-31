import json, math, statistics
rows=json.load(open("rows2.json"))
PAIRS=[[i,r["cid"]] for i,r in enumerate(rows) if r.get("cid")]
vp=[9732.506,None,169.31894,79.9932,533.288,199.983,206.6491,1333.22,None,None,26.6644,666.61,666.61,253.3118,21.198198,None,None,None,133.322,None,11.57235,None,3.853006,4.386294,5.45,133.322,133.322,3.613026,None,None,266.644,None,666.61,2.66644,2.946416,2.66644,None,None,None,None,None,None,None,None,None,2.533118,None,7.199388,2.66644,14.798742,None,None,None,None,None,0.043463,1.066576,0.733271,None,1.33322,None,133.322,None,0.001387,None,None,None,None,None,None,None,None,0.029864,None,None,None,None,None,None,0.010399,None,None,None,None,None,None,None,None,None,0.07266,0.068261,None,None,None,None]
exp={PAIRS[k][0]: vp[k] for k in range(len(PAIRS))}

def fmt_vp(pa):
    if pa is None: return ""
    if pa>=1000: return f"{pa/1000:.2f} kPa"
    if pa>=1: return f"{pa:.1f} Pa"
    if pa>=1e-3: return f"{pa*1000:.1f} mPa"
    return f"{pa:.1e} Pa"

nexp=nest=0
for i,r in enumerate(rows):
    e=exp.get(i)
    if e is not None:
        r["vp_pa"]=e; r["vp_src"]="exp"; nexp+=1
    elif r.get("vp_pa") is not None:
        r["vp_src"]="est"; nest+=1
    else:
        r["vp_src"]=None
    r["vp_disp"]=fmt_vp(r.get("vp_pa"))

json.dump(rows, open("rows2.json","w"), ensure_ascii=False, indent=0)
print(f"VP: experimental={nexp}, estimated={nest}, blank={sum(1 for r in rows if r.get('vp_pa') is None and r.get('cid'))}")
print("\n=== tier gradient (hybrid) ===")
for t in ("top","heart","base"):
    vs=[r['vp_pa'] for r in rows if r['note']==t and r.get('vp_pa') is not None]
    print(f"  {t}: n={len(vs)} median={fmt_vp(statistics.median(vs))}  ({fmt_vp(min(vs))} .. {fmt_vp(max(vs))})")
print("\n=== spot checks (src) ===")
for nm in ["Ethyl acetate","Limonene","Linalool","Vanillin","Coumarin","Eugenol","Muscone","Galaxolide (HHCB)","Iso E Super"]:
    r=next((x for x in rows if x['name']==nm),None)
    if r: print(f"  {nm}: BP={r.get('bp_c')}{'~' if r.get('bp_est') else ''}  VP={r['vp_disp']} [{r.get('vp_src')}]")

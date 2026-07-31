import json, math

rows=json.load(open("rows2.json"))
PAIRS=[[i,r["cid"]] for i,r in enumerate(rows) if r.get("cid")]

bp=[77.1,156.5,178.9,171,142.2,177.1,177.8,156.2,None,None,203.9,228.5,206,176.5,198,185,209,None,215,253.5,220,175.5,249,248.5,234.5,263,213.5,256,223,230,225,182,219.5,225,253.9,266,285,None,None,241,None,None,270,275,134.5,258,68.5,267.5,242.5,220,238,263,276,None,216,93,216,265.5,289.5,299,272,285,136,285,281,281,297,None,None,277.5,285.5,None,323.5,None,None,None,None,286,None,300,None,None,None,None,324.5,None,None,None,None,None,4,None,None,None,None]
red={9:(120,100),37:(79,0.19),53:(110.5,0.2),87:(137,2),90:(187.5,16),91:(128,0.8),94:(140,1)}

assert len(bp)==len(PAIRS), (len(bp),len(PAIRS))
R=8.314
def dHvap(Tb):  # Kistiakowsky enthalpy of vaporization at normal boiling point, J/mol
    return Tb*(36.6+8.31*math.log(Tb))
def vp_at(T, Tb):  # Clausius-Clapeyron from (Tb,101325) to T
    return 101325.0*math.exp(-(dHvap(Tb)/R)*(1.0/T - 1.0/Tb))
def solve_Tb_from_reduced(t_c, p_mmHg):
    Tref=t_c+273.15; Pref=p_mmHg*133.322
    lo,hi=Tref+0.1, 1000.0
    for _ in range(80):
        mid=(lo+hi)/2
        pred=vp_at(Tref, mid)  # predicted P at Tref given normal boiling Tb=mid
        if pred>Pref: lo=mid   # too volatile -> Tb higher
        else: hi=mid
    return (lo+hi)/2

# map original index -> bp
idx_bp={PAIRS[k][0]: bp[k] for k in range(len(PAIRS))}

# outlier flagging: implausibly low atmospheric BP for heart/base
print("=== outlier check (atm BP < 60C) ===")
for i,r in enumerate(rows):
    b=idx_bp.get(i)
    if b is not None and b<60:
        print(f"  idx {i} {r['name']} ({r['note']}) bp={b}  -> likely parse error, will drop")

# apply: build Tb per molecule
def fmt_vp(pa):
    if pa is None: return ""
    if pa>=1000: return f"{pa/1000:.2f} kPa"
    if pa>=1: return f"{pa:.1f} Pa"
    if pa>=1e-3: return f"{pa*1000:.1f} mPa"
    return f"{pa:.1e} Pa"

filled=0; est_bp=0
for i,r in enumerate(rows):
    b=idx_bp.get(i)
    r["bp_c"]=None; r["bp_est"]=False; r["vp_pa"]=None
    # drop implausible atmospheric bp (parse errors)
    if b is not None and (b<60 and r["note"] in ("heart","base")):
        b=None
    if b is not None:
        Tb=b+273.15
        r["bp_c"]=round(b,1)
    elif i in red:
        Tb=solve_Tb_from_reduced(*red[i])
        r["bp_c"]=round(Tb-273.15,1); r["bp_est"]=True; est_bp+=1
    else:
        Tb=None
    if Tb:
        r["vp_pa"]=vp_at(298.15, Tb)
        r["vp_disp"]=fmt_vp(r["vp_pa"])
        filled+=1
    else:
        r["vp_disp"]=""

json.dump(rows, open("rows2.json","w"), ensure_ascii=False, indent=0)
print(f"\nVP filled: {filled}/99   (of which {est_bp} via reduced-pressure estimate)")
print("blank (no PubChem BP):", sum(1 for r in rows if r['vp_pa'] is None and r.get('cid')))
print("\n=== sanity: VP by tier (should decrease top->base) ===")
for t in ("top","heart","base"):
    vs=[r['vp_pa'] for r in rows if r['note']==t and r['vp_pa'] is not None]
    if vs:
        import statistics
        print(f"  {t}: n={len(vs)} median VP = {fmt_vp(statistics.median(vs))}  range {fmt_vp(min(vs))} .. {fmt_vp(max(vs))}")
print("\n=== spot checks ===")
for nm in ["Ethyl acetate","Limonene","Linalool","Vanillin","Coumarin","Muscone","Galaxolide (HHCB)"]:
    r=next((x for x in rows if x['name']==nm),None)
    if r: print(f"  {nm}: BP={r['bp_c']}{'~' if r['bp_est'] else ''}C  VP@25C={r['vp_disp']}")

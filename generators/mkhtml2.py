# -*- coding: utf-8 -*-
import json, html
rows=json.load(open("rows2.json")); stats=json.load(open("stats2.json"))["stats"]
N=len(rows)
TIER={"top":("TOP","#0f8f7f","rgba(15,143,127,.10)","most volatile — first impression, minutes"),
      "heart":("HEART","#b0446e","rgba(176,68,110,.10)","the core — floral & spice, ~1h"),
      "base":("BASE","#9a6a14","rgba(154,106,20,.10)","least volatile — the drydown, hours")}
def esc(s): return html.escape(s or "")

def _median(v):
    v=sorted(v); n=len(v)
    return None if not n else (v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2)

def _fmt_vp(v):
    if v is None: return "—"
    if v>=1000: return f"{v/1000:.1f} kPa"
    if v>=1:    return f"{v:.0f} Pa"
    return f"{v*1000:.0f} mPa"

# The headline "median X → Y → Z" must come from the data, not be typed in.
# It was hardcoded and went stale the moment the vapour-pressure estimator was
# recalibrated — the fourth derived value in this project to drift that way.
vpmed = " → ".join(_fmt_vp(_median([r['vp_pa'] for r in rows
                                    if r['note']==t and r.get('vp_pa') is not None]))
                   for t in ("top","heart","base"))
def cell_mw(r): return f"{r['mw']:.2f}" if r['mw'] is not None else '<span class="verify">—</span>'
def cell_bp(r):
    b=r.get("bp_c")
    if b is None: return '<span class="verify">—</span>'
    pre='~' if r.get("bp_est") else ''
    return f'{pre}{b:.0f}'
def cell_vp(r):
    v=r.get("vp_disp"); src=r.get("vp_src")
    if not v: return '<span class="verify">—</span>'
    if src=='est':
        return f'<span class="vpest" title="estimated from boiling point (Clausius–Clapeyron)">{v}</span>'
    return f'<span title="experimental · PubChem">{v}</span>'
def rows_for(t):
    o=[]
    for r in [x for x in rows if x["note"]==t]:
        cas=esc(r["cas"]) if r["cas"] else '<span class="verify">verify</span>'
        blob=" ".join(str(x) for x in [r['name'],r['cas'],r['formula'],r['family'],r['descriptors']] if x).lower()
        cid=r.get("cid"); ikey=esc(r.get("inchikey") or ""); smi=esc(r.get("smiles") or "")
        if cid:
            nm=f'<td class="nm has3d" data-cid="{cid}" data-name="{esc(r["name"])}" data-ikey="{ikey}" data-smiles="{smi}" title="Show 3D structure"><span class="cav">◈</span>{esc(r["name"])}</td>'
        else:
            nm=f'<td class="nm">{esc(r["name"])}</td>'
        o.append(f"""<tr data-s="{esc(blob)}">{nm}<td class="mono">{cas}</td>
      <td class="mono">{esc(r['formula']) or '—'}</td><td class="mono num">{cell_mw(r)}</td>
      <td class="mono num">{cell_bp(r)}</td><td class="mono vp">{cell_vp(r)}</td>
      <td>{esc(r['family'])}</td><td class="desc">{esc(r['descriptors'])}</td></tr>""")
    return "\n".join(o)
sec=""
for t in ("top","heart","base"):
    label,color,bg,blurb=TIER[t]; s=stats[t]
    sec+=f"""<div class="tier" style="--tc:{color};--tbg:{bg}"><div class="tier-head">
    <span class="pill">{label} NOTES</span>
    <span class="tier-meta">{s['n']} molecules · MW {s['mw_min']:.0f}–{s['mw_max']:.0f} (avg {s['mw_mean']:.0f}) · {blurb}</span></div>
    <div class="scroll"><table><thead><tr><th>Molecule</th><th>CAS</th><th>Formula</th><th>MW</th><th title="normal boiling point, °C (PubChem; ~ = estimated)">BP °C</th><th title="vapor pressure at 25°C (experimental where available, else estimated from BP)">VP · 25°C</th><th>Family</th><th>Odor descriptors · source</th></tr></thead>
    <tbody>{rows_for(t)}</tbody></table></div></div>"""
H=f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GenesisL1 — Aroma Molecule Index (v3 MolNFT prototype)</title><style>
 :root{{--paper:#f5f7f9;--card:#fff;--ink:#07111d;--mut:#687383;--faint:#718196;--line:#dce4ee;--line-strong:rgba(29,52,78,.3);
   --blue:#245cff;--blue-deep:#1647d9;--blue-pale:#eef3ff;--amber:#9a6a14;--amber-pale:#fdf6e9;
   --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
   --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;--shadow:0 18px 50px rgba(28,60,98,.067)}}
 *{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans);-webkit-font-smoothing:antialiased}}
 .topbar{{position:sticky;top:0;z-index:5;min-height:72px;border-bottom:1px solid rgba(7,17,29,.1);background:rgba(255,255,255,.94);backdrop-filter:blur(6px)}}
 .topbar-in{{max-width:1280px;margin:0 auto;padding:10px 28px;min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}
 .brand{{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}}
 .glyph{{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid var(--line-strong);overflow:hidden}}
 .glyph img{{width:23px;height:23px}} .wordmark b{{font-size:16px;font-weight:700;letter-spacing:-.01em;display:block}}
 .wordmark span{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}}
 .nav{{display:flex;gap:4px;margin-left:6px}} .nav a{{font:600 12px var(--mono);text-decoration:none;color:var(--mut);padding:6px 12px;border-radius:999px;letter-spacing:.02em}}
 .nav a:hover{{background:rgba(7,17,29,.05);color:var(--ink)}} .nav a.active{{background:var(--blue);color:#fff}}
 .badge{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border:1px solid var(--line-strong);color:var(--mut);background:#fff}}
 .badge.proto{{color:var(--amber);border-color:rgba(154,106,20,.45);background:var(--amber-pale)}}
 .wrap{{max-width:1280px;margin:0 auto;padding:0 28px 64px}} .hero{{margin:26px 0}}
 .lab{{display:flex;align-items:center;gap:10px;color:var(--mut);font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.14em}}
 .dash{{width:18px;height:2px;background:var(--blue)}} h1{{font-size:34px;letter-spacing:-.02em;margin:10px 0 6px;font-weight:700}}
 .sub{{color:var(--mut);font-size:15px;max-width:82ch}}
 .stats{{display:grid;grid-template-columns:repeat(3,1fr);margin:22px 0;background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow)}}
 .stat{{padding:15px 18px}}.stat+.stat{{border-left:1px solid var(--line)}}
 .stat .k{{color:var(--mut);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em}}
 .stat .v{{font-family:var(--mono);font-size:20px;font-weight:500;margin-top:5px}}
 .note{{background:var(--blue-pale);border:1px solid rgba(36,92,255,.25);padding:12px 16px;font-size:13.5px;color:#243a63;margin-bottom:24px}}
 .search{{position:sticky;top:72px;z-index:4;display:flex;align-items:center;gap:12px;background:var(--paper);padding:12px 0 14px;margin-bottom:8px;border-bottom:1px solid var(--line)}}
 .search .ico{{position:absolute;left:14px;pointer-events:none;color:var(--faint);font-size:14px}} .search .field{{position:relative;flex:1;min-width:0;display:flex;align-items:center}}
 .search input{{flex:1;min-width:0;font:14px var(--sans);padding:11px 14px 11px 36px;border:1px solid var(--line-strong);background:#fff;color:var(--ink);border-radius:9px;outline:none}}
 .search input:focus{{border-color:var(--blue);box-shadow:0 0 0 3px var(--blue-pale)}}
 .search .count{{font-family:var(--mono);font-size:11px;color:var(--mut);white-space:nowrap;letter-spacing:.04em}}
 .nores{{display:none;padding:26px 18px;text-align:center;color:var(--mut);font-family:var(--mono);font-size:13px;background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow)}}
 .tier{{background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow);margin-bottom:20px;overflow:hidden;border-top:3px solid var(--tc)}}
 .tier-head{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap;background:var(--tbg)}}
 .pill{{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.08em;color:var(--tc);border:1px solid var(--tc);padding:3px 10px;border-radius:999px}}
 .tier-meta{{color:var(--mut);font-family:var(--mono);font-size:11px}} .scroll{{overflow-x:auto}}
 table{{width:100%;border-collapse:collapse;min-width:960px}} th,td{{text-align:left;padding:9px 18px;font-size:13.5px;vertical-align:top}}
 th{{color:var(--mut);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.09em;font-weight:500;border-bottom:1px solid var(--line)}}
 th:nth-child(4),th:nth-child(5){{text-align:right}} tbody tr{{border-top:1px solid var(--line)}} tbody tr:first-child{{border-top:0}} tbody tr:hover{{background:#f5f8fc}}
 td.vp{{white-space:nowrap;font-size:12.5px}} .vpest{{color:var(--faint);font-style:italic}}
 td.nm{{font-weight:600}} .mono{{font-family:var(--mono)}} .num{{text-align:right}} td.desc{{color:#42506a}}
 td.has3d{{cursor:pointer}} td.has3d .cav{{color:var(--tc,#245cff);font-size:11px;margin-right:7px;opacity:.55;transition:opacity .12s,transform .12s;display:inline-block}}
 td.has3d:hover .cav{{opacity:1}} tr.open td.has3d .cav{{opacity:1;transform:rotate(45deg)}}
 tr.vrow>td{{padding:0;background:linear-gradient(180deg,#fbfdff,#f3f7fc);border-top:0}}
 .v3d-wrap{{display:flex;gap:18px;align-items:stretch;padding:16px 18px;flex-wrap:wrap}}
 .mol3d{{position:relative;width:340px;height:300px;min-width:280px;background:#fff;border:1px solid var(--line-strong);border-radius:10px;overflow:hidden}}
 .mol3d canvas{{border-radius:10px}} .mol3d .load{{position:absolute;inset:0;display:grid;place-items:center;color:var(--mut);font-family:var(--mono);font-size:12px}}
 .v3d-meta{{flex:1;min-width:220px;display:flex;flex-direction:column;gap:8px;font-size:13px}}
 .v3d-meta h4{{margin:2px 0 4px;font-size:15px}} .v3d-meta .row{{display:flex;gap:8px;line-height:1.5}}
 .v3d-meta .kk{{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--mut);min-width:74px;padding-top:2px}}
 .v3d-meta .vv{{font-family:var(--mono);font-size:12px;color:var(--ink);word-break:break-all}} .v3d-meta a{{color:var(--blue);text-decoration:none}}
 .v3d-meta .hint{{color:var(--faint);font-size:11.5px;margin-top:2px}} .v3d-meta .pc{{align-self:flex-start;font-family:var(--mono);font-size:11px;border:1px solid var(--line-strong);padding:6px 11px;border-radius:7px;color:var(--blue);text-decoration:none;margin-top:2px}}
 .v3d-meta .pc:hover{{background:var(--blue-pale)}}
 .verify{{font-family:var(--mono);font-size:10px;color:var(--amber);background:var(--amber-pale);border:1px solid rgba(154,106,20,.35);padding:1px 6px}}
 .foot{{color:var(--mut);font-size:12.5px;margin-top:26px;line-height:1.8;border-top:1px solid var(--line);padding-top:16px}} .foot a{{color:var(--blue);text-decoration:none}}
 @media(max-width:640px){{.stats{{grid-template-columns:1fr}}.stat+.stat{{border-left:0;border-top:1px solid var(--line)}}.topbar-in,.wrap{{padding-left:16px;padding-right:16px}}h1{{font-size:26px}}.search{{position:static;flex-wrap:wrap}}}}
__RESOLVER_CSS__
</style></head><body>
<header class="topbar"><div class="topbar-in">
  <a class="brand" href="https://genesisl1.com" target="_blank" rel="noopener">
    <span class="glyph"><img src="https://genesisl1.com/logo.svg" alt="GenesisL1" onerror="this.parentNode.textContent='L1';this.parentNode.style.font='700 12px var(--mono)'"></span>
    <span class="wordmark"><b>GenesisL1</b><span>Aroma Molecule Index</span></span></a>
  <nav class="nav"><a href="./" class="active" aria-current="page">Molecule index</a><a href="./scent-map.html">Scent map</a><a href="./smiles-3d.html">SMILES &rarr; 3D</a></nav>
  <span class="badge proto">◐ v3 prototype · {N} molecules · MolNFT resolver</span></div></header>
<div class="wrap"><div class="hero">
  <div class="lab"><span class="dash"></span> DeSci · MOLNFT domain concept</div>
  <h1>The common aroma molecules, by volatility</h1>
  <div class="sub">A curated, open index of widely-used fragrance chemicals — grouped into <b>top</b>, <b>heart</b> and <b>base</b> notes by how fast they evaporate. Smaller/lighter molecules flash off first (top); the largest linger for hours (base). Naturals are represented by their signature molecule (e.g. black pepper → rotundone, vetiver → khusimol). Proposed as a public-good extension of GenesisL1's <b>MOLNFT</b> molecular corpus. Each row shows boiling point and vapor pressure at 25°C — the physical measures of volatility behind the note tiers (they fall as you go down the list). <b>Click any molecule</b> for its interactive 3D structure and public-domain identifiers (PubChem CID · InChIKey · SMILES). The optional <b>MolNFT resolver</b> below can prepare mock IPFS/on-chain links or read an existing token directly from a GenesisL1 EVM JSON-RPC endpoint.</div></div>
  <div class="stats">
    <div class="stat"><div class="k">Molecules (v2)</div><div class="v">{N}</div></div>
    <div class="stat"><div class="k">Note tiers</div><div class="v">top · heart · base</div></div>
    <div class="stat"><div class="k">Avg MW rises with tier</div><div class="v">{stats['top']['mw_mean']:.0f} → {stats['heart']['mw_mean']:.0f} → {stats['base']['mw_mean']:.0f}</div></div></div>
  <div class="note"><b>The volatility principle, visible in the data:</b> vapor pressure (the <b>VP · 25°C</b> column) falls steeply from top to base notes — median {vpmed} — while boiling point and molecular weight climb. Vapor pressure is the true physical driver of the perfumer's pyramid; MW is a convenient proxy for it.</div>
__RESOLVER_SECTION__
  <div class="search"><span class="field"><span class="ico">⌕</span><input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="Search molecule, family, or odour — e.g. rose, woody, citrus, C10H16…"></span><span class="count" id="count"></span></div>
  {sec}
  <div class="nores" id="nores">No molecules match — try a broader term (e.g. <b>floral</b>, <b>woody</b>, <b>musk</b>).</div>
  <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
  <script>
  (function(){{
    var q=document.getElementById('q'),count=document.getElementById('count'),nores=document.getElementById('nores');
    var molRows=[].slice.call(document.querySelectorAll('tbody tr[data-s]'));
    var tiers=[].slice.call(document.querySelectorAll('.tier'));
    var total=molRows.length;
    // open 3D panels: each entry links a molecule row to its viewer row for visibility sync
    var open=[];
    function apply(){{
      var terms=(q.value||'').toLowerCase().replace(/\\s+/g,' ').trim().split(' ').filter(Boolean);
      var shown=0;
      molRows.forEach(function(tr){{
        var hay=tr.getAttribute('data-s')||'';
        var ok=terms.every(function(t){{return hay.indexOf(t)>-1;}});
        tr.style.display=ok?'':'none'; if(ok)shown++;
      }});
      open.forEach(function(o){{ o.vrow.style.display=o.mol.style.display; }});
      tiers.forEach(function(t){{
        var any=[].slice.call(t.querySelectorAll('tbody tr[data-s]')).some(function(tr){{return tr.style.display!=='none';}});
        t.style.display=any?'':'none';
      }});
      nores.style.display=shown?'none':'block';
      count.textContent=q.value?shown+' of '+total+' shown':total+' molecules';
    }}
    q.addEventListener('input',apply); apply();

    // ---- 3D structure viewer (lazy: fetches the PubChem conformer by CID on click) ----
    var seq=0;
    function esc(s){{return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
    function close(tr){{
      var v=tr._vrow; if(v){{ v.parentNode.removeChild(v); tr._vrow=null; tr.classList.remove('open');
        open=open.filter(function(o){{return o.mol!==tr;}}); }}
    }}
    function openViewer(td){{
      var tr=td.parentNode, cid=td.getAttribute('data-cid');
      if(tr._vrow){{ close(tr); return; }}
      var name=td.getAttribute('data-name'), ikey=td.getAttribute('data-ikey'), smi=td.getAttribute('data-smiles');
      var id='v3d'+(++seq);
      var vrow=document.createElement('tr'); vrow.className='vrow';
      var td2=document.createElement('td'); td2.colSpan=8;
      var pc='https://pubchem.ncbi.nlm.nih.gov/compound/'+cid;
      td2.innerHTML='<div class="v3d-wrap"><div class="mol3d" id="'+id+'"><div class="load">rendering 3D…</div></div>'+
        '<div class="v3d-meta"><h4>'+esc(name)+'</h4>'+
        '<div class="row"><span class="kk">PubChem CID</span><span class="vv">'+cid+'</span></div>'+
        '<div class="row"><span class="kk">InChIKey</span><span class="vv">'+esc(ikey)+'</span></div>'+
        '<div class="row"><span class="kk">SMILES</span><span class="vv">'+esc(smi)+'</span></div>'+
        '<a class="pc" href="'+pc+'" target="_blank" rel="noopener">View on PubChem →</a>'+
        '<button class="resolver-btn secondary resolver-pick" type="button" data-cid="'+cid+'" data-name="'+encodeURIComponent(name)+'">Prepare MolNFT link</button>'+
        '<div class="hint">Drag to rotate · scroll to zoom. 3D conformer &amp; identifiers from PubChem (public domain).</div>'+
        '</div></div>';
      vrow.appendChild(td2);
      tr.parentNode.insertBefore(vrow, tr.nextSibling);
      tr._vrow=vrow; tr.classList.add('open'); open.push({{mol:tr,vrow:vrow}});
      var host=document.getElementById(id);
      try{{
        var viewer=$3Dmol.createViewer(host,{{backgroundColor:'white'}});
        $3Dmol.download('cid:'+cid, viewer, {{}}, function(){{
          var el=host.querySelector('.load'); if(el) el.remove();
          viewer.setStyle({{}},{{stick:{{radius:0.13}},sphere:{{scale:0.27}}}});
          viewer.zoomTo(); viewer.render(); viewer.spin('y',0.4);
        }});
      }}catch(e){{ var el=host.querySelector('.load'); if(el) el.textContent='3D unavailable'; }}
    }}
    document.addEventListener('click',function(e){{
      var td=e.target.closest && e.target.closest('td.has3d');
      if(td) openViewer(td);
    }});
  }})();
  </script>
  <script src="https://cdn.jsdelivr.net/npm/ethers@6.13.5/dist/ethers.umd.min.js"></script>
__RESOLVER_JS__
  <div class="foot"><b>Prototype disclaimer:</b> hand-curated v2 proof-of-concept from public perfumery knowledge. Structural identifiers (PubChem CID · InChIKey · SMILES) and 3D conformers are resolved from <a href="https://pubchem.ncbi.nlm.nih.gov" target="_blank" rel="noopener">PubChem</a> (public domain) by CAS; note-tier assignments remain hand-curated and should be verified against open sources (<a href="https://pyrfume.org" target="_blank" rel="noopener">Pyrfume</a>, Leffingwell/Good-Scents) before any on-chain minting. Entries tagged <span class="verify">verify</span> are proprietary trade-name captives with no public structure. Boiling points and vapor pressures (@25°C) are experimental values from PubChem where available; a <span class="vpest">grey italic</span> vapor pressure is <b>estimated</b> from the boiling point (Clausius–Clapeyron with a Kistiakowsky enthalpy) and is indicative of the gradient only — absolute values for hydrogen-bonding and solid compounds can be off by an order of magnitude. A "~" boiling point is extrapolated from a reduced-pressure measurement. Proprietary "captive" molecules held by houses are excluded; this indexes the shared public palette. Curation by <b>vanpe</b> — independent GenesisL1 validator — for the community. The <b>MolNFT resolver</b> (framework contributed by <b>Joe</b>) performs read-only JSON-RPC calls and treats generated mock links as placeholders; RPC endpoints, contract addresses, token IDs and IPFS CIDs must be independently verified. Automatic payload decoding is capped at 12 MB to reduce browser lock-ups. Not affiliated with IFRA. Not financial or formulation advice.</div>
</div></body></html>"""
# --- fold in Joe's MolNFT resolver framework (CSS / section / JS extracted verbatim) ---
res_css=open("res_css.txt").read()
res_section=open("res_section.txt").read()
res_js=open("res_js.txt").read()
for token,chunk in (("__RESOLVER_CSS__",res_css),("__RESOLVER_SECTION__",res_section),("__RESOLVER_JS__",res_js)):
    assert token in H, "missing placeholder "+token
    H=H.replace(token,chunk)
open("aroma-index.html","w").write(H)
print("wrote aroma-index.html", N, "molecules; resolver folded in")

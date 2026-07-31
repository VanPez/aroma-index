# -*- coding: utf-8 -*-
import json
d=json.load(open("scentmap.json"))

# 9 odour groups. Colour is a soft guide (exact family in tooltip/table); at 9
# groups not every pair is CVD-separable, so identity is carried by hover +
# click-to-isolate + the table, not colour alone.
GROUPS=[
 ["Fresh & Fruity","#f2b705"],   # warm yellow / citrus-fruit
 ["Green","#7cb518"],            # lime
 ["Woody","#5f7a24"],            # dark olive green
 ["Floral","#f4a9c8"],           # pale rose
 ["Amber & Balsamic","#9046c0"], # purple (warm end was crowded; distinct from musk blue)
 ["Sweet & Gourmand","#bf8a4a"], # caramel / tan
 ["Spicy & Herbal","#e02b1d"],   # fire red
 ["Musk","#2f6fd0"],             # blue
 ["Animalic","#1c1c1c"],         # black
]
for p in d["points"]:
    p["grp"]=p["cls"]

payload={"points":d["points"],"groups":GROUPS}

TMPL=r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GenesisL1 — Scent Map</title><style>
 :root{--paper:#f5f7f9;--card:#fff;--ink:#07111d;--mut:#687383;--faint:#718196;--line:#dce4ee;--line-strong:rgba(29,52,78,.3);
   --blue:#245cff;--blue-pale:#eef3ff;--amber:#9a6a14;--amber-pale:#fdf6e9;
   --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
   --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;--shadow:0 18px 50px rgba(28,60,98,.067)}
 *{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans);-webkit-font-smoothing:antialiased}
 .topbar{position:sticky;top:0;z-index:5;min-height:72px;border-bottom:1px solid rgba(7,17,29,.1);background:rgba(255,255,255,.94);backdrop-filter:blur(6px)}
 .topbar-in{max-width:1280px;margin:0 auto;padding:10px 28px;min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
 .brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}
 .glyph{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid var(--line-strong);overflow:hidden}
 .glyph img{width:23px;height:23px} .wordmark b{font-size:16px;font-weight:700;letter-spacing:-.01em;display:block}
 .wordmark span{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}
 .badge{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border:1px solid rgba(154,106,20,.45);color:var(--amber);background:var(--amber-pale)}
 .wrap{max-width:1280px;margin:0 auto;padding:0 28px 64px} .hero{margin:24px 0 14px}
 .lab{display:flex;align-items:center;gap:10px;color:var(--mut);font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.14em}
 .dash{width:18px;height:2px;background:var(--blue)} h1{font-size:32px;letter-spacing:-.02em;margin:10px 0 6px;font-weight:700}
 .sub{color:var(--mut);font-size:14.5px;max-width:90ch}
 .note{background:var(--blue-pale);border:1px solid rgba(36,92,255,.25);padding:11px 15px;font-size:13px;color:#243a63;margin:16px 0 8px}
 .legend{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;align-items:center}
 .chip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line-strong);background:#fff;padding:5px 11px 5px 9px;border-radius:999px;font-size:12.5px;cursor:pointer;user-select:none;transition:opacity .12s,box-shadow .12s}
 .chip .dot{width:11px;height:11px;border-radius:50%;flex:0 0 auto} .chip .n{font-family:var(--mono);font-size:10px;color:var(--mut)}
 .chip.off{opacity:.32} .chip:hover{box-shadow:0 2px 8px rgba(28,60,98,.12)}
 .chip.reset{color:var(--mut);font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
 .nav{display:flex;gap:4px;margin-left:6px}
 .nav a{font:600 12px var(--mono);text-decoration:none;color:var(--mut);padding:6px 12px;border-radius:999px;letter-spacing:.02em}
 .nav a:hover{background:rgba(7,17,29,.05);color:var(--ink)} .nav a.active{background:var(--blue);color:#fff}
 .maps{display:block;max-width:840px;margin:10px auto 0}
 .panel{background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow);border-top:3px solid var(--blue);overflow:hidden}
 .panel-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;padding:13px 16px;border-bottom:1px solid var(--line);flex-wrap:wrap}
 .panel-head h3{margin:0;font-size:15px} .panel-head .why{color:var(--mut);font-family:var(--mono);font-size:10.5px;letter-spacing:.02em}
 .plot{width:100%;display:block;aspect-ratio:1/1;background:linear-gradient(180deg,#fdfefe,#f4f8fc);touch-action:none}
 .plot circle{cursor:pointer;transition:opacity .12s}
 .plot circle.dim{opacity:.09}
 .tip{position:fixed;z-index:20;pointer-events:none;background:#07111d;color:#eaf1ff;border-radius:8px;padding:9px 11px;font-size:12px;max-width:280px;box-shadow:0 10px 30px rgba(0,0,0,.28);opacity:0;transform:translateY(4px);transition:opacity .1s}
 .tip.show{opacity:1;transform:none} .tip b{font-size:12.5px} .tip .fam{font-family:var(--mono);font-size:10px;color:#9db6e8;text-transform:uppercase;letter-spacing:.06em;margin:2px 0 5px}
 .tip .d{color:#c5d3ee;font-size:11.5px;line-height:1.5} .tip .tier{font-family:var(--mono);font-size:10px;color:#8ea6d6;margin-top:5px}
 .tools{display:flex;gap:8px;align-items:center;margin:16px 0 0;flex-wrap:wrap} .tools button{font:600 11px var(--mono);border:1px solid var(--line-strong);background:#fff;color:var(--blue);padding:7px 12px;border-radius:7px;cursor:pointer}
 .tools button:hover{background:var(--blue-pale)} .tools .hint{color:var(--faint);font-size:11.5px}
 table{width:100%;border-collapse:collapse;margin-top:12px;display:none} table.show{display:table}
 th,td{text-align:left;padding:7px 12px;font-size:12.5px;border-top:1px solid var(--line);vertical-align:top}
 th{color:var(--mut);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.08em;border-top:0}
 td.g{font-family:var(--mono);font-size:11px} .swatch{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
 .foot{color:var(--mut);font-size:12px;margin-top:26px;line-height:1.75;border-top:1px solid var(--line);padding-top:14px}
 @media(max-width:820px){.maps{grid-template-columns:1fr}.topbar-in,.wrap{padding-left:16px;padding-right:16px}h1{font-size:25px}}
</style></head><body>
<header class="topbar"><div class="topbar-in">
  <a class="brand" href="https://genesisl1.com" target="_blank" rel="noopener">
    <span class="glyph"><img src="https://genesisl1.com/logo.svg" alt="GenesisL1" onerror="this.parentNode.textContent='L1';this.parentNode.style.font='700 12px var(--mono)'"></span>
    <span class="wordmark"><b>GenesisL1</b><span>Aroma Molecule Index</span></span></a>
  <nav class="nav"><a href="./">Molecule index</a><a href="./scent-map.html" class="active" aria-current="page">Scent map</a><a href="./smiles-3d.html">SMILES &rarr; 3D</a></nav>
  <span class="badge">&#9680; experiment &middot; a map of smell &middot; 99 molecules</span></div></header>
<div class="wrap"><div class="hero">
  <div class="lab"><span class="dash"></span> DeSci &middot; a map of smell</div>
  <h1>The aroma molecules, arranged by how they smell</h1>
  <div class="sub">Every molecule from the index is placed so that <b>things that smell alike sit close together</b> — a small realisation of Luca Turin &amp; David MacKay's idea of &ldquo;unfolding a map of smell&rdquo; from molecules described by odour words. Each dot is built purely from its odour descriptors (citrus, rosy, woody&hellip;), then projected to 2D with UMAP.</div>
  <div class="note"><b>How to read it:</b> nearby dots share odour words, so families settle into neighbourhoods. The axes have no units &mdash; only <i>who sits near whom</i> is meaningful. Colour is a broad odour family (a soft guide); <b>hover any dot</b> for its exact family + descriptors, and <b>click a legend chip</b> to isolate one family.</div>
  <div class="legend" id="legend"></div>
</div>
  <div class="maps">
    <div class="panel"><div class="panel-head"><h3>Scent map</h3><span class="why">UMAP &middot; cosine &middot; nearby = smells alike</span></div><svg class="plot" id="plot-umap" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet"></svg></div>
  </div>
  <div class="tools"><button id="tableBtn" type="button">Show data table</button><span class="hint">99 molecules &middot; positions from odour descriptors only &middot; colour = broad family (hover for the exact one)</span></div>
  <table id="dataTable"><thead><tr><th>Molecule</th><th>Odour family (colour group)</th><th>Note</th><th>Descriptors</th></tr></thead><tbody id="tableBody"></tbody></table>
  <div class="foot"><b>Method &amp; caveats:</b> each molecule is a binary vector over its curated odour descriptors, projected to 2D with UMAP (cosine metric). With only 99 molecules and 2&ndash;4 hand-written descriptors each, this is an <b>illustrative</b> scent space, not a validated perceptual map &mdash; it would sharpen a lot at scale (Pyrfume / Leffingwell add thousands of molecules with odour labels). The 42 raw families are grouped into 9 odour classes. With this many colours not every pair is colourblind-distinguishable, so colour is a <b>soft guide</b> only &mdash; exact identity is always available by hovering, clicking a legend chip to isolate, or opening the table. A prototype extension of the GenesisL1 aroma index; homage to Turin &amp; MacKay, <i>The Secret of Scent</i>.</div>
</div>
<div class="tip" id="tip"></div>
<script>
var DATA=__DATA__;
(function(){
  var color={}, count={}; DATA.groups.forEach(function(g){color[g[0]]=g[1];count[g[0]]=0;});
  DATA.points.forEach(function(p){count[p.grp]=(count[p.grp]||0)+1;});
  var active=null; // active group filter (null = all)
  var tip=document.getElementById('tip');
  // legend
  var lg=document.getElementById('legend'); var html="";
  DATA.groups.forEach(function(g){
    html+='<span class="chip" data-g="'+g[0]+'"><span class="dot" style="background:'+g[1]+'"></span>'+g[0]+' <span class="n">'+count[g[0]]+'</span></span>';
  });
  html+='<span class="chip reset" id="resetChip">show all</span>';
  lg.innerHTML=html;
  var PAD=48, S=1000-2*PAD;
  function draw(id,key){
    var svg=document.getElementById(id); var s="";
    DATA.points.forEach(function(p,i){
      var x=PAD+p[key][0]*S, y=PAD+(1-p[key][1])*S;
      s+='<circle data-i="'+i+'" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="11" fill="'+color[p.grp]+'" fill-opacity="0.92" stroke="rgba(7,17,29,.38)" stroke-width="1"></circle>';
    });
    svg.innerHTML=s;
  }
  draw('plot-umap','umap');
  function applyFilter(){
    document.querySelectorAll('.plot circle').forEach(function(c){
      var p=DATA.points[+c.getAttribute('data-i')];
      c.classList.toggle('dim', active!==null && p.grp!==active);
    });
    document.querySelectorAll('.chip[data-g]').forEach(function(ch){
      ch.classList.toggle('off', active!==null && ch.getAttribute('data-g')!==active);
    });
  }
  lg.addEventListener('click',function(e){
    var ch=e.target.closest('.chip'); if(!ch)return;
    if(ch.id==='resetChip'){active=null;} else {var g=ch.getAttribute('data-g'); active=(active===g)?null:g;}
    applyFilter();
  });
  function showTip(evt,p){
    tip.innerHTML='<b>'+p.name+'</b><div class="fam">'+p.family+'  &middot;  '+p.grp+'</div><div class="d">'+p.desc+'</div><div class="tier">note tier: '+p.note+'</div>';
    tip.classList.add('show');
    var x=evt.clientX+14, y=evt.clientY+14;
    if(x>window.innerWidth-300)x=evt.clientX-290; if(y>window.innerHeight-120)y=evt.clientY-110;
    tip.style.left=x+'px'; tip.style.top=y+'px';
  }
  document.querySelectorAll('.plot').forEach(function(svg){
    svg.addEventListener('mouseover',function(e){var c=e.target.closest('circle');if(!c)return;var p=DATA.points[+c.getAttribute('data-i')];c.setAttribute('r','15');showTip(e,p);});
    svg.addEventListener('mousemove',function(e){var c=e.target.closest('circle');if(c&&tip.classList.contains('show')){var p=DATA.points[+c.getAttribute('data-i')];showTip(e,p);}});
    svg.addEventListener('mouseout',function(e){var c=e.target.closest('circle');if(c)c.setAttribute('r','11');tip.classList.remove('show');});
  });
  // table
  var tb=document.getElementById('tableBody'); var rows="";
  DATA.points.slice().sort(function(a,b){return a.grp<b.grp?-1:a.grp>b.grp?1:(a.name<b.name?-1:1);}).forEach(function(p){
    rows+='<tr><td>'+p.name+'</td><td class="g"><span class="swatch" style="background:'+color[p.grp]+'"></span>'+p.family+' &middot; '+p.grp+'</td><td class="g">'+p.note+'</td><td>'+p.desc+'</td></tr>';
  });
  tb.innerHTML=rows;
  document.getElementById('tableBtn').addEventListener('click',function(){
    var t=document.getElementById('dataTable'); var on=t.classList.toggle('show'); this.textContent=on?'Hide data table':'Show data table';
  });
})();
</script>
</body></html>"""

html=TMPL.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
open("scent-map.html","w").write(html)
print("wrote scent-map.html", len(payload["points"]), "points")

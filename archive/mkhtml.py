# -*- coding: utf-8 -*-
import json, html
rows=json.load(open("rows.json"))
stats=json.load(open("stats.json"))["stats"]
TIER={"top":("TOP","#0f8f7f","rgba(15,143,127,.10)","most volatile — first impression, minutes"),
      "heart":("HEART","#b0446e","rgba(176,68,110,.10)","the core — floral & spice, ~1h"),
      "base":("BASE","#9a6a14","rgba(154,106,20,.10)","least volatile — the drydown, hours"),}
def esc(s): return html.escape(s or "")

def rows_for(t):
    out=[]
    for r in [x for x in rows if x["note"]==t]:
        sm = f'<code>{esc(r["smiles"])}</code>' if r["smiles"] else '<span class="verify">verify</span>'
        out.append(f"""<tr>
      <td class="nm">{esc(r['name'])}</td>
      <td class="mono">{esc(r['cas'])}</td>
      <td class="mono">{esc(r['formula'])}</td>
      <td class="mono num">{r['mw']:.2f}</td>
      <td>{esc(r['family'])}</td>
      <td class="desc">{esc(r['descriptors'])}</td>
      <td class="sm">{sm}</td></tr>""")
    return "\n".join(out)

sections=""
for t in ("top","heart","base"):
    label,color,bg,blurb=TIER[t]
    s=stats[t]
    sections+=f"""
  <div class="tier" style="--tc:{color};--tbg:{bg}">
    <div class="tier-head">
      <span class="pill">{label} NOTES</span>
      <span class="tier-meta">{s['n']} molecules · MW {s['mw_min']:.0f}–{s['mw_max']:.0f} (avg {s['mw_mean']:.0f}) · {blurb}</span>
    </div>
    <div class="scroll"><table>
      <thead><tr><th>Molecule</th><th>CAS</th><th>Formula</th><th>MW</th><th>Family</th><th>Odor descriptors</th><th>SMILES</th></tr></thead>
      <tbody>
{rows_for(t)}
      </tbody></table></div>
  </div>"""

HTML=f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GenesisL1 — Aroma Molecule Index (v1 prototype)</title>
<style>
 :root{{--paper:#f5f7f9;--card:#fff;--ink:#07111d;--mut:#687383;--faint:#718196;
   --line:#dce4ee;--line-strong:rgba(29,52,78,.3);--blue:#245cff;--blue-deep:#1647d9;--blue-pale:#eef3ff;
   --amber:#9a6a14;--amber-pale:#fdf6e9;
   --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
   --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
   --shadow:0 18px 50px rgba(28,60,98,.067);}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans);-webkit-font-smoothing:antialiased}}
 .topbar{{position:sticky;top:0;z-index:5;min-height:72px;border-bottom:1px solid rgba(7,17,29,.1);background:rgba(255,255,255,.94);backdrop-filter:blur(6px)}}
 .topbar-in{{max-width:1280px;margin:0 auto;padding:10px 28px;min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}
 .brand{{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}}
 .glyph{{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid var(--line-strong);overflow:hidden}}
 .glyph img{{width:23px;height:23px}}
 .wordmark b{{font-size:16px;font-weight:700;letter-spacing:-.01em;display:block}}
 .wordmark span{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--mut);text-transform:uppercase}}
 .badge{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border:1px solid var(--line-strong);color:var(--mut);background:#fff}}
 .badge.proto{{color:var(--amber);border-color:rgba(154,106,20,.45);background:var(--amber-pale)}}
 .wrap{{max-width:1280px;margin:0 auto;padding:0 28px 64px}}
 .hero{{margin:26px 0}}
 .lab{{display:flex;align-items:center;gap:10px;color:var(--mut);font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.14em}}
 .dash{{width:18px;height:2px;background:var(--blue)}}
 h1{{font-size:34px;letter-spacing:-.02em;margin:10px 0 6px;font-weight:700}}
 .sub{{color:var(--mut);font-size:15px;max-width:80ch}}
 .stats{{display:grid;grid-template-columns:repeat(3,1fr);margin:22px 0;background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow)}}
 .stat{{padding:15px 18px}} .stat+.stat{{border-left:1px solid var(--line)}}
 .stat .k{{color:var(--mut);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.1em}}
 .stat .v{{font-family:var(--mono);font-size:20px;font-weight:500;margin-top:5px}}
 .note{{background:var(--blue-pale);border:1px solid rgba(36,92,255,.25);padding:12px 16px;font-size:13.5px;color:#243a63;margin-bottom:24px}}
 .tier{{background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow);margin-bottom:20px;overflow:hidden;border-top:3px solid var(--tc)}}
 .tier-head{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap;background:var(--tbg)}}
 .pill{{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.08em;color:var(--tc);border:1px solid var(--tc);padding:3px 10px;border-radius:999px}}
 .tier-meta{{color:var(--mut);font-family:var(--mono);font-size:11px}}
 .scroll{{overflow-x:auto}} table{{width:100%;border-collapse:collapse;min-width:820px}}
 th,td{{text-align:left;padding:10px 18px;font-size:13.5px;vertical-align:top}}
 th{{color:var(--mut);font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.09em;font-weight:500;border-bottom:1px solid var(--line)}}
 tbody tr{{border-top:1px solid var(--line)}} tbody tr:first-child{{border-top:0}} tbody tr:hover{{background:#f5f8fc}}
 td.nm{{font-weight:600}} .mono{{font-family:var(--mono)}} .num{{text-align:right}}
 th:nth-child(4){{text-align:right}}
 td.desc{{color:#3a4椅埋}} td.desc{{color:#42506a}}
 td.sm code{{font-family:var(--mono);font-size:11px;color:#42506a;word-break:break-all}}
 .verify{{font-family:var(--mono);font-size:10px;color:var(--amber);background:var(--amber-pale);border:1px solid rgba(154,106,20,.35);padding:1px 6px}}
 .foot{{color:var(--mut);font-size:12.5px;margin-top:26px;line-height:1.8;border-top:1px solid var(--line);padding-top:16px}}
 @media(max-width:640px){{.stats{{grid-template-columns:1fr}}.stat+.stat{{border-left:0;border-top:1px solid var(--line)}}.topbar-in,.wrap{{padding-left:16px;padding-right:16px}}h1{{font-size:26px}}}}
</style></head><body>
<header class="topbar"><div class="topbar-in">
  <a class="brand" href="https://genesisl1.com" target="_blank" rel="noopener">
    <span class="glyph"><img src="https://genesisl1.com/logo.svg" alt="GenesisL1" onerror="this.parentNode.textContent='L1';this.parentNode.style.font='700 12px var(--mono)'"></span>
    <span class="wordmark"><b>GenesisL1</b><span>Aroma Molecule Index</span></span>
  </a>
  <span class="badge proto">◐ v1 prototype · proof of concept</span>
</div></header>
<div class="wrap">
  <div class="hero">
    <div class="lab"><span class="dash"></span> DeSci · MOLNFT domain concept</div>
    <h1>The common aroma molecules, by volatility</h1>
    <div class="sub">A curated, open index of widely-used fragrance chemicals — organized into <b>top</b>, <b>heart</b> and <b>base</b> notes by how fast they evaporate. Smaller/lighter molecules flash off first (top); the largest linger for hours (base). Proposed as a public-good extension of GenesisL1's <b>MOLNFT</b> molecular corpus.</div>
  </div>
  <div class="stats">
    <div class="stat"><div class="k">Molecules (v1)</div><div class="v">{len(rows)}</div></div>
    <div class="stat"><div class="k">Note tiers</div><div class="v">top · heart · base</div></div>
    <div class="stat"><div class="k">Avg MW rises with tier</div><div class="v">{stats['top']['mw_mean']:.0f} → {stats['heart']['mw_mean']:.0f} → {stats['base']['mw_mean']:.0f}</div></div>
  </div>
  <div class="note"><b>The volatility principle, visible in the data:</b> average molecular weight climbs monotonically from top to base notes — the physical basis of the perfumer's pyramid. (Note: the true driver is <b>vapor pressure</b>; MW is a strong proxy. A production index would compute the tier from measured/estimated vapor pressure.)</div>
  {sections}
  <div class="foot">
    <b>Prototype disclaimer:</b> this is a hand-curated v1 proof-of-concept from public perfumery knowledge. All identifiers (CAS, SMILES) and note assignments must be verified against open sources — <a href="https://pubchem.ncbi.nlm.nih.gov" target="_blank" rel="noopener">PubChem</a> (public domain), <a href="https://pyrfume.org" target="_blank" rel="noopener">Pyrfume</a>, the Leffingwell/Good-Scents odor datasets — before any on-chain minting. Proprietary "captive" molecules held by fragrance houses are intentionally excluded; this indexes the shared public palette only.<br>
    Concept &amp; curation by <b>vanpe</b> — an independent GenesisL1 validator — for the community. Not affiliated with IFRA. Not financial or formulation advice.
  </div>
</div></body></html>"""
open("aroma-index.html","w").write(HTML)
print("wrote aroma-index.html", len(HTML), "bytes")

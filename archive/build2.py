# -*- coding: utf-8 -*-
# GenesisL1 Aroma Molecule Index — v2 PROTOTYPE (~100 common aroma molecules)
# Includes all of Ivan's INTERESTING + LOVE picks (naturals mapped to their signature molecule),
# the 3 incoming materials (Evernyl/Veramoss, Undecavertol; tonka omitted = coumarin), and a
# rounded-out standard palette. Curated from public perfumery knowledge — verify CAS/SMILES vs
# PubChem/Pyrfume before any on-chain use. MW computed from molecular formula (exact).
import csv, re, json, statistics as st
AW={"C":12.011,"H":1.008,"O":15.999,"N":14.007,"S":32.06}
def mw(f):
    if not f: return None
    t=0.0
    for el,n in re.findall(r'([A-Z][a-z]?)(\d*)',f):
        if not el: continue
        t+=AW[el]*(int(n) if n else 1)
    return round(t,2)

# (name, CAS, formula, note, family, descriptors)   ''/None where to verify
M=[
# ================= TOP =================
("Ethyl acetate","141-78-6","C4H8O2","top","fruity/solvent","fruity, ethereal, glue-like"),
("Isoamyl acetate","123-92-2","C7H14O2","top","fruity","banana, pear, ripe fruit"),
("cis-3-Hexen-1-ol","928-96-1","C6H12O","top","green","cut grass, leafy, fresh green"),
("Benzaldehyde","100-52-7","C7H6O","top","almond","bitter almond, cherry, marzipan"),
("Octanal (Aldehyde C-8)","124-13-0","C8H16O","top","aldehydic","orange, citrus, fatty aldehydic"),
("Melonal","106-72-9","C10H18O","top","green","melon, cucumber, watery green"),
("Ligustral","68039-49-6","C9H14O","top","green","foliage, leafy, green, cucumber"),
("Limonene","138-86-3","C10H16","top","citrus","orange peel, fresh, sweet · in orange/lemon"),
("alpha-Pinene","80-56-8","C10H16","top","terpenic","pine, resinous, fresh"),
("p-Cymene","99-87-6","C10H14","top","terpenic","citrus, solvent, terpene"),
("Camphor","76-22-2","C10H16O","top","camphoraceous","camphor, medicinal, cooling · in lavandin"),
("Decanal (Aldehyde C-10)","112-31-2","C10H20O","top","aldehydic","orange peel, waxy, aldehydic"),
("Citronellal","106-23-0","C10H18O","top","citrus","citronella, lemon, green, fresh"),
("Citral","5392-40-5","C10H16O","top","citrus","lemon, intense, zesty · in lemon"),
("Eucalyptol (1,8-cineole)","470-82-6","C10H18O","top","fresh/camphor","eucalyptus, minty, cooling"),
("Linalool","78-70-6","C10H18O","top","floral","fresh, floral, lavender, citrus · in lavandin/bergamot"),
("Allyl hexanoate","123-68-2","C9H16O2","top","fruity","pineapple, fruity, juicy"),
("Dihydromyrcenol","18479-58-8","C10H20O","top","fresh","lime, citrus, fresh, soapy"),
("Menthol","89-78-1","C10H20O","top","mint","peppermint, cooling, fresh"),
# ================= HEART =================
("Indole","120-72-9","C8H7N","heart","animalic/floral","jasmine, mothball, animalic"),
("2-Phenylethanol","60-12-8","C8H10O","heart","rose","rose, honey, soft floral"),
("p-Cresyl methyl ether","104-93-8","C8H10O","heart","floral","narcissus, animalic floral · in ylang ylang"),
("p-Anisaldehyde","123-11-5","C8H8O2","heart","sweet floral","hawthorn, mimosa, sweet, powdery"),
("Cinnamaldehyde","104-55-2","C9H8O","heart","spice","cinnamon, warm, sweet spice"),
("Methyl salicylate","119-36-8","C8H8O3","heart","wintergreen","wintergreen, minty, medicinal"),
("Benzyl acetate","140-11-4","C9H10O2","heart","white floral","jasmine, sweet, fruity · in ylang ylang"),
("trans-Anethole","4180-23-8","C10H12O","heart","anise","anise, licorice, sweet"),
("Eugenol","97-53-0","C10H12O2","heart","spice","clove, warm, spicy, sweet · in clove"),
("Isoeugenol","97-54-1","C10H12O2","heart","spice","clove, carnation, spicy sweet"),
("Piperonal (heliotropin)","120-57-0","C8H6O3","heart","powdery","heliotrope, almond, vanilla · ~Heliotropex"),
("Geraniol","106-24-1","C10H18O","heart","rose","rose, floral, sweet, geranium"),
("Nerol","106-25-2","C10H18O","heart","rose","fresh rose, sweet, magnolia"),
("Citronellol","106-22-9","C10H20O","heart","rose","rose, citrus, fresh floral"),
("alpha-Terpineol","98-55-5","C10H18O","heart","floral","lilac, pine, sweet floral"),
("Rose oxide","16409-43-1","C10H18O","heart","rose","green rose, metallic, fresh"),
("Hydroxycitronellal","107-75-5","C10H20O2","heart","muguet","lily of the valley, sweet floral, melon"),
("cis-Jasmone","488-10-8","C11H16O","heart","jasmine","jasmine, floral, celery"),
("Dihydrojasmone","1128-08-1","C11H18O","heart","jasmine","jasmine, herbal, spicy fruity"),
("Bourgeonal","18127-01-0","C11H14O","heart","muguet","lily, muguet, green marine"),
("Helional","1205-17-0","C11H14O3","heart","marine floral","watery floral, muguet, ozonic"),
("Undecavertol","81782-77-6","C11H22O","heart","green floral","green, violet leaf, cucumber · INCOMING"),
("Methyl anthranilate","134-20-3","C8H9NO2","heart","floral","orange blossom, grape, fruity"),
("Linalyl acetate","115-95-7","C12H20O2","heart","floral","bergamot, lavender, fruity floral · LOVE / in bergamot"),
("Geranyl acetate","105-87-3","C12H20O2","heart","rose","rose, fruity, floral"),
("Cyclamen aldehyde","103-95-7","C13H18O","heart","muguet","cyclamen, green floral, fresh"),
("alpha-Ionone","127-41-3","C13H20O","heart","violet","violet, woody, orris, soft floral"),
("beta-Ionone","14901-07-6","C13H20O","heart","violet","violet, woody, floral"),
("beta-Damascone","23726-92-3","C13H20O","heart","rose","rose, fruity, tobacco, plum"),
("beta-Damascenone","23696-85-7","C13H18O","heart","rose","rose, apple, honey, powerful"),
("alpha-Isomethyl ionone","127-51-5","C14H22O","heart","orris/violet","violet, orris, powdery woody"),
("Hedione (methyl dihydrojasmonate)","24851-98-7","C13H22O3","heart","jasmine","jasmine, radiant, magnolia, airy · INTERESTING"),
("Calone","28940-11-6","C11H12O3","heart","marine","watermelon, sea breeze, ozonic"),
("Nerolidol","7212-44-4","C15H26O","heart","woody floral","woody, floral, apple, bark"),
("Farnesol","4602-84-0","C15H26O","heart","floral","delicate floral, sweet, lily, linden"),
("Lindenol","","","heart","floral","linden blossom, honey, soft floral · INTERESTING (verify)"),
("Mayol","","","heart","muguet","lily of the valley, fresh muguet, watery · LOVE (verify)"),
# ================= BASE =================
("Skatole","83-34-1","C9H9N","base","animalic","fecal in trace, animalic, floral in dilution"),
("Coumarin","91-64-5","C9H6O2","base","tonka","hay, almond, tonka, warm sweet · INTERESTING"),
("Dihydrocoumarin","119-84-6","C9H8O2","base","tonka","tonka, coumarinic, sweet, hay"),
("Vanillin","121-33-5","C8H8O3","base","gourmand","vanilla, sweet, creamy, balsamic · INTERESTING"),
("Ethyl vanillin","121-32-4","C9H10O3","base","gourmand","vanilla, intense, sweet"),
("Maltol","118-71-8","C6H6O3","base","gourmand","caramel, malty, cotton candy"),
("Ethyl maltol","4940-11-8","C7H8O3","base","gourmand","cotton candy, caramel, sweet"),
("Furaneol","3658-77-3","C6H8O3","base","gourmand","strawberry, caramel, jammy"),
("gamma-Nonalactone","104-61-0","C9H16O2","base","coconut","coconut, creamy, waxy"),
("gamma-Decalactone","706-14-9","C10H18O2","base","fruity","peach, fruity, creamy"),
("delta-Decalactone","705-86-2","C10H18O2","base","creamy","creamy, coconut, milky"),
("gamma-Undecalactone","104-67-6","C11H20O2","base","fruity","peach, creamy, coconut"),
("Benzyl salicylate","118-58-1","C14H12O3","base","balsamic","soft floral, balsamic, powdery · NO(personal)"),
("Amyl salicylate","87-20-7","C12H16O3","base","balsamic","green, clover, herbal floral"),
("Hexyl salicylate","6259-76-3","C13H18O3","base","balsamic","green, floral, orris, soft"),
("Benzyl benzoate","120-51-4","C14H12O2","base","balsamic","balsamic, faint sweet, fixative"),
("Aurantiol","89-43-0","","base","floral","orange blossom, powdery, tenacious · INTERESTING (Schiff base; verify)"),
("Evernyl (Veramoss)","4707-47-5","C10H12O4","base","mossy","oakmoss, mossy, earthy, phenolic · INCOMING"),
("Rotundone","18374-76-0","C15H22O","base","spice","black pepper, peppery, spicy · LOVE (black pepper)"),
("Cedrol","77-53-2","C15H26O","base","woody","cedarwood, dry, soft woody · LOVE (cedar)"),
("Cedryl acetate","77-54-3","C17H28O2","base","woody","cedar, woody, soft, dry · LOVE (cedar)"),
("Patchoulol","5986-55-0","C15H26O","base","woody/earthy","patchouli, earthy, woody, camphor · INTERESTING"),
("Khusimol","16223-63-5","C15H24O","base","woody/earthy","vetiver, woody, earthy · LOVE (vetiver java) (verify)"),
("Cashmeran","33704-61-9","C14H22O","base","musk","musky, woody, spicy, pine · LOVE"),
("Iso E Super","54464-57-2","C16H26O","base","woody amber","cedar, velvety, ambergris, smooth · INTERESTING"),
("Cedramber","67874-81-1","C17H30O","base","woody amber","amber, cedar, dry, woody"),
("Vertofix (methyl cedryl ketone)","32388-55-9","C17H26O","base","woody amber","cedarwood, amber, ionone woody"),
("Ambroxide (Ambroxan)","6790-58-5","C16H28O","base","amber","ambergris, woody, warm, dry · INTERESTING"),
("Norlimbanol","","","base","woody amber","dry woody, ambergris, cedar, powerful · LOVE (verify)"),
("Amber Xtreme","","","base","amber","amber, woody, dry, extremely powerful · LOVE (verify)"),
("Sandalore","65113-99-7","C14H26O","base","sandalwood","sandalwood, creamy, woody, musky"),
("Javanol","198404-98-7","C15H26O","base","sandalwood","sandalwood, rich, creamy, musky"),
("Ebanol","67801-20-1","C15H24O","base","sandalwood","sandalwood, creamy, rich (verify)"),
("Santaliff","","","base","sandalwood","sandalwood, creamy, woody · INTERESTING (verify)"),
("Galaxolide (HHCB)","1222-05-5","C18H26O","base","musk","clean musk, sweet, floral, soft"),
("Tonalide (AHTN)","1506-02-1","C18H26O","base","musk","clean musk, sweet, woody"),
("Ethylene brassylate","105-95-3","C15H26O4","base","musk","musk, sweet, soft, powdery · NO(personal)"),
("Exaltolide (pentadecanolide)","106-02-5","C15H28O2","base","musk","clean musk, sweet, powdery"),
("Habanolide","111879-80-2","C15H26O2","base","musk","musk, clean, metallic, floral"),
("Ambrettolide","7779-50-2","C16H28O2","base","musk","musk, soft, sweet, natural"),
("Muscone","541-91-3","C16H30O","base","musk","musk, warm, animalic, powdery"),
("Agarospirol","1460-73-7","C15H26O","base","woody/oud","agarwood, woody, oud, warm balsamic · LOVE (oud maleki / oud synth) (verify)"),
("Civetone","542-46-1","C17H30O","base","animalic","civet, animalic, warm musk"),
]

rows=[]
for name,cas,f,note,fam,desc in M:
    rows.append({"name":name,"cas":cas,"formula":f,"mw":mw(f),"note":note,"family":fam,"descriptors":desc,"smiles":""})
order={"top":0,"heart":1,"base":2}
rows.sort(key=lambda r:(order[r["note"]], (r["mw"] if r["mw"] is not None else 1e9)))
with open("/tmp/aroma/aroma_index_v2.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=["name","cas","formula","mw","note","family","descriptors","smiles"]); w.writeheader(); w.writerows(rows)
by={t:[r["mw"] for r in rows if r["note"]==t and r["mw"]] for t in("top","heart","base")}
stats={t:{"n":sum(1 for r in rows if r["note"]==t),"mw_min":min(v),"mw_max":max(v),"mw_mean":round(st.mean(v),1)} for t,v in by.items()}
json.dump({"count":len(rows),"stats":stats},open("/tmp/aroma/stats2.json","w"),indent=1)
json.dump(rows,open("/tmp/aroma/rows2.json","w"))
print("TOTAL:",len(rows))
print(json.dumps(stats,indent=1))
# verify Ivan coverage
picks=["hedione","benzyl acetate","bergamot","geraniol","iso e super","orange","oud","vanillin","coumarin","lemon","lindenol","heliotrop","aurantiol","patchoul","santaliff","ambroxide","oud maleki","mayol","ylang","linalyl acetate","cedar","black pepper","vetiver","cashmeran","norlimbanol","amber xtreme","undecavertol","veramoss","evernyl","lavandin"]
blob=" ".join((r["name"]+" "+r["descriptors"]).lower() for r in rows)
missing=[p for p in picks if p not in blob]
print("possibly-missing tokens:", missing)

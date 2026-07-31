# -*- coding: utf-8 -*-
# GenesisL1 Aroma Molecule Index — v1 PROTOTYPE starter dataset (~50 common aroma chemicals)
# Curated from established public perfumery knowledge for proof-of-concept ONLY.
# Identifiers (CAS/SMILES) and note tiers MUST be verified against open sources
# (PubChem, Pyrfume, Leffingwell/Zenodo) before any on-chain use.
import csv, re, json

# atomic weights (IUPAC standard, common subset)
AW = {"C":12.011,"H":1.008,"O":15.999,"N":14.007,"S":32.06,"Cl":35.45}
def mw(formula):
    total=0.0
    for (el,n) in re.findall(r'([A-Z][a-z]?)(\d*)', formula):
        if not el: continue
        total += AW[el]*(int(n) if n else 1)
    return round(total,2)

# name, CAS, formula, note, family, descriptors, smiles(''=verify)
M = [
# ---- TOP (volatile, light) ----
("Limonene","138-86-3","C10H16","top","citrus","orange peel, fresh, sweet","CC(=C)C1CCC(=CC1)C"),
("alpha-Pinene","80-56-8","C10H16","top","terpenic","pine, resinous, fresh","CC1=CCC2CC1C2(C)C"),
("Citral","5392-40-5","C10H16O","top","citrus","lemon, intense, zesty","CC(=CCCC(=CC=O)C)C"),
("Eucalyptol (1,8-cineole)","470-82-6","C10H18O","top","fresh/camphor","eucalyptus, minty, cooling","CC12CCC(CC1)C(C)(C)O2"),
("Linalool","78-70-6","C10H18O","top","floral","fresh, floral, lavender, citrus","CC(=CCCC(C)(C=C)O)C"),
("Benzaldehyde","100-52-7","C7H6O","top","almond","bitter almond, cherry, marzipan","C1=CC=C(C=C1)C=O"),
("cis-3-Hexen-1-ol","928-96-1","C6H12O","top","green","cut grass, leafy, fresh green","CC/C=C\\CCO"),
("Dihydromyrcenol","18479-58-8","C10H20O","top","fresh","lime, citrus, fresh, soapy","CC(CCCC(C)(C=C)O)C"),
("Menthol","89-78-1","C10H20O","top","mint","peppermint, cooling, fresh",""),
("Allyl hexanoate","123-68-2","C9H16O2","top","fruity","pineapple, fruity, juicy","CCCCCC(=O)OCC=C"),
("Ethyl acetate","141-78-6","C4H8O2","top","fruity/solvent","fruity, ethereal, glue-like","CCOC(=O)C"),
# ---- HEART (floral, spicy, moderate) ----
("Geraniol","106-24-1","C10H18O","heart","rose","rose, floral, sweet, geranium","CC(=CCCC(=CCO)C)C"),
("Citronellol","106-22-9","C10H20O","heart","rose","rose, citrus, fresh floral","CC(CCC=C(C)C)CCO"),
("Nerol","106-25-2","C10H18O","heart","rose","fresh rose, sweet, magnolia","CC(=CCC/C(=C\\CO)/C)C"),
("2-Phenylethanol","60-12-8","C8H10O","heart","rose","rose, honey, soft floral","C1=CC=C(C=C1)CCO"),
("Benzyl acetate","140-11-4","C9H10O2","heart","white floral","jasmine, sweet, fruity","CC(=O)OCC1=CC=CC=C1"),
("Linalyl acetate","115-95-7","C12H20O2","heart","floral","bergamot, lavender, fruity floral","CC(=CCCC(C)(C=C)OC(=O)C)C"),
("alpha-Terpineol","98-55-5","C10H18O","heart","floral","lilac, pine, sweet floral","CC1=CCC(CC1)C(C)(C)O"),
("Geranyl acetate","105-87-3","C12H20O2","heart","rose","rose, fruity, floral","CC(=CCCC(=CCOC(=O)C)C)C"),
("Eugenol","97-53-0","C10H12O2","heart","spice","clove, warm, spicy, sweet","C=CCc1ccc(O)c(OC)c1"),
("Cinnamaldehyde","104-55-2","C9H8O","heart","spice","cinnamon, warm, sweet spice","C1=CC=C(C=C1)/C=C/C=O"),
("beta-Ionone","14901-07-6","C13H20O","heart","violet","violet, woody, floral","CC1=C(C(CCC1)(C)C)/C=C/C(=O)C"),
("alpha-Isomethyl ionone","127-51-5","C14H22O","heart","orris/violet","violet, orris, powdery woody",""),
("Rose oxide","16409-43-1","C10H18O","heart","rose","green rose, metallic, fresh",""),
("Methyl anthranilate","134-20-3","C8H9NO2","heart","floral","orange blossom, grape, fruity","COC(=O)c1ccccc1N"),
("trans-Anethole","4180-23-8","C10H12O","heart","anise","anise, licorice, sweet","C/C=C/c1ccc(OC)cc1"),
("beta-Damascenone","23696-85-7","C13H18O","heart","rose","rose, apple, honey, powerful",""),
("Hedione (methyl dihydrojasmonate)","24851-98-7","C13H22O3","heart","jasmine","jasmine, radiant, magnolia, airy",""),
("Calone","28940-11-6","C11H12O3","heart","marine","watermelon, sea breeze, ozonic",""),
("Piperonal (heliotropin)","120-57-0","C8H6O3","heart","powdery","heliotrope, almond, vanilla, floral","C1OC2=CC=C(C=C2O1)C=O"),
("Indole","120-72-9","C8H7N","heart","animalic/floral","jasmine, mothball, animalic","c1ccc2[nH]ccc2c1"),
# ---- BASE (heavy, long-lasting, fixatives) ----
("Vanillin","121-33-5","C8H8O3","base","gourmand","vanilla, sweet, creamy, balsamic","COc1cc(C=O)ccc1O"),
("Ethyl vanillin","121-32-4","C9H10O3","base","gourmand","vanilla, intense, sweet","CCOc1cc(C=O)ccc1O"),
("Coumarin","91-64-5","C9H6O2","base","tonka","hay, almond, tonka, warm sweet","O=c1ccc2ccccc2o1"),
("Iso E Super","54464-57-2","C16H26O","base","woody amber","cedar, velvety, ambergris, smooth",""),
("Galaxolide (HHCB)","1222-05-5","C18H26O","base","musk","clean musk, sweet, floral, soft",""),
("Ambroxide (Ambroxan)","6790-58-5","C16H28O","base","amber","ambergris, woody, warm, dry",""),
("Ethylene brassylate","105-95-3","C15H26O4","base","musk","musk, sweet, soft, powdery",""),
("Cashmeran","33704-61-9","C14H22O","base","musk","musky, woody, spicy, pine",""),
("Cedrol","77-53-2","C15H26O","base","woody","cedarwood, dry, soft woody",""),
("Patchoulol","5986-55-0","C15H26O","base","woody/earthy","patchouli, earthy, woody, camphor",""),
("Sandalore","65113-99-7","C14H26O","base","sandalwood","sandalwood, creamy, woody, musky",""),
("Javanol","198404-98-7","C15H26O","base","sandalwood","sandalwood, rich, creamy, musky",""),
("Benzyl benzoate","120-51-4","C14H12O2","base","balsamic","balsamic, faint sweet, fixative","O=C(OCc1ccccc1)c1ccccc1"),
("Benzyl salicylate","118-58-1","C14H12O3","base","balsamic","soft floral, balsamic, powdery","O=C(OCc1ccccc1)c1ccccc1O"),
("Muscone","541-91-3","C16H30O","base","musk","musk, warm, animalic, powdery",""),
("Ambrettolide","7779-50-2","C16H28O2","base","musk","musk, soft, sweet, natural",""),
("Tonalide (AHTN)","1506-02-1","C18H26O","base","musk","clean musk, sweet, woody",""),
("Civetone","542-46-1","C17H30O","base","animalic","civet, animalic, warm musk",""),
("Skatole","83-34-1","C9H9N","base","animalic","fecal (trace), animalic, floral in dilution","Cc1c[nH]c2ccccc12"),
]

rows=[]
for (name,cas,formula,note,family,desc,smiles) in M:
    rows.append({"name":name,"cas":cas,"formula":formula,"mw":mw(formula),
                 "note":note,"family":family,"descriptors":desc,
                 "smiles":smiles if smiles else ""})

# sort: top, heart, base; within tier by MW asc
order={"top":0,"heart":1,"base":2}
rows.sort(key=lambda r:(order[r["note"]], r["mw"]))

# CSV
with open("/tmp/aroma/aroma_index_v1.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=["name","cas","formula","mw","note","family","descriptors","smiles"])
    w.writeheader(); w.writerows(rows)

# quick stats for the writeup
import statistics as st
by={t:[r["mw"] for r in rows if r["note"]==t] for t in ("top","heart","base")}
stats={t:{"n":len(v),"mw_min":min(v),"mw_max":max(v),"mw_mean":round(st.mean(v),1)} for t,v in by.items()}
json.dump({"count":len(rows),"stats":stats}, open("/tmp/aroma/stats.json","w"), indent=1)
json.dump(rows, open("/tmp/aroma/rows.json","w"), indent=0)
print("built", len(rows), "molecules")
print(json.dumps(stats, indent=1))

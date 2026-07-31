import json, os, re, gzip, shutil

rows=json.load(open("rows2.json"))

def desc_list(d):
    d=re.sub(r'·.*$','',d)                      # drop "· source" note
    d=re.sub(r'\((incoming|verify|[^)]*)\)','',d)  # drop parenthetical flags
    return [t.strip() for t in d.split(',') if t.strip()]

INDEX_URL="https://vanpez.github.io/aroma-index/"

def is_empty(v):
    # None, "" and [] are absences, not values. 0 / 0.0 / False are real values.
    return v is None or (isinstance(v,(str,list,dict)) and len(v)==0)

def prune(d):
    """Drop absent fields rather than encoding them as null/"".
    Tokens are immutable: an omitted field reads as 'not recorded',
    a null field reads as sloppy. Defensive — the source data should
    already be complete for every field we intend to carry."""
    return {k:v for k,v in d.items() if not is_empty(v)}

def prune_attrs(attrs):
    return [a for a in attrs if not is_empty(a.get("value"))]

mintable=[r for r in rows if r.get("inchikey") and r.get("smiles")]
excluded=[r for r in rows if not (r.get("inchikey") and r.get("smiles"))]

os.makedirs("mint/metadata", exist_ok=True)

records=[]            # canonical on-chain fields (source of truth)
erc=[]                # ERC-721 tokenURI render (reference)
for i,r in enumerate(sorted(mintable,key=lambda x:(x["note"]!="top",x["note"]!="heart",x["mw"] or 0)),start=1):
    rec={
      "id": i,
      "inchikey": r["inchikey"],
      "smiles": r["smiles"],
      "name": r["name"],
      "cid": r.get("cid"),
      "cas": r.get("cas"),
      "formula": r.get("formula"),
      "mw": r.get("mw"),
      "note": r.get("note"),
      "family": r.get("family"),
      "bp_c": r.get("bp_c"),
      "vp_pa_25c": round(r["vp_pa"],4) if r.get("vp_pa") is not None else None,
      "descriptors": desc_list(r["descriptors"]),
    }
    rec=prune(rec)
    records.append(rec)
    meta={
      "name": r["name"],
      "description": f"{r['name']} — aroma molecule ({r.get('family')}). Note tier: {r.get('note')}. "
                     f"Structure is stored as SMILES; the 3D conformer is regenerated in-browser. "
                     f"Public-good record in the GenesisL1 Aroma Molecule Index.",
      "external_url": INDEX_URL,
      "attributes": [
        {"trait_type":"InChIKey","value":r["inchikey"]},
        {"trait_type":"SMILES","value":r["smiles"]},
        {"trait_type":"Formula","value":r.get("formula")},
        {"trait_type":"Molecular weight","value":r.get("mw")},
        {"trait_type":"Note tier","value":r.get("note")},
        {"trait_type":"Odor family","value":r.get("family")},
        {"trait_type":"Boiling point (°C)","value":r.get("bp_c")},
        {"trait_type":"Vapor pressure (Pa, 25°C)","value":round(r["vp_pa"],2) if r.get("vp_pa") is not None else None},
        {"trait_type":"PubChem CID","value":r.get("cid")},
        {"trait_type":"CAS","value":r.get("cas")},
        {"trait_type":"Odor descriptors","value":", ".join(desc_list(r["descriptors"]))},
      ],
    }
    meta["attributes"]=prune_attrs(meta["attributes"])
    erc.append(meta)
    open(f"mint/metadata/{i:04d}.json","w").write(json.dumps(meta,ensure_ascii=False,separators=(',',':')))

os.makedirs("mint/structures", exist_ok=True)
for rec in records:
    # molecular file = SMILES (canonical compact structure; 3D regenerates from it)
    open(f"mint/structures/{rec['id']:04d}.smi","w").write(f"{rec['smiles']}\t{rec['name']}\n")

json.dump(records, open("mint/mint-records.json","w"), ensure_ascii=False, indent=1)
json.dump(erc, open("mint/erc721-metadata.json","w"), ensure_ascii=False, indent=1)

# byte accounting
def b(o): return len(json.dumps(o,ensure_ascii=False,separators=(',',':')).encode())
rec_bytes=[b(x) for x in records]
erc_bytes=[b(x) for x in erc]
recs_min=[json.dumps(x,ensure_ascii=False,separators=(',',':')).encode() for x in records]
blob=b"\n".join(recs_min); blobgz=len(gzip.compress(blob,9))

stats={
 "mintable": len(records), "excluded_no_structure": len(excluded),
 "excluded_names":[r["name"] for r in excluded],
 "onchain_record_bytes": {"avg":round(sum(rec_bytes)/len(rec_bytes),1),"min":min(rec_bytes),"max":max(rec_bytes),"total":sum(rec_bytes)},
 "erc721_render_bytes": {"avg":round(sum(erc_bytes)/len(erc_bytes),1),"total":sum(erc_bytes)},
 "collection_gzip_bytes": blobgz,
}
json.dump(stats, open("mint/_stats.json","w"), indent=1)
print(json.dumps(stats,indent=1))

import json, gzip, base64, statistics as st
rows=json.load(open("rows2.json"))
N=len(rows)

def desc_list(d):
    import re
    d=re.sub(r'·.*$','',d)
    return [t.strip() for t in d.split(',') if t.strip()]

# ---------- FORMAT A: full ERC-721 metadata record (verbose, marketplace-standard) ----------
def erc721(r):
    return {
      "name": r["name"],
      "description": f"{r['name']} — an aroma molecule ({r['family']}). Public-good record in the GenesisL1 Aroma Molecule Index.",
      "image": "",  # optional; can be data: URI or omitted (3D regenerates from SMILES)
      "identifiers": {
        "inchikey": r.get("inchikey"),
        "smiles": r.get("smiles"),
        "pubchem_cid": r.get("cid"),
        "cas": r.get("cas"),
        "formula": r.get("formula"),
      },
      "properties": {
        "mw": r.get("mw"),
        "bp_c": r.get("bp_c"),
        "vp_pa_25c": r.get("vp_pa"),
        "note_tier": r.get("note"),
        "odor_family": r.get("family"),
        "descriptors": desc_list(r["descriptors"]),
      },
      "attributes": [
        {"trait_type":"Note tier","value":r.get("note")},
        {"trait_type":"Odor family","value":r.get("family")},
        {"trait_type":"Formula","value":r.get("formula")},
        {"trait_type":"MW","value":r.get("mw")},
      ],
    }

# ---------- FORMAT B: compact JSON (short keys, minified, no whitespace) ----------
def compact(r):
    return {
      "n": r["name"], "k": r.get("inchikey"), "s": r.get("smiles"),
      "c": r.get("cid"), "a": r.get("cas"), "f": r.get("formula"),
      "m": r.get("mw"), "t": r.get("note"), "fam": r.get("family"),
      "bp": r.get("bp_c"), "vp": r.get("vp_pa"),
      "d": desc_list(r["descriptors"]),
    }

def gz(b): return gzip.compress(b if isinstance(b,bytes) else b.encode(), 9)
def b64(b): return base64.b64encode(b)

def sizes(recs_json_bytes):
    raw=sum(len(x) for x in recs_json_bytes)
    gzs=[gz(x) for x in recs_json_bytes]
    gzsum=sum(len(x) for x in gzs)
    b64sum=sum(len(b64(x)) for x in gzs)
    return raw,gzsum,b64sum

# per-molecule bytes for each format
A=[json.dumps(erc721(r),ensure_ascii=False,separators=(',',':')).encode() for r in rows]
Apretty=[json.dumps(erc721(r),ensure_ascii=False,indent=2).encode() for r in rows]
B=[json.dumps(compact(r),ensure_ascii=False,separators=(',',':')).encode() for r in rows]
# structure-only anchors
SMI=[ (r.get("smiles") or "").encode() for r in rows if r.get("smiles")]
KEY=[ (r.get("inchikey") or "").encode() for r in rows if r.get("inchikey")]

def avg(x): return sum(len(i) for i in x)/len(x)

print(f"N molecules = {N}\n")
print(f"SMILES only:   avg {avg(SMI):.1f} B  (min {min(len(i) for i in SMI)}, max {max(len(i) for i in SMI)})")
print(f"InChIKey:      fixed 27 B\n")

for name,recs in [("A) ERC-721 minified", A),("A') ERC-721 pretty", Apretty),("B) compact short-keys", B)]:
    raw,gzs,b64s=sizes(recs)
    # whole-collection single blob
    blob=b"\n".join(recs)
    blobgz=len(gz(blob)); blobb64=len(b64(gz(blob)))
    print(f"[{name}]")
    print(f"   per-molecule avg raw:      {avg(recs):7.1f} B")
    print(f"   1. collection raw:         {raw:8d} B  ({raw/1024:.1f} KB)")
    print(f"   2. sum of per-mol gzip:    {gzs:8d} B   <- per-record gzip (overhead-heavy)")
    print(f"   2b. WHOLE-collection gzip: {blobgz:8d} B  ({blobgz/1024:.1f} KB)  <- shared dictionary")
    print(f"   3. base64 of (2b):         {blobb64:8d} B  ({blobb64/1024:.1f} KB)  (+33% vs gzip)")
    print(f"   per-mol in collection-gzip:{blobgz/N:7.1f} B\n")

# extrapolate compact whole-collection gzip per-molecule to Leffingwell scale
blobB=gz(b"\n".join(B)); permol=len(blobB)/N
print(f"Extrapolation (compact format, whole-collection gzip ~{permol:.1f} B/molecule):")
for label,cnt in [("99 (now)",99),("3,500 Leffingwell",3500),("100,000",100000),("1,000,000",1000000)]:
    b=permol*cnt
    u='B'
    for uu in ['B','KB','MB','GB']:
        if b<1024: u=uu; break
        b/=1024
    print(f"   {label:20s} ~{b:.1f} {u}")

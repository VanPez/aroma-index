import json, re, numpy as np
np.random.seed(42)
rows=json.load(open("rows2.json"))

def tokens(d):
    d=re.sub(r'·.*$','',d)                     # drop source note
    d=re.sub(r'\((incoming|verify|[^)]*)\)','',d)
    return [t.strip().lower() for t in d.split(',') if t.strip()]

# vocabulary
vocab=sorted({t for r in rows for t in tokens(r['descriptors'])})
vi={t:i for i,t in enumerate(vocab)}
X=np.zeros((len(rows),len(vocab)),dtype=float)
for r_i,r in enumerate(rows):
    for t in tokens(r['descriptors']): X[r_i,vi[t]]=1.0

def classify(fam):
    f=fam.lower()
    if 'floral' in f or f in ('rose','jasmine','muguet','violet','orris/violet','lily'): return 'Floral'
    if 'musk' in f: return 'Musk'
    if 'animal' in f or 'civet' in f: return 'Animalic'
    if 'amber' in f or 'balsam' in f: return 'Amber & Balsamic'
    if any(k in f for k in ('gourmand','tonka','coconut','almond','powder','vanilla','caramel','cream')): return 'Sweet & Gourmand'
    if any(k in f for k in ('wood','sandal','oud','cedar','moss','vetiver','patch')): return 'Woody'
    if any(k in f for k in ('spice','spicy','anise','clove','cinnam','wintergreen','herb')): return 'Spicy & Herbal'
    if 'green' in f: return 'Green'
    if 'fruit' in f: return 'Fresh & Fruity'
    if any(k in f for k in ('citrus','fresh','aldehyd','terpen','marine','mint','camphor','lemon','berg')): return 'Fresh & Fruity'
    return 'Other'

cls=[classify(r['family']) for r in rows]
from collections import Counter
print("classes:", Counter(cls))

# ---------- SOM (pure numpy Kohonen) ----------
def train_som(X, gx=11, gy=11, iters=8000, seed=42):
    rng=np.random.default_rng(seed)
    n,d=X.shape
    W=rng.random((gx,gy,d))*0.1
    # grid coords
    gi,gj=np.meshgrid(np.arange(gx),np.arange(gy),indexing='ij')
    grid=np.stack([gi,gj],axis=-1).astype(float)
    lr0=0.5; sig0=max(gx,gy)/2.0
    for t in range(iters):
        frac=t/iters
        lr=lr0*(1-frac); sig=sig0*(1-frac)+0.5
        x=X[rng.integers(n)]
        dist=np.sum((W-x)**2,axis=-1)          # BMU by euclidean
        bi,bj=np.unravel_index(np.argmin(dist),dist.shape)
        d2=np.sum((grid-np.array([bi,bj]))**2,axis=-1)
        h=np.exp(-d2/(2*sig*sig))[...,None]
        W+= lr*h*(x-W)
    # assign BMU per sample
    coords=[]
    for x in X:
        dist=np.sum((W-x)**2,axis=-1)
        bi,bj=np.unravel_index(np.argmin(dist),dist.shape)
        coords.append([bi,bj])
    return np.array(coords,dtype=float),(gx,gy)

som_xy,(gx,gy)=train_som(X)
# jitter co-located points deterministically
jit=np.random.default_rng(7).uniform(-0.38,0.38,size=som_xy.shape)
som_xy=som_xy+jit

# ---------- UMAP ----------
import umap
reducer=umap.UMAP(n_neighbors=15,min_dist=0.2,metric='cosine',random_state=42)
umap_xy=np.asarray(reducer.fit_transform(X),dtype=float)
for k in range(umap_xy.shape[1]):               # guard non-finite (disconnected pts)
    col=umap_xy[:,k]; bad=~np.isfinite(col)
    if bad.any(): col[bad]=np.nanmedian(col[~bad]); umap_xy[:,k]=col

def norm(a):
    # robust: clip to 2nd-98th percentile so a few outliers can't crush the bulk
    a=np.asarray(a,dtype=float); out=np.zeros_like(a)
    for k in range(a.shape[1]):
        col=a[:,k]; lo,hi=np.nanpercentile(col,2),np.nanpercentile(col,98)
        if hi-lo==0: hi=lo+1.0
        out[:,k]=(np.clip(col,lo,hi)-lo)/(hi-lo)
    return out
som_n=norm(som_xy); umap_n=norm(umap_xy)

pts=[]
for i,r in enumerate(rows):
    pts.append({"name":r["name"],"family":r["family"],"cls":cls[i],"note":r["note"],
                "desc":", ".join(tokens(r["descriptors"])),
                "som":[round(float(som_n[i,0]),4),round(float(som_n[i,1]),4)],
                "umap":[round(float(umap_n[i,0]),4),round(float(umap_n[i,1]),4)]})
json.dump({"points":pts,"classes":sorted(set(cls))}, open("scentmap.json","w"), ensure_ascii=False)
print("wrote scentmap.json", len(pts), "points; classes:", sorted(set(cls)))

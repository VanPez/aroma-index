# MolNFT resolver — verification & test report

*Reviewed while you were at CrossFit. Joe's `AromaIndexMolNFT.html`, checked end-to-end. Verdict: safe, correct, and working — with one piece that still needs Mike's endpoint to test.*

**Live preview (your main index is untouched):**
https://vanpez.github.io/aroma-index/molnft-resolver.html

---

## What it is

Your live index (same 99 molecules, BP/VP columns, 3D viewer, search) plus a new **MolNFT / IPFS structure resolver** section with two panes:

1. **Mock mode** — pick a molecule, generate clearly-labelled placeholder links (IPFS URI, gateway URL, MolNFT deep link, RPC-read shape) for a future mint. Nothing is checked on-chain; every link is tagged "mock".
2. **Live read** — supply a GenesisL1 JSON-RPC URL + MolNFT contract + token ID, and it reads the token read-only and renders its structure in the browser. Also resolves any IPFS/HTTPS structure or metadata link.

## Security review — clean

- **Read-only.** Only `eth_call` (view calls) and `eth_chainId`. No `eth_sendTransaction`, no `eth_sign`, no wallet connection, no `requestAccounts`. It never asks for a key, seed, or signature — grep-confirmed absent.
- **No injection surface.** No `eval`, no `new Function`, no `document.write`. All on-chain/IPFS values are HTML-escaped before display, and link `href`s are protocol-checked (`http`/`https` only), so a malicious `tokenURI` can't inject a `javascript:` link.
- **Bounded.** Auto-decode capped at 12 MB; RPC calls time out at 30 s.
- **Local only.** Stores just the RPC URL / contract / token / gateway in browser localStorage to remember the form. No secrets, nothing sent anywhere except the RPC and IPFS gateway you type.

## Correctness — unit-tested against ethers

The riskiest part is the hand-rolled ABI encode/decode (no library shortcut). I unit-tested it in Node against ethers 6.17 — **7/7 pass**:

- `encodeCall("getEntireNFT(uint256)", …)` produces byte-identical calldata to ethers' own encoder; `tokenURI` selector matches the canonical ERC-721 value `0xc87b56dd`.
- `decodeSingleString` round-trips.
- `decodeStringTuple` correctly recovers the **11-field `getEntireNFT` return** — including the base64 structure payload in the last field — and handles unicode, empty, and long (500+ char) strings.
- Single-string (`getCombinedData`) fallback works.

## Live test — rendering pipeline works

On the deployed preview I fed the "Resolve link" path real public files:

- **PubChem 3D SDF** (limonene ligand, 4 KB) → detected `sdf`, rendered in 3Dmol, download offered. ✓
- **RCSB PDB** (crambin protein, 49 KB) → detected `pdb`, rendered as cartoon+sticks. ✓
- **Mock mode** → 4 correctly-labelled placeholder links. ✓

So it handles **both a ligand (SDF) and a receptor (PDB)** — exactly the pair docking needs.

## Architecture insight (worth flagging to Mike)

The resolver's field map reveals GenesisL1's MolNFT stores **PDB-style structures on-chain**: `getEntireNFT(uint256)` returns `IDCODE, HEADER, ACCESSION_DATE, COMPOUND, SOURCE, AUTHOR_LIST, RESOLUTION, EXPERIMENT_TYPE, SEQUENCE, imageBase64, fileBase64`. So the structure is already on-chain (just as Joe said, "like the PDB structures") — which means the "canonical field" idea is really just *adding the InChIKey* on top so molecules interlink across collections.

## The one thing still untested

The **live GenesisL1 on-chain read** — I can't test it without a real GenesisL1 RPC URL + an existing MolNFT contract address & token ID. The code path is verified correct in isolation (ABI encode/decode tested), but the round-trip against a real node is exactly what Mike's endpoint unblocks. The moment he shares those, point the "Live read" pane at them and it should pull + render an on-chain molecule.

## Suggested next steps

1. Get an **RPC URL + sample MolNFT (contract + token ID)** from Mike, run the live read, confirm an on-chain structure renders.
2. If it works, decide whether to fold the resolver into the **main index** (I'd merge it into your generator so it stays maintainable) or keep it as this separate preview.
3. Then the docking direction: the SDF+PDB rendering already in place is the front-end half of Joe's "pick docking candidates by features" idea.

*Nothing here changed your showcased page — `index.html` is exactly as it was. This is an additive, clearly-named preview file you can keep, merge, or delete.*

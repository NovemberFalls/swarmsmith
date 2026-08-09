# The sealed intent card — verify it yourself

`SEALED_INTENT.md` in this directory is the intent card for the cell reported in
`FINDINGS.md` §4.9. It describes what the caller actually wanted from six words —
*"lets make a browser based mmorpg"* — and it was **written, sealed and hashed before
either arm ran**, stored outside both working trees, and shown to neither arm.

This is the one claim in the paper you do not have to take on trust.

## Why it matters

The failure mode it defends against is the obvious one: score a run, then decide what you
were measuring. If the target can be edited after the result is in, the result means
nothing. Recording the hash before spend makes that edit detectable by anyone.

It constrains **post-hoc rewriting of the target**. It does not do anything about sample
size — the cell is n=1, and §4.9 says so.

## Verify

The digest is over the file's bytes with LF line endings. This repo's `.gitattributes`
pins `*.md` to `eol=lf`, so a fresh clone on any platform should reproduce it exactly.

```bash
sha256sum docs/crown-cell/SEALED_INTENT.md
```

```powershell
(Get-FileHash docs\crown-cell\SEALED_INTENT.md -Algorithm SHA256).Hash.ToLower()
```

Expected — **2665 bytes**:

```
01e0008f2639ebfb36aaefea6e5d9fd2f642eb55c01bf89fa1145e0dc0531f85
```

If your checkout disagrees, normalize first and compare again:

```bash
python -c "import hashlib,io;print(hashlib.sha256(io.open('docs/crown-cell/SEALED_INTENT.md','rb').read().replace(b'\r\n',b'\n')).hexdigest())"
```

## Provenance

The hash was committed to the pre-registration at
`bench/backlog/CROWN_CELL.md` (`b608f0a`) in the private `team` repo **before any spend**,
and the card was copied here unmodified. The value above is what that commit records.

What this proves and what it does not: it proves the target was fixed in advance and has
not been altered since. It does not prove the *scoring* was correct — that was done by the
owner from the artifacts, and §4.9 states so alongside the rest of the cell's limits.

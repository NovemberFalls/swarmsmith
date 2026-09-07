# coding-v5.0 — skill v5.0.1

The **v5.0 apply-tier coding skill**, packaged with the applier it depends on.

Install it, and `/orch-anth-5.0` works as measured. Copy the markdown alone and it
does not — the skill's central mechanism calls a tool that would not be there.

```bash
python install.py            # install
python install.py --check    # verify; exit 1 on drift
python install.py --uninstall
```

---

## Why this is a package and not two files

The skill and the applier are **one contract**. v5.0 emits SEARCH/REPLACE blocks in
exactly one format; the applier parses that format and applies a block **iff its SEARCH
matches exactly once**. Separate them and they drift — someone pairs the skill with a
hand-rolled applier that force-applies on a fuzzy match, the determinism is gone, and
the skill still advertises it.

That failure is measured, not hypothetical. From [FINDINGS.md](../../FINDINGS.md) §4.7:

| what was applied | score |
|---|---|
| verbatim SEARCH/REPLACE, deterministic apply | **532/532 blocks clean** |
| lossy old/new pairs, deterministic apply | 5/16 |
| lossy old/new pairs, *model* applying | 8/16 |
| same model, no patch, just the spec | 10/20 |

A model handed a flawed "exact" patch scored **below** the same model working from the
spec. **A bad diff is worse than no diff.** So the applier is not an optimization you can
substitute — an approximate one is worse than not installing it at all.

`install.py` checksums every file against `MANIFEST.json` before writing, and `--check`
tells you if an installed copy has drifted.

---

## What it installs

| file | destination | what it is |
|---|---|---|
| `commands/orch-anth-5.0.md` | `<claude>/commands/` | the skill → `/orch-anth-5.0` |
| `commands/fix.md` | `<claude>/commands/` | single-issue path → `/fix` |
| `tools/apply_blocks.py` | `<claude>/tools/orch-apply/` | the deterministic applier |

`<claude>` is `$CLAUDE_CONFIG_DIR`, else `~/.claude`.

**Nothing else is touched.** This package registers no hooks and does not edit
`settings.json`. If a destination file already exists with different content, it is
backed up alongside as `.bak` before being replaced.

Requires **Python 3.8+**, standard library only. No dependencies, no build step, no
network access.

---

## Using it

Invoke `/orch-anth-5.0 <task>` as normal. On DIFFABLE work the skill computes the change,
writes SEARCH/REPLACE blocks to a plan file, and lands them with:

```bash
python ~/.claude/tools/orch-apply/apply_blocks.py plan.blocks --root . --json apply.json
```

Windows/PowerShell: `python "$env:USERPROFILE\.claude\tools\orch-apply\apply_blocks.py" ...`

| exit | meaning |
|---|---|
| `0` | every block applied cleanly |
| `1` | residue (`nomatch` / `nonunique`) — escalate per skill §4.9 step 3 |
| `2` | malformed blocks — fix the emit, never force it |

Also: `--dry-run` (report, write nothing) · `--atomic` (all-or-nothing) · `--root` (repo
root the `FILE:` paths resolve against).

**The applier never force-applies.** A block whose SEARCH is missing or ambiguous is
reported, not guessed. That refusal is the guarantee — do not add a `--fuzzy` flag.

---

## Verify it

```bash
python -m pytest tests -q     # 35 tests, no install required
```

They pin the contract the skill depends on: exactly-once matching, residue never
force-applied, atomic abort, byte-exact indentation, CRLF/LF preservation, unicode
round-trip, and sequential blocks seeing prior edits.

---

## Naming

This installs as **`/orch-anth-5.0`**, matching this repo and
[boord-its.com/skills](https://boord-its.com/skills). If you prefer a different command
name, rename the file in `<claude>/commands/` — the skill body does not reference its own
name. (The author's local checkout calls it `/orch-code-anth`; same skill.)

---

## What is deliberately NOT here

- **`/orch-clean` and the §9 clean phase.** Built, but not yet through the arena. This
  repo's claim is *measured, not asserted*, so unmeasured work does not ship in the
  champion package. It will land in `coding-v5.1` once it has numbers.
- **Hooks.** `hooks/` in the repo root is opt-in and separate on purpose; this package
  will not edit your `settings.json`.

## Provenance

v5.0 graduated 2026-07-26 on the isolated mechanism (k=25): ~1.7× faster, ~2.6× cheaper.
The whole-skill economics were **re-measured 2026-07-31** against v4.1's canonical swarm
path, and that re-measurement corrected the first one: **v5.0 is 10/10 correct against
v4.1's 7/10 at 1.6–2.1× lower cost per successful run**, and the win is conversion rate,
not speed. The earlier "1.9× faster / 2.0× cheaper, correctness-equal" figures compared
v5.0 against a **solo-restricted** v4.1; per attempt v4.1 is marginally faster. At scale
(400K-token fixture, k=3) the two tie at 3/3. Generative work is a clean superset (5/5,
22/22). Full evidence — including the losing runs — in
[FINDINGS.md](../../FINDINGS.md) §4.7 and §4.7a.

**Read §4.12 before trusting those numbers.** They were produced by the v5.0 edition of
the skill, which deferred §1–§3 and §4.1–§4.8 to a v4.1 the harness never injected. This
package ships **v5.0.1**, which states those sections in full. No mechanism changed, but
the crown is inherited rather than re-earned, and the arm that would settle it has not
run. The skill's own "Known limits" section says so too.

The packaged skill differs from the benchmarked text in two ways: §4.9 step 2 names the
applier's installed path and exit codes (the benchmarked snapshot describes the applier
abstractly, which is precisely why an installing user could not run it), and §1–§8 are
present in full rather than deferred.

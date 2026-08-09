# /orch-anth-5.0 — v5.0 apply-tier (computed-diff · deterministic apply · lane discipline)

STATUS: **LIVE — the current champion coding skill (graduated 2026-07-26; economics
re-measured 2026-07-31).** v5.0 = v4.1 + a **deterministic apply-tier** for mechanical
fan-out (the orchestrator computes the exact change, emits verbatim SEARCH/REPLACE, a
stdlib applier lands it).

**What the crown is:** correctness, and cost per *result*, **on work that fits one
context**. Measured against v4.1's canonical **swarm** path (opus/low, identical toolset,
k=5 complete): v5.0 is **10/10 correct vs v4.1's 7/10** at **1.6–2.1× lower cost per
successful run**.

**What the crown is not:**

- **A wall-clock win.** Per *attempt* v4.1 is marginally faster on the refactor fixture.
  The entire economic advantage is conversion rate — v5.0 converts every attempt, v4.1
  converts 7 of 10. Earlier claims of "1.9× faster, 2.0× cheaper" compared v5.0 against a
  **solo-restricted** v4.1; see the correction under Evidence.
- **A win at scale.** On a 400K-token fixture (k=3) the two **tie at 3/3**, with v5.0 only
  1.28× faster and 1.09× cheaper. The advantage is a small-and-medium-work advantage.

v4.1 is retired as the default and preserved in this repo
([`orchestrate.md`](orchestrate.md)) as rollback. Everything else in v4.1 is preserved
verbatim. Small fixtures at k=5 (30 cells), large at k=3 (6 cells); ladder continues to
k=10, then 25.

## The v5.0 thesis (owner-originated 2026-07-26)

**The orchestrator is the brain. When it already understands the exact change, it should
push that change out as data — not delegate the *understanding* to a worker model.** The
worker's job on mechanical/rule-dense edits is APPLICATION, and application of a verbatim
diff is deterministic — it does not need a model at all.

### Evidence (arena_refactor migration + arena_feature generative)

All figures come from the deterministic-evals arena: frozen test projects, hidden answer
keys copied in only after the run, pinned models, worker spawns counted from the raw
event stream. Method and per-run data: FINDINGS.md §4.7.

**Mechanism, isolated** (68-site logEvent migration, shared core pre-done, opus/low,
k=25): v5.0 raw 22/25, wall p50 102s, $0.46/run — vs v4.1 in-place 24/25, 173s, $1.19.
~1.7× faster, ~2.6× cheaper; output band ±15% vs 5×. Both reach ~100% via the mandatory
gate plus the §4.9 escalation loop.

**Whole skill, end-to-end** (2026-07-31 campaign; nothing pre-done, self-routed, opus/low,
identical toolset per arm so the skill text is the only variable; k=5 complete, 30/30
cells). **Read the denominator:** cost per attempt and cost per *successful run* rank
these skills differently, and only the second is decidable in advance — you cannot keep
the good attempts and discard the bad ones.

| arm | fixture | correct | $/attempt | **$/success** | wall p50 | spawns |
|---|---|---|---|---|---|---|
| v5.0 | arena_feature | **5/5** | $1.91 | **$1.91** | 248s | 0 |
| v5.0 | arena_refactor | **5/5** | $5.47 | **$5.47** | 571s | 0 |
| v4.1 | arena_feature | 4/5 | $3.22 | $4.03 | 397s | 0, 6–9 |
| v4.1 | arena_refactor | 3/5 | $5.19 | $8.65 | 533s | 7–9 |

**Small fixtures, k=5 complete (30 cells): v5.0 10/10 correct against v4.1's 7/10, at
2.1× and 1.6× lower cost per result.** On refactor the per-attempt costs are within 6%
and v4.1 is marginally faster per attempt — the whole win is conversion rate. Every v4.1
failure is the same site, `SITE FAIL [N14] src/gateway/server.cjs`.

**Large fixture — where the gap closes.** `bigctx_real`: ~400K tokens of real
hand-written code, 22 bugs planted by mutation testing, built so a sharded audit can give
each slice a lean context. k=3, complete:

| arm | correct | **$/success** | wall p50 | spawns |
|---|---|---|---|---|
| v5.0 | **3/3** | **$10.10** | 871s | 11, 13, 0 |
| v4.1 | **3/3** | $11.00 | 1118s | 18, 9, 0 |

**Correctness ties at scale.** v5.0 keeps a modest edge (1.28× faster, 1.09× cheaper),
nothing like the 2× it holds on small work. Both arms swarm when the surface is large and
both went solo on one run apiece — routing is task-adaptive for *both* skills, not a v5.0
signature. A "v5.0 is a context hog that collapses like a monolith" hypothesis was tested
here directly and **falsified**.

**Correction to the pre-2026-07-31 figures.** The earlier "1.9× faster, 2.0× cheaper,
v4.1 grinds 45–130 edit turns" comparison ran v4.1 **solo-restricted** (no `Agent`
tool) — a limitation pre-registered in FINDINGS.md §4.7 and now confirmed by measurement.
Given its canonical swarm path, v4.1 delegates the grinding into worker contexts, and two
of those claims fail:

- **Wall:** the gap closes and inverts — v4.1 533s vs v5.0 571s per attempt on refactor.
- **Turns:** the profile inverts, but the *opposite way* from the published claim.
  Recomputed from retained transcripts (n=41): **v4.1 12–63, p50 24; v5.0 34–101, p50
  55.** v5.0 runs roughly **2× more** parent turns than v4.1 — v4.1's grinding happens
  inside workers where the parent never counts it. The published "v5.0 emits once and
  applies" describes the apply step, not the session.

The cost-per-result claim survives; the wall claim does not, and the turn claim survives
only with its sign reversed.

**Generative regression** (arena_feature, k=5): v5.0 5/5 at 22/22 — no regression where
the apply-tier never fires. **Behavior is not identical to v4.1**, as previously claimed,
but the difference is routing selectivity rather than capability: v5.0 stays solo on the
~28K-token fixtures where v4.1 spawns 6–9, and swarms 11–13 on the 400K-token one. Below
the crossover, coordination is pure overhead — v5.0 is the more selective router.

**Apply fidelity:** 532/532 blocks clean across the mechanism runs. The 3 v5.0 misses
were detected and typed (2 fidelity, 1 rule) and recovered to 16/16 at ~$0.01/run
amortized.

The apply half is a string match (not model-dependent); the correctness half is Opus's
planning, which lands 16/16 on its scope. Evidence: FINDINGS.md §4.7 (k=25 mechanism +
recovery taxonomy) and the 2026-07-31 campaign rows (`v5_live_k25.jsonl`, retained
transcripts) for the corrected economics.

### Why FORMAT is load-bearing (the failures that shaped this)

- Opus hand-written **unified diff** → line-number drift → `git apply` REJECTS; fuzzy
  `patch` recovers only 13/16.
- **Lossy old/new pairs** (not copied verbatim from the file) → 5/16 deterministic,
  8/16 even with a model applying. **A bad diff is WORSE than no diff**: a worker handed
  a flawed "exact" patch scored *below* the same worker interpreting the spec (8/16 <
  10/20). Do not emit approximate edits.
- **SEARCH/REPLACE with verbatim SEARCH** (copied byte-for-byte from the file Opus just
  read) removes drift entirely → 532/532 clean apply. This is the only sanctioned format.

---

## §0 · The apply-tier gate (NEW — decide before choosing SOLO/SWARM)

After the §1 inventory, ask one added question of the work: **is a node's change
EXPRESSIBLE as localized, verbatim text swaps against files that already exist?**

- **DIFFABLE** — logging/API migrations, signature threading, rename sweeps, config
  edits, mechanical refactors: the change is N independent site-edits with a computable
  before/after. These are the v5.0 apply-tier's target.
- **GENERATIVE** — new files, structural rewrites, algorithm design, anything whose
  output isn't a swap against existing text. These stay on the v4.1 paths (a model
  implements; the apply-tier does not apply).

Print: `APPLY-TIER: <DIFFABLE n=<sites> | GENERATIVE | MIXED c=<diffable>/<generative>>`

MIXED is normal: the CRITICAL/GENERATIVE core (e.g. a shared contract rewrite) is
implemented by Opus as in v4.1; the DIFFABLE fan-out (the dozens of call-site migrations
that depend on it) routes to the apply-tier. This is the same split v4.1 already draws
between the pinned-contract core and its downstream sites — v5.0 just makes the
downstream deterministic instead of a worker swarm.

## §1 · Inventory — unchanged from v4.1

[Read the task and spec/source. COUNT sites, files, read-volume, nodes-by-RISK
(CRITICAL / WORKHORSE / MUNDANE). See v4.1 §1 — carried verbatim.]

## §2 · Scale gate — unchanged from v4.1

[`GATE: SOLO|SWARM — sites=… files=… read≈…K nodes=… mix=C/W/M`, thresholds and
tiebreak per v4.1 §2. The apply-tier does not change WHEN to swarm — it changes HOW the
DIFFABLE portion of a swarm is executed.]

## §3 · SOLO path — unchanged from v4.1

[In-session checklist discipline + §5 gate. If the SOLO job is DIFFABLE and large, the
orchestrator MAY still use the apply-tier (§4.9) on itself: compute the blocks, apply
deterministically, gate — this is where the 3×/4× win shows up even without a swarm.]

## §4 · SWARM path

§4.1–§4.8 are **carried verbatim from v4.1** (plan-as-data, worker grouping, THE MANDATE,
lanes, briefs, landing protocol, the gate, escalation ladder). THE MANDATE still holds:
the orchestrator does not hand-implement GENERATIVE work to save effort. The apply-tier is
not an exception to the mandate — it is a *deterministic* execution of work the
orchestrator has fully computed, which is categorically different from the orchestrator
secretly doing a worker's judgment job.

### §4.9 · The apply-tier (NEW — for the DIFFABLE portion only)

When the plan marks a node/cluster DIFFABLE:

1. **Compute, don't delegate.** The orchestrator (Opus) reads the target files and the
   binding spec and emits one **SEARCH/REPLACE block per site**, in exactly this format:

   ```
   FILE: <path from repo root>
   <<<<<<< SEARCH
   <exact current line(s), copied VERBATIM from the file — byte-for-byte, same indent;
    include enough surrounding lines to be UNIQUE if a bare line repeats>
   =======
   <replacement line(s) per the spec rules>
   >>>>>>> REPLACE
   ```

   The SEARCH text MUST be verbatim from disk — that is the entire fidelity mechanism.
   Approximate SEARCH is a defect worse than no diff (see evidence). This is emitted as
   plan data to the scratch dir (`plan.blocks`), never narrated inline.

2. **Apply deterministically — no worker model.** A stdlib applier: for each block, find
   the SEARCH text in the named file; apply iff it matches **exactly once**. Record
   `applied / nomatch / nonunique` counts. A clean run is `applied == blocks, nomatch=0,
   nonunique=0`. This step costs ~0 tokens and ~0 seconds and is 100% reproducible.

   The applier ships with this skill — do NOT write your own, and do NOT hand the
   blocks to a model to apply. Both defeat the mechanism (see the FORMAT evidence
   above: a model applying a flawed patch scored 8/16, *below* the same model
   interpreting the spec at 10/20).

   ```
   python ~/.claude/tools/orch-apply/apply_blocks.py plan.blocks --root . --json apply.json
   ```

   Windows/PowerShell: `python "$env:USERPROFILE\.claude\tools\orch-apply\apply_blocks.py" ...`

   Exit `0` = every block applied cleanly · `1` = residue to escalate (step 3) ·
   `2` = malformed blocks (fix the emit, do not force it). `--dry-run` reports without
   writing; `--atomic` refuses partial application.

   If the applier is not installed, SAY SO and stop — do not silently fall back to
   in-place editing, which discards the entire speed and cost win this tier exists for.
   Install: `python packages/coding-v5.0/install.py` from the swarmsmith checkout.

3. **Residual → escalate, don't guess.** Any `nomatch` (Opus's SEARCH wasn't verbatim)
   or `nonunique` (insufficient context) block does NOT get force-applied. It is handed
   to a single cheap worker (sonnet) with the block + the file, "apply this one edit;"
   OR bounced back to Opus to re-emit that block with more context. Deterministic-first;
   model only for the residue. (In the validation run the residue was zero.)

4. **Gate as always (§4.7).** The deterministic apply changes nothing about the gate —
   the script, not the block counts, decides done. Verbatim-clean apply is necessary,
   not sufficient: Opus can still mis-RULE a REPLACE (a planning miss), which only the
   oracle/gate catches. The 15→16 gap in early runs was a planning/ scope issue caught
   exactly here.

### §4.9a · Fleet reuse (the scale multiplier)

Because the SEARCH/REPLACE set is data and the apply is deterministic, the SAME computed
diff applies to N repositories/instances at ~0 marginal cost. For fleet-wide mechanical
migrations, Opus computes once; apply runs everywhere. This is the "scale through Opus"
case: the compute is spent on understanding ONCE, not re-litigated per target.

### §4.4′ · Lanes — reframed for v5.0

| tier | v4.1 | v5.0 |
|---|---|---|
| CRITICAL / GENERATIVE core | `opus` worker | `opus` (orchestrator implements, unchanged) |
| DIFFABLE fan-out | `haiku`/`sonnet` worker interprets + applies | **orchestrator computes blocks → deterministic apply** |
| DIFFABLE residue (nomatch/nonunique) | — | one `sonnet` apply, or Opus re-emit |

The worker model tier stops mattering for DIFFABLE work — application is deterministic.
The local lane finding corroborates: a *faithful* diff flipped the local 30B from 0/4 to
5/5 on a slice; where its lane matters at all is only the residue.

## §5 · SOLO gate — unchanged. §6 · Destructive interlock — unchanged (a computed diff
touching auth/money/concurrency/migrations is STILL destructive; it is presented as a
plan with rollback and never auto-applied without human approval).

### §7 · Reconcile & hand off

- Add to the routing table: DIFFABLE nodes with `blocks applied / nomatch / nonunique`
  and any residue escalations.
- **Avoid towering commits.** Each CDG node / DIFFABLE cluster lands as its own local
  candidate commit — a rollback/attribution boundary, not publication — tagged
  `[UNREVIEWED][<node>][<CLASS>] <summary>`. Do NOT accumulate the whole apply-tier
  fan-out into one giant working-tree diff; the apply-tier's per-node data already gives
  the boundaries, so commit along them. No human approval is required to create a local
  candidate commit; approval is still required ONLY before merge to a protected branch,
  push, PR, release, or deploy (§6). In auto-approve/headless mode, leave the tree
  uncommitted per §8 rather than towering it.

§8 · Hygiene — unchanged (commit only with human approval; in auto-approve mode leave the
tree uncommitted).

## Invariants (v4.1 + v5.0)

- All v4.1 invariants hold.
- The apply-tier is ONLY for DIFFABLE nodes; GENERATIVE work is never faked as a diff.
- SEARCH text is verbatim-from-disk or the block is invalid. Approximate diffs are banned.
- Deterministic apply never force-applies a non-unique/no-match block; residue escalates.
- The gate, not the apply counts, is the evidence. A clean apply of a wrong REPLACE is
  still a failure the gate must catch.
- The orchestrator does not hand-implement GENERATIVE work to save effort (THE MANDATE).
- Nothing is pushed, merged, or deployed without human approval.

## Known limits — read before trusting a number

- The whole-skill campaign is at **k=5** and climbing (→10 →25); only the isolated
  mechanism ran k=25. Treat the multipliers as directional. Two fixtures only, both
  `task_class: MIXED`; the large and hygiene fixtures ran at k=3. No pure-generative
  fixture yet.
- **Routing tracks context size, as designed.** v5.0 spawns 0 workers on the ~28K-token
  fixtures — correctly solo, since below the crossover coordination is pure overhead —
  and **11–13 workers** on the 400K-token `bigctx_real`. Both skills went solo on one
  large-fixture run apiece, so task-adaptive routing is not a v5.0 signature. An earlier reading of those 0-spawn counts as a MANDATE violation was **wrong**;
  it generalized from two fixtures that both sit below the swarm threshold. The narrower
  true claim: "behavior identical to v4.1" is false, because v4.1 swarms on the small
  fixtures where v5.0 correctly does not.
- **Big-context cell (k=3, complete):** both arms 3/3. v5.0 $10.10 / 871s; v4.1 $11.00 /
  1118s. Correctness ties at scale — v5.0's edge shrinks to 1.28× wall, 1.09× cost.
- v5.0 runs 34–101 parent turns (p50 55) against a `max_turns: 100` cap on the small
  fixtures where v4.1 runs 12–63 (p50 24). On the large fixture it delegates instead, so that ceiling is not the
  binding constraint it first appeared to be.
- **A mandatory clean phase (§9 in the live variant) measured as a null.** On the
  `arena_cleanup` hygiene fixture at k=3, v4.1+§9 scored 3/3 at +30% cost and +34% wall
  against v4.1 without it — zero correctness gain, and no over-deletion (the oracle's 8
  restraint checks passed for every arm). Caveat: all arms hit the 16/16 ceiling, so the
  fixture had no headroom for §9 to show value. The narrow finding is that on cleanup a
  competent orchestrator already handles unaided, a mandatory phase is pure overhead.
- **Report cost per successful run, never per attempt.** Per-attempt figures rank a skill
  that fails half its runs as competitive. It is not.
- The DIFFABLE/GENERATIVE call is itself a defect surface: mis-labeling a generative node
  as diffable produces bad blocks. The gate is what catches it.
- Opus effort for the emit step: low held 16/16 on scope; high did not improve it. Your
  mileage will vary with task shape.
- Fleet reuse across drifted targets reintroduces nomatch residue at scale — unmeasured
  above single-digit target counts.

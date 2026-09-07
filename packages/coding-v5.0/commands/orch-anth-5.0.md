# /orch-anth-5.0 — v5.0.1 apply-tier (computed-diff · deterministic apply · lane discipline)

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

v4.1 is retired as the default. Its §1–§8 are inlined below, so this file needs no prior
version and ships none — the standalone v4.1 text is kept for rollback in the swarmsmith
repo at `.claude/commands/orchestrate.md` and is deliberately not part of this package. Small fixtures at k=5 (30 cells), large at k=3 (6 cells); ladder continues to
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

**v5.0.1 (2026-09-06) — what changed, and why you should replace v5.0.** The v5.0
edition of this file was NOT self-contained: §1, §2, §3 and §4.1–§4.8 deferred their rules
to an earlier version that does not ship with this package. A model reading it had to
invent the inventory rules, the scale-gate thresholds, the SOLO path and the whole swarm
protocol. Those sections are now present in full. Two further repairs: §7 and
§8 stated contradictory commit rules and now there is exactly one (§7.1), and the applier
is specified by CONTRACT so the skill works whether or not you kept `apply_blocks.py`.
No mechanism changed — §0, §4.9 and §4.9a are the same apply-tier.

## §0 · The apply-tier gate (decide after §1, before choosing SOLO/SWARM)

After the §1 inventory, ask one added question of the work: **is a node's change
EXPRESSIBLE as localized, verbatim text swaps against files that already exist?**

- **DIFFABLE** — logging/API migrations, signature threading, rename sweeps, config edits,
  mechanical refactors: the change is N independent site-edits with a computable
  before/after. These are the apply-tier's target.
- **GENERATIVE** — new files, structural rewrites, algorithm design, anything whose output
  isn't a swap against existing text. A model implements these; the apply-tier does not
  apply.

Print: `APPLY-TIER: <DIFFABLE n=<sites> | GENERATIVE | MIXED c=<diffable>/<generative>>`

MIXED is normal: the CRITICAL/GENERATIVE core (e.g. a shared contract rewrite) is
implemented by a capable worker per §4.4; the DIFFABLE fan-out (the dozens of call-site
migrations that depend on it) routes to the apply-tier. This is the same split §4.2 draws
between the pinned-contract core and its downstream sites — the apply-tier just makes the
downstream deterministic instead of a worker swarm.

## §1 · Inventory (mandatory, before choosing anything)

Read the task and the spec/source. COUNT the real work — do not estimate from the prompt
alone:

- **sites** — individual edit/creation points (grep the call sites; list the stubs)
- **files** — files you must create or modify
- **read volume** — bytes of code/spec that must actually be read (`wc -c`, ÷4 ≈ tokens)
- **nodes** — discrete deliverables, labeled by RISK (not size):
  - **CRITICAL** — shared contracts others import · auth/security · money math ·
    concurrency · migrations · anything DESTRUCTIVE (§6)
  - **WORKHORSE** — contained implementation against a clear spec · trap-dense edits
  - **MUNDANE** — mechanical, fully specified, judgment-light

## §2 · Scale gate (computed — print the verdict, then obey it)

Print one line: `GATE: SOLO|SWARM — sites=<n> files=<n> read≈<n>K nodes=<n> mix=<C/W/M>`

**SWARM** if ANY of:

- sites ≥ 25, or files to create/modify ≥ 12
- nodes ≥ 12 AND ≥ 40% of them are MUNDANE+WORKHORSE (displacement value exists)
- read volume ≥ 150K tokens, or projected work ≥ 60% of the session's turn budget
- the human flagged premium-token pressure

**SOLO** otherwise — that is the measured optimum below these lines, not laziness.

**Tiebreak:** when a count sits within one honest re-count of a line (e.g. 9 vs 10
deliverables), take SOLO — below the wall the cheaper error is under-routing.

These four triggers are the whole gate. They are measured, and they are the only ones —
if you have seen looser values for this skill anywhere, they were a paraphrase and they
were wrong. The node trigger sits at 12 with a SOLO tiebreak *because* two runs of the
same fixture read it as 9 vs 10 deliverables, flipped SOLO→SWARM, and cost **$2.35 vs
$6.69 at equal correctness**. Lowering the trigger re-buys that loss.

**Mid-run re-gate (the insurance a monolithic pass lacks):** while SOLO, if you reach half
the turn budget with less than half the checklist done, or discovered sites exceed 1.5×
your inventory, STOP — write the plan (§4.1) for the REMAINDER and switch to SWARM.

The apply-tier does not change WHEN to swarm — it changes HOW the DIFFABLE portion of the
work is executed.

## §3 · SOLO path

Do the work in-session with the discipline that survives the wall: write the full checklist
first (every site, `file:line`), execute in file-order batches, tick each site off, re-grep
after each batch to catch missed sites, then run the §5 gate.

If the SOLO job is DIFFABLE and large, use the apply-tier (§4.9) on yourself: compute the
blocks, apply deterministically, gate. That is where the speed and cost win shows up even
without a swarm.

## §4 · SWARM path

### §4.1 · Plan-as-data

Create a scratch dir OUTSIDE the repo (`mktemp -d`, or `%TEMP%\orch-<name>`). Write
`plan.json` there before any implementation:

```json
{"mode":"swarm","gate":"GATE line verbatim",
 "workers":[{"id":"W1","nodes":["N01"],"lane":"critical","files":["lib/log.js"],
             "deps":[],"spec":"SPEC.md 2.1-2.4","destructive":false,"apply_tier":false}],
 "batches":[["W1","W2"],["W3"]],
 "gate_cmd":"<the 4.7 script>"}
```

NOTHING non-product is ever written inside the repo — no plan, no scratch, no gate script,
no self-check artifacts. The repo receives product code only.

**Output diet (the orchestrator's tokens are the expensive ones):** plan.json ≤ ~40 lines;
each worker card ≤ ~12 lines beyond the shared preamble; reconciliation ≤ ~30 lines; gate
script focused (contracts + named traps + spot-sites + one integration path, ≤ ~150 lines)
— the per-worker CHECKs already covered the breadth. Do not restate preamble content in
cards; do not narrate between tool calls.

Present the plan (worker table + lanes + batches). If a human is present, pause for
approval; in auto-approve/headless mode print it and proceed (`PLAN-APPROVED: AUTO`).

### §4.2 · Group into workers, collapse tiers

- **One worker per cohesive cluster** — a subsystem/file family of ~3–8 sites or 1–3
  modules — NOT one worker per graded requirement. Target 6–12 workers for a 15–70-site
  job. Never two writers of the same file in the same batch.
- **Group WITHIN a lane, never across lanes.** Folding a MUNDANE node into a mid- or
  top-tier worker silently up-lanes it, and that is where the cheap lane disappears. A
  worker whose nodes are all MUNDANE runs on the cheap lane; promoting it requires a trap
  you can NAME in that worker's own files, named in plan.json.
- **Contract-pinned tier collapse:** a dependency whose interface is pinned by a normative
  spec (exact signatures, values, worked examples) is NOT a batch edge — downstream workers
  code against the pinned contract while the upstream is built in parallel. Only
  physically-shared prerequisites (foundation modules everyone imports, with no pinned spec)
  create a second batch. Most swarms are 1–2 batches; minimize the critical path — two
  correct plans can differ 2x in wall-clock.

### §4.3 · THE MANDATE (hard rule on this path — the three excuses are pre-refuted)

- You do NOT implement GENERATIVE work. Every such worker is dispatched as a subagent.
  "It's quicker to just do this one myself" is the defection measured 28/28 times.
- "Spec fidelity" is preserved by the brief plus the worker reading the spec FROM DISK — not
  by hoarding the work. "It fits in one context" is answered by the gate, which already said
  SWARM. "Per-node briefing cost" is answered by grouping (§4.2) and the shared preamble
  (§4.5).
- Dispatch every ready worker of a batch as parallel spawns in ONE message — all the tool
  calls in the SAME assistant turn (≤ ~10 per message; split larger batches). **Spawning one
  worker, awaiting its result, then spawning the next is a mandate violation, not
  prudence** — an earlier version did exactly that 10/10 times and turned the swarm into a
  relay race. There is nothing to check between same-batch spawns: landing checks (§4.6) run
  after the WHOLE batch has returned, never between spawns.
- Pass the model EXPLICITLY on every spawn — never inherit. Put the worker id and node ids
  in the spawn description (e.g. `"W3 N04-N07 mundane sweep"`) so routing is auditable.
- The orchestrator's own turns are reserved for: inventory, the plan, briefs, computing
  apply-tier blocks, reading reports, landing checks, the gate, escalations, reconciliation.
- **The apply-tier is not an exception to the mandate.** It is deterministic execution of
  work the orchestrator has FULLY computed as verbatim data, which is categorically
  different from quietly doing a worker's judgment job. If you are making judgment calls
  while "applying," you are implementing — dispatch it.

### §4.4 · Lanes (rubric, decided once in the plan)

| capability class | tier | goes there |
|---|---|---|
| CHEAP | MUNDANE | mechanical and fully-ruled, WITH the exact rules and trap warnings in the card |
| WORKHORSE | WORKHORSE | contained implementation; also trap-DENSE mundane clusters |
| CRITICAL | CRITICAL | shared unpinned contracts, auth, money, concurrency, destructive |
| DETERMINISTIC | DIFFABLE fan-out | orchestrator computes blocks → §4.9 applier. No model. |

The capability class is the architecture; which model you map it to is today's mapping.
When a provider re-points a model alias, the mapping changed and **the numbers behind it do
not carry** — re-qualify before trusting them. That is a release event, never a silent
upgrade.

**Demotion rule:** a CRITICAL-labeled node whose behavior is fully pinned by the spec
(signatures + values + worked examples) MAY run one tier down — but NEVER auth, money,
concurrency, or destructive nodes. **Promotion rule:** a mundane cluster dense with
anti-mechanical traps runs one tier up.

### §4.5 · Briefs (cache-shaped; pointers, not pastes)

Assemble ONE shared preamble, byte-identical across every spawn of the run (identical
prefixes are prompt-cache hits — the swarm pays for it once):

```
Repo root = your working directory. SPEC.md is the binding contract — READ the
sections named in your card FROM DISK; they are normative, never paraphrased here.
Global constraints: <the task's own rules: stdlib-only, no new files outside X, ...>
Self-check before reporting, with all scratch files OUTSIDE the repo (system temp).
Report EXACTLY:
STATUS: DONE | BLOCKED(<question>)
FILES: <touched>
CHECK: <command> -> <result, 1 line>
NOTES: <=3 lines
If any instruction cannot be applied exactly as written: STATUS: BLOCKED. Never guess.
```

Then a per-worker card: worker id · OWNED files (exact list — touch nothing else) · spec
sections BY REFERENCE · the byte-exact rules and trap warnings that bite (these are the only
pasted lines — error templates, orderings, "must NOT change" items) · upstream state
("contracts.py is FINAL on disk — import it, never modify") · done-looks-like · the
self-check command to run.

### §4.6 · Landing protocol (reports are claims)

After the WHOLE batch returns (all spawns of the dispatch message — never between spawns):
run `git status --porcelain` plus `git diff --name-only` — any changed file outside the
union of dispatched OWNED lists is reverted and the owner re-briefed. Spot-check each worker
with its own CHECK command or a 1-line import/run probe. A BLOCKED report gets an answer
(from spec/plan), then a fresh spawn, same lane. Never accept a green self-report as the
gate — in testing a correct diff arrived under a wrong report, and only the script told the
truth.

### §4.7 · The gate (orchestrator-owned, deterministic)

Write your OWN gate script in the scratch dir — worked examples from the spec made
executable, one end-to-end integration path, the anti-regression traps ("must not change"
items verified verbatim), and the scope sweep. **Exit code decides.** Non-zero blocks: fix
via §4.8 and re-run. LLM review is optional and never substitutes.

**The gate is not answerable to the implementation.** A failing gate means the code is wrong
until you produce independent evidence that the CHECK ITSELF is malformed — the
implementation disagreeing with the gate is never that evidence. If the gate is genuinely
broken, or cannot observe the behavior the spec promises, stop and say so; do not weaken it
and declare a pass.

### §4.8 · Escalation ladder (evidence travels, work doesn't restart)

Per failing worker: (1) fresh spawn, SAME lane, with the gate failure plus the current diff
of its owned files pasted in; (2) one lane up, same evidence; (3) `LADDER_EXHAUSTED` — the
orchestrator repairs the minimal failing diff in-session and logs it in reconciliation. Hard
cap: 3 attempts per worker, then stop and report to the human.

### §4.9 · The apply-tier (for the DIFFABLE portion only)

When the plan marks a node or cluster DIFFABLE:

1. **Compute, don't delegate.** The orchestrator reads the target files and the binding spec
   and emits one **SEARCH/REPLACE block per site**, in exactly this format:

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
   Approximate SEARCH is a defect worse than no diff: measured, a worker handed a lossy
   "exact" patch scored BELOW the same worker reading the spec. Emit this as plan data to
   the scratch dir (`plan.blocks`), never narrated inline.

2. **Apply deterministically — no worker model.** Run an applier meeting this contract:

   - A block applies **iff** its SEARCH text is found **exactly once** in the current
     in-memory state of the file. Zero matches → `nomatch`. Two or more → `nonunique`.
   - Non-matching blocks are **NEVER** force-applied, fuzzed, or eyeballed into place.
   - Blocks for one file apply sequentially against the evolving in-memory text (a later
     block sees earlier blocks' results); the file is written once, at the end.
   - Line endings are preserved. Try an exact byte match first; count an EOL-normalized
     match separately so CRLF/LF drift stays visible rather than hidden.
   - Report `applied / nomatch / nonunique` counts and per-block residue.
   - Support an `--atomic` mode that refuses partial application (§4.9a needs it).

   A clean run is `applied == blocks, nomatch=0, nonunique=0`. This step costs ~0 tokens and
   ~0 seconds and is 100% reproducible.

   **Implementation.** `apply_blocks.py` ships next to this skill and already meets the
   contract — use it rather than re-implementing. If you do not have it, write a short
   stdlib script to the contract above in the SCRATCH dir, never in the repo. The contract
   is normative; the file is a convenience.

3. **Residue → escalate, don't guess.** Any `nomatch` (your SEARCH wasn't verbatim) or
   `nonunique` (insufficient context) block does NOT get force-applied. Either re-emit that
   block yourself with more surrounding context, or hand the single block plus the file to
   one cheap worker: "apply this one edit." Deterministic-first; model only for the residue.

4. **Gate as always (§4.7).** The deterministic apply changes nothing about the gate — the
   script, not the block counts, decides done. A verbatim-clean apply is necessary, not
   sufficient: you can still compute a WRONG replacement (a planning miss), which only the
   gate catches.

### §4.9a · Fleet reuse (the scale multiplier)

Because the SEARCH/REPLACE set is data and the apply is deterministic, the SAME computed
diff applies to N repositories or instances at ~0 marginal cost. Compute once; apply
everywhere. The compute is spent on understanding ONCE, not re-litigated per target.

**A fleet needs its own policy, because per-target success does not imply fleet success.**
93 of 100 clean with 7 residue is not "93% done" — it is a fleet running two versions.
Declare the policy in plan.json before applying:

- `FLEET_POLICY: ATOMIC` — every target must apply clean or NONE are kept; any residue rolls
  the whole fleet back. **This is the default, and it is mandatory** for anything touching a
  shared contract, a wire format, auth, money, or a migration.
- `FLEET_POLICY: PARTIAL_ALLOWED` — clean targets are kept and residue targets are
  QUARANTINED: named explicitly in reconciliation, with the resume condition. Permitted only
  for independent, non-contract edits.

Print `FLEET: <policy> targets=<n> clean=<n> residue=<n> quarantined=<list|NONE>`. A fleet
run with unreported residue is a failed run.

## §5 · SOLO gate

Same as §4.7 — the script, not your eyes, decides done. Run it before declaring, and the
same "the gate is not answerable to the implementation" rule applies. If there is no
deterministic check, write one before declaring the work finished.

## §6 · Destructive interlock

DESTRUCTIVE = schema/data migrations, data deletion or movement, git history rewrites or
force-push, deploy/infra mutation, secret or auth-provider changes — anything irreversible
outside the working tree. Rules, regardless of path:

- never routed below the CRITICAL lane; the worker returns PLAN plus exact commands plus
  diff plus rollback — it does not execute;
- you verify the rollback actually restores state before presenting;
- a live human approves execution. In auto-approve/headless mode the irreversible step is
  NOT executed: mark it `DEFERRED-DESTRUCTIVE` with the ready-to-run plan.

A computed diff touching auth, money, concurrency or migrations is STILL destructive. The
apply-tier does not launder it: it is presented as a plan with rollback and never
auto-applied.

## §7 · Reconcile and hand off

- **Requirement matrix:** every spec item → IMPLEMENTED / PARTIAL / DEFERRED / SCOPE-CREEP,
  with file refs.
- **Routing table:** planned vs ACTUAL spawns (worker · lane · model · attempts) plus any
  `LADDER_EXHAUSTED` or `DEFERRED-DESTRUCTIVE` events. Planned not equal to actual must be
  explained. DIFFABLE nodes carry `blocks applied / nomatch / nonunique` and any residue
  escalations.
- **Gate evidence:** the script's final output tail.

### §7.1 · Commit policy — ONE rule, stated once, nowhere else

The boundary is **publication**, not branch name:

| action | approval |
|---|---|
| local candidate commit (not pushed) | **none required**, unless §6 applies |
| push · PR · merge to a shared branch · release · deploy | **human approval, always** |
| auto-approve / headless mode | **no commits at all** — leave the tree uncommitted |

**Avoid towering commits.** Each node or DIFFABLE cluster lands as its own local candidate
commit — a rollback and attribution boundary, not publication — tagged
`[UNREVIEWED][<node>][<CLASS>] <summary>`. Do NOT accumulate a whole fan-out into one giant
working-tree diff; the plan's per-node data already gives you the boundaries, so commit along
them.

If any other section of this file appears to state a different commit rule, this table wins
and the other section is a defect — report it.

## §8 · Hygiene and optional add-ons

Cleanliness the core already enforces by construction: nothing non-product ever enters the
repo; every landing runs the scope sweep and reverts strays; SCOPE-CREEP is a named
reconciliation state. Beyond that, after the gate passes and before handoff, you MAY add
(interactively ask; pre-authorized runs note it in reconciliation):

- **Hygiene sweep (deterministic-first):** run the repo's own tooling when present (ruff /
  eslint / knip / vulture / tsc-unused ...) on the changed surface; what tooling can't see
  (orphaned files, dead branches, stale docs touched by this change) goes to ONE cheap worker
  scoped to THE DIFF ONLY — never a whole-repo crusade mid-task.
- **LLM review:** optional second read for hygiene, architecture, or requirement-fit — never
  the correctness gate (LLM reviewers hallucinate exactly where the deterministic gate
  doesn't).
- **Security — NOT optional:** any diff touching auth, sessions, input handling, or secrets
  gets a security read before handoff.

There is **no mandatory clean phase.** A cleanup pass measured as a null on the one fixture
that tested it, and that fixture had no headroom, so the honest state is unmeasured. Run
cleanup deliberately when you have a REASON (an untraced rename or signature migration, a
run that removed or commented out code, a repo with known half-migrated state) — and when
you do, the ordering is **gate → clean → re-gate**, because cleanup deletes code and the
gate that ran before the deletion has verified nothing.

Commit behavior in this section is governed by §7.1. This section states no commit rule.

## Invariants

- **This file is complete.** No rule this skill enforces lives in a document you were not
  given. A cross-reference you cannot resolve is a defect to report, never a gap to fill by
  inference.
- One writer per file per batch. Specs are read from disk by whoever implements.
- Worker reports are claims; the gate is the only evidence. A failing implementation never
  grants authority to demote the gate.
- Nothing non-product inside the repo, ever.
- Max 3 attempts per worker; the human is the fourth tier.
- The apply-tier is ONLY for DIFFABLE nodes; GENERATIVE work is never faked as a diff.
- SEARCH text is verbatim-from-disk or the block is invalid. Approximate diffs are banned.
- Deterministic apply never force-applies a non-unique or no-match block; residue escalates.
- The gate, not the apply counts, is the evidence. A clean apply of a wrong REPLACE is still
  a failure the gate must catch.
- A fleet apply declares FLEET_POLICY before it runs; ATOMIC is the default.
- §7.1 is the only commit rule in this file. Nothing is pushed, merged, or deployed without
  human approval.
- The orchestrator does not hand-implement GENERATIVE work to save effort (THE MANDATE).
- The capability class is the architecture; the model behind it is a mapping. Re-pointing an
  alias invalidates the numbers, not the algorithm.
- Report cost per SUCCESSFUL run, never per attempt. Per-attempt figures rank skills that
  fail half their runs as competitive; they are not.

## Known limits — read before trusting a number

- **Every number above was measured on the v5.0 edition of this file, not on this one.**
  That edition deferred §1, §2 (the scale gate and all four of its thresholds), §3 and
  §4.1–§4.8 to a v4.1 that the benchmark harness never injected and that shipped in no
  package — so the measured runs had a model improvising the inventory rules, the gate
  numbers and the swarm protocol. v5.0.1 states them. **The crown is therefore inherited,
  not re-earned:** stating the rules may beat inventing them, or the added length may
  crowd out the apply-tier that earns the win. The head-to-head that settles it is
  registered and unrun. Full disclosure: FINDINGS.md §4.12.
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
- **A mandatory clean phase (section 9 of the internal variant, not a section of this
  file) measured as a null.** On the
  `arena_cleanup` hygiene fixture at k=3, v4.1 plus that phase scored 3/3 at +30% cost and +34% wall
  against v4.1 without it — zero correctness gain, and no over-deletion (the oracle's 8
  restraint checks passed for every arm). Caveat: all arms hit the 16/16 ceiling, so the
  fixture had no headroom for it to show value. The narrow finding is that on cleanup a
  competent orchestrator already handles unaided, a mandatory phase is pure overhead.
- **Report cost per successful run, never per attempt.** Per-attempt figures rank a skill
  that fails half its runs as competitive. It is not.
- The DIFFABLE/GENERATIVE call is itself a defect surface: mis-labeling a generative node
  as diffable produces bad blocks. The gate is what catches it.
- Opus effort for the emit step: low held 16/16 on scope; high did not improve it. Your
  mileage will vary with task shape.
- Fleet reuse across drifted targets reintroduces nomatch residue at scale — unmeasured
  above single-digit target counts.

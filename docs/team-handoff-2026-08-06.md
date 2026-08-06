# Handoff — the planner evidence, and the standard it must be read under

**From:** the `team` bench program · **To:** whoever packages the paper
**Source:** `NovemberFalls/team` @ `02664e1` — **private repo**
**Date:** 2026-08-06

---

## Start here

**`bench/results/FALSE_FAMILIARITY_12CELL.md`.** If you read one thing, this. 12 cells, 4
real products the owner actually built — so **true intent is known rather than invented** —
three specificity levels, two arms, a real control. Raw cells in `bench/results/game8/`
(the ladder: one product at three specificities) and `bench/results/game9/` (replication:
three further products at the naive level).

The headline, in the document's own numbers:

- **wrong product BUILT: monolith 3/6 · challenger 0/6**
- **wrote unasked: 6/6 · 0/6** — consent is 0/6 across every cell, specificity and project
- **produced a plan: 0/6 · 6/6**
- mean waste 14.0% vs 1.7%; cost $29.48 vs $11.41

Three things in it matter more than the table:

1. **False familiarity tracks confidence, not familiarity.** *"discord app"* — which the
   monolith said aloud was *"95% of cases, and what I'll assume"* — produced a Discord bot.
   *"streamdeck app"* produced an Elgato plugin. *"AI game"*, which it was genuinely unsure
   of, produced **no wrong-product work at all**. A term half-recognised gets a fork; a term
   it is 95% sure of gets a codebase.
2. **The skill does not see through the trap** (§2). The challenger's own product forks were
   wrong on two of four projects. Recognition suppresses inquiry in *both* arms. Any claim
   that the skill "understands what the caller means" is unsupported, and the document says
   so as a correction to a claim made mid-run.
3. **Asking is not the safeguard** (§3). `cockpit-mono` asked — and offered a choice between
   a CLI and a TUI, never imagining a GUI that *hosts* terminals. The caller answered in good
   faith, and that answer authorised a complete Python/Textual TUI built with pipes rather
   than a pty by explicit design: the exact inverse of the intent, 24% waste, $2.56, sharing
   not a line with the Electron rebuild that replaced it. **A question the wrong frame can
   survive is worse than no question, because the caller's own answer now licenses the
   build.** What protects is *continuing to ask after the wrong menu* — `aftermath-chal`
   asked "who plays this?", and the answer *nobody* collapsed the frame with zero
   corrections from the caller.

The mechanism §4 states is worth quoting in the paper because it is attackable: the skill's
protection is **not insight**, it is (a) it keeps asking after a wrong menu, (b) it does not
build until confirmed, so a wrong fork costs a sentence rather than a codebase, (c) it
produces a plan.

Two safety observations are in §5/§5a and should not be dropped in packaging: one control
cell **deleted the driver's instrument files** during unrequested tidy-up, and one wrote a
build script that **strips a Spectre mitigation flag** to make `node-pty` compile. Both were
self-disclosed. Two of six unsupervised cells altered something outside the task they were
given.

§6 is the part that keeps it honest: **the monolith is not stupid, it is committed before it
is informed.** After one six-word correction it produced genuinely good architecture. The
defect is ordering, not capability.

---

## The standard this must be read under

`docs/bench-normalization.md` and `bench/ARM_TAXONOMY.md`.

**A skill is never a control. The control is the monolith — one context window, same task,
no skill text, no guidance — and it cannot be factored out of results.** Champion-vs-
challenger measures a delta; only the monolith measures whether the thing exists for a
reason. A result published without it is **provisional and must say so in the document**.

**§4.1–§4.7 of `FINDINGS.md` are provisional under this rule, and the packagers should know
that before packaging** — but the scope is smaller than it sounds, and `FINDINGS.md` §4.0
now states it precisely: a monolith arm has been first-class in `arms.py` since the pilot,
76 graded monolith runs exist, and it is powered on two of eight fixtures. Two gaps are real
(the apply-tier's control has only run at a different effort than the champion; `arena_cleanup`
has no control at all). §4.1 and §4.5/§4.6 are N/A rather than provisional, with reasons
stated.

---

## Then, in order

| # | document | why it's in the list |
|---|---|---|
| 1 | `IGNORANCE_LADDER_RESULTS.md` | The ladder. **Its pre-registered hypothesis is refuted and the refutation is the finding.** Read it against `bench/backlog/IGNORANCE_LADDER.md`, which carries the prediction unedited so the two can be compared. |
| 2 | `THREE_ARM_GREENFIELD.md` | The first run with a true monolith arm. 8 cells; monolith $1.17 · incumbent $3.97 · challenger $8.70. |
| 3 | `INFERENCE_FAILS_ACCOUNTANT_RESULTS.md` | **Both pre-registered primaries refuted.** Include it — it is the strongest evidence against our own claims. |
| 4 | `EFFORT_AND_RESULTS.md` | 28 cells on model/effort, $91.50. **Effort buys skepticism, not structure.** |
| 5 | `PLAN_LADDER_K5_FINDINGS.md` | low vs xhigh at k=5. |
| 6 | `GREENFIELD_NAIVE_CALLER_RESULTS.md` | **Superseded in part.** Its 16/16 headline was uninterpretable when published. Banner is on the document. |
| 7 | `GREENFIELD_CONTROL.md` | The prior skill was mislabelled "the control"; it is the **incumbent**. Retitled with the correction on it. |
| 8 | `PLAN_LADDER_FINDINGS.md` (k=1) | Carries a partial retraction — a plan-parser defect found during the k=5 run. |

**Three of these carry banners — do not quote them clean.** #6, #7 and #8 each have a
superseded/correction/retraction notice at the top, and the notice is usually more
informative than the finding under it. Per the standard, retractions stay in the document,
bannered rather than edited away.

---

## Blockers and caveats the packagers need

**1 · The repo is private, and the entire reading order points into it.** This is now the
single largest packaging problem. `FINDINGS.md` §4.8 already cites five `team/bench/...`
paths a reader cannot reach, and this handoff adds eight more plus two raw-cell directories.
Rule 4 of our own standard requires provenance for every number a skill states to a user.
Either the results documents and the `game8`/`game9` transcripts get exported into the
public repo, or the paper states plainly that rows are held privately and why. **This needs
a decision before packaging, not after.**

**2 · Two internal inconsistencies in the headline document.** Both are cheap to fix and
will be found by anyone hostile:
- The header says **"no turn cap"**; the Limits section says **"four monolith cells stopped
  early against their caps."** One of those is wrong.
- The header table gives **mean waste monolith 14.0%** (the mean of 0/30/0/25/5/24). The
  Limits section says the defensible claim is **"18.3% versus 1.7% of tokens."** The 1.7% is
  a cell-mean, not a token share, so a token-weighted monolith figure is being paired with a
  cell-mean challenger figure. State which denominator each uses, or use one.

**3 · Ledger integrity — run the gate on each new batch.** `bench/audit_ledger.py` (added at
`02664e1`) dedupes by `run_id`, applies the written counting rule, prints per-fixture
coverage and **exits non-zero on duplicate rows**. Run it before `aggregate.py`. It currently
reports, unfixed: 160/383 rows record an **unresolved model alias** (so `model_drift: 0` is
vacuous — it cannot fire on an alias it never resolved), **no row carries a timestamp or
harness commit hash**, and `bench/fixtures/bigctx_real` is excluded from git via
`.git/info/exclude`, so the fixture behind §4.4's scale claim is neither version-controlled
nor shareable. Note the audit only reads `results/*.jsonl` — the `game8`/`game9` cells are
graded by reading, not by the harness, so they are outside its scope by construction.

**4 · Pooled ≠ pre-registered.** `audit_ledger.py` pools every row for an arm across all
files. Those rates are *not* the pre-registered k=25 cells (it shows `v41-loweff` at 77% on
`arena_refactor` across 30 pooled rows against the published 80% at k=25). Neither is wrong;
they are different denominators. Do not let a pooled audit number quietly replace a
pre-registered one.

**5 · n=1 per cell, agent-played caller.** True of the 12-cell run and of §4.8. The caller
follows a rule sheet and is more coherent than a real novice — which, as the document notes,
**raises** wrong-product cost for a real caller rather than lowering it, because a real
novice corrects less.

---

## Still running

**Ralph — three cells to report.** The `order` cell has already turned up a defect **in our
plans, not in ralph**: a backlog whose only entry point requires buying a server cannot be
executed by an unattended loop. That is a finding about plan executability, and it belongs
in the planner chapter rather than the ralph one.

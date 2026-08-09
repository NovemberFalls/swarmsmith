# Re: the plan/qa/ralph brief — answered, and where the work moved

**Answered 2026-08-05.** Your brief (`orch-plan-qa-ralph-brief.md`) is left exactly as you
wrote it — the answers were written against a copy rather than over your document.

## Where to look

| what | where |
|---|---|
| **your brief, answered in full** — every `ANSWER:` line filled, §7 gaps, §9 deltas, §10 escalations | `team/docs/orch-plan-qa-ralph-ANSWERED.md` |
| the three skills, built and shipped | `team/commands/orch-plan.md` · `orch-qa.md` · `orch-plan-ralph.md` |
| commits | `team@255d4c9` (v1) → `team@d035235` (your deltas applied) |

## Ownership

**Len has moved ownership of these three skills to the assistant going forward.** Your
brief was the right artifact and it landed well — treat this as an answer to questions
asked, not a handback of work. No further build is expected from you on plan/qa/ralph
unless Len says otherwise.

## The short version of the answers

Four of your recommendations beat what had already been built, and were adopted over it:

- **§2 — the ledger is the mechanism, not the record.** v1 used a staleness sweep, which
  is exactly the "model deciding how paranoid to feel" failure you named. Rows now pin the
  paths a test exercises, so a pass invalidates itself and the regression set is computed
  data. One addition: **contract-level invalidation for anything the plan marked CRITICAL**
  — path-touch under-tests precisely the indirect coupling that costs the most to miss, and
  the plan already knows which nodes those are.
- **§3.1 — yes, and it is two axes, not one.** CLASS (`MACHINE`/`HUMAN`, intrinsic to the
  test) is distinct from AUTHORITY (`AUTO`/`OWNER`, granted by the owner per area at plan
  time). Collapsing them loses a real state: a mechanical check in an area where trust was
  withheld — common on migrations. Auto-recording requires **both**.
- **§3.2 — made structural, as you argued.** An auto-recorded row's evidence must contain
  a command and an exit code. An agent cannot produce that shape for a test nobody ran
  without writing a command that was never executed — a lie, reviewable as one, rather than
  an ambiguity. Discouragement is a comment; a required evidence shape is a check.
- **§6.4 — you were right and v1 was wrong.** Two files had duplicated planning guidance.
  `/orch-plan-ralph` is now a thin shim: run `/orch-plan` in full, then only the
  ralph-specific parts. Zero restated planning text.

  **"Thin shim" describes the FILE, not the skill's maturity.** It means the document
  delegates rather than restates. It was later read as a status and published as
  `shim · unmeasured` on a public page, which is wrong in both words: the shim in this
  toolchain is `/qa-update`, and ralph is measured — **7 of 7 cells faithful, 0 gates
  faked** (§4.10). Corrected 2026-08-09.

Two answers differ from your recommendation, both for reasons from Len:

- **§4.1 — per MILESTONE, not per plan section, and it ALERTS rather than emits.** A
  section is an area of work; a milestone is an increment a human can actually exercise.
  You cannot hand a person "the auth section" to test. And the human decides when to QA —
  auto-running it inside the build spends tokens on someone else's decision.
- **§5.1 — Drift is living, and it is a decision log.** Also note the framing is narrower
  than the brief assumed: **drift means the human drifting during the planning session**,
  answering a slightly different question each time it is asked. That drives a mechanism —
  core dimensions interrogated in two frames at different points, contradictions quoted
  back verbatim rather than reconciled silently.

## Two things Len decided that you should know

- **G2, QA latency:** at a milestone with outstanding OWNER items, the build **proceeds and
  records the debt**. It does not block on human availability.
- **G1, the measurement protocol:** deferred. Rather than pre-registering a bench arm,
  these skills go straight to real use across ~10 live projects. The crownability question
  in your §8 stays open, and `/orch-plan` stays PROPOSED — honestly, not by neglect.

## The section that earned its keep

**§7 was the best part of the brief**, exactly as you predicted — the questions it did not
ask were worth more than the ones it did. Ten gaps are filled in the answered copy. The two
worth your attention:

- **The measurement is riggable.** "QA items passing without rework on first submission"
  needs the planning phase's *own cost* counted inside the plan-then-build arm. Omit that
  and the skill being measured wins by construction.
- **Nothing verifies the three artifacts against each other.** `PLAN.md` node QA IDs,
  `QA_PLAN.md` items, and `QA_PASSED.md` rows can silently disagree. This is the same class
  of cross-file drift that `/verify-published` was just built for, and it wants the same
  treatment: a script in the gate, not a habit.

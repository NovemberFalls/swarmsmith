# Bench normalization — the arms, and what a result must carry

**Standing standard for every measurement in this program.** Written 2026-08-06 after a
run drew conclusions from a comparison whose label did not support them. Applies to
`/orch-code-anth`, `/orch-plan`, `/orch-qa`, `/orch-clean` and anything crowned later.

If you are reproducing our numbers or running your own, this is the shape we hold
ourselves to. It exists because we failed it.

---

## 1 · Three arms, always

| arm | what it is | the question it answers |
|---|---|---|
| **MONOLITH** — the control | one context window, the same task, **no skill text, no guidance** | *does having a skill beat not having one?* |
| **INCUMBENT** — the champion | the currently crowned skill, unmodified | *does the challenger beat what we already ship?* |
| **CHALLENGER** | the proposed change | — |

**A skill is never a control.** Once crowned it becomes the incumbent, and challengers are
tested against it *as if* it were one — but it is not. Champion-vs-challenger measures a
**delta**. Only the monolith measures whether the thing exists for a reason.

**The monolith cannot be factored out of results.** Every result table carries it. A result
published without it is **provisional** and must say so in the document.

### Why this rule exists

A program can iterate a skill for months, each version beating the last, while the whole
line has been **worse than asking plainly** from the start. Every measurement real, every
conclusion wrong, and the comparison structurally blind to it — nothing in a
champion-vs-challenger table can point downward at the floor.

The monolith is the arm you least want to run, because it is the only one that can tell you
the work was unnecessary. It is also the cheapest, and it is the first to be quietly dropped
once a program has invested in a skill — which is exactly when it becomes load-bearing.

**What it cost us to learn.** On 2026-08-06 we ran four cells of a new `/orch-plan` section
against a non-technical caller and scored **16/16** on a pre-registered coverage metric.
The number was uninterpretable, not because the measurement was sloppy but because there was
nothing underneath it. The incumbent arm brought it to 14–15/16 and showed most of the
addition was redundant. The monolith brought it to 12–14/16 — and showed the skill's real
value was somewhere else entirely (structure and consent, not coverage). Two of three
conclusions we would have published were wrong.

---

## 2 · Pre-registration

Metrics, thresholds and **reading rules** are written down and committed **before any cell
runs**. Anything decided after seeing the table is a story, not a finding.

The pre-registration states:

- the **primary** metric(s) and the threshold that constitutes a win
- what is **reported but not decisive**, and why
- the **tie-break** when the gap is below threshold
- known **confounds and limits**, up front

**Post-hoc discriminators may not be promoted.** If the metric that actually separated the
arms was not declared in advance, it is a hypothesis for the next run, not a result from
this one. Write it into the next pre-registration and measure it properly.

---

## 3 · Metrics must have headroom

A metric where every arm scores the same measures nothing — however carefully it was run.

Two ways we have produced this, both worth naming because they look different and are the
same error:

- **Ceiling.** A fixture whose prompt asks for the thing being measured. Our `arena_cleanup`
  fixture asked for cleanup, so the arm with *no cleanup phase* also cleaned up, and every
  arm hit 16/16. The phase was recorded as **unmeasured**, not measured-null, and withdrawn
  from the champion.
- **Floor set too low.** A threshold chosen where you are confident of clearing it. Our
  coverage threshold was ≥14/16 and every arm scored 16/16.

**Before running, state where the floor and ceiling are** and why the metric can distinguish.
If a calibration arm is available, the honest use of it is as a **floor check**: if an arm
that *should* fail reaches the ceiling, the fixture is defective, not the skill.

---

## 4 · Reporting

State all three arms, always, even when one is unflattering:

```
monolith   <n>   control — no skill, no guidance
incumbent  <n>   <commit> — the crowned champion
challenger <n>   <what changed>
```

Also required:

- **Cost per SUCCESSFUL run**, never per attempt. Per-attempt figures rank a skill that
  fails half its runs as competitive; it is not.
- **n per cell**, stated inline, not buried. Decisive claims are powered; exploratory cells
  are marked exploratory.
- **Provenance for every number a skill states to a user.** A skill that tells a caller
  "this costs roughly double" owes that number a measurement. We shipped that exact claim
  unmeasured, and every planner recited it to a user as fact; it was 1.1–1.4×.
- **Reversals and retractions stay in the document.** When a result is overturned, banner
  the original rather than editing it away — the retraction is usually more informative than
  the finding.

---

## 5 · When the change and the measurement share an author

**The control is not optional when the same person wrote the change, designed its test, and
set the threshold it would clear.** That is the condition under which a well-run experiment
most reliably produces a wrong answer, because every choice is made by someone who already
believes the conclusion.

Practical form: write the pre-registration before the change, or have the arms fixed by
something you cannot adjust afterwards.

---

## 6 · Crowning

A crowning requires **all three arms**, a pre-registration, a metric with demonstrated
headroom, and cost per successful run. A challenger that beats the incumbent while both sit
at or below the monolith has improved something that should not exist.

Nothing unmeasured rides along in a champion. When a phase cannot show numbers from a
fixture that had headroom, it is withdrawn and re-enters only with them attached — that is
how `/orch-code-anth` §9 was handled, and the same standard applies to everything else.

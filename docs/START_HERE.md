# START HERE — what to read, in what order

You have 3 days, ~1 hour each, one attempt. There is more material here than
that. **This is the list. Ignore everything not on it.**

## Day 1 — OOP from scratch (60 min)

Read **`C_OOP_FROM_SCRATCH.pdf`**, typing every example into a REPL.

- Sections 1–5 (~25 min): why classes exist, `__init__`, `self`, methods,
  instance vs. class attributes, `__repr__`
- Sections 6–7 (~20 min): properties and dataclasses — the two things the
  assessment's given code will be full of
- Section 9 (~5 min): how it all assembles into the pattern you'll use
- Section 10 (~10 min): exercises A, B, C

Skip section 8 (inheritance) if you're short on time; you only need to
recognize it, not write it.

## Day 2 — The format (60 min)

Read **`A_ICF_PLAYBOOK.pdf`** (~25 min). This is the highest-value document
here. It's built from CodeSignal's own technical brief: the per-level
expectations, what's explicitly excluded, and — critically — the two patterns
that Level 3 and Level 4 almost always take.

Then memorize the Level 1 skeleton in section 3 by **writing it from scratch,
twice, without looking** (~20 min). Not to reproduce it verbatim in the test,
but so the shape is automatic when the clock starts.

Then read the domain archetype table in section 6 (~10 min) so no domain
feels unfamiliar.

## Day 3 — One timed mock (60 min)

**`mock_oa_infer/`** — the LLM inference engine, written in authentic ICF
house style. Read `README.md`, then `tests.py`, then implement in
`engine.py`. Run `python tests.py` often.

Give yourself 50 minutes, then spend 10 reviewing against
`solution/engine_solution.py` — which is written *as* the playbook skeleton,
so you can see the pattern working.

This matches both the format CodeSignal documents *and* the domain your
cohort reported, so it's the single best use of the hour.

### If you find a spare hour

**`mock_oa_kv/`** — the in-memory database, same ICF structure, different
domain. Doing two domains in the same format is what stops you pattern-
matching on surface details.

**`mock_oa/`** (the original inference mock) is function-based rather than
class-based, so it drills the domain but not the ICF shape. Lowest priority.

---

## Check your invite email

Sources disagree on the format for **your specific track**. The 4-level,
200–600 scale is documented for CodeSignal's standard ICF and for Anthropic's
new-grad SWE assessment. But at least two sources report that the Research /
AI Safety Fellows tracks use a *different* configuration — possibly scored out
of 1,000, possibly 6 parts rather than 4.

Your invite email is the only authority. Confirm the level count, the scale,
and the time limit before test day so nothing surprises you on the opening
screen. The preparation is the same either way — only the pacing changes.

## Reference — use when stuck, don't read cover to cover

- **`2_python_syntax_reference.pdf`** — look up syntax you've forgotten.
  Section 10 (sorting with tie-breaks) is worth 10 minutes on its own if you
  have them.
- **`day1_drills.py`** — run `python day1_drills.py`; do c9 and c10 after
  Day 1, the rest only if you have spare time.
- **`4_inference_engine_primer.pdf`** — only if your assessment turns out to
  be inference-themed, or for the final-round Colab interview later.
- **`mock_oa/`** — the inference-engine mock. A second practice run if you
  find extra time.

## Skip entirely

`3_oop_refresher.pdf` (superseded by the from-scratch version),
`7_study_plan_7_days.pdf`, `8_python_quick_refresher.pdf`,
`1_crash_plan_3_days.pdf`, `9_session_next_2_hours.pdf` — all earlier drafts
of the plan you're now holding.

---

## On test day

1. Read the whole problem and **all visible tests** before writing anything.
   Eight minutes, no code.
2. Sketch your record fields and class skeleton. Give every internal method a
   timestamp parameter even if Level 1 doesn't use it.
3. Level 1 fast, then **submit** — partial credit is per test passed, and an
   unsubmitted correct method scores zero.
4. Public methods delegate to internals. Never duplicate logic between
   `get()` and `get_at()`.
5. Log every mutation. Level 4 will probably want to reconstruct past state.
6. Never change a method signature the tests already call.
7. If Level 3 hurts at minute 60, stop and make sure 1–2 are fully green.
   Complete lower levels beat partial higher ones.
8. If panic hits: 60 seconds of slow breathing, then write one sentence
   describing what the current level actually asks for before touching the
   keyboard.

Sleep the night before matters more than a fourth hour of prep.

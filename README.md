# Python Quick Refresher & Systems-OA Prep

Study materials for relearning Python fast and preparing for CodeSignal-style
**systems coding assessments** — the format where you're handed a pre-built
codebase, a terse README, and asked to extend a stateful system across
escalating levels.

Built originally to prep for an LLM-inference-engine assessment, but the
Python and OOP material stands on its own.

## Contents

| Path | What it is |
|---|---|
| `docs/python_syntax_reference.md` | Complete Python syntax refresher — 20 sections, from numbers to classes, with a traps list and complexity table |
| `docs/refresher_day2_oop.md` | Object-oriented Python: classes, dunders, properties, dataclasses, plus a "read an unfamiliar codebase fast" drill |
| `docs/inference_engine_primer.md` | LLM inference engines from scratch: prefill/decode, KV cache, batching, scheduling, load balancing |
| `docs/crash_plan_3_days.md` | 3-day, 1-hour-per-day plan |
| `docs/session_next_2_hours.md` | A single guided 2-hour session with external links |
| `docs/study_plan_7_days.md` | Longer 7-day version |
| `drills/day1_drills.py` | 10 fill-in-the-blank exercises with a self-grading runner |
| `mock_oa/` | A full mock assessment: 4 levels, 800 points, pre-built classes, grader |
| `pdf/` | Everything above, typeset as PDFs |

## Quick start

```bash
# Drills — fill in the TODOs, then:
python drills/day1_drills.py

# Mock assessment — read mock_oa/README.md first, implement in scheduler.py:
cd mock_oa && python tests.py

# Verify the reference solution scores 800/800:
cd mock_oa && python tests.py --solution
```

Requires Python 3.9+. No dependencies.

## The mock assessment

`mock_oa/` simulates the real thing, including its frustrations:

- **Level 1** (200 pts) — sequential worker, FIFO
- **Level 2** (200 pts) — continuous batching under a memory limit
- **Level 3** (200 pts) — load balancing across workers
- **Level 4** (200 pts) — priority scheduling with preemption

It deliberately includes a README whose example contradicts the code, strict
tick-ordering semantics, and a level that invalidates an assumption from an
earlier level. Read `SPOILERS.md` **only after** attempting it.

## Roadmap

- [ ] Static site (GitHub Pages) for the Python refresher
- [ ] Searchable, sectioned HTML version of the syntax reference
- [ ] Interactive drills in-browser (Pyodide)
- [ ] More mock problems in other domains (in-memory DB, rate limiter, job scheduler)

## License

MIT — see `LICENSE`.

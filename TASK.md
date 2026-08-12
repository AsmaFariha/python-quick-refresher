# TASK.md — instructions for Claude Code

**You are being asked to publish this repository to GitHub.** Everything you
need is in this file. Read it fully, then execute Part 1. Do not start Part 2
unless the user explicitly asks for it.

---

## Context: what this repository is

Study materials for relearning Python quickly and practicing CodeSignal-style
systems coding assessments. The owner is preparing for a technical assessment
and wants this published so it can later become a website.

```
.
├── README.md                  Project overview (already written)
├── GITHUB_SETUP.md            Publishing + website roadmap (already written)
├── TASK.md                    This file
├── LICENSE                    MIT
├── .gitignore
├── .github/workflows/tests.yml    CI: runs the two verification commands below
├── docs/                      Markdown study material (7 files)
│   ├── python_syntax_reference.md     20-section Python syntax refresher
│   ├── refresher_day2_oop.md          OOP, dataclasses, code-reading drill
│   ├── inference_engine_primer.md     LLM inference concepts
│   ├── crash_plan_3_days.md           Study plans
│   ├── session_next_2_hours.md
│   ├── study_plan_7_days.md
│   └── refresher_day1_python.md
├── drills/
│   ├── day1_drills.py         10 fill-in-the-blank exercises + self-grading runner
│   ├── day1_drills_answers.py Reference answers
│   └── verify_answers.py      CI check: answers satisfy all drill assertions
├── mock_oa/                   A 4-level, 800-point practice assessment
│   ├── README.md              The problem statement
│   ├── engine.py              Pre-built classes (intentionally not to be modified)
│   ├── scheduler.py           Stubs the user fills in
│   ├── tests.py               Grader
│   ├── SPOILERS.md            Post-attempt debrief
│   └── solution/              Reference solution (scores 800/800)
└── pdf/                       Typeset PDFs of the docs
```

The repo already has **one commit**. It needs its author fixed, two files
committed, and a remote.

---

## CRITICAL CONSTRAINTS — read before touching anything

1. **Do not edit, reformat, reword, or "improve" any file in `docs/`,
   `drills/`, or `mock_oa/`.** These are study materials the user is actively
   working through. `mock_oa/tests.py` and `drills/day1_drills.py` contain
   exact hard-coded expected values that were hand-verified; a cleanup pass
   would silently corrupt material the user is about to be graded against.
   Publishing only. No content changes.

2. **Do not fill in the stubs in `mock_oa/scheduler.py`.** They raise
   `NotImplementedError` on purpose — that is the user's exercise. Leaving
   them unimplemented is correct. `python tests.py` scoring 0/800 against
   `scheduler.py` is the expected state.

3. **Do not commit or push anything if the verification step in Part 1
   fails.** Report the failure instead.

4. Ask before doing anything destructive beyond the single deletion listed
   below.

---

## Part 1 — Publish to GitHub

Do these in order.

### Step 1: Clean up

Delete `pdf/test.pdf`. It's a leftover duplicate of
`pdf/2_python_syntax_reference.pdf` from the build process. It's the only
file that should be removed.

### Step 2: Fix commit authorship

The existing commit was created in a sandbox with a placeholder author.

```bash
git config user.name  "<the user's name>"
git config user.email "<the user's GitHub email>"
git commit --amend --reset-author --no-edit
```

Ask the user for the name and email to use if you can't determine them from
their global git config. If a global config already exists and looks correct,
use it.

### Step 3: Verify before publishing

Both commands must pass:

```bash
cd mock_oa && python tests.py --solution     # must print: SCORE: 800/800
cd .. && python drills/verify_answers.py     # must print: 10/10 passing
```

If either fails, **stop** and report what broke. Do not attempt to fix the
test expectations to make them pass — a failure here means something is
genuinely wrong and the user needs to know.

### Step 4: Commit remaining files

`TASK.md` and `GITHUB_SETUP.md` may be untracked. Stage everything and commit:

```bash
git add -A
git commit -m "Add publishing instructions and website roadmap"
```

`.gitignore` already excludes `__pycache__/` and similar — confirm no
`.pyc` files are staged.

### Step 5: Create the remote and push

Repository name: **`python-quick-refresher`**
Visibility: **public**
Default branch: **main**

```bash
gh repo create python-quick-refresher --public --source=. --remote=origin --push
```

If `gh` isn't installed or authenticated, tell the user rather than guessing
at credentials. The manual alternative is documented in `GITHUB_SETUP.md`.

### Step 6: Confirm CI

`.github/workflows/tests.yml` runs on push. Check that the first run passes
(`gh run list`, `gh run watch`). If it fails, diagnose and report — the most
likely cause is a working-directory issue in the workflow, not broken tests,
since Step 3 already verified them locally.

### Step 7: Report back

Give the user the repository URL and the CI status. Keep it brief.

---

## Part 2 — Website (ONLY if the user asks)

Do not start this as part of Part 1. It's a separate piece of work the user
wants to review on its own.

Goal: publish `docs/` as a documentation site using **MkDocs Material**, at
GitHub Pages.

`GITHUB_SETUP.md` contains a ready-to-use `mkdocs.yml` sketch and a deploy
workflow. The work involves:

1. `pip install mkdocs-material`, add `mkdocs.yml` at the repo root.
2. Create `docs/index.md` — a landing page explaining what this is and who
   it's for. Draw from `README.md`; don't duplicate it verbatim.
3. Fix inter-document markdown links so they resolve on the rendered site
   (references like `mock_oa/README.md` and `day1_drills.py` currently assume
   a local filesystem). **This is the one case where editing `docs/` files is
   allowed — but change links only, never prose or code samples.**
4. Verify locally with `mkdocs serve`.
5. Add the Pages deploy workflow and confirm the site builds.

Consider splitting `docs/python_syntax_reference.md` into per-topic pages
(numbers, containers, sorting, classes...) — 20 sections is a lot for one
page — but **ask the user first**, since it changes a file they're studying
from.

Longer-term ideas are in the Roadmap section of `README.md`.

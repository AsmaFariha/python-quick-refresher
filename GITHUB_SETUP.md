# Publishing this to GitHub

The `repo/` folder is already a git repository with one commit, a `.gitignore`,
an MIT `LICENSE`, a `README.md`, and a CI workflow. You just need to push it.

## 1. Create the remote and push (5 minutes)

**Option A — GitHub CLI** (easiest if you have `gh` installed):

```bash
cd path/to/repo
gh auth login                     # once, if you haven't
gh repo create python-quick-refresher --public --source=. --remote=origin --push
```

**Option B — web + git:**

1. Go to <https://github.com/new>, name it `python-quick-refresher`,
   **don't** initialize with a README/license (you already have both).
2. Then:

```bash
cd path/to/repo
git remote add origin https://github.com/<your-username>/python-quick-refresher.git
git branch -M main
git push -u origin main
```

If the commit author looks wrong (it was created in a sandbox), fix it first:

```bash
git config user.name "Asma Fariha Ahmad"
git config user.email "asma.fariha.ahmad@gmail.com"
git commit --amend --reset-author --no-edit
```

## 2. What CI does

`.github/workflows/tests.yml` runs on every push and verifies:

- the mock OA reference solution still scores 800/800
- all 10 drill answers pass

That matters more than it sounds: if you later edit the drills or the mock,
CI catches a broken expected value before you study from something wrong.

## 3. Turning it into a website

You have three realistic paths, cheapest first.

### Path A — GitHub Pages with a Jekyll theme (~15 min, zero build tools)

Your content is already markdown, so this nearly works out of the box.

1. Add a `_config.yml` at the repo root:

   ```yaml
   title: Python Quick Refresher
   description: Relearn Python fast, then practice systems-style coding assessments
   theme: jekyll-theme-cayman        # or minima, hacker, architect
   markdown: kramdown
   ```

2. Repo **Settings → Pages → Source: Deploy from a branch → main / (root)**.
3. Your site appears at `https://<username>.github.io/python-quick-refresher/`.

Caveat: Jekyll serves `README.md` as the index and links between `.md` files
need to become `.html` links. Fine for a first pass.

### Path B — MkDocs Material (~45 min, best result for a docs site)

This is what most Python documentation sites use. Search, dark mode, a real
sidebar, syntax highlighting — all built in, and your files need almost no
changes.

```bash
pip install mkdocs-material
```

`mkdocs.yml` at the repo root:

```yaml
site_name: Python Quick Refresher
theme:
  name: material
  features: [navigation.sections, navigation.top, search.suggest, content.code.copy]
  palette:
    - scheme: default
      toggle: {icon: material/brightness-7, name: Dark mode}
    - scheme: slate
      toggle: {icon: material/brightness-4, name: Light mode}
nav:
  - Home: index.md
  - Python:
      - Syntax Reference: python_syntax_reference.md
      - OOP: refresher_day2_oop.md
  - Systems OA:
      - Inference Engine Primer: inference_engine_primer.md
      - Mock Assessment: mock_oa.md
  - Plans:
      - 2-Hour Session: session_next_2_hours.md
      - 3-Day Crash Plan: crash_plan_3_days.md
      - 7-Day Plan: study_plan_7_days.md
markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - toc: {permalink: true}
```

Point `docs_dir` at your `docs/` folder (the default), add an `index.md`,
then:

```bash
mkdocs serve          # preview at localhost:8000
mkdocs gh-deploy      # builds and pushes to the gh-pages branch
```

Then set **Settings → Pages → Source: gh-pages branch**.

To automate deploys, add a second workflow:

```yaml
name: docs
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

### Path C — Interactive drills in the browser (later)

The genuinely useful version of this site lets people *run* the drills. Use
[Pyodide](https://pyodide.org/) — CPython compiled to WebAssembly — to execute
`day1_drills.py` client-side with no backend:

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>
<script>
  const pyodide = await loadPyodide();
  const result = pyodide.runPython(userCode);
</script>
```

Pair it with [CodeMirror](https://codemirror.net/) for the editor. This is a
weekend project, not an afternoon one — but it's the thing that would make the
site worth visiting rather than just readable.

## 4. Suggested next commits

- `docs/index.md` — a landing page explaining who this is for
- Split `python_syntax_reference.md` into per-topic pages (containers,
  sorting, classes...) once it's on a site; 20 sections is a lot for one page
- Add the "traps" section as a standalone quiz
- More mock problems: in-memory DB with TTL, rate limiter, job scheduler —
  same 4-level structure, different domains

## 5. A note on content

Everything here is your own material and safe to publish. The mock assessment
is an original problem written to imitate a *format*, not a reproduction of
any company's actual assessment — keep it that way if you add more, since
posting real assessment questions violates most companies' terms and this
subreddit's rules too.

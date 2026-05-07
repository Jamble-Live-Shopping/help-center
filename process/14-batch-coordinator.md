# 14, Batch coordinator + reviewer pack

This document is the operating manual for `scripts/run-help-article-batch.py`,
the coordinator that orchestrates 1 to 10 article worktrees through the
factory and produces a single static reviewer pack the human reviewer
can audit in one pass.

The coordinator is **not a writer**. It does not generate article
content, does not call any LLM from Python, and does not auto-publish,
auto-merge, or mark a PR ready. It strictly:

- validates the batch contract (10-article cap, no duplicates),
- prepares isolated worktrees with a worker brief,
- collects validate output and mockup status after the worker has
  written content,
- emits a static HTML reviewer pack and a machine-readable JSON.

## Why a 10-article cap

The cap was raised from 3 to 10 in PR #88, after the PR #84 batch-3
calibration run validated the coordinator end-to-end. The reviewer
pack now relies on three triage signals to stay reviewable at 10:

1. **Top scorecard.** One row per article with the validator counts +
   mockup ratio + audit ratio + status badge. Lets the reviewer
   triage by status colour in seconds.
2. **Manual gates per screen** (PR #88). Each article block opens
   with a table that lists `required_icons` and `review_checks` per
   declared screen, sourced from `flow.yml.mockup_plan.screens`.
   This is what the reviewer scans to decide which articles need a
   close look at the mockups vs. which can be approved on the
   scorecard alone.
3. **Collapsed details.** pt-BR / EN body previews are collapsed by
   default. The reviewer expands only the articles flagged on the
   scorecard or where a manual gate looks suspicious.

Above 10 the format would need a different review pattern (sampled
review or sub-batches). The cap is hardcoded as
`MAX_BATCH_ARTICLES = 10` in `run-help-article-batch.py` and aligned
with `validate-article-batch.py`'s own `MAX_BATCH_SIZE = 10`, so 11+
is rejected at preflight by either layer.

## Per-screen contract (PR #88)

Each entry in `mockup_plan.screens` accepts two new optional fields:

```yaml
mockup_plan:
  screens:
    - name: composer
      purpose: "DM composer with photo + send icons"
      source: ios_required
      required_icons:
        - icon-send
        - icon-camera
      review_checks:
        - icons_match_ios_source
        - labels_match_xcstrings
        - no_invented_ui_state
```

Validator rules (deterministic, no LLM):

- `screen_icon_not_in_html` (HARD FAIL): when `required_icons` is
  non-empty, every icon name must appear in BOTH
  `articles/<slug>/mockup-sources/<screen>__pt-br.html` AND
  `<screen>__en.html` via `alt="<icon>"`,
  `<!-- icon: <icon> -->`, or
  `Assets.xcassets/<icon>.imageset` comment. Defends against the bug
  PR #87 surfaced: invented icons inside a mockup that the global
  `flow.icons_required` rule cannot catch per-screen.
- `screen_review_checks_missing` (SOFT WARN): when
  `source: ios_required` and `review_checks` is empty, nudges the
  worker to record what the reviewer must check. Backward-compatible:
  historical articles that pre-date the contract keep validating
  exit 0.

The validator does NOT enforce the semantic content of
`review_checks`. It is descriptive metadata that the writer-packet
prints to the worker and the reviewer pack surfaces at the top of
each article block.

## Lifecycle

```
       prepare                          review                     cleanup
  ┌──────────────┐                  ┌──────────────┐             ┌──────────┐
  │ batch.yml    │                  │ Claude wrote │             │ list/rm  │
  │ + worktrees  │  → Claude works →│ each article │ → Aymar  →  │ work-    │
  │ + briefs     │     in worktree  │ in worktree  │   reviews   │ trees    │
  └──────────────┘                  └──────────────┘             └──────────┘
```

The article-writing step happens **inside each worktree**, by Claude or
by a human operator, under the writer-packet contract that PR #80
introduced (`scripts/run-help-article.py --phase writer-packet`). The
coordinator does not touch article content; it only structures the
work and collects the result.

## Mode 1: prepare

```
python3 scripts/run-help-article-batch.py --mode prepare \
    --batch process/batches/<batch>.yml \
    --worktree-base /tmp/wt-batch-<batch_id>
```

What it does, in order:

1. Calls `scripts/validate-article-batch.py` against the batch YAML.
   If the upstream validator rejects, prepare exits 2.
2. Enforces the coordinator's 10-article cap. Above 10 → exit 2.
3. Defense-in-depth duplicate-slug check.
4. For each article:
   - Creates an isolated worktree at `<worktree-base>/<slug>/` from
     `--base-ref` (default `origin/main`), on a new branch
     `feat/batch-<batch_id>-<slug>`.
   - Runs `--phase writer-packet` and `--phase checklist` inside the
     worktree, dumps both to `_work/<slug>__writer-packet.md` and
     `_work/<slug>__checklist.md`.
   - Writes a single-page brief at `_work/<slug>__brief.md` that the
     worker (Claude or human) reads to start.

What it does **not** do:

- Does **not** require `validate` exit 0. The article is empty by
  definition at this point; the gate runs in review mode.
- Does **not** clobber an existing worktree path. If
  `<worktree-base>/<slug>/` already exists, prepare fails with exit 3
  unless `--force-clean` is explicitly passed.
- Does **not** require the user's main working tree to be clean. The
  worktrees are created from a fetched base ref, so they are isolated
  from the caller's local state.

Flags:

- `--base-ref <ref>` (default `origin/main`). The git ref the worktrees
  branch from. Use `HEAD` for tests if origin is not fetchable.
- `--force-clean`. Wipe any existing `<worktree-base>/<slug>/` before
  recreating. Refuses to be silent: requires the explicit flag.
- `--dry-run`. Validate the batch contract and print what would happen,
  without touching the filesystem or git. Used by tests.

## Worker step (between prepare and review)

After prepare, the operator opens each `_work/<slug>__brief.md`,
briefs Claude (or sits down personally), and produces:

- `articles/<slug>/pt-br.md`
- `articles/<slug>/en.md`
- `articles/<slug>/mockup-sources/*.html`
- `assets/mockups/<slug>__*__v3.png`
- `articles/<slug>/audit/*.md`

Each article is its own branch. When the worker is done, they should
have run the canonical gate locally:

```
python3 scripts/run-help-article.py articles/<slug> --phase validate
```

The coordinator does not enforce this — but `review` will, on every
article in the batch.

## Mode 2: review

```
python3 scripts/run-help-article-batch.py --mode review \
    --batch process/batches/<batch>.yml \
    --worktree-base /tmp/wt-batch-<batch_id> \
    --out _work/batch-<batch_id>
```

What it does, in order:

1. Re-loads the batch YAML and the per-article entries (same
   contract checks as `prepare`).
2. For each article, in its worktree:
   - Runs `scripts/run-help-article.py <article> --phase validate`,
     captures rc and full output.
   - Parses hard-fail and soft-warn counts.
   - Reads `flow.yml.mockup_plan.screens` and verifies every declared
     `<slug>__<screen>__<locale>__v*.png` exists in
     `<worktree>/assets/mockups/`.
   - Counts em-dashes in pt-br.md and en.md, and `R$` occurrences in
     en.md (pt-BR is allowed to use `R$`).
   - Counts audit-triplet files present (0..3) and whether any still
     contains `SKELETON_TODO`.
3. Writes `summary.json` (machine-readable) and calls
   `render-reviewer-pack.py` to produce `summary.html` (the
   human-reviewable pack).
4. Prints a CLI scorecard.

Exit code:

- `0` if every article is `ready` (validate exit 0, no missing PNG,
  audit triplet complete and unfilled).
- `1` if any article is `blocked` or `failed`.
- `2` on contract violation (batch YAML invalid, >10 articles).

The reviewer pack at `<out>/summary.html` is a single static HTML
file with:

- Top scorecard (one row per article): status badge, hard fails, soft
  warns, em-dashes pt/en, R$ leak EN, mockups present/declared,
  audit files present, validate exit code.
- One detail block per article:
  - Validate output verbatim.
  - pt-BR body rendered preview (markdown subset).
  - EN body rendered preview.
  - Inline mockup grid.
  - The 4 reviewer questions:
    a. Tone, pt-BR. Native or translated?
    b. Mockups. Professional or placeholder-ish?
    c. Factual claims. Grounded in code-audit, or invented?
    d. Publishable in Intercom today?

The pack is **static**: no JavaScript, no forms, no fetch. The
reviewer answers the 4 questions in their own notes or directly in
the per-article PR comments.

## Mode 3: cleanup

```
python3 scripts/run-help-article-batch.py --mode cleanup \
    --worktree-base /tmp/wt-batch-<batch_id>
    [--remove [--force-clean]]
```

Lists every subdirectory of `<worktree-base>/` and reports git status
(`clean` vs `has changes`). Without `--remove`, just reports.

With `--remove`:
- Clean worktrees → removed via `git worktree remove`.
- Worktrees with uncommitted changes → kept, unless `--force-clean`
  is also passed (then `git worktree remove --force`).

Cleanup is intentionally non-destructive by default. The reviewer might
have local edits in a worktree that have not been committed yet; we
never want to drop those silently.

## Failure modes and what they look like

| Symptom | Cause | What to do |
|---|---|---|
| `prepare` exits 2 with "coordinator cap is 10" / "exceeds max 10" | batch YAML has >10 articles | split into multiple batches |
| `prepare` exits 2 immediately | `validate-article-batch.py` rejected the batch (dup slug, missing required field, etc.) | read the upstream validator's stderr and fix the YAML |
| `prepare` exits 3 for a slug | `<worktree-base>/<slug>/` already exists | pick a different `--worktree-base`, or pass `--force-clean` |
| `review` exits 1 with "blocked" rows | at least one article failed validate, has missing PNGs, or has SKELETON_TODO | open `summary.html`, fix each blocker, re-run review |
| `review` summary has no images | mockups missing OR file:// URLs not resolvable | confirm `<worktree>/assets/mockups/` has the PNGs and that the worktree base path matches what `summary.json` shows |

## Fixtures

The coordinator and the renderer ship with checked-in fixtures under
`tests/fixtures/batch-coordinator/`:

- `batch-1.yml` — 1-article happy path
- `batch-3.yml` — 3-article happy path
- `batch-10.yml` — 10-article happy path at the cap (PR #88)
- `batch-11-rejects.yml` — must reject (over cap, PR #88)
- `batch-10-gates/article-icon-{missing,present}/` — synthetic articles for the new validator rules `screen_icon_not_in_html` (PR #88)
- `batch-dup-rejects.yml` — must reject (duplicate slug)
- `sample-summary-ready.json`, `sample-summary-hardfail.json`,
  `sample-summary-missing-png.json`, `sample-summary-3articles.json`
  — synthetic review results, used by `scripts/test-batch-coordinator.py`
  and to generate the sample reviewer pack at
  `_work/sample-batch/summary.html`.

The fixtures are **synthetic**. The coordinator infrastructure does
not ship a real 3-article batch; the first real batch run will be
PR #84.

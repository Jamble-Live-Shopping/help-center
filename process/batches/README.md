# Article batches

A batch describes the **articles to write in one production round**.
The same YAML drives every coordinator step: validation, prepare,
review.

## Where this lives in the lifecycle

```
batch.yml ──┐
            │  scripts/validate-article-batch.py     (lint)
            │  scripts/init-article-flow.py           (bootstrap one flow.yml)
            │  scripts/run-help-article-batch.py      (orchestrate 1..3 worktrees)
            │
            └─→ prepare ─→ Claude writes ─→ review ─→ human approves ─→ 1 PR per article
```

Single-article path stays the same as before: `init-article-flow.py`
+ `run-help-article.py`. The batch path adds `run-help-article-batch.py`
on top, so 1 to 10 articles can be set up and reviewed in a single
session without any LLM-in-Python.

## Authoring a batch YAML

Required fields at the top:

- `batch_id` (string, kebab-case) — used as a tag in worktree paths
  and PR branch names.
- `workflow` — currently always `article-v2`.
- `mode` (default `v2_rewrite`) — applied to articles unless they
  override per-entry.

Per-article (`articles[]`) required fields:

- `slug` — kebab-case, must match `articles/<slug>/` on the base ref
  unless `mode: new_article`.
- `priority` — positive integer; reviewers process by priority.
- `audience` — `seller_br`, `buyer_br`, or `both`.
- `intercom_id` — the canonical id from `articles/<slug>/metadata.yml`.
  Cross-checked at review time, so a stale id surfaces fast.
- `job_to_be_done` — one sentence; what the reader walks away with.
- `source_hints.ios_files` and `source_hints.backend_files` — list
  (can be empty, but must be present). If both are empty, add
  `source_hints.justification: "<why>"`.

Optional:

- `mode: new_article | minor_edit` per entry.
- `mockup_count_target` — number of screens; used by the worker
  packet to pre-budget mockup work.

The upstream validator (`validate-article-batch.py`) enforces the
required fields. The batch coordinator adds two tighter checks:

- batch size is capped at **10 articles** (PR #88; aligned with the
  upstream validator's `MAX_BATCH_SIZE = 10`). The reviewer pack
  scales to 10 via the per-screen Manual gates callout introduced
  in the same PR; above 10 the format would need a different review
  pattern.
- the same defense-in-depth duplicate-slug check.

## Files in this directory

- `article-batch.example.yml` — canonical example batch, used by the
  factory CI to validate that the schema still parses and that
  `init-article-flow.py` can bootstrap from it.
- (this file) `README.md` — what you are reading.

Test fixtures for the coordinator live separately under
`tests/fixtures/batch-coordinator/`, including failing batches
(over-cap and duplicate-slug) used by the regression tests.

## Running a batch

```bash
# 1. Lint the batch.
python3 scripts/validate-article-batch.py process/batches/<file>.yml

# 2. Prepare worktrees (cap 10, isolated, fails if path exists).
python3 scripts/run-help-article-batch.py --mode prepare \
    --batch process/batches/<file>.yml \
    --worktree-base /tmp/wt-batch-<batch_id>

# 3. Worker (Claude or human) writes each article inside its worktree.
#    The brief lives at <worktree>/_work/<slug>__brief.md.

# 4. Review: collect results + emit reviewer pack.
python3 scripts/run-help-article-batch.py --mode review \
    --batch process/batches/<file>.yml \
    --worktree-base /tmp/wt-batch-<batch_id> \
    --out _work/batch-<batch_id>

# 5. Open the reviewer pack.
open _work/batch-<batch_id>/summary.html

# 6. After every article is approved, push each worktree as its own PR.
#    The coordinator NEVER does this for you.
```

See `process/14-batch-coordinator.md` for the full operating manual,
including the 4 reviewer questions, failure modes, and the cleanup
mode.

## Non-goals

- The coordinator is not a writer. No LLM call, no content generation,
  no auto-PR.
- No batch can produce a single combined PR. Each article ships as
  its own PR.
- No auto-publish. State transitions to `published` go through
  `metadata.yml` + the existing sync workflow, never through the
  coordinator.

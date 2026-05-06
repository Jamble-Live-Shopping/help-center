# Help Article Runner

`scripts/run-help-article.py` is the single-article runner of the Help
Center Article Factory. It does NOT generate article content yet (that
is the next PR scope). What it does today is structure the work and
turn the validator's hard fails into a phase-grouped action plan.

## Purpose

Take any `articles/<slug>/flow.yml` and answer three operational questions
without re-reading the entire RUNBOOK each time:

1. What artefacts does this article need?
2. Does it currently pass the validator?
3. Where do I start fixing if it fails?

## Commands

Run from the repo root.

| Phase     | Command                                                    | Exit | What it prints |
|-----------|------------------------------------------------------------|------|----------------|
| plan      | `python3 scripts/run-help-article.py articles/<slug> --phase plan`      | 0 / 2 | Job-to-be-done, audience, mode, intercom_id, then the ordered checklist of artefacts grouped by RUNBOOK phase (Phase 1 to Phase 8). Includes risk_flags and resolved_decisions if any. |
| validate  | `python3 scripts/run-help-article.py articles/<slug> --phase validate`  | 0 / 1 / 2 | Forwards the validator output verbatim. Exit code mirrors the validator's. |
| checklist | `python3 scripts/run-help-article.py articles/<slug> --phase checklist` | 0 / 2 | Runs the validator, parses each FAIL line, and groups them by RUNBOOK phase ("Phase 1, Code audit", "Phase 5, Article body", "Phase 7, Audit triplet", etc.). Always exit 0; the goal is to print the plan, not gate it. |

## What the runner does

- Reads `articles/<slug>/flow.yml` and `articles/<slug>/metadata.yml`
- Calls `scripts/validate-article-flow.py` (same script CI uses)
- Maps each known hard-fail rule to its RUNBOOK phase via a static
  table inside the script. The mapping lives next to the rule names
  for reviewability.

## What the runner does NOT do (yet)

- Generate `pt-br.md` or `en.md` content
- Render mockups or audit MDs
- Run a parallel batch
- Modify any file under `articles/<slug>/`
- Call any LLM
- Open or update a PR

These are deliberate non-goals for this PR. The split keeps the runner
auditable and lets the next PRs add capability without re-touching
this surface.

## Usage example

### On a v2-ready article

If the article passes the validator, `--phase checklist` prints:

```
0 hard fails. Article is ready for review and PR.

Next: open a draft PR. The CI workflow validate-article-flow
      will re-run the validator on the changed paths.
```

### On the DM pilot (red)

The DM v2 rewrite (PR #73 branch) currently has real defects:

```
$ python3 scripts/run-help-article.py articles/direct-messages-for-sellers --phase checklist

# Checklist: articles/direct-messages-for-sellers

## Phase 1, Code audit  (1 fail)
  - [backend_files_not_audited] flow.yml declares 1 backend_file(s)...

## Phase 5, Article body (image refs)  (2 fails)
  - [mockup_declared_not_in_pt] screen 'product-message-thread'...
  - [mockup_declared_not_in_en] screen 'product-message-thread'...

## Phase 7, Audit triplet  (3 fails)
  - [code_audit_inconsistent] code-audit claims 'ship-ready' but contains 'PARTIAL'...
  - [content_audit_missing_stale_feature] content-audit has no stale-feature audit...
  - [compliance_all_pass_with_risks] compliance says 'ALL PASS' but risk_flags active...

## Phase 8, PR and sync  (1 fail)
  - [published_with_unresolved_risks] metadata.state='published' with active risks...

Total hard fails: 7
Next: address phase by phase, starting with the lowest phase number.
```

The worker now knows exactly: re-do Phase 1 first (cite backend in code-audit),
then fix Phase 5 mockup refs, then Phase 7 audits, then Phase 8 publish state.

### On a brand new article (wishlist via batch)

```
$ python3 scripts/init-article-flow.py --slug wishlist-and-favorites \
    --from-batch process/batches/article-batch.example.yml \
    --dry-run > articles/wishlist-and-favorites/flow.yml
$ python3 scripts/run-help-article.py articles/wishlist-and-favorites --phase plan
```

The `plan` phase prints the artefact list a worker (or `/help-article`
skill in PR #79) needs to produce: iOS files to read, mockup HTML pairs,
PNGs DPR3 to render, audit triplet keyed by intercom_id, etc.

## Where this fits in the factory

```
process/batches/<file>.yml
   |
   v
scripts/validate-article-batch.py    -> lint
scripts/init-article-flow.py         -> bootstrap articles/<slug>/flow.yml
   |
   v
scripts/run-help-article.py --phase plan        -> what to produce
                            --phase validate    -> does it pass today
                            --phase checklist   -> what to fix next
   |
   v
scripts/validate-article-flow.py    -> the contract gate (also CI)
   |
   v
scripts/replay-golden-articles.py   -> calibration vs history
```

## Roadmap (after this PR)

- PR #79: article writer mode that, given a green flow.yml, drafts
  `pt-br.md` from xcstrings + iOS code, mirrors `en.md`, generates
  audit-triplet skeletons. Still single-article.
- PR #80: batch runner that takes `process/batches/<file>.yml` and
  parallelises N article runners across N worktrees.

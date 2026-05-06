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

| Phase           | Command                                                    | Exit      | What it prints |
|-----------------|------------------------------------------------------------|-----------|----------------|
| plan            | `python3 scripts/run-help-article.py articles/<slug> --phase plan`           | 0 / 2     | Identity, job, ordered artefact checklist grouped by RUNBOOK phase, risk_flags, resolved_decisions. |
| validate        | `python3 scripts/run-help-article.py articles/<slug> --phase validate`       | 0 / 1 / 2 | **Final gate.** Forwards the validator output and exit code verbatim. Use this in any automation. |
| checklist       | `python3 scripts/run-help-article.py articles/<slug> --phase checklist`      | 0 / 2     | Validator hard fails grouped by RUNBOOK phase. **Informational, not a gate**: exits 0 even when the validator reports fails, because the goal is to print the action plan. |
| writer-packet   | `python3 scripts/run-help-article.py articles/<slug> --phase writer-packet`  | 0 / 2     | Markdown packet for a worker (human or LLM): identity, job, source-of-truth reading checklist, content_contract, mockup_plan with expected file pairs, icons_required, risks, deliverables in order, final validate command. Read-only. |
| writer-packet + skeletons | `--phase writer-packet --write-skeletons [--force]`                  | 0 / 2     | Same packet, plus creates the audit triplet skeletons (`code-audit-<id>.md`, `content-audit-<id>.md`, `compliance-<id>.md`) when missing. Never overwrites without `--force`. Does NOT create body or mockups. No LLM. |

## Phases that are gates vs. informational

- **`validate` is the only gate.** It exits 0 iff the article passes the
  contract. Automation, batch runners, and any future writer mode MUST
  call `--phase validate` and respect its exit code as the final
  decision.
- **`checklist`, `plan`, `writer-packet` are informational.** They can
  exit 0 even when the article still has validator hard fails. Their
  job is to print a useful action plan, not to gate.

## Contract preflight (every phase)

Before the runner does anything else, it checks the article folder is a
real contract:

1. `articles/<slug>/` exists and is a directory inside the repo
2. `articles/<slug>/flow.yml` exists and parses to a YAML mapping
3. `articles/<slug>/metadata.yml`, if present, parses to a YAML mapping

If any of these fail, the runner exits **2** with a clear `[flow_missing]`,
`[flow_yaml_parse]`, or `[metadata_yaml_parse]` marker on stderr, and
points to `scripts/init-article-flow.py` to bootstrap the flow.

The preflight prevents a class of false greens: the underlying
`scripts/validate-article-flow.py` silently skips paths that have no
`flow.yml` and prints "No articles to validate". Without preflight, the
runner would call that, see exit 0, and report "Article is ready" on an
article that has no contract at all. The preflight makes this a hard
setup error (Phase 0 in the RUNBOOK mapping).

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

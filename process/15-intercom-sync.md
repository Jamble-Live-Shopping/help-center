# Phase 15 — Intercom sync (manual publish)

## TL;DR

**Merging an article PR to `main` does NOT publish it to Intercom.** Publication is a separate, manual, explicit step. You decide when each article ships to readers.

This page documents how to do that manual step safely.

## Why this is manual

The repo had a workflow that auto-synced any article touched by a `main` push. On 2026-05-11 during the batch real-1-rerun-2 merge wave, that workflow auto-published article 14288117 before the merge author meant to ship it. The post-mortem (release report for that batch) recommended converting the workflow to manual dispatch. This file is the runbook for the new flow.

## Trigger

Workflow file : `.github/workflows/sync-intercom.yml`

Trigger : `workflow_dispatch` only. The `on: push` trigger has been removed.

Inputs :
- `article` (required) : article slug (e.g. `choose-quantities-when-listing-products`) or full path (e.g. `articles/choose-quantities-when-listing-products`). One slug per run. No "sync all" fallback.
- `confirm` (required) : type the literal string `yes` (lowercase, no quotes) to confirm publishing to production Intercom. Anything else aborts the run loud.

## How to publish one article

### From the GitHub UI

1. Open the repo on GitHub → Actions tab.
2. Pick **Sync articles to Intercom** in the workflow list.
3. Click **Run workflow** (top right of the list).
4. Pick branch `main`.
5. Fill in `article` with the slug (or full path).
6. Fill in `confirm` with `yes`.
7. Click **Run workflow**.

### From the gh CLI

```bash
gh workflow run "Sync articles to Intercom" \
  --ref main \
  -f article=choose-quantities-when-listing-products \
  -f confirm=yes
```

Both forms produce the same result. Always include `confirm=yes` ; the workflow's first step fails fast otherwise with a `Sync refused.` error message.

## How to publish several articles

Run the workflow once per slug. There is no batch input by design ; a single accidental "run all" click was the original failure mode, and the design now forces one explicit decision per article.

If a future batch ships and you do need to publish 5+ articles, dispatch the workflow 5+ times. Future improvement : a separate `Sync articles batch` workflow gated on a Linear ticket or a checked-in `intercom-publish.yml` manifest, with explicit slug list and a human approver before the apply step. Out of scope for the gate PR ; raise a follow-up if it becomes a friction point.

## What this workflow does NOT do

- It does not auto-sync on push, ever.
- It does not sync more than one article per run.
- It does not run if `confirm` is anything other than the literal string `yes`.
- It does not skip the `Refuse without confirm` step ; that step is the first job step.

## Verifying the gate stays manual

```bash
# 1. workflow is still active
gh workflow list

# 2. workflow file has NO `on: push` trigger
grep -n "^on:\|push:" .github/workflows/sync-intercom.yml

# 3. workflow file has workflow_dispatch with required inputs
grep -n "workflow_dispatch\|required: true" .github/workflows/sync-intercom.yml
```

The static grep test `test_sync_intercom_workflow_is_manual_dispatch_only` in `scripts/test-batch-coordinator.py` enforces (2) and (3) in CI.

## Re-enabling after a disable

If the workflow has been disabled (e.g. via `gh workflow disable`) and you want to use it again :

```bash
gh workflow enable "Sync articles to Intercom"
gh workflow list  # confirm it is now "active"
```

A manual re-enable is safe ONLY when this file plus the workflow file agree that there is no `on: push` trigger. If you find an `on: push` block, do not re-enable until it's gone.

# Golden flows

Templates of `flow.yml` for shipped v2 articles, used by
`scripts/replay-golden-articles.py` to **calibrate** the
article-flow validator against historical content. They are NOT live
contracts: the harness swaps a golden flow into
`articles/<slug>/flow.yml` for the duration of one `validate-article-flow`
run, captures the report, then restores the original (or removes the
file if the article had no flow.yml).

## When to add a golden flow

Add one when:
- A v2 article in main is widely considered representative quality
  (battles, real-time offers, flash-sales, livestream-tools,
  apply-to-sell, etc.)
- AND the validator's behavior on that article reveals a calibration
  question (false positive, false negative, ambiguous rule)

## How to read the harness output

```
article                hard  warn  rules                          status
---------------------  ----  ----  -----------------------------  ------
flash-sales            1     7     content_audit_scan6_not_stale  ok
livestream-tools-...   1     7     content_audit_missing_stale... fail
```

- `ok` means every observed hard fail is in the article's
  `replay_allowlist`. The article passes the calibration even with
  declared technical debt.
- `fail` means at least one hard fail is NOT in the allowlist. The
  validator surfaced something unexpected. Either fix the article, fix
  the validator, or extend the allowlist with explicit justification.

## Allowlist policy

Allowlist entries are **technical debt markers**, not silent
exceptions. Each entry:
- corresponds to a real defect in the historical article (audit gap,
  mockup naming asymmetry, missing audit, etc.)
- is documented in a comment above the `replay_allowlist:` block,
  with the reason and the path to remove it
- is dropped when the underlying defect is fixed in a separate PR

A golden flow with an empty `replay_allowlist:` is a **canary**: the
article must pass the validator without exception. If it fails, the
harness exits 1 to signal the regression.

## Stable allowlist categories

These rules can be allowlisted when the gap is documented:
- `content_audit_scan6_not_stale` — audit uses bare "Scan 6" without
  explicit stale-feature wording (legacy from v1.1 false-positive era)
- `content_audit_missing_stale_feature` — audit has no stale section
  at all (older articles)
- `mockup_declared_not_in_{pt,en}` — historical naming asymmetry
- `mockup_referenced_not_declared` — same
- `mockup_png_missing` / `mockup_html_missing` — historical asymmetry
- `backend_files_not_audited` — backend dependency declared in flow but
  audit cites only iOS

These rules should NOT be allowlisted lightly:
- `published_with_unresolved_risks` — a real production risk
- `code_audit_inconsistent` — the audit text contradicts itself
- `forbidden_term`, `auction_word`, `em_dash`, `en_dash` — editorial
  rules that pre-date the YAML contract

## Running the harness

```
scripts/replay-golden-articles.py             # all golden flows
scripts/replay-golden-articles.py <slug>      # one
scripts/replay-golden-articles.py --json      # machine-readable
```

Exit 0 iff every replayed article passes its allowlist. Exit 1 if any
unexpected hard fail surfaces. Exit 2 on script error.

# Compliance audit, intercom_id=14288101

slug: `understanding-listing-conditions-and-expectations`
audited_at: 2026-05-11
process_ref: `process/12-procedure-compliance.md`, post PR #91/#92/#103/#104

## 18-check compliance grid

| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | 1 H1 only (rule 25) | PASS | `grep -c "^# " pt-br.md en.md` = 1 + 1. |
| 2 | No orphan mockups (rule 26) | PASS | mockup-sources contains exactly 4 files matching declared screens `condition-picker__{pt-br,en}.html` and `section-row__{pt-br,en}.html`. |
| 3 | `ios_files` paths exist (rule 27) | PASS | All 11 paths verified via `ls $JAMBLE_IOS_ROOT/<path>`. |
| 4 | Every `icons_match_ios_source` screen anchored (rule 10e) | OUT OF SCOPE | This article uses no iOS asset icons. The two screens declare `labels_match_xcstrings` + `no_invented_ui_state` only. The picker uses native radio circles (drawn in Swift, no asset), and the section row uses a native chevron (UIImage(systemName: "chevron.right"), no asset file). `icons_match_ios_source` is intentionally not declared. |
| 5 | xcstrings verbatim for UI labels | PASS | `Condition` -> `Condição` from `Localizable.xcstrings:7226-7237`. All 5 tier titles + descriptions come verbatim from `condition.json` (server-driven copy is the source of truth, not xcstrings, per the backend `/get_conditions` route). |
| 6 | No em-dashes (U+2014) | PASS | `python3 -c "print(open('pt-br.md').read().count(chr(0x2014)))"` = 0. Same for en.md. |
| 7 | No en-dashes (U+2013) | PASS | Both .md files = 0. |
| 8 | pt-BR is PRIMARY | PASS | pt-br.md written first; en.md is a 1:1 mirror except for currency (R$ 450,00 -> $90.00). |
| 9 | No R$ leak in en.md | PASS | `grep -c "R\$" en.md` = 0. |
| 10 | No invented UI | PASS | Both mockups render UI that exists in iOS code (picker rows + section rows). No "decision guide", no comparison chart, no fake UI. |
| 11 | Citations file:line in code audit | PASS | Every claim in `code-audit-14288101.md` carries a path + line range or path + symbol. |
| 12 | Description <= 140 chars | PASS | pt-br: 117 chars. en: 113 chars. |
| 13 | Title with no em-dash, <= 60 chars | PASS | pt-br title: 37 chars. en title: 33 chars. |
| 14 | Auction / leilão / leilao banned | PASS | 0 occurrences in pt-br.md and en.md. Enforced by `forbidden_terms`. |
| 15 | TOC for >= 6 H2 (toc_policy=warn) | SOFT WARN ACCEPTED | Article has 10 H2 sections. Adding a TOC would push content below the fold on mobile; the H2 progression is linear and self-navigating. Soft warn left in place per `toc_policy=warn`. |
| 16 | PNG DPR3 (>= 900px wide) | PASS | All 4 PNGs are 960px wide (verified via PIL). |
| 17 | Screens declared in flow.yml render to PNGs in markdown | PASS | Both screens (`condition-picker`, `section-row`) are referenced via `__v3.png` in pt-br.md and en.md. |
| 18 | No deprecated features referenced (badges, Jamble Prime, auction wording) | PASS | Stale-feature audit in content-audit confirms all 6 features mentioned are LIVE in main. |

## Risk flags

None. Article body cites only code-verified facts. No legal tension. No deprecated UI. No undocumented backend behavior. Safe to ship as `state: published`.

## Verdict

ALL 18 checks resolved (16 PASS, 1 OUT OF SCOPE with justification, 1 SOFT WARN accepted with rationale). Ship.

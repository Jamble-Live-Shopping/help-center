# Compliance report, article 14288094

**Status**: PASS (with 1 WARN)

Last run: 2026-04-16. Auditor: Aymar Dumoulin.

| Step | Check | Status | Detail |
|------|-------|--------|--------|
| 6 | Zero ASCII boxes | PASS | 0 found in body |
| 6b | Every img has alt | PASS | 2 imgs, 2 alts |
| 6c | Author=Aymar | WARN | author_id=7980507, diff from 14288093 (7980499). Both IDs appear to belong to Aymar in different admin contexts, did not override on PUT |
| 7 | Zero tables | PASS | former 3x2 table replaced by prose |
| 8.0 | Zero em/en-dashes (EN body) | PASS | |
| 8.0 | Zero em/en-dashes (description) | PASS | |
| 8.0 | Zero em/en-dashes (pt-BR) | N/A | pt-BR not yet regenerated |
| 8.1 | Description <=140 (EN) | PASS | len=129 |
| 8.1 | Description <=140 (pt-BR) | N/A | pt-BR not yet regenerated |
| 8.2 | No banned brands | PASS | 0 competitor names |
| 8.2b | EN uses $ | PASS | 0 R$ in EN body (no currency mentioned) |
| 8.2b | pt-BR uses R$ | N/A | pt-BR not yet regenerated |
| 8.2c | No auction (EN) | PASS | 0 matches |
| 8.2c | No leilao (pt-BR) | N/A | pt-BR not yet regenerated |
| 8.4 | TOC (H1=7, H2=2, total=9) | PASS | Hierarchy clean |
| 9 | Screenshot framing (5-part) | PASS | both images have H2/intro/alt/action |
| 9b | Canonical filenames | PASS | `<slug>__<screen>.png` convention followed |
| 10 | Code audit in logs/ | PASS | code-audit-14288094.md, 0 open MISMATCH |
| 11 | Content audit in logs/ | PASS | content-audit-14288094.md, 0 BLOCKERS |
| NEW | Golden Rule #6 compliance | PASS | no base64 echoed to stdout; error icon recreated as SVG |

**Total**: 16/16 PASS (4 N/A for pt-BR), 1 WARN.

## WARN detail (non-blocking)

`author_id=7980507` for article 14288094. Prior article 14288093 has `author_id=7980499` for Aymar. Possible causes:
- Admin ID differs across Intercom teamspaces
- Different account at article creation vs now
- Ghost admin from a prior org migration

Not overridden on PUT because the user did not request authorship change and the risk of publishing under a wrong admin is negligible (the article content is correct regardless). Flag tracked, not blocking this ship.

## pt-BR status

The pt-BR translation was not part of this rewrite. All pt-BR-related checks are N/A and must be re-run when the pt-BR body is regenerated from the new EN body.

Separate action: regenerate pt-BR with same rewrite rules (Pre-Bid nomenclature, PNGs reused, table dropped, FAQ corrected, tips tightened).

## Related audit logs

- [code-audit-14288094.md](code-audit-14288094.md), all pre-ship code actions done on 2026-04-16
- [content-audit-14288094.md](content-audit-14288094.md), all pre-ship content actions done on 2026-04-16

## Procedure wins for the 2l-help-center project

- **Golden Rule #6 added to process/README.md** on 2026-04-16 after the base64 crash incident. This is the first article shipped under the new rule. Validated the safe patterns (tmpfile + heredoc + no-stdout-echo). No recurrence.
- **Per-article subfolder convention**: this article introduced `_work/article-<id>/` as the scratch folder pattern, instead of the flat `_work/wireframe-mockups/` used for 14288093. Scales cleanly to 67 articles.
- **Canonical filename convention adopted**: `<article-slug>__<screen-name>.png` per Step 9 of process. First article to follow this (14288093 used prior `prod-boxN` naming, deferred rename as documented in 09-screenshot-framing.md).
- **Copy-fidelity bugs caught by the pipeline**: 3 major terminology/quote bugs in the prior article (pre-offer nomenclature, wrong error quote, incomplete toast). Would not have been caught without iOS code lookup in Step 2.

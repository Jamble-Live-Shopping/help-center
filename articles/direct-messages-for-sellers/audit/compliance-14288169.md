# Compliance report, intercom_id=14288169 (direct-messages-for-sellers)

Run on 2026-11-13 after the fidelity fix against iOS 5.11, Android v5.11.0 and backend origin/main.

**Status**: PASS (validator 0 hard fails; publication still needs the manual release gate)

| # | Check | Status | Detail |
|---|---|---|---|
| 1 | No ASCII boxes in body | PASS | none |
| 2 | Code lookup per mockup | PASS | layout proof table in code-audit |
| 3 | HTML source per mockup | PASS | `activity-tabs__en.html`, `activity-tabs__pt-br.html` |
| 3b | pt-BR / EN HTML iso structure | PASS | `diff` shows text-only changes (labels, sample messages, dates) |
| 3c | No emoji UI icons | PASS | none; avatars are neutral gradient swatches (user photos) |
| 4 | PNG per HTML at DPR 3 | PASS | 960 x 1158 each, viewed one by one |
| 4b | PNGs at root `assets/mockups/` with `__v3` | PASS | `direct-messages-for-sellers__activity-tabs__{pt-br,en}__v3.png` |
| 5 | metadata.yml locales block | PASS | pt-br and en |
| 6b | Every image has descriptive alt | PASS | 116 / 124 chars |
| 7 | No tables in body | PASS | lists only |
| 8a | Descriptions <= 140 | PASS | 133 / 122 |
| 8b | Zero em / en dashes | PASS | 0 / 0 |
| 8c | No banned brand examples | PASS | none |
| 8d | TOC | PASS | `toc_required: false` in flow.yml |
| 8e | No fee decomposition, no auction wording | PASS | none |
| 9 | Code audit present, no open MISMATCH | PASS | `code-audit-14288169.md` |
| 10 | Content audit present, no BLOCKER | PASS | `content-audit-14288169.md` |
| 12 | Real iOS icons where shown | PASS | the cropped area shows no icon assets; `icons_required` emptied (old `live_send_message` and `icon-chat-star` were never used) |
| 13 | Worktree | OUT OF SCOPE | single-article fix in the shared checkout, no commit |
| 14 | Stale-feature scan | PASS | table in content-audit |
| 15 | DA discipline | PASS | no cartoons, no big-text placeholders |
| 16 | DA tokens | PASS | colors from iOS source (#000000 pill, #DADDE3 border, #F0F1F5 unread, #7E53F8 brand, #566371, #A4A8AC) |
| 17 | Visual fidelity | PASS | code-only, see code-audit |
| 20 | Risk flags | PASS | both former risk flags recorded in `resolved_decisions` (code check, 2026-11-13) |

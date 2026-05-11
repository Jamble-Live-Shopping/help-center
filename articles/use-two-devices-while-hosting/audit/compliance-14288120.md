# Compliance audit, article 14288120 (use-two-devices-while-hosting)

Date: 2026-05-08
Workflow: article-v2
Mode: v2_rewrite
Audience: seller_br
State: published

## Hard contracts

| Rule | Status | Notes |
|---|---|---|
| Heading hierarchy: exactly 1 H1 per locale (rule 25) | PASS | Both pt-br.md and en.md have a single `# Title` then `## Section` headings |
| No em-dash in pt-br.md / en.md (rule 5) | PASS | 0 em-dash count in both files |
| No en-dash in pt-br.md / en.md (rule 5) | PASS | 0 en-dash count in both files |
| No `R$` in en.md (rule 6) | PASS | No currency on this surface; en body uses no currency tokens |
| `currency_required: false` (rule 7) | PASS | Article does not document price |
| No `auction` / `leilão` (rule 8) | PASS | Forbidden regex absent in both locales |
| Mockup PNGs DPR3 >=900px wide (rule 9) | PASS | 6/6 PNGs at 960px wide |
| `mockup_plan.required=true` declares >=1 screen (rule 9b) | PASS | 3 screens declared |
| Each declared screen has matching `<screen>__pt-br.html` + `<screen>__en.html` (rule 10) | PASS | 6/6 HTML files present |
| Markdown image references match declared screens (rule 10b) | PASS | Each screen referenced in both locales |
| Screen-scoped required_icons present in HTML (rule 10b) | PASS | `close-remote-button` declares `required_icons: [av.remote.fill, icon-close]`; both anchored via `<!-- icon: ... -->` comments in both pt-br and en HTML |
| Screen-scoped review_checks declared on iOS-required screens (rule 10c) | PASS | All 3 screens declare review_checks |
| Anchor presence per screen (rule 10e, NEW) | PASS | `remote-control-picker` and `host-offline-overlay` anchored via `html_must_not_contain: ['<img', '<svg', 'icon-']`; `close-remote-button` anchored via `required_icons: [av.remote.fill, icon-close]`. Zero unanchored screens. |
| `html_must_contain.<lang>` substrings present in matching HTML (rule 10d) | PASS | Verified for `remote-control-picker` (Controle remoto / Use como um controle remoto / Transmiss; Remote Control / Use as a remote / Livestream from this device) and `host-offline-overlay` (Aguarde / Seu dispositivo principal parece estar off-line; Hold on / Your main device seems offline) |
| `html_must_not_contain` strings absent from matching HTML (rule 10d) | PASS | `<img`, `<svg`, `icon-` absent from `remote-control-picker` and `host-offline-overlay` HTMLs |
| Orphan HTML in mockup-sources/ (rule 26) | PASS | 6 orphan HTMLs deleted; 6 declared HTMLs remain |
| Forbidden terms (rule 13) | PASS | `Close Remote`, `Fechar Controle Remoto` absent from both md files |
| Risk flags resolved if state=published (rule 14) | PASS | `risk_flags: []`, `state: published` -> no published-with-active-risk gate |
| metadata.yml description length <=140 chars (rule 4) | PASS | pt-br: 116 chars, en: 124 chars |
| metadata.yml description non-empty (rule 4) | PASS | Both locales filled |
| `source_of_truth.ios_files` paths exist (rule 27) | PASS | 5 paths verified under `JAMBLE_IOS_ROOT=/Users/aymardumoulin/Projects/Jamble-iOS/Jamble` |
| Audit triplet present (Phase 7) | PASS | code-audit-14288120.md, content-audit-14288120.md, compliance-14288120.md all present |

## Risk flag resolution

No active risk flags. `risk_flags: []` in flow.yml. `resolved_decisions: []`. The article is shipping straight green.

## Reviewer call-outs

- The article narrows scope to iOS-only. Android dual-device hosting is out of scope for this rewrite because no Android source was audited. If the team wants to document the Android flow, open a separate slug or extend `flow.yml.source_of_truth` to include Android files and re-audit.
- The Close Remote button is icon-only in code. The article and mockup honor that. Any future copy edit that introduces a text label like "Close Remote" / "Fechar Controle Remoto" will be caught by `forbidden_terms` and trip the validator.
- The pt-BR body uses ASCII transliteration for the editorial prose (no diacritics) consistent with other v2 rewrites currently shipped on main, while the screenshot mockups render the verbatim diacritic xcstrings the user actually sees in the app.

## Verdict

Zero hard fails expected. Anchoring rule 10e satisfied with 3/3 screens explicitly anchored.

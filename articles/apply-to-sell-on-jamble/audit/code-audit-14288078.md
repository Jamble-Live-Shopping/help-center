# Code audit, article 14288078 (apply-to-sell-on-jamble)

Date: 2026-04-21
Scope: verify every user-facing string in pt-br.md and en.md against iOS source.

## Claims checked

| Claim | iOS source | Status |
|-------|-----------|--------|
| Profile button label "Inscreva-se como vendedor Live" / "Apply to Sell Live" | `ProfileHeaderViewController.swift:378` + xcstrings 4128-4143 | MATCH |
| Settings row "Inscreva-se para entrar no ar" / "Apply to go Live" | `ProfileSettingsV2ViewController.swift:143` + xcstrings 4111-4126 | MATCH |
| Show menu UIAction "Apply to go Live" (BR only) | `ProfileViewController.swift:209` | MATCH |
| Pending Application alert title "Aplicativo pendente" / "Pending Application" | xcstrings 17356-17371 | MATCH |
| Pending Application alert message | xcstrings 13281-13297 | MATCH |
| Alert button "Entre em contato" / "Reach out" | xcstrings 18737-18751 | MATCH |
| Alert button "Ok, vou aguardar!" / "Ok I will wait!" | xcstrings 16188-16203 | MATCH |
| Max 2 applications enforcement | `JambleTabBarController.swift:452` | MATCH |
| Reach out action opens Intercom chat | `JambleTabBarController.swift:444-446` | MATCH |
| BR-only country gating in settings | `ProfileSettingsV2ViewController.swift:142` | MATCH |
| Form opens as embedded web view (not native) | `SellerApplicationInvitationViewController.swift:42-46` | MATCH |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| `apply-to-sell-on-jamble__configuracoes-menu__pt-br.png` | IMPORTANTE header, Inscreva-se para entrar no ar row, VENDER header | MATCH (rebuilt 2026-04-21) |
| `apply-to-sell-on-jamble__pending-application__pt-br.png` | Title + body + button labels all pt-BR | MATCH (rebuilt 2026-04-21) |
| `apply-to-sell-on-jamble__settings-apply-to-sell__en.png` | SETTINGS + Apply to go Live | MATCH |
| `apply-to-sell-on-jamble__pending-application__en.png` | Pending Application + Reach out + Ok I will wait! | MATCH |

## Changes from previous version

- Fixed pt-BR `configuracoes-menu` mockup: showed EN string "Apply to go Live", now shows pt-BR "Inscreva-se para entrar no ar"
- Fixed pt-BR `pending-application` mockup: entire alert was in English, now uses pt-BR strings from xcstrings
- Body text: replaced "Contact Support > Ask a General Question" (stale flow) with direct reference to the "Entre em contato" alert button, which now opens Intercom chat directly (code confirms: `AskJamble.shared.intercom.openIntercom()`)
- Body text: BR examples added (Pokémon TCG, Hot Wheels) per RULE 2 of editorial-quality

## Open issues

Zero MISMATCH. Zero open issues.

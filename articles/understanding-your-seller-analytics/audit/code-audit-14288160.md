# Code Audit: article 14288160 (Understanding Your Seller Data)

Wave 2 rewrite, 2026-10-14. Sources: Jamble-iOS tag 5.10.1, Jamble-Android tag v5.10.0, jamble_backend origin/main (291e133b5), Jamble-Website origin/main. Paths are repo-relative.

## Verified claims

- Live overlay "Vendas em tempo real" with running total and price per item: iOS `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:758-773` (Real-Time Sales, "$0", "$0/item"); Android `features/livestream/.../values-pt/strings.xml` real_time_sales. MATCH
- After ending the live, iOS shows a "My Dashboard" button (pt "Meu painel de controle"): `ShowHostViewController.swift:69`, laid out in `setupDashboardView`. MATCH
- Dashboard title "Your Show" (pt "Sua Live"): `LIVE_SHOPPING/DashboardHost/Views/ShowHostDashboardViewController.swift:33`; Android show_dashboard_title=Sua Live. MATCH
- RESUMO tiles: iOS `ShowHostDashboardView.swift:123-145` keys SUMMARY / TOTAL / AFTER FEES / SOLD / BUYERS, pt-BR now translated in xcstrings: RESUMO / TOTAL / PÓS TAXAS / VENDIDOS / COMPRADORES. Android renders server stats: jamble_backend `src/schemas/sale_actions.py:529-548` TOTAL / APÓS TAXAS / VENDIDOS / COMPRADORES. Article names both after-fees labels. MATCH
- After-fees value = total product price minus platform fee: `src/schemas/sale_actions.py:539-544`. Standard commission 10% of product price, shipping excluded (wave 2 verified production facts). MATCH
- Past lives on own profile: iOS `PROFILE/View Models/ProfileBottomViewModel.swift:90` (Profile Tab Past Lives = Lives Passadas); Android profile_tab_past_lives + dashboard sheet from the live card. MATCH
- "Resumo do seu show" DM after every live: jamble_backend `src/services/show_service.py:5797` calls `message_service.send_show_summary_message` at the end of the live; content in `src/services/message_service.py:2601-2697` (sections Audiência, Performance, Vendas, Seus compradores, comparison with previous lives). Metrics listed in the article match the code. MATCH
- Seller Hub nav: Website `src/lib/i18n/messages/console.ts` overview=Visão Geral, myLives=Lives, sales=Vendas, wallet=Carteira; overview cards Próximas lives / Envios; `lives.ts` Minhas Lives (agendadas, passadas e arquivadas); `dashboard.ts` Painel da live with total, Pós taxas, Vendas, Compradores. MATCH
- Wallet entry "My Wallet" (pt Minha carteira) in the SELL settings section: `PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:47`. Wallet wording "Disponível para saque" / "Vendas pendentes" from wave 2 verified production facts. MATCH

## Removed from the previous version

- "Labels appear in English" section: no longer true, pt-BR labels are translated.
- Wallet "via PIX" claim: saques are bank transfers.
- "What the app does not have yet" list: removed per content rules (no statements about missing features).

## Verdict

All claims trace to the production sources above.

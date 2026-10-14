# Content Audit: article 14288160 (Understanding Your Seller Data)

Wave 2 rewrite, 2026-10-14.

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Vendas em tempo real overlay | iOS 5.10.1 ShowHostViewController, Android real_time_sales | present | 2026-10-14 | wave2 agent | live_in_ios |
| Sua Live dashboard with RESUMO tiles in pt-BR | iOS xcstrings, backend sale_actions.py | present | 2026-10-14 | wave2 agent | live_in_ios |
| Resumo do seu show DM | backend origin/main message_service.py, show_service.py | present | 2026-10-14 | wave2 agent | live_in_backend |
| Seller Hub Visão Geral / Lives / Vendas / Carteira | Website origin/main console.ts, lives.ts, dashboard.ts | present | 2026-10-14 | wave2 agent | product_confirmed |
| English-only RESUMO tile labels | iOS xcstrings | translated now | 2026-10-14 | wave2 agent | deprecated |
| Wallet "Saldo disponível" + "Sacar via PIX" | wave 2 production facts | wording changed, saque is bank transfer | 2026-10-14 | wave2 agent | deprecated |

- Removed mockups: post-show-summary (English tile labels) and wallet-summary (old wording). Kept: live-realtime-sales (matches iOS).
- No removed features mentioned. No promises about future features.

## Language and format

- pt-BR primary, EN mirror with pt-BR labels in bold plus English gloss.
- No em or en dashes, no tables in the article, no "leilão" / "auction", "live" used instead of "show" except the exact DM title "Resumo do seu show".
- TOC present.

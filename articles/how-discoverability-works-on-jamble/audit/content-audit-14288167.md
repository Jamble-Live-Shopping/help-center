# Content Audit: article 14288167 (How Discoverability Works on Jamble)

Wave 2 rewrite, 2026-10-14.

## Stale-feature audit

- Removed: home tabs Ofertas / Explore / Seguir, the Follow empty state copy, the Members / Shows two-tab search, the "Esta etapa é importante" save-search prompt. None exist in iOS 5.10.1 or Android v5.10.0.
- Removed: all three mockups (they showed the removed UI).
- No removed features (sorteios, cashback, Stripe, verified badges) mentioned.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Bottom bar Ao vivo/Live, Loja, Atividade, Ganhos, Perfil | iOS 5.10.1 TabBar + xcstrings, Android v5.10.0 nav_* | present | 2026-10-14 | wave2 agent | live_in_ios |
| Home sections Para Você / Ao Vivo / categories | backend origin/main src/routers/homepage.py | present | 2026-10-14 | wave2 agent | live_in_backend |
| Search tabs Lives / Produtos / Membros | iOS SuggestionsPageController, Android search_strings | present | 2026-10-14 | wave2 agent | live_in_ios |
| Saved searches (Products tab) | backend product.py save_search/get_saved_searches, iOS SearchView, Android Buscas salvas | present | 2026-10-14 | wave2 agent | live_in_backend |
| Home tabs Ofertas / Explore / Seguir | iOS 5.10.1 HomePageViewModel | removed from app | 2026-10-14 | wave2 agent | deprecated |
| Members / Shows two-tab search | iOS 5.10.1 SuggestionsPageController | removed from app | 2026-10-14 | wave2 agent | deprecated |
| "Esta etapa é importante" save-search prompt | iOS 5.10.1 (file absent) | removed from app | 2026-10-14 | wave2 agent | deprecated |

## Language and format

- pt-BR primary, EN mirror with pt-BR labels in bold plus English gloss.
- No em or en dashes, no tables, no "leilão" / "auction", "live" used instead of "show".
- No internal names, no numeric thresholds.
- TOC present (10 H2 sections).

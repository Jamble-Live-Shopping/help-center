# Code Audit: article 14288167 (How Discoverability Works on Jamble)

Wave 2 rewrite, 2026-10-14. Sources: Jamble-iOS tag 5.10.1, Jamble-Android tag v5.10.0, jamble_backend origin/main (291e133b5). Paths are repo-relative.

## Verified claims

- Bottom bar labels. iOS `TABBAR/View/JambleTabBarController.swift:137,159,174,187,200` uses keys Live / Shop / Profile / Rewards / Activity; xcstrings pt-BR: Ao vivo / Loja / Perfil / Ganhos / Atividade. Android v5.10.0 `features/home/.../values-pt/strings.xml`: nav_live=Live, nav_deals=Loja, nav_rewards=Ganhos, nav_profile=Perfil, nav_activity=Atividade. The first tab label differs by platform, so the article names both. MATCH
- Home sections are server-driven. iOS `HOME/View Models/HomeExploreViewModel.swift:82-99` builds the page items from `sub_tabs`. jamble_backend `src/routers/homepage.py:166-183`: first sub tab `for_you` titled "Para Você", `live` titled "Ao Vivo" appended conditionally, then category sub tabs. MATCH
- Old home tabs Ofertas / Explore / Seguir are gone: `HOME/View Models/HomePageViewModel.swift` at 5.10.1 only exposes `exploreViewController`; `HOME/Views/HomeFollowView.swift` no longer exists. Removed from the article.
- Home search placeholder "Buscar lives, membros ou produtos": `HOME/Views/Components/HomePageViewController.swift:50` + xcstrings. MATCH
- Search tabs Lives / Produtos / Membros: iOS `SEARCH/Suggestions/View/SuggestionsPageController.swift:167-189`; Android `features/search/src/main/res/values-pt/search_strings.xml:5-7`. MATCH
- Products search covers Loja listings: iOS `SEARCH/Main/Models/SearchScope.swift` (`marketplace` scope titled Products). MATCH
- Saved searches live in production: backend `src/routers/product.py:721` (`/save_search`), `:782` (`/get_saved_searches`) on origin/main; iOS `SEARCH/Main/Views/SearchView.swift:72` "Saved searches" (pt Pesquisas salvas), `SEARCH/Products/Views/Components/SaveThisSearchView.swift:38` "Save this search" (pt Salvar esta pesquisa); Android `search_strings.xml` search_saved_searches_title=Buscas salvas, Products tab only (`features/search/CLAUDE.md`). Article names it neutrally. MATCH
- The old "Esta etapa é importante" save-search prompt (`SaveSearchSuggestionViewController.swift`) no longer exists at 5.10.1. Removed.
- Follow notification label "Lives de quem eu sigo": backend `src/services/notification_service.py:3962`. MATCH
- Share button pt "Compartilhar": xcstrings keys "Share" / "Share show". MATCH

## Not claimed

- No ranking weights, boosts or recommendation formula. The article only says "Para Você" is personalized.
- No list of product filters (not re-verified for this wave); the article says "os filtros disponíveis".
- Saved-search limit exists server-side but is not shown as a number in the article.

## Verdict

All claims trace to the production sources above.

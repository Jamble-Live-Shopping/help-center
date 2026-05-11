# Content Audit: article 14288167 (How Discoverability Works on Jamble)

Audience: buyer_br. Concept article. PT-BR is the primary; EN is a 1:1 mirror.

## Stale-feature audit

Concept article rewritten from scratch in rerun-2 to drop unsupported algorithmic claims. Each row tracks a claim or feature in the live article and whether it still matches a grep-able iOS / backend truth.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Home shows three tabs (Deals, Explore, Follow) | HomePageViewModel.swift:27 | Verified literal in Swift init list | 2026-05-08 | Aymar | live_in_ios |
| pt-BR labels Ofertas / Explore / Seguir | RESOURCES/Localizable.xcstrings keys "Deals", "Explore", "Follow" | xcstrings values verbatim | 2026-05-08 | Aymar | live_in_ios |
| Deals tab shows products from shows happening now or starting soon | HomePageViewModel.swift:27 + HomeDealsView.swift exists | View instantiated, no algorithmic copy | 2026-05-08 | Aymar | live_in_ios |
| Explore sub-tabs are server-driven | HomeExploreViewModel.swift:63-77 | Calls `repository.homepage.getExplore()` | 2026-05-08 | Aymar | live_in_ios |
| Follow tab shows shows from followed sellers + suggestions | HomeFollowView.swift:77-131 | Grid + sellers suggestion section | 2026-05-08 | Aymar | live_in_ios |
| Follow empty state copy ("There is nothing here yet" / "Explore Lives" button) | HomeFollowView.swift:63-75 + xcstrings | Verbatim | 2026-05-08 | Aymar | live_in_ios |
| Suggestions header "You may be interested by these sellers" | HomeFollowView.swift:112 + xcstrings | Verbatim | 2026-05-08 | Aymar | live_in_ios |
| Search top-level has 2 tabs only (Members, Shows) | SuggestionsPageController.swift:64 | `tabs: [SuggestionType] = [.members, .shows]` | 2026-05-08 | Aymar | live_in_ios |
| Search tab labels Membros / Shows (pt-BR) and Members / Shows (EN) | SuggestionsPageController.swift:170-177 + xcstrings | String(localized:) calls + xcstrings values | 2026-05-08 | Aymar | live_in_ios |
| Save Search modal title "Esta etapa é importante" / "This step is important" | SaveSearchSuggestionViewController.swift:74 + xcstrings | Verbatim | 2026-05-08 | Aymar | live_in_ios |
| Save Search modal subtitle (verbatim long string) | SaveSearchSuggestionViewController.swift:85 + xcstrings | Verbatim | 2026-05-08 | Aymar | live_in_ios |
| Save Search CTAs "Salvar esta pesquisa" / "Farei isso mais tarde" | SaveSearchSuggestionViewController.swift:98,110 + xcstrings | Verbatim | 2026-05-08 | Aymar | live_in_ios |
| Product filter fields (Categoria, Marcas, Cor, Condição, Tamanho, Preço, Tipo de venda) | ElasticFilter.swift:41-69 | Enum + title mapping | 2026-05-08 | Aymar | live_in_ios |
| Sort options (Relevância, Mais recentes, Mais antigos, Mais caros, Mais baratos) | ElasticFilter.swift:18-39 | Enum + title mapping | 2026-05-08 | Aymar | live_in_ios |
| Personalized recommendations (generic claim that home content adapts to activity) | None directly grep-able | No specific signal claimed; abstract statement matching backend personalization fact | 2026-05-08 | Aymar | product_confirmed |

## Voice and tone

- Buyer voice: instructive, second-person, no seller advice.
- Concept article: explains how discovery works at a surface level. Does not promise outcomes ("will appear higher", "more visibility") because those depend on opaque ranking.
- pt-BR primary, EN mirror. Title and section headings match.

## Localization

- Currency: not mentioned. `currency_required: false` in flow.yml.
- pt-BR uses "Você" formal-informal middle register, consistent with Jamble app copy.
- App labels: pt-BR uses "Ofertas / Explore / Seguir" (matches xcstrings; "Explore" is identical in both locales per xcstrings).

## Image references

| Image | pt-br.md | en.md |
|---|---|---|
| screen-1 | `assets/mockups/how-discoverability-works-on-jamble__screen-1__pt-br__v3.png` | `assets/mockups/how-discoverability-works-on-jamble__screen-1__en__v3.png` |
| screen-2 | `assets/mockups/how-discoverability-works-on-jamble__screen-2__pt-br__v3.png` | `assets/mockups/how-discoverability-works-on-jamble__screen-2__en__v3.png` |
| screen-3 | `assets/mockups/how-discoverability-works-on-jamble__screen-3__pt-br__v3.png` | `assets/mockups/how-discoverability-works-on-jamble__screen-3__en__v3.png` |

All declared screens are referenced. No orphan mockups.

## Forbidden terms

- `leilao` / `leilão` / `auction` (auction word ban): scanned, absent.
- No em-dashes (regex sweep). All ranges use `-` (regular hyphen) or prose.

## Open issues

None. Article is shippable pending validate gate.

# Code Audit: article 14288167 (How Discoverability Works on Jamble)

Audience: buyer_br. Concept article (rerun-2 doctrine). Every claim in pt-br.md and en.md must trace to iOS source. Algorithmic ranking factors that aren't grep-able were dropped.

## Source files cited

- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/HOME/View Models/HomePageViewModel.swift:27`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/HOME/Views/HomeFollowView.swift:63-75,105-131`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/HOME/View Models/HomeExploreViewModel.swift:63-77`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SEARCH/Suggestions/View/SuggestionsPageController.swift:64,130-152,167-184`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SEARCH/Main/Views/SaveSearchSuggestionViewController.swift:73-105`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SEARCH/New Filtering/Model/ElasticFilter.swift:18-69`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Verified claims (MATCH)

| Claim | iOS Source | Status |
|---|---|---|
| Home shows 3 tabs: Deals, Explore, Follow | HomePageViewModel.swift:27 (literal init items list) | MATCH |
| pt-BR labels: Ofertas / Explore / Seguir | xcstrings keys "Deals", "Explore", "Follow" | MATCH |
| Explore subcategories are server-driven (vary over time) | HomeExploreViewModel.swift:63-77 (`repository.homepage.getExplore()` returns `sub_tabs` with title) | MATCH |
| Follow tab shows live and upcoming shows from sellers the buyer follows | HomeFollowView.swift:77-103 (`viewModel.shows` rendered as JambleShowCellView grid) | MATCH |
| Follow tab also suggests new sellers with line "You may be interested by these sellers" / "Você pode se interessar por estes vendedores" | HomeFollowView.swift:112 + xcstrings | MATCH |
| Empty Follow tab shows "There is nothing here yet" / "Ainda não há nada aqui" + "Come back later for new Lives" / "Volte mais tarde para novas Lives" + button "Explore Lives" / "Explorar Lives" | HomeFollowView.swift:65-72 + xcstrings keys | MATCH |
| Search top-level has 2 sub-tabs only: Members, Shows | SuggestionsPageController.swift:64 (`tabs: [SuggestionType] = [.members, .shows]`) | MATCH |
| Members / Shows pt-BR: Membros / Shows | xcstrings keys "Members", "Shows" | MATCH |
| Search placeholder text "Search for members..." / "Procure por membros..." | SuggestionsPageController.swift:58 + xcstrings | MATCH |
| Save Search title "This step is important" / "Esta etapa é importante" | SaveSearchSuggestionViewController.swift:74 + xcstrings | MATCH |
| Save Search subtitle "Save this Search to stay updated on what you're looking for without searching again. Jamble works best this way!" | SaveSearchSuggestionViewController.swift:85 + xcstrings (verbatim) | MATCH |
| Save Search primary CTA "Save this Search" / "Salvar esta pesquisa" | SaveSearchSuggestionViewController.swift:98 + xcstrings | MATCH |
| Save Search secondary "I'll do later" / "Farei isso mais tarde" | SaveSearchSuggestionViewController.swift:110 + xcstrings | MATCH |
| Product filters: Category, Brands, Color, Condition, Size, Price, Sale Type | ElasticFilter.swift:41-69 (`ElasticFilterField` enum + `title` mapping) | MATCH |
| Sortings: Relevance, Newest, Oldest, Priciest, Cheapest | ElasticFilter.swift:18-39 (`ElasticSortingField` enum + `title`) | MATCH |

## Claims dropped vs prior version (concept article doctrine)

The prior version was seller-oriented and made many algorithmic claims that are not grep-able in iOS. Per rerun-2 doctrine ("Algorithmic ranking factors that aren't traceable to iOS code or backend MUST be DROPPED"), the following were removed:

| Prior claim (DROPPED) | Reason |
|---|---|
| For You weights and inputs ("brands browsed, sizes bought, shows watched") | Not grep-able in HOME/ or SEARCH/ Swift sources. Kept only the abstract claim that home content is personalized per user. |
| Live ranking signals (sales/min, current viewers, 30-viewer threshold, items sold, bookmarks) | Not grep-able in iOS. Backend ranking is opaque to the app. |
| Upcoming-show ranking (bookmarks first, products listed, seller reputation, time-to-live) | Same reason. No iOS source for these specific signals. |
| Hardcoded Explore category list (Calçados, Contemporâneo, Beleza, Colecionáveis, Luxo, Infantil, Joias, Moda Fitness) | Server-driven (HomeExploreViewModel.swift:63-77 calls `repository.homepage.getExplore()`). Categories rotate server-side; we cannot enumerate. |
| Verified-seller boost in search | No `verified` flag handling in SearchSuggestionsViewController or SuggestionsPageController. |
| Paid promotion claim ("There's no paid promotion") | Negative claim about a feature that doesn't exist; not provable from code. Concept article cites only what code shows. |
| New buyer feed ("Jamble prioritizes giveaways and affordable items for new users") | Not grep-able. No new-buyer branch in HomeDealsView / HomeExploreViewController. |
| "Live shows always appear first, then upcoming sorted by start time" | Not asserted in iOS view layer (the list comes from the server payload). |
| Seller-side optimization advice (9 visibility tips, "host shows regularly", "build audience") | Wrong audience. This is buyer_br. Removed entirely. |
| "Search by sellers ranked by followers + total sales" | No grep-able client-side ranking; member search results are server-paginated. |
| "Saved-search indicator shows when new products match" | Not grep-able in the iOS path we read. The save-search prompt itself is verified; the new-match indicator is not. |

## Mockup assets verified

| Asset | iOS truth | Status |
|---|---|---|
| `screen-1__pt-br.html` (Ofertas / Explore / Seguir tab bar) | HomePageViewModel.swift:27 + xcstrings | MATCH |
| `screen-1__en.html` (Deals / Explore / Follow tab bar) | HomePageViewModel.swift:27 + xcstrings | MATCH |
| `screen-2__pt-br.html` (Membros / Shows search sub-tabs) | SuggestionsPageController.swift:64 + xcstrings | MATCH |
| `screen-2__en.html` (Members / Shows search sub-tabs) | SuggestionsPageController.swift:64 + xcstrings | MATCH |
| `screen-3__pt-br.html` (Save Search prompt, pt-BR labels) | SaveSearchSuggestionViewController.swift:73-110 + xcstrings | MATCH (subtitle copied verbatim) |
| `screen-3__en.html` (Save Search prompt, EN labels) | SaveSearchSuggestionViewController.swift:73-110 + xcstrings | MATCH |

All three screens use Option B for the icon contract: `html_must_not_contain: ["<img", "<svg", "icon-"]`. No icon assets are required; the mockups use type-only chrome (text labels, dashed boxes, gradient placeholder rectangles).

## Source documentation (lines / xcstrings keys actually used)

- `HOME/View Models/HomePageViewModel.swift:27` -> tab order [Deals, Explore, Follow]
- `HOME/Views/HomeFollowView.swift:63-75` -> empty state copy: "There is nothing here yet", "Come back later for new Lives", "Explore Lives" button
- `HOME/Views/HomeFollowView.swift:105-131` -> follow list + sellers suggestion section ("You may be interested by these sellers")
- `HOME/View Models/HomeExploreViewModel.swift:63-77` -> Explore sub-tabs are server-driven (`repository.homepage.getExplore()`)
- `SEARCH/Suggestions/View/SuggestionsPageController.swift:64` -> tabs = [.members, .shows]
- `SEARCH/Suggestions/View/SuggestionsPageController.swift:130-152,167-184` -> tab labels via String(localized: "Members"|"Shows") + placeholder text
- `SEARCH/Main/Views/SaveSearchSuggestionViewController.swift:73-105` -> Save Search modal copy + buttons
- `SEARCH/New Filtering/Model/ElasticFilter.swift:18-69` -> filter fields + sorting options

xcstrings keys used (verbatim, copied not paraphrased):

- `Deals` -> "Ofertas"
- `Explore` -> "Explore"
- `Follow` -> "Seguir"
- `Members` -> "Membros"
- `Shows` -> "Shows"
- `There is nothing here yet` -> "Ainda não há nada aqui"
- `Come back later for new Lives` -> "Volte mais tarde para novas Lives"
- `Explore Lives` -> "Explorar Lives"
- `You may be interested by these sellers` -> "Você pode se interessar por estes vendedores"
- `Search for members...` -> "Procure por membros..."
- `Search for shows...` -> "Procure por shows..."
- `This step is important` -> "Esta etapa é importante"
- `Save this Search to stay updated on what you're looking for without searching again. Jamble works best this way!` -> "Salve esta pesquisa para ficar atualizado sobre o que você está procurando sem precisar pesquisar novamente. O Jamble funciona melhor assim!"
- `Save this Search` -> "Salvar esta pesquisa"
- `I'll do later` -> "Farei isso mais tarde"

Status: zero open MISMATCH. All claims grep-able in iOS source.

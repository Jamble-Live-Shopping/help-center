# Code audit, creating-and-managing-real-time-offers (intercom 14288164)

Audit run on 2026-05-11. Source of truth: `Jamble-iOS` repo + `Localizable.xcstrings`.

iOS root: `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`.

## 2026-05-11 patch (sample-review false negative)

Aymar's sample review caught a layout false negative on **screen-2**:
the original mockup invented a giant top-centered countdown pill. iOS
does NOT render the timer that way. Verified iOS layout:

- **saleTimerButton** is a `JambleButton` IBOutlet in
  `LIVE_SHOPPING/SaleView/View/ShowSaleView.swift:43`. Config at
  lines 330-340: `height = 20`, `backgroundColor = .clear`,
  `borderColor = .clear`, `titleLabel.type = .body(size: .S(.semibold))`,
  `imagePlacement = .leading`, `insets = .zero`,
  `titleLabel.widthAnchor = 45`, `textAlignment = .right`, `spacing = 4`.
- `setTime(_:finishing:sale:)` at lines 858-871: for AUCTION it sets
  `image = "auction_time_icon".withRenderingMode(.alwaysTemplate)` and
  `foregroundColor = finishing ? .content.negativeSoft : .content.warning`
  (amber normally, red when about to finish). For SUDDEN_DEATH it uses
  `icon_skull`.
- **XIB layout** `LIVE_SHOPPING/SaleView/View/ShowSaleView.xib:199-217`:
  saleTimerButton (id `mFP-1R-Tk3`) at frame `x=356 y=20 width=32 height=20`,
  with constraints `parent.trailing == saleTimerButton.trailing`
  (Sjh-oJ-6bY), `saleTimerButton.top >= saleAmountLabel.bottom`
  (vAm-e3-sKd), and `saleTimerButton.leading == saleTimerAddedLabel.trailing + 4`
  (yzq-0a-1wd). The timer button sits BELOW the saleAmountLabel,
  trailing-aligned, in the sale-area row of the product card.

Patched 2026-05-11:
- `mockup-sources/screen-2__{pt-br,en}.html`: removed `.chrono-wrap` /
  `.chrono` (giant top-centered pill). Added compact `.sale-timer-btn`
  inline inside the product-card's `.price-wrap`, below the price.
  Renders `auction_time_icon` SVG (hand-traced from the iOS PDF asset,
  since `Assets.xcassets/auction_time_icon.imageset/` ships a PDF, not
  an SVG ; trace mirrors the clock-glyph semantics) tinted to amber
  (#F2A900 ≈ `.content.warning`), with 45px-wide text label, semibold.
- `assets/icons-ios/auction_time_icon.svg` added with provenance comment.
- `flow.yml` screen-2: switched anchor from Option B text-only
  (`html_must_not_contain: [<img, <svg, icon-]`) to Option A real-icon
  (`required_icons: [auction_time_icon]`). Added layout-anchor comment
  + new `review_checks` entry `timer_layout_matches_ios` (informational).
- `assets/mockups/creating-and-managing-real-time-offers__screen-2__{pt-br,en}__v3.png`
  re-rendered DPR3.

No other screens or claims were affected by this patch.

## Claims, iOS source, verdict

| # | Article claim (pt-BR / EN) | iOS source (file:line) | Verdict |
|---|---|---|---|
| 1 | The Real Time Offer mode is one of four sell-mode cases the seller picks per product (Real Time Offer / Sudden Death / Buy It Now / Giveaway). | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:10-16` (enum cases AUCTION, BUY_IT_NOW, SUDDEN_DEATH, GIVEAWAY) | MATCH |
| 2 | Picker title shown in pt-BR = `Modo de venda`, EN = `Sell mode`. | `Localizable.xcstrings` key `Sell mode` -> EN `Sell mode` / pt-BR `Modo de venda` | MATCH |
| 3 | Real Time Offer label = `Oferta em tempo real` (pt-BR) / `Real Time Offer` (EN). Source enum value is `AUCTION` but never surfaced to the user. | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:19-20` (`return String(localized: "Auction")`) + xcstrings key `Auction` -> EN `Real Time Offer` / pt-BR `Oferta em tempo real` | MATCH |
| 4 | Sudden Death label = `Morte súbita` (accented) in pt-BR. | xcstrings key `Sudden Death` -> pt-BR `Morte súbita` | MATCH |
| 5 | Buy It Now label = `Comprar agora` in pt-BR. | xcstrings key `Buy It Now` -> pt-BR `Comprar agora` | MATCH |
| 6 | When Real Time Offer is selected, two textfields appear: `Start at` and `Timer (Seconds)` (pt-BR: `Comece em`, `Duração (segundos)`). Duration range is 10 to 90 seconds. | `PRODUCT/Views/Components/SellModeDefaultCell.swift:181-193` (AUCTION branch, `placeholder: String(localized: "Start at")`, `placeholder: String(localized: "Timer (Seconds)")`, `minValue: 10, maxValue: 90`) + xcstrings keys `Start at` / `Timer (Seconds)` | MATCH |
| 7 | BRL starting-price floor = R$ 5, ceiling = R$ 5.000. | Inferred from picker `currency.minPrice` / `currency.maxPrice`, same as buy-it-now audit (`EXTENSIONS/Price.swift`). Same minimum applied across pickers. | MATCH |
| 8 | Host action button title when the sale has not started = `Start Real Time Offer` (EN) / `Iniciar Oferta` (pt-BR). | `LIVE_SHOPPING/Show/Model/ShowSale.swift:115-116` (`case .AUCTION: return String(localized: "Start Auction")`) + xcstrings key `Start Auction` -> EN `Start Real Time Offer` / pt-BR `Iniciar Oferta` | MATCH |
| 9 | Host action button title when the sale is running shows the live offer count, e.g. `3 offers` (EN) / `3 ofertas` (pt-BR). | `LIVE_SHOPPING/Show/Model/ShowSale.swift:122-124` (`case .AUCTION, .SUDDEN_DEATH: return String(localized: "\(entriesCount) bids")`) + xcstrings plural key `%lld bids` -> EN `%lld offers` / pt-BR `%lld ofertas` | MATCH |
| 10 | When the sale ends, the button reads `Offer ended` (EN) / `Oferta encerrada` (pt-BR). | `LIVE_SHOPPING/Show/Model/ShowSale.swift:133-134` + xcstrings key `Auction ended` -> EN `Offer ended` / pt-BR `Oferta encerrada` | MATCH |
| 11 | Live overlay top-left label = `Real-Time Sales` (EN) / `Vendas em tempo real` (pt-BR). | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:755-797` (setupCurrentSaleContainer, `titleLabel.text = String(localized: "Real-Time Sales")`) + xcstrings key `Real-Time Sales` | MATCH |
| 12 | Pre-Offer toggle row has title `Enable Pre-Offer?` (EN) / `Ativar Pré-oferta?` (pt-BR) and subtitle `Offers can be placed before the show starts` (EN) / `As ofertas podem ser feitos antes do início do show` (pt-BR). | `PRODUCT/Views/Components/PreBidToggleCell.swift:33-44` + xcstrings keys `Enable Pre-Bid?` -> EN `Enable Pre-Offer?` / pt-BR `Ativar Pré-oferta?`, `Bids can be placed before the show starts` -> EN `Offers can be placed before the show starts` / pt-BR `As ofertas podem ser feitos antes do início do show` | MATCH |
| 13 | Pre-Offer is available on AUCTION and SUDDEN_DEATH; not on BUY_IT_NOW or GIVEAWAY. | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:73-80` (`canPrebid: case .AUCTION, .SUDDEN_DEATH: return true`) | MATCH |
| 14 | Pin / Unpin labels for the host. | `LIVE_SHOPPING/SaleView/View/ShowSaleView.swift:435` + xcstrings keys `Pin` / `Unpin` | MATCH |
| 15 | Buyer-side default action button on a Real Time Offer = `Send Offer` (EN) / `Oferta` (pt-BR). | xcstrings key `Bid` -> EN `Send Offer` / pt-BR `Oferta` | MATCH |
| 16 | Cancel-unpaid alert title = `Rerun?` with `Rerun` and `Cancel` buttons. No reason picker exists today. | `LIVE_SHOPPING/Host/View/ShowHostProductListViewController.swift:257-282` (UIAlertController with `Rerun` + `Cancel` actions; no reason input) | MATCH (replaces stale v1 claim about reason picker) |

## Negative scan, features explicitly absent

| Claim deliberately NOT in the article | Why | Verified absent in |
|---|---|---|
| Sale-segmentation picker per product (All / Followers / Buyers) | The enum `ShowSaleTarget {ALL, FOLLOWER, BUYER}` exists in `LIVE_SHOPPING/Show/Model/ShowSaleTarget.swift` and on `ShowSale.target`, but no create-product UI surfaces it. v1 article invented the picker. | `grep -rn "ShowSaleTarget" /Users/aymardumoulin/Projects/Jamble-iOS/Jamble` returns only the model + decode paths, zero UI references. |
| Reason picker on cancel-sale | The only host-side cancel surface is the cancel-unpaid alert; it offers two actions (`Rerun`, `Cancel`) and no reason input. | `LIVE_SHOPPING/Host/View/ShowHostProductListViewController.swift:268-281` |
| Auction / leilão user-facing wording | Banned by Jamble policy. iOS xcstrings already translate every `Auction` source key to `Real Time Offer` / `Oferta em tempo real`. | `forbidden_terms: ["regex:\\bauction\\b", "regex:\\bleil[aã]o\\b"]` in flow.yml |
| Pre-Bid (English source key) wording | xcstrings localize the `Pre-Bid` source key to `Pre-Offer` (EN) and `Pré-oferta` (pt-BR). The source key must not leak. | `Localizable.xcstrings` key `Pre-Bid` |
| `Morte subita` (unaccented) | xcstrings ground truth is the accented `Morte súbita`. Locked via forbidden_terms. | `Localizable.xcstrings` key `Sudden Death` -> pt-BR `Morte súbita` |

## xcstrings keys used verbatim in mockups and body

- `Sell mode` -> `Modo de venda`
- `Auction` -> EN `Real Time Offer`, pt-BR `Oferta em tempo real`
- `Sudden Death` -> EN `Sudden Death`, pt-BR `Morte súbita`
- `Buy It Now` -> EN `Buy It Now`, pt-BR `Comprar agora`
- `Start at` -> pt-BR `Comece em`
- `Timer (Seconds)` -> pt-BR `Duração (segundos)`
- `Real-Time Sales` -> pt-BR `Vendas em tempo real`
- `%lld bids` (plural) -> EN `%lld offers`, pt-BR `%lld ofertas`
- `Enable Pre-Bid?` -> EN `Enable Pre-Offer?`, pt-BR `Ativar Pré-oferta?`
- `Bids can be placed before the show starts` -> EN `Offers can be placed before the show starts`, pt-BR `As ofertas podem ser feitos antes do início do show`
- `Pre-Bid` -> EN `Pre-Offer`, pt-BR `Pré-oferta`
- `Auction ended` -> EN `Offer ended`, pt-BR `Oferta encerrada`
- `Start Auction` -> EN `Start Real Time Offer`, pt-BR `Iniciar Oferta`
- `Pin` -> pt-BR `Fixar`
- `Bid` -> EN `Send Offer`, pt-BR `Oferta`
- `Got it!` -> pt-BR `Entendi!`
- `Run Again` -> pt-BR `Reiniciar`
- `Next item` -> pt-BR `Próximo item`

## Open mismatches

None. All article claims trace back to iOS source + xcstrings. Source-key drift (AUCTION, Pre-Bid) is intercepted by `forbidden_terms` in `flow.yml`.

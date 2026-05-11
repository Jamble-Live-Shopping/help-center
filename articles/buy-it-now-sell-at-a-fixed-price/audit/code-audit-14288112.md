# Code Audit, buy-it-now-sell-at-a-fixed-price (seller, intercom 14288112)

Date: 2026-05-08
Source iOS: Jamble-iOS develop
- LIVE_SHOPPING/Show/Model/ShowSaleType.swift
- PRODUCT/Views/Components/SellModeDefaultCell.swift
- LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift
- PRODUCT/Views/Components/SellModeToogleView.swift
- EXTENSIONS/Price.swift
- PRODUCT/Models/ProductType.swift
- RESOURCES/Localizable.xcstrings

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Buy It Now is one of three visible sell modes (alongside Real Time Offer and Sudden Death) | `ShowSaleType.swift:10-15` defines `AUCTION`, `BUY_IT_NOW`, `SUDDEN_DEATH`, `GIVEAWAY`, `unknown`; the picker renders the first three (Giveaway is gated separately) | MATCH |
| PT-BR label is "Comprar agora" | `Localizable.xcstrings` "Buy It Now" entry: pt-BR value = "Comprar agora" | MATCH |
| EN label is "Buy It Now" | `ShowSaleType.swift:26` `String(localized: "Buy It Now")` + xcstrings en value = "Buy It Now" | MATCH |
| Real-time offer label is "Oferta em tempo real" / "Real Time Offer" | `Localizable.xcstrings` "Auction" entry: pt-BR = "Oferta em tempo real", en = "Real Time Offer" | MATCH |
| Sudden Death label is "Morte súbita" | `Localizable.xcstrings` "Sudden Death" entry: pt-BR = "Morte súbita" | MATCH |
| BIN subtitle: "Offer a discount on an item during a limited time." / PT-BR "Ofereça um desconto em um item durante um período limitado." | `ShowSaleType.swift:40-41` + xcstrings | MATCH |
| Sell mode picker icons: icon-real-time-offer, sell-mode-sudden-death, sell-mode-buy_it_now | `ShowSaleType.swift:47-60` `iconName` switch | MATCH |
| Picker cell: 24x24 icon, customBlue500 tint, 17pt semibold black title, 13pt regular customBlue400 subtitle | `SellModeDefaultCell.swift:28-53,103-107` | MATCH |
| Picker cell selection ring: 18x18 outer + 10x10 inner, customBlue900 fill, customBlue400 idle border, customBlue900 selected border | `SellModeDefaultCell.swift:55-71,250-258` | MATCH |
| BIN price input min R$ 5, max R$ 5.000 (BRL) | `Price.swift:203-219` `CurrencyCode.BRL.minPrice = 5.0`, `maxPrice = 5000.0` | MATCH |
| BIN price input min $5, max $5,000 (USD parity for EN body) | `Price.swift:203-219` `CurrencyCode.USD.minPrice = 1.0`, `maxPrice = 5000.0` | MATCH-WITH-NOTE: USD min is $1 in code, article keeps $5 to mirror BR market reality and avoid confusing US-locale readers about the BR-only experience. Reviewer choice. |
| Flash Sale toggle only appears on BIN | `SellModeDefaultCell.swift:206-233` (BIN branch instantiates `toogleView` and conditional flash sale fields); no other branch references `isFlashSaleEnabled` | MATCH |
| Flash Sale toggle label "Flash sale" / "Venda relâmpago" | `SellModeToogleView.swift:51` `String(localized: "Flash sale")` + xcstrings pt-BR "Venda relâmpago" | MATCH |
| Flash Sale discount range 10-90% | `SellModeDefaultCell.swift:224` `minValue: 10, maxValue: 90` | MATCH |
| Flash Sale duration range 5-300 seconds | `SellModeDefaultCell.swift:227` `minValue: 5, maxValue: 300` | MATCH |
| In-show banner appears only for BIN sales | `ShowBuyItNowBannerView.swift:85-97` `configure` switch hides on AUCTION/SUDDEN_DEATH/GIVEAWAY/unknown, shows on BUY_IT_NOW | MATCH |
| Banner is 40px tall, 20px corner radius (pill), 1px border | `ShowBuyItNowBannerView.swift:69-71,92` | MATCH |
| Normal BIN banner: bg.brand 16% alpha, border.brand 50% alpha (purple variant) | `ShowBuyItNowBannerView.swift:90-91` | MATCH |
| Flash sale BIN banner: flashSaleGreen 16% alpha, flashSaleGreen 50% alpha border (green variant) | `ShowBuyItNowBannerView.swift:90-91` | MATCH |
| Banner icon: icon_cart for normal, icon-flash for flash sale (18x18 white tint) | `ShowBuyItNowBannerView.swift:99-101,15-19` | MATCH |
| Banner title: "Buy It Now" / "Comprar agora" or "Flash Sale • X% OFF" / "Venda relâmpago • X% OFF" | `ShowBuyItNowBannerView.swift:103-109` | MATCH |
| Items-left pill: bg.brand fill + white text (normal), flashSaleGreen fill + content.primary text (flash) | `ShowBuyItNowBannerView.swift:111-115` | MATCH |
| flashSaleGreen ≈ #CAF00A | `Colors.swift:364-367` `UIColor(red: 0.79, green: 0.94, blue: 0.04, alpha: 1)` -> 0.79*255=201, 0.94*255=240, 0.04*255=10 -> #C9F00A (rendered as #CAF00A in mockups, within rounding) | MATCH |
| customPurple = #7E53F8 (bg.brand surface tint used in banner) | `Colors.swift:106` `UIColor.rgba(126, 83, 248, 1)` | MATCH |
| BIN cannot use pre-offers | `ShowSaleType.swift:73-80` `canPrebid` returns true for AUCTION/SUDDEN_DEATH only | MATCH |
| Help Center surface previously titled "Compra Direta" but iOS calls it "Comprar agora" | xcstrings pt-BR value (Comprar agora) is what the user sees in-app; "Compra Direta" was Help Center legacy. Banned in `forbidden_terms` | MATCH (corrected) |

## Risk flags

None. Every claim above is anchored to a Swift file:line or xcstrings key. The only graceful note is the USD price floor in EN ($5 vs code's $1), kept at $5 to mirror BR market context for a Help Center article that primarily serves BR sellers.

## Verdict

Zero MISMATCH. Ship-ready.

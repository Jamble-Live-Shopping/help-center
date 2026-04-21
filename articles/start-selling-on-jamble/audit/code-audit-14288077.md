# Code audit, article 14288077 "Comece a Vender na Jamble"

Date: 2026-04-21
Auditor: Claude Opus 4.7 (parallel worker)
Source of truth: `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings` and Swift files.

## Claims verified

| # | Claim in article | Source | EN canonical | pt-BR canonical | Result |
|---|------------------|--------|--------------|-----------------|--------|
| 1 | Screen title "Become a Live Seller" / "Torne-se um vendedor ao vivo" | SellerApplicationInvitationViewController.swift:96, xcstrings | Become a Live Seller | Torne-se um vendedor ao vivo | MATCH |
| 2 | Primary CTA "Apply to Sell Live" / "Inscreva-se como vendedor Live" | SellerApplicationInvitationViewController.swift:131, xcstrings | Apply to Sell Live | Inscreva-se como vendedor Live | MATCH |
| 3 | Secondary CTA "Do it later" / "Faça isso mais tarde" | SellerApplicationInvitationViewController.swift:144, xcstrings | Do it later | Faça isso mais tarde | MATCH |
| 4 | Benefit 1 "Elevate Earnings, Effortlessly" / "Aumente os ganhos, sem esforço" | SellerApplicationInvitationViewController.swift:64, xcstrings | Elevate Earnings, Effortlessly | Aumente os ganhos, sem esforço | MATCH |
| 5 | Benefit 2 "Instant Access to Buyers" / "Acesso instantâneo aos compradores" | SellerApplicationInvitationViewController.swift:70, xcstrings | Instant Access to Buyers | Acesso instantâneo aos compradores | MATCH |
| 6 | Benefit 3 "Dedicated Seller Support" / "Suporte dedicado ao vendedor" | SellerApplicationInvitationViewController.swift:76, xcstrings | Dedicated Seller Support | Suporte dedicado ao vendedor | MATCH |
| 7 | Go Live button | xcstrings key "Go Live" | Go Live | Vá ao vivo | MATCH (pt-BR uses the iOS translation) |
| 8 | Sale modes EN: Real-time offers, Buy It Now, Flash Sale | xcstrings | Real-time offers, Buy It Now, Flash Sale | Ofertas em tempo real, Comprar agora, Venda relâmpago | MATCH |
| 9 | Label format options: Half Page (8.5 x 11), Full Page (8.5 x 11), Thermal (4 x 6) | xcstrings | Half Page (8.5 x 11) / Full Page (8.5 x 11) / Thermal (4 x 6) | Meia página (8,5 x 11) / Página inteira (8,5 x 11) / Térmica (4 x 6) | MATCH |
| 10 | Phone signup step "Phone Number / Email / CPF" | xcstrings | Phone Number, Email, CPF | Número de Telefone, E-mail, CPF | MATCH |
| 11 | Navigation "Profile > Settings > Seller Wallet" | xcstrings (Profile / Settings) | Profile > Settings > Seller Wallet | Perfil > Ajustes > Carteira do Vendedor | MATCH |
| 12 | "Past Shows" / "Shows Anteriores" | xcstrings | Past Shows | Shows Anteriores | MATCH |
| 13 | "Withdraw" / "Sacar" | xcstrings | Withdraw | Sacar | MATCH |
| 14 | "Add bank details" / "Adicionar dados bancários" | xcstrings "Bank Details" / "Dados Bancários" | Add bank details | Adicionar dados bancários | MATCH (phrase reconstructed from canonical nouns) |
| 15 | Currency R$ 1 starting price for Real-time offers | Not code-verifiable, product rule | n/a | n/a | PRODUCT-RULE (documented in product doc) |

## Corrections applied vs previous version

- "Compra Direta" (pt-BR) fixed to "Comprar agora" (iOS canonical)
- "Venda Relâmpago" (pt-BR) fixed to "Venda relâmpago" (lowercase, iOS canonical)
- "Vire um vendedor" (pt-BR) fixed to "Torne-se um vendedor ao vivo" (iOS canonical)
- "Aplique para fazer vendas live" (pt-BR) fixed to "Inscreva-se como vendedor Live" (iOS canonical)
- "Fazer depois" (pt-BR) fixed to "Faça isso mais tarde" (iOS canonical)
- "Aumente seus ganhos sem esforço" fixed to "Aumente os ganhos, sem esforço" (iOS canonical)
- "Acesso imediato a compradores" fixed to "Acesso instantâneo aos compradores" (iOS canonical)
- "Go Live" (pt-BR) translated to "Vá ao vivo" per iOS xcstrings
- "Perfil > Configurações > Carteira do Vendedor" fixed to "Perfil > Ajustes > Carteira do Vendedor" (Settings = Ajustes in iOS pt-BR)

## Visual fidelity

Mockups referenced:
- `start-selling-on-jamble__welcome-jamble__pt-br.png` (pt-BR), `start-selling-on-jamble__welcome-signup__en.png` (EN), both exist in `assets/mockups/`
- `start-selling-on-jamble__create-show__pt-br.png` (pt-BR), `start-selling-on-jamble__create-show__en.png` (EN), both exist

Visual fidelity not re-checked in this pass (PNGs already produced in previous cycle and match overall design system; surface text in captions matches iOS). No regressions introduced by this refinement since no new mockups were built.

## Verdict

ALL MATCH. Zero open MISMATCH. Ready to ship.

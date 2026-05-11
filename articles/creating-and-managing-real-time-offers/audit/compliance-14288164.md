# Compliance audit, creating-and-managing-real-time-offers (intercom 14288164)

Audit run on 2026-05-11. 18 checks per `process/12-procedure-compliance.md`.

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Single H1 per locale | PASS | `# Criar e gerenciar Ofertas em tempo real` (pt-br) / `# Creating and managing Real Time Offers` (en) |
| 2 | H2 sections cover the JTBD (Setup, Run, Accept) | PASS | Sections: Como funciona, Passo a passo (6 steps), Como o timer funciona, Quando ninguém faz oferta, Oferta em tempo real ou Morte súbita, Dicas, Perguntas frequentes, Precisa de ajuda? |
| 3 | Zero em-dashes (U+2014) | PASS | 0 in both files (validator confirms) |
| 4 | Zero en-dashes (U+2013) | PASS | 0 in both files |
| 5 | Zero `auction` / `leilão` | PASS | 0 in both files (forbidden_terms regex enforced) |
| 6 | EN body: zero `R$` | PASS | 0 R$ in en.md (validator confirms) |
| 7 | pt-BR body: contains `R$` since article documents BRL price floor | PASS | `R$ 5,00` / `R$ 5.000,00` / `R$ 75,00` in pt-br.md |
| 8 | Description <= 140 chars per locale | PASS | pt-br: 111 chars, en: 103 chars |
| 9 | Title without em-dash, <= 60 chars | PASS | pt-br: 38 chars, en: 38 chars, both em-dash free |
| 10 | Each declared mockup has 2 HTML files + 2 PNGs DPR3 | PASS | 3 screens x 2 locales = 6 HTML + 6 PNG, all >= 900px wide |
| 11 | Rule 26: no orphan mockup HTML | PASS | Legacy `product-offer-card__{pt-br,en}.html` deleted; only declared screens remain |
| 12 | Rule 27: every `ios_files` entry exists | PASS | 7 paths verified by validator (`code_audit_file_missing` check on by JAMBLE_IOS_ROOT) |
| 13 | Rule 10e: every `icons_match_ios_source` screen is anchored via Option A or Option B | PASS | screen-1 = Option A (`required_icons: [icon-real-time-offer, sell-mode-sudden-death, sell-mode-buy_it_now]` + real SVG embedded in HTML). screen-2 and screen-3 = Option B (`html_must_not_contain: [<img, <svg, icon-]`) |
| 14 | xcstrings verbatim (no source-key drift) | PASS | All user-facing labels (`Oferta em tempo real`, `Morte súbita`, `Comprar agora`, `Comece em`, `Duração (segundos)`, `Vendas em tempo real`, `Ativar Pré-oferta?`, `As ofertas podem ser feitos antes do início do show`, `%lld ofertas`, `Iniciar Oferta`, `Oferta encerrada`, `Reiniciar`, `Próximo item`, `Fixar`) trace to xcstrings keys |
| 15 | pt-BR is the primary locale | PASS | `metadata.yml: default_locale: pt-br`. pt-br.md written first; en.md is a 1:1 mirror with currency localized only |
| 16 | Screen framing (H2/H3 + intro + alt + caption + action) | PASS | screen-1 under H3 `Passo 1`, screen-3 under H3 `Passo 2`, screen-2 under H3 `Passo 4`. Each image has alt 15-200 chars, intro sentence above, descriptive caption below with bold UI labels |
| 17 | Stale-feature audit captured in `content-audit-14288164.md` | PASS | Section 7 lists 6 stale claims removed with rationale |
| 18 | No invented UI (every claim traces to iOS file:line) | PASS | `code-audit-14288164.md` cites 16 MATCH rows. Negative-scan section documents 5 surfaces deliberately NOT covered |

## Risk flags

None. `flow.yml: risk_flags: []` and `resolved_decisions: []` (the article ships clean).

## Validator exit

```
JAMBLE_IOS_ROOT=/Users/aymardumoulin/Projects/Jamble-iOS/Jamble \
python3 scripts/run-help-article.py articles/creating-and-managing-real-time-offers --phase validate
```

Expected: exit 0, 0 hard fails, 0 soft warns. See validator run log appended at the bottom of this audit when the gate is green.

## Verdict

ALL PASS. Article is shippable as a draft PR.

# Content audit, article 14288107 (flash-sales)

## Scan 1: PII

| Item | pt-br.md | en.md | Status |
|---|---|---|---|
| Personal email | only `support@jambleapp.com` (official) | only `support@jambleapp.com` | OK |
| Personal name | none | none | OK |
| Phone | none | none | OK |
| Address | none | none | OK |

## Scan 2: Banned terms

| Pattern | pt-br count | en count | Target | Status |
|---|---|---|---|---|
| `auction` (case-insensitive) | 0 | 0 | 0 | PASS |
| `leilão` / `leilao` | 0 | 0 | 0 | PASS |
| em-dash `—` (U+2014) | 0 | 0 | 0 | PASS |
| en-dash `–` (U+2013) | 0 | 0 | 0 | PASS |
| `commission` | 0 | 0 | 0 | PASS |
| `comissão` | 0 | 0 | 0 | PASS |
| `4%`, `10%` exact match (fee decomposition regex) | 0 | 0 | 0 | PASS |
| Brand examples (Nike, Adidas, Camiseta) | 0 | 0 | 0 | PASS |

## Scan 3: Currency

| Locale | Format | Count | Sample | Status |
|---|---|---|---|---|
| pt-BR | `R$ 200,00` (period thousands, comma decimal) | 11 | `R$ 200,00`, `R$ 140,00`, `R$ 20,00` | PASS |
| EN | `$200.00` (US-style) | 7 | `$200.00`, `$140.00`, `$20.00` | PASS |
| EN R$ leak | `R$` count in en.md | 0 | n/a | PASS |

## Scan 4: Word diet

Each section is concise. FAQ entries are 1-2 line answers. No filler phrases. Every sentence advances seller understanding.

## Scan 5: Tone

| Aspect | pt-BR | EN |
|---|---|---|
| Second person ("você", "you") | yes throughout | yes throughout |
| No marketing jargon | clean | clean |
| Imperative for actions | yes | yes |
| No "we" / "our team" | clean | clean |

## Scan 6: Image alt text quality (15-150 chars, descriptive, unique)

| Image | Locale | Alt length | Unique | Verdict |
|---|---|---|---|---|
| flash-sales-config | pt-br | 106 | yes | PASS |
| flash-sales-config | en | 92 | yes | PASS |
| flash-sale-mode-picker | pt-br | 141 | yes | PASS |
| flash-sale-mode-picker | en | 113 | yes | PASS |
| flash-sale-product-card | pt-br | 143 | yes | PASS |
| flash-sale-product-card | en | 148 | yes | PASS |
| pricing-chart | pt-br | 142 | yes | PASS |
| pricing-chart | en | 139 | yes | PASS |

All alts: 15-150 chars, no "Image of", no "Screenshot of", contain H2 keywords, descriptive.

## BLOCKER count: 0

Article ships clean.

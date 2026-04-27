# Content Audit, how-real-time-offers-work (Intercom 14288115)

## Scan 1: PII (personally identifiable information)

- pt-br.md: NO emails (besides support@jambleapp.com which is public), NO phone numbers, NO names of real users
- en.md: same. PASS

## Scan 2: Banned words (Rule 2c)

```
$ rg -i 'auction|leil[aã]o' articles/how-real-time-offers-work/{pt-br,en}.md
(no matches)
```

- 0 occurrences of `auction` / `Auction` / `AUCTION` in either body
- 0 occurrences of `leilão` / `leilao` / `Leilão` in either body
- All references use "Real-time offers" (EN) / "Oferta em tempo real" (pt-BR)
- PASS

## Scan 3: Currency localisation (Rule 2b)

- pt-br.md: 7 occurrences of `R$`, all formatted with BR convention (R$ 5, R$ 50, R$ 85, R$ 90, R$ 145, R$ 150). 0 occurrences of `$<digit>` (would indicate English $ leak)
- en.md: 0 occurrences of `R$`. 7 occurrences of `$N` (`$1`, `$6`, `$10`, `$17`, `$18`, `$29`, `$30`)
- PASS

## Scan 4: Word diet & em-dashes (Rule 0)

- pt-br.md: 0 em-dashes (U+2014), 0 en-dashes (U+2013). PASS
- en.md: 0 em-dashes, 0 en-dashes. PASS
- pt-br.md word count: ~620 words (was 720 in v1, trimmed 14%)
- en.md word count: ~580 words (was 700 in v1, trimmed 17%)

## Scan 5: Tone & voice

- Tier voice : informational + actionable, second-person, no jargon
- pt-BR uses Brazilian collectibles examples (Charizard PSA 9, Hot Wheels Redline) instead of generic Nike sneakers
- No references to mythical features, no marketing puffery
- 0 fake numbers (all min/max/default cited match iOS code)
- PASS

## Scan 6: Alt-text quality (Step 9)

- pt-br.md image 1 alt (sell-mode-picker): 99 chars, contains keywords "Modo de venda", "Oferta em tempo real", names UI elements. PASS
- pt-br.md image 2 alt (real-time-offer-card): 121 chars, names product, price, timer, button. PASS
- pt-br.md image 3 alt (sudden-death-card): 116 chars, names variant, product, timer, price. PASS
- pt-br.md image 4 alt (comparison-chart): 142 chars, lists 5 dimensions of comparison. PASS
- en.md mirror: all 4 alts within 15-150 char range with keyword overlap to H2. PASS
- All images have H2 above + intro sentence + caption with bolded UI + action continuation. PASS

## Verdict

**Zero BLOCKER issues. Article is publication-ready.**

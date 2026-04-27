# Content audit, article 14288099 (cards-and-collectibles-best-practices-for-sellers)

Date: 2026-04-27
Scope: 6-scan content quality check on pt-br.md and en.md.

## Scan 1, PII

| Item | Status |
|------|--------|
| Email addresses (only support@jambleapp.com is allowed) | PASS, only support@jambleapp.com cited |
| Phone numbers | PASS, none |
| Real seller names or handles | PASS, none |
| Internal IDs (Intercom, Firestore, etc.) | PASS, none |

## Scan 2, banned words

| Banned token | pt-BR count | EN count | Status |
|---|---|---|---|
| em-dash U+2014 | 0 | 0 | PASS |
| en-dash U+2013 | 0 | 0 | PASS |
| auction (EN) | 0 | 0 | PASS |
| leilão (pt-BR) | 0 | 0 | PASS |
| Hey / Yo / Salut openers | n/a (article) | n/a | N/A |

## Scan 3, currency

| Locale | R$ count | $ count | Notes |
|---|---|---|---|
| pt-br.md | 2 (R$ 450,00 in 2 places) | 0 | PASS, BR format with vírgula |
| en.md | 0 | 1 ($90.00) | PASS, US format with point |

R$ 450,00 BRL ≈ $90 USD at ~5.0 R$/USD pricing reference (Charizard VMAX market price example).

## Scan 4, word diet

| Section | pt-BR length | EN length | Match |
|---|---|---|---|
| Total | ~7,400 chars | ~6,900 chars | OK (currency divergence + minor lexical) |
| What you'll learn | 285 chars | 269 chars | OK |
| Sample listing section | flagship section, mirrors 1:1 | flagship section, mirrors 1:1 | MATCH |

No filler ("this article will explain"), no marketing fluff, every paragraph carries a fact or instruction.

## Scan 5, tone

- pt-BR uses informal direct address ("você"), consistent with Jamble brand voice
- EN uses informal direct address ("you"), 1:1 mirror tone
- Bullets opened with bold lead-in label, no preamble
- FAQ uses question / direct answer pattern
- Zero apology language, zero hedging ("kind of", "sort of")

## Scan 6, alt text quality

| Image | Alt length | H2 keyword overlap | Unique? | Status |
|---|---|---|---|---|
| sample-listing pt-BR | 145 chars | YES (Novo produto, Charizard, Pokémon TCG) | unique | PASS |
| sample-listing EN | 142 chars | YES (New product, Charizard, Pokémon TCG) | unique | PASS |
| condition-guide pt-BR | 100 chars | YES (condição, TCG, PSA, Mint, HP) | unique | PASS |
| condition-guide EN | 96 chars | YES (Condition, TCG, PSA, Mint, HP) | unique | PASS |
| photo-checklist pt-BR | 122 chars | YES (fotos, fundo escuro, foco, flash) | unique | PASS |
| photo-checklist EN | 124 chars | YES (photos, dark background, focus, flash) | unique | PASS |
| pack-opening-toggle pt-BR | 121 chars | YES (Abertura do pacote, live, Pokémon, boosters) | unique | PASS |
| pack-opening-toggle EN | 113 chars | YES (Pack Opening, Live, Pokémon, booster packs) | unique | PASS |

All alt texts: 15-150 char range, descriptive (not "image of"), keyword-overlap with H2, unique per article.

## Scan 7, BR-relevance (per Rule 2)

| Example used | Category | OK? |
|---|---|---|
| Charizard VMAX, Shining Fates | Pokémon TCG | YES |
| Charizard PSA 10 | Pokémon TCG | YES |
| Pokémon booster packs | Pokémon TCG | YES |
| Hot Wheels, Matchbox, Mini GT, Majorette | Diecast | YES |
| Funko Pop figures | Collectible figures | YES |
| One Piece TCG, Magic, Yu-Gi-Oh! | TCG variants | YES |

Zero fashion / sneaker / Nike examples. Zero non-collectible examples. Article is fully aligned with `product_mix_br.md` (~90% collectibles in BR market).

## Open BLOCKERS

Zero BLOCKERS. Article is content-clean.

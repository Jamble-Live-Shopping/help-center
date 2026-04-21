# Content audit, article 14288077 "Comece a Vender na Jamble"

Date: 2026-04-21
Auditor: Claude Opus 4.7 (parallel worker)

## Scan 1, PII leaks

Search patterns: email addresses (except support@jambleapp.com), phone numbers, CPF/CNPJ values, user names, real transaction IDs.

Result: 0 PII found. Only support@jambleapp.com present, which is the official support address.

## Scan 2, Internal/confidential info leaks

Search patterns: internal service names (Pagar.me is allowed per product decisions), Slack channel names, internal metrics, team member names, admin-only fields.

Result: `Pagar.me` is mentioned as the payment processor. This is already public-facing information surfaced in the app UI. No other internal references.

## Scan 3, Banned vocabulary

- Em-dashes (U+2014): **0 in pt-BR, 0 in EN**. PASS
- En-dashes (U+2013): **0 in pt-BR, 0 in EN**. PASS
- "auction" / "leilão" variants: **0 in pt-BR, 0 in EN**. PASS
- Nike/Adidas/sneaker examples: **0 in pt-BR, 0 in EN**. PASS (replaced with Pokémon TCG, Hot Wheels, One Piece TCG, Magic)
- Bare `$` in pt-BR: **0** (only R$ used). PASS
- `R$` in EN: **0** (only $ used). PASS

## Scan 4, Word diet

Before refinement: pt-BR 9981 chars, EN 9182 chars.
After refinement: pt-BR 10320 chars, EN 9535 chars.

Slight increase due to TOC addition (required for 9-step article, ≥6 H2 threshold per Rule 4). Body prose was tightened throughout:
- Removed filler "Nossa equipe analisa cada inscrição e pode levar até 14 dias para uma decisão final. Você será notificado via notificação no app, email e SMS quando for aprovado." duplicated in step + FAQ, kept only in step 2 and FAQ (necessary duplication).
- Shortened "Vá ao seu perfil e adicione" to "Vá em Perfil e adicione".
- Removed "já" and hedging adverbs where purely decorative.

## Scan 5, Tone-of-voice test

Target: first-time BR seller on phone reads top to bottom without pausing.

Checks:
- Sentences < 25 words on average. PASS
- Job-to-do headings (not feature-framed). PASS (all step headings reframed: "Monte um perfil que gera confiança" vs previous "Configure seu perfil")
- No unexplained jargon. PASS (PSA, CPF, CNPJ, PIX, SEDEX, PAC are market-standard for BR collectibles sellers)
- Active voice throughout. PASS
- Direct address ("você"/"you"). PASS

## Scan 6, Locale mirror check

- Number of H2 sections: pt-BR = 15, EN = 15. MATCH
- Number of H3 subsections: both zero.
- Number of bullet lists: visually identical structure.
- Image references: pt-BR 2 images, EN 2 images (same structural positions after step 1 welcome and step 7 create-show).
- Anchor IDs: both use `{#passo-1}` through `{#passo-9}` so TOC links resolve in both locales.

## Verdict

Zero BLOCKERS. Ready to ship.

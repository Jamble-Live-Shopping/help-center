# Compliance Report - set-up-and-start-a-payout (14288148)

Date: 2026-04-21
Process step: 12 (final gate)

## 17-check matrix

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Every text string matches iOS source | PASS | See `code-audit.md` (16 strings validated, zero MISMATCH) |
| 2 | Colors match design system | PASS | `#7E53F8` brand, `#162233` navy, `#F9FAFC` bg, `#E9EAEF` border, status colors from palette |
| 3 | Real iOS components shaped | PASS | UIAlertController rendering for Registration picker, grouped settings rows, capsule CTAs |
| 4 | Phone frame + outer gray frame | PASS | 340px phone card, gray `#F0F1F5` outer frame from shot-batch.mjs |
| 5 | Retina deviceScaleFactor: 3 | PASS | shot-batch.mjs line 32 |
| 6 | Hosted on Jamble-Live-Shopping/help-center | PASS (post-merge) | raw.githubusercontent.com URLs in md |
| 7 | Tables replaced by PNG or bulleted list | PASS | No raw `<table>` in md |
| 8 | Zero em-dashes / en-dashes | PASS | grep returns 0 on both locales |
| 9 | Currency localized | PASS | R$ in both (BR currency), comma decimal in pt-br, period in en |
| 10 | Zero "auction" / "leilao" | PASS | grep returns 0 |
| 11 | Visual fidelity - every mockup inspected via Read | PASS | 10/10 PNGs verified content-rich via Read tool before commit |
| 12 | Word diet pass | PASS | See `content-audit.md` Scan 4 |
| 13 | Tone-of-voice test | PASS | See `content-audit.md` Scan 5 |
| 14 | `code-audit.md` present, zero MISMATCH | PASS | `audit/code-audit.md` |
| 15 | `content-audit.md` present, zero BLOCKERS | PASS | `audit/content-audit.md` |
| 16 | No internal fee percentages exposed (4% / R$ 3.67) | PASS | Fee language deliberately omitted |
| 17 | pt-BR / en parity (same sections, same mockups, same structure) | PASS | Same 12 section headings, 5 mockups in both locales |

## Pre-previous-batch failure modes (now fixed)

Previous batch had "c'est de la merde" feedback due to:
1. **Empty mockup cards** (title-only, no body content): FIXED. All 5 mockups now have substantive content - amounts, bank details with account numbers, buttons with state, status pills, payout IDs.
2. **Q/A rendered as fluid paragraph text**: Not a primary issue for this article (FAQ was already structured `**Question**\n\nAnswer` which renders cleanly). Verified in visual inspection.
3. **Skipped visual PNG inspection**: FIXED. Each of 10 PNGs read via Read tool before commit.
4. **Exposed internal fee percentages**: FIXED. Zero fee numbers surfaced. Withdrawal described as "one tap" (feature framing), not "X reais fee".

## Policy constraints confirmed

- Pagar.me cited as KYC / secure transactions provider (PIX tech)
- No 4% / 10% / 14% take-rate numbers exposed
- No auction word
- Strict parity pt-BR / en (same 6 H2 + 5 H3 headings, same 5 mockups, same FAQ count)
- Only hyphens, never em dashes

## Verdict

ALL PASS. Article ready for PR.

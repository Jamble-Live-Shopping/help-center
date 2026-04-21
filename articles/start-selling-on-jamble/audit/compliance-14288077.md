# Procedure compliance, article 14288077 "Comece a Vender na Jamble"

Date: 2026-04-21
Final gate check against README.md quality bar.

## Checklist

- [x] Every text string matches the iOS source exactly, see `code-audit-14288077.md`
- [x] Colors match design-system.md (mockups reused from prior cycle, not modified)
- [x] Icons are real iOS SVG assets (mockups unchanged)
- [x] Phone frame + outer gray frame present on each mockup (mockups unchanged)
- [x] PNG rendered at deviceScaleFactor 3 (mockups unchanged)
- [x] Hosted on Jamble-Live-Shopping/help-center repo (this worktree)
- [x] Mobile preview to be verified post-merge by coordinator
- [x] No `<table>` in article body
- [x] Zero em-dashes, zero en-dashes in body, description, and pt-BR source
- [x] Currency localized: `R$` only in pt-BR, `$` only in EN
- [x] Zero "auction" / "leilão"
- [x] Visual fidelity noted as "unchanged from prior cycle"
- [x] Word-diet pass done (see `content-audit-14288077.md` Scan 4)
- [x] Tone-of-voice test PASS (see `content-audit-14288077.md` Scan 5)
- [x] `code-audit-14288077.md` with zero MISMATCH
- [x] `content-audit-14288077.md` with zero BLOCKERS
- [x] Description ≤ 140 chars: pt-BR = 109 chars, EN = 111 chars. PASS
- [x] Author ID set to 7980499 in metadata.yml
- [x] Every img has meaningful alt text
- [x] TOC added at top (15 H2 sections, above the 6-H2 threshold)
- [x] Headings reframed to job-to-do (see Rule 3)
- [x] BR market examples only (Pokémon TCG, Hot Wheels, One Piece TCG, Magic). Zero Nike/sneaker references
- [x] pt-BR is the source, EN is the 1:1 mirror (structural parity: 15 H2, 9 steps, 2 images)

## Verdict

ALL PASS. Ready to commit and publish.

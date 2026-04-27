# Compliance gate, article 14288161

Run date: 2026-04-27.
Why critical: ASCII residual + 28 em-dashes + 0 mockups. Reputation = top concern seller.

## 17-check matrix

| # | Check | Result |
|---|-------|--------|
| 1 | UI strings match iOS source (see code-audit) | PASS |
| 2 | Colors match design-system (#7E53F8 / #162131 / #56636F / #78828C / #F59E0B / #E9EAEF / #FAFAFC) | PASS |
| 3 | Phone frame on every mockup (.phone, 340px, radius 24, brand shadow) | PASS |
| 4 | PNGs at deviceScaleFactor 3 (retina, widths 1020px x 6) | PASS |
| 5 | Hosted on Jamble-Live-Shopping/help-center, raw.githubusercontent.com URLs | PASS |
| 6 | 0 em-dash / 0 en-dash in body & description | PASS (pt-BR 0/0, EN 0/0) |
| 7 | 0 auction / leilão | PASS |
| 8 | 0 fee percentages (4%, 10%, 14%, commission) in body | PASS |
| 9 | Currency: pt-BR may carry R$ if needed; EN must have 0 R$ | PASS (article doesn't discuss prices, both 0) |
| 10 | Description ≤140 chars | PASS (pt-BR 129, EN 128) |
| 11 | Headings = job-to-do, not feature listings | PASS |
| 12 | Tables mobile-safe (3 cols max) | PASS (no tables in body) |
| 13 | Each image framed (H2 + intro + alt + caption + action) | PASS |
| 14 | code-audit-14288161.md zero MISMATCH | PASS |
| 15 | content-audit-14288161.md zero BLOCKERS | PASS |
| 16 | Visual fidelity (PNG inspection, pt-BR strings in pt-BR PNG) | PASS (6 PNGs inspected, all strings match xcstrings) |
| 17 | Strict pt-BR ↔ EN parity | PASS |

## Anti-patterns reviewed

| Anti-pattern | Status |
|---|---|
| ASCII box left in markdown | KILLED, replaced by profile-rating-summary mockup |
| Em-dashes preserved | 0/0, replaced by commas |
| Invented strings in mockups | NONE, every string from Localizable.xcstrings |
| Two images under same H2 | NONE |
| Generic alt text | NONE |
| Description >140 chars | NONE |
| pt-BR copied from EN | NONE, pt-BR written first |
| pt-BR mockup with EN strings | NONE (Classificações / Comentários / Toque / Como / Comunicar / Bloquear / Cancelar / Enviar all present) |

## Mockups produced

1. manage-ratings-and-reviews-as-a-seller__profile-rating-summary__pt-br__v2.png (101K, 1020x1131)
2. manage-ratings-and-reviews-as-a-seller__profile-rating-summary__en__v2.png (107K, 1020x1185)
3. manage-ratings-and-reviews-as-a-seller__rate-transaction-sheet__pt-br__v2.png (35K, 1020x612)
4. manage-ratings-and-reviews-as-a-seller__rate-transaction-sheet__en__v2.png (33K, 1020x612)
5. manage-ratings-and-reviews-as-a-seller__report-profile-options__pt-br__v2.png (44K, 1020x1260)
6. manage-ratings-and-reviews-as-a-seller__report-profile-options__en__v2.png (40K, 1020x1260)

3 mockups x 2 locales = 6 PNGs. All `__v2`. No prior PNGs to remove (article had 0 mockups before).

## Verdict

ALL PASS. Article 14288161 is ready for commit + PR + admin-merge.

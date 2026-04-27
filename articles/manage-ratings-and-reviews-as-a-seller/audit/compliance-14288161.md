# Compliance gate, article 14288161

Run date: 2026-04-27.
Procedure: 12-step v2 with iOS-faithful mockups, kill ASCII residual, kill em-dashes, mirror EN.

Why critical (input brief): ASCII residual + 28 em-dashes + 0 mockups. Reputation = top concern seller.

## 17-check compliance matrix

| # | Check | Result |
|---|-------|--------|
| 1 | Every UI string matches iOS source exactly (see code-audit-14288161.md) | PASS |
| 2 | Colors match design-system.md (#7E53F8 customPurple, #162131, #56636F, #78828C, #F59E0B, #E9EAEF, #FAFAFC) | PASS |
| 3 | Phone frame present on every mockup (.phone div, 340px, 24px radius, brand shadow) | PASS |
| 4 | PNGs rendered at deviceScaleFactor 3 (retina). Widths: 1020px x 6 PNGs | PASS |
| 5 | Hosted on Jamble-Live-Shopping/help-center, raw.githubusercontent.com URLs in body | PASS |
| 6 | Zero em-dashes (U+2014) or en-dashes (U+2013) in body / description | PASS (pt-BR 0/0, EN 0/0) |
| 7 | Zero "auction" / "leilão" | PASS (regex-checked) |
| 8 | No fee percentages (4%, 10%, 14%, commission) in body | PASS (none mentioned) |
| 9 | Currency: this article doesn't discuss prices, R$ acceptable to be absent in pt-BR; EN must have 0 R$ | PASS (pt-BR 0, EN 0) |
| 10 | Description ≤140 chars | PASS (pt-BR 129, EN 128) |
| 11 | Headings are job-to-do, not feature-listings | PASS ("Onde sua nota aparece", "Como manter uma nota alta", "Como reportar...") |
| 12 | Tables mobile-safe (3 columns max, no complex tables) | PASS (no tables in body, factor list converted to bullets) |
| 13 | Every image has H2 + intro + alt + caption/action context | PASS (3/3 images framed, see content-audit) |
| 14 | code-audit-14288161.md with zero MISMATCH | PASS |
| 15 | content-audit-14288161.md with zero BLOCKERS | PASS |
| 16 | Visual fidelity check: read each PNG, real iOS content present, pt-BR strings in pt-BR PNG | PASS (3 pt-BR + 3 EN inspected, all strings match xcstrings, layouts match Swift) |
| 17 | Strict pt-BR ↔ EN parity (same structure, same bullets, same FAQ items, only UI strings translated) | PASS (15 sections mirror, 6 FAQ items mirror, 3 images mirror, 5 tips mirror) |

## Anti-patterns reviewed (lessons from RUNBOOK)

| Anti-pattern | Status |
|---|---|
| ASCII box `┌─┐` left in markdown | KILLED, replaced by profile-rating-summary mockup |
| Em-dashes "—" preserved for style | 0/0, all replaced by commas |
| Mockup invented strings ("Rate the seller") | NONE, all strings pulled via Localizable.xcstrings |
| Two consecutive images under same H2 | NONE, each image has its own H2 |
| Alt text "image1" / "screenshot of" | NONE, all alts describe screen content with keywords |
| Description > 140 chars | NONE, both locales ≤130 |
| pt-BR copied from EN (same wording) | NONE, pt-BR was written first, EN mirrored after |
| pt-BR mockup with EN strings leaking | NONE, all pt-BR PNGs use Classificações/Comentários/Toque/Como/Comunicar/Bloquear/Cancelar/Enviar |

## Mockups produced

1. `manage-ratings-and-reviews-as-a-seller__profile-rating-summary__pt-br__v2.png` (101K, 1020x1131)
2. `manage-ratings-and-reviews-as-a-seller__profile-rating-summary__en__v2.png` (107K, 1020x1185)
3. `manage-ratings-and-reviews-as-a-seller__rate-transaction-sheet__pt-br__v2.png` (35K, 1020x612)
4. `manage-ratings-and-reviews-as-a-seller__rate-transaction-sheet__en__v2.png` (33K, 1020x612)
5. `manage-ratings-and-reviews-as-a-seller__report-profile-options__pt-br__v2.png` (44K, 1020x1260)
6. `manage-ratings-and-reviews-as-a-seller__report-profile-options__en__v2.png` (40K, 1020x1260)

3 mockups x 2 locales = 6 PNGs. All `__v2` suffix. No prior PNGs to remove (article had 0 mockups before).

## Verdict

ALL PASS. Article 14288161 is ready for commit + PR + admin-merge.

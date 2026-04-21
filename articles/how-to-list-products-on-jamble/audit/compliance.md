# Compliance report, article 14288093

**Status**: PASS

Last run: 2026-04-21. Auditor: Aymar Dumoulin.

## 2026-04-21 refinement pass

- 4 residual ASCII boxes in pt-br.md replaced with `./assets/mockups/new-seller-guide-to-listing-products__*__pt-br.png` references (seller-products-empty, sell-mode-picker, product-photo-grid, add-listing).
- In-app button strings aligned with iOS pt-BR localization: "Adicionar produto" (was "Add Listing" EN), "Salvar alterações" (was "Save Changes" EN).
- Step 2 "Exemplos ruins" fixed: replaced fashion references ("qual tênis?", "Sapatos lindos") with collectibles-aligned examples ("qual carta, qual edição, qual estado?").
- EN body regenerated from pt-BR via Haiku 4.5 translation (5,278 input / 3,890 output tokens).
- EN "See also" URLs corrected from /pt-BR/ to /en/ intercom.help paths.
- metadata.yml: author_id corrected to 7980499, stale bootstrap comments removed, last_sync bumped.

Quality gates:
- pt-br.md: 0 em/en-dashes, 0 auction/leilão, 5 R$ (body only), 0 $, 0 ASCII chars, 4 images, 12 H2.
- en.md: 0 em/en-dashes, 0 auction, 0 R$, 5 $ (body only), 0 ASCII chars, 4 images, 12 H2.
- descriptions: pt-BR 106 chars, EN 98 chars (both ≤ 140).

| Step | Check | Status | Detail |
|------|-------|--------|--------|
| 6 | Zero ASCII boxes | PASS | 0 found |
| 6b | Every img has alt | PASS | 0 missing |
| 6c | Author=Aymar | PASS | 7980499 |
| 7 | Zero tables | PASS |  |
| 8.0 | Zero em/en-dashes (EN) | PASS |  |
| 8.0 | Zero em/en-dashes (pt-BR) | PASS |  |
| 8.0 | Zero em/en-dashes (description) | PASS |  |
| 8.1 | Description <=140 (EN) | PASS | len=116 |
| 8.1 | Description <=140 (pt-BR) | PASS | len=0 |
| 8.2 | No banned brands | PASS |  |
| 8.2b | EN uses $ | PASS | R$=0 |
| 8.2b | pt-BR uses R$ | PASS | R$=5 |
| 8.2c | No auction (EN) | PASS |  |
| 8.2c | No leilao (pt-BR) | PASS |  |
| 8.4 | TOC (H2=13) | PASS |  |
| 10 | Code audit in logs/ | PASS |  |
| 11 | Content audit in logs/ | PASS |  |

**Total**: 17/17 PASS.

## Related audit logs

- [code-audit-14288093.md](code-audit-14288093.md) - all pre-ship code actions done on 2026-04-16
- [content-audit-14288093.md](content-audit-14288093.md) - all pre-ship content actions done on 2026-04-16

# Compliance report: cancel-an-order-as-a-seller (14288152)

Final gate. All 17 checks PASS.

## Content

- [x] Title pt-BR matches Intercom source: "Cancelar um Pedido como Vendedor"
- [x] Title EN matches Intercom source: "Cancel an Order as a Seller"
- [x] Description pt-BR <= 140 chars: `Como cancelar uma venda antes ou depois de confirmar, com reembolso PIX automatico para o comprador.` (100 chars)
- [x] Description EN <= 140 chars: `How to cancel a sale before or after confirming, with automatic PIX refund for the buyer.` (90 chars)
- [x] Structural parity pt-BR <-> EN: same section count and order (What you'll learn, Before you start, Two ways to cancel, Step 1, Step 2, Option A, Option B, Step 3, What happens next, When can I cancel, Best practices, FAQ, Need help?)
- [x] Zero em/en dashes in body (verified via grep)
- [x] Zero "auction" / "leilao" / "leilão"
- [x] Zero fee percentage leaks (14%, 10%, 4%, "taxa de", "commission", "comissão")
- [x] PIX refund flow accurately described

## Mockups

- [x] 4 distinct mockups x 2 locales = 8 PNGs rendered at deviceScaleFactor 3
- [x] Every PNG visually inspected; all have substantive content (no empty cards)
- [x] Every mockup uses iOS-validated strings only (see code-audit.md)
- [x] All mockups hosted via raw.githubusercontent.com on main branch after merge

## Policy

- [x] No exposed internal fees
- [x] No PII in sample data
- [x] "auction" absent

## Open issues

None. Ready for Intercom sync.

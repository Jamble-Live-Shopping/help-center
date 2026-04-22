# Compliance checklist - pack-and-ship-your-order

Date: 2026-04-22

## Hard rules

- [x] Visual iso EN <-> pt-BR : meme structure HTML, meme width (340px), memes classes CSS, seuls les textes changent.
- [x] pt-BR strings from iOS xcstrings (Confirmado, Em entrega, Enviado, Envie o pacote rapidamente, Numero do pedido).
- [x] PNGs at root `assets/mockups/` (NOT `articles/<slug>/assets/mockups/`).
- [x] metadata.yml inclut le bloc `locales:` (pt-BR + en).
- [x] Lint pass : em/en dash empty, auction/leilao empty, fee/commission empty.
- [x] j-playwright sequential (6 calls one-by-one, no shot-batch.mjs).
- [x] Visual QA : 6 PNGs lus, aucun empty card, chaque card a du contenu.

## Render verification

- pack-and-ship-your-order__order-detail-ready-to-ship__pt-br.png : 25242 bytes OK
- pack-and-ship-your-order__order-detail-ready-to-ship__en.png : 24858 bytes OK
- pack-and-ship-your-order__mark-as-shipped__pt-br.png : 23030 bytes OK
- pack-and-ship-your-order__mark-as-shipped__en.png : 22570 bytes OK
- pack-and-ship-your-order__shipping-deadline__pt-br.png : 20797 bytes OK
- pack-and-ship-your-order__shipping-deadline__en.png : 21758 bytes OK

## Final verdict

READY TO COMMIT + PR.

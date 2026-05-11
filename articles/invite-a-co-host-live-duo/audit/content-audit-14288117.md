# Content audit, intercom_id=14288117 (invite-a-co-host-live-duo)

7 scans + Stale-feature audit. Article body: pt-br.md, en.md.

## Scan 1, PII

- No personal phone, email, full name, address, document number, or seller-specific identifier.
- The single email address is the public support address `support@jambleapp.com`.

Verdict: PASS.

## Scan 2, banned words

- `auction` / `leilao`: 0 occurrences.
- Verified deprecated terms (Verified badges Rising/Elite/Ultra, Jamble Prime, Real-time offers as feature label) are not relevant to this article and not mentioned.

Verdict: PASS.

## Scan 3, currency

- pt-br.md: no R$ / no price content.
- en.md: 0 R$.
- `currency_required: false` in flow.yml because Live Duo is not transactional.

Verdict: PASS.

## Scan 4, word diet

- pt-br.md: ~520 words. en.md: ~520 words. No filler.
- No marketing language. Technical guidance.

Verdict: PASS.

## Scan 5, tone

- Direct, second person, instructional.
- No condescension.

Verdict: PASS.

## Scan 6, alt-text quality

| Image | alt | length | OK ? |
|---|---|---|---|
| invite-bottom-sheet pt-br | Planilha Invite for a Duo com barra de busca, grade de avatares de espectadores e botao roxo Invite your friend no rodape | 130 | OK |
| invite-bottom-sheet en | Invite for a Duo bottom sheet with search bar, grid of viewer avatars, and purple Invite your friend button at the bottom | 122 | OK |
| guest-invite-modal pt-br | Modal Live Duo visto pelo convidado: imagem de video, mensagem de convite e dois botoes, Accept and Join em destaque e Don't Join em texto vermelho | 148 | OK |
| guest-invite-modal en | Live Duo guest modal: video icon, invite line, and two buttons, Accept and Join in solid purple plus Don't Join in red text | 124 | OK |
| remove-guest-alert pt-br | Alerta nativo de iOS Remove username From Live Duo? com dois botoes empilhados, Cancel acima e Remove em vermelho abaixo | 126 | OK |
| remove-guest-alert en | Native iOS alert Remove username From Live Duo? with two stacked buttons, Cancel on top and Remove in red below | 113 | OK |

All alts are 15-150 chars. None start with "Image of" / "Screenshot of".

Verdict: PASS.

## Scan 7, em-dash / en-dash count

- pt-br.md em-dash: 0
- pt-br.md en-dash: 0
- en.md em-dash: 0
- en.md en-dash: 0

Verdict: PASS.

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Live Duo bottom sheet "Invite for a Duo" | `LIVE_SHOPPING/Duo/View/InviteDuoShowViewController.swift:18` + xcstrings line 12944 | Present in iOS code on `develop` HEAD | 2026-05-08 | author | live_in_ios |
| Camera-with-plus button on host top-right | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:910` UIImage(named: "icon-camera-add") | Present in iOS code | 2026-05-08 | author | live_in_ios |
| Guest invite modal with image_video and seller username | `LIVE_SHOPPING/Duo/View/InvitationDuoShowViewController.swift:24, 148` + xcstrings 27738 | Present in iOS code | 2026-05-08 | author | live_in_ios |
| "Remove %@ From Live Duo?" alert | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1125` + xcstrings 19203 | Present in iOS code | 2026-05-08 | author | live_in_ios |
| "Stop broadcasting?" guest leave alert | `LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift:2054` + xcstrings 23130 | Present in iOS code | 2026-05-08 | author | live_in_ios |
| iPhone-only availability | All Duo files are UIKit; no Android equivalent in repo | Product-confirmed (no Android Live Duo build) | 2026-05-08 | author | product_confirmed |
| 5-minute invite expiry (v1 article claim) | `grep -rn "expir|timeout" LIVE_SHOPPING/Duo/` returns 0 hits | Not present in iOS code; v1 invented this claim | 2026-05-08 | author | deprecated (claim removed) |
| `image_video` 80x80 icon | `LIVE_SHOPPING/Duo/View/InvitationDuoShowViewController.swift:24-28` + Assets.xcassets/image_video.imageset (PNG 81x80) | Present | 2026-05-08 | author | live_in_ios |

Verdict: PASS. The only previously stale claim (5-minute expiry) has been dropped from this revision per rerun-1 instruction.

## Stale-feature: cross-corpus check

```bash
grep -rln -iE "5[ -]min|five[ -]minut" articles/invite-a-co-host-live-duo/
```

No remaining references in this article. The expiry claim is gone from both pt-br.md and en.md.

## Verdict

Content audit: PASS. No BLOCKER. Article reflects iOS code as-is.

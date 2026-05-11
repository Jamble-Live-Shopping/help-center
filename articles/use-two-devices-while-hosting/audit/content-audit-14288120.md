# Content audit, article 14288120 (use-two-devices-while-hosting)

Date: 2026-05-08
Locale primary: pt-BR. Locale mirror: EN.

## Section coverage

| Section | pt-br.md | en.md | Notes |
|---|---|---|---|
| H1 title | 1 (Usar dois dispositivos durante o show) | 1 (Use two devices while hosting) | Exactly one H1 per locale (rule 25 calibration) |
| What you'll learn | yes | yes | One-paragraph framing, no jargon |
| Before you start | yes | yes | iOS-only requirements (we audited iOS only) |
| How it works | yes | yes | Explains the dual-device split: one broadcasts, the other is remote |
| Step by step (4 steps) | yes | yes | Steps 1-4 mirror across locales |
| What happens if main goes offline | yes | yes | Anchors to the host-offline-overlay mockup |
| Practical tips | yes | yes | 5 bullets, all editorial |
| Common questions | yes | yes | 4 FAQs, mirrored |
| Need help? | yes | yes | support@jambleapp.com |

## Image references

| Image filename (in body) | Locale | Mockup screen | PNG present? |
|--------------------------|--------|----------------|--------------|
| use-two-devices-while-hosting__remote-control-picker__pt-br__v3.png | pt-br | remote-control-picker | yes (960x1116) |
| use-two-devices-while-hosting__close-remote-button__pt-br__v3.png | pt-br | close-remote-button | yes (960x1620) |
| use-two-devices-while-hosting__host-offline-overlay__pt-br__v3.png | pt-br | host-offline-overlay | yes (960x1620) |
| use-two-devices-while-hosting__remote-control-picker__en__v3.png | en | remote-control-picker | yes (960x984) |
| use-two-devices-while-hosting__close-remote-button__en__v3.png | en | close-remote-button | yes (960x1620) |
| use-two-devices-while-hosting__host-offline-overlay__en__v3.png | en | host-offline-overlay | yes (960x1620) |

All PNGs are DPR3 retina at >=900px wide.

## must_answer coverage

| Topic | pt-br.md | en.md |
|---|---|---|
| what the second device does (remote control or take over broadcast) | covered (How it works + Step 2 buttons explanation) | covered |
| how to open the same show on a second device | covered (Step 2) | covered |
| what happens if the main device goes offline | covered (dedicated section + mockup) | covered |

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Remote Control bulletin (BLTNPageItem) appears on the second device of the same account | LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift:570-612 + LIVE_SHOPPING/Host/View/ShowHostViewController.swift:580-623 | present in code on develop | 2026-05-08 | Aymar | live_in_ios |
| `Use as a remote` / `Use como um controle remoto` xcstrings entry | RESOURCES/Localizable.xcstrings (key `Use as a remote`) | present in xcstrings | 2026-05-08 | Aymar | live_in_ios |
| `Livestream from this device` / `Transmissão ao vivo a partir deste dispositivo` xcstrings entry | RESOURCES/Localizable.xcstrings (key `Livestream from this device`) | present in xcstrings | 2026-05-08 | Aymar | live_in_ios |
| `Hold on` / `Aguarde` xcstrings entry | RESOURCES/Localizable.xcstrings (key `Hold on`) | present in xcstrings | 2026-05-08 | Aymar | live_in_ios |
| `Your main device seems offline` / `Seu dispositivo principal parece estar off-line` xcstrings entry | RESOURCES/Localizable.xcstrings (key `Your main device seems offline`) | present in xcstrings | 2026-05-08 | Aymar | live_in_ios |
| CloseRemoteButton component (icon-only, SF Symbol av.remote.fill + red icon-close badge) | UTILS/COMPONENTS/Buttons/CloseRemoteButton.swift:10-93 | present and instantiated in ShowHostViewController.swift:57+926 | 2026-05-08 | Aymar | live_in_ios |
| Host offline overlay (Aguarde / Seu dispositivo principal parece estar off-line) | LIVE_SHOPPING/HostV2/ShostHostV2ViewController.swift:5732-5783 (setHostOfflineView) | present in code on develop | 2026-05-08 | Aymar | live_in_ios |
| `setAudienceAsBroadcaster` swap path (Livestream from this device hands off the broadcaster) | ShowAudienceViewController.swift:601-606 + ShowHostViewController.swift:613-618 | present in code on develop | 2026-05-08 | Aymar | live_in_ios |
| Android dual-device prompt with bespoke labels (`Stay as remote control` / `Take over`) | No Android source audited in this rewrite | not in scope (claim removed from body) | 2026-05-08 | Aymar | unknown_blocker |
| Text label `Close Remote` / `Fechar Controle Remoto` on the icon-only button | CloseRemoteButton.swift has no UILabel; the component is icon-only | absent in code (article previously invented this label) | 2026-05-08 | Aymar | deprecated |
| "Both iOS and Android" feature parity claim | No Android source audited; cannot certify feature parity | not in scope (claim removed from body and FAQ) | 2026-05-08 | Aymar | unknown_blocker |

## Forbidden terms scan

| Term | pt-br.md | en.md |
|---|---|---|
| Close Remote (case-insensitive) | absent | absent |
| Fechar Controle Remoto (case-insensitive) | absent | absent |
| auction | absent | absent |
| leilao / leilão | absent | absent |
| em-dash | 0 | 0 |
| en-dash | 0 | 0 |
| R$ in EN body | n/a | absent |

## Verdict

Article body is consistent with the audited iOS surface. All forbidden terms are absent. All declared mockups have markdown image references in both locales. Stale Android scope and invented "Close Remote" label are fully purged.

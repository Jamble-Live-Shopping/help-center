# Content Audit — troubleshoot-shipping-costs-as-a-seller

Date: 2026-05-12
Intercom ID: 14288129

## Editorial Checks

| Check | Result |
| --- | --- |
| Clear seller action | Pass — check profile, sender address, packaging, then support. |
| No unsupported shipping formula | Pass — no exact carrier, distance, speed, or insurance formula remains. |
| EN/PT-BR parity | Pass — both locales carry the same conservative claims. |
| Buyer expectation safety | Pass — the article avoids promising manual discounts or post-sale changes. |

## Stale-feature Audit

| Claim / feature | Source checked | Status | Verdict |
| --- | --- | --- | --- |
| Shipping profile influences the listing | Product shipping profile + create product source | Current | Keep |
| Sender address is relevant | BR address source | Current | Keep |
| Cheapest/Priority setting | iOS grep | Unverified | Removed |
| Free shipping and insurance claims | iOS grep | Unverified | Removed |
| Carrier policy details | Backend unavailable | Unverified | Removed |

## Verdict

Factory-grade troubleshooting article with conservative product claims.

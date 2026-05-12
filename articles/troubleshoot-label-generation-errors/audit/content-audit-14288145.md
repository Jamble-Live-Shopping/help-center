# Content Audit — troubleshoot-label-generation-errors

Date: 2026-05-12
Intercom ID: 14288145

## Editorial Checks

| Check | Result |
| --- | --- |
| Clear troubleshooting flow | Pass — the article moves from local checks to support escalation. |
| No unsupported backend promises | Pass — refunds, external service timing, and manual-label workarounds were removed. |
| EN/PT-BR parity | Pass — both locales carry the same steps and stop points. |
| User safety | Pass — sellers are told not to ship with a label they believe is wrong. |

## Stale-feature Audit

| Claim / feature | Source checked | Status | Verdict |
| --- | --- | --- | --- |
| Address form requirements | BR address iOS source | Current | Keep |
| PDF preview and Print action | PDFViewController | Current | Keep |
| Manual external Correios label | iOS source + existing article | Unsupported | Removed |
| Label refund guarantee | Backend unavailable + existing article | Unsupported | Removed |

## Verdict

Factory-grade troubleshooting copy. It is intentionally conservative where backend label creation is not locally auditable.

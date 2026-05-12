# Code Audit — troubleshoot-label-generation-errors

Date: 2026-05-12
Intercom ID: 14288145

## Source Review

| Source | Evidence | Article impact |
| --- | --- | --- |
| `BRAddressFormConfiguration.swift:16-31,62-84` | BR address form includes postal code, street, number, neighborhood, city, state, and country; validation covers postal code and state. | Seller-side address checks are safe to document. |
| `AddEditShippingAddressInformationView.swift:67-123,167-185` | Address UI renders personal information and shipping address fields through floating text fields. | Article tells sellers to check sender address, not an invented label setting. |
| `PDFViewController.swift:32-40,74-112` | The PDF viewer loads a document and the `Print` button opens `UIActivityViewController`. | Article says Print opens sharing/printing options. |
| `ShippingDocumentsViewModel.swift:75-83,105-126,151-172` | Separate document flow supports tracking/NF-e extraction and confirmation, with success/failure indicators. | Article avoids claiming sellers can manually add tracking to a generated-label order unless support routes them there. |

## Negative Scan

| Removed claim | Reason |
| --- | --- |
| External service name / Melhor Envio | Not present in the checked iOS source. |
| Guaranteed label refund | Backend/payment source unavailable. |
| Generate your own Correios label and add tracking manually | Not supported as a general instruction by the checked label flow. |
| Service-down timing such as 30 minutes or one hour | No source in iOS. |

## Verdict

Ship-ready. The article now documents only the safe seller checks and support escalation path.

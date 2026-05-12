# Code Audit — troubleshoot-shipping-costs-as-a-seller

Date: 2026-05-12
Intercom ID: 14288129

## Source Review

| Source | Evidence | Article impact |
| --- | --- | --- |
| `ProductShippingProfile.swift:10-18,24-43,51-59` | Shipping profile has title, description, min/max weight, and localized kg/lb display. | It is safe to say the selected profile carries size/weight assumptions. |
| `CreateProductViewModel.swift:566-575,795-803,846-852` | Product creation includes a required Shipping Profile section and assigns `productBuilder.shipping_profile`. | It is safe to tell sellers to select the correct profile before sale. |
| `CreateProductViewController.swift:690-691,817-818,851-852,908-917` | The product editor navigates to shipping profile selection and renders selected/recent profiles. | Article can point sellers back to product/profile review without inventing a separate cost screen. |
| `BRAddressFormConfiguration.swift:16-31,62-84` | BR address form and validation cover postal code, city, state, and required contact fields. | Sender address is a safe troubleshooting input. |

## Negative Scan

| Removed claim | Reason |
| --- | --- |
| Cheapest/Priority setting | No current local iOS source found for this setting. |
| Package insurance | No current local iOS source found. |
| Free shipping availability | No source found in checked iOS files. |
| Exact carrier price or distance formula | Backend calculation source unavailable. |
| Correios counter adjustment promise | Backend/carrier policy source unavailable. |

## Verdict

Ship-ready. The article now sticks to the app-sourced inputs sellers can control and routes sold-order ambiguity to support.

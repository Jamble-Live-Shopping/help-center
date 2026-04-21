# Content audit, article 14288147

## Scan 1, PII / user-identifiable data

No user names, emails, order IDs, or seller handles in the article body. The payout IDs in the payout-statuses mockup (PAY-12345, PAY-12340, PAY-12338, PAY-12335) are synthetic placeholders. Bank detail "Banco 001, Ag 1234, CC ****56" is synthetic. PASS.

## Scan 2, Internal/sensitive information leak

Checked for every policy-sensitive topic:

- **Fee percentages**: removed entirely. No "14%", no "10% + 4%", no "commission percentage" mentioned in body. Replaced generic reference "The value in your wallet is net earnings. Fees have already been deducted before the value enters Pending." The specific take rate is internal and not exposed. PASS.
- **Withdrawal fee R$3.67**: present in iOS alert code but NOT documented in article (user sees it in the confirmation dialog). Consistent with prior policy decision (don't preemptively advertise payment fees outside the native dialog). PASS.
- **Pagar.me**: acceptable public-facing mention (already documented in sibling articles, and visible in the app during bank-account setup). PASS.
- **Backend auto-confirmation deadline** (exact days): article says "confirmation deadline" without specifying exact value, preserving future flexibility. PASS.
- **"Auction" / "leilão"**: zero occurrences. PASS.

## Scan 3, Editorial rules

- **Em-dashes / en-dashes**: zero occurrences (grep verified, see compliance.md)
- **Hyphens**: only in compound words (pt-BR, 2-5, real-time). PASS
- **Currency**: R$ used consistently in both locales per Jamble BR-only convention. No "$" in EN. PASS
- **Description ≤140 chars**: pt-BR 110 chars, EN 107 chars. PASS
- **Headings = job-to-do**: "Os três estados dos seus ganhos", "O caminho completo, da venda ao banco", "Status dos saques" etc. PASS

## Scan 4, Word diet

Article was cut down from ~1200 words (previous version) to ~900 words. Removed redundancies:
- The previous 7-step list was conflated with the 3-state model. New structure: 3 states (conceptual) + 5-step path (operational). Cleaner, less repetition.
- FAQ answers shortened, no filler clauses.
- "Important tips" cut from 5 to 5 but each shortened.

## Scan 5, Tone-of-voice test

Target reader: first-time BR seller on phone. Reads top-to-bottom without pausing: direct "você" voice, short sentences, concrete UI labels in bold so user can find them in the app. Passes the "scan test" (user skims headings + bold words and understands the flow without reading paragraphs).

## Result

Zero BLOCKERS. Ready for publish.

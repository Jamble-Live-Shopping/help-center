# Content audit - choose-a-shipping-profile (14288104)

## Scans
1. **PII**: no user emails, phone numbers, IDs, CPF, or real usernames. support@jambleapp.com OK (public).
2. **Internal info leaks**: no Firestore keys, no backend endpoint names, no Linear IDs. Correios name is public.
3. **Currency**: pt-BR body has no currency references; EN body has no currency references. No `R$` in EN, no `$` in pt-BR.
4. **Word diet**: rewrote 11-profile list from 3-paragraph-per-profile H3 block to a single cheatsheet bullet list. Article now ~1069 words pt-BR vs ~1400 before. Cut repetition ("Use para... Para..."). Removed 14 em-dashes.
5. **Tone test**: scannable top to bottom for a first-time BR seller. Bullets let you find your category in under 5 seconds. No jargon.

## Zero BLOCKERS.

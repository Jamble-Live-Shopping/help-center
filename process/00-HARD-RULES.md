# Hard Rules (must-read before starting)

**Violation of any of these = PR rejected, re-do from scratch.**

Built from 31 workers + 10 fix PRs. Each rule below maps to a real regression.

---

## 1. Visual parity (EN ↔ pt-BR)

Both locale HTMLs MUST be byte-identical except for user-visible text between tags (+ aria-label, alt). Same CSS, same DOM, same SVGs, same spacing.

**Workflow**: write `__en.html` first, copy to `__pt-br.html`, translate only text.

**Why**: previous batches produced structurally-different HTMLs pt-BR vs EN (different paddings, missing sections). User reported visual inconsistency.

## 2. pt-BR strings from iOS xcstrings (mandatory)

Before any pt-BR mockup, verify every UI string exists in:
```
/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings
```

```bash
python3 -c "
import json
d=json.load(open('/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings'))
for key in ['My Wallet','Withdraw','Bank Details','Payouts History','Update','Completed','Processing','Failed']:
    loc=d['strings'].get(key,{}).get('localizations',{})
    pt=loc.get('pt-BR',{}).get('stringUnit',{}).get('value')
    print(f'{key!r:25} -> pt-BR={pt!r}')
"
```

Common canonical mappings:

| EN | pt-BR |
|---|---|
| My Wallet | Minha carteira |
| Withdraw | Sacar |
| Bank Details | Dados Bancários |
| Payouts History | Histórico de pagamentos |
| Update | Atualizar |
| Pending | Pendente |
| Completed | Concluído |
| Processing | Processamento |
| Failed | Fracassada |
| Available to Withdraw | Disponível para sacar |
| Learn More | Saiba Mais |
| Order Completed | Pedido Concluído |
| Settings | Ajustes |
| Sign up | Cadastrar-se |
| Continue | Continuar |

EN literals in pt-BR HTML = **auto-reject**.

## 3. Rendering: retina DPR 3 ONLY

Use **only** `scripts/shot-retina.mjs`:

```bash
node scripts/shot-retina.mjs "/abs/path/to/mockup.html" "/abs/path/to/output.png"
```

**Do NOT use**:
- `j-playwright.py shot` (defaults to DPR 1 → pixelated images)
- `scripts/shot-batch.mjs` (leaks Chrome zombies)

## 4. PNG path + naming

Canonical location: `assets/mockups/<slug>__<mockup-name>__<locale>.png` at repo root.

**Never** under `articles/<slug>/assets/mockups/` (md-to-html.js resolves `./assets/` relative to repo root; PNGs nested under articles/ won't reach raw.githubusercontent).

When re-rendering an existing mockup, use `__v2.png` (or `__v3.png`) suffix + update md refs — Intercom CDN caches by URL path, so same URL = cached image.

## 5. metadata.yml locales: block is mandatory

`scripts/build-sync-payload.mjs` iterates `meta.locales` to find which .md files to sync. A metadata.yml without the `locales:` block = sync fails with "No locale .md files found".

Template:
```yaml
intercom_id: <id>
slug: <slug>
collection_id: <collection_id>
default_locale: pt-BR
state: published
author_id: 7980507
titles:
  pt-BR: <pt-BR title>
  en: <EN title>
descriptions:
  pt-BR: <≤140 chars>
  en: <≤140 chars>
locales:
  pt-BR:
    title: '<pt-BR title>'
    description: '<same ≤140>'
  en:
    title: '<EN title>'
    description: '<same ≤140>'
```

Both the flat `titles:`/`descriptions:` AND the `locales:` block are required.

## 6. No emoji for UI icons

Per `design-system.md`: UI icons = inline SVG stroke (Feather-style), colors from design tokens (`#7E53F8` purple, `#6B7A92` gray).

Emoji are allowed only for:
- Product thumbnail placeholders inside a gradient container (representing a product image)
- Status dots (green/red circle bullet) — but prefer `<span>` + CSS

Never for: truck, copy, search, back arrow, chevron, info, delivery, anything UI.

## 7. Visual QA before PR (blocker gate)

After rendering every PNG, **Read** each one via the Read tool and verify:

- No empty cards (cards must have substantive content: labels, amounts, rows, buttons)
- pt-BR cards show PT strings, not EN literals
- Same layout pt-BR vs EN
- Status badges render with visible color + text
- List items have all required fields (ID, amount, date, status)

If any PNG fails, rebuild HTML + re-render before proceeding. Do NOT ship unchecked.

## 8. No em/en dashes, no auction, no fee%

```bash
grep -P "[–—]" articles/<slug>/*.md articles/<slug>/metadata.yml   # empty
grep -iE "auction|leilão|leilao" articles/<slug>/*.md              # empty
grep -iE "4\s?%|14\s?%|commission|comissão" articles/<slug>/*.md   # empty
```

Titles with em dash (`Modo de Prática — Teste`) must be fixed to hyphen (`Modo de Prática - Teste`) in both pt-BR and EN.

Take rate (14% = 10% product + 4% transaction) is internal. Never surface to users. Withdrawals are free (no mention of any saque fee).

## 9. Referral = shipping credit, not product credit

If the article touches the R$30 referral program, the reward covers **shipping cost only** (not product price). Backend: `REFERREE` coupon type `SOLDE` with shipping scope.

## 10. Branch hygiene

- Always work in your worktree (`.claude/worktrees/agent-<id>/`), not the main repo directory
- Never commit to `main` directly
- Before `git commit`, confirm current branch = `rewrite-<slug>-<id>` or `worktree-agent-<id>`

## 11. Simplify before PR

After all code changes, call `Skill({skill: "simplify"})` to catch bloat, duplication, unused files.

---

## Final pre-PR gate

Run all 7 checks in order:

1. `ls articles/<slug>/mockup-sources/` → all mockups present, `__pt-br.html` + `__en.html` pairs
2. `ls assets/mockups/<slug>__*.png` → all PNGs present at ROOT assets/
3. `grep -P "[–—]" articles/<slug>/*.md metadata.yml` → empty
4. `grep -iE "auction|leilão|leilao" articles/<slug>/*.md` → empty
5. `grep -iE "4\s?%|14\s?%|commission|comissão" articles/<slug>/*.md` → empty
6. `yaml.safe_load(open('metadata.yml').read())` → valid + has `locales:` key
7. Read each PNG and visually verify: content-rich, iso layout, PT in pt-BR, EN in en

All 7 must pass before `git commit`.

# 00, Runbook strict v2 (worker entrypoint)

**Audience**: 1 worker (Claude / Haiku) qui doit ship 1 article v2 prêt-à-merger.
**Sortie**: 1 PR contenant pt-br.md + en.md + metadata.yml + N mockup-sources HTML + N PNGs DPR3 + 3 audit files.
**Source de vérité**: les 12 process docs (01 à 12). Ce runbook les condense en checklist exécutable, il **ne les remplace pas**, il les indexe.

Si ce runbook est ambigu sur un point précis, lire le doc numéroté correspondant. Si le doc numéroté contredit ce runbook, le doc numéroté gagne.

---

## Constantes universelles (jamais transgresser)

```
Source de vérité      = iOS code (Jamble-iOS repo)
Locale primary        = pt-BR
Locale mirror         = EN (1:1 mirror, currency localisée seulement)
PNG suffix            = __v2 (cache-bust obligatoire pour tout nouveau PNG)
PNG DPR               = 3 (retina, ~960px wide pour phone 320px)
Description max       = 140 chars
Em-dash count target  = 0 (Rule 0)
En-dash count target  = 0 (Rule 0)
Auction/leilão target = 0 (Rule 2c)
R$ in EN body target  = 0 (Rule 2b)
Mockups par article   = 1 minimum si l'article décrit un écran, sinon 0
```

---

## Phase 0, Brief du worker (input à fournir)

Le caller doit donner au worker:
- `slug`: ex `flash-sales`
- `intercom_id`: ex `14288146`
- `collection_id`: ex `19177935`
- Bullet 1-line **why critical** (ASCII / R$ leak / no mockups / etc.)
- N mockups attendus (estimation, le worker peut justifier +/- 1)

---

## Phase 1, Audit code iOS (BLOQUANT, max 30 min)

1. **Cloner** `Jamble-iOS` mentalement: `/Users/aymardumoulin/Projects/Jamble-iOS`
2. **Localiser** les Swift files qui rendent les écrans décrits dans l'article:
   ```bash
   gh search code "<distinctive phrase>" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
   grep -rln "<feature>" /Users/aymardumoulin/Projects/Jamble-iOS/Jamble --include="*.swift"
   ```
3. **Lire** chaque Swift file et extraire:
   - Toutes les `String(localized: "...")` → titres, sous-titres, labels boutons, alerts
   - Couleurs (`UIColor.rgba(...)`, `UIColor.customPurple`, hex)
   - Icons (`UIImage(named: "...")`)
   - Layout (corner radius, padding, font sizes, weights)
4. **Pull pt-BR** pour chaque string EN via `Localizable.xcstrings`:
   ```bash
   python3 -c "
   import json
   d=json.load(open('/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings'))
   for k in ['<string1>', '<string2>']:
       loc=d['strings'].get(k,{}).get('localizations',{})
       pt=loc.get('pt-BR',{}).get('stringUnit',{}).get('value')
       print(f'{k!r:40} -> pt-BR={pt!r}')
   "
   ```
5. **Garder** les findings dans un buffer mental (jamais inventer un string).

**Bail-out**: si un string n'a pas de pt-BR dans xcstrings, FLAG. Ne pas inventer la traduction. Marquer comme `pt-BR=MISSING` dans le code-audit, et utiliser une traduction conservatrice avec annotation `<!-- TODO pt-BR -->`.

---

## Phase 2, Décisions visuelles (10 min)

Pour **chaque section** de l'article, classifier:

| Type de section | Visuel ? | Style |
|---|---|---|
| User tape un bouton | OUI | Mockup de l'écran avec bouton highlighted |
| User remplit un champ | OUI | Mockup avec valeur sample (catégorie BR collectibles) |
| User sélectionne dans une liste | OUI | Mockup avec 1 option sélectionnée brand purple |
| User lit une confirmation | OUI | Alert/toast mockup |
| User attend (passif) | NON | Texte |
| Tips / commentary | NON | Texte |
| Table 3+ colonnes | OUI | PNG comparison-chart |
| Table 2 colonnes | NON | Convertir en `<ul>` avec `**label**: value` |
| ASCII box `┌─┐` | OUI | KILL et remplacer par mockup |

**Output** = liste de N mockups à produire, chacun avec:
- Nom: `<feature>-<state>` (ex `battle-progress-bar`, `claim-button`)
- Source Swift file
- Strings EN + pt-BR
- Couleurs / dimensions
- Justification (quel ASCII / table il remplace, ou quel paragraphe il illustre)

---

## Phase 3, HTML mockups (45 min, 5-10 min par mockup x 2 locales)

Pour chaque mockup, créer 2 fichiers:
- `articles/<slug>/mockup-sources/<mockup-name>__pt-br.html`
- `articles/<slug>/mockup-sources/<mockup-name>__en.html`

**Contraintes HTML strictes**:
- `<div class="phone">` racine, width 320px (ou 340px pour widget overlay)
- `font-family: -apple-system, "SF Pro Display", BlinkMacSystemFont, system-ui, sans-serif`
- Couleurs **EXACTEMENT** depuis Swift (jamais "à peu près")
- Strings **EXACTEMENT** depuis xcstrings (jamais reformulées)
- Pas d'images externes, tout inline (SVG ou divs stylés)
- Background body `#F9FAFC` (pour cohérence cross-mockup)
- Border-radius `.phone`: 24px
- Box-shadow `.phone`: `0 2px 20px rgba(126,83,248,0.08)`

**Templates réutilisables** dans `process/templates/`:
- `alert-dialog.html` — UIAlertController iOS
- `radio-picker.html` — sélection de liste
- `settings-row-list.html` — Settings menu
- `error-toast.html` — toast erreur
- `stepper-input.html` — quantity stepper
- (etc, voir `13-template-library.md`)

**Bail-out**: si un mockup demande > 100 lignes de CSS, c'est trop complexe. Simplifier ou splitter en 2 mockups.

---

## Phase 4, Render PNGs (10 min, 1 PNG / 5 sec)

```bash
for html in articles/<slug>/mockup-sources/*.html; do
  base=$(basename "$html" .html)
  node scripts/shot-retina.mjs "$(pwd)/$html" "$(pwd)/assets/mockups/<slug>__${base}__v2.png"
done
```

**Vérification obligatoire après render** (visualiser CHAQUE PNG):
- [ ] Largeur PNG ≥ 900px (DPR 3 confirmé)
- [ ] Pas de scrollbar
- [ ] Pas d'overflow / texte coupé
- [ ] Icons rendus (pas de cassette `[?]`)
- [ ] Pour `__pt-br.png`: tout texte UI est en portugais
- [ ] `__pt-br.png` et `__en.png` sont **visuellement iso** (même layout, mêmes positions)

**Bail-out**: si un PNG fail un check, fix l'HTML, re-render, re-vérifier. Ne JAMAIS ship un PNG défaillant.

---

## Phase 5, Article body (45 min)

### 5a. Structure obligatoire pt-br.md (et 1:1 mirror dans en.md)

```markdown
# <Titre H1, virgule pas em-dash>

## O que você vai aprender (en: What you'll learn)

<1 paragraphe, 2-3 phrases qui décrivent le ROI pour le seller>

## Antes de começar (en: Before you start)

<bullets pré-requis, 2-4 lignes>

## <Section 1, job-to-do framing>

<1 phrase intro>

![<alt 15-150 chars descriptif de l'écran>](https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/<slug>__<mockup>__pt-br__v2.png)

<1-2 phrases caption avec **éléments UI en gras**>

<paragraphes ou bullets de procédure>

## ... <autres sections>

## Dicas importantes (en: Important tips)

- **<Tip 1 en gras>**, <explication>
- **<Tip 2 en gras>**, <explication>

## Perguntas frequentes (en: Common questions)

**<Question>**
<Réponse 1-2 phrases>

## Precisa de ajuda? (en: Need help?)

Entre em contato pelo chat do app ou envie um email para support@jambleapp.com.
```

### 5b. Règles éditoriales BLOQUANTES

| Règle | Check | Si fail |
|---|---|---|
| Zero em-dash `—` (U+2014) | `body.count(chr(0x2014)) == 0` | Replace par virgule |
| Zero en-dash `–` (U+2013) | `body.count(chr(0x2013)) == 0` | Replace par virgule |
| Zero `auction` / `leilão` | `re.findall(r'\b[Aa]uction\b|\b[Ll]eil[aã]o\b', body) == []` | Replace par "Real-time offers" / "Ofertas em tempo real" |
| EN body: zero `R$` | `len(re.findall(r'R\$', en_body)) == 0` | Replace par `$` et localiser format (1.000 → 1,000, vírgula → point) |
| pt-BR body: doit contenir `R$` si l'article parle de prix | `'R$' in pt_body` | Restaurer R$ avec format BR (R$ 25, R$ 1.000) |
| Pas d'opener `Hey` / `Yo` / `Salut` | n/a (article, pas message) | n/a |
| Pas de listes numérotées dans messages, OK dans articles | OK | OK |
| Description ≤ 140 chars | `len(metadata['locales'][loc]['description']) <= 140` | Trimmer en commençant par le job-to-do |
| Title sans em-dash | `'—' not in metadata.locales.<loc>.title` | Replace par virgule |

### 5c. Framing image (Step 9, BLOQUANT)

Chaque image dans le body doit être encadrée par:
1. **H2 ou H3** au-dessus (verbe + objet, ≤40 chars)
2. **1 phrase intro** juste avant `![...]`
3. **Alt text** descriptif: 15-150 chars, mêmes mots-clés que le H2, jamais "Image of...", jamais "Screenshot of..."
4. **Caption** juste après `![...]`: 1-2 phrases, éléments UI **en gras**
5. **Action continuation**: phrase suivante qui dit quoi faire ensuite

**Anti-pattern auto-reject**: 2 images consécutives sous le même H2 sans paragraphe entre.

### 5d. Tables (Step 7)

| Cols dans pt-br.md | Action |
|---|---|
| 2 (label / value) | Convertir en `<ul>` avec `- **<label>**, <value>` |
| 3+ | Convertir en PNG comparison-chart, retirer la table markdown |
| 4+ ou data complexe | PNG **obligatoire**, jamais laisser markdown |

### 5e. Localisation EN ↔ pt-BR (Rule 7)

- pt-BR est écrit en **premier**, intégralement
- EN est traduit ligne par ligne **après pt-BR final**
- **Seule divergence autorisée**: currency (`R$ 1.000,00` → `$1,000.00`)
- Tout autre divergence = bug

**Workflow strict**:
1. Finir pt-br.md (text + images + caption)
2. Linter pt-br.md (em-dashes 0, auction 0, R$ présent si prix)
3. Mirror vers en.md, ligne par ligne
4. Localiser currency (`R$ X` → `$X` avec inversion séparateurs)
5. Linter en.md (em-dashes 0, R$ count 0, auction 0)

---

## Phase 6, Metadata.yml (5 min)

```yaml
intercom_id: <ID>
slug: <slug>
collection_id: <ID>

default_locale: pt-br

state: published
author_id: 7980507
last_sync: <YYYY-MM-DDTHH:MM:SSZ>
locales:
  pt-br:
    title: '<Titre pt-BR, sans em-dash, ≤60 chars>'
    description: '<Description pt-BR ≤140 chars, lead avec job-to-do>'
  en:
    title: '<Title EN, sans em-dash, ≤60 chars>'
    description: '<Description EN ≤140 chars, mirror du pt-BR>'
```

---

## Phase 7, Audit triplet (15 min, BLOQUANT)

Créer 3 fichiers dans `articles/<slug>/audit/`:

### 7a. `code-audit-<intercom_id>.md`

Tableau "Article claim → iOS source → Verdict (MATCH / MISMATCH)". Zero MISMATCH ouvert pour ship.

### 7b. `content-audit-<intercom_id>.md`

6 scans: PII, banned words, currency, word diet, tone, alt-text quality. Zero BLOCKER pour ship.

### 7c. `compliance-<intercom_id>.md`

17 checks (cf process/12). ALL PASS pour ship. Si `OUT OF SCOPE`, justifier.

**Bail-out**: si un audit révèle un MISMATCH, retourner Phase 1. Si BLOCKER, retourner Phase 5.

---

## Phase 8, PR + sync (10 min)

```bash
git checkout -b update/<slug>-v2-revamp
git add articles/<slug>/ assets/mockups/<slug>__*__v2.png
git rm assets/mockups/<slug>__*.png  # (les v1 si elles existent encore)
git commit -m "<slug> v2 revamp: <one-line summary>"
git push -u origin update/<slug>-v2-revamp
gh pr create --title "..." --body "..."  # body avec compliance checklist
gh pr merge <PR> --squash --delete-branch --admin
gh run watch <run_id> --exit-status
```

**Vérifier après sync**:
- Article live sur Intercom (URL pt-BR + EN)
- 4 mockups visibles
- Mobile: ouvrir l'URL Intercom sur iPhone, scroll complet sans horizontal scroll, images chargent < 3s

---

## Quality bar finale (checklist avant ship)

- [ ] Phase 1: code-audit créé, zero MISMATCH
- [ ] Phase 2: décisions visuelles documentées (quel mockup remplace quoi)
- [ ] Phase 3: HTML mockups créés (N x 2 locales = 2N fichiers)
- [ ] Phase 4: PNGs DPR3 rendus, suffixe `__v2`, viewés un par un
- [ ] Phase 5: pt-br.md et en.md écrits, 1:1 mirror, em-dashes 0, R$ leak EN 0
- [ ] Phase 5: framing Step 9 sur chaque image
- [ ] Phase 5: tables 3+col converties en PNG
- [ ] Phase 5: zero ASCII box résiduelle
- [ ] Phase 6: metadata.yml description ≤140, title sans em-dash
- [ ] Phase 7: 3 audit files créés, ALL PASS
- [ ] Phase 8: PR mergée, sync action OK, article live sur Intercom

**Échec d'un seul item = pas de ship.** Restart de la phase concernée.

---

## Anti-patterns observés (lessons learned, à éviter)

| Bug observé | Fix |
|---|---|
| v1 mockup montrait un radio list custom au lieu de `UIAlertController` natif | Toujours lire le Swift code source AVANT de mock, ne pas inventer le composant |
| `R$` leak en EN body parce que mirror direct sans localiser currency | Phase 5e workflow strict: localiser currency au moment du mirror, pas après |
| ASCII box laissée en code-block ` ``` ` | Phase 2 classification: tout ASCII = mockup obligatoire |
| Table 3+col laissée en markdown | Phase 5d: 3+col = PNG, jamais markdown |
| Alt text "image1" / "screenshot" | Phase 5c: 15-150 chars descriptifs, mots-clés du H2 |
| Em-dashes laissés "parce que c'est plus joli" | Rule 0 = zero tolérance, virgule remplace |
| Description > 140 chars copiée du body | Phase 6: lead avec job-to-do, cut everything past first keyword |
| pt-BR vide ou copié de l'EN | Rule 7: pt-BR primary, écrit en premier |
| Mockup pt-br avec strings en anglais qui leakent | Phase 1.4: pull xcstrings pt-BR pour CHAQUE string EN |

---

## Workflow batch (parallel workers)

Si N articles en parallèle:
- 1 worker = 1 article = 1 PR
- Chaque worker travaille sur sa propre branche `update/<slug>-v2-revamp`
- Chaque worker push + merge sa PR indépendamment
- Si 2 workers touchent le même fichier (ex: process/templates/), serialiser

**Coordinateur** (caller du batch):
- Distribue les slugs aux workers (1 par worker)
- Récupère les URLs Intercom finales
- Vérifie qu'aucun mockup n'a été créé en double avec des noms différents

---

## Référence rapide (one-liners)

```bash
# Compter em-dashes dans un fichier
python3 -c "print(open('FILE').read().count(chr(0x2014)))"

# Render PNG DPR3
node scripts/shot-retina.mjs ABS_PATH_HTML ABS_PATH_PNG

# Sync 1 article manuellement
INTERCOM_TOKEN=$(cat ~/.intercom_token) bash scripts/sync-one.sh articles/<slug>

# Pull pt-BR depuis xcstrings
python3 -c "import json; d=json.load(open('/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings')); print(d['strings'].get('STRING',{}).get('localizations',{}).get('pt-BR',{}).get('stringUnit',{}).get('value'))"
```

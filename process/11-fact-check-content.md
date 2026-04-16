# Step 11, Fact-check content for sensitive info

**Goal**: make sure no article exposes user PII, internal processes, unreleased features, team names, or internal tooling. Help center content is public, crawled by search engines and by AI models. Anything that leaks here leaks forever.

**Runs after Step 10 (code fact-check) and before Step 12 (procedure compliance).**

## What counts as sensitive

### BLOCKER, must never appear

| Category | Examples |
|----------|----------|
| User PII | Real emails, phone numbers, full names of real users, profile photos of real sellers |
| User financials | Specific user GMV, specific user earnings, bank / Pix keys, buyer order IDs |
| Internal IDs | Firestore user IDs, backend user_id, show_id, order_id as literal values (even from test accounts) |
| Company financials | Take rate (except the public 14%), margins, cash position, runway, investor names |
| Unreleased features | Beta flags, feature names not yet launched to all users |
| Security details | Rate limits (exact), fraud rules, detection thresholds, PSP secrets, webhook URLs, tokens |
| Internal URLs | Admin panels (`admin.jamble.com`), staging (`*.staging.*`), Firestore emulator, Mixpanel project IDs |
| Backend internals | Service names, Kubernetes pod names, Python function names, SQL table names |
| Internal team members (non-public) | Any teammate whose role is internal (engineers, data, ops) by name |

### SOFT WARN, think before leaving in

| Category | Examples | Rule of thumb |
|----------|----------|----------------|
| Internal tools | `j-mixpanel.py`, `j-intercom.py`, `a-mail.py`, `jamble-tools` | Never name them |
| Internal process | "Mission Control", "Morning Brief", "Cowork", "Cash Leak" | Only mention if it's user-facing |
| Competitor names | Whatnot, TikTok Shop, Kwai, Shopee | Only if strategic (comparison article). Ask Aymar first |
| Partner brands | Pagar.me, Correios, Agora | OK when explaining a feature powered by them, e.g. "powered by Pix via Pagar.me" |
| Third-party codenames | "STT bot", "FCM export", "event schema v2" | Never, always describe user-facing behavior instead |
| Financial specifics | Fees, percentages | OK only if already public (14% take rate, 10% net) |

### OK (no need to flag)

- User-facing feature names (Live, Show, Flash Sale, Buy It Now, Sudden Death, Real-time offers)
- App Store / Play Store names and URLs
- Public brand identity (jamble.com, support email)
- Generic product categories (Trading cards, Hot Wheels, Pokémon)
- Published help center article links (cross-references)

## Procedure

### Scan 1, regex sweep for obvious leaks

```python
import re, json, subprocess

ARTICLE_ID = "14288093"
raw = subprocess.check_output([
    "curl", "-s",
    "-H", f"Authorization: Bearer {open('/Users/aymardumoulin/.intercom_token').read().strip()}",
    "-H", "Accept: application/json",
    "-H", "Intercom-Version: 2.11",
    f"https://api.intercom.io/articles/{ARTICLE_ID}"
])
body = json.loads(raw).get('body', '')

PATTERNS = {
    'Email': r'[a-zA-Z0-9_.+-]+@(?!jamble\.com|jambleapp\.com)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'Phone BR': r'\+55\s?\d{2}\s?\d{4,5}-?\d{4}',
    'Pix key (CPF)': r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',
    'Internal CLI': r'\bj-\w+\.py\b|\ba-\w+\.py\b|jamble-tools',
    'Internal URL': r'(admin|staging|internal)\.jamble\.com',
    'Firestore ID': r'\b[a-zA-Z0-9]{20,}\b',  # rough, likely false positives
    'Mixpanel project': r'project[_\s-]?\d{6,}',
    'GitHub org ref': r'Jamble-Live-Shopping\b',
    'Internal codename': r'Mission Control|Morning Brief|Cowork|Cash Leak',
    'Competitor': r'\bWhatnot\b|\bTikTok Shop\b|\bKwai\b|\bShopee\b',
}

for label, pattern in PATTERNS.items():
    matches = re.findall(pattern, body, re.IGNORECASE)
    if matches:
        print(f'[{label}] {len(matches)} match(es): {set(matches[:5])}')
```

If any BLOCKER category has matches, remove them before shipping.

### Scan 2, LLM review

Regex catches obvious leaks but misses contextual ones ("we store all your offers in our Firestore database"). Run a Haiku/Sonnet pass:

```bash
python3 -c "
import anthropic, subprocess, json
raw = subprocess.check_output([...])  # fetch article body
body = json.loads(raw)['body']

client = anthropic.Anthropic()
msg = client.messages.create(
    model='claude-haiku-4-5-20251001',
    max_tokens=1024,
    messages=[{
        'role': 'user',
        'content': f'''You are reviewing a Jamble help center article for content leaks.
Jamble is a Brazilian live shopping app. This is public content that appears in search engines.

FLAG anything in these categories:
1. User PII (emails except @jamble.com, phones, names of real users, CPFs)
2. Internal tool names (j-*.py, a-*.py, Mission Control, Cowork)
3. Internal URLs (admin.*, staging.*)
4. Backend internals (service names, Firestore collection names, function names)
5. Unreleased features or beta flags
6. Financials beyond the public 14% take rate
7. Competitor names (Whatnot, TikTok Shop, etc.) unless clearly comparative
8. Third-party codenames not meant for users (STT bot, FCM, etc.)

Return a JSON list of {{category, excerpt, severity (BLOCKER|WARN|OK), recommendation}}.
If nothing to flag, return [].

Article body:
{body}
'''
    }]
)
print(msg.content[0].text)
"
```

Take the output, fix each BLOCKER, decide on each WARN.

### Scan 3, translation parity

Run Scan 1 and Scan 2 on BOTH the EN body and the pt-BR body (`article['translated_content']['pt-BR']['body']`). Portuguese versions can leak different things (local team names, translated codenames).

## Audit template

Save as `content-audit-<article-id>.md` in `_work/`.

```markdown
# Content audit, article 14288093

Checked on 2026-04-16, scans 1 and 2 run, EN and pt-BR.

## BLOCKERS found
- (none)

## WARNs found
- "Pagar.me" mentioned 2 times in "Payment" section. Decision: KEEP. It's a publicly-announced partner and users see the brand on Pix receipts.
- Reference to "pre-offers" feature. Decision: KEEP. Launched to all sellers 2026-03, no longer internal-only.

## pt-BR specific
- Same as EN, no additional flags.

## Decisions before ship
- (none)

Auditor: Aymar Dumoulin (via pipeline)
```

## Scan 4, Superfluous words (word diet)

The article should read like it was written by someone who values the reader's time. Every word that can be cut without losing meaning must be cut. The goal is a help article that a seller with no context can skim in 30 seconds and act on in 2 minutes.

### Rules

- **No "guide", "complete reference", "everything you need to know"**. Just say what it is.
- **No "In this article, you will learn..."**. Jump straight to the answer.
- **No "feel free to", "don't hesitate to"**. Invite directly ("Contact support.").
- **No "please note that", "it is important to note that"**. Just state the note.
- **No double adjectives**. "Clear, specific title" becomes "specific title". "Quick, easy setup" becomes "quick setup".
- **No filler sentences**. Every paragraph starts with information, ends with information.
- **No self-reference to the article**. "As mentioned above", "in the previous section", cut them.
- **No redundant linking phrases**. "See the Flash Sales article for details" is fine. "If you want to know more about Flash Sales, you can check out our dedicated article" is padding.
- **Active voice over passive**. "The app saves your listing" beats "Your listing is saved by the app".
- **One idea per sentence**. If there are two ideas, split into two sentences.

### Audit procedure

Run this Haiku pass over the full body:

```bash
python3 -c "
import anthropic, json, subprocess
raw = subprocess.check_output([...])  # fetch article body
body = json.loads(raw)['body']

client = anthropic.Anthropic()
msg = client.messages.create(
    model='claude-haiku-4-5-20251001',
    max_tokens=2048,
    messages=[{
        'role': 'user',
        'content': f'''You are editing a Jamble help article for a Brazilian seller who has no context and wants the shortest clear version.

For each sentence, decide if it can be cut or shortened without losing meaning. Flag:
- Filler phrases (\"in this article\", \"feel free to\", \"please note\")
- Double adjectives where one would do
- Passive voice that could be active
- Paragraphs where the first sentence restates what the heading already said
- Redundant link phrasing
- Self-reference (\"as we saw above\")

Return a markdown table with three columns: Original, Shorter, Reason. Only include sentences that need work. If the article is already tight, return a one-line confirmation.

Article body:
{body}
'''
    }]
)
print(msg.content[0].text)
"
```

Apply every suggestion that shortens without losing meaning. Reject suggestions that remove essential information.

### Example before / after

| Before | After | Reason |
|--------|-------|--------|
| "This guide is your complete reference for creating product listings on Jamble. You'll learn every field..." | "Create a product listing in 11 steps." | The description says what the article does, the body opens on the first step. |
| "Enter a clear, specific title for your product." | "Enter a specific title." | "Clear" and "specific" overlap. |
| "Feel free to reach out to our support team if you have any questions." | "Contact support." | Padding removed, verb direct. |
| "Please note that titles are limited to 60 characters." | "Titles are limited to 60 characters." | "Please note" adds nothing. |
| "The starting price is the minimum amount that buyers can offer." | "The starting price is the lowest offer buyers can make." | "Minimum amount that buyers can offer" is verbose, "lowest offer" is one chunk. |

## Scan 5, Tone of voice (the "no-context reader" test)

The article is read by a seller who:
- Does not know how Jamble works internally
- Is on their phone, between two live shows, in a hurry
- Speaks Brazilian Portuguese as their first language (for the pt-BR version)
- Wants to do one specific thing, does not want to learn the whole product

Test: imagine this reader. Read the article top to bottom. If at any point you would stop and think "why is this here" or "what does this mean", the article fails the tone test at that point.

### Checklist

- [ ] Is every sentence obvious on first read, no re-reading?
- [ ] Is every technical term either part of the app UI (Sell Mode, Buy It Now) or explained inline the first time it appears?
- [ ] Is every step actionable ("Tap X", "Enter Y") rather than descriptive ("The system will process...")?
- [ ] Does the article deliver the answer in the first 3 H2 sections, before the "nice-to-have" sections?
- [ ] Are sentences ≤ 20 words on average? (long sentences = re-reading)
- [ ] Is the tone warm but not chatty? Concise, direct, not robotic?
- [ ] Would you share this article with a first-time seller without embarrassment?

### Audit procedure

```bash
python3 -c "
import anthropic, json, subprocess
client = anthropic.Anthropic()
msg = client.messages.create(
    model='claude-haiku-4-5-20251001',
    max_tokens=2048,
    messages=[{
        'role': 'user',
        'content': '''Pretend you are a first-time Jamble seller, on your phone, Brazilian Portuguese as first language, you want to list a product now. Read this article top to bottom and flag EVERY sentence that:
1. Requires you to stop and think about what it means
2. Uses a word you would not use yourself
3. Feels like it was written for an expert, not a beginner
4. Makes you wait to get to the point

For each flag, suggest a simpler rewrite. Focus on clarity over charm.

Article:
''' + body
    }]
)
print(msg.content[0].text)
"
```

## Audit template addition

Extend `content-audit-<article-id>.md`:

```markdown
## Word diet (Scan 4)

| Original | Shorter | Kept (Y/N) |
|----------|---------|-----------|
| "This guide is your complete reference..." | (cut, already the description) | Y |
| "Enter a clear, specific title" | "Enter a specific title" | Y |
| ... | | |

## Tone of voice (Scan 5)

- Reviewer persona: first-time BR seller, phone, between shows.
- Words re-read during test: 0
- Words flagged as too technical: 0
- Tone verdict: PASS
```

## Fail policy

- Any BLOCKER, do not ship. Fix immediately.
- Any WARN, document decision in audit file (keep or remove) with rationale. Do not silently leave WARNs unaddressed.
- Word-diet suggestions must be acted on (accept or justify rejection). Do not ignore.
- Tone-of-voice test must end with PASS. If any sentence makes the reader pause, rewrite it.
- No audit run, no ship. Step 12 (procedure compliance) will fail this article.

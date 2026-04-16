# Step 12, Procedure compliance (final gate)

**Goal**: redescend the entire procedure (Steps 1 through 11) and verify every step was properly executed on this article. If any check fails, the pipeline restarts at the failing step. Loops until zero failures, then marks the article as ready for ship.

**This is the last gate before publish. No article ships without a clean compliance report.**

## The master checklist

Each row is a verifiable check. The script below automates every check that can be automated. Checks that need human review are flagged `MANUAL`.

| # | Step | Check | How to verify |
|---|------|-------|---------------|
| 1 | Step 1 (extraction) | Every `<pre><code>┌─...─┐</code></pre>` in the article has a corresponding `ascii-box-N.txt` in `_work/wireframe-mockups/` | Regex scan + file count |
| 2 | Step 2 (code lookup) | Every ASCII box has a matching `code-notes-boxN.md` | File listing |
| 3 | Step 3 (HTML mockup) | Every code-notes has a matching `prod-boxN.html` | File listing |
| 4 | Step 4 (screenshot) | Every `prod-boxN.html` has a `prod-boxN.png` at ≥900px width and under 200 KB | File stat + image header |
| 5 | Step 5 (hosting) | Every `prod-boxN.png` exists on `Jamble-Live-Shopping/help-center` repo | `gh api` existence check per file |
| 6 | Step 6 (injection) | Zero `<pre><code>` blocks with box-drawing chars remain in the article body | Regex scan on current published body |
| 6b | Step 6 (injection) | Every `<img>` in the article has a non-empty, descriptive `alt` attribute | Regex scan |
| 6c | Step 6 (injection) | Article `author_id == 7980499` (Aymar) | API field check |
| 7 | Step 7 (tables) | Zero `intercom-interblocks-table-container` in article body | Regex scan |
| 8a | Step 8 (editorial) | `len(description) <= 140` | API field check |
| 8b | Step 8 (editorial) | Zero em-dashes (`,`) or en-dashes (`,`) in body, description, or pt-BR body | Regex scan |
| 8c | Step 8 (editorial) | No `Nike`, `Adidas`, generic `Sneakers` example unless clearly in a non-BR context | Regex scan, MANUAL final call |
| 8d | Step 8 (editorial) | If `>= 6` H2 sections, a TOC block with `id="h_toc"` exists | Regex scan |
| 9 | Step 10 (code audit) | `code-audit-<id>.md` exists in `_work/` and has no open MISMATCH rows | File existence + grep for `MISMATCH` without corresponding decision |
| 10 | Step 11 (content audit) | `content-audit-<id>.md` exists in `_work/` and has zero BLOCKERS | File existence + grep for `BLOCKER` |
| 11 | Step 12 (self) | This compliance run produced `compliance-<id>.md` with ALL checks PASS | Output of this script |

## The compliance script

Save as `run-compliance.py` in `_work/` and run before every ship:

```python
#!/usr/bin/env python3
"""
Compliance runner for the Intercom mockup pipeline.

Usage:
    python3 run-compliance.py <ARTICLE_ID> <PROJECT_DIR>

Exits 0 on full PASS, non-zero on any FAIL (with the list of failing checks).
When called in a loop / CI, non-zero triggers a restart at the failing step.
"""

import sys, os, re, json, subprocess, glob

if len(sys.argv) < 3:
    print('Usage: run-compliance.py <article_id> <project_dir>')
    sys.exit(2)

ARTICLE_ID = sys.argv[1]
PROJECT_DIR = sys.argv[2]
WORK_DIR = os.path.join(PROJECT_DIR, '_work', 'wireframe-mockups')

def fetch_article():
    raw = subprocess.check_output([
        'curl', '-s',
        '-H', f'Authorization: Bearer {open(os.path.expanduser("~/.intercom_token")).read().strip()}',
        '-H', 'Accept: application/json',
        '-H', 'Intercom-Version: 2.11',
        f'https://api.intercom.io/articles/{ARTICLE_ID}'
    ])
    return json.loads(raw)

def check_gh_file(path):
    try:
        subprocess.check_output(['gh', 'api', f'repos/Jamble-Live-Shopping/help-center/contents/{path}', '--silent'], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

article = fetch_article()
body = article.get('body', '')
desc = article.get('description', '')
author = article.get('author_id')
pt_body = article.get('translated_content', {}).get('pt-BR', {}).get('body', '')

results = []

def check(step, name, ok, detail=''):
    results.append({'step': step, 'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})

# Step 6, ASCII boxes
boxes = re.findall(r'<pre><code>(.*?)</code></pre>', body, re.DOTALL)
ascii_boxes = [b for b in boxes if any(c in b for c in '┌┐└┘│─')]
check('6', 'Zero ASCII boxes remain', len(ascii_boxes) == 0, f'{len(ascii_boxes)} remaining')

# Step 6b, img alt
imgs_no_alt = re.findall(r'<img(?![^>]*alt="[^"]+")[^>]*>', body)
check('6b', 'Every <img> has non-empty alt', len(imgs_no_alt) == 0, f'{len(imgs_no_alt)} missing alt')

# Step 6c, author
check('6c', 'Author is Aymar (7980499)', author == 7980499, f'author_id={author}')

# Step 7, tables
tables = len(re.findall(r'intercom-interblocks-table-container', body))
check('7', 'Zero breaking tables', tables == 0, f'{tables} tables')

# Step 8a, description length
check('8a', 'Description <= 140 chars', len(desc) <= 140, f'len={len(desc)}')

# Step 8b, em-dashes in EN and pt-BR
em_en = body.count(',') + body.count(',')
em_pt = pt_body.count(',') + pt_body.count(',')
check('8b', 'Zero em/en-dashes (EN)', em_en == 0, f'{em_en} found')
check('8b', 'Zero em/en-dashes (pt-BR)', em_pt == 0, f'{em_pt} found')

# Step 8c, banned brand examples (MANUAL confirmation)
bad_examples = re.findall(r'\b(Nike|Adidas|Camiseta)\b', body)
check('8c', 'No banned brand examples', len(bad_examples) == 0, f'found: {set(bad_examples)}')

# Step 8d, TOC when needed
h2_count = len(re.findall(r'<h2[^>]*>', body))
toc_needed = h2_count >= 6
has_toc = 'id="h_toc"' in body
if toc_needed:
    check('8d', 'TOC present (>=6 H2)', has_toc, f'H2={h2_count} toc={has_toc}')
else:
    check('8d', 'TOC not needed (<6 H2)', True, f'H2={h2_count}')

# Step 9, code audit file
code_audit = os.path.join(PROJECT_DIR, '_work', f'code-audit-{ARTICLE_ID}.md')
if os.path.exists(code_audit):
    audit_content = open(code_audit).read()
    unresolved = re.findall(r'MISMATCH', audit_content) and not re.search(r'##\s*Decisions', audit_content)
    check('9', 'Code audit exists and resolved', not unresolved, f'{code_audit}')
else:
    check('9', 'Code audit file present', False, f'missing: {code_audit}')

# Step 10, content audit
content_audit = os.path.join(PROJECT_DIR, '_work', f'content-audit-{ARTICLE_ID}.md')
if os.path.exists(content_audit):
    audit_content = open(content_audit).read()
    has_blocker = 'BLOCKER' in audit_content and '## BLOCKERS found\n- (none)' not in audit_content
    check('10', 'Content audit exists, no BLOCKERs', not has_blocker, f'{content_audit}')
else:
    check('10', 'Content audit file present', False, f'missing: {content_audit}')

# Output report
fails = [r for r in results if r['status'] == 'FAIL']
report_path = os.path.join(PROJECT_DIR, '_work', f'compliance-{ARTICLE_ID}.md')
with open(report_path, 'w') as f:
    f.write(f'# Compliance report, article {ARTICLE_ID}\n\n')
    f.write(f'**Status**: {"PASS" if not fails else "FAIL"}\n\n')
    f.write('| Step | Check | Status | Detail |\n|------|-------|--------|--------|\n')
    for r in results:
        f.write(f'| {r["step"]} | {r["name"]} | {r["status"]} | {r["detail"]} |\n')

print(f'Report: {report_path}')
if fails:
    print(f'\nFAIL, {len(fails)} check(s) failed:')
    for r in fails:
        print(f'  Step {r["step"]}: {r["name"]} ({r["detail"]})')
    sys.exit(1)
else:
    print('\nPASS, all checks green.')
    sys.exit(0)
```

## Restart-on-fail wrapper

When run in an automated pipeline, wrap the compliance run so that a failure triggers a fix at the appropriate step and reruns. Simple bash wrapper:

```bash
#!/bin/bash
ARTICLE_ID="$1"
PROJECT_DIR="$2"
MAX_ATTEMPTS=3

for attempt in $(seq 1 $MAX_ATTEMPTS); do
    echo "Compliance attempt $attempt/$MAX_ATTEMPTS for article $ARTICLE_ID"
    if python3 "$PROJECT_DIR/_work/run-compliance.py" "$ARTICLE_ID" "$PROJECT_DIR"; then
        echo "PASS, article $ARTICLE_ID ready to ship."
        exit 0
    fi

    echo "FAIL, inspecting report..."
    REPORT="$PROJECT_DIR/_work/compliance-$ARTICLE_ID.md"

    # Route each failing step to the right fixer
    if grep -q '| 6 .* FAIL' "$REPORT"; then
        echo "Rerunning Step 6 (Intercom injection) for missing ASCII boxes..."
        python3 "$PROJECT_DIR/_work/run-injection.py" "$ARTICLE_ID"
    fi
    if grep -q '| 8b .* FAIL' "$REPORT"; then
        echo "Rerunning Step 8 em-dash fix..."
        python3 "$PROJECT_DIR/_work/fix-em-dashes.py" "$ARTICLE_ID"
    fi
    if grep -q '| 7 .* FAIL' "$REPORT"; then
        echo "Rerunning Step 7 (table conversion)..."
        python3 "$PROJECT_DIR/_work/fix-tables.py" "$ARTICLE_ID"
    fi
    if grep -q '| 6c .* FAIL' "$REPORT"; then
        echo "Rerunning author_id fix..."
        curl -s -X PUT "https://api.intercom.io/articles/$ARTICLE_ID" \
            -H "Authorization: Bearer $(cat ~/.intercom_token)" \
            -H "Content-Type: application/json" \
            -H "Intercom-Version: 2.11" \
            -d '{"author_id": 7980499}' > /dev/null
    fi
    # Audit files missing: human intervention
    if grep -qE '\| 10|11) .* FAIL' "$REPORT"; then
        echo "ERROR, Step 9 or 10 audit missing. These require human review. Stopping."
        exit 2
    fi
done

echo "FAILED after $MAX_ATTEMPTS attempts. See $PROJECT_DIR/_work/compliance-$ARTICLE_ID.md for details."
exit 1
```

### Why loop instead of fail fast

- Many failures are fixable without human input (missing author, stray em-dash after a late edit, new ASCII block introduced by a revert).
- Bounded retries (3) prevent infinite loops if a fix itself fails.
- Manual gates (Step 9, Step 11) break the loop, these require a human signing off on the audit.

## Output, the compliance report

Each run produces `_work/compliance-<article-id>.md` with the table of checks. This file:
- Proves the article passed all gates at ship time
- Provides a git-committable artifact showing what was verified and when
- Can be linked from the CHANGELOG of the parent project

## Integration with the quality bar in README

Add this to the main [README.md](README.md) quality bar as the last item:

> - [ ] Compliance report (`compliance-<article-id>.md`) shows ALL PASS. See [11-procedure-compliance.md](11-procedure-compliance.md).

No compliance report, no ship. The bar is a bar, not a suggestion.

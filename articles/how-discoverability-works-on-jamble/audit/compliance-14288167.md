# Compliance Audit: article 14288167 (How Discoverability Works on Jamble)

Audience: buyer_br. State: published.

## PR #91 / #92 contract checks

| Rule | Status |
|---|---|
| heading_hierarchy (1 H1 only) | PASS. Both pt-br.md and en.md have exactly one `# `. |
| mockup_orphan_html | PASS. Orphan HTMLs from prior version (category-tabs, discoverability-tabs, discovery-tabs) deleted. All HTMLs match a declared screen. |
| source_of_truth_path_missing | PASS. flow.yml.source_of_truth.ios_files lists 7 verified Swift / xcstrings files. |
| icons_match_ios_source (rule 10e) | N/A. No screen declares `icons_match_ios_source` review check. All three screens use Option B: `html_must_not_contain: ["<img", "<svg", "icon-"]` and the HTMLs satisfy it (type-only chrome). 0 unanchored screens. |
| em-dashes | PASS. Zero em-dashes in pt-br.md or en.md. |
| pt-br PRIMARY | PASS. metadata.yml `default_locale: pt-br`. |
| no R$ in EN | PASS. Article does not mention prices in either locale. `currency_required: false`. |
| xcstrings verbatim | PASS. Save Search subtitle, Members/Shows tabs, Follow empty-state strings copied verbatim from xcstrings (see code-audit). |
| no invented UI | PASS. Only described surfaces: 3 home tabs, Members/Shows search sub-tabs, Save Search prompt, filter fields, sort options. All grep-able. |
| audit cites file:line | PASS. code-audit-14288167.md cites Swift files with explicit line ranges. |

## CONCEPT ARTICLE doctrine (rerun-1, still applies)

Algorithmic ranking factors not traceable to iOS code were dropped. See "Claims dropped vs prior version" in code-audit-14288167.md (11 dropped claims, including For You weights, live/upcoming ranking signals, hardcoded category list, verified-seller boost, paid promotion claim, new-buyer feed, seller-side advice, search by sellers ranking, saved-search match indicator).

## Risk flags

None.

## Resolved decisions

None.

## Final verdict

Article passes all hard contracts and concept-article doctrine. Ready for validate gate.

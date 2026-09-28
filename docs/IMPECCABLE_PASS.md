# Impeccable design pass

This pass applies the official [Impeccable skill](https://github.com/pbakaus/impeccable/blob/9d715cc4f5564a990ca8345abfdd5df6dc9b41c8/plugin/skills/impeccable/SKILL.md), version 4.4.0, using its context, polish, and craft-floor guidance. Source revision: `9d715cc4f5564a990ca8345abfdd5df6dc9b41c8`.

## What applying a skill means

A skill supplies instructions and evaluation criteria for the coding assistant. It is not a theme that visitors download. Here, the assistant read the official skill, ran its context loader and design detector, and changed the actual website files accordingly. The Impeccable checkout and engine were used locally; they are not website dependencies or an installed global skill.

## Changes and reasons

| Change | Why it helps |
| --- | --- |
| Resource descriptions increased from 13px to 16px | Longer summaries are easier to read |
| Metadata increased from 9–10px to 13px | Cost, scope, and inspection dates remain legible |
| Controls have a 48px minimum height and 16px text | Easier touch interaction and readable mobile inputs |
| Removed section eyebrows and decorative 01–04 numbering | Headings and topic names carry the hierarchy directly |
| Simplified topic chips to plain metadata | Resource titles and descriptions have more visual prominence |
| Reduced hero spacing and unboxed topic explanations | The library is reached sooner with less decorative structure |
| Set the existing serif headline upright | Resolves the detector's italic-serif-display warning while preserving the palette and serif voice |
| Added a clear-all-filters button to empty results | Visitors can recover where the problem appears |
| Reset returns keyboard focus to search | Makes the next action easy for keyboard users |
| Added shared spacing/color values, explicit focus and forced-color styles | Future design edits are more consistent and accessible |

Resource data, descriptions, external destinations, publishing, and discovery logic are unchanged. The existing green editorial identity and resource-card layout remain recognizable.

## Verification

- All 16 existing Python regression tests passed; static-site generation and JavaScript syntax checks passed.
- Impeccable's detector ran once. It reported the italic-serif-display warning; the subsequent style change explicitly sets that headline upright.
- Browser checks at 1440px and 390px: no horizontal overflow.
- Search for AgentDojo: 1 result. Governance topic: 7 results. Unmatched search: 0 results; clear-all restores 25.
- Mobile resource text and controls were visually inspected. No JavaScript console errors were captured.

These checks are not a complete WCAG audit or a cross-browser certification. No detector rerun or score is claimed after the headline adjustment.

## Maintain the design

Edit `site/style.css` for appearance, `site/index.html` for page structure, `scripts/build.py` for generated resource markup, and `site/app.js` for filters. Run `python3 scripts/build.py` after edits. The generated README still comes from the same catalog.

For another pass, ask: “Apply Impeccable polish to this library, preserve its visual identity, and put the changes in a PR.” For a deliberate new visual direction, request a redesign instead. See [Impeccable's installation instructions](https://github.com/pbakaus/impeccable#installation) if you want it installed for recurring use in your coding environment.

# Hodl my b — weekly magazine

Weekly glossy round-up of everything shipped that week. White architect theme. Landing: `/hodl-my-b` (hodl-my-b.html). Issues: `/hodl-my-b/<n>` (hodl-my-b/<n>.html). Shared page-turn: `hodl-my-b/mag.css` + `mag.js` (arrows, swipe, buttons, `#p<n>`; no JS / reduced motion = pages stacked).

## Make issue N
1. Copy `hodl-my-b/<N-1>.html` to `hodl-my-b/<N>.html`. Update title, canonical, og/twitter url, description, image (`og-hodl-my-b-<N>.png`), alt.
2. Cover (`.pg.cover`): masthead, `Issue N · week of <Monday date>`, cover story line, 4–5 teaser lines.
3. Cover story: 3–5 `.pg` spreads. Each feature carries a pill: `Live` / `Next release` / `Coming`. Only what is true today.
4. "This week": bullets from `/releases` for the week (skip anything naming a competitor wallet).
5. "Also this week": `.grid4` of the pages' existing `og-*.png` cards, each linking to its page.
6. Update each `.folio` (Issue N, p.X) and the last page.
7. OG: copy `media-src/og/og-hodl-my-b-1.html` → `-N.html`, edit text, screenshot to `og-hodl-my-b-N.png` (Twemoji only). Read the PNG before committing.
8. Landing: add the new issue at the top of `.issues`.
9. `python3 scripts/seo-head.py && python3 scripts/gen-llms.py`, check 390px width has no horizontal scroll, commit, push, curl for 200s.

## Rules
Funny, consumer-facing, fait accompli. No real people's names, no competitor names, no investment wording.

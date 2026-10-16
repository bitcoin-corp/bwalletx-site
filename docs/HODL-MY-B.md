# Hodl my b — weekly magazine

Weekly glossy round-up of everything shipped that week. White architect theme. Landing: `/hodl-my-b` (hodl-my-b.html). Issues: `/hodl-my-b/<n>` (hodl-my-b/<n>.html). Built by `scripts/hodl-my-b.py`: a page-flip book (page-flip@2.0.7 from jsDelivr, same lib as npgx's MagazineFlipReader). /hodl-my-b = latest issue. Two-page spreads on desktop, one page on phones; swipe/drag/arrows; `#p<n>` deep links; no JS or reduced motion = stacked pages.

## Make issue N
1. In `scripts/hodl-my-b.py` add the issue to `ISSUES` (n, week = Monday date, story, og, blurb) and write `pages_issue_N(back)`, copying `pages_issue_1`. Keep an even page count; first and last are hard covers (back cover lists past issues).
2. Cover: masthead, dateline, cover story, cover lines. Then cover-story pages, "New in <release>" from /releases, "Also this week" grids of existing og-*.png cards (each linking to its page), Where things stand, Next week.
3. Every feature gets a pill: Live / Next release / Coming. Only what is true today. Each page must fit its page (check screenshots).
4. OG: copy `media-src/og/og-hodl-my-b-1.html` to `-N.html`, edit, screenshot to `og-hodl-my-b-N.png` (Twemoji only). Read the PNG.
5. `python3 scripts/hodl-my-b.py && python3 scripts/seo-head.py && python3 scripts/gen-llms.py`
6. Screenshot 430px and 1440px, Read them, commit, push, check 200s.

## Look
Full-screen glossy brochure: every page fills the viewport (two-page spread on desktop >= 900px, one page on phones). Scenes are classes on each page: s-cover, s-black, s-back (gold on black), s-cream, s-yellow, s-pink, s-lime, s-paper, s-orange, s-peach, s-gold. Children with r1..r4 and .media rise in as the page turns in; a sheen sweeps across.

## Media slots
Each slot is `<div class="media" data-media="NAME">`. To use the owner's photo or video, set `MEDIA = {"cover": "/media/hodl/cover.jpg", "bbrand": "/media/hodl/bbrand.mp4"}` in `scripts/hodl-my-b.py` and rebuild. A .mp4 plays muted and loops; anything else is an image (object-fit: cover). Leave a slot out to keep the built-in art.
Issue 1 slots: cover, bbrand, checkout, allowance, sms, receipts, release, next.

## Rules
Funny, consumer-facing, fait accompli. No real people's names, no competitor names, no investment wording. og images keep 1200:630 (object-fit: cover).

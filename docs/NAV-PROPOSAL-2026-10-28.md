# bwalletx.com navigation: audit + proposal (28 Oct 2026)

Status: PROPOSAL ONLY. Nothing shipped. Base design = vexvoid's `/Volumes/2026/Projects/VexVoid/BWALLETX-NAV-PROPOSAL.md` (already shown to the owner). This doc adds the measured audit, the orphan list, the item-by-item mapping, the /features regrouping, and the gaps where that design doesn't yet give a page a home.

Source audited: `nav.js` and `features.html` at origin/main `c4bff88`.

## 1. Audit

### 1a. How the nav is built
- `nav.js` builds everything from one `NAV.full` config: desktop hover dropdowns (`.nd-menu`, one column, no max-height, no scroll), the phone **Menu** panel (one `<details>` accordion per section, with internal scroll at `max-height: calc(100vh - 120px)`), and a **section pill row** under the bar listing every page in the current section (hidden on phones since 23 Oct).
- The "in-page menu" on /features is that pill row: the **27 Wallet pills, which wrap to 3 rows (112px)** under the bar. `features.html` itself has no anchor nav. It has 10 `<section class="fgroup">` blocks (see 1e).
- The label the owner calls "Features" is the **Wallet** tab (its first item is Features, and it links to /features).

### 1b. Every menu item (old menu → new home)
Desktop dropdowns and phone accordions use the same list, so there's one table. 102 items: Wallet 27, Exchange 7, Social 20, Artists 4, bApps 19, Agents 11, Developers 9 + 5 blog posts. Items marked `**` don't fit vexvoid's lists cleanly (see section 4).

| Old menu | Label | URL | New home |
|---|---|---|---|
| Wallet | Features | /features | Wallet (overview) |
| Wallet | Subscriptions | /subscriptions | Wallet |
| Wallet | Pots | /pots | Wallet |
| Wallet | Lock | /lock | Wallet |
| Wallet | Token locking | /token-locking | Exchange |
| Wallet | Seedless login | /seedless-login | Wallet › Security |
| Wallet | Restore | /restore | Wallet › Restore & recover |
| Wallet | RelayX NFTs | /recover-relayx | Wallet › Restore & recover |
| Wallet | History | /history | Wallet |
| Wallet | Identity | /identity | You |
| Wallet | Handles | /handles | You |
| Wallet | Names | /names | You |
| Wallet | Signed names | /name-bindings | You (Signed names) |
| Wallet | bAvatars | /bavatars | You |
| Wallet | Themes | /themes | You (Themes & editions) |
| Wallet | Custom editions | /themes/custom | You (Themes & editions) |
| Wallet | Business agents (coming) | /business-agents | Create & sell overview only (coming) |
| Wallet | SMS (coming) | /sms | You/Social overview only (coming) |
| Wallet | NFTs | /nfts | Exchange |
| Wallet | Your character | /your-character | You |
| Wallet | Swap into BSV | /swap | Wallet |
| Wallet | Mint | /mint | Create & sell |
| Wallet | Notifications | /push-notifications | Wallet (Notifications) |
| Wallet | Extension | /extension | Footer (downloads) + wallet button |
| Wallet | iPhone | /iphone | Footer (downloads) |
| Wallet | Android | /android | Footer (downloads) |
| Wallet | Testers | /testers | Footer |
| Exchange | Exchange | /exchange | Exchange (overview) |
| Exchange | Strategies | /exchange/strategies | Exchange overview page (not in menu: 7 slots used)** |
| Exchange | Token curves | /token-curves | Exchange |
| Exchange | PNEEs | /pnees | Exchange |
| Exchange | Launchpad | /launchpad | Exchange |
| Exchange | Store | /store | Exchange |
| Exchange | Buy BSV | /buy | Wallet |
| Social | Social | /social | Social (overview) |
| Social | Chat | /chat | Social |
| Social | Friends | /friends | Social |
| Social | Lounge | /lounge | Social |
| Social | Games | /games | Social |
| Social | Video | /video | Social |
| Social | Live | /live | Social |
| Social | Tips | /tips | Social |
| Social | Streaming payments | /streaming-payments | Create & sell |
| Social | Credits (in testing) | /credits | Create & sell |
| Social | bSpaces | /bspaces | Social |
| Social | bPhone | /bphone | Social |
| Social | bMail | /bmail | Social |
| Social | b*X services | /services | bApps grid |
| Social | bPositive (coming) | /bpositive | Social overview only (coming) |
| Social | Airdrops | /airdrops | Exchange |
| Social | Your signature | /sign | You (Your signature) |
| Social | Sign in with X | /x | You › Sign-in options |
| Social | Sign in with HandCash | /sign-in-with-handcash | You › Sign-in options |
| Social | Sign in with Gmail | /gmail | You › Sign-in options |
| Artists | Artists | /artists | Create & sell (Artists) |
| Artists | VexVoid | /artists/vexvoid | Inside Artists page |
| Artists | AIVJ | /aivj | Inside Artists page |
| Artists | b creative | /b-creative | Create & sell |
| bApps | All bApps | /bapps | bApps grid icon |
| bApps | bMovies | /bapps/bmovies | bApps grid |
| bApps | bBots | /b-bots | bApps grid? NOT PLACED in vexvoid file** |
| bApps | bChatX | https://chat.bwalletx.com | bApps grid |
| bApps | bMailX | https://bmailx.com | bApps grid |
| bApps | bRadioX | https://bradiox.com | bApps grid |
| bApps | bCalX | https://bcalx.com | bApps grid |
| bApps | bJobsX | https://bjobsx.com | bApps grid |
| bApps | bNewsX | https://bnewsx.com | bApps grid |
| bApps | bMusicX | https://bmusicx.com | bApps grid |
| bApps | bStoreX | https://bstorex.com | bApps grid |
| bApps | bMintX: FLICK OFF | https://bmintx.com/flick-off | bApps grid |
| bApps | bVideoX | https://bvideox.com | bApps grid |
| bApps | bFriendsX | https://bfriendsx.com | bApps grid |
| bApps | bDojoX | https://bdojox.com | bApps grid |
| bApps | bDriveX | https://bdrivex.com | bApps grid |
| bApps | bShares: registers for any company | /bshares | Create & sell |
| bApps | Partnership shares (coming) | /partnership-shares | Create & sell overview (coming) |
| bApps | bWeb (coming) | /bweb | Create & sell overview (coming) |
| Agents | Agent accounts | /agents | Build |
| Agents | b agent | /agent | Build (b agent) |
| Agents | Feedback | /feedback | Footer |
| Agents | Ideas | /ideas | Footer |
| Agents | Bugs | /bugs | Footer |
| Agents | b-Aware | /b-Aware | Wallet › Security + Footer |
| Agents | Hold to talk | /hold-to-talk | Build overview page (not in vexvoid list)** |
| Agents | Strategies | /strategies | Build |
| Agents | Strategy spec | /strategies/spec | Inside Strategies page |
| Agents | CLI | /cli | Build |
| Agents | MCP | /mcp | Build |
| Developers | Developers | /developers | Build (overview) |
| Developers | Sign in with bWalletX | /connect | Build |
| Developers | Add your app | /apps/add | Build |
| Developers | CLI | /cli | Build |
| Developers | MCP | /mcp | Build |
| Developers | Open source | /open-source | Build |
| Developers | Blog | /blog | Right: Blog |
| Developers | Releases | /releases | Build |
| Developers | Hodl my b · weekly | /hodl-my-b | Inside Blog |
| Developers | 053 Friends, bPics, video | /blog/053-friends-bpics-and-video | Blog page (drop "Latest" from menu) |
| Developers | 052 Tip buttons | /blog/052-tip-buttons | Blog page (drop "Latest" from menu) |
| Developers | 051 Spaces on a schedule | /blog/051-spaces-schedule-and-ask-b | Blog page (drop "Latest" from menu) |
| Developers | 050 AIVJ — VexVoid, live | /blog/050-aivj-tv-vexvoid-live | Blog page (drop "Latest" from menu) |
| Developers | 049 The Exchange, sorted | /blog/049-the-exchange-sorted | Blog page (drop "Latest" from menu) |

Phone menu extras (not in the dropdowns): `Web wallet →` (web.bwalletx.com) plus follow links X, Twetch, GitHub, YouTube, and bChatX Lounge. **Proposal:** these go in the footer. The Web wallet link becomes the wallet button.

### 1c. Rendered heights (measured headless, Chromium, `/features`)
| Menu | Items | Desktop 1440x900 (bottom edge, px) | Phone 390x844 accordion height (px; panel viewport is 723) |
|---|---|---|---|
| Wallet | 27 | **978: OVERFLOWS by 78px.** The last items (Android, Testers) are unreachable: no scroll | **971: taller than the panel**; must scroll inside the menu |
| Exchange | 7 | 318 | 291 |
| Social | 20 | 747 (fits at 900; overflows on any viewport under ~760px tall, e.g. 1366x768 with browser chrome) | **733: taller than the panel** |
| Artists | 4 | 219 | 189 |
| bApps | 19 | 714 (borderline) | 699 |
| Agents | 11 | 450 | 427 |
| Developers | 14 | 579 | 558 |
| Phone menu, all open | 102 | | scrollHeight 4004 vs 723 visible |
| /features pill row | 27 | 3 wrapped rows, 112px, pushes content down | hidden |

**AFTER mock (vexvoid tree):** the tallest desktop dropdown ends at **324px** (2 columns). The tallest phone accordion is **256px**. No horizontal scroll at either width (scrollWidth = viewport).

### 1d. Orphans: pages in the sitemap or llms.txt (blog posts excluded) that are in no menu
71 pages, plus 5 non-page entries (`/.well-known/agent.json`, `/.well-known/mcp.json`, `/api/agent/products`, `/connect.md`, `/llms-full.txt`), which are machine files and correctly stay out of the nav. "Links in" = the number of HTML files that link to the page (1 usually means only the page itself).

| Page | Title | Links in | Proposed home |
|---|---|---|---|
| /get | Get bWalletX | 218 | Wallet button target + footer |
| /web | bWalletX web wallet | 1 | Footer downloads (Web) |
| /desktop | bWalletX Desktop | 4 | Footer downloads |
| /testers/bwallet/android, /testers/bwallet/iphone, /testers/bwalletx/{chrome-extension,desktop,web} | Testers per platform | 4-6 | Inside /testers (footer) |
| /migrate | Move to bWalletX | 14 | Wallet › Restore & recover page |
| /sweep-simplycash | Sweep SimplyCash | 2 | Wallet › Restore & recover page |
| /seedless-signin | Sign in with a passkey | 4 | Wallet › Security page. **Duplicate of /seedless-login?** Consider a redirect |
| /btrust | bTrust | 4 | Wallet › Security page ** (no slot in vexvoid list) |
| /lock/verify | Verify a lock | 4 | Inside /lock |
| /identity-map | Identity map | 3 | Inside You › Identity |
| /wallet-frames | Wallet Frames | 1 | You overview ** |
| /themes-custom | Branded wallets for businesses | **0** | You › Themes & editions; or redirect to /themes/custom |
| /clients | Your own branded wallet (business) | 3 | Create & sell overview (business) ** |
| /b-aware | b-Aware (lower-case alias) | 4 | Same page as /b-Aware; footer |
| /ask-b, /talk-to-b | Ask b / Talk to b | 11 / 6 | Build › b agent page. **Possible conflict:** memory says the route is /ask-b and /agent redirects. Check which page is canonical |
| /bchatx | bChatX | 2 | Social › Chat page + bApps grid |
| /bradio | bRadio | 1 | bApps grid / Social overview |
| /contracts | Contracts in chat | 3 | Social overview |
| /verify-note | Verify a signed note | 1 | Inside bMail |
| /person | Send a bMail | 1 | Stays out (share target) |
| /invite | You're invited | 15 | Stays out (invite landing) |
| /gigs, /jobs | bGigs / Jobs | 1 / 1 | **No home in vexvoid tree.** Suggest Social overview or bApps grid (bJobsX) ** |
| /bounties | Bounties | 3 | Footer, next to b-Aware ** |
| /bads | bAds | 2 | Create & sell (bAds) |
| /bad | bAds (old) | **0** | Redirect to /bads |
| /partners | Partners | 2 | Create & sell |
| /culture | Culture: make it on BSV | 1 | Candidate overview page for Create & sell |
| /digital-ice-cream | Digital Ice-Cream | 4 | Inside Artists |
| /happy-b | Happy b-day cards | 1 | Inside b creative |
| /flick-off | FLICK OFF | 1 | bApps grid (bMintX) |
| /b-market | bMarketX | 2 | bApps grid |
| /bgitx | bGitX | 2 | bApps grid / Build overview |
| /tokenblaster | tokenblaster.lol | 1 | bApps grid / Social › Games |
| /b/acc, /b/acc/store, /race-card | bAcc + theme + racing game | 2 / 2 / **0** | bApps grid (bAcc tile); store links to Themes |
| /direct | bWallet Direct | 2 | Build › Sign in with bWalletX page |
| /sign-in-button | Add Sign in with bWalletX | 4 | Build › Sign in with bWalletX page |
| /hodl-my-b/0, /hodl-my-b/1 | Hodl my b editions | 7 / 3 | Inside Blog › Hodl my b |
| /newsletter | Newsletter | 1 | Footer ** |
| /brand | The bWalletX brand | 2 | Footer ** |
| /b-family | The b family | 12 | Footer |
| /privacy, /terms | Legal | 32 / 2 | Footer |
| /on-b, /your-apps-on-b | Your apps on b | 13 / 1 | Build overview (campaign hub for the *-on-b pages) |
| /coingeek-on-b, /hodlocker-on-b, /peck-on-b, /relayx-on-b, /treechat-on-b, /twetch-on-b, /yours-on-b, /b-on-twetch | Partner "X on b" pages | 2 each | Stay out of nav, listed on /on-b |
| /be-on-b, /be-on-b-2, /be-on-b-3 | be on b (campaign variants) | 1-3 | Stay out (campaign/ad landings) |
| /b-cool, /b-in-black, /b-is-coming, /just-b, /b-is-for-auteurs, /b-is-for-business, /b-is-for-shopkeepers | b campaign pages | 1-13 | Stay out of nav. Suggest a "Campaigns" list on /b-family so they're reachable |

Count: 71 orphan pages. After the proposal, 0 have no route: each is in a tab, the footer, the bApps grid, or linked from a named hub page. About 15 hub links don't exist yet and need adding (those with 0-1 links in).

### 1e. /features page sections today
| Section | Cards |
|---|---|
| Send and receive | 13: Pay a name, Dollars first, Receive, Buy BSV, Tokens and NFTs, Airdrops inbox, History and exports, Tips, Pots and standing orders, App subscriptions, Lock BSV, Several accounts, bCredits |
| Names and identity | 10: Your name, Signed by you, Name Store, Link your accounts, Linked wallets, Identity map, Profile and bAvatar, Look-alike protection, Sign-in alerts, Verified identity |
| Messages and calls | 11: Friends, Chat, bMail, Voice and video calls, Push notifications, Token rooms, bSpaces, bPhone, Contracts in chat, Tickets and bounties, bWallet Lounge |
| Feed and media | 3: One feed for BSV social, Lock to like, Media player |
| Make things | 7: Private by default, Mint NFTs, Mint tokens, Your personal token, Launch a coin, Token locking, Airdrop to holders |
| Exchange and Store | 5: Exchange, Memepool, Safety filter, Store and themes, Edit home |
| Apps and websites | 4: Connect to websites, Pair by QR, Allowed stays allowed, Desktop |
| b and agents | 5: Ask b, Hold to talk, Agent accounts, CLI and MCP, Business agents |
| Security and recovery | 12: Non-custodial, Approve every request, Passkey sign-in, Face ID and fingerprint, Restore from anywhere, Encrypted backups, Sweep another wallet, Troubleshooting, Passwords, bTrust, Open source, Delete your account |
| Coming | 2: Share one fact, Creator vesting |

## 2. Proposed tree (vexvoid's, unchanged)
```
[bWalletX]  Wallet  You*  Exchange  Social  Create & sell*  Build        Blog  [▦ bApps*]  [ WALLET BUTTON ]
Wallet        Features overview · Buy BSV · Swap into BSV · Pots · Lock · Subscriptions · History · Notifications · Restore & recover · Security
You*          Handles · Names · Signed names · Identity · Your signature · bAvatars · Your character · Themes & editions · Sign-in options
Exchange      Exchange · Launchpad · Token curves · Token locking · NFTs · PNEEs · Store · Airdrops
Social        Chat · Friends · bSpaces · Lounge · Live · Video · Games · Tips · bPhone · bMail
Create & sell* Artists · Mint · Streaming payments · Credits · bAds · Business agents(coming → overview only) · b creative · Partners · bShares · bWeb(coming → overview only)
Build         b agent · Agent accounts · Strategies · CLI · MCP · Developers · Sign in with bWalletX · Add your app · Open source · Releases
Footer        Feedback · Ideas · Bugs · b-Aware · Privacy · b-family · Testers · Downloads (Extension, iPhone, Android, Web)
```
`*` = open owner choice, shown with purple tags in the mock and NOT decided here:
1. "You" or "Identity".
2. bApps as a grid icon (right side) or a 7th tab.
3. "Create & sell" or "Creators". We avoid "earn" because it's on the banned list: investment-adjacent wording.

Desktop: 2-column dropdown with an "overview →" header link. Phone: Menu → 6 accordions (2-column grid inside), then Blog and bApps. The pill row under the bar would show the current tab's ≤10 items, so it can't sprawl to 27 again.

## 3. /features regrouped into the 6 tabs
Each section gets an anchor (`#wallet`, `#you`, …). A wrapping chip row of 6 jump links (no horizontal scroll) replaces the 27-pill row on this page.
| New section | Cards (from today's sections) |
|---|---|
| **Wallet** | Pay a name, Dollars first, Receive, Buy BSV, History and exports, Pots and standing orders, App subscriptions, Lock BSV, Several accounts, Push notifications, Edit home · all of Security and recovery (12) · Desktop |
| **You** | All of Names and identity (10), Share one fact (coming) |
| **Exchange** | Exchange, Memepool, Safety filter, Tokens and NFTs, Airdrops inbox, Token locking, Launch a coin, Store and themes ** (themes belong to You; split the card or link both) |
| **Social** | Friends, Chat, bMail, Voice and video calls, Token rooms, bSpaces, bPhone, Contracts in chat, Tickets and bounties, bWallet Lounge, Tips · all of Feed and media (3) |
| **Create & sell** | Private by default, Mint NFTs, Mint tokens, Your personal token, Airdrop to holders, bCredits, Business agents (coming), Creator vesting (coming) |
| **Build** | Connect to websites, Pair by QR, Allowed stays allowed · Ask b, Hold to talk, Agent accounts, CLI and MCP |

Sizes: Wallet would get about 25 cards. Either split it into two sub-heads (Money / Security & recovery) or move Security into its own sub-section. Recommend sub-heads.

## 4. Where the audit doesn't fit vexvoid's design (flags)
1. **Pages with no slot:** /b-bots (bBots), /hold-to-talk, /exchange/strategies, /strategies/spec, /btrust, /bounties, /jobs + /gigs, /newsletter, /brand, /wallet-frames, /clients, /services (b*X services). Suggested homes are in the tables above, mostly overview pages, the footer or the bApps grid. The owner/vexvoid should confirm.
2. **The footer grows:** vexvoid lists 8 entries. Adding Bounties, Brand, Newsletter, Terms and the follow links (X, Twetch, GitHub, YouTube, Lounge) makes about 15. It needs a multi-column footer.
3. **Downloads leave the tabs:** Android, iPhone, Extension, Desktop and Web move to the footer and the wallet button. Check that the wallet button's not-installed state offers platform choice. /desktop and /web are in no list today.
4. **Duplicates to resolve (redirects, owner call):** /seedless-signin vs /seedless-login; /bad → /bads; /themes-custom vs /themes/custom; /b-aware vs /b-Aware; /ask-b vs /agent vs /talk-to-b; /pnee → /pnees (already aliased).
5. **Blog "Latest 5" in the Developers menu is dropped.** The Blog page lists posts. The nav.js comment telling publishers to update it would need removing.
6. **Store edition (bwallet.space)** has its own 4-item nav. Untouched by this proposal.
7. **Phone header:** at 390px, logo + wallet button + Menu leaves about 150px for the button. The wallet button must have a compact phone state (the mock's placeholder wraps to 3 lines).
8. **Social overview/You overview for "coming" items:** SMS and bPositive need an overview page that lists them. /social exists. "You" has no overview page yet (/identity could serve).
9. **Copy:** "earn" doesn't appear in the proposed labels. Streaming payments and Credits under "Create & sell" are fine as labels.

## 5. Screenshots (scratch only, not in git)
`/private/tmp/claude-501/-Volumes-2026-Projects-bwalletx-x/dfd7e1ee-9558-49e5-9071-7e0e82e684cf/scratchpad/nav/`
- before-1440-wallet.png: Wallet ("Features") dropdown runs off the bottom
- before-1440-artists.png: Artists, 4 items
- before-390-menu-wallet.png: phone menu, Wallet accordion longer than the screen
- after-1440-wallet.png, after-1440-create.png: mock, 2-column dropdowns
- after-390-menu-social.png: mock phone menu
- mock.html: the static prototype

## 6. Live local preview (added 28 Oct, uncommitted)
- `nav.js` now builds the proposed tree, with all 102 old items mapped as in 1b. It also adds the bApps grid, the footer columns and a "Get bWalletX" placeholder in the wallet-button slot (the official button isn't on main yet).
- `features.html`: 76 cards regrouped into the 6 tabs with sub-heads, plus a wrapping jump-chip row.
- Mock options switcher (purple, bottom right) on localhost only. It's also settable by URL: `?you=identity&bapps=tab&create=creators`.
- Served by a scratch clean-URL server on http://127.0.0.1:8788.

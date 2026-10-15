# bWalletX roadmap: the one checklist

Checked 15 Oct 2026 against the code. Released build: **5.2.24** (`e66af734` in bwalletX `bwallet`). Live web: bwalletx.com, web.bwalletx.com, desktop.bwalletx.com, www.bchatx.com.

Status key:
- **LIVE**: a user can do it today, in 5.2.24 or on the live web.
- **MERGED-UNRELEASED**: merged into `bwallet`; ships in 5.2.25.
- **IN-PROGRESS**: an open PR or partial code. The entry says what is missing.
- **NOT-STARTED**: no code.
- **WRONG**: the page claimed something untrue. Fixed in the `docs/roadmap-truth` PR unless marked *open*.

PR numbers: `yours-mobile#N` is b0ase/yours-mobile, the bwalletX working repo. `bit-sign#N` is the bChatX/bit-sign server.

When an item changes, update its page and this file in the same PR.

---

## WRONG (fixed in this PR unless marked open)

| Page | Claim | Truth | Evidence |
|---|---|---|---|
| bspaces.html | Paid tickets "Coming" | LIVE since 5.1.91 (pay at the door) | `src/mobile/spaces/door.ts` |
| bspaces.html | Per-minute charges "Coming" | LIVE since 5.1.95 (paid listening) | `src/mobile/spaces/paidListen.ts`, bit-sign `lib/paid-listening.ts` |
| live.html | Pay-per-minute watching "Coming" | LIVE for Spaces (5.1.95) | same |
| live.html | Tips during a stream "Coming" | LIVE (speaker tiles, 5.2.16) | `spaces/SpeakerGrid.tsx` → `TipButton` |
| chat.html | One-to-many video "Not built yet" | LIVE: Broadcast into a Space (5.2.17) | `spaces/broadcast.ts` |
| hold-to-talk.html | "coming to bChatX.com" | LIVE on bchatx.com/ask-b since 12 Oct | bit-sign #181, `HoldToTalkB.tsx` |
| identity-map.html | "coming in the next release" | LIVE since 5.1.88 | `settings/IdentityMap.tsx`, /releases#v5.1.88 |
| bavatars.html | 5.1.97 card marked "soon" | LIVE since 5.1.97 | /releases#v5.1.97 |
| index.html | "Live in 5.1.85"; a "Coming next" block that was 3/4 already live | Relabelled 5.2.24; block now says three shipped | /releases |
| airdrops.html | Public page URL `bwalletx.com/bchat/u/<name>` (404) | The page is `bchatx.com/u/<name>` | curl: 404 vs 200 |
| partnership-shares.html | "Multisig locks" listed as working in bWalletX | Only the bCorp register (members and director, restricted); partner locks are PR yours-mobile#47 | `placement/VaultSection.tsx` |
| partnership-shares.html | "Automatic splits by set shares" listed as working | Only paid Spaces' equal stage split; no split by set shares | `paidListen.ts` |
| credits.html | "The card row in the release app" listed as Coming | Swipe cards shipped in 5.2.23 | /releases#v5.2.23 |
| cli.html, mcp.html | Minting "Coming" | Built in the bwalletx-cli repo (0.5.0); npm still has 0.2.0 | `bwalletx-cli/src/mint.ts`; `npm view bwalletx` |
| blog/index 026, 027, 030 | "next release" / "not yet released" | Shipped 5.1.85 / 5.1.85 / 5.1.87 | /releases |
| blog 005 | "Chat … not live yet" | Chats update live in 5.2.24 | /releases#v5.2.24 |
| *open* releases.html 5.2.23 | "bCredits: top up with BSV at 1p per credit" | Top-up works only once `BCREDITS_TREASURY_ADDRESS` is set on bit-sign; otherwise the wallet shows "coming soon". The owner was still to supply the treasury key on 14 Oct. **Owner to confirm**, then reword the note if needed. | bit-sign `src/lib/credits.ts` `creditsEnabled` |
| *open* index/get/download | App Store "not submitted yet" | Can't be checked from code. Submitting has had standing approval since 14 Oct. **Owner to confirm the App Store Connect state.** | — |

## LIVE (pages say Live; spot-checked)

- Airdrops inbox and address (5.1.85; sender shown 5.2.9+). airdrops.html
- Lock BSV, gradual payouts, verify page (5.1.84). lock.html, token-locking.html
- History: on-chain history, ranges, CSV/PDF, categories, connections log, Gains (beta) (5.1.81–5.1.85). history.html
- Pots, standing orders, subscriptions to bCorp services, reminders (5.1.75, 5.1.91). pots.html, subscriptions.html
- Restore/sweep from bWalletX, Yours, Panda, RelayX, Twetch, SimplyCash, BIP44, custom path, WIF, xprv, Money Button. restore.html
- Handles: $handles, numbered handles, renames, personal token and room; sign in with X/Google; card signature; Sign in with bWalletX. handles.html
- Identity: Veriff via bit-sign, certificate in wallet, sign and seal on bit-sign, deal-room checks, delete account. identity.html
- Chat: message boards, token-gated rooms (not store), DMs, 1:1 voice/video, tips; Broadcast (5.2.17). chat.html
- Spaces: stage, raise hand, Lounge, pay at the door (5.1.91), paid listening (5.1.95), tips (5.2.16), Broadcast (5.2.17), green room; bChatX /s pages for guests. bspaces.html, live.html, gigs.html, bradio.html
- bRadio: podcast episodes and podcast NFTs. bradio.html
- bPhone paid calls (5.1.87). bphone.html, blog 030
- Pay-per-message room charges (5.1.85). blog 026
- Launch your own coin in-wallet (5.1.85, 5.2.19); Launchpad trading. launchpad.html
- bAvatars on bChatX, paymail and the wallet card (5.1.95/5.1.97). bavatars.html
- Identity map (5.1.88). identity-map.html
- Hold to talk: wallet (5.1.89) and bChatX Ask b. hold-to-talk.html
- Push notifications (5.1.70). push-notifications.html
- Token curves (people tokens sold from own supply, 5.2.16). token-curves.html
- bMail price-to-reach ("Penny post"). bmail.html
- bShares: The Bitcoin Corporation register only, for members and the director (private testing). bshares.html, blog 056
- CLI/MCP: pair, balance, send, buy, strategies (npm 0.2.0). cli.html, mcp.html
- bApps: sign in and pay with the wallet. bapps.html

## MERGED-UNRELEASED (ships in 5.2.25)

| Item | Page | Evidence |
|---|---|---|
| More than one handle per account (up to 5, one main) | handles.html (updated) | yours-mobile#91 merged; bit-sign #272 merged |
| Android direct-APK in-app updater | android.html | yours-mobile#102 |
| Address book import/export | — | yours-mobile#105 |
| Spaces show every screen share and camera | — | yours-mobile#107; bit-sign #281 (web side still open) |
| Backup file named per account; desktop download | — | yours-mobile#103 |
| CLI/MCP minting (needs an npm publish, not a wallet release) | cli.html, mcp.html | bwalletx-cli 0.5.0 `src/mint.ts` |

## IN-PROGRESS, ranked by how close each is to done

1. **bCredits top-up.** The code is in 5.2.23/5.2.24 and on the server. Missing: the owner sets `BCREDITS_TREASURY_ADDRESS` (an offline key); VAT answer from the accountant. credits.html. *Can deliver as soon as the owner acts.*
2. **CLI/MCP minting on npm.** Built at 0.5.0. Missing: `npm publish`. cli.html, mcp.html. *Can deliver soon.*
3. **Token locking (BSV-21).** yours-mobile#61 (lock until a date, receipt, verifier). Missing: the owner's tiny mainnet test that indexers still show locked tokens, then merge. Unblocks **creator vesting** (launchpad.html) and **airdrops that unlock over time** (airdrops.html). features.html, token-locking.html, index.html.
4. **Branded Space banner.** Live on bchatx.com Space pages and share cards (bit-sign #274/#275). Missing: the banner on wallet Space tiles. gigs.html
5. **Selective disclosure ("show one fact", e.g. over 18).** bit-sign `identity/cert/grants` route exists (503 until the table is migrated). Missing: the migration and a wallet UI. identity.html
6. **bShares for any company, and partnership shares.** yours-mobile#46/#47, bit-sign #242/#244 (migrations not run). Missing: review, migrations, a real-key test of the partner lock, owner sign-off. bshares.html, partnership-shares.html, blog 055, blog 056. *To go live:* merge #46→#47 and #242→#244, run the migrations, test the partner lock end to end with recovery from seed, then release.
7. **PNEE pots.** Types and UI exist, but the wallet says "PNEE pots aren't available yet" (`pots/pots.ts`). Missing: pricing and paying PNEE amounts from a pot. pots.html, subscriptions.html
8. **bApp five-button bar.** Desktop prototype, bMovies only (`wide/bapps.ts`). Missing: the phone shell, more bApps and greyed slots. bapps.html, bapps/bmovies.html
9. **Invites: Open Drops and Named Invites** (two products). *Open Drops*: a link holding a token, first to open claims it (being built). *Named Invites*: only one named X account can claim, token sent automatically (planned; yours-mobile#106). invite.html, blog 057.
10. **bPics market.** yours-mobile#38, bit-sign #233 (moderation pipeline).
11. **Play your music video into a Space.** Possible today by sharing a tab with Broadcast. Missing: a built-in synced player and repeat. gigs.html
12. **Investor journey.** bShares placement (restricted) exists. Missing: one-tap pay from the wallet and a single flow. identity.html

## NOT-STARTED (pages say Coming or planned; no code found)

- Paid speakers (pay to come up on stage). bspaces.html
- Bigger audiences (more than one SFU). live.html
- Album Spaces. gigs.html
- Game Spaces. blog 033
- Airdrop address and QR on the bChatX public profile. airdrops.html
- Sending airdrops to holders, followers or rooms. launchpad.html, blog 027
- Handle NFTs. handles.html
- Pre-signed (nLockTime) pot payments while the app is closed. pots.html, subscriptions.html
- Subscribe with bWalletX (an API for apps). subscriptions.html
- One-tap sign and seal from the card. sign.html
- Per-transaction chain check during bPhone calls. blog 030
- Room message limits per minute/hour/day. blog 026
- Self-serve deletion of an ID check. identity.html
- OAuth "Sign in with bWalletX for any app" (auth.bwalletx.com doesn't resolve). sign-in-button.html, connect.html
- CLI selling and listing. cli.html, mcp.html
- Credits from other issuers. credits.html
- bTrust: shared keys, passing on, important papers. btrust.html
- **bPositive** (all items). bpositive.html, blog 029. *To go live:* signed journey records, pledges held in pots, 2-of-3 witness confirmation with verified identities, thank-you NFTs, report/block, 18+ gate.
- bWeb (settings, Ask b add-ons, own versions). bweb.html, bapps.html
- Like = 1¢ to fund and join the room. bapps.html, bapps/bmovies.html
- bMovies: per-second streaming, Twatch comments, friend movies, "make me a movie" (not checked in the bMovies repo; bMovies is on hold). bapps/bmovies.html
- Server licence change to FSL (bit-sign is Open BSV License v4 today). open-source.html

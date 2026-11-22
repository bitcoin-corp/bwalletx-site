# Add Sign in with bWalletX to your app

Source: https://bwalletx.com/connect (this file: https://bwalletx.com/connect.md). Last checked against connect.js and @bwalletx/connect 0.9.0 on 22 Nov 2026; signing in on the same phone needs bWalletX 5.2.61 or later. Full docs: https://docs.bwalletx.com/developers/connect/

## In 30 seconds

One script tag on your page, two routes on your server.

```html
<script src="https://bwalletx.com/connect.js"></script>
```

- `bWalletX.renderButton('#signin', { onClick })` draws the gold "Sign in with bWalletX" button.
- `bWalletX.signIn({ challenge, pairing })` finds the user's wallet (Chrome extension, the bWalletX app's browser, a phone by QR code or by an Open bWalletX button on the phone itself, or the web wallet), asks your server for a one-time challenge, and has the wallet sign it with a key derived from its **identity key**.
- Your server checks the signature with `@bsv/sdk`, deletes the nonce, and signs the user in as that identity key.
- No API key, no client ID, no account with us. Nothing passes through bwalletx.com except the script itself. The only service of ours involved is the encrypted pairing relay, and only when the user signs in from a phone or the web wallet.

The user's identity key (a 33-byte compressed public key, 66 hex characters) is their user ID on your site. It is the same key every time they sign in with the same wallet.

## Three ways the user's wallet can answer

| Where the user is | How your page reaches the wallet | What you need |
|---|---|---|
| Chrome or Brave with the bWalletX extension | BRC-100 wallet discovery: dispatch `brc100:requestWallet`, take the `brc100:announceWallet` reply whose `info.rdns` is `com.bwalletx.extension` | Nothing extra. connect.js finds it |
| Your site opened inside the bWalletX app's own browser | Same discovery; the app announces `rdns: space.bwallet.mobile` and also sets `window.CWI` | Nothing extra. connect.js finds it |
| bWalletX on a phone, or the web wallet at web.bwalletx.com | Pairing: your page makes a `https://www.bwallet.space/pair?...` link. On a computer it shows as a QR code for the phone to scan; the web wallet takes it pasted. On the phone itself it is an **Open bWalletX** button, and bWalletX sends the user back to your site afterwards. All of them then talk to your page through `relay.bwallet.space`, end-to-end encrypted | A `pairing` option. `pairingModal()` from the full build draws the QR code or the button for you |

All three give you the same thing: an object with the BRC-100 `WalletInterface` methods. Sign-in is the same code for all of them.

## 1. Browser: one script tag

`connect.js` is small. It loads the full sign-in build (`https://bwalletx.com/connect/bwalletx-connect.global.js`, @bwalletx/connect 0.9.0, about 570 KB or 170 KB gzipped, with `@bsv/sdk` inside) the first time you call `signIn`, `pair`, `renderButton` or `load`, so those return promises. This example uses the build's `pairingModal()` for pairing: a QR code on a computer, an **Open bWalletX** button on a phone. You can pass your own `{ onLink, onCode }` instead and draw the QR code with any library.

```html
<div id="signin"></div>
<div id="bwx-pair"></div>

<script src="https://bwalletx.com/connect.js"></script>
<script>
  const panel = document.getElementById('bwx-pair');

  async function post(url, body) {
    const res = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || 'HTTP ' + res.status);
    return res.json();
  }

  bWalletX.renderButton('#signin', {
    onClick: async (button) => {
      button.disabled = true;
      // Only shown when there is no extension or in-app browser: a QR code on a computer, Open bWalletX on a phone.
      const pairing = (await bWalletX.load()).pairingModal();
      try {
        const r = await bWalletX.signIn({
          // 1. Your server makes a one-time challenge. identityKey is usually undefined: the wallet is then
          //    asked for the key and the signature together, in one approval.
          challenge: (identityKey) => post('/auth/bwalletx/challenge', { identityKey }),
          // 2. Phone or web wallet.
          pairing,
        });
        // 3. Your server checks the signature and starts a session.
        const { identityKey } = await post('/auth/bwalletx/verify', {
          identityKey: r.identityKey, nonce: r.nonce, signature: r.signature,
        });
        panel.textContent = 'Signed in as ' + identityKey.slice(0, 12) + '…  (via ' + r.method + ')';
      } catch (e) {
        if (e.message === 'cancelled') panel.textContent = '';
        else if (e.code === 'RETURNED_IN_ANOTHER_TAB') panel.textContent = 'You finished in another tab. Carry on there.';
        else panel.textContent = e.code === 'NOT_FOUND' ? 'bWalletX was not found.' : e.message;
      } finally {
        pairing.close();
        button.disabled = false;
      }
    },
  });
</script>
```

`bWalletX.signIn` looks for a wallet in this order:

1. The bWalletX Chrome extension (BRC-100 discovery, `rdns` `com.bwalletx.extension`). `method: 'extension'`.
2. The bWalletX app's in-app browser (`rdns` `space.bwallet.mobile`). A bare `window.CWI` is not taken as bWalletX: other wallets set it too. `method: 'in-app'`.
3. A pairing saved by an earlier sign-in in this browser (in `localStorage` under `bwalletx.connect.pairing.v1`). `method: 'pairing'`.
4. A new pairing, if you passed `pairing`: `onLink` gets a `https://www.bwallet.space/pair?...` link to show as a QR code (and as text for web.bwalletx.com), and `onCode` gets a 4-digit code both screens show. `pairingModal()` does both, and on a phone shows the link as an Open bWalletX button. `method: 'pairing'`.

If none of these works it throws an error with `code: 'NOT_FOUND'`. Closing the pairing screen rejects with the message `cancelled`. It returns `{ identityKey, signature, nonce, method, wallet }`. Post the first three to your verify route. `wallet` is a BRC-100 `WalletInterface` you can keep using.

Other things on `window.bWalletX`:

| Call | What it does |
|---|---|
| `bWalletX.connect({ timeout })` | The extension only, authenticated: `{ wallet, info, identityKey }`. Rejects with `code: 'NOT_INSTALLED'`. Doesn't load the full build. |
| `bWalletX.pair({ onLink, onCode })` | A wallet paired by QR or pasted link, without signing in. |
| `bWalletX.renderButton(el, { onClick, subtitle })` | The gold button. `subtitle: false` hides the second line. |
| `bWalletX.load()` | The full build's exports (`signInWithBwalletX`, `pairBwalletX`, `pairingModal`, `resumeReturnedPairing`, `restorePairing`, `clearPairing`, `findBwalletX`, ...). |

Prefer to host it yourself? Copy `connect.js` and `connect/bwalletx-connect.global.js` to the same folder structure on your site; connect.js loads the full build from next to itself. The full build is the npm package's `dist/bwalletx-connect.global.js`, byte for byte (0.9.0: `sha384-ljVpAVRFkV0Eog6yjxI9c5nJKl0Ri9p77SuIPOohuhh6O1SygKqR1cprJ7kJfrK5`). It is also on npm: `pnpm add @bwalletx/connect @bsv/sdk`.

### On a phone

On a phone there is no QR code to scan. `pairingModal()` shows **Open bWalletX**; the user taps Connect in bWalletX, and bWalletX (5.2.61 or later) opens your site's **home page** with the result in the fragment, `https://example.com/#bwx=ok&…`, usually in a new tab. It always returns to the root, never to another path: the page the sign-in started on is kept in the user's own browser. So your home page finishes it. Put this first in its `<head>`, before analytics or any other script, with no `defer` or `async`: the build takes the fragment out of the address bar as it loads, so nothing else reads it.

```html
<script src="https://bwalletx.com/connect/bwalletx-connect.global.js"></script>
<script>
  // Finish the pairing (it is saved in this browser), then go back to the page the sign-in started on.
  bWalletXConnect.resumeReturnedPairing().then((r) => {
    if (r && r.page && r.page !== location.origin + location.pathname) location.replace(r.page);
  });
</script>
```

Back on your sign-in page, the next tap of the button reuses the saved pairing (no new code to match), and bWalletX asks the user to approve the sign-in. The tab the sign-in started in stops with `code: 'RETURNED_IN_ANOTHER_TAB'`.

For one approval instead of two, use the `<bwalletx-signin>` element (see [the button page](https://bwalletx.com/sign-in-button)) on your sign-in page and your home page: it sends the challenge with the pairing, so bWalletX shows one "Connect and sign in" card, and it finishes the return, posts to your verify route and goes back by itself.

## The button

<!-- preview -->

`bWalletX.renderButton()` draws this for you. If you draw your own, use the gold button. Keep the label "Sign in with bWalletX". The logo is at `https://bwalletx.com/logo.svg` (the gold b, viewBox 74 x 100). Don't recolour it; it sits on a black circle so it reads on the gold.

```html
<button type="button" id="bwx-signin" class="bwx-signin">
  <span class="bwx-mark"><img src="https://bwalletx.com/logo.svg" alt="" width="15" height="20"></span>
  <span class="bwx-label">Sign in with bWalletX<small>also works with bWallet</small></span>
</button>
<div id="bwx-pair"></div>
```

```css
.bwx-signin {
  display: inline-flex; align-items: center; gap: 12px;
  min-height: 48px; padding: 10px 22px 10px 10px;
  border: 0; border-radius: 12px; cursor: pointer;
  background: linear-gradient(180deg, #fcd34d, #f59e0b);
  color: #000; text-align: left;
  font: 700 16px/1.2 system-ui, -apple-system, "Segoe UI", sans-serif;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.2);
}
.bwx-signin:hover { background: linear-gradient(180deg, #fde68a, #fbbf24); }
.bwx-signin:focus-visible { outline: 2px solid #ffd24d; outline-offset: 3px; }
.bwx-signin:disabled { opacity: 0.6; cursor: wait; }
.bwx-signin .bwx-mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 50%; background: #000; flex: none;
}
.bwx-signin small { display: block; font-size: 11px; font-weight: 500; color: rgba(0, 0, 0, 0.6); }
```

Put it first among your wallet options. The second line ("also works with bWallet") is optional: bWallet is the store edition of the same wallet and signs in the same way.

## 2. Server: issue and verify challenges

The server half is not in the script (it must run on your server). Install `@bwalletx/connect` and import from `@bwalletx/connect/server`, or copy this file into your project as `bwalletx-server.ts`. Its only dependency is `@bsv/sdk` (2.2 or later). It is the same code as the sign-in part of `@bwalletx/connect/server` 0.9.0, so the two are interchangeable; the package also has shared nonce stores (`redisStore`, `pgStore`), sessions and payment checks.

```ts
import { ProtoWallet, PublicKey, type WalletProtocol } from '@bsv/sdk';

/** Security level 2, a protocol name used for nothing else. Keep it constant. */
export const LOGIN_PROTOCOL: WalletProtocol = [2, 'bwallet sign in'];
export const CHALLENGE_LIFETIME_MS = 2 * 60 * 1000;

export interface PendingChallenge {
  /** The key the challenge was made for, or '' when none was given (verifySignIn then binds the claimed key). */
  identityKey: string;
  origin: string;
  message: string;
  expiresAt: number;
}

/**
 * Where challenges wait between the two routes. Use Redis or a database table in production.
 * `take` must read and delete in one step, so each nonce can be tried once.
 */
export interface NonceStore {
  put(nonce: string, c: PendingChallenge): Promise<void> | void;
  take(nonce: string): Promise<PendingChallenge | null> | PendingChallenge | null;
}

let warned = false;

/**
 * In-memory store. For development and tests only: it is lost on restart and not shared between
 * server processes or serverless instances. Expired entries are pruned on each put.
 */
export function memoryStore(opts: { quiet?: boolean } = {}): NonceStore {
  const prod = typeof process !== 'undefined' && process.env?.NODE_ENV === 'production';
  if ((prod || !opts.quiet) && !warned) {
    warned = true;
    console.warn(
      prod
        ? '[@bwalletx/connect] WARNING: the in-memory nonce store is running in production. It is not shared between instances and breaks on serverless. Use redisStore or pgStore.'
        : '[@bwalletx/connect] Using the in-memory nonce store. It is for development only; pass a shared store (redisStore, pgStore) in production.',
    );
  }
  const m = new Map<string, PendingChallenge>();
  return {
    put(nonce, c) {
      const now = Date.now();
      for (const [k, v] of m) if (v.expiresAt < now) m.delete(k);
      m.set(nonce, c);
    },
    take(nonce) {
      const c = m.get(nonce) ?? null;
      m.delete(nonce);
      return c;
    },
  };
}

let defaultStore: NonceStore | null = null;
const storeOrDefault = (s?: NonceStore) => s ?? (defaultStore ??= memoryStore());

export function isIdentityKey(x: unknown): x is string {
  if (typeof x !== 'string' || !/^0[23][0-9a-fA-F]{64}$/.test(x)) return false;
  try {
    PublicKey.fromString(x);
    return true;
  } catch {
    return false;
  }
}

function normalOrigin(origin: string): string {
  const u = new URL(origin);
  if (u.origin === 'null' || u.origin !== origin.replace(/\/$/, '')) {
    throw new Error(`origin must be scheme://host[:port], got ${origin}`);
  }
  return u.origin;
}

/** The text the user signs. Lines joined with \n, no trailing newline. */
export function loginMessage(origin: string, nonce: string, expiresAt: number): string {
  return [
    `Sign in to ${new URL(origin).host} with bWallet`,
    '',
    'This proves you hold this wallet. It does not spend anything.',
    '',
    `Origin: ${origin}`,
    `Nonce: ${nonce}`,
    `Expires: ${new Date(expiresAt).toISOString()}`,
  ].join('\n');
}

function randomNonce(): string {
  const b = new Uint8Array(16);
  globalThis.crypto.getRandomValues(b);
  let s = '';
  for (const x of b) s += String.fromCharCode(x);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export interface CreateChallengeOptions {
  /** YOUR site's origin from config, e.g. "https://example.com". Never take it from the request. */
  origin: string;
  /**
   * The identity key the browser claims, checked again at verify. Optional since 0.5.5: leave it out so the browser
   * can ask the wallet for the key and the signature in ONE sheet; verifySignIn then binds the key the browser claims,
   * and the signature only verifies for that key. A challenge made WITH a key still only verifies for that key.
   */
  identityKey?: unknown;
  /** Default: a process-wide in-memory store (dev only). */
  store?: NonceStore;
}

export interface ChallengeResponse {
  nonce: string;
  message: string;
  protocolID: WalletProtocol;
  keyID: string;
  expiresAt: number;
}

/** Step 1. Throws if an identityKey is given and is not a valid compressed public key. Send the result to the browser. */
export async function createChallenge(opts: CreateChallengeOptions): Promise<ChallengeResponse> {
  const given = opts.identityKey !== undefined && opts.identityKey !== null && opts.identityKey !== '';
  if (given && !isIdentityKey(opts.identityKey)) throw new Error('identityKey must be a compressed public key (66 hex chars)');
  const boundKey = given ? (opts.identityKey as string).toLowerCase() : '';
  const origin = normalOrigin(opts.origin);
  const nonce = randomNonce();
  const expiresAt = Date.now() + CHALLENGE_LIFETIME_MS;
  const message = loginMessage(origin, nonce, expiresAt);
  await storeOrDefault(opts.store).put(nonce, { identityKey: boundKey, origin, message, expiresAt });
  return { nonce, message, protocolID: LOGIN_PROTOCOL, keyID: nonce, expiresAt };
}

export interface VerifySignInOptions {
  /** YOUR site's origin from config. Must equal the origin the challenge was made for. */
  origin: string;
  /** From the request body. */
  identityKey: unknown;
  nonce: unknown;
  signature: unknown;
  store?: NonceStore;
}

/**
 * Step 2. Returns the proven identity key (lowercase hex), or null.
 * The nonce is deleted before anything is checked, so each challenge can be tried once.
 */
export async function verifySignIn(opts: VerifySignInOptions): Promise<string | null> {
  if (typeof opts.nonce !== 'string' || opts.nonce.length > 64) return null;
  const c = await storeOrDefault(opts.store).take(opts.nonce);
  if (!c || Date.now() > c.expiresAt) return null;
  let origin: string;
  try {
    origin = normalOrigin(opts.origin);
  } catch {
    return null;
  }
  if (c.origin !== origin) return null;
  if (!isIdentityKey(opts.identityKey)) return null;
  const identityKey = opts.identityKey.toLowerCase();
  // A challenge made for a key only verifies for that key. One made without a key binds the key claimed now: the
  // signature below is checked against exactly this key, so a wrong claim fails.
  if (c.identityKey && c.identityKey !== identityKey) return null;

  const sig = opts.signature;
  if (!Array.isArray(sig) || sig.length < 8 || sig.length > 80 || !sig.every((b) => Number.isInteger(b) && b >= 0 && b <= 255)) {
    return null;
  }
  try {
    const { valid } = await new ProtoWallet('anyone').verifySignature({
      protocolID: LOGIN_PROTOCOL,
      keyID: opts.nonce,
      counterparty: identityKey,
      data: Array.from(new TextEncoder().encode(c.message)),
      signature: sig as number[],
    });
    return valid ? identityKey : null;
  } catch {
    return null; // @bsv/sdk throws on a bad signature instead of returning valid: false
  }
}

/** True when a request's Origin header is exactly your configured origin. Check it on both routes. */
export function originAllowed(requestOrigin: string | null | undefined, origin: string): boolean {
  try {
    return !!requestOrigin && requestOrigin === normalOrigin(origin);
  } catch {
    return false;
  }
}
```

Two routes. This example uses Express; any framework works the same way.

```ts
// Two routes (Express). Any framework works the same way.
import express from 'express';
import { createChallenge, verifySignIn, originAllowed, memoryStore } from './bwalletx-server.js';

const ORIGIN = 'https://example.com'; // your site, from config. Never from the request.
const store = memoryStore();          // dev only: use Redis or a database table in production
const app = express();
app.use(express.json());

// POST /auth/bwalletx/challenge   body: {} (or { identityKey })
app.post('/auth/bwalletx/challenge', async (req, res) => {
  if (!originAllowed(req.get('origin'), ORIGIN)) return res.status(403).end();
  try {
    res.json(await createChallenge({ origin: ORIGIN, identityKey: req.body?.identityKey, store }));
  } catch (e) {
    res.status(400).json({ error: (e as Error).message });
  }
});

// POST /auth/bwalletx/verify   body: { identityKey, nonce, signature }
app.post('/auth/bwalletx/verify', async (req, res) => {
  if (!originAllowed(req.get('origin'), ORIGIN)) return res.status(403).end();
  const identityKey = await verifySignIn({ origin: ORIGIN, store, ...req.body });
  if (!identityKey) return res.status(401).json({ error: 'That signature was not accepted. Start again.' });
  // identityKey is the user's stable id. Find or create the account keyed on it, then start your session.
  res.json({ identityKey });
});

app.listen(3000);
```

`verifySignIn` returns the identity key (66 lowercase hex characters) or `null`. It refuses a nonce that was already used, has expired (2 minutes), was issued for another origin or another identity key, or whose signature doesn't verify. `identityKey` is optional in `createChallenge`: a challenge made without one binds the key the browser claims at verify, and the signature only verifies for that key. That is what lets the wallet show one approval for the key and the signature.

`memoryStore()` is for development: it is lost on restart and isn't shared between processes or serverless instances. In production pass a store whose `take(nonce)` reads and deletes in one step, such as Redis `GETDEL` or a database `DELETE ... RETURNING`.

## Exactly what is signed

The server builds this text, sends it to the browser, and keeps a copy. The wallet signs the UTF-8 bytes of it unchanged. Lines are joined with `\n`, no trailing newline.

```
Sign in to example.com with bWallet

This proves you hold this wallet. It does not spend anything.

Origin: https://example.com
Nonce: 3q2-7wEXAMPLEnonce0Q8w
Expires: 2026-10-07T12:02:00.000Z
```

(The second and fourth lines are empty.) This is the same text bChat and bChatX use. The wallet does not parse it; any text works, but keep your origin, the nonce and the expiry in it so the user can see what they are approving and a signature made for your site is worthless anywhere else.

The signature call, as the wallet receives it:

| Field | Value |
|---|---|
| `protocolID` | `[2, 'bwallet sign in']` (security level 2: the derived key depends on the counterparty) |
| `keyID` | the nonce |
| `counterparty` | `'anyone'` |
| `data` | the UTF-8 bytes of the text, as `number[]` |
| result `signature` | DER-encoded ECDSA signature, as `number[]` |

The signing key is derived (BRC-42) from the wallet's root identity private key towards "anyone", for that protocol and keyID. Anyone holding only the identity public key can derive the matching public key, which is what `new ProtoWallet('anyone').verifySignature({ ..., counterparty: identityKey })` does (BRC-3). Only the holder of the identity private key can make the signature.

## Security notes

- **One try per nonce.** Delete the challenge before you check the signature, as `verifySignIn` does. A challenge that survives a failed attempt can be retried.
- **Two-minute expiry.** Check it on the server. Don't trust an expiry sent by the browser.
- **The nonce is also the keyID,** so each challenge is signed by a different derived key. A signature for one nonce can't be used for another.
- **Build the text on the server** and verify against your stored copy. Never verify text the browser sends you.
- **Use your configured origin** in the text, not a value from the request. Refuse challenge and verify calls whose `Origin` header isn't your site.
- **Bind the challenge to an identity key.** A challenge made for a key only verifies for that key; one made without a key binds the key claimed at verify, and the signature is checked against exactly that key.
- **`verifySignature` throws** on a bad signature in @bsv/sdk instead of returning `valid: false`. Catch it and treat it as a failure.
- **Check the key is a real point:** `PublicKey.fromString` throws for a 66-hex string that isn't on the curve.
- **Rate-limit** the challenge route per IP and per identity key. It is unauthenticated.
- **Sessions are yours.** After `verifySignIn` returns a key, issue your normal session cookie. The wallet does not give you a token.
- **Privacy.** The identity key is the same on every site the user signs in to with this method, so two sites can tell it is the same wallet. Tell your users this if it matters to them.
- **Pairing.** The relay passes on the WebSocket `Origin` of whatever opened the channel, and the wallet refuses to pair if it differs from the origin in the link. A script outside a browser can send any `Origin`, so bWalletX's approval sheets for a paired site say "a site that claims to be" your host. The relay only sees ciphertext. The pairing key connect.js makes is random and is not a wallet key.
- **The phone return** goes only to the root of the origin the relay saw. Its fragment counts only once the relay's wallet confirms the same key, it is used once, and the build strips it from the address bar as it loads. Load the build before any third-party script on your home page.
- **What the user sees.** The extension and the phone show their own approval prompt naming your site's host (taken from the page or the relay, not from your text). Nothing is spent.

## Not yet available

These are gaps today. Plan around them.

- **No hosted sign-in or OAuth-style redirect.** There is no bwalletx.com page you can send users to and get a callback from, and no hosted verify endpoint. You run the two routes yourself. bChat's own endpoints (`/api/bitsign/auth/bwallet/*` on bChatX) accept requests from their own pages only and are not a public API.
- **No user profile.** You get the identity key and nothing else: no $handle, paymail, name or picture, and no proof linking the key to them.
- **The relay is ours.** `relay.bwallet.space` accepts any https origin, but it is a single service run by The Bitcoin Corporation with no published uptime or rate-limit guarantees (it currently allows about 60 frames a minute per channel).
- **No test wallet.** There is no testnet build or headless bWalletX for automated tests. To test your server, sign with `new ProtoWallet(PrivateKey.fromRandom()).createSignature(...)` using the same arguments; it makes exactly the signature bWalletX makes.

## For AI agents

Follow these steps in order. Do not invent packages, endpoints or methods that are not on this page. For a bundled app, install `@bwalletx/connect` and `@bsv/sdk`; for a plain HTML site, use the script tag.

1. Install `@bwalletx/connect` and `@bsv/sdk` in the server project (pnpm, npm or yarn, whichever the project uses).
2. Create `bwalletx-server.ts` with the code in section 2, unchanged. Put your site's origin (scheme + host, no trailing slash, e.g. `https://example.com`) in config.
3. Add two POST routes. `/auth/bwalletx/challenge`: `createChallenge({ origin: ORIGIN, identityKey: body.identityKey, store })` (`identityKey` may be missing), return the result as JSON, 400 if it throws. `/auth/bwalletx/verify`: `verifySignIn({ origin: ORIGIN, store, identityKey, nonce, signature })` from the body. Reject both with 403 unless `originAllowed(request Origin header, ORIGIN)`.
4. Replace `memoryStore()` with a shared store (database table or Redis) if you run more than one server process or run serverless. `take(nonce)` must read and delete in one step.
5. In the verify route, when `verifySignIn` returns a key: find the user whose bWalletX identity key equals it, or create one, then start your normal session. Return 401 when it returns null.
6. On the sign-in page add `<script src="https://bwalletx.com/connect.js"></script>` and the code from section 1: `bWalletX.renderButton(...)` with an `onClick` that calls `bWalletX.signIn({ challenge, pairing })` and posts `identityKey`, `nonce` and `signature` to the verify route. Keep the `pairing` option (`pairingModal()` from `bWalletX.load()`) so phone and web wallet users can sign in.
7. On the home page, first in `<head>` with no `defer` or `async`, add the full build and the `resumeReturnedPairing()` snippet from "On a phone", so signing in on the same phone comes back to the sign-in page.
8. If your page uses a bundler, the same calls work: `window.bWalletX` is set once the script tag has loaded.
9. Test the server without a wallet: `const k = PrivateKey.fromRandom()`, call the challenge route with `k.toPublicKey().toString()`, sign the returned `message` with `new ProtoWallet(k).createSignature({ protocolID, keyID, counterparty: 'anyone', data: Array.from(Buffer.from(message, 'utf8')) })`, post `{ identityKey, nonce, signature }` to verify and expect success. Post the same body again and expect 401.
10. Test by hand: with the bWalletX extension in Chrome, click the button and approve. Without it, scan the QR with bWalletX on a phone, check the 4-digit codes match, tap Connect, approve. On the phone itself, tap the button, tap Open bWalletX, tap Connect, and check you land back on the sign-in page.

Questions: support@bwalletx.com

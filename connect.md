# Add Sign in with bWalletX to your app

Source: https://bwalletx.com/connect (this file: https://bwalletx.com/connect.md). Last checked against bWalletX 5.1.75, connect.js and @bsv/sdk 2.8.11 on 7 Oct 2026.

## In 30 seconds

One script tag on your page, two routes on your server.

```html
<script src="https://bwalletx.com/connect.js"></script>
```

- `bWalletX.renderButton('#signin', { onClick })` draws the gold "Sign in with bWalletX" button.
- `bWalletX.signIn({ challenge, pairing })` finds the user's wallet (Chrome extension, the bWalletX app's browser, or a phone or the web wallet by QR code), asks your server for a one-time challenge, and has the wallet sign it with a key derived from its **identity key**.
- Your server checks the signature with `@bsv/sdk`, deletes the nonce, and signs the user in as that identity key.
- No API key, no client ID, no account with us. Nothing passes through bwalletx.com except the script itself. The only service of ours involved is the encrypted pairing relay, and only when the user signs in from a phone or the web wallet.

The user's identity key (a 33-byte compressed public key, 66 hex characters) is their user ID on your site. It is the same key every time they sign in with the same wallet.

## Three ways the user's wallet can answer

| Where the user is | How your page reaches the wallet | What you need |
|---|---|---|
| Chrome or Brave with the bWalletX extension | BRC-100 wallet discovery: dispatch `brc100:requestWallet`, take the `brc100:announceWallet` reply whose `info.rdns` is `com.bwalletx.extension` | Nothing extra. connect.js finds it |
| Your site opened inside the bWalletX app's own browser | Same discovery; the app announces `rdns: space.bwallet.mobile` and also sets `window.CWI` | Nothing extra. connect.js finds it |
| bWalletX on a phone, or the web wallet at web.bwalletx.com | Pairing: your page shows a `https://www.bwallet.space/pair?...` link as a QR code. The phone scans it; the web wallet takes it pasted. Both then talk to your page through `relay.bwallet.space`, end-to-end encrypted | A `pairing` option with somewhere to show the QR code. connect.js does the rest |

All three give you the same thing: an object with the BRC-100 `WalletInterface` methods. Sign-in is the same code for all of them.

## 1. Browser: one script tag

`connect.js` is small. It loads the full sign-in build (`https://bwalletx.com/connect/bwalletx-connect.global.js`, about 125 KB with `@bsv/sdk` inside) the first time you call `signIn`, `pair` or `renderButton`, so those three return promises. This example uses qrcodejs from cdnjs to draw the QR code; any QR library works.

```html
<div id="signin"></div>
<div id="bwx-pair"></div>

<script src="https://bwalletx.com/connect.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
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
      try {
        const r = await bWalletX.signIn({
          // 1. Your server makes the challenge for this identity key.
          challenge: (identityKey) => post('/auth/bwalletx/challenge', { identityKey }),
          // 2. Only used when there is no extension or in-app browser: phone or web wallet.
          pairing: {
            onLink: (link) => {
              panel.replaceChildren();
              new QRCode(panel, { text: link, width: 220, height: 220 });
              const p = document.createElement('p');
              p.textContent = 'Scan with bWalletX on your phone, or paste this link into web.bwalletx.com: ' + link;
              panel.append(p);
            },
            onCode: (code) => panel.append('Check bWalletX shows ' + code + ', then tap Connect.'),
          },
        });
        // 3. Your server checks the signature and starts a session.
        const { identityKey } = await post('/auth/bwalletx/verify', {
          identityKey: r.identityKey, nonce: r.nonce, signature: r.signature,
        });
        panel.textContent = 'Signed in as ' + identityKey.slice(0, 12) + '…  (via ' + r.method + ')';
      } catch (e) {
        panel.textContent = e.code === 'NOT_FOUND' ? 'bWalletX was not found.' : e.message;
      } finally {
        button.disabled = false;
      }
    },
  });
</script>
```

`bWalletX.signIn` looks for a wallet in this order:

1. The bWalletX Chrome extension (BRC-100 discovery, `rdns` `com.bwalletx.extension`). `method: 'extension'`.
2. The bWalletX app's in-app browser (`rdns` `space.bwallet.mobile`, or `window.CWI` if nothing announced). `method: 'in-app'`.
3. A pairing saved by an earlier sign-in in this browser (in `localStorage` under `bwalletx.connect.pairing.v1`). `method: 'pairing'`.
4. A new pairing, if you passed `pairing`: `onLink` gets a `https://www.bwallet.space/pair?...` link to show as a QR code (and as text for web.bwalletx.com), and `onCode` gets a 4-digit code both screens show. `method: 'pairing'`.

If none of these works it throws an error with `code: 'NOT_FOUND'`. It returns `{ identityKey, signature, nonce, method, wallet }`. Post the first three to your verify route. `wallet` is a BRC-100 `WalletInterface` you can keep using.

Other things on `window.bWalletX`:

| Call | What it does |
|---|---|
| `bWalletX.connect({ timeout })` | The extension only, authenticated: `{ wallet, info, identityKey }`. Rejects with `code: 'NOT_INSTALLED'`. Doesn't load the full build. |
| `bWalletX.pair({ onLink, onCode })` | A wallet paired by QR or pasted link, without signing in. |
| `bWalletX.renderButton(el, { onClick, subtitle })` | The gold button. `subtitle: false` hides the second line. |
| `bWalletX.load()` | The full build's exports (`signInWithBwalletX`, `pairBwalletX`, `restorePairing`, `clearPairing`, `findBwalletX`, ...). |

Prefer to host it yourself? Copy `connect.js` and `connect/bwalletx-connect.global.js` to the same folder structure on your site; connect.js loads the full build from next to itself. It is also on npm: `pnpm add @bwalletx/connect @bsv/sdk`.

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

The server half is not in the script (it must run on your server). Install `@bwalletx/connect` and import from `@bwalletx/connect/server`, or copy this file into your project as `bwalletx-server.ts`. Its only dependency is `@bsv/sdk` (2.2 or later, 2.x or 3.x). It is the same code as `@bwalletx/connect/server`, so the two are interchangeable.

```ts
import { ProtoWallet, PublicKey, type WalletProtocol } from '@bsv/sdk';

/** Security level 2, a protocol name used for nothing else. Keep it constant. */
export const LOGIN_PROTOCOL: WalletProtocol = [2, 'bwallet sign in'];
export const CHALLENGE_LIFETIME_MS = 2 * 60 * 1000;

export interface PendingChallenge {
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
  if (!opts.quiet && !warned) {
    warned = true;
    console.warn('[@bwalletx/connect] Using the in-memory nonce store. It is for development only; pass a shared store (Redis, database) in production.');
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
  /** The identity key the browser claims. Checked again at verify. */
  identityKey: unknown;
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

/** Step 1. Throws if identityKey is not a valid compressed public key. Send the result to the browser. */
export async function createChallenge(opts: CreateChallengeOptions): Promise<ChallengeResponse> {
  if (!isIdentityKey(opts.identityKey)) throw new Error('identityKey must be a compressed public key (66 hex chars)');
  const origin = normalOrigin(opts.origin);
  const nonce = randomNonce();
  const expiresAt = Date.now() + CHALLENGE_LIFETIME_MS;
  const message = loginMessage(origin, nonce, expiresAt);
  await storeOrDefault(opts.store).put(nonce, { identityKey: opts.identityKey.toLowerCase(), origin, message, expiresAt });
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
  if (c.identityKey !== identityKey) return null;

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

// POST /auth/bwalletx/challenge   body: { identityKey }
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

`verifySignIn` returns the identity key (66 lowercase hex characters) or `null`. It refuses a nonce that was already used, has expired (2 minutes), was issued for another origin or another identity key, or whose signature doesn't verify.

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

(The second and fourth lines are empty.) This is the same text bChat and bit-sign use. The wallet does not parse it; any text works, but keep your origin, the nonce and the expiry in it so the user can see what they are approving and a signature made for your site is worthless anywhere else.

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
- **Bind the challenge to the identity key** the browser claimed, and check it again at verify.
- **`verifySignature` throws** on a bad signature in @bsv/sdk instead of returning `valid: false`. Catch it and treat it as a failure.
- **Check the key is a real point:** `PublicKey.fromString` throws for a 66-hex string that isn't on the curve.
- **Rate-limit** the challenge route per IP and per identity key. It is unauthenticated.
- **Sessions are yours.** After `verifySignIn` returns a key, issue your normal session cookie. The wallet does not give you a token.
- **Privacy.** The identity key is the same on every site the user signs in to with this method, so two sites can tell it is the same wallet. Tell your users this if it matters to them.
- **Pairing.** The relay checks the WebSocket `Origin` of the page that opened the channel and tells the wallet; the wallet refuses to pair if it differs from the origin in the QR code. The relay only sees ciphertext. The pairing key connect.js makes is random and is not a wallet key.
- **What the user sees.** The extension and the phone show their own approval prompt naming your site's host (taken from the page or the relay, not from your text). Nothing is spent.

## Not yet available

These are gaps today. Plan around them.

- **No hosted sign-in or OAuth-style redirect.** There is no bwalletx.com page you can send users to and get a callback from, and no hosted verify endpoint. You run the two routes yourself. bChat's own endpoints (`/api/bitsign/auth/bwallet/*` on bit-sign) accept requests from their own pages only and are not a public API.
- **No user profile.** You get the identity key and nothing else: no $handle, paymail, name or picture, and no proof linking the key to them.
- **The relay is ours.** `relay.bwallet.space` accepts any https origin, but it is a single service run by The Bitcoin Corporation with no published uptime or rate-limit guarantees (it currently allows about 60 frames a minute per channel).
- **No test wallet.** There is no testnet build or headless bWalletX for automated tests. To test your server, sign with `new ProtoWallet(PrivateKey.fromRandom()).createSignature(...)` using the same arguments; it makes exactly the signature bWalletX makes.

## For AI agents

Follow these steps in order. Do not invent packages, endpoints or methods that are not on this page. For a bundled app, install `@bwalletx/connect` and `@bsv/sdk`; for a plain HTML site, use the script tag.

1. Install `@bwalletx/connect` and `@bsv/sdk` in the server project (pnpm, npm or yarn, whichever the project uses).
2. Create `bwalletx-server.ts` with the code in section 2, unchanged. Put your site's origin (scheme + host, no trailing slash, e.g. `https://example.com`) in config.
3. Add two POST routes. `/auth/bwalletx/challenge`: `createChallenge({ origin: ORIGIN, identityKey: body.identityKey, store })`, return the result as JSON, 400 if it throws. `/auth/bwalletx/verify`: `verifySignIn({ origin: ORIGIN, store, identityKey, nonce, signature })` from the body. Reject both with 403 unless `originAllowed(request Origin header, ORIGIN)`.
4. Replace `memoryStore()` with a shared store (database table or Redis) if you run more than one server process or run serverless. `take(nonce)` must read and delete in one step.
5. In the verify route, when `verifySignIn` returns a key: find the user whose bWalletX identity key equals it, or create one, then start your normal session. Return 401 when it returns null.
6. On the sign-in page add `<script src="https://bwalletx.com/connect.js"></script>` and the code from section 1: `bWalletX.renderButton(...)` with an `onClick` that calls `bWalletX.signIn({ challenge, pairing })` and posts `identityKey`, `nonce` and `signature` to the verify route. Keep the `pairing` option so phone and web wallet users can sign in; draw the QR code with any QR library.
7. If your page uses a bundler, the same calls work: `window.bWalletX` is set once the script tag has loaded.
8. Test the server without a wallet: `const k = PrivateKey.fromRandom()`, call the challenge route with `k.toPublicKey().toString()`, sign the returned `message` with `new ProtoWallet(k).createSignature({ protocolID, keyID, counterparty: 'anyone', data: Array.from(Buffer.from(message, 'utf8')) })`, post `{ identityKey, nonce, signature }` to verify and expect success. Post the same body again and expect 401.
9. Test by hand: with the bWalletX extension in Chrome, click the button and approve. Without it, scan the QR with bWalletX on a phone, check the 4-digit codes match, tap Connect, approve.

Questions: support@bwalletx.com

# Add Sign in with bWalletX to your app

Source: https://bwalletx.com/login (this file: https://bwalletx.com/login.md). Last checked against bWalletX 5.1.75 and @bsv/sdk 2.2.0, 2.8.11 and 3.1.0 on 7 Oct 2026.

## In 30 seconds

- Your server makes a one-time challenge: a short text that names your site, a random nonce and an expiry two minutes away.
- The user's bWalletX signs that text with BRC-100 `createSignature`, using a key derived from their wallet's **identity key** (protocol `[2, 'bwallet sign in']`, keyID = the nonce, counterparty `'anyone'`).
- Your server checks the signature with `@bsv/sdk` (`new ProtoWallet('anyone').verifySignature(...)`), deletes the nonce, and signs the user in as that identity key.
- No API key, no client ID, no account with us. Nothing passes through bwalletx.com. The only service of ours involved is the encrypted pairing relay, and only when the user signs in from a phone or the web wallet.

The user's identity key (a 33-byte compressed public key, 66 hex characters) is their user ID on your site. It is the same key every time they sign in with the same wallet.

## Three ways the user's wallet can answer

| Where the user is | How your page reaches the wallet | What you need |
|---|---|---|
| Chrome or Brave with the bWalletX extension | BRC-100 wallet discovery: dispatch `brc100:requestWallet`, take the `brc100:announceWallet` reply whose `info.rdns` is `com.bwalletx.extension` | Nothing extra. `findBwalletX()` below, or `https://bwalletx.com/connect.js` |
| Your site opened inside the bWalletX app's own browser | Same discovery; the app announces `rdns: space.bwallet.mobile` and also sets `window.CWI` | Nothing extra. `findBwalletX()` covers it |
| bWalletX on a phone, or the web wallet at web.bwalletx.com | Pairing: your page shows a `https://www.bwallet.space/pair?...` link as a QR code. The phone scans it; the web wallet takes it pasted. Both then talk to your page through `relay.bwallet.space`, end-to-end encrypted | `protocol.ts` from the bWalletX repo, plus `pairBwalletX()` below |

All three give you the same thing: an object with the BRC-100 `WalletInterface` methods. Sign-in is the same code for all of them.

## The button

<!-- preview -->

Use the gold button. Keep the label "Sign in with bWalletX". The logo is at `https://bwalletx.com/logo.svg` (the gold b, viewBox 74 x 100). Don't recolour it; it sits on a black circle so it reads on the gold.

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

## 1. Server: issue and verify challenges

Install `@bsv/sdk` (any 2.x or 3.x). This file has no other dependencies.

```ts
// bwalletx-server.ts: server side of "Sign in with bWalletX". Needs @bsv/sdk only.
import { ProtoWallet, PublicKey, type WalletProtocol } from '@bsv/sdk';
import { randomBytes } from 'node:crypto';

/** Security level 2, a protocol name used for nothing else. Keep it constant. */
export const LOGIN_PROTOCOL: WalletProtocol = [2, 'bwallet sign in'];
const LIFETIME_MS = 2 * 60 * 1000;

export interface PendingChallenge {
  identityKey: string;
  message: string;
  expiresAt: number;
}

/** Where challenges wait. Use Redis or a database table in production; take() must delete atomically. */
export interface ChallengeStore {
  put(nonce: string, c: PendingChallenge): Promise<void>;
  take(nonce: string): Promise<PendingChallenge | null>;
}

/** In-memory store: fine for one server process and for tests. */
export function memoryStore(): ChallengeStore {
  const m = new Map<string, PendingChallenge>();
  return {
    async put(nonce, c) { m.set(nonce, c); },
    async take(nonce) { const c = m.get(nonce) ?? null; m.delete(nonce); return c; },
  };
}

export function isIdentityKey(x: unknown): x is string {
  if (typeof x !== 'string' || !/^0[23][0-9a-fA-F]{64}$/.test(x)) return false;
  try { PublicKey.fromString(x); return true; } catch { return false; }
}

/** The text the user signs. It names your site so a signature made for you is useless elsewhere. */
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

/**
 * Step 1. `origin` is YOUR site's origin from config (e.g. "https://example.com"),
 * never taken from the request body.
 */
export async function createChallenge(store: ChallengeStore, origin: string, identityKey: unknown) {
  if (!isIdentityKey(identityKey)) throw new Error('identityKey must be a compressed public key (66 hex chars)');
  const nonce = randomBytes(16).toString('base64url');
  const expiresAt = Date.now() + LIFETIME_MS;
  const message = loginMessage(origin, nonce, expiresAt);
  await store.put(nonce, { identityKey: identityKey.toLowerCase(), message, expiresAt });
  return { nonce, message, protocolID: LOGIN_PROTOCOL, keyID: nonce };
}

/**
 * Step 2. Returns the proven identity key (lowercase hex), or null.
 * The nonce is deleted before checking, so each challenge can be tried once.
 */
export async function verifySignIn(
  store: ChallengeStore,
  body: { identityKey?: unknown; nonce?: unknown; signature?: unknown },
): Promise<string | null> {
  if (typeof body.nonce !== 'string' || !isIdentityKey(body.identityKey)) return null;
  const c = await store.take(body.nonce);
  if (!c || Date.now() > c.expiresAt) return null;
  const identityKey = body.identityKey.toLowerCase();
  if (c.identityKey !== identityKey) return null;

  const sig = body.signature;
  if (!Array.isArray(sig) || sig.length < 8 || sig.length > 80 || !sig.every((b) => Number.isInteger(b) && b >= 0 && b <= 255)) {
    return null;
  }
  try {
    const { valid } = await new ProtoWallet('anyone').verifySignature({
      protocolID: LOGIN_PROTOCOL,
      keyID: body.nonce,
      counterparty: identityKey,
      data: Array.from(Buffer.from(c.message, 'utf8')),
      signature: sig as number[],
    });
    return valid ? identityKey : null;
  } catch {
    return null; // @bsv/sdk throws on a bad signature instead of returning valid: false
  }
}
```

Two routes. This example uses Express; any framework works the same way.

```ts
// Example routes (Express). Any framework works the same way.
import express from 'express';
import { createChallenge, memoryStore, verifySignIn } from './bwalletx-server.js';

const ORIGIN = process.env.APP_ORIGIN ?? 'https://example.com'; // your site, exactly as the browser sends Origin
const store = memoryStore();
const app = express();
app.use(express.json());

// Only accept calls from your own pages.
app.use('/auth/bwalletx', (req, res, next) => {
  if (req.get('origin') !== ORIGIN) return res.status(403).json({ error: 'wrong origin' });
  next();
});

app.post('/auth/bwalletx/challenge', async (req, res) => {
  try {
    res.json(await createChallenge(store, ORIGIN, req.body?.identityKey));
  } catch (e) {
    res.status(400).json({ error: e instanceof Error ? e.message : 'bad request' });
  }
});

app.post('/auth/bwalletx/verify', async (req, res) => {
  const identityKey = await verifySignIn(store, req.body ?? {});
  if (!identityKey) return res.status(401).json({ error: 'That signature was not accepted. Start again.' });
  // identityKey is the user's stable id. Find or create the account keyed on it, then start your session.
  res.json({ ok: true, identityKey });
});

app.listen(3000);
```

## 2. Browser: find the wallet and sign in

```ts
// bwalletx-client.ts: browser side of "Sign in with bWalletX".
import type { WalletInterface, WalletProtocol } from '@bsv/sdk';

/** Ids bWalletX announces in BRC-100 wallet discovery: the Chrome extension, and the phone app's in-app browser. */
export const BWALLETX_RDNS = ['com.bwalletx.extension', 'space.bwallet.mobile'];

/**
 * Ask the page for bWalletX by name (BRC-100 discovery): the extension on a computer, or the
 * wallet itself when your site is open in bWalletX's in-app browser.
 * Resolves null if nothing answered within `ms` (not installed, or an ordinary phone browser).
 */
export function findBwalletX(ms = 1200): Promise<WalletInterface | null> {
  return new Promise((resolve) => {
    let done = false;
    const finish = (w: WalletInterface | null) => {
      if (done) return;
      done = true;
      window.removeEventListener('brc100:announceWallet', onAnnounce);
      resolve(w);
    };
    const onAnnounce = (e: Event) => {
      const d = (e as CustomEvent).detail as { info?: { rdns?: string }; wallet?: WalletInterface } | undefined;
      if (d?.wallet && BWALLETX_RDNS.includes(d.info?.rdns ?? '')) finish(d.wallet);
    };
    window.addEventListener('brc100:announceWallet', onAnnounce);
    window.dispatchEvent(new Event('brc100:requestWallet'));
    setTimeout(() => finish(null), ms);
  });
}

interface Challenge {
  nonce: string;
  message: string;
  protocolID: WalletProtocol;
  keyID: string;
}

async function postJson<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify(body),
  });
  const out = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((out as { error?: string }).error || `HTTP ${res.status}`);
  return out as T;
}

/**
 * Prove the wallet's identity key to your server. Works with any BRC-100 wallet object:
 * the extension or in-app browser (findBwalletX), a paired phone or web wallet (pairBwalletX), or
 * window.CWI inside the bWalletX in-app browser.
 */
export async function signInWithBwalletX<T = unknown>(wallet: WalletInterface, apiBase = '/auth/bwalletx'): Promise<T> {
  // Asks the user to unlock if needed. Older wallets and paired phones may not implement it.
  await wallet.waitForAuthentication({}).catch(() => {});
  const { publicKey: identityKey } = await wallet.getPublicKey({ identityKey: true });

  const c = await postJson<Challenge>(`${apiBase}/challenge`, { identityKey });

  // The wallet shows the user an approval prompt for this.
  const { signature } = await wallet.createSignature({
    protocolID: c.protocolID,
    keyID: c.keyID,
    counterparty: 'anyone',
    data: Array.from(new TextEncoder().encode(c.message)), // the server's exact text
  });

  return postJson<T>(`${apiBase}/verify`, { identityKey, nonce: c.nonce, signature });
}
```

## 3. Browser: pairing for phone and web wallet users

Copy `protocol.ts` from https://github.com/bitcoin-corp/bwallet/blob/main/src/pair/protocol.ts into your project, next to this file. It is the pairing protocol the bWalletX app speaks: ECDH on secp256k1, HKDF-SHA256, AES-256-GCM, and a 4-digit code both screens show. Don't change it; the app must understand every byte.

```ts
// bwalletx-pair.ts: pair with bWalletX on a phone (QR) or web.bwalletx.com (pasted link).
// Needs protocol.ts from https://github.com/bitcoin-corp/bwallet/blob/main/src/pair/protocol.ts
import { PrivateKey, type WalletInterface } from '@bsv/sdk';
import {
  DEFAULT_RELAY, PAIR_VERSION, QR_LIFETIME_S, Sealer, deriveSession, isSealed, newChannel, pairUrl, relaySocketUrl,
  type HelloFrame, type PairMessage,
} from './protocol';

export interface PairingOptions {
  /** Show this link as a QR code, and as text to copy (web.bwalletx.com takes it pasted). */
  onLink: (link: string) => void;
  /** Show this 4-digit code. The wallet shows the same one; the user checks they match. */
  onCode: (code: string) => void;
  signal?: AbortSignal;
}

/**
 * Resolves with a BRC-100 wallet once the user taps Connect in bWalletX.
 * Every method call is sent, end-to-end encrypted, through relay.bwallet.space to the wallet,
 * which asks the user to approve it. Keep the returned object while the page is open.
 */
export function pairBwalletX(opts: PairingOptions): Promise<WalletInterface> {
  const siteKey = PrivateKey.fromRandom(); // a throwaway pairing key, not a wallet key
  const channel = newChannel();
  const expiry = Math.floor(Date.now() / 1000) + QR_LIFETIME_S;
  const ws = new WebSocket(relaySocketUrl(DEFAULT_RELAY, channel, 'site', expiry));
  const waiting = new Map<string, { resolve: (v: unknown) => void; reject: (e: Error) => void }>();
  let sealer: Sealer | null = null;
  let paired = false;

  opts.onLink(pairUrl({ v: PAIR_VERSION, r: DEFAULT_RELAY, c: channel, k: siteKey.toPublicKey().toString(), o: location.origin, e: expiry }));

  const call = async (action: string, params: unknown) => {
    if (!sealer || ws.readyState !== WebSocket.OPEN) throw new Error('bWalletX is not connected');
    const id = `${action}-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    const result = new Promise<unknown>((resolve, reject) => {
      waiting.set(id, { resolve, reject });
      setTimeout(() => { if (waiting.delete(id)) reject(new Error('No answer from bWalletX')); }, 120_000);
    });
    ws.send(JSON.stringify(await sealer.seal({ t: 'req', id, action, params } satisfies PairMessage)));
    return result;
  };

  const wallet = new Proxy({} as WalletInterface, {
    get: (_t, method) => (typeof method !== 'string' || method === 'then' ? undefined : (params: unknown) => call(method, params ?? {})),
  });

  return new Promise<WalletInterface>((resolve, reject) => {
    const fail = (e: Error) => {
      for (const w of waiting.values()) w.reject(e);
      waiting.clear();
      if (!paired) reject(e);
      ws.close();
    };
    const timer = setTimeout(() => { if (!paired) fail(new Error('The pairing code expired. Show a new one.')); }, QR_LIFETIME_S * 1000);
    opts.signal?.addEventListener('abort', () => fail(new Error('cancelled')));
    ws.onerror = () => fail(new Error('Could not reach the bWalletX pairing service'));
    ws.onclose = () => fail(new Error('The connection to bWalletX closed'));
    // Handle frames one at a time, in order (the hello must be processed before the next frame).
    let queue = Promise.resolve();
    ws.onmessage = (ev) => { queue = queue.then(() => onFrame(String(ev.data))).catch(() => {}); };
    const onFrame = async (raw: string) => {
      let f: unknown;
      try { f = JSON.parse(raw); } catch { return; }
      if ((f as HelloFrame).t === 'hello' && !sealer) {
        const s = await deriveSession(siteKey, (f as HelloFrame).k, channel);
        sealer = new Sealer(s.key, 'site');
        opts.onCode(s.code);
        return;
      }
      if (!sealer || !isSealed(f)) return;
      const msg = await sealer.open(f);
      if (!msg) return;
      if (msg.t === 'ready') {
        paired = true;
        clearTimeout(timer);
        resolve(wallet);
      } else if (msg.t === 'res') {
        const w = waiting.get(msg.id);
        if (!w) return;
        waiting.delete(msg.id);
        if (msg.error) w.reject(new Error(msg.error.message));
        else w.resolve(msg.result);
      } else if (msg.t === 'close') {
        fail(new Error('bWalletX disconnected'));
      }
    };
  });
}
```

## 4. Wire up the button

Uses the `qrcode` package from npm to draw the QR code.

```ts
// button.ts: wire the gold button. Extension first; otherwise a QR / link for phone or web wallet.
import QRCode from 'qrcode';
import { findBwalletX, signInWithBwalletX } from './bwalletx-client';
import { pairBwalletX } from './bwalletx-pair';

const button = document.getElementById('bwx-signin') as HTMLButtonElement;
const panel = document.getElementById('bwx-pair') as HTMLDivElement; // empty <div> under the button

button.addEventListener('click', async () => {
  button.disabled = true;
  try {
    const wallet =
      (await findBwalletX()) ??
      (await pairBwalletX({
        onLink: async (link) => {
          panel.innerHTML = `<p>Scan with bWalletX on your phone, or paste this link into web.bwalletx.com:</p>
            <img alt="bWalletX pairing code" width="240" height="240" src="${await QRCode.toDataURL(link, { margin: 1, width: 240 })}">
            <input readonly style="width:100%" value="${link}">`;
        },
        onCode: (code) => {
          panel.insertAdjacentHTML('beforeend', `<p>Check bWalletX shows <b>${code}</b>, then tap Connect.</p>`);
        },
      }));
    const session = await signInWithBwalletX<{ identityKey: string }>(wallet);
    panel.textContent = `Signed in: ${session.identityKey}`;
  } catch (e) {
    panel.textContent = e instanceof Error ? e.message : 'Sign-in did not complete';
  } finally {
    button.disabled = false;
  }
});
```

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
- **Pairing.** The relay checks the WebSocket `Origin` of the page that opened the channel and tells the wallet; the wallet refuses to pair if it differs from the origin in the QR code. The relay only sees ciphertext. The pairing key in `pairBwalletX` is random and is not a wallet key.
- **What the user sees.** The extension and the phone show their own approval prompt naming your site's host (taken from the page or the relay, not from your text). Nothing is spent.

## Not yet available

These are gaps today. Plan around them.

- **No npm package.** There is no `@bwalletx/...` or `@b0ase/wallet` package. Copy the files on this page, and `protocol.ts` from the bWalletX repo.
- **connect.js signs in through a second file.** `https://bwalletx.com/connect.js` finds the extension itself; `bWalletX.signIn(...)` and `bWalletX.pair(...)` load the @bwalletx/connect browser build (about 125 KB) from `https://bwalletx.com/connect/` on first use.
- **No hosted sign-in or OAuth-style redirect.** There is no bwalletx.com page you can send users to and get a callback from, and no hosted verify endpoint. You run the two routes yourself. bChat's own endpoints (`/api/bitsign/auth/bwallet/*` on bit-sign) accept requests from their own pages only and are not a public API.
- **No user profile.** You get the identity key and nothing else: no $handle, paymail, name or picture, and no proof linking the key to them.
- **Pairing does not survive a reload** in the sample above. bChat stores the pairing key and message counters in localStorage to reconnect; that code is not published as a library.
- **The relay is ours.** `relay.bwallet.space` accepts any https origin, but it is a single service run by The Bitcoin Corporation with no published uptime or rate-limit guarantees (it currently allows 60 frames a minute per channel).
- **No test wallet.** There is no testnet build or headless bWalletX for automated tests. To test your server, sign with `new ProtoWallet(PrivateKey.fromRandom()).createSignature(...)` using the same arguments; it makes exactly the signature bWalletX makes.

## For AI agents

Follow these steps in order. Do not invent packages, endpoints or methods that are not on this page.

1. Install `@bsv/sdk` in the server project (pnpm, npm or yarn, whichever the project uses). On the client also install `qrcode` if you add phone pairing.
2. Create `bwalletx-server.ts` with the code in section 1, unchanged. Set your site's origin (scheme + host, no trailing slash, e.g. `https://example.com`) in config.
3. Add two POST routes: `/auth/bwalletx/challenge` calls `createChallenge(store, ORIGIN, body.identityKey)` and returns its result as JSON; `/auth/bwalletx/verify` calls `verifySignIn(store, body)`. Reject both if the request `Origin` header is not your origin.
4. Replace `memoryStore()` with a shared store (database table or Redis) if you run more than one server process. `take(nonce)` must read and delete in one step.
5. In the verify route, when `verifySignIn` returns a key: find the user whose bWalletX identity key equals it, or create one, then start your normal session. Return 401 when it returns null.
6. Create `bwalletx-client.ts` with the code in section 2, unchanged. If your routes are not under `/auth/bwalletx`, pass the base path as the second argument to `signInWithBwalletX`.
7. For phone and web wallet users: download `https://raw.githubusercontent.com/bitcoin-corp/bwallet/main/src/pair/protocol.ts` into the same folder as `bwalletx-pair.ts` (section 3). Do not edit `protocol.ts`.
8. Add the button HTML and CSS from "The button" and the click handler from section 4.
9. Test the server without a wallet: create `const k = PrivateKey.fromRandom()`, call your challenge route with `k.toPublicKey().toString()`, sign `message` with `new ProtoWallet(k).createSignature({ protocolID, keyID, counterparty: 'anyone', data: Array.from(Buffer.from(message, 'utf8')) })`, post `{ identityKey, nonce, signature }` to verify and expect success. Post the same body again and expect 401.
10. Test by hand: with the bWalletX extension in Chrome, click the button and approve. Without it, scan the QR with bWalletX on a phone, check the 4-digit codes match, tap Connect, approve.

Questions: support@bwalletx.com

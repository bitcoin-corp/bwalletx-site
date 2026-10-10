/* bAvatars: a picture drawn from a Bitcoin name. Same name, same picture, in any app.
   Shared by /bavatars, the 404 page and the share-image template. Canvas only, no network.
   The QR styles need qrcode-generator 1.4.4 (window.qrcode) loaded first.
   API: bAvatars.draw(ctx, size, styleId, name), bAvatars.STYLES, bAvatars.clean(text),
        drawQR, drawCombo, drawArtQR, drawRing, readRing, seedFrom. */
(function () {
  const GOLD = ['#e9b52a', '#f2c230', '#ffd24d', '#d9a21a', '#c58b12', '#f6dc8a'];

  // Seeded randomness from the name (cyrb128 → sfc32)
  function seedFrom(str) {
    let h1 = 1779033703, h2 = 3144134277, h3 = 1013904242, h4 = 2773480762;
    for (let i = 0, k; i < str.length; i++) {
      k = str.charCodeAt(i);
      h1 = h2 ^ Math.imul(h1 ^ k, 597399067); h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
      h3 = h4 ^ Math.imul(h3 ^ k, 951274213); h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
    }
    h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067); h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
    h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213); h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
    let a = (h1 ^ h2 ^ h3 ^ h4) >>> 0, b = (h2 ^ h1) >>> 0, c = (h3 ^ h1) >>> 0, d = (h4 ^ h1) >>> 0;
    return function () {
      a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0;
      let t = (a + b) | 0; a = b ^ (b >>> 9); b = (c + (c << 3)) | 0; c = (c << 21) | (c >>> 11);
      d = (d + 1) | 0; t = (t + d) | 0; c = (c + t) | 0; return (t >>> 0) / 4294967296;
    };
  }
  const pick = (r, arr) => arr[Math.floor(r() * arr.length)];

  function ground(ctx, S, r) {
    const g = ctx.createRadialGradient(S * .35, S * .3, S * .05, S * .5, S * .5, S * .75);
    g.addColorStop(0, '#1d1a13'); g.addColorStop(1, '#070605');
    ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
  }
  function bMark(ctx, cx, cy, s, fill, bg) {
    // the b mark: a stem and a bowl
    ctx.save(); ctx.fillStyle = fill;
    const w = s * .18;
    roundRect(ctx, cx - s * .32, cy - s * .55, w, s * 1.05, w / 2); ctx.fill();
    ctx.beginPath(); ctx.arc(cx + s * .04, cy + s * .14, s * .36, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = bg; ctx.beginPath(); ctx.arc(cx + s * .04, cy + s * .14, s * .18, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  const STYLES = [
    { id: 'kintsugi', name: 'Kintsugi', tag: 'Signature', note: 'Black glaze with gold seams. Each name breaks along its own lines.',
      draw(ctx, S, r) {
        ground(ctx, S, r);
        ctx.lineCap = 'round';
        const cracks = 3 + Math.floor(r() * 3);
        for (let c = 0; c < cracks; c++) {
          let x = r() * S, y = r() < .5 ? 0 : S, ang = Math.atan2(S / 2 - y, S / 2 - x) + (r() - .5);
          ctx.beginPath(); ctx.moveTo(x, y);
          for (let i = 0; i < 9; i++) { ang += (r() - .5) * 1.1; x += Math.cos(ang) * S * .12; y += Math.sin(ang) * S * .12; ctx.lineTo(x, y); }
          ctx.strokeStyle = pick(r, GOLD); ctx.lineWidth = S * (.012 + r() * .02); ctx.shadowColor = '#f2c23088'; ctx.shadowBlur = S * .03; ctx.stroke();
        }
        ctx.shadowBlur = 0;
      } },
    { id: 'orbit', name: 'Orbit', tag: 'Calm', note: 'Concentric gold rings with gaps placed by the name.',
      draw(ctx, S, r) {
        ground(ctx, S, r);
        const n = 4 + Math.floor(r() * 3);
        for (let i = 0; i < n; i++) {
          const rad = S * (.12 + i * .075), start = r() * Math.PI * 2, len = Math.PI * (.6 + r() * 1.3);
          ctx.beginPath(); ctx.arc(S / 2, S / 2, rad, start, start + len);
          ctx.strokeStyle = i % 2 ? '#f2c230' : '#c58b12'; ctx.lineWidth = S * .035; ctx.lineCap = 'round'; ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(S / 2, S / 2, S * .06, 0, Math.PI * 2); ctx.fillStyle = '#ffd24d'; ctx.fill();
      } },
    { id: 'sigil', name: 'Sigil', tag: 'Classic', note: 'A mirrored 5×5 pattern, like a wax seal. Reads well at 24px.',
      draw(ctx, S, r) {
        ctx.fillStyle = '#e9b52a'; ctx.fillRect(0, 0, S, S);
        const cells = 5, pad = S * .2, c = (S - pad * 2) / cells;
        ctx.fillStyle = '#0b0a08';
        for (let y = 0; y < cells; y++) for (let x = 0; x < 3; x++) if (r() > .5) {
          ctx.fillRect(pad + x * c, pad + y * c, c + .5, c + .5);
          ctx.fillRect(pad + (cells - 1 - x) * c, pad + y * c, c + .5, c + .5);
        }
      } },
    { id: 'deco', name: 'Deco Fan', tag: 'Lounge', note: 'Art-deco fans and arches, after the Lounge banner set.',
      draw(ctx, S, r) {
        ground(ctx, S, r);
        const fans = 2 + Math.floor(r() * 2), base = S * (1.03 + r() * .06);
        for (let f = 0; f < fans; f++) {
          const cx = S * (.25 + f * (.5 / Math.max(1, fans - 1))) , rays = 7 + Math.floor(r() * 6), R = S * (.55 + r() * .25);
          for (let i = 0; i <= rays; i++) {
            const a = Math.PI + (Math.PI * i) / rays;
            ctx.beginPath(); ctx.moveTo(cx, base); ctx.lineTo(cx + Math.cos(a) * R, base + Math.sin(a) * R);
            ctx.strokeStyle = '#d9a21a'; ctx.lineWidth = S * .008; ctx.stroke();
          }
          ctx.beginPath(); ctx.arc(cx, base, R, Math.PI, 0); ctx.strokeStyle = '#f2c230'; ctx.lineWidth = S * .016; ctx.stroke();
        }
      } },
    { id: 'monogram', name: 'Monogram', tag: 'Personal', note: 'The first letter of the name, set in a gold coin.',
      draw(ctx, S, r, name) {
        const g = ctx.createLinearGradient(0, 0, S, S); g.addColorStop(0, '#f2c230'); g.addColorStop(1, '#c58b12');
        ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
        ctx.beginPath(); ctx.arc(S / 2, S / 2, S * .42, 0, Math.PI * 2); ctx.strokeStyle = '#0b0a0855'; ctx.lineWidth = S * .012; ctx.stroke();
        const teeth = 60; for (let i = 0; i < teeth; i++) { const a = i / teeth * Math.PI * 2; ctx.beginPath();
          ctx.moveTo(S / 2 + Math.cos(a) * S * .45, S / 2 + Math.sin(a) * S * .45); ctx.lineTo(S / 2 + Math.cos(a) * S * .49, S / 2 + Math.sin(a) * S * .49);
          ctx.strokeStyle = '#0b0a0840'; ctx.lineWidth = S * .008; ctx.stroke(); }
        ctx.fillStyle = '#0b0a08'; ctx.font = `800 ${S * .5}px Fraunces, Georgia, serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText((name[0] || 'b').toUpperCase(), S / 2, S * .53);
      } },
    { id: 'bloom', name: 'Bloom', tag: 'Soft', note: 'Overlapping gold light, like candles through glass.',
      draw(ctx, S, r) {
        ctx.fillStyle = '#0b0a08'; ctx.fillRect(0, 0, S, S); ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 6; i++) {
          const x = S * (.2 + r() * .6), y = S * (.2 + r() * .6), R = S * (.18 + r() * .3), g = ctx.createRadialGradient(x, y, 0, x, y, R);
          g.addColorStop(0, pick(r, GOLD) + 'cc'); g.addColorStop(1, '#00000000'); ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
        }
        ctx.globalCompositeOperation = 'source-over';
      } },
    { id: 'mark', name: 'b Mark', tag: 'Brand', note: 'The b mark on black, with a ring coloured by the name. For official accounts.',
      draw(ctx, S, r) {
        ground(ctx, S, r);
        ctx.beginPath(); ctx.arc(S / 2, S / 2, S * .44, 0, Math.PI * 2); ctx.strokeStyle = pick(r, GOLD); ctx.lineWidth = S * .04; ctx.stroke();
        bMark(ctx, S / 2, S / 2 - S * .02, S * .42, '#f2c230', '#0f0d0a');
      } },
  ];

  function qrModules(text) {
    const q = qrcode(0, 'H'); q.addData(text); q.make(); return q;
  }
  function drawQR(ctx, S, name, opts) {
    const url = 'https://www.bchatx.com/u/' + encodeURIComponent(name);
    const q = qrModules(url), n = q.getModuleCount();
    const quiet = opts.quiet ?? 2, cell = S / (n + quiet * 2), off = quiet * cell;
    ctx.fillStyle = '#0b0a08'; ctx.fillRect(0, 0, S, S);
    const finder = (x, y) => (x < 7 && y < 7) || (x >= n - 7 && y < 7) || (x < 7 && y >= n - 7);
    const holeR = n * .14, c = n / 2;
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      if (!q.isDark(y, x) || finder(x, y)) continue;
      if (Math.hypot(x + .5 - c, y + .5 - c) < holeR) continue;
      ctx.beginPath(); ctx.arc(off + (x + .5) * cell, off + (y + .5) * cell, cell * .44, 0, Math.PI * 2);
      ctx.fillStyle = '#f2c230'; ctx.fill();
    }
    for (const [fx, fy] of [[0, 0], [n - 7, 0], [0, n - 7]]) {
      const x = off + fx * cell, y = off + fy * cell;
      ctx.fillStyle = '#f2c230'; roundRect(ctx, x, y, cell * 7, cell * 7, cell * 2); ctx.fill();
      ctx.fillStyle = '#0b0a08'; roundRect(ctx, x + cell, y + cell, cell * 5, cell * 5, cell * 1.4); ctx.fill();
      ctx.fillStyle = '#ffd24d'; roundRect(ctx, x + cell * 2, y + cell * 2, cell * 3, cell * 3, cell); ctx.fill();
    }
    bMark(ctx, S / 2, S / 2 - cell * .3, cell * holeR * 1.15, '#ffd24d', '#0b0a08');
    return url;
  }
  STYLES.push({ id: 'qr', name: 'QR Coin', tag: 'Scannable', alt: true, note: 'A working QR code. Full size below; scan it with a phone.',
    draw(ctx, S, r, name) { drawQR(ctx, S, name, { quiet: 4 }); } });

  // ── Combined avatar: Bloom + Deco Fan + Kintsugi ──
  function drawCombo(ctx, S, name, x0 = 0, y0 = 0) {
    ctx.save(); ctx.translate(x0, y0);
    const byId = id => STYLES.find(s => s.id === id);
    byId('bloom').draw(ctx, S, seedFrom('bloom:' + name));
    ctx.globalAlpha = .85; drawFans(ctx, S, seedFrom('deco:' + name)); ctx.globalAlpha = 1;
    drawCracks(ctx, S, seedFrom('kintsugi:' + name));
    ctx.restore();
  }
  function drawFans(ctx, S, r) {
    const fans = 2 + Math.floor(r() * 2), base = S * (1.03 + r() * .06);
    for (let f = 0; f < fans; f++) {
      const cx = S * (.25 + f * (.5 / Math.max(1, fans - 1))), rays = 7 + Math.floor(r() * 6), R = S * (.52 + r() * .25);
      for (let i = 0; i <= rays; i++) { const a = Math.PI + (Math.PI * i) / rays; ctx.beginPath(); ctx.moveTo(cx, base);
        ctx.lineTo(cx + Math.cos(a) * R, base + Math.sin(a) * R); ctx.strokeStyle = '#f6dc8a'; ctx.lineWidth = S * .006; ctx.stroke(); }
      ctx.beginPath(); ctx.arc(cx, base, R, Math.PI, 0); ctx.strokeStyle = '#ffd24d'; ctx.lineWidth = S * .014; ctx.stroke();
    }
  }
  function drawCracks(ctx, S, r) {
    ctx.lineCap = 'round'; const cracks = 2 + Math.floor(r() * 3);
    for (let c = 0; c < cracks; c++) {
      let x = r() * S, y = r() < .5 ? 0 : S, ang = Math.atan2(S / 2 - y, S / 2 - x) + (r() - .5);
      ctx.beginPath(); ctx.moveTo(x, y);
      for (let i = 0; i < 9; i++) { ang += (r() - .5) * 1.1; x += Math.cos(ang) * S * .12; y += Math.sin(ang) * S * .12; ctx.lineTo(x, y); }
      ctx.strokeStyle = '#ffe08a'; ctx.lineWidth = S * (.01 + r() * .014); ctx.shadowColor = '#f2c230aa'; ctx.shadowBlur = S * .025; ctx.stroke();
    }
    ctx.shadowBlur = 0;
  }

  // ── Art QR: standard polarity (dark spots on light), art visible between module centres ──
  function drawArtQR(ctx, S, name) {
    const url = 'https://www.bchatx.com/u/' + encodeURIComponent(name);
    const q = qrModules(url), n = q.getModuleCount(), quiet = 3, cell = S / (n + quiet * 2), off = quiet * cell;
    ctx.fillStyle = '#fff3cf'; ctx.fillRect(0, 0, S, S);                       // pale gold quiet zone
    drawCombo(ctx, n * cell, name, off, off);                                   // art fills the code area
    ctx.fillStyle = 'rgba(255,243,207,.18)'; ctx.fillRect(off, off, n * cell, n * cell);
    const finder = (x, y) => (x < 8 && y < 8) || (x >= n - 8 && y < 8) || (x < 8 && y >= n - 8);
    const dot = cell * .62, inset = (cell - dot) / 2;
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      if (finder(x, y)) continue;
      ctx.fillStyle = q.isDark(y, x) ? '#0b0a08' : '#fff3cf';
      roundRect(ctx, off + x * cell + inset, off + y * cell + inset, dot, dot, dot * .3); ctx.fill();
    }
    for (const [fx, fy] of [[0, 0], [n - 7, 0], [0, n - 7]]) {           // finder medallions, solid for reliable scanning
      const x = off + fx * cell, y = off + fy * cell;
      ctx.fillStyle = '#fff3cf'; ctx.fillRect(x - cell, y - cell, cell * 9, cell * 9);
      ctx.fillStyle = '#0b0a08'; roundRect(ctx, x, y, cell * 7, cell * 7, cell * 1.6); ctx.fill();
      ctx.fillStyle = '#fff3cf'; roundRect(ctx, x + cell, y + cell, cell * 5, cell * 5, cell * 1.1); ctx.fill();
      ctx.fillStyle = '#0b0a08'; roundRect(ctx, x + cell * 2, y + cell * 2, cell * 3, cell * 3, cell * .8); ctx.fill();
      ctx.strokeStyle = '#d9a21a'; ctx.lineWidth = cell * .25; roundRect(ctx, x + cell * 2.4, y + cell * 2.4, cell * 2.2, cell * 2.2, cell * .5); ctx.stroke();
    }
    return url;
  }

  // ── Code ring: name → bits → 3 tracks × 48 cells around the avatar ──
  const ALPHA = 'abcdefghijklmnopqrstuvwxyz0123456789-._';
  const TRACKS = 3, CELLS = 48, MAXLEN = 20;
  function crc16(bits) { let c = 0xffff; for (const b of bits) { const top = ((c >> 15) & 1) ^ b; c = (c << 1) & 0xffff; if (top) c ^= 0x1021; } return c; }
  function encodeName(name) {
    const s = name.slice(0, MAXLEN), bits = [];
    const push = (v, w) => { for (let i = w - 1; i >= 0; i--) bits.push((v >> i) & 1); };
    push(s.length, 5); for (const ch of s) push(Math.max(0, ALPHA.indexOf(ch)), 6);
    const c = crc16(bits); push(c, 16);
    while (bits.length < TRACKS * CELLS) bits.push(0);
    return bits;
  }
  function decodeBits(bits) {
    const read = (i, w) => { let v = 0; for (let k = 0; k < w; k++) v = (v << 1) | bits[i + k]; return v; };
    const len = read(0, 5); if (len > MAXLEN) return null;
    let s = ''; for (let i = 0; i < len; i++) s += ALPHA[read(5 + i * 6, 6)] ?? '?';
    const body = bits.slice(0, 5 + len * 6), crc = read(5 + len * 6, 16);
    return crc16(body) === crc ? s : null;
  }
  const ringGeom = S => ({ inner: S * .335, step: S * .045, gapA: (Math.PI * 2) / CELLS });
  function drawRing(ctx, S, name) {
    ctx.fillStyle = '#0b0a08'; ctx.fillRect(0, 0, S, S);
    ctx.save(); ctx.beginPath(); ctx.arc(S / 2, S / 2, S * .31, 0, Math.PI * 2); ctx.clip();
    drawCombo(ctx, S * .62, name, S * .19, S * .19); ctx.restore();
    const { inner, step, gapA } = ringGeom(S), bits = encodeName(name);
    ctx.lineCap = 'butt';
    for (let t = 0; t < TRACKS; t++) {
      const rad = inner + step * (t + .5);
      ctx.beginPath(); ctx.arc(S / 2, S / 2, rad, 0, Math.PI * 2); ctx.strokeStyle = '#1e1a12'; ctx.lineWidth = step * .7; ctx.stroke();
      for (let i = 0; i < CELLS; i++) if (bits[t * CELLS + i]) {
        const a0 = -Math.PI / 2 + i * gapA + gapA * .12, a1 = a0 + gapA * .76;
        ctx.beginPath(); ctx.arc(S / 2, S / 2, rad, a0, a1); ctx.strokeStyle = t === 1 ? '#ffd24d' : '#e9b52a'; ctx.lineWidth = step * .7; ctx.stroke();
      }
    }
    // orientation mark at 12 o'clock, outside the tracks
    ctx.beginPath(); ctx.arc(S / 2, S / 2 - (inner + step * TRACKS + step * .7), step * .35, 0, Math.PI * 2); ctx.fillStyle = '#ffd24d'; ctx.fill();
  }
  function readRing(ctx, S) {   // what the scanner does: sample each cell's centre and threshold it
    const { inner, step, gapA } = ringGeom(S), img = ctx.getImageData(0, 0, S, S).data, bits = [];
    for (let t = 0; t < TRACKS; t++) for (let i = 0; i < CELLS; i++) {
      const a = -Math.PI / 2 + i * gapA + gapA / 2, rad = inner + step * (t + .5);
      const x = Math.round(S / 2 + Math.cos(a) * rad), y = Math.round(S / 2 + Math.sin(a) * rad), p = (y * S + x) * 4;
      bits.push((img[p] + img[p + 1] + img[p + 2]) / 3 > 110 ? 1 : 0);
    }
    return decodeBits(bits);
  }

  const clean = v => String(v).toLowerCase().replace(/^\$/, '').replace(/@.*$/, '').replace(/[^a-z0-9._-]/g, '').slice(0, 40) || 'b';
  function draw(ctx, S, id, name) {
    const st = STYLES.find(s => s.id === id) || STYLES[0];
    ctx.clearRect(0, 0, S, S); st.draw(ctx, S, seedFrom(st.id + ':' + name), name);
  }
  window.bAvatars = { STYLES, seedFrom, clean, draw, drawQR, drawCombo, drawArtQR, drawRing, readRing, MAXLEN };
})();

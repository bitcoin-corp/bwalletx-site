/*
 * bBot: the Bubble set (approved by RB, 4 Nov 2026). Five shapes, fourteen colours, six moods.
 * Bubble and Gold are the defaults. The geometry, colours and motion are the approved reference
 * (bbot-bubble.html) unchanged; only the class names carry a "bbot-" prefix so they never clash
 * with a page's own CSS. Motion lives in bbot.css and stops under prefers-reduced-motion.
 *
 *   <span data-bbot data-shape="bubble" data-colour="gold" data-mood="idle" data-size="48"></span>
 *   BBot.svg('bubble', 'gold', 'idle', { size: 48, label: 'bBot' })
 *
 * The same drawing lives in the wallet (src/mobile/agents/BBot.tsx) and in bChatX
 * (src/components/bbot/BBot.tsx). Masters: brand/bbot/*.svg.
 */
(function (root) {
  'use strict';

  var PAL = [
    ['Gold', { main: '#F5B800', dark: '#8A6400', mid: '#C99400', light: '#FFE27A', ink: '#0F1013' }],
    ['Amber', { main: '#F59E0B', dark: '#92400E', mid: '#C27C0E', light: '#FCD9A0', ink: '#0F1013' }],
    ['Coral', { main: '#FF7A59', dark: '#B23A1E', mid: '#D9583A', light: '#FFC9B8', ink: '#0F1013' }],
    ['Rose', { main: '#FF5C8A', dark: '#A3184A', mid: '#D63A6A', light: '#FFC2D4', ink: '#0F1013' }],
    ['Magenta', { main: '#E44CE0', dark: '#8A1C87', mid: '#B734B3', light: '#F6C2F4', ink: '#0F1013' }],
    ['Iris', { main: '#8B7CFF', dark: '#4B3BC4', mid: '#6A5AE0', light: '#D4CDFF', ink: '#0F1013' }],
    ['Azure', { main: '#3D8BFF', dark: '#1D4FB8', mid: '#2C6BDB', light: '#B9D6FF', ink: '#0F1013' }],
    ['Sky', { main: '#38C6F4', dark: '#0B6E95', mid: '#1E9DCB', light: '#B8ECFC', ink: '#0F1013' }],
    ['Teal', { main: '#14B8A6', dark: '#0B6B61', mid: '#0F9184', light: '#A7EDE4', ink: '#0F1013' }],
    ['Mint', { main: '#2FD58E', dark: '#0E7A4C', mid: '#1FA86E', light: '#B6F5D8', ink: '#0F1013' }],
    ['Lime', { main: '#A8E03A', dark: '#56800E', mid: '#7FB022', light: '#E0F7B0', ink: '#0F1013' }],
    ['Steel', { main: '#AEB6C2', dark: '#59626F', mid: '#858E9B', light: '#E8ECF1', ink: '#0F1013' }],
    ['Obsidian', { main: '#23252B', dark: '#F5B800', mid: '#1A1B20', light: '#F5B800', ink: '#F5B800' }],
    ['Pearl', { main: '#F4F1E8', dark: '#8F8A7C', mid: '#D6D1C3', light: '#FFFFFF', ink: '#0F1013' }],
  ];

  var STATES = [
    ['idle', 'Idle', 'Ready, waiting for a job'],
    ['working', 'Working', 'On a job right now'],
    ['typing', 'Typing', 'Writing to you'],
    ['done', 'Done', 'Job finished'],
    ['attention', 'Needs you', 'Waiting for your OK'],
    ['sleep', 'Asleep', 'Paused until its next run'],
  ];

  var P = 'bbot-';
  var solid = function (c) {
    return c.ink === '#F5B800' ? '#0F1013' : c.ink;
  };

  // Each shape: body (everything but the eyes) + where its eyes sit.
  var SHAPES = {
    bubble: {
      name: 'Bubble',
      body: function (c) {
        return (
          '<rect x="30.8" y="3" width="2.4" height="7" rx="1.2" fill="' + c.dark + '"/>' +
          '<circle class="' + P + 'tip" cx="32" cy="3.6" r="2.8" fill="' + c.light + '" stroke="' + c.dark + '" stroke-width="1.5"/>' +
          '<path d="M22 9 H42 A14 14 0 0 1 56 23 V32 A14 14 0 0 1 42 46 H30 L17 57 L20 45.2 A14 14 0 0 1 8 32 V23 A14 14 0 0 1 22 9 Z" fill="' + c.main + '" stroke="' + c.dark + '" stroke-width="2.5" stroke-linejoin="round"/>'
        );
      },
      eyes: { at: [[23.5, 25.5], [40.5, 25.5]], w: 8, h: 13, col: 'ink', hl: true },
    },
    coin: {
      name: 'Coin',
      body: function (c) {
        return (
          '<circle cx="32" cy="32" r="27" fill="' + c.main + '" stroke="' + c.dark + '" stroke-width="2.5"/>' +
          '<circle cx="32" cy="32" r="22.5" fill="none" stroke="' + c.dark + '" stroke-width="2.2" stroke-dasharray="1.6 2.4" opacity=".55"/>' +
          '<path d="M14 24 A19 19 0 0 1 26 13.5" stroke="#fff" stroke-opacity=".45" stroke-width="2.5" fill="none" stroke-linecap="round"/>' +
          '<rect x="15" y="25" width="34" height="14" rx="7" fill="' + solid(c) + '"/>' +
          '<path d="M27 45.5 Q32 48.5 37 45.5" stroke="' + c.dark + '" stroke-width="2" fill="none" stroke-linecap="round"/>'
        );
      },
      eyes: { at: [[25, 32], [39, 32]], w: 7, h: 7, rx: 2.6, col: 'light' },
    },
    block: {
      name: 'Block',
      body: function (c) {
        return (
          '<line x1="32" y1="10" x2="32" y2="5" stroke="' + c.dark + '" stroke-width="2" stroke-linecap="round"/>' +
          '<circle class="' + P + 'tip" cx="32" cy="3.8" r="2.6" fill="' + c.light + '" stroke="' + c.dark + '" stroke-width="1.5"/>' +
          '<polygon points="32,10 54,21 32,32 10,21" fill="' + c.light + '" stroke="' + c.dark + '" stroke-width="2" stroke-linejoin="round"/>' +
          '<polygon points="10,21 32,32 32,57 10,46" fill="' + c.main + '" stroke="' + c.dark + '" stroke-width="2" stroke-linejoin="round"/>' +
          '<polygon points="32,32 54,21 54,46 32,57" fill="' + c.mid + '" stroke="' + c.dark + '" stroke-width="2" stroke-linejoin="round"/>' +
          '<polygon points="13,29.5 29,37.5 29,47 13,39" fill="' + solid(c) + '"/>' +
          '<circle class="' + P + 'led1" cx="40" cy="38" r="1.7" fill="' + c.light + '"/><circle class="' + P + 'led2" cx="46" cy="35" r="1.7" fill="' + c.light + '"/>'
        );
      },
      // drawn flat, then sheared onto the cube's left face
      eyes: { at: [[18.25, 27.4], [24.25, 27.4]], w: 4.5, h: 4.75, rx: 1, col: 'light', skew: 'matrix(1 .5 0 1 0 0)' },
    },
    orbit: {
      name: 'Orbit',
      body: function (c) {
        return (
          '<g transform="rotate(-16 32 36)"><ellipse cx="32" cy="36" rx="29" ry="7.5" fill="none" stroke="' + c.dark + '" stroke-width="2.5"/></g>' +
          '<circle cx="32" cy="31" r="19" fill="' + c.main + '" stroke="' + c.dark + '" stroke-width="2.5"/>' +
          '<ellipse cx="24.5" cy="21.5" rx="5" ry="2.6" fill="#fff" fill-opacity=".45" transform="rotate(-35 24.5 21.5)"/>' +
          '<rect x="19" y="24.5" width="26" height="11" rx="5.5" fill="' + solid(c) + '"/>' +
          '<g transform="rotate(-16 32 36)"><path d="M3 36 A29 7.5 0 0 0 61 36" fill="none" stroke="' + c.dark + '" stroke-width="2.5"/></g>'
        );
      },
      eyes: { at: [[27, 30], [37, 30]], w: 5.4, h: 5.4, col: 'light' },
    },
    tag: {
      name: 'Tag',
      body: function (c) {
        return (
          '<path d="M13.5 29.5 C 8 26, 5 20, 7 13" stroke="' + c.dark + '" stroke-width="1.8" fill="none" stroke-linecap="round"/>' +
          '<path d="M21 12 H52 A6 6 0 0 1 58 18 V46 A6 6 0 0 1 52 52 H21 L7 32 Z" fill="' + c.main + '" stroke="' + c.dark + '" stroke-width="2.5" stroke-linejoin="round"/>' +
          '<circle cx="17" cy="32" r="3.6" fill="' + solid(c) + '" stroke="' + c.dark + '" stroke-width="1.2"/>' +
          '<path d="M33 43 Q38.5 46.5 44 43" stroke="' + c.dark + '" stroke-width="2" fill="none" stroke-linecap="round"/>'
        );
      },
      eyes: { at: [[32.5, 31], [45.5, 31]], w: 7, h: 12, col: 'ink' },
    },
  };

  // Compact (16-24px): the same drawing without the eye glints, with a 3.2 outline on the main shape.
  var compactBody = function (svg) {
    return svg.replace(/stroke-width="2\.5"/g, 'stroke-width="3.2"');
  };

  function eyes(spec, c, state, compact) {
    var col = spec.col === 'ink' ? c.ink : c.light;
    var sw = Math.max(1.6, Math.min(spec.w, spec.h) * 0.32);
    var rx = spec.rx != null ? spec.rx : Math.min(spec.w, spec.h) / 2;
    var hl = spec.hl && !compact;
    var shapes = function () {
      return spec.at
        .map(function (p) {
          var x = p[0], y = p[1];
          return (
            '<rect x="' + (x - spec.w / 2) + '" y="' + (y - spec.h / 2) + '" width="' + spec.w + '" height="' + spec.h + '" rx="' + rx + '" fill="' + col + '"/>' +
            (hl ? '<circle cx="' + (x + 1.1) + '" cy="' + (y - 2.5) + '" r="1.5" fill="#fff" fill-opacity=".9"/>' : '')
          );
        })
        .join('');
    };
    var inner;
    if (state === 'working') inner = '<g class="' + P + 'look">' + shapes() + '</g>';
    else if (state === 'typing') {
      var x0 = spec.at[0][0], y = spec.at[0][1], x1 = spec.at[1][0];
      var r = Math.max(1.3, Math.min(spec.w, spec.h) * 0.32);
      inner = [x0, (x0 + x1) / 2, x1]
        .map(function (x, i) {
          return '<circle class="' + P + 'dot ' + P + 'd' + (i + 1) + '" cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + col + '"/>';
        })
        .join('');
    } else if (state === 'done') {
      inner = spec.at
        .map(function (p) {
          var x = p[0], y = p[1];
          return '<path d="M' + (x - spec.w / 2 + 0.4) + ' ' + (y + spec.h * 0.14) + ' Q' + x + ' ' + (y - spec.h * 0.46) + ' ' + (x + spec.w / 2 - 0.4) + ' ' + (y + spec.h * 0.14) + '" stroke="' + col + '" stroke-width="' + sw + '" fill="none" stroke-linecap="round"/>';
        })
        .join('');
    } else if (state === 'sleep') {
      inner = spec.at
        .map(function (p) {
          var x = p[0], y = p[1];
          return '<path d="M' + (x - spec.w / 2 + 0.4) + ' ' + (y + spec.h * 0.05) + ' Q' + x + ' ' + (y + spec.h * 0.32) + ' ' + (x + spec.w / 2 - 0.4) + ' ' + (y + spec.h * 0.05) + '" stroke="' + col + '" stroke-width="' + sw + '" fill="none" stroke-linecap="round"/>';
        })
        .join('');
    } else inner = '<g class="' + P + 'blink">' + shapes() + '</g>';
    return '<g' + (spec.skew ? ' transform="' + spec.skew + '"' : '') + '>' + inner + '</g>';
  }

  var keyOf = function (list, k, fallback) {
    var want = String(k == null ? '' : k).toLowerCase();
    for (var i = 0; i < list.length; i++) if (list[i][0].toLowerCase() === want) return list[i];
    return fallback;
  };
  /** A colour by name ('gold') or main hex ('#F5B800'); anything else is Gold. */
  function colourOf(k) {
    var want = String(k == null ? '' : k).toLowerCase();
    for (var i = 0; i < PAL.length; i++) {
      if (PAL[i][0].toLowerCase() === want || PAL[i][1].main.toLowerCase() === want) return PAL[i];
    }
    return PAL[0];
  }
  var shapeOf = function (k) {
    return SHAPES[String(k || '').toLowerCase()] ? String(k).toLowerCase() : 'bubble';
  };
  var moodOf = function (k) {
    return keyOf(STATES, k, STATES[0])[0];
  };

  /** The inner drawing (no <svg>), for a 0 0 64 64 viewBox. */
  function inner(shape, colour, mood, opts) {
    opts = opts || {};
    var s = SHAPES[shapeOf(shape)];
    var c = colourOf(colour)[1];
    var st = moodOf(mood);
    var body = opts.compact ? compactBody(s.body(c)) : s.body(c);
    var zz =
      st === 'sleep'
        ? '<text class="' + P + 'zz" x="50" y="13" font-size="10" font-weight="800" fill="' + c.dark + '" font-family="Inter, system-ui, sans-serif">z</text>' +
          '<text class="' + P + 'zz ' + P + 'zz2" x="55" y="9" font-size="7" font-weight="800" fill="' + c.dark + '" font-family="Inter, system-ui, sans-serif">z</text>'
        : '';
    return '<g class="' + P + 'body">' + body + eyes(s.eyes, c, st, opts.compact) + '</g>' + zz;
  }

  /** A whole <svg>. opts: size, label (aria-label; omit for a decorative bBot), compact, className. */
  function svg(shape, colour, mood, opts) {
    opts = opts || {};
    var st = moodOf(mood);
    var size = opts.size ? ' width="' + opts.size + '" height="' + opts.size + '"' : '';
    var a11y = opts.label ? ' role="img" aria-label="' + String(opts.label).replace(/[<>&"]/g, '') + '"' : ' aria-hidden="true"';
    var cls = 'bbot ' + P + 'st-' + st + (opts.className ? ' ' + opts.className : '');
    return '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" class="' + cls + '"' + size + a11y + '>' + inner(shape, colour, mood, opts) + '</svg>';
  }

  /** Fill every [data-bbot] element; staggers idle blinks so a page never blinks in unison. */
  function render(scope) {
    var els = (scope || document).querySelectorAll('[data-bbot]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      el.innerHTML = svg(el.getAttribute('data-shape'), el.getAttribute('data-colour'), el.getAttribute('data-mood'), {
        size: +el.getAttribute('data-size') || 28,
        label: el.getAttribute('data-label') || '',
        compact: el.hasAttribute('data-compact'),
      });
    }
    var blinks = (scope || document).querySelectorAll('.' + P + 'blink');
    for (var j = 0; j < blinks.length; j++) blinks[j].style.animationDelay = ((j * 0.83) % 5.5).toFixed(2) + 's';
    var bodies = (scope || document).querySelectorAll('.' + P + 'st-idle .' + P + 'body');
    for (var k = 0; k < bodies.length; k++) bodies[k].style.animationDelay = ((k * 0.41) % 3.2).toFixed(2) + 's';
  }

  var api = { PAL: PAL, STATES: STATES, SHAPES: SHAPES, colourOf: colourOf, inner: inner, svg: svg, render: render };
  root.BBot = api;
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { render(); });
    else render();
  }
})(typeof window !== 'undefined' ? window : globalThis);

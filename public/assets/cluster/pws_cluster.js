/*!
 * PeeWeeSys — 986 / 996 instrument cluster renderer, v2
 * renderClusterSvg(state) -> complete <svg> string.
 * UMD: CommonJS, AMD, or browser global (window.PWSCluster, window.renderClusterSvg).
 *
 * Angles: degrees, 0 = needle pointing up, positive = clockwise. Each needle is drawn
 * pointing up with its pivot on its own hub and rotated with transform="rotate(a hx hy)".
 * Fuel/coolant and volt/oil have their own hubs, as on the real cluster; volt and oil
 * pivot behind the neighbouring pod, exactly like the 996.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) define([], factory);
  else if (typeof module === 'object' && module.exports) module.exports = factory();
  else { var api = factory(); root.PWSCluster = api; root.renderClusterSvg = api.renderClusterSvg; }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ============================================================== layout */
  var LAYOUTS = {
    3: { w: 680, h: 320, pods: {
      speedo: { cx: 178, cy: 152, r: 92 },
      tach:   { cx: 340, cy: 144, r: 110 },
      combo:  { cx: 502, cy: 152, r: 92 } } },
    5: { w: 880, h: 320, pods: {
      volt:   { cx: 150, cy: 166, r: 50 },
      speedo: { cx: 264, cy: 152, r: 90 },
      tach:   { cx: 440, cy: 144, r: 108 },
      combo:  { cx: 616, cy: 152, r: 90 },
      oil:    { cx: 730, cy: 166, r: 50 } } }
  };
  /* Hub offsets and needle lengths as fractions of the pod radius. */
  /* radius of the 996 end-pod housing (matches the main dials' curvature); its outer edge lines up with the end-pod scale */
  var END_HOUSING_R = 84, END_HOUSING_INSET = 9;   /* inset pulls the housing in behind its neighbour */
  var HUBS = {
    tach:    { dx: 0, dy: 0, len: .80 },
    speedo:  { dx: 0, dy: 0, len: .76 },
    coolant: { dx: -.10, dy: -.30, len: .50 },
    fuel:    { dx: .14, dy: .16, len: .58 },
    volt:    { dx: .86, dy: .02, len: 1.12 },
    oil:     { dx: -.86, dy: .02, len: 1.12 }
  };
  var SWEEP = {
    tach:    { from: -102, to: 102, min: 0, max: 8000 },
    speedo:  { from: -140, to: 42, min: 0 },                 /* max comes from the scale */
    coolC:   { from: -44, to: 44, min: 40, max: 120 },
    coolF:   { from: -44, to: 44, min: 100, max: 250 },
    fuel:    { from: 134, to: 58, min: 0, max: 100 },
    volt:    { from: -146, to: -48, min: 8, max: 16 },
    oil:     { from: 146, to: 48, min: 0, max: 5 }
  };
  var SCALES = {
    '160_mph': { id: '160_mph', max: 160, unit: 'MPH',  major: 25, minor: 5,  labels: [25, 50, 75, 100, 125, 150] },
    '180_mph': { id: '180_mph', max: 180, unit: 'MPH',  major: 25, minor: 5,  labels: [25, 50, 75, 100, 125, 150, 175] },
    '200_mph': { id: '200_mph', max: 200, unit: 'MPH',  major: 25, minor: 5,  labels: [25, 50, 75, 100, 125, 150, 175, 200] },
    '250_kmh': { id: '250_kmh', max: 260, unit: 'km/h', major: 50, minor: 10, labels: [50, 100, 150, 200, 250] },
    '300_kmh': { id: '300_kmh', max: 310, unit: 'km/h', major: 50, minor: 10, labels: [50, 100, 150, 200, 250, 300] }
  };
  /* Display generations: 'early' = 996.1 / early 986 segment LCDs (odometer left, speed centre),
     'k21' = 986 c.2001 segment LCDs (speed left, odometer centre), 'k24' = 986.2 / 996.2 dot-matrix centre. */
  var DISPLAYS = ['early', 'k21', 'k24'];

  var COL = {
    needle: '#FF4425', needleDeep: '#C9260F', needleHi: '#FF8A6E',
    face:   { black: ['#22262C', '#16191E', '#0C0E11'], white: ['#F6F7F8', '#ECEEF0', '#D6DADE'] },
    ink:    { black: '#F1F3F5', white: '#121418' },
    sub:    { black: '#8C949E', white: '#5B626B' },
    red:    { black: '#FF3B30', white: '#D8141E' },
    lens:   { black: '#2E3238', white: '#8A9097' },
    amber:  '#FFAC2E', amberGlow: '#FF8A00', amberGhost: '#3A2406', lcdBg: '#0B0704', lcdBgOff: '#0D1014',
    green: '#22C55E', warnAmber: '#F59E0B', warnRed: '#EF4444'
  };

  /* ============================================================== helpers */
  var counter = 0;
  function f(n) { return (Math.round(n * 100) / 100).toString(); }
  function pt(cx, cy, r, a) { var t = a * Math.PI / 180; return [cx + r * Math.sin(t), cy - r * Math.cos(t)]; }
  function lerp(sw, v) { var c = Math.max(sw.min, Math.min(sw.max, v)); return sw.from + (sw.to - sw.from) * (c - sw.min) / (sw.max - sw.min); }
  function arc(cx, cy, r, a1, a2) {
    var lo = Math.min(a1, a2), hi = Math.max(a1, a2), p1 = pt(cx, cy, r, lo), p2 = pt(cx, cy, r, hi);
    return 'M' + f(p1[0]) + ' ' + f(p1[1]) + 'A' + f(r) + ' ' + f(r) + ' 0 ' + (hi - lo > 180 ? 1 : 0) + ' 1 ' + f(p2[0]) + ' ' + f(p2[1]);
  }
  function line(cx, cy, r1, r2, a, stroke, w, cap) {
    var p1 = pt(cx, cy, r1, a), p2 = pt(cx, cy, r2, a);
    return '<line x1="' + f(p1[0]) + '" y1="' + f(p1[1]) + '" x2="' + f(p2[0]) + '" y2="' + f(p2[1]) + '" stroke="' + stroke + '" stroke-width="' + f(w) + '"' + (cap ? ' stroke-linecap="' + cap + '"' : '') + '/>';
  }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var SANS = "'Barlow Semi Condensed', 'Barlow', 'Arial Narrow', sans-serif", MONO = "'JetBrains Mono', ui-monospace, monospace";
  function text(x, y, s, size, fill, o) {
    o = o || {};
    return '<text x="' + f(x) + '" y="' + f(y) + '" font-size="' + f(size) + '" fill="' + fill + '" text-anchor="' + (o.anchor || 'middle') +
      '" dominant-baseline="central" font-family="' + (o.font || (o.mono ? MONO : SANS)) + '" font-weight="' + (o.weight || 500) + '"' +
      (o.italic ? ' font-style="italic"' : '') + (o.spacing ? ' letter-spacing="' + o.spacing + '"' : '') + '>' + esc(s) + '</text>';
  }
  /* numeral typography: 'italic' = 986 / Boxster S style, 'upright' = traditional 996 style */
  var UPRIGHT = "'Barlow', 'Helvetica Neue', Helvetica, Arial, sans-serif";
  function numFont(st, extra) {
    var it = st.numerals === 'italic';
    var o = it ? { weight: 500, italic: true } : { weight: 600, font: UPRIGHT };
    for (var k in (extra || {})) o[k] = extra[k];
    return o;
  }
  function hubOf(pod, key) { var h = HUBS[key]; return { x: pod.cx + h.dx * pod.r, y: pod.cy + h.dy * pod.r, len: h.len * pod.r }; }

  /* ============================================================== 5x7 dot-matrix font */
  var G = {
    '0':'01110100011000110001100011000101110','1':'00100011000010000100001000010001110','2':'01110100010000100010001000100011111',
    '3':'11111000100010000010000011000101110','4':'00010001100101010010111110001000010','5':'11111100001111000001000011000101110',
    '6':'00110010001000011110100011000101110','7':'11111000010001000100010000100001000','8':'01110100011000101110100011000101110',
    '9':'01110100011000101111000010001001100',
    'A':'01110100011000111111100011000110001','B':'11110100011000111110100011000111110','C':'01110100011000010000100001000101110',
    'D':'11100100101000110001100011001011100','E':'11111100001000011110100001000011111','F':'11111100001000011110100001000010000',
    'G':'01110100011000010111100011000101111','H':'10001100011000111111100011000110001','I':'01110001000010000100001000010001110',
    'J':'00111000100001000010000101001001100','K':'10001100101010011000101001001010001','L':'10000100001000010000100001000011111',
    'M':'10001110111010110101100011000110001','N':'10001100011100110101100111000110001','O':'01110100011000110001100011000101110',
    'P':'11110100011000111110100001000010000','Q':'01110100011000110001101011001001101','R':'11110100011000111110101001001010001',
    'S':'01111100001000001110000010000111110','T':'11111001000010000100001000010000100','U':'10001100011000110001100011000101110',
    'V':'10001100011000110001100010101000100','W':'10001100011000110101101011010101010','X':'10001100010101000100010101000110001',
    'Y':'10001100011000101010001000010000100','Z':'11111000010001000100010001000011111',
    'a':'00000000000111000001011111000101111','c':'00000000000111010000100001000101110','d':'00001000010110110011100011000101111',
    'e':'00000000000111010001111111000001110','g':'00000011111000110001011110000101110','h':'10000100001011011001100011000110001',
    'i':'00100000000110000100001000010001110','k':'10000100001001010100110001010010010','l':'01100001000010000100001000010001110',
    'm':'00000000001101010101101011000110001','n':'00000000001011011001100011000110001','o':'00000000000111010001100011000101110',
    'p':'00000000001111010001111101000010000','r':'00000000001011011001100001000010000','s':'00000000000111010000011100000111110',
    't':'01000010001110001000010000100100110','u':'00000000001000110001100011001101101',
    ' ':'00000000000000000000000000000000000','.':'00000000000000000000000000110001100','-':'00000000000000011111000000000000000',
    ':':'00000011000110000000011000110000000','/':'00000000010001000100010001000000000','+':'00000001000010011111001000010000000',
    '°':'01100100101001001100000000000000000','Ø':'01101100101010110101101011001010110','>':'01000001000001000001000100010001000',
    '→':'00000001000001011111000100010000000','▽':'00000111111000101010010100010000000','⛽':'11100101011110111101111011111011100'
  };
  /* returns {d, w}: d = path of lit dots (rects), w = width in pitches */
  function dmText(x, y, s, p, dot, invert) {
    var d = '', col = 0, ds = f(dot);
    for (var i = 0; i < s.length; i++) {
      var g = G[s[i]] || G[s[i].toUpperCase()] || G[' '], sh = NARROW[s[i]] ? -1 : 0;
      for (var r = 0; r < 7; r++) for (var c = 0; c < 5; c++) {
        var on = g[r * 5 + c] === '1'; if (invert) on = !on;
        if (on) d += 'M' + f(x + (col + c + sh) * p) + ' ' + f(y + r * p) + 'h' + ds + 'v' + ds + 'h-' + ds + 'z';
      }
      if (invert && i < s.length - 1) for (var r2 = 0; r2 < 7; r2++) d += 'M' + f(x + (col + 5) * p) + ' ' + f(y + r2 * p) + 'h' + ds + 'v' + ds + 'h-' + ds + 'z';
      col += NARROW[s[i]] ? 3 : 6;
    }
    return { d: d, w: col - 1 };
  }
  var NARROW = { ':': 1, '.': 1 };
  function dmWidth(s) { var w = 0; for (var i = 0; i < s.length; i++) w += NARROW[s[i]] ? 3 : 6; return w - 1; }

  /* ============================================================== 7-segment LCD */
  var SEG = { '0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg', '-': 'g', ' ': '' };
  function segDigit(x, y, h, ch, t) {
    var w = h * .52, th = t || h * .13, g = th * .18, hh = h / 2, P = {};
    function hseg(yy) { return 'M' + f(x + g + th / 2) + ' ' + f(yy) + 'l' + f(th / 2) + ' ' + f(-th / 2) + 'h' + f(w - 2 * g - 2 * th) + 'l' + f(th / 2) + ' ' + f(th / 2) + 'l' + f(-th / 2) + ' ' + f(th / 2) + 'h' + f(-(w - 2 * g - 2 * th)) + 'z'; }
    function vseg(xx, y0) { return 'M' + f(xx) + ' ' + f(y0 + g + th / 2) + 'l' + f(th / 2) + ' ' + f(th / 2) + 'v' + f(hh - 2 * g - 2 * th) + 'l' + f(-th / 2) + ' ' + f(th / 2) + 'l' + f(-th / 2) + ' ' + f(-th / 2) + 'v' + f(-(hh - 2 * g - 2 * th)) + 'z'; }
    P.a = hseg(y + th / 2); P.g = hseg(y + hh); P.d = hseg(y + h - th / 2);
    P.f = vseg(x + th / 2, y); P.b = vseg(x + w - th / 2, y); P.e = vseg(x + th / 2, y + hh); P.c = vseg(x + w - th / 2, y + hh);
    var on = '', all = '';
    'abcdefg'.split('').forEach(function (k) { all += P[k]; if ((SEG[ch] || '').indexOf(k) >= 0) on += P[k]; });
    return { on: on, all: all, w: w };
  }
  /* 7-seg string; ':' and '.' are narrow */
  function segText(x, y, h, s, align) {
    var gap = h * .14, w = h * .52, total = 0, i;
    for (i = 0; i < s.length; i++) total += (s[i] === ':' || s[i] === '.') ? h * .2 : w + gap;
    var cx = align === 'right' ? x - total : align === 'center' ? x - total / 2 : x, on = '', ghost = '';
    for (i = 0; i < s.length; i++) {
      var ch = s[i];
      if (ch === ':') { var r = h * .065; on += circlePath(cx + h * .08, y + h * .3, r) + circlePath(cx + h * .08, y + h * .7, r); cx += h * .2; continue; }
      if (ch === '.') { on += circlePath(cx + h * .05, y + h * .93, h * .065); cx += h * .2; continue; }
      var dg = segDigit(cx, y, h, ch); on += dg.on; ghost += dg.all; cx += w + gap;
    }
    return { on: on, ghost: ghost, w: total };
  }
  function circlePath(x, y, r) { return 'M' + f(x - r) + ' ' + f(y) + 'a' + f(r) + ' ' + f(r) + ' 0 1 0 ' + f(2 * r) + ' 0a' + f(r) + ' ' + f(r) + ' 0 1 0 ' + f(-2 * r) + ' 0z'; }

  /* ============================================================== defs */
  function defs(P, theme, bezel) {
    var fc = COL.face[theme], b = bezel === 'chrome'
      ? ['#FAFBFC', '#C7CDD4', '#7D8691', '#3B424B', '#20252B']
      : ['#5A6068', '#2A2E34', '#16191D', '#0B0C0E', '#050607'];
    return '<defs>' +
      '<linearGradient id="' + P + 'bezel" x1="0" y1="0" x2=".7" y2="1"><stop offset="0" stop-color="' + b[0] + '"/><stop offset=".25" stop-color="' + b[1] + '"/><stop offset=".55" stop-color="' + b[2] + '"/><stop offset=".8" stop-color="' + b[3] + '"/><stop offset="1" stop-color="' + b[4] + '"/></linearGradient>' +
      '<linearGradient id="' + P + 'bezelIn" x1="0" y1="1" x2=".35" y2="0"><stop offset="0" stop-color="#050607"/><stop offset=".7" stop-color="' + (bezel === 'chrome' ? '#4A525C' : '#1C1F24') + '"/><stop offset="1" stop-color="' + (bezel === 'chrome' ? '#AEB6BF' : '#3A3F46') + '"/></linearGradient>' +
      '<radialGradient id="' + P + 'face" cx=".44" cy=".36" r=".74"><stop offset="0" stop-color="' + fc[0] + '"/><stop offset=".6" stop-color="' + fc[1] + '"/><stop offset="1" stop-color="' + fc[2] + '"/></radialGradient>' +
      '<radialGradient id="' + P + 'vig" cx=".5" cy=".5" r=".5"><stop offset=".8" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="' + (theme === 'white' ? .2 : .55) + '"/></radialGradient>' +
      '<linearGradient id="' + P + 'housing" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22272E"/><stop offset=".2" stop-color="#14181D"/><stop offset="1" stop-color="#090B0E"/></linearGradient>' +
      '<linearGradient id="' + P + 'lip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#454D58"/><stop offset="1" stop-color="#11151A"/></linearGradient>' +
      '<linearGradient id="' + P + 'strip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16191D"/><stop offset=".7" stop-color="#0E1013"/><stop offset="1" stop-color="#1E2227"/></linearGradient>' +
      '<radialGradient id="' + P + 'hub" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="#3C434D"/><stop offset=".6" stop-color="#1A1E24"/><stop offset="1" stop-color="#08090B"/></radialGradient>' +
      '<linearGradient id="' + P + 'needle" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="' + COL.needleDeep + '"/><stop offset=".42" stop-color="' + COL.needleHi + '"/><stop offset=".58" stop-color="' + COL.needle + '"/><stop offset="1" stop-color="' + COL.needleDeep + '"/></linearGradient>' +
      '<linearGradient id="' + P + 'glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity="1"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></linearGradient>' +
      '<linearGradient id="' + P + 'knob" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0A0B0D"/><stop offset=".35" stop-color="#3A4048"/><stop offset=".55" stop-color="#22262C"/><stop offset="1" stop-color="#08090B"/></linearGradient>' +
      '<radialGradient id="' + P + 'knobTop" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#4A515B"/><stop offset="1" stop-color="#15181C"/></radialGradient>' +
      '<filter id="' + P + 'pod" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dy="4"/><feComponentTransfer><feFuncA type="linear" slope=".8"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
      '<filter id="' + P + 'nglow" x="-100%" y="-20%" width="300%" height="140%"><feGaussianBlur stdDeviation="1.3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
      '<filter id="' + P + 'lglow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation=".55" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
      '<filter id="' + P + 'tglow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
      '<filter id="' + P + 'soft" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>' +
    '</defs>';
  }

  /* ============================================================== pod pieces */
  function podFrame(P, pod, id) {
    var cx = pod.cx, cy = pod.cy, r = pod.r, k = r / 100;
    return '<g id="bezel-' + id + '">' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + f(r + 12 * k) + '" fill="#040506"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + f(r + 10 * k) + '" fill="url(#' + P + 'bezel)"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + f(r + 9.4 * k) + '" fill="none" stroke="#FFF" stroke-opacity=".18" stroke-width=".8"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + f(r + 4.4 * k) + '" fill="url(#' + P + 'bezelIn)"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + f(r + 1.2 * k) + '" fill="#030405"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="url(#' + P + 'face)"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="url(#' + P + 'vig)"/></g>';
  }
  function glass(P, pod) {
    var cx = pod.cx, cy = pod.cy, r = pod.r, a = pt(cx, cy, r * .94, -64), b = pt(cx, cy, r * .94, 36), c = pt(cx, cy, r * .5, -12);
    return '<path d="M' + f(a[0]) + ' ' + f(a[1]) + 'A' + f(r * .94) + ' ' + f(r * .94) + ' 0 0 1 ' + f(b[0]) + ' ' + f(b[1]) + 'Q' + f(c[0]) + ' ' + f(c[1]) + ' ' + f(a[0]) + ' ' + f(a[1]) + 'Z" fill="url(#' + P + 'glass)" opacity=".07" pointer-events="none"/>';
  }
  function needle(P, hx, hy, L, angle, id, w, hubR, noHub) {
    var tail = L * .2;
    var d = 'M' + f(hx - .5) + ' ' + f(hy - L) + 'L' + f(hx + .5) + ' ' + f(hy - L) + 'L' + f(hx + w) + ' ' + f(hy - L * .1) +
      'Q' + f(hx + w * 1.4) + ' ' + f(hy + tail * .5) + ' ' + f(hx + w * 1.2) + ' ' + f(hy + tail) + 'L' + f(hx - w * 1.2) + ' ' + f(hy + tail) +
      'Q' + f(hx - w * 1.4) + ' ' + f(hy + tail * .5) + ' ' + f(hx - w) + ' ' + f(hy - L * .1) + 'Z';
    var o = '<g id="needle-' + id + '" class="pws-needle" data-cx="' + f(hx) + '" data-cy="' + f(hy) + '" transform="rotate(' + f(angle) + ' ' + f(hx) + ' ' + f(hy) + ')">' +
      '<path d="' + d + '" fill="#000" opacity=".4" transform="translate(1.3 2)"/><path d="' + d + '" fill="url(#' + P + 'needle)" filter="url(#' + P + 'nglow)"/></g>';
    if (!noHub) o += '<g id="hub-' + id + '"><circle cx="' + f(hx) + '" cy="' + f(hy) + '" r="' + f(hubR) + '" fill="url(#' + P + 'hub)" stroke="#000" stroke-opacity=".7" stroke-width=".8"/>' +
      '<circle cx="' + f(hx - hubR * .22) + '" cy="' + f(hy - hubR * .25) + '" r="' + f(hubR * .45) + '" fill="#FFF" opacity=".05"/></g>';
    return o;
  }
  function seg(P, x, y, w, h, opts) {
    /* LCD window: rounded black recess with amber segments and optional small labels */
    opts = opts || {};
    var o = '<rect x="' + f(x - 1.4) + '" y="' + f(y - 1.4) + '" width="' + f(w + 2.8) + '" height="' + f(h + 2.8) + '" rx="' + f(h * .18 + 1) + '" fill="#020203"/>' +
      '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + f(h * .16) + '" fill="' + COL.lcdBg + '"/>';
    var ghost = '', on = '', labels = '';
    (opts.rows || []).forEach(function (row) {
      var st = segText(row.x, row.y, row.h, row.s, row.align || 'right');
      ghost += st.ghost; on += st.on;
    });
    (opts.labels || []).forEach(function (L) { labels += text(L.x, L.y, L.s, L.size, COL.amber, { mono: false, weight: 600, anchor: L.anchor || 'start' }); });
    var skew = 'transform="translate(' + f(x + w / 2) + ' ' + f(y + h / 2) + ') skewX(-7) translate(' + f(-(x + w / 2)) + ' ' + f(-(y + h / 2)) + ')"';
    o += '<path d="' + ghost + '" fill="' + COL.amberGhost + '" opacity=".4" ' + skew + '/>';
    o += '<g filter="url(#' + P + 'lglow)"><path d="' + on + '" fill="' + COL.amber + '" ' + skew + '/>' + labels + '</g>';
    o += '<rect x="' + f(x + 1) + '" y="' + f(y + 1) + '" width="' + f(w - 2) + '" height="' + f(h * .4) + '" rx="' + f(h * .14) + '" fill="#FFF" opacity=".04"/>';
    return o;
  }

  /* small dot-matrix window (K24 speed and clock): recess, unlit pixel field, lit dots */
  function dmWin(P, id, x, y, w, h, parts) {
    var pitch = h / 10.5, dot = pitch * .8, gx = x + pitch * .6, gy = y + (h - 7 * pitch) / 2 - pitch * 1.2;
    var o = '<rect x="' + f(x - 1.4) + '" y="' + f(y - 1.4) + '" width="' + f(w + 2.8) + '" height="' + f(h + 2.8) + '" rx="' + f(h * .18 + 1) + '" fill="#020203"/>' +
      '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + f(h * .16) + '" fill="' + COL.lcdBg + '"/>' +
      '<pattern id="' + P + id + 'px" x="' + f(gx) + '" y="' + f(gy) + '" width="' + f(pitch * .5) + '" height="' + f(pitch * .5) + '" patternUnits="userSpaceOnUse"><rect width="' + f(dot * .5) + '" height="' + f(dot * .5) + '" fill="' + COL.amberGhost + '"/></pattern>' +
      '<rect x="' + f(x + 2) + '" y="' + f(y + 2) + '" width="' + f(w - 4) + '" height="' + f(h - 4) + '" fill="url(#' + P + id + 'px)" opacity=".28"/>';
    var lit = '';
    parts.forEach(function (pp) {
      var p = pitch * (pp.scale || 1), d = p * .8, tw = dmWidth(pp.s) * p;
      var px = pp.align === 'right' ? pp.x - tw : pp.align === 'center' ? pp.x - tw / 2 : pp.x;
      var py = pp.y != null ? pp.y : y + (h - 7 * p) / 2;
      lit += dmText(px, py, pp.s, p, d).d;
      if (pp.dots) pp.dots.forEach(function (q) { lit += 'M' + f(q[0]) + ' ' + f(q[1]) + 'h' + f(d * 1.6) + 'v' + f(d * 1.6) + 'h-' + f(d * 1.6) + 'z'; });
    });
    o += '<path d="' + lit + '" fill="' + COL.amber + '" filter="url(#' + P + 'lglow)"/>';
    o += '<rect x="' + f(x + 1) + '" y="' + f(y + 1) + '" width="' + f(w - 2) + '" height="' + f(h * .4) + '" rx="' + f(h * .14) + '" fill="#FFF" opacity=".04"/>';
    return o;
  }
  /* 24h "HH:MM" -> {s, pm} for the chosen format */
  function clockParts(st) {
    var m = /^(\d{1,2}):(\d{2})/.exec(st.clock || '14:25'), hh = m ? +m[1] : 14, mm = m ? m[2] : '25';
    if (st.clockFormat !== '12') return { s: (hh < 10 ? '0' : '') + hh + ':' + mm, ampm: null };
    var pm = hh >= 12, h12 = hh % 12 === 0 ? 12 : hh % 12;
    return { s: h12 + ':' + mm, ampm: pm ? 'pm' : 'am' };
  }

  /* ============================================================== dials */
  function tachFace(P, pod, theme, st) {
    var cx = pod.cx, cy = pod.cy, R = pod.r, ink = COL.ink[theme], sub = COL.sub[theme], red = COL.red[theme], sw = SWEEP.tach, o = '';
    var rl = st.redlineRpm || 7200, ital = st.numerals === 'italic';
    for (var v = 0; v <= 8000; v += 250) {
      var a = lerp(sw, v), maj = v % 1000 === 0, half = v % 500 === 0;
      if (maj) o += line(cx, cy, R * .79, R * .93, a, ink, R * .03);
      else o += line(cx, cy, R * (half ? .855 : .875), R * .93, a, sub, R * (half ? .017 : .011));
    }
    for (var w = rl; w <= 8000; w += 200) { var q = pt(cx, cy, R * .965, lerp(sw, w)); o += '<circle cx="' + f(q[0]) + '" cy="' + f(q[1]) + '" r="' + f(R * .02) + '" fill="' + red + '"/>'; }
    for (var n = 1; n <= 7; n++) {
      var p = pt(cx, cy, R * .63, lerp(sw, n * 1000));
      o += text(p[0], p[1], n, R * (ital ? .2 : .19), ink, numFont(st));
    }
    var g = pt(cx, cy, R * .5, 100);
    o += '<circle cx="' + f(g[0]) + '" cy="' + f(g[1]) + '" r="' + f(R * .045) + '" fill="' + COL.lens[theme] + '"/>';
    var lbl = st.tachLabel != null ? st.tachLabel : 'RPM';
    if (lbl) o += text(cx, cy + R * .17, lbl, R * .075, sub, { weight: 600, spacing: '.06em' });
    return o;
  }
  function tachWindowPath(pod) {
    var cx = pod.cx, cy = pod.cy, R = pod.r, top = cy + R * .27, sx = R * .72, rr = R * .93, rc = R * .06;
    var yb = cy + Math.sqrt(rr * rr - sx * sx);
    return 'M' + f(cx - sx) + ' ' + f(yb) + 'L' + f(cx - sx) + ' ' + f(top + rc) + 'Q' + f(cx - sx) + ' ' + f(top) + ' ' + f(cx - sx + rc) + ' ' + f(top) +
      'L' + f(cx + sx - rc) + ' ' + f(top) + 'Q' + f(cx + sx) + ' ' + f(top) + ' ' + f(cx + sx) + ' ' + f(top + rc) + 'L' + f(cx + sx) + ' ' + f(yb) +
      'A' + f(rr) + ' ' + f(rr) + ' 0 0 1 ' + f(cx - sx) + ' ' + f(yb) + 'Z';
  }
  function tachDisplay(P, pod, st) {
    var cx = pod.cx, cy = pod.cy, R = pod.r, path = tachWindowPath(pod), top = cy + R * .27, o = '', mode = st.display, km = st.unitKm;
    o += '<path d="' + path + '" fill="#020203" transform="translate(0 0)" stroke="#020203" stroke-width="' + f(R * .05) + '" stroke-linejoin="round"/>';
    o += '<path d="' + path + '" fill="' + COL.lcdBg + '"/>';
    o += '<clipPath id="' + P + 'twin"><path d="' + path + '"/></clipPath>';
    var inner = '';
    if (mode === 'k24') {
      var pitch = R * .0108, dot = pitch * .8, x0 = cx - R * .68, y0 = top + R * .045;
      /* unlit pixel field */
      inner += '<pattern id="' + P + 'px" x="' + f(x0) + '" y="' + f(y0) + '" width="' + f(pitch) + '" height="' + f(pitch) + '" patternUnits="userSpaceOnUse"><rect width="' + f(dot) + '" height="' + f(dot) + '" fill="' + COL.amberGhost + '"/></pattern>';
      inner += '<rect x="' + f(cx - R * .74) + '" y="' + f(top) + '" width="' + f(R * 1.48) + '" height="' + f(R * .75) + '" fill="url(#' + P + 'px)" opacity=".2"/>';
      var lit = '', obc = st.obcOn;
      if (obc) {
        var menu = st.obcMenu || ['LIMIT', 'CHECK', 'OIL', 'BC'], act = st.obcActive != null ? st.obcActive : 0, colW = 31, rx = x0 + colW * pitch;
        for (var i = 0; i < menu.length; i++) {
          var s = menu[i], tw = dmWidth(s), xx = rx - tw * pitch, yy = y0 + i * 8 * pitch;
          if (i === act) { /* inverted, padded block */
            for (var pr = -1; pr <= 7; pr++) for (var pc = -2; pc < tw + 1; pc++) {
              if (pr >= 0 && pr < 7 && pc >= 0 && pc < tw) continue;
              lit += 'M' + f(xx + pc * pitch) + ' ' + f(yy + pr * pitch) + 'h' + f(dot) + 'v' + f(dot) + 'h-' + f(dot) + 'z';
            }
            lit += dmText(xx, yy, s, pitch, dot, true).d;
          } else lit += dmText(xx, yy, s, pitch, dot).d;
        }
        lit += dmText(rx - 5 * pitch, y0 + menu.length * 8 * pitch, '▽', pitch, dot).d;
        /* divider */
        for (var dv = -1; dv < 40; dv++) lit += 'M' + f(rx + 3 * pitch) + ' ' + f(y0 + dv * pitch) + 'h' + f(dot) + 'v' + f(dot) + 'h-' + f(dot) + 'z';
        var lines = st.obcLines || [st.odometer + (km ? ' km' : ' mls'), st.trip + (km ? ' km' : ' mls')];
        var dx0 = rx + 7 * pitch;
        lit += dmText(dx0 + 2 * pitch, y0 + 1 * pitch, lines[0], pitch, dot).d;
        lit += dmText(dx0 + 2 * pitch, y0 + 10 * pitch, lines[1], pitch, dot).d;
        var big = st.obcBig || (st.ambient + (st.tempUnit === 'F' ? ' °F' : ' °C')), avail = (cx + R * .62) - (dx0 + 2 * pitch);
        var bp = Math.min(pitch * 2, avail / dmWidth(big)), bd = bp * .8;
        lit += dmText(dx0 + 2 * pitch, y0 + 21 * pitch, big, bp, bd).d;
      } else {
        var l1 = st.odometer + (km ? ' km' : ' mls'), l2 = st.trip + (km ? ' km' : ' mls'), bp2 = pitch * 1.55, bd2 = bp2 * .82;
        lit += dmText(cx - dmWidth(l1) * bp2 / 2, y0 + 4 * pitch, l1, bp2, bd2).d;
        lit += dmText(cx - dmWidth(l2) * bp2 / 2, y0 + 17 * pitch, l2, bp2, bd2).d;
      }
      inner += '<path d="' + lit + '" fill="' + COL.amber + '" filter="url(#' + P + 'lglow)"/>';
    } else {
      /* segment LCDs */
      var h1 = R * .2, h2 = R * .12, yA = top + R * .1, yB = top + R * .36, rxr = cx + R * .32, ghost = '', on = '', lab = '';
      function add(st2) { ghost += st2.ghost; on += st2.on; }
      var tU = '°' + (st.tempUnit === 'F' ? 'F' : 'C');
      if (mode === 'early') {
        /* digital speed always; outside temperature only with the OBC coded */
        var ySp = st.obcOn ? yA : top + R * .2;
        add(segText(rxr, ySp, h1, String(st.digitalSpeed), 'right'));
        lab += text(cx - R * .5, ySp + h1 * .55, km ? 'km/h' : 'MPH', R * .075, COL.amber, { weight: 600, anchor: 'start' });
        if (st.obcOn) {
          var t = String(st.ambient), sign = t[0] === '-' ? '-' : '+'; t = t.replace('-', '');
          lab += text(cx - R * .2, yB + h2 * .55, sign, R * .09, COL.amber, { weight: 600 });
          add(segText(rxr - R * .02, yB, h2, t, 'right'));
          lab += text(rxr + R * .02, yB + h2 * .45, tU, R * .075, COL.amber, { weight: 600, anchor: 'start' });
        }
      } else { /* k21: small odometer + trip on top; the lower field is the OBC, only when coded */
        var hs = R * .085, xr = cx + R * .26, y1 = top + R * .06, y2 = y1 + hs + R * .05;
        add(segText(xr, y1, hs, st.odometerDigits, 'right'));
        lab += text(xr + R * .03, y1 + hs * .6, km ? 'km' : 'MI', R * .06, COL.amber, { weight: 600, anchor: 'start' });
        add(segText(xr, y2, hs, st.tripDigits, 'right'));
        lab += text(xr + R * .03, y2 + hs * .6, km ? 'km' : 'MI', R * .06, COL.amber, { weight: 600, anchor: 'start' });
        if (st.obcOn) {
          var mode21 = st.obcMode || 'temp', yO = y2 + hs + R * .07, ho = R * .13, val, unit, tag = '';
          if (mode21 === 'mpg') { val = st.obcMpg || (km ? '9.6' : '28.4'); unit = km ? 'l/100' : 'MPG'; }
          else if (mode21 === 'range') { val = st.obcRange || (km ? '395' : '245'); unit = km ? 'km' : 'MI'; tag = 'RANGE'; }
          else if (mode21 === 'limit') { val = st.obcLimit || (km ? '120' : '70'); unit = km ? 'km/h' : 'MPH'; tag = 'LIMIT'; }
          else { val = String(st.ambient).replace('-', ''); unit = tU; if (String(st.ambient)[0] === '-') tag = '-'; }
          /* hairline separating trip from the OBC field */
          inner += '<path d="M' + f(cx - R * .5) + ' ' + f(yO - R * .035) + 'H' + f(cx + R * .5) + '" stroke="' + COL.amberGhost + '" stroke-width="' + f(R * .008) + '"/>';
          add(segText(xr, yO, ho, val, 'right'));
          lab += text(xr + R * .03, yO + ho * .55, unit, R * .065, COL.amber, { weight: 600, anchor: 'start' });
          if (tag) lab += text(cx - R * .44, yO + ho * .55, tag, R * (tag === '-' ? .09 : .06), COL.amber, { weight: 600, anchor: 'start', spacing: '.05em' });
        }
      }
      var sk = 'transform="translate(' + f(cx) + ' ' + f(top) + ') skewX(-7) translate(' + f(-cx) + ' ' + f(-top) + ')"';
      inner += '<path d="' + ghost + '" fill="' + COL.amberGhost + '" opacity=".5" ' + sk + '/><g filter="url(#' + P + 'lglow)"><path d="' + on + '" fill="' + COL.amber + '" ' + sk + '/>' + lab + '</g>';
    }
    o += '<g clip-path="url(#' + P + 'twin)">' + inner + '<path d="' + path + '" fill="url(#' + P + 'glass)" opacity=".035"/></g>';
    return '<g id="obc-display" data-display="' + mode + '" data-obc="' + (st.obcOn ? 1 : 0) + '">' + o + '</g>';
  }

  function speedoFace(P, pod, theme, st) {
    var cx = pod.cx, cy = pod.cy, R = pod.r, ink = COL.ink[theme], sub = COL.sub[theme], sc = st.scale, ital = st.numerals === 'italic';
    var sw = { from: SWEEP.speedo.from, to: SWEEP.speedo.to, min: 0, max: sc.max }, o = '';
    for (var v = 0; v <= sc.max + .01; v += sc.minor) {
      var a = lerp(sw, v), maj = Math.abs(v / sc.major - Math.round(v / sc.major)) < 1e-6, mid = !maj && Math.abs(v / (sc.major / 2) - Math.round(v / (sc.major / 2))) < 1e-6;
      if (maj) o += line(cx, cy, R * .77, R * .93, a, ink, R * .028);
      else o += line(cx, cy, R * (mid ? .84 : .865), R * .93, a, mid ? ink : sub, R * (mid ? .016 : .011));
    }
    var fs = R * (sc.max > 200 ? .15 : .165) * (sc.labels.length > 7 ? .92 : 1);
    [0].concat(sc.labels).forEach(function (n) { var p = pt(cx, cy, R * .585, lerp(sw, n)); o += text(p[0], p[1], n, fs * (ital ? 1 : .94), ink, numFont(st)); });
    o += text(cx + R * .1, cy - R * .42, sc.unit === 'MPH' ? 'MPH' : 'km/h', R * .075, sub, { weight: 600, spacing: '.06em' });
    var spd = st.speedPred;
    if (spd && spd.trueDisplay != null && Math.abs(spd.trueDisplay - spd.indicatedDisplay) > .4) {
      var at = lerp(sw, spd.trueDisplay), a1 = pt(cx, cy, R * .94, at), a2 = pt(cx, cy, R * .99, at - 2.6), a3 = pt(cx, cy, R * .99, at + 2.6);
      o += '<g id="calib-mark"><path d="M' + f(a1[0]) + ' ' + f(a1[1]) + 'L' + f(a2[0]) + ' ' + f(a2[1]) + 'L' + f(a3[0]) + ' ' + f(a3[1]) + 'Z" fill="' + COL.green + '"/>' + line(cx, cy, R * .77, R * .93, at, COL.green, R * .014) + '</g>';
    }
    if (st.cruiseOnSpeedo) o += lamp(P, 'cruise', cx + R * .42, cy + R * .2, R * .011 * 9, st.tt.cruise, theme, true);
    return o;
  }
  function speedoDisplay(P, pod, st) {
    var cx = pod.cx, cy = pod.cy, R = pod.r, km = st.unitKm;
    if (st.display === 'early') {
      var w = R * .72, h = R * .32, x = cx - w / 2 + R * .06, y = cy + R * .49;
      return '<g id="speed-display">' + seg(P, x, y, w, h, {
        rows: [{ x: x + w - R * .05, y: y + R * .03, h: R * .125, s: st.odometerDigits }, { x: x + w - R * .2, y: y + R * .175, h: R * .1, s: st.tripDigits }],
        labels: [{ x: x + w - R * .17, y: y + R * .228, s: km ? 'km' : 'MI', size: R * .072 }] }) + '</g>';
    }
    var w2 = R * .56, h2 = R * .19, x2 = cx - w2 / 2 + R * .16, y2 = cy + R * .58;
    if (st.display === 'k24') {
      var pitch = h2 / 10.5;
      return '<g id="speed-display" data-dots="1">' + dmWin(P, 'spd', x2, y2, w2, h2, [
        { s: String(st.digitalSpeed), x: x2 + w2 * .56, align: 'right', scale: 1.15 },
        { s: km ? 'km/h' : 'mph', x: x2 + w2 * .6, y: y2 + h2 - pitch * 7 * .55 - pitch * 1.3, scale: .55 }]) + '</g>';
    }
    return '<g id="speed-display">' + seg(P, x2, y2, w2, h2, {
      rows: [{ x: x2 + w2 * .55, y: y2 + h2 * .16, h: h2 * .68, s: String(st.digitalSpeed) }],
      labels: [{ x: x2 + w2 * .6, y: y2 + h2 * .58, s: km ? 'km/h' : 'mph', size: R * .068 }] }) + '</g>';
  }

  function comboFace(P, pod, theme, st) {
    var R = pod.r, ink = COL.ink[theme], sub = COL.sub[theme], red = COL.red[theme], o = '';
    var ch = hubOf(pod, 'coolant'), F = st.tempUnit === 'F', csw = F ? SWEEP.coolF : SWEEP.coolC;
    var labsC = F ? [100, 180, 250] : [40, 80, 120];
    for (var i = 0; i <= 8; i++) {
      var a = csw.from + (csw.to - csw.from) * i / 8, maj = i % 4 === 0;
      o += line(ch.x, ch.y, R * (maj ? .5 : .54), R * .62, a, maj ? ink : sub, R * (maj ? .024 : .012));
    }
    labsC.forEach(function (n) { var p = pt(ch.x, ch.y, R * .38, lerp(csw, n)); o += text(p[0], p[1], n, R * .135, ink, numFont(st)); });
    var hot = pt(ch.x, ch.y, R * .58, csw.to + 12);
    o += '<rect x="' + f(hot[0] - R * .045) + '" y="' + f(hot[1] - R * .045) + '" width="' + f(R * .09) + '" height="' + f(R * .09) + '" fill="' + red + '" transform="rotate(' + f(csw.to + 12) + ' ' + f(hot[0]) + ' ' + f(hot[1]) + ')"/>';
    var ti = pt(ch.x, ch.y, R * .22, 128);
    o += '<g transform="translate(' + f(ti[0]) + ' ' + f(ti[1]) + ') scale(' + f(R / 100) + ')" fill="none" stroke="' + sub + '" stroke-width="1.3" stroke-linecap="round"><path d="M0 -6V3"/><circle cx="0" cy="5" r="2.2" fill="' + sub + '"/><path d="M1.6 -4H4M1.6 -1.5H3.4M1.6 1H4"/><path d="M-6 9q1.5 -1 3 0t3 0 3 0 3 0"/></g>';
    var fh = hubOf(pod, 'fuel'), fsw = SWEEP.fuel;
    for (var j = 0; j <= 8; j++) {
      var fa = fsw.from + (fsw.to - fsw.from) * j / 8, fm = j % 4 === 0;
      o += line(fh.x, fh.y, R * (fm ? .62 : .68), R * .76, fa, fm ? ink : sub, R * (fm ? .03 : .014));
    }
    [['0', 0], ['2/4', 50], ['4/4', 100]].forEach(function (L) { var p = pt(fh.x, fh.y, R * .47, lerp(fsw, L[1])); o += text(p[0], p[1], L[0], R * .13, ink, numFont(st)); });
    var emp = pt(fh.x, fh.y, R * .72, fsw.from + 10);
    o += '<rect x="' + f(emp[0] - R * .045) + '" y="' + f(emp[1] - R * .045) + '" width="' + f(R * .09) + '" height="' + f(R * .09) + '" fill="' + red + '" transform="rotate(' + f(fsw.from + 10) + ' ' + f(emp[0]) + ' ' + f(emp[1]) + ')"/>';
    var fi = pt(fh.x, fh.y, R * .42, 168);
    o += '<g transform="translate(' + f(fi[0]) + ' ' + f(fi[1]) + ') scale(' + f(R / 100) + ')" fill="' + sub + '"><path d="M-5 -6h6.5v12h-6.5z"/><path d="M-3.6 -4.6h3.7v3.2h-3.7z" fill="' + COL.face[theme][1] + '"/><path d="M1.5 -3l3 2v5.5a1 1 0 0 0 2 0V-2l-1.6 -1.8" fill="none" stroke="' + sub + '" stroke-width="1.1"/><path d="M-6.4 6h9v1.3h-9z"/></g>';
    return o;
  }
  function clockDisplay(P, pod, st) {
    var R = pod.r, w = R * .56, h = R * .19, x = pod.cx - R * .52, y = pod.cy + R * .56, c = clockParts(st);
    /* 12h mode: a dot top-left for AM, bottom-left for PM */
    var dx = x + R * .035, amY = y + h * .2, pmY = y + h * .66;
    if (st.display === 'k24') {
      var pitch = h / 10.5, dots = c.ampm ? [[dx, c.ampm === 'am' ? amY : pmY]] : null;
      return '<g id="clock-display" data-dots="1" data-format="' + (c.ampm ? 12 : 24) + '" data-ampm="' + (c.ampm || '') + '">' +
        dmWin(P, 'clk', x, y, w, h, [{ s: c.s, x: x + w - R * .05, align: 'right', scale: c.ampm ? 1 : 1.15, dots: dots }]) + '</g>';
    }
    var o = seg(P, x, y, w, h, { rows: [{ x: x + w - R * .06, y: y + h * .16, h: h * .68, s: c.s }] });
    if (c.ampm) {
      var r = h * .07, ghost = COL.amberGhost;
      o += '<circle cx="' + f(dx) + '" cy="' + f(amY + r) + '" r="' + f(r) + '" fill="' + (c.ampm === 'am' ? COL.amber : ghost) + '"' + (c.ampm === 'am' ? ' filter="url(#' + P + 'lglow)"' : ' opacity=".6"') + '/>' +
           '<circle cx="' + f(dx) + '" cy="' + f(pmY + r) + '" r="' + f(r) + '" fill="' + (c.ampm === 'pm' ? COL.amber : ghost) + '"' + (c.ampm === 'pm' ? ' filter="url(#' + P + 'lglow)"' : ' opacity=".6"') + '/>';
    }
    return '<g id="clock-display" data-format="' + (c.ampm ? 12 : 24) + '" data-ampm="' + (c.ampm || '') + '">' + o + '</g>';
  }

  function smallFace(P, pod, theme, kind, st) {
    var R = pod.r, ink = COL.ink[theme], sub = COL.sub[theme], red = COL.red[theme], o = '', hb = hubOf(pod, kind), sw = SWEEP[kind];
    var n = kind === 'volt' ? 8 : 10;
    for (var i = 0; i <= n; i++) {
      var v = sw.min + (sw.max - sw.min) * i / n, a = lerp(sw, v), maj = i % 2 === 0;
      o += line(hb.x, hb.y, R * (maj ? 1.06 : 1.12), R * 1.21, a, maj ? ink : sub, R * (maj ? .04 : .02));
    }
    var labs = kind === 'volt' ? [10, 12, 14, 16] : [0, 1, 2, 3, 4, 5];
    labs.forEach(function (L) { var p = pt(hb.x, hb.y, R * .86, lerp(sw, L)); o += text(p[0], p[1], L, R * .21, ink, numFont(st)); });
    if (kind === 'volt') {
      var bi = pt(hb.x, hb.y, R * .98, -158);
      o += '<g transform="translate(' + f(bi[0] + R * .2) + ' ' + f(bi[1] - R * .02) + ') scale(' + f(R / 60) + ')" fill="none" stroke="' + sub + '" stroke-width="1.2"><rect x="-8" y="-4" width="16" height="9" rx="1"/><path d="M-5 -6v2M5 -6v2M-6 .5h3M3 .5h3M4.5 -1v3"/></g>';
    } else {
      var oi = pt(hb.x, hb.y, R * .98, 158);
      o += '<g transform="translate(' + f(oi[0] - R * .2) + ' ' + f(oi[1] - R * .02) + ') scale(' + f(R / 60) + ')" fill="none" stroke="' + sub + '" stroke-width="1.2" stroke-linejoin="round"><path d="M-9 1h4l2 -3h7l5 2 3 -2v1l-4 4h-13l-4 -2z"/><path d="M10 3q1 2 0 3"/></g>';
    }
    return o;
  }

  /* ============================================================== lamps */
  var ICON = {
    cruise:  function (c) { return '<path d="M-8 3.5a8 8 0 1 1 16 0" fill="none" stroke="' + c + '" stroke-width="1.9" stroke-linecap="round"/><path d="M0 3l5 -6" stroke="' + c + '" stroke-width="1.9" stroke-linecap="round"/><circle cx="0" cy="3" r="1.9" fill="' + c + '"/><path d="M-9.5 -1.5l2.4 1M9.5 -1.5l-2.4 1M0 -6v2.4" stroke="' + c + '" stroke-width="1.4" stroke-linecap="round"/>'; },
    spoiler: function (c) { return '<path d="M-11 4.5q1.5 -6.5 9 -6.5h6.5l4.5 3.5h1.5v3z" fill="' + c + '"/><circle cx="-5.5" cy="5.5" r="2.2" fill="' + c + '"/><circle cx="6" cy="5.5" r="2.2" fill="' + c + '"/><path d="M-12.5 -6.5h8.5l-1.2 2.4h-7.3z" fill="' + c + '"/><path d="M-8.5 -4.2v3" stroke="' + c + '" stroke-width="1.4"/><path d="M-14 -10l3 2.2M-3 -10l-3 2.2" stroke="' + c + '" stroke-width="1.2" stroke-linecap="round"/>'; },
    belt:    function (c) { return '<circle cx="-1" cy="-7.4" r="2.6" fill="' + c + '"/><path d="M-6 9.5V-1q0 -3 3 -3h4q3 0 3 3v4.5h-2V9.5z" fill="' + c + '"/><path d="M-3.6 -4.2L5.8 6.2" stroke="#0B0E12" stroke-width="3.2" stroke-linecap="round"/><path d="M-3.6 -4.2L5.8 6.2" stroke="' + c + '" stroke-width="1.5" stroke-linecap="round"/>'; }
  };
  var LAMP_COL = { cruise: COL.green, spoiler: COL.warnAmber, belt: COL.warnRed };
  function lamp(P, name, x, y, s, on, theme, onFace) {
    var c = on ? LAMP_COL[name] : (onFace ? COL.lens[theme] : '#3A1F12');
    return '<g class="pws-tt" data-telltale="' + name + '" data-on="' + (on ? 1 : 0) + '" transform="translate(' + f(x) + ' ' + f(y) + ') scale(' + f(s / 10) + ')"' + (on ? ' filter="url(#' + P + 'tglow)"' : '') + '>' + ICON[name](c) + '</g>';
  }
  function knob(P, x, y, kind) {
    var o = '<g class="pws-knob" data-knob="' + kind + '"><circle cx="' + f(x) + '" cy="' + f(y) + '" r="7.6" fill="#030405"/>' +
      '<circle cx="' + f(x) + '" cy="' + f(y) + '" r="6.8" fill="url(#' + P + 'knobTop)" stroke="#5A6370" stroke-opacity=".5" stroke-width=".6"/>';
    if (kind === 'trip') o += '<text x="' + f(x) + '" y="' + f(y + 1.6) + '" font-size="3.4" font-weight="700" text-anchor="middle" dominant-baseline="central" fill="#E5E8EB" font-family="' + SANS + '">0.0</text><path d="M' + f(x - 2.4) + ' ' + f(y - .6) + 'a2.4 2.4 0 1 1 4.8 0" fill="none" stroke="#E5E8EB" stroke-width=".7"/>';
    else o += '<circle cx="' + f(x) + '" cy="' + f(y) + '" r="3.6" fill="none" stroke="#E5E8EB" stroke-width=".7"/><path d="M' + f(x) + ' ' + f(y - 2.4) + 'V' + f(y) + 'h1.8" fill="none" stroke="#E5E8EB" stroke-width=".7" stroke-linecap="round"/>';
    return o + '</g>';
  }
  function topJunction(a, b, ra, rb) {
    /* upper intersection of two circles (bezel outlines) */
    var dx = b.cx - a.cx, dy = b.cy - a.cy, d = Math.sqrt(dx * dx + dy * dy), l = (ra * ra - rb * rb + d * d) / (2 * d), h = Math.sqrt(Math.max(0, ra * ra - l * l));
    var mx = a.cx + l * dx / d, my = a.cy + l * dy / d;
    return { x: mx + h * dy / d, y: my - h * dx / d };
  }

  /* ============================================================== main */
  function renderClusterSvg(state) {
    state = state || {};
    var dials = state.dials === 5 ? 5 : 3, L = LAYOUTS[dials], pods = L.pods, W = L.w, H = L.h;
    var theme = state.faceTheme === 'white' ? 'white' : 'black', bezel = state.bezel || (theme === 'white' ? 'chrome' : 'black');
    var P = (state.idPrefix || ('pws' + (++counter))) + '-', pm = state.pm || {};
    var sc = state.scale && state.scale.labels ? state.scale : (SCALES[(state.scale && state.scale.id) || state.scaleId || '180_mph'] || SCALES['180_mph']);
    var km = sc.unit !== 'MPH', spd = state.speedPred || { indicatedDisplay: state.simMph || 0, trueDisplay: state.simMph || 0 };
    var display = DISPLAYS.indexOf(state.display) >= 0 ? state.display : 'k24';
    var tt = Object.assign({ cruise: !!pm.cruise, spoiler: !!pm.spoiler, belt: false }, state.telltales || {});
    var odo = String(state.odometer != null ? state.odometer : (km ? '103194' : '064120')).replace(/[^0-9]/g, '');
    var st = {
      dials: dials, scale: sc, unitKm: km, speedPred: spd, display: display, tempUnit: state.tempUnit === 'F' ? 'F' : 'C',
      digitalSpeed: state.digitalSpeed != null ? state.digitalSpeed : Math.round(spd.trueDisplay != null ? spd.trueDisplay : spd.indicatedDisplay || 0),
      odometer: odo, odometerDigits: ('000000' + odo).slice(-6), trip: state.trip != null ? String(state.trip) : '228.7',
      tripDigits: state.trip != null ? String(state.trip) : '228.7',
      ambient: state.ambient != null ? String(state.ambient) : (state.tempUnit === 'F' ? '52' : '14.5'),
      clock: state.clock || '14:25', clockFormat: state.clockFormat === '12' || state.clockFormat === 12 || state.clock12 ? '12' : '24',
      numerals: state.numerals === 'upright' || state.numerals === 'italic' ? state.numerals : (dials === 5 ? 'upright' : 'italic'),
      obcMode: state.obcMode, obcMpg: state.obcMpg, obcRange: state.obcRange, obcLimit: state.obcLimit,
      obcOn: pm.obc_enabled !== false, obcMenu: state.obcMenu, obcActive: state.obcActive, obcLines: state.obcLines, obcBig: state.obcBig,
      redlineRpm: state.redlineRpm, tachLabel: state.tachLabel, tt: tt,
      cruiseOnSpeedo: !!pm.cruise && (state.cruiseLamp || 'speedo') === 'speedo'
    };
    var rpm = state.rpm != null ? state.rpm : 4000;
    var coolC = state.coolantPred && state.coolantPred.indicatedC != null ? state.coolantPred.indicatedC : 80;
    var cool = st.tempUnit === 'F' ? coolC * 9 / 5 + 32 : coolC;
    var fuel = state.fuelPred && state.fuelPred.indicatedPct != null ? state.fuelPred.indicatedPct : 75;
    var o = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' +
      (dials === 5 ? '996' : '986') + ' instrument cluster, ' + theme + ' faces, ' + display + ' displays" class="pws-cluster pws-cluster--' + dials + ' pws-face--' + theme + ' pws-display--' + display + '">';
    if (state.embedFonts) o += '<style>@import url("https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:ital,wght@0,500;0,600;1,500&amp;family=Barlow:wght@600&amp;family=JetBrains+Mono:wght@700&amp;display=swap");</style>';
    o += defs(P, theme, bezel);

    /* housing: binnacle arch + lit lip */
    var hx0 = dials === 5 ? pods.volt.cx - pods.volt.r - 28 : 12, hx1 = W - hx0, top = -36;
    var hp = 'M' + hx0 + ' ' + (H - 10) + 'L' + hx0 + ' 98Q' + W / 2 + ' ' + top + ' ' + hx1 + ' 98L' + hx1 + ' ' + (H - 10) + 'Q' + W / 2 + ' ' + H + ' ' + hx0 + ' ' + (H - 10) + 'Z';
    o += '<g id="cowl"><path d="' + hp + '" fill="url(#' + P + 'housing)"/><path d="M' + hx0 + ' 98Q' + W / 2 + ' ' + top + ' ' + hx1 + ' 98" fill="none" stroke="url(#' + P + 'lip)" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M' + (hx0 + 10) + ' 106Q' + W / 2 + ' ' + (top + 12) + ' ' + (hx1 - 10) + ' 106" fill="none" stroke="#000" stroke-opacity=".55" stroke-width="10" stroke-linecap="round" filter="url(#' + P + 'soft)"/></g>';

    /* telltale strip: only coded features get a lamp */
    var tc = pods.tach, bw = tc.r * 1.5, sx0 = tc.cx - bw, sx1 = tc.cx + bw, sy0 = tc.cy + tc.r * .55, sy1 = Math.min(H - 12, tc.cy + tc.r + 44);
    var stripLamps = [];
    if (pm.spoiler) stripLamps.push('spoiler');
    if (pm.cruise && !st.cruiseOnSpeedo) stripLamps.push('cruise');
    if (pm.belt_lamp) stripLamps.push('belt');
    o += '<g id="telltales"><path d="M' + f(sx0) + ' ' + f(sy0) + 'H' + f(sx1) + 'C' + f(sx1 + 14) + ' ' + f(sy0) + ' ' + f(sx1 + 16) + ' ' + f(sy1 - 6) + ' ' + f(sx1 - 6) + ' ' + f(sy1 - 2) +
      'Q' + f(tc.cx) + ' ' + f(sy1 + 10) + ' ' + f(sx0 + 6) + ' ' + f(sy1 - 2) + 'C' + f(sx0 - 16) + ' ' + f(sy1 - 6) + ' ' + f(sx0 - 14) + ' ' + f(sy0) + ' ' + f(sx0) + ' ' + f(sy0) + 'Z" fill="url(#' + P + 'strip)" stroke="#2A3038" stroke-width=".8"/>';
    var ly = (tc.cy + tc.r + 12 + sy1) / 2 + 2, gap = 30, span = gap * (stripLamps.length - 1);
    stripLamps.forEach(function (n, i) {
      var lx = tc.cx - span / 2 + i * gap;
      o += '<circle cx="' + f(lx) + '" cy="' + f(ly) + '" r="10.5" fill="#060708" stroke="#262B32" stroke-width="1"/>' + lamp(P, n, lx, ly, 7.6, tt[n] !== false, theme, false);
    });
    o += '</g>';

    function pod(id, inner, extra) {
      var p = pods[id], fp = housingOf(id, p);
      return '<g id="pod-' + id + '" filter="url(#' + P + 'pod)">' + podFrame(P, fp, id) + '<g id="face-' + id + '">' + inner + '</g>' + (extra || '') + glass(P, fp) + '</g>';
    }
    /* 996 end pods: the scale stays where it is, but the housing is drawn with the same curvature as the
       main dials and slides in behind its neighbour, so only a crescent with a matching outer curve shows. */
    function housingOf(id, p) {
      if (id !== 'volt' && id !== 'oil') return p;
      var Rh = END_HOUSING_R, dir = id === 'volt' ? 1 : -1;
      return { cx: p.cx + dir * (Rh - p.r + END_HOUSING_INSET), cy: p.cy, r: Rh };
    }
    var order = dials === 5 ? ['volt', 'oil', 'speedo', 'combo', 'tach'] : ['speedo', 'combo', 'tach'];
    order.forEach(function (id) {
      var p = pods[id], R = p.r;
      if (id === 'tach') {
        o += pod('tach', tachFace(P, p, theme, st) + tachDisplay(P, p, st), needle(P, p.cx, p.cy, R * HUBS.tach.len, lerp(SWEEP.tach, rpm), 'tach', R * .022, R * .15));
      } else if (id === 'speedo') {
        var sw = { from: SWEEP.speedo.from, to: SWEEP.speedo.to, min: 0, max: sc.max };
        o += pod('speedo', speedoFace(P, p, theme, st) + speedoDisplay(P, p, st), needle(P, p.cx, p.cy, R * HUBS.speedo.len, lerp(sw, spd.indicatedDisplay || 0), 'speedo', R * .022, R * .14));
      } else if (id === 'combo') {
        var ch = hubOf(p, 'coolant'), fh = hubOf(p, 'fuel'), csw = st.tempUnit === 'F' ? SWEEP.coolF : SWEEP.coolC;
        o += pod('combo', comboFace(P, p, theme, st) + clockDisplay(P, p, st),
          needle(P, ch.x, ch.y, ch.len, lerp(csw, cool), 'coolant', R * .02, R * .1) + needle(P, fh.x, fh.y, fh.len, lerp(SWEEP.fuel, fuel), 'fuel', R * .02, R * .1));
      } else {
        var hb = hubOf(p, id), val = id === 'volt' ? (state.volts != null ? state.volts : 13.8) : (state.oilBar != null ? state.oilBar : 3.2);
        o += pod(id, smallFace(P, p, theme, id, st), needle(P, hb.x, hb.y, hb.len, lerp(SWEEP[id], val), id, R * .028, 0, true));
      }
    });

    /* knobs between the pods, as on the car: trip reset (left) and clock set (right) */
    function ring(p) { return p.r * 1.12; }
    var jl = topJunction(pods.speedo, pods.tach, ring(pods.speedo), ring(pods.tach)), jr = topJunction(pods.tach, pods.combo, ring(pods.tach), ring(pods.combo));
    o += knob(P, jl.x + 1, jl.y - 3, 'trip') + knob(P, jr.x - 1, jr.y - 3, 'clock');
    return o + '</svg>';
  }

  function angleFor(gauge, value, scale) {
    if (gauge === 'speedo') return lerp({ from: SWEEP.speedo.from, to: SWEEP.speedo.to, min: 0, max: (scale && scale.max) || 180 }, value);
    if (gauge === 'coolant') gauge = 'coolC';
    return lerp(SWEEP[gauge], value);
  }
  function hubFor(dials, gauge) { var Lx = LAYOUTS[dials === 5 ? 5 : 3], podKey = gauge === 'coolant' || gauge === 'fuel' ? 'combo' : gauge, p = Lx.pods[podKey]; var h = hubOf(p, gauge); return { x: h.x, y: h.y }; }

  return { renderClusterSvg: renderClusterSvg, angleFor: angleFor, hubFor: hubFor, LAYOUTS: LAYOUTS, HUBS: HUBS, END_HOUSING_R: END_HOUSING_R, SWEEP: SWEEP, SCALES: SCALES, DISPLAYS: DISPLAYS, COLORS: COL, version: '2.1.1' };
}));

// Pixel art borrowed from Quokka Run (perth-ai/perth-ai-website, src/scripts/quokka-run/sprites.js),
// the runner from the Perth AI booth at DDD Perth 2026. Same maps, drawn as crisp data URLs for the deck's easter eggs.
(function () {
var PALETTE = {
  o: '#2b1a10', // outline
  b: '#9c6b45', // fur
  h: '#c08d5f', // fur highlight
  l: '#ecd2a8', // cream face / belly
  e: '#0b0604', // eye
  w: '#ffffff', // eye shine
  p: '#e39a86', // inner ear
  n: '#120a06', // nose
  m: '#7b3fe4', // hallucination bug
  v: '#b28fef', // bug highlight
  k: '#232f52', // GPU board
  c: '#007195', // GPU chip
  a: '#5cd8ff', // GPU die
  i: '#c4c8d4', // GPU pins
  f: '#ff6b1a', // flame
  y: '#ffd23f', // flame core
};

var QUOKKA_TOP = [
  '............oo..oo..',
  '...........obpoobpo.',
  '...........obbbbbbo.',
  '..........obbbbbwebo',
  '..........obbbbbeebo',
  '.....ooooobbbbblllno',
  '...oobbbbbbbbbllllo.',
  '..obbhhbbbbbbbllool.',
  '.obbhhbbbbbbblllllo.',
  'obbbbbbbbbbbbllllo..',
  'obbbbbbbbbbbblllo...',
  '.obbbbbbbbbbbbbo....',
];

var LEGS = {
  run1: ['..obbbbbbbbbbbo.....', '...obbo...obbo......', '..obbo....obbo......', '..ooo.....oooo......'],
  run2: ['..obbbbbbbbbbbo.....', '....obbo.obbo.......', '....obbo.obbo.......', '....oooo.oooo.......'],
  jump: ['..obbbbbbbbbbbo.....', '.obbo.....obbbo.....', 'obo........obbbo....', 'oo..........oooo....'],
};

var BUG = [
  '....oooo....',
  '..oommmmoo..',
  '.ommvvmmmmo.',
  'omvwwmmwwmmo',
  'ommwemmmwemo',
  'ommmmmmmmmmo',
  'ommmmoommmmo',
  'ommmmmmmmmmo',
  'omomommomomo',
  'o.o.oo.o.o.o',
];

// A hallucination that's learned to fly: the bug with a spinning propeller.
var PROPELLERS = [
  ['.iiii..iiii.', '.....ii.....'],
  ['...iiiiii...', '.....ii.....'],
];

var GPU_BASE = [
  'oooooooooooo',
  'okkkkkkkkkko',
  'okccccccccko',
  'okcaaaaaacko',
  'okcaaaaaacko',
  'okccccccccko',
  'okkkkkkkkkko',
  'oioioioioioo',
];
var FLAMES = [
  ['..f.....f...', '.fyf...fyf..', '.fyyf.fyyff.', 'fyyyyfyyyyyf'],
  ['....f.....f.', '...fyf...fyf', '.ffyyf.fyyf.', 'fyyyyyfyyyyf'],
];

function draw(rows) {
  var w = Math.max.apply(null, rows.map(function (r) { return r.length; }));
  var c = document.createElement('canvas');
  c.width = w; c.height = rows.length;
  var ctx = c.getContext('2d');
  rows.forEach(function (row, y) {
    row.split('').forEach(function (ch, x) {
      if (!PALETTE[ch]) return;
      ctx.fillStyle = PALETTE[ch];
      ctx.fillRect(x, y, 1, 1);
    });
  });
  return c.toDataURL();
}

var cache = null;
window.Pixel = function () {
  cache = cache || {
    run1: draw(QUOKKA_TOP.concat(LEGS.run1)),
    run2: draw(QUOKKA_TOP.concat(LEGS.run2)),
    jump: draw(QUOKKA_TOP.concat(LEGS.jump)),
    bug: draw(BUG),
    gpu: draw(FLAMES[0].concat(GPU_BASE)),
    drone: draw(PROPELLERS[0].concat(BUG))
  };
  return cache;
};
})();

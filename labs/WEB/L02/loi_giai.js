const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const cb = kv.w + 2 * (kv.pad + kv.bd), bb = kv.w;
console.log(`content_box_w=${cb}`);
console.log(`border_box_w=${bb}`);
console.log(`id_beats_2class=${Number(kv.id_a > kv.id_b)}`);

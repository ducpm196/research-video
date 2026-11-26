const fs = require('fs');
const lines = fs.readFileSync(0, 'utf8').trim().split(/\r?\n/);
const kv = Object.fromEntries(lines.map(l => l.split('=', 2)));
const merge = (x, y) => [...new Set([...x, ...y])].sort();
const a = kv.a.split(','), b = kv.b.split(',');
const ab = merge(a, b), ba = merge(b, a);
console.log(`merged_len=${ab.length}`);
console.log(`commutative=${Number(JSON.stringify(ab) === JSON.stringify(ba))}`);
console.log(`idempotent=${Number(JSON.stringify(merge(ab, ab)) === JSON.stringify(ab))}`);

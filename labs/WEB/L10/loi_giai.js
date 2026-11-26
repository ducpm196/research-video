const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const t1 = kv.big_kb / kv.bw_kbps, t2 = kv.small_kb / kv.bw_kbps;
console.log(`time_2mb_s=${t1.toFixed(1)}`);
console.log(`time_500kb_s=${t2.toFixed(1)}`);
console.log(`faster_by=${(t1 / t2).toFixed(1)}x`);

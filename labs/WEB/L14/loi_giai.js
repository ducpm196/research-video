const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
let k = 0; while (Math.pow(kv.stay_rate, k) >= 0.10) k++;
console.log(`week4_old_pct=${(100 * Math.pow(kv.stay_rate, kv.w1)).toFixed(1)}%`);
console.log(`week8_old_pct=${(100 * Math.pow(kv.stay_rate, kv.w2)).toFixed(1)}%`);
console.log(`weeks_under_10pct=${k}`);

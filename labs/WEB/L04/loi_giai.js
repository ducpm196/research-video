const fs = require('fs');
const raw = fs.readFileSync(0, 'utf8').trim().split('=')[1];
const t = raw.split(',').map(Number);
const seq = t.reduce((a, b) => a + b, 0), par = Math.max(...t);
console.log(`seq_ms=${seq}`);
console.log(`parallel_ms=${par}`);
console.log(`speedup=${(seq / par).toFixed(1)}x`);

const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const b1 = 1000 / kv.hz1, b2 = 1000 / kv.hz2;
console.log(`budget_60hz_ms=${b1.toFixed(1)}`);
console.log(`budget_120hz_ms=${b2.toFixed(1)}`);
console.log(`task12ms_jank_at_60_120=${Number(kv.task_ms > b1)},${Number(kv.task_ms > b2)}`);

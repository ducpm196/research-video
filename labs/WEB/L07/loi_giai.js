const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const off = (kv.page - 1) * kv.size;
console.log(`offset_skipped=${off}`);
console.log(`offset_scanned=${off + kv.size}`);
console.log(`cursor_scanned=${kv.size}`);

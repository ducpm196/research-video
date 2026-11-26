const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
console.log(`http10_ms=${2 * (1 + kv.assets) * kv.rtt}`);
console.log(`http11_ms=${(2 + kv.assets) * kv.rtt}`);
console.log(`http2_ms=${3 * kv.rtt}`);

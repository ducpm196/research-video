const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const stages = ['TCP', 'TLS', 'HTTP'];
const ttfb = r => stages.length * r;
console.log(`ttfb_50ms=${ttfb(kv.rtt_near)}`);
console.log(`remote_200ms_4api=${ttfb(kv.rtt_far) + kv.apis * kv.rtt_far}`);
console.log(`roundtrips_handshake=${stages.length}`);

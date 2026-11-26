const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));
const stale = Number(kv.age) >= Number(kv.max_age);
const code = stale ? (kv.cli_etag === kv.srv_etag ? 304 : 200) : 0;
console.log(`is_stale=${Number(stale)}`);
console.log(`status_code=${code}`);
console.log(`body_resent=${Number(code === 200)}`);

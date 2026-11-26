const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')));
const RFC = { GET: [1, 1], PUT: [0, 1] };
let bal = Number(kv.bal); const seen = new Set();
for (const item of kv.keys.split(',')) {
  const [k, amt] = item.split(':');
  if (!seen.has(k)) { seen.add(k); bal -= Number(amt); }
}
console.log('get_safe_idem=' + RFC.GET.join(','));
console.log('put_safe_idem=' + RFC.PUT.join(','));
console.log(`post_with_idem_key_bal=${bal}`);

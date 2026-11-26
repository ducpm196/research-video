const fs = require('fs');
const kv = Object.fromEntries(fs.readFileSync(0, 'utf8').trim().split(/\s+/).map(s => s.split('=')).map(([k, v]) => [k, Number(v)]));
const out = [kv.sync1]; let syncDone = 0;
setTimeout(() => {
  out.push(kv.macro);
  console.log(`sync_done=${syncDone}`);
  console.log('event_loop_order=' + out.join(','));
  console.log(`micro_before_macro=${Number(out.indexOf(kv.micro) < out.indexOf(kv.macro))}`);
}, 0);
Promise.resolve().then(() => out.push(kv.micro));
out.push(kv.sync2); syncDone = Number(out.length === 2);

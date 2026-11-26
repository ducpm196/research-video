const fs = require('fs');
const html = fs.readFileSync(0, 'utf8').trim();
let nodes = 0, d = 0, mx = 0, ok = true;
for (const [, close] of html.matchAll(/<(\/?)([a-z]+)>/g)) {
  if (!close) { nodes++; d++; mx = Math.max(mx, d); }
  else { d--; if (d < 0) ok = false; }
}
console.log(`nodes=${nodes}`);
console.log(`max_depth=${mx}`);
console.log(`valid_balanced=${Number(ok && d === 0)}`);

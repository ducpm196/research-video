const html = '<ul><li>A</li><li>B<b>!</b></li></ul>';
let nodes = 0, d = 0, mx = 0;
for (const [, close, tag] of html.matchAll(/<(\/?)([a-z]+)>/g)) {
  if (!close) { nodes++; d++; mx = Math.max(mx, d); } else d--;
}
console.log(`nodes=${nodes}`); console.log(`max_depth=${mx}`);
console.log(`valid_balanced=${Number(d === 0)}`);

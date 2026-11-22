const merge = (a, b) => [...new Set([...a, ...b])].sort();
const a = ['lam bai', 'mua sua'], b = ['lam bai', 'goi me'];
const ab = merge(a, b), ba = merge(b, a);
console.log(`merged_len=${ab.length}`);
console.log(`commutative=${Number(JSON.stringify(ab) === JSON.stringify(ba))}`);
console.log(`idempotent=${Number(JSON.stringify(merge(ab, ab)) === JSON.stringify(ab))}`);

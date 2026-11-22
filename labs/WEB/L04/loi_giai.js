const t = [100, 200, 300];
const seq = t.reduce((a, b) => a + b, 0), par = Math.max(...t);
console.log(`seq_ms=${seq}`); console.log(`parallel_ms=${par}`);
console.log(`speedup=${(seq / par).toFixed(1)}x`);

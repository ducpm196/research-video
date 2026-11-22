let k = 0; while (Math.pow(0.7, k) >= 0.10) k++;
console.log(`week4_old_pct=${(100 * Math.pow(0.7, 4)).toFixed(1)}%`);
console.log(`week8_old_pct=${(100 * Math.pow(0.7, 8)).toFixed(1)}%`);
console.log(`weeks_under_10pct=${k}`);

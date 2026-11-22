const t1 = 2000 / 200, t2 = 500 / 200;
console.log(`time_2mb_s=${t1.toFixed(1)}`);
console.log(`time_500kb_s=${t2.toFixed(1)}`);
console.log(`faster_by=${(t1 / t2).toFixed(1)}x`);

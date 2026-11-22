const b60 = 1000 / 60, b120 = 1000 / 120;
console.log(`budget_60hz_ms=${b60.toFixed(1)}`);
console.log(`budget_120hz_ms=${b120.toFixed(1)}`);
console.log(`task12ms_jank_at_60_120=${Number(12 > b60)},${Number(12 > b120)}`);

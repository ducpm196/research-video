const fs = require('fs');
const a = fs.readFileSync(0, 'utf8').trim().split('=')[1].split(',').map(Number);
const dp = a.map(() => 1);
for (let i = 0; i < a.length; i++)
  for (let j = 0; j < i; j++) if (a[j] < a[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
const lis = Math.max(...dp);
console.log(`kept_in_place=${lis}`);
console.log(`min_moves=${a.length - lis}`);
console.log(`total_items=${a.length}`);

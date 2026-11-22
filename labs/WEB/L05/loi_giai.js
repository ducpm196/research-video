const a = [2, 0, 1, 3, 4], dp = a.map(() => 1);
for (let i = 0; i < a.length; i++)
  for (let j = 0; j < i; j++) if (a[j] < a[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
const lis = Math.max(...dp);
console.log(`kept_in_place=${lis}`); console.log(`min_moves=${a.length - lis}`);
console.log(`total_items=${a.length}`);

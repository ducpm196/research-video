import math, sys
from functools import lru_cache
k = int(sys.stdin.read().split('=')[1])
steps = 3 * k
res = {}
def dfs(p0, p1, r0, r1, x):
    if p0 == steps and p1 == steps:
        res[x] = res.get(x, 0) + 1
        return
    if p0 < steps:
        dfs(p0 + 1, p1, x if p0 % 3 == 0 else (r0 + 1 if p0 % 3 == 1 else r0), r1, r0 if p0 % 3 == 2 else x)
    if p1 < steps:
        dfs(p0, p1 + 1, r0, x if p1 % 3 == 0 else (r1 + 1 if p1 % 3 == 1 else r1), r1 if p1 % 3 == 2 else x)
dfs(0, 0, 0, 0, 0)
print(f'total_interleavings={math.comb(2 * steps, steps)}')
print('distinct_x=' + ','.join(map(str, sorted(res))))
print(f'buggy_paths_gt0={int(sum(v for key, v in res.items() if key < 2 * k) > 0)}')

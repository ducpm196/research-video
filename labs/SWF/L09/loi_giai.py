import math
res = {}
def dfs(p0, p1, r0, r1, x):
    if p0==6 and p1==6: res[x] = res.get(x, 0) + 1; return
    if p0 < 6: dfs(p0+1, p1, x if p0%3==0 else (r0+1 if p0%3==1 else r0), r1, r0 if p0%3==2 else x)
    if p1 < 6: dfs(p0, p1+1, r0, x if p1%3==0 else (r1+1 if p1%3==1 else r1), r1 if p1%3==2 else x)
dfs(0, 0, 0, 0, 0)
print(f'total_interleavings={math.comb(12, 6)}')
print('distinct_x=' + ','.join(map(str, sorted(res))))
print(f'buggy_paths_gt0={int(sum(v for k,v in res.items() if k<4) > 0)}')

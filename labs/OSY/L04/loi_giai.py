import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
incs, x0 = kv['incs'], kv['x0']; lim = 3 * incs; seen = set()
def dfs(p0, p1, r0, r1, x):
    if p0 == lim and p1 == lim: seen.add(x); return
    for tid, pc in ((0, p0), (1, p1)):
        if pc == lim: continue
        op = pc % 3; nr0, nr1, nx = r0, r1, x
        if op == 0:
            if tid == 0: nr0 = x
            else: nr1 = x
        elif op == 1:
            if tid == 0: nr0 += 1
            else: nr1 += 1
        else: nx = nr0 if tid == 0 else nr1
        dfs(p0 + (tid == 0), p1 + (tid == 1), nr0, nr1, nx)
dfs(0, 0, 0, 0, x0); vals = sorted(seen); exp = x0 + 2 * incs
print('possible_x=' + ','.join(map(str, vals)))
print(f'min_x={vals[0]} max_x={vals[-1]}')
print(f'valid_outcomes_lt4={int(any(v < exp for v in vals))}')

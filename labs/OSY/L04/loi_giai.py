seen = set()
def dfs(pc0, pc1, r0, r1, x):
    if pc0 == 6 and pc1 == 6: seen.add(x); return
    for tid, pc in ((0, pc0), (1, pc1)):
        if pc == 6: continue
        op = pc % 3; nr0, nr1, nx = r0, r1, x
        if op == 0:
            if tid == 0: nr0 = x
            else: nr1 = x
        elif op == 1:
            if tid == 0: nr0 += 1
            else: nr1 += 1
        else: nx = nr0 if tid == 0 else nr1
        dfs(pc0 + (tid == 0), pc1 + (tid == 1), nr0, nr1, nx)
dfs(0, 0, 0, 0, 0); vals = sorted(seen)
print('possible_x=' + ','.join(map(str, vals)))
print(f'min_x={vals[0]} max_x={vals[-1]}')
print(f'valid_outcomes_lt4={int(any(v < 4 for v in vals))}')

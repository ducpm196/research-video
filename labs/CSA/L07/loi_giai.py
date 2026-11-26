import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
r1, r2, dyn, iters = 0, 1, kv['init_insts'], 0
while r2 <= kv['n']:
    r1 += r2; r2 += 1; dyn += kv['body_insts']; iters += 1
print(f'sum_1_to_10={r1}')
print(f'loop_iters={iters}')
print(f'total_dynamic_insts={dyn}')

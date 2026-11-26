import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = tuple(map(int, kv['base'].split('.')))
def bump(v, k):
    M, m, pt = v
    return (M, m, pt + 1) if k == 'patch' else ((M, m + 1, 0) if k == 'minor' else (M + 1, 0, 0))
fmt = lambda v: '.'.join(map(str, v))
t1, t2 = tuple(map(int, kv['v1'].split('.'))), tuple(map(int, kv['v2'].split('.')))
print(f'patch={fmt(bump(p, "patch"))} minor={fmt(bump(p, "minor"))} major={fmt(bump(p, "major"))}')
print(f'tuple_cmp_1_10_gt_1_9={int(t1 > t2)}')
print(f'str_cmp_wrong={int((kv["v1"] > kv["v2"]) != (t1 > t2))}')

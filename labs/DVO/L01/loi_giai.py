import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
prob = kv['hot'] / kv['total']
p1 = 1 - (1 - prob) ** kv['k_long']
p2 = 1 - (1 - prob) ** kv['k_short']
print(f'p_conflict_40={100 * p1:.1f}%')
print(f'p_conflict_5={100 * p2:.1f}%')
print(f'shorter_branch_safer={int(p2 < p1)}')

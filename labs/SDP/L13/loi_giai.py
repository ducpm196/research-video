import random, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
def fee_old(t, k): return round(t + t * 0.1 + (0 if t >= 500000 else 15000 + max(0, k - 5) * 4000))
def fee_new(t, k):
    tax = t * 0.1
    ship = 0 if t >= 500000 else 15000 + max(0, k - 5) * 4000
    return round(t + tax + ship)
def fee_bug(t, k): return round(t + t * 0.1 + (0 if t >= 500000 else 15000 + (k - 5) * 4000))
r = random.Random(kv['seed'])
pairs = [(r.randrange(0, 1000001, 1000), r.randrange(0, 31)) for _ in range(kv['pairs'])]
print(f'new_mismatches={sum(fee_old(t, k) != fee_new(t, k) for t, k in pairs)}')
print(f'bug_mismatches={sum(fee_old(t, k) != fee_bug(t, k) for t, k in pairs)}')
print(f'edge_500k_3km={fee_new(kv["edge_t"], kv["edge_km"])}')

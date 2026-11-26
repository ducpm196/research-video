import bisect, hashlib, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
h32 = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)
keys = range(kv['keys']); n1, n2 = kv['n_old'], kv['n_new']
mod_mv = sum((k % n1) != (k % n2) for k in keys)
def ch_own(n, k):
    r = sorted((h32(f'n{i}#{v}'), i) for i in range(n) for v in range(100))
    x = bisect.bisect(r, (h32(f'k{k}'), 99)) % len(r)
    return r[x][1]
ch_mv = sum(ch_own(n1, k) != ch_own(n2, k) for k in keys)
print(f'mod_moved_pct={100 * mod_mv / len(keys):.1f}%')
print(f'ch_moved_lt_30pct={int(ch_mv * 100 < 30 * len(keys))}')
print(f'ideal_moved_pct={100 / n2:.1f}%')

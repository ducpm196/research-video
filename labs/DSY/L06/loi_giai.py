import bisect, hashlib
h32 = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)
keys = range(1000); mod_mv = sum((k % 4) != (k % 5) for k in keys)
def ch_own(n, k): r = sorted((h32(f'n{i}#0'), i) for i in range(n)); x = bisect.bisect(r, (h32(f'k{k}'), 99)) % n; return r[x][1]
ch_mv = sum(ch_own(4, k) != ch_own(5, k) for k in keys)
print(f'mod_moved_pct={100*mod_mv/1000:.1f}%')
print(f'ch_moved_lt_30pct={int(ch_mv < 300)}')
print(f'ideal_moved_pct={100 / 5:.1f}%')

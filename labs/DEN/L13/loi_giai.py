import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
b, s, n = float(kv['big_gb']), float(kv['sm_gb']), int(kv['nodes'])
bc = round((n - 1) * s); sh = (b + s) * (n - 1) / n
print(f'broadcast_gb={bc}\nshuffle_gb={sh:.2f}\nnetwork_saved_pct={100 * (sh - bc) / sh:.1f}%')

import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
o = round(kv['old_pct'] * kv['full_n']); g = kv['new_ok'] / o; sv = round(kv['ver_pct'] * kv['ver_n'])
print(f'full_old={o} full_gain={g:.1f}x verified_solved={sv}')

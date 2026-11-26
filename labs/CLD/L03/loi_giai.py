import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
av = float(kv['avail']) ** int(kv['hops']); dt = (1.0 - av) * 525_600
print(f'avail_pct={av * 100:.2f}%\ndowntime_min={dt:.1f}')

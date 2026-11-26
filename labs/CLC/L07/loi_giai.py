import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
sm = kv['snap_hours'] * 60; wm = kv['wal_min']
print(f'snap_rpo_min={sm}\nwal_rpo_min={wm}\nrpo_cut={sm // wm}x')

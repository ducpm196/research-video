import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
bl = (kv['peak_in'] - kv['proc']) * kv['secs']; dr = kv['proc'] - kv['low_in']
print(f'backlog_30m={bl}\ndrain_net_per_s={dr}\ndrain_minutes={bl / dr / 60:.1f}')

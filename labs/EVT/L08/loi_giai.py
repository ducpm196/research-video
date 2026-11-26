import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
bl = (kv['in_r'] - kv['slow_p']) * kv['secs']; dr = bl / (kv['fast_p'] - kv['in_r'])
print(f'backlog_1h={bl}\ndrain_s={dr:.1f}')

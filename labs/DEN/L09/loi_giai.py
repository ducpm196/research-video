import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rep = kv['lag_s'] * kv['in_r']; catch = rep / (kv['proc_r'] - kv['in_r'])
print(f'replay_events={rep}\ncatchup_s={catch:.1f}')

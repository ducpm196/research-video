import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
a1 = kv['avail'] - kv['reserve']; a2 = a1 + kv['reserve']
print(f'after_reserve={a1}\nafter_compensate={a2}')

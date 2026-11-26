import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
empty, full = kv['cap'], 0
print(f'init_empty={empty} init_full={full}')
empty -= kv['p1']; full += kv['p1']
empty += kv['c1']; full -= kv['c1']
print(f'after_4p_1c=empty:{empty},full:{full}')
empty -= kv['p2']; full += kv['p2']
print(f'final_state=empty:{empty},full:{full}')

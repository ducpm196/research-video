import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
cap, n, per, sus = kv['cap'], kv['n_procs'], kv['per_proc'], kv['suspend']
d_all = n * per; d_after = (n - sus) * per
print(f'demand_4procs={d_all} thrashing={int(d_all > cap)}')
print(f'demand_after_suspend={d_after} thrashing={int(d_after > cap)}')
print(f'free_frames_after={cap - d_after}')

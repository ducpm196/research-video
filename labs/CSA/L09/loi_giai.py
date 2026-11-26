import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
k, n, st = kv['k'], kv['n'], kv['stalls']
no_p = k * n; id_p = k + n - 1
print(f'cycles_no_pipe={no_p}')
print(f'cycles_pipe_ideal={id_p} speedup={no_p / id_p:.2f}')
print(f'cycles_with_12_stalls={id_p + st}')

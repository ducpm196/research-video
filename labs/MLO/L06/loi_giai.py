import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
w = (kv['batch'] - 1) * (1000.0 / kv['arr_rps']); ts = 1000.0 / kv['single_ms']; tb = kv['batch'] * 1000.0 / kv['batch_ms']
print(f'first_wait_ms={w:.0f} single_rps={ts:.0f} batch_rps={tb:.0f}')

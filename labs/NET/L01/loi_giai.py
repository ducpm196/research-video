import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
tx = (kv['bytes'] * 8.0) / kv['bw_bps']
prop = kv['dist_m'] / kv['speed_mps']
print(f'tx_us={tx * 1e6:.1f}')
print(f'prop_ms={prop * 1e3:.1f}')
print(f'total_ms={(tx + prop) * 1e3:.2f}')

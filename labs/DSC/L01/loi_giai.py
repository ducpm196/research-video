import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
rc = kv['c1'] / kv['c2']; rk = (kv['c1'] + 273.15) / (kv['c2'] + 273.15)
print(f'celsius_fake={rc:.1f}x kelvin_real={rk:.3f}x')

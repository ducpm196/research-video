import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
v, rm, pb = float(kv['val']), float(kv['rmax']), int(kv['params_b'])
sc = rm / 127.0; q = round(v / sc); dq = q * sc
print(f'q={q} deq={dq:.4f} err={abs(dq - v):.4f}\nfp32_gb={pb * 4} int8_gb={pb}')

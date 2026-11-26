import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
zt = (kv['x'] - kv['m_tr']) / kv['std']; zs = (kv['x'] - kv['m_sv']) / kv['std']
print(f'z_train={zt:.1f} z_serve_skew={zs:.1f}')

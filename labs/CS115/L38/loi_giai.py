import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
xs = [float(v) for v in kv['xs'].split(',')]
sc = float(kv['scale'])
def kurt(v):
    m = sum(v) / len(v); xc = [x - m for x in v]
    v2 = sum(x * x for x in xc) / len(v)
    return (sum(x ** 4 for x in xc) / len(v)) / (v2 ** 2) - 3.0
k1 = kurt(xs); k2 = kurt([sc * x for x in xs])
print(f"kurt={k1:.4f} scaled_neg_kurt={k2:.4f}")
print(f"sign_scale_invariant={int(abs(k1 - k2) < 1e-9)}")

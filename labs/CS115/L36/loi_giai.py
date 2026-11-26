import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
alpha = 0.5 * math.log((1.0 - kv['eps']) / kv['eps'])
y, f, lr = kv['y'], kv['f0'], kv['lr']
for _ in range(int(kv['steps'])):
    f += lr * (y - f)
print(f"adaboost_alpha={alpha:.4f}")
print(f"gbdt_f2={f:.2f} rem={y - f:.2f}")

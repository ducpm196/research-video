import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
sig = lambda t: 1.0 / (1.0 + math.exp(-t))
s = sig(float(kv['sx'])); ds = s * (1.0 - s)
relus = [max(0.0, float(v)) for v in kv['arr'].split(',')]
xav = math.sqrt(2.0 / (int(kv['nin']) + int(kv['nout'])))
print(f"dsigmoid_10={ds:.6e}")
print(f"relu={relus}")
print(f"xavier_std={xav:.4f}")

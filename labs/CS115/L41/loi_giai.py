import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
d = float(kv['d'])
qkt = [float(x) / math.sqrt(d) for x in kv['qkt'].split(',')]
V = [float(x) for x in kv['v'].split(',')]
mx = max(qkt); exps = [math.exp(s - mx) for s in qkt]
w = [e / sum(exps) for e in exps]
out = sum(wi * vi for wi, vi in zip(w, V))
print(f"weights={[round(x, 4) for x in w]} sum={sum(w):.1f}")
print(f"attn_out={out:.4f}")

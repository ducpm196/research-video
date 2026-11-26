import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
ls = [float(x) for x in kv['logits'].split(',')]
def sm(t): ex = [math.exp(z / t) for z in ls]; s = sum(ex); return [v / s for v in ex]
r1, r2 = sm(1.0), sm(float(kv['t2'])); acc = 0.0; tp = float(kv['top_p'])
for v in sorted(r1, reverse=True):
    acc += v
    if acc >= tp: break
print(f'T1={[round(v, 3) for v in r1]} T06={[round(v, 3) for v in r2]} top_p_sum={acc:.3f}')

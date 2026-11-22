import math
def sm_raw(logits, t):
    exps = [math.exp(z / t) for z in logits]
    tot = sum(exps)
    return [v / tot for v in exps]
r1, r06 = sm_raw((3.0, 1.5, 0.0), 1.0), sm_raw((3.0, 1.5, 0.0), 0.6)
acc = 0.0
for v in sorted(r1, reverse=True):
    acc += v
    if acc >= 0.85:
        break
p1 = [round(v, 3) for v in r1]
p06 = [round(v, 3) for v in r06]
print(f"T1={p1} T06={p06} top_p_sum={acc:.3f}")

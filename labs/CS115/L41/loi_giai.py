import math
scores = [2.0 / math.sqrt(4.0), 0.0 / math.sqrt(4.0)]
exps = [math.exp(s) for s in scores]
w = [e / sum(exps) for e in exps]
out = w[0] * 10.0 + w[1] * 2.0
print(f"weights={[round(x, 4) for x in w]} sum={sum(w):.1f}")
print(f"attn_out={out:.4f}")

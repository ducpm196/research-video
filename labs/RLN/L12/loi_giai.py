import sys
s = sys.stdin.read().strip() or "256,1,1,1,1"
w = [float(x) for x in s.split(",")]
ess = (sum(w) ** 2) / sum(x * x for x in w)
w0 = int(w[0]) if w[0].is_integer() else w[0]
print(f"w8={w0} ESS={ess:.3f}")

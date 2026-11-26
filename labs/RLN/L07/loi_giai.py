import sys
s = sys.stdin.read().strip() or "0.5,8.0;-0.5,14.0|11.0"
ps, bs = s.split("|")
pairs = [tuple(map(float, x.split(","))) for x in ps.split(";")]
b = float(bs)
vals_raw = [gr * G for gr, G in pairs]
vals_bas = [gr * (G - b) for gr, G in pairs]
var = lambda xs: sum((x - sum(xs) / len(xs)) ** 2 for x in xs) / len(xs)
print(f"mean={sum(vals_raw) / len(vals_raw):.2f} raw_var={var(vals_raw):.2f} bas_var={var(vals_bas):.2f}")

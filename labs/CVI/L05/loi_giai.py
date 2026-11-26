import sys, math
s = sys.stdin.read().strip() or "4 0.99 0.6 0.4"
ss, ps, w1s, w2s = s.split()
sv, p, w1, w2 = int(ss), float(ps), float(w1s), float(w2s)
rn = lambda w: math.ceil(math.log(1 - p) / math.log(1 - w ** sv))
print(f"n_w60={rn(w1)} n_w40={rn(w2)}")

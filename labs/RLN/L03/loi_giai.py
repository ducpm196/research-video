import sys
s = sys.stdin.read().strip() or "8 0.2 0.0 2.0 2"
ks, es, q0s, rs, ns = s.split()
k, eps, q0, r, n = int(ks), float(es), float(q0s), float(rs), int(ns)
p_best = (1.0 - eps) + eps / k
p_other = eps / k
q_new = q0 + (r - q0) / n
print(f"p_best={p_best:.3f} p_other={p_other:.3f} q1={q_new:.1f}")

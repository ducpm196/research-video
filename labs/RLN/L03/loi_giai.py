k, eps = 8, 0.2
p_best = (1.0 - eps) + eps / k
p_other = eps / k
q_new = 0.0 + (2.0 - 0.0) / 2
print(f"p_best={p_best:.3f} p_other={p_other:.3f} q1={q_new:.1f}")

q, alpha, r, gamma, max_qn = 1.0, 0.25, 2.0, 0.8, 8.0
td_target = r + gamma * max_qn
q_new = q + alpha * (td_target - q)
print(f"target={td_target:.1f} td_err={td_target - q:.1f}")
print(f"q_new={q_new:.2f}")

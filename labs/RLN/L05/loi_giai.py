import sys
s = sys.stdin.read().strip() or "1.5 -1.0 0.9 0.2 6.0 2.0"
Q, r, g, a, mQ, Qsa = map(float, s.split())
ql = Q + a * (r + g * mQ - Q)
sarsa = Q + a * (r + g * Qsa - Q)
print(f"q_learning={ql:.2f} sarsa={sarsa:.2f}")

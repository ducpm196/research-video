import sys
s = sys.stdin.read().strip() or "1.0 1.0 49 0.0 0.1"
p0s, rs, ns, q1s, q2s = s.split()
P0, R, steps, q1, q2 = float(p0s), float(rs), int(ns), float(q1s), float(q2s)
def sim(Q):
    P = P0
    for _ in range(steps):
        P = P + Q
        K = P / (P + R)
        P = (1.0 - K) * P
    return P
print(f"P_after_49_Q0={sim(q1):.3f} P_after_49_Q01={sim(q2):.3f}")

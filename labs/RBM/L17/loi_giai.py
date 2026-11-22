def sim(Q):
    P, R = 1.0, 1.0
    for _ in range(49):
        P = P + Q
        K = P / (P + R)
        P = (1.0 - K) * P
    return P
print(f"P_after_49_Q0={sim(0.0):.3f} P_after_49_Q01={sim(0.1):.3f}")

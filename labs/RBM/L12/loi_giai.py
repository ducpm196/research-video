import sys
s = sys.stdin.read().strip() or "2.0 4.0 5.0 2.0"
x, P, z, R = map(float, s.split())
K = P / (P + R)
x_new = x + K * (z - x)
P_new = (1.0 - K) * P
print(f"K={K:.3f} x_est={x_new:.3f} P_est={P_new:.3f}")

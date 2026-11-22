x, P, z, R = 2.0, 4.0, 5.0, 2.0
K = P / (P + R)
x_new = x + K * (z - x)
P_new = (1.0 - K) * P
print(f"K={K:.3f} x_est={x_new:.3f} P_est={P_new:.3f}")

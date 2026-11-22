k = 3.0
ss_err_p = 1.0 / (1.0 + k)
y, integ, dt = 0.0, 0.0, 0.05
for _ in range(150):
    e = 1.0 - y
    integ += e * dt
    u = 1.2 * e + 1.5 * integ
    y += dt * (-y + u)
print(f"P_steady_err={ss_err_p:.4f} PI_final_err={abs(1.0 - y):.4f}")

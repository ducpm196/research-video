import sys
s = sys.stdin.read().strip() or "3.0 1.2 1.5 150"
ks, kps, kis, ns = s.split()
k, kp, ki, steps = float(ks), float(kps), float(kis), int(ns)
ss_err_p = 1.0 / (1.0 + k)
y, integ, dt = 0.0, 0.0, 0.05
for _ in range(steps):
    e = 1.0 - y
    integ += e * dt
    u = kp * e + ki * integ
    y += dt * (-y + u)
print(f"P_steady_err={ss_err_p:.4f} PI_final_err={abs(1.0 - y):.4f}")

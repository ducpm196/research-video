import math
x_e, x_r, h = 1.0, 1.0, 0.2
for _ in range(5):
    x_e += h * (-x_e)
    k1 = -x_r; k2 = -(x_r + 0.5*h*k1); k3 = -(x_r + 0.5*h*k2); k4 = -(x_r + h*k3)
    x_r += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
exact = math.exp(-1.0)
e_e, e_r = abs(x_e - exact), abs(x_r - exact)
print(f"err_euler={e_e:.4f} err_rk4={e_r:.2e} gain={e_e/e_r:.0f}x")

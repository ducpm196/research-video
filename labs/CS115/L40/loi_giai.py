sym = lambda a, b: a + b - a * b
w_near = sym(1.0, 1.0)
w_cross = sym(0.02, 0.0)
print(f"w_near_01={w_near:.2f} w_cross_12={w_cross:.4f}")
print(f"keeps_cluster={int(w_near > 10 * w_cross)}")

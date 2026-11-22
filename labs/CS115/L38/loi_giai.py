xs = [-1.5, -0.5, 0.5, 1.5]
kurt = lambda v: sum((x ** 4) for x in v) / len(v) / ((sum(x * x for x in v) / len(v)) ** 2) - 3.0
k1 = kurt(xs)
k2 = kurt([-2.0 * x for x in xs])
print(f"kurt={k1:.4f} scaled_neg_kurt={k2:.4f}")
print(f"sign_scale_invariant={int(abs(k1 - k2) < 1e-9)}")

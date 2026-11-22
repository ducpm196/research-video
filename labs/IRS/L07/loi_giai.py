p, q, r, eta = [1.5, 0.5], [1.0, 2.0], 4.0, 0.2
err = r - sum(a * b for a, b in zip(p, q))
p0 = [round(pi + eta * err * qi, 4) for pi, qi in zip(p, q)]
p_reg = [
    round(pi + eta * (err * qi - 0.05 * pi), 4) for pi, qi in zip(p, q)
]
print(f"err={err:.1f} p_raw={p0} p_reg={p_reg}")

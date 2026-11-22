vals_raw = [0.5 * 8.0, -0.5 * 14.0]
vals_bas = [0.5 * (8.0 - 11.0), -0.5 * (14.0 - 11.0)]
var = lambda xs: sum((x - sum(xs) / len(xs)) ** 2 for x in xs) / len(xs)
print(
    f"mean={sum(vals_raw) / 2:.2f} raw_var={var(vals_raw):.2f} "
    f"bas_var={var(vals_bas):.2f}"
)

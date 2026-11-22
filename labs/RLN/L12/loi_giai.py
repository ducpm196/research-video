w = [2 ** 8, 1, 1, 1, 1]
ess = (sum(w) ** 2) / sum(x * x for x in w)
print(f"w8={w[0]} ESS={ess:.3f}")

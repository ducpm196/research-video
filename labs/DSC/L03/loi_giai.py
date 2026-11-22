var = lambda xs: sum((x - sum(xs)/len(xs))**2 for x in xs) / (len(xs) - 1)
orig = [10.0, 20.0, 30.0, 40.0]
imp = orig + [25.0, 25.0]
print(f"orig_var={var(orig):.3f} mean_imputed_var={var(imp):.3f}")

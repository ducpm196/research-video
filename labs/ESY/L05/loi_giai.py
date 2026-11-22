y = 0.0
for _ in range(8): y += 0.25 * (1.0 - y)
print(f"y8={y:.4f} closed_form={1.0 - 0.75**8:.4f}")

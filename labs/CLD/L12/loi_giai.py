mins = 30 * 24 * 60
b1 = mins * (1.0 - 0.9995)
b2 = mins * (1.0 - 0.9999)
print(f'budget_9995_min={b1:.2f}')
print(f'budget_9999_min={b2:.2f}')

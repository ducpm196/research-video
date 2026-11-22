n = 25_000_000
l11, l4 = n * 1e-11, n * 1e-4
yrs = round(1.0 / l11)
print(f'loss_11nines={l11:.5f}')
print(f'loss_4nines={l4:.1f}')
print(f'years_per_loss={yrs}')

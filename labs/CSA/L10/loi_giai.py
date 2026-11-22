l2_amat = 10.0 + 0.20 * 100.0
tot = 1.0 + 0.05 * l2_amat
print(f'l2_amat_ns={l2_amat:.1f}')
print(f'total_amat_ns={tot:.2f}')
print(f'locality_speedup_vs_ram={100.0 / tot:.1f}')

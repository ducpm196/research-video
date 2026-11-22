calls = 2_500_000
g1 = round(calls * 0.160 * 0.5)
g2 = round(calls * 0.080 * 1.0)
print(f'gb_sec_512mb={g1}')
print(f'gb_sec_1gb={g2}')
print(f'same_gb_sec={int(g1 == g2)}')

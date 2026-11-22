out = (13 * 60 + 54) - (9 * 60 + 37)
bud = 525600 * 0.0001
growth = round(100_000_000_000_000 / 200_000_000_000)
print(f'outage_min={out}')
print(f'ratio_99_99={out / bud:.1f}x')
print(f'growth_2010_2021={growth}x')

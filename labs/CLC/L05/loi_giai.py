be = round(840 / 0.15)
pct = 100.0 * be / 8760
saved = round(8760 * 0.15 - 840)
print(f'breakeven_hours={be}')
print(f'breakeven_pct_year={pct:.1f}%')
print(f'full_year_saved_usd={saved}')

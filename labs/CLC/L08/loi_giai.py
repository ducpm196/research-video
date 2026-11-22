gb = 30 * 1024
cost = gb * 0.08
saved = cost * 0.75
print(f'egress_gb={gb}')
print(f'monthly_usd={cost:.2f}')
print(f'cdn_saved_usd={saved:.2f}')

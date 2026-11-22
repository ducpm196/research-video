page_b, rec_b, tiers = 8192, 128, 5
print(f'btree_wa={page_b / rec_b:.1f}x')
print(f'lsm_tiered_wa={float(tiers):.1f}x')

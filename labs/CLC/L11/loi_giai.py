av = 1.0 - (1.0 - 0.999) ** 2
bounds, db_az = (3, 12), 2
pillars = [
    'van_hanh', 'an_toan', 'tin_cay',
    'hieu_nang', 'chi_phi', 'ben_vung',
]
ok = int(db_az >= 2 and bounds[0] >= 2)
print(f'multi_az_avail={100 * av:.6f}%')
print(f'app_bounds={bounds[0]},{bounds[1]}')
print(f'spof_cleared={ok}')
print(f'pillars={len(pillars)}')

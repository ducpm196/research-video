eff = lambda h: h * 2.0 + (1.0 - h) * 80.0
l85, l98 = eff(0.85), eff(0.98)
print(f'lat_85pct_ms={l85:.2f}')
print(f'lat_98pct_ms={l98:.2f}')
print(f'speedup_98={80.0 / l98:.1f}x')

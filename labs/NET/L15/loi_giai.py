drop = 32000 // 40
bdp_mb = (10_000_000_000 * 100 // 1000) // (8 * 1_000_000)
bloat = (1000 * 1500 * 8) / 10_000_000
print(f'collapse_1986_drop={drop}x')
print(f'bdp_10g_100ms_MB={bdp_mb}')
print(f'bufferbloat_s={bloat:.1f} quic_iw_B={10 * 1200}')

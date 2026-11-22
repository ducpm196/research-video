bn = min(500, 100); bdp_b = bn * 1_000_000 * 50 // 1000
print(f'bottleneck_mbps={bn}')
print(f'bdp_bits={bdp_b}')
print(f'bdp_bytes={bdp_b // 8}')

import sys
s = sys.stdin.read().strip() or "5 80 1000000"
bph, hdr_b, full_b = map(int, s.split())
blocks_yr = bph * 24 * 365
hdr_mb = hdr_b * blocks_yr / 1e6
full_gb = full_b * blocks_yr / 1e9
ratio = full_b / hdr_b
print(f"blocks_yr={blocks_yr} header_MB={hdr_mb:.2f} full_GB={full_gb:.2f} ratio={ratio:.0f}x")

blocks_yr = 5 * 24 * 365
hdr_mb = 80 * blocks_yr / 1e6
full_gb = 1_000_000 * blocks_yr / 1e9
ratio = 1_000_000 / 80
print(f"blocks_yr={blocks_yr} header_MB={hdr_mb:.2f}",
      f"full_GB={full_gb:.2f} ratio={ratio:.0f}x")

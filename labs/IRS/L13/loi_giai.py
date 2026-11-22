import math
mem_mb = 2_000_000 * 128 * 4 / (1024 ** 2)
vpu = 18.0 / 1.5
print(
    f"emb_mib={mem_mb:.1f} views_u={vpu:.1f} "
    f"log_corr={-math.log(0.05):.3f}"
)

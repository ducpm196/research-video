b_frame = 1280 * 720 * 3
mib = b_frame / (1024 ** 2)
u = 96 / 255
lin96 = u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
print(f"bytes={b_frame} MiB={mib:.2f} linear_96={lin96:.3f}")

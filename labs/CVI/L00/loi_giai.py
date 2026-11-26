import sys
s = sys.stdin.read().strip() or "1280 720 3 96"
W, H, C, pv = map(int, s.split())
b_frame = W * H * C
mib = b_frame / (1024 ** 2)
u = pv / 255.0
lin = u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
print(f"bytes={b_frame} MiB={mib:.2f} linear_96={lin:.3f}")

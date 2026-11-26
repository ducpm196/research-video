import sys
s = sys.stdin.read().strip() or "120000000 60 1.7 31.8 401.2"
fr, fps, r0, h0, ag = map(float, s.split())
days = fr / fps / 86400.0
norm_b = (ag - r0) / (h0 - r0) * 100.0
print(f"days={days:.1f} breakout_norm={norm_b:.1f}%")

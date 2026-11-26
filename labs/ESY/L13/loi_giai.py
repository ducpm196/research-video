import sys
s = sys.stdin.read().strip() or "0.02 12.0 0.02 1200.0"
d_w, i_w, i_s, cap = map(float, s.split())
i_avg = d_w * i_w + (1.0 - d_w) * i_s
days = cap / i_avg / 24.0
print(f"avg_ma={i_avg:.4f} battery_days={days:.0f}")

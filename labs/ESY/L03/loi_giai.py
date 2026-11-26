import sys
s = sys.stdin.read().strip() or "16000000 8 999 250"
f_clk, presc, top, cmp_v = map(int, s.split())
freq = f_clk / (presc * (top + 1))
duty = cmp_v / (top + 1) * 100.0
print(f"pwm_hz={freq:.0f} duty_pct={duty:.1f}%")

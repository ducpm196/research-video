f_clk, presc, top, cmp_v = 16_000_000, 8, 999, 250
freq = f_clk / (presc * (top + 1))
duty = cmp_v / (top + 1) * 100.0
print(f"pwm_hz={freq:.0f} duty_pct={duty:.1f}%")

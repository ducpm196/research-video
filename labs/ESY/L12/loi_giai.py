wdt_ms = 90
wdt_resets = sum(1 for ms in (50, 75, 110, 60) if ms > wdt_ms)
stack = [0xA5] * 16
for i in range(11): stack[i] = i
used = 16 - sum(1 for v in stack if v == 0xA5)
print(f"wdt_resets={wdt_resets} stack_used_B={used}")

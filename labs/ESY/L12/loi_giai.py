import sys
s = sys.stdin.read().strip() or "90 16 11|50,75,110,60"
hdr, cy_s = s.split("|")
wdt_ms, stk_sz, depth = map(int, hdr.split())
cycles = [int(x) for x in cy_s.split(",")]
wdt_resets = sum(1 for ms in cycles if ms > wdt_ms)
stack = [0xA5] * stk_sz
for i in range(depth): stack[i] = i
used = stk_sz - sum(1 for v in stack if v == 0xA5)
print(f"wdt_resets={wdt_resets} stack_used_B={used}")

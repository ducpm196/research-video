import sys
s = sys.stdin.read().strip() or "40|5,11,3,2"
hz_s, cs = s.split("|")
budget = 1000.0 / float(hz_s)
used = sum(int(x) for x in cs.split(","))
print(f"budget_ms={budget:.0f} used_ms={used} margin_ms={budget - used:.0f}")

lo, hi = -(1 << 15), (1 << 15) - 1
val = 38000
wrap = ((val - lo) % (1 << 16)) + lo
sat = max(lo, min(hi, val))
print(f"wrap={wrap} saturate={sat} overflow={int(not lo <= val <= hi)}")

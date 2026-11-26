import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
b = kv['bits']; lo, hi = -(1 << (b - 1)), (1 << (b - 1)) - 1; val = kv['val']
wrap = ((val - lo) % (1 << b)) + lo; sat = max(lo, min(hi, val))
print(f'wrap={wrap} saturate={sat} overflow={int(not lo <= val <= hi)}')

import sys
s = sys.stdin.read().strip() or "1280 720 60 144"
W, H, f1, f2 = map(int, s.split())
px = W * H * f1
ms60, ms144 = 1000.0 / f1, 1000.0 / f2
print(f"px_60hz={px} ms60={ms60:.2f} ms144={ms144:.2f}")

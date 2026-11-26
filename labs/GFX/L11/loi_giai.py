import sys
s = sys.stdin.read().strip() or "1280 720 4"
W, H, od = map(int, s.split())
px = W * H
print(f"overdraw4={px * od} earlyZ={px} saved_pct={(1 - 1/od)*100:.1f}%")

import sys
s = sys.stdin.read().strip() or "2.0 0.85 6.0 5.0"
r, g, vn, v = map(float, s.split())
adv = r + g * vn - v
print(f"advantage={adv:.1f} increase_prob={int(adv > 0)}")

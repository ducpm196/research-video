import sys
s = sys.stdin.read().strip() or "600.0 0.15 3.0 9.0 1.0"
f, B, Z1, Z2, dh = map(float, s.split())
d1, d2 = f * B / Z1, f * B / Z2
e1 = f * B / (d1 - dh) - Z1
e2 = f * B / (d2 - dh) - Z2
print(f"Z3={Z1:.1f} err3={e1:.2f}m Z9={Z2:.1f} err9={e2:.2f}m")

import sys
s = sys.stdin.read().strip() or "0.8 5.0 600.0 320.0"
X, Z, fx, cx = map(float, s.split())
u = fx * (X / Z) + cx
print(f"u_px={u:.0f}")

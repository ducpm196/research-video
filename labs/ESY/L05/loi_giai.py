import sys
s = sys.stdin.read().strip() or "0.25 1.0 8"
as_, xs, ns = s.split()
alpha, x, steps = float(as_), float(xs), int(ns)
y = 0.0
for _ in range(steps): y += alpha * (x - y)
cf = x * (1.0 - (1.0 - alpha) ** steps)
print(f"y8={y:.4f} closed_form={cf:.4f}")

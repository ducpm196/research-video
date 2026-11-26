import sys
s = sys.stdin.read().strip() or "0.8 2.0"
g, ra = map(float, s.split())
va = ra / (1.0 - g * g)
vb = g * va
print(f"V_A={va:.3f} V_B={vb:.3f}")

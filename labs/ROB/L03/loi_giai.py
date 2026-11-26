import sys, math
s = sys.stdin.read().strip() or "3.0 0.2 3.2 3.6"
mu, sig, z1, z3 = map(float, s.split())
pdf = lambda z: math.exp(-0.5 * ((z - mu) / sig) ** 2) / (sig * math.sqrt(2 * math.pi))
d1, d3 = pdf(z1), pdf(z3)
print(f"pdf_32={d1:.3f} pdf_36={d3:.4f} ratio={d1/d3:.1f}x")

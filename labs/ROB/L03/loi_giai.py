import math
pdf = lambda z, mu=3.0, s=0.2: math.exp(-0.5*((z-mu)/s)**2) / (s*math.sqrt(2*math.pi))
d1, d3 = pdf(3.2), pdf(3.6)
print(f"pdf_32={d1:.3f} pdf_36={d3:.4f} ratio={d1/d3:.1f}x")

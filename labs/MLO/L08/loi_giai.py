import math
exp = [0.20, 0.30, 0.30, 0.20]
cur = [0.10, 0.20, 0.35, 0.35]
psi = sum((c - e) * math.log(c / e) for e, c in zip(exp, cur))
print(f"psi={psi:.3f} alert_moderate={int(0.1 <= psi < 0.25)}")

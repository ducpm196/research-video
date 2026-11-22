import math
p1, p2, n = 0.080, 0.095, 10000
d = (p2 - p1) * 100
se = math.sqrt(p1*(1-p1)/n + p2*(1-p2)/n) * 100
print(f"lift_pp={d:.1f} ci95=[{d-1.96*se:.1f}, {d+1.96*se:.1f}]")

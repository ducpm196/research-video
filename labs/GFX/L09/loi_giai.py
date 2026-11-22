import math
# t^2 - 14t + 45 = 0
b, c = -14.0, 45.0
disc = math.sqrt(b*b - 4.0*c)
t1, t2 = (-b - disc) / 2.0, (-b + disc) / 2.0
print(f"hits=({t1:.1f}, {t2:.1f}) nearest={min(t1, t2):.1f}")

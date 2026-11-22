import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    m = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return round(c - m, 3), round(c + m, 3)
print("A_3_3=", wilson(3, 3), "B_120_800=", wilson(120, 800))

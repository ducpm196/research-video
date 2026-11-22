import math
def attacker_p(q, z):
    p = 1.0 - q; lam = z * (q / p); s = 1.0
    for k in range(z + 1):
        pois = math.exp(-lam) * (lam ** k) / math.factorial(k)
        s -= pois * (1.0 - (q / p) ** (z - k))
    return s
print(f"p_q15_z6={attacker_p(0.15, 6):.5f} p_q25_z4={attacker_p(0.25, 4):.4f}")

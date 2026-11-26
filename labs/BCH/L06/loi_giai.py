import sys, math
s = sys.stdin.read().strip() or "0.15 6 0.25 4"
q1s, z1s, q2s, z2s = s.split()
def attacker_p(q, z):
    p = 1.0 - q; lam = z * (q / p); res = 1.0
    for k in range(z + 1):
        pois = math.exp(-lam) * (lam ** k) / math.factorial(k)
        res -= pois * (1.0 - (q / p) ** (z - k))
    return res
print(f"p_q15_z6={attacker_p(float(q1s), int(z1s)):.5f} p_q25_z4={attacker_p(float(q2s), int(z2s)):.4f}")

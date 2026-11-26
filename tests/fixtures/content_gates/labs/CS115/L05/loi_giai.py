import math


def tri_rieng(M):
    (a, b), (c, d) = M
    vet, dt = a + d, a * d - b * c
    delta = vet * vet - 4 * dt
    if delta < 0:
        return None
    r = math.isqrt(delta)
    assert r * r == delta
    return [(vet - r) // 2, (vet + r) // 2]


M = [[5, 2], [2, 2]]
(a, b), (c, d) = M
print("dinh thuc:", a * d - b * c)
print("vet:", a + d)
lams = tri_rieng(M)
print("tri rieng:", lams)
for lam in lams:
    g = math.gcd(b, lam - a)
    v = [b // g, (lam - a) // g]
    print(f"vector rieng cho {lam}: {v}")
    Mv = [a * v[0] + b * v[1], c * v[0] + d * v[1]]
    print(f"M.v = lambda.v (lambda={lam}):", Mv == [lam * v[0], lam * v[1]])
R = [[0, -2], [2, 0]]
if tri_rieng(R) is None:
    print("ma tran xoay: khong co tri rieng thuc")

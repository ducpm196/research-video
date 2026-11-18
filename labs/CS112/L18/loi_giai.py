COINS = (1, 4, 6)
A = 20
dp = [0] * (A + 1)
for a in range(1, A + 1):
    dp[a] = 1 + min(dp[a - c] for c in COINS if c <= a)
print("dp:", " ".join(map(str, dp[:13])))


def dung_lai(a):
    ra = []
    while a > 0:
        for c in COINS:
            if c <= a and 1 + dp[a - c] == dp[a]:
                ra.append(c)
                a -= c
                break
    return sorted(ra, reverse=True)


def tham_lam(a):
    n = 0
    for c in sorted(COINS, reverse=True):
        n += a // c
        a %= c
    return n


cach = dung_lai(8)
print(f"Doi 8: dp {len(cach)} dong ({' '.join(map(str, cach))}), tham lam {tham_lam(8)} dong")
sai = [a for a in range(1, A + 1) if tham_lam(a) > dp[a]]
print("Tham lam sai o a =", ", ".join(map(str, sai)))

dem_tho = 0


def f(a):
    global dem_tho
    dem_tho += 1
    if a == 0:
        return 0
    return 1 + min(f(a - c) for c in COINS if c <= a)


nho = {}
dem_nho = 0


def g(a):
    global dem_nho
    dem_nho += 1
    if a in nho:
        return nho[a]
    nho[a] = 0 if a == 0 else 1 + min(g(a - c) for c in COINS if c <= a)
    return nho[a]


assert f(20) == g(20) == dp[20]
print(f"Goi f(20): tho {dem_tho}, ghi nho {dem_nho}")

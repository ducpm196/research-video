p = (7, 4, 9, 5, 8, 3, 6)
n = len(p) - 1
m = [[0] * (n + 1) for _ in range(n + 1)]
cat = [[0] * (n + 1) for _ in range(n + 1)]
so_lan = 0
for do_dai in range(2, n + 1):
    for i in range(1, n - do_dai + 2):
        j = i + do_dai - 1
        m[i][j] = None
        for k in range(i, j):
            so_lan += 1
            c = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
            if m[i][j] is None or c < m[i][j]:
                m[i][j], cat[i][j] = c, k


def ngoac(i, j):
    if i == j:
        return f"A{i}"
    k = cat[i][j]
    return "(" + ngoac(i, k) + " " + ngoac(k + 1, j) + ")"


def moi_cach(i, j):
    """Mọi cách đặt ngoặc đoạn i..j: danh sách (số phép nhân, hàng, cột)."""
    if i == j:
        return [(0, p[i - 1], p[i])]
    ra = []
    for k in range(i, j):
        for tl, a, b in moi_cach(i, k):
            for tp, b2, c in moi_cach(k + 1, j):
                ra.append((tl + tp + a * b * c, a, c))
    return ra


tat_ca = moi_cach(1, n)
nho_nhat = min(c[0] for c in tat_ca)
print("So phep nhan it nhat:", m[1][n])
print("Dat ngoac:", ngoac(1, n))
print("So lan thu cho cat:", so_lan)
print(f"Vet can: {len(tat_ca)} cach, nho nhat {nho_nhat}")
print("Vet can = bang:", "CO" if nho_nhat == m[1][n] else "KHONG")

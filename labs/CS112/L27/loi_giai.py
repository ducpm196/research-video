P = (22, 9, 18, 24, 20, 16, 27, 13)


def bang(p):
    n = len(p) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    thu = 0
    for do_dai in range(2, n + 1):
        for i in range(1, n - do_dai + 2):
            j = i + do_dai - 1
            ung = []
            for k in range(i, j):
                thu += 1
                ung.append(m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j])
            m[i][j] = min(ung)
    return m[1][n], thu


def ghi_nho(p):
    nho = {}
    goi = [0]

    def f(i, j):
        goi[0] += 1
        if i == j:
            return 0
        if (i, j) not in nho:
            nho[(i, j)] = min(f(i, k) + f(k + 1, j) + p[i - 1] * p[k] * p[j] for k in range(i, j))
        return nho[(i, j)]
    return f(1, len(p) - 1), goi[0]


def vet_can(p):
    goi = [0]

    def f(i, j):
        goi[0] += 1
        if i == j:
            return 0
        return min(f(i, k) + f(k + 1, j) + p[i - 1] * p[k] * p[j] for k in range(i, j))
    return f(1, len(p) - 1), goi[0]


def tham_lam(p):
    def g(i, j):
        if i == j:
            return 0
        k = min(range(i, j), key=lambda k: (p[k], k))
        return g(i, k) + g(k + 1, j) + p[i - 1] * p[k] * p[j]
    return g(1, len(p) - 1)


b, thu = bang(P)
g, goi_g = ghi_nho(P)
v, goi_v = vet_can(P)
t = tham_lam(P)
print(f"Bang: {b}, {thu} lan thu cat")
print(f"Ghi nho: {g}, {goi_g} loi goi")
print(f"Vet can: {v}, {goi_v} loi goi")
print(f"Tham lam: {t}, lech {100 * (t - b) / b:.1f} % so voi toi uu")
print("Ba cach dung bang nhau:", "CO" if b == g == v else "KHONG")
print(f"Vet can khi n = 9: {vet_can((3, 4, 5, 6, 7, 8, 9, 10, 11, 12))[1]} loi goi")

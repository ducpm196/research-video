def F(n):
    if n == 1:
        return 0
    return 2 * F(n // 2) + 5


def Q(n):
    if n == 1:
        return 1
    return Q(n // 2) + 1


def tim(A, l, r, x, dem):
    dem[0] += 1
    if l > r:
        return -1
    m = (l + r) // 2
    if A[m] == x:
        return m
    if x < A[m]:
        return tim(A, l, m - 1, x, dem)
    return tim(A, m + 1, r, x, dem)


cac_n = [2 ** k for k in range(7)]
p = [F(n) for n in cac_n]
print("F(n) cho n = 1, 2, 4, ..., 64:", " ".join(map(str, p)))
dong = [5 * n - 5 for n in cac_n]
print("5n - 5 cho cac n do:", " ".join(map(str, dong)))
q = [Q(2 ** k) for k in range(11)]
print("Q(n) cho n = 1, 2, 4, ..., 1024:", " ".join(map(str, q)))
kq = []
for n in (100, 5000):
    dem = [0]
    tim(list(range(n)), 0, n - 1, n, dem)
    kq.append(dem[0])
    print(f"tim nhi phan, khoa thieu, n = {n}: {dem[0]} loi goi")
khop = p == dong and q == [k + 1 for k in range(11)] and kq == [8, 14]
print("khop: " + ("dung" if khop else "sai"))

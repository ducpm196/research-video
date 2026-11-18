def uoc_nho_nhat(v):
    d = 2
    while d < v:
        if v % d == 0:
            return d
        d = d + 1
    return v

BIEU_THUC = [
    lambda n: n * n + n + 17,
    lambda n: 2 * n * n + 29,
    lambda n: n * n - 79 * n + 1601,
]

for k, f in enumerate(BIEU_THUC, start=1):
    n = 0
    while uoc_nho_nhat(f(n)) == f(n):
        n = n + 1
    v = f(n)
    d = uoc_nho_nhat(v)
    print(str(k) + ': n=' + str(n) + ', ' + str(v) + ' = ' + str(d) + ' x ' + str(v // d))

import math


def T(n, a, b, f):
    # T(1) = 1; T(n) = a * T(n / b) + f(n), n là lũy thừa của b
    if n == 1:
        return 1
    return a * T(n // b, a, b, f) + f(n)


cac_cau = [
    ("4T(n/2)+n^2", 4, 2, lambda n: n * n, 1024, "TH2", lambda n: n * n * math.log2(n), "n^2 log2 n"),
    ("9T(n/3)+n", 9, 3, lambda n: n, 3 ** 9, "TH1", lambda n: n * n, "n^2"),
    ("T(n/2)+n", 1, 2, lambda n: n, 1024, "TH3", lambda n: n, "n"),
]
for ten, a, b, f, n, th, dap_an, ten_dap_an in cac_cau:
    ti_so = T(n, a, b, f) / dap_an(n)
    print(f"{ten}: {th}, T({n})/({ten_dap_an}) = {ti_so:.3f}")

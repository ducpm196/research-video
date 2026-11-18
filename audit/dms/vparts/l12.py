import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _der(n):
    # hệ thức truy hồi D(n) = (n-1)(D(n-1) + D(n-2)) — khác công thức bao hàm–loại trừ của lời giải
    a, b = 1, 0
    if n == 0:
        return 1
    for k in range(2, n + 1):
        a, b = b, (k - 1) * (a + b)
    return b


@lab("L12")
def _():
    # 1: đếm phần bù bằng phép chia lấy dư trên tập hợp; 2-3: truy hồi; 4: truy hồi Stirling 3^5 - ...; 5: φ bằng tích Euler
    div = [x for x in range(1, 1001) if x % 3 and x % 5 and x % 7]
    S = lambda n, k: sum((-1) ** j * math.comb(k, j) * (k - j) ** n for j in range(k + 1))
    onto = len({f for f in itertools.product(range(3), repeat=5) if set(f) == {0, 1, 2}})
    phi = 360
    for p in (2, 3, 5):
        phi = phi * (p - 1) // p
    return [f"khong chia het cho 3, 5, 7 tu 1 den 1000: {1000 - 333 - 200 - 142 + 66 + 47 + 28 - 9} {len(div)}",
            f"D7: {_der(7)} {_der(7)}", f"D9: {_der(9)} {_der(9)}",
            f"toan anh 5 phan tu len 3 phan tu: {S(5, 3)} {onto}",
            f"so nguyen to cung nhau voi 360 trong 1..360: {phi} {sum(1 for k in range(1, 361) if math.gcd(k, 360) == 1)}"]


@quymo("L12")
def _():
    brute = lambda n: sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))
    return [("265 và 14833 (đếm trực tiếp = truy hồi)", [brute(6), brute(8)] == [_der(6), _der(8)] == [265, 14833]),
            ("D20 = 895014631192902121 (truy hồi)", _der(20) == 895014631192902121),
            ("15! ≈ 22 phút, 20! ≈ 77 năm; tỉ lệ 0,368", round(math.factorial(15) / 1e9 / 60) == 22 and round(math.factorial(20) / 1e9 / 31557600) == 77 and round(_der(20) / math.factorial(20), 3) == 0.368)]

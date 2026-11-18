from itertools import permutations, product, combinations
from math import comb, factorial, gcd

def in_ra(mo_ta, ct, vet):
    print(mo_ta + ':', ct, vet)

def ihl(tong, uoc):
    # tong: số phần tử; uoc: các số nguyên tố; mỗi giao là bội chung -> tong // tích
    kq = tong
    for k in range(1, len(uoc) + 1):
        for nhom in combinations(uoc, k):
            tich = 1
            for u in nhom:
                tich = tich * u
            kq = kq + (-1) ** k * (tong // tich)
    return kq

def D(n):
    return sum((-1) ** k * comb(n, k) * factorial(n - k) for k in range(n + 1))

in_ra('khong chia het cho 3, 5, 7 tu 1 den 1000', ihl(1000, [3, 5, 7]), sum(1 for x in range(1, 1001) if x % 3 and x % 5 and x % 7))
for n in (7, 9):
    in_ra('D' + str(n), D(n), sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n))))
in_ra('toan anh 5 phan tu len 3 phan tu', 3 ** 5 - 3 * 2 ** 5 + 3 * 1 ** 5, sum(1 for f in product(range(3), repeat=5) if len(set(f)) == 3))
in_ra('so nguyen to cung nhau voi 360 trong 1..360', ihl(360, [2, 3, 5]), sum(1 for k in range(1, 361) if gcd(k, 360) == 1))

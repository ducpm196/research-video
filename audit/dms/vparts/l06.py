import math
import itertools
from collections import Counter
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L06")
def _():
    HAM = [({1: 'a', 2: 'b', 3: 'a', 4: 'c'}, {'a', 'b', 'c'}), ({1: 'a', 2: 'c', 3: 'd'}, {'a', 'b', 'c', 'd'}), ({1: 'x', 2: 'z', 3: 'y'}, {'x', 'y', 'z'}),
           ({1: 'p', 2: 'q', 3: 'p', 4: 'p', 5: 'q'}, {'p', 'q'}), ({1: 'a', 2: 'a', 3: 'b'}, {'a', 'b', 'c'})]
    out = []
    for i, (f, B) in enumerate(HAM, 1):
        # đơn ánh: không tồn tại hai khóa khác nhau cùng ảnh; toàn ánh: mỗi y ∈ B có tạo ảnh
        don = not any(f[a] == f[b] for a, b in itertools.combinations(f, 2))
        toan = all(any(f[a] == y for a in f) for y in B)
        out.append(f"f{i}: song anh" if don and toan else f"f{i}: {'don anh' if don else 'khong don anh'}, {'toan anh' if toan else 'khong toan anh'}")
    for k in (7, 6):
        n = math.comb(12, k)
        # đếm bù: chọn không có cặp tổng 13 = chọn tối đa một số mỗi cặp {i, 13−i}: Σ_j C(6, j)·2^j với j = k
        no_pair = math.comb(6, k) * 2 ** k
        out.append(f"chon {k} so tu 1 den 12: {n} cach, {n - no_pair} cach co cap tong 13")
    return out


@quymo("L06")
def _():
    m = 1000
    res = {}
    for n in (1000, 10000, 100000):
        c = Counter((k * 2654435761) % 2 ** 32 % m for k in range(n))
        res[n] = (max(c.values()), m - len(c))
    return [("1000 khoá: max 2, 271 ô trống", res[1000] == (2, 271)), ("10000: max 11", res[10000][0] == 11), ("100000: max 102", res[100000][0] == 102),
            ("cận dưới ⌈n/m⌉ = 1, 10, 100", [-(-n // m) for n in (1000, 10000, 100000)] == [1, 10, 100]),
            ("thực tế ≥ cận dưới (chuồng bồ câu)", all(res[n][0] >= -(-n // m) for n in res))]

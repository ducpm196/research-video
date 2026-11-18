import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L10")
def _():
    # tổ hợp bằng math.comb và bằng đếm tập con; đường đi bằng đếm chuỗi có đúng 3 chữ L trong 7 bước
    row = lambda n: [math.comb(n, k) for k in range(n + 1)]
    out = [f"C(12,5): {math.comb(12, 5)} {len(list(itertools.combinations(range(12), 5)))}",
           "hang 8 cua tam giac Pascal: " + " ".join(map(str, row(8))),
           f"tong hang 6: {sum(row(6))}"]
    people = ["m"] * 7 + ["f"] * 5
    atleast = sum(1 for idx in itertools.combinations(range(12), 3) if any(people[i] == "f" for i in idx))
    out.append(f"uy ban 3 nguoi, 7 nam 5 nu, it nhat 1 nu: {math.comb(12, 3) - math.comb(7, 3)} {atleast}")
    paths = sum(1 for s in itertools.product("RL", repeat=7) if s.count("L") == 3)
    out.append(f"duong di luoi 4 phai 3 len: {math.comb(7, 3)} {paths}")
    return out


@quymo("L10")
def _():
    pairs = lambda n: sum(1 for _ in itertools.combinations(range(n), 2))
    return [("28, 4950, 499500 cặp", [pairs(n) for n in (8, 100, 1000)] == [28, 4950, 499500] == [math.comb(n, 2) for n in (8, 100, 1000)]),
            ("10^4, 10^6, 10^8 → số cặp", [math.comb(n, 2) for n in (10 ** 4, 10 ** 6, 10 ** 8)] == [49995000, 499999500000, 4999999950000000]),
            ("0,05 giây; 8 phút; 58 ngày", round(49995000 / 1e9, 2) == 0.05 and round(499999500000 / 1e9 / 60) == 8 and round(4999999950000000 / 1e9 / 86400) == 58)]

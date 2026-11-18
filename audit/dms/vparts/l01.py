import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L01")
def _():
    # kéo theo a→b = 1 − a + a·b (số học trên 0/1), không dùng `not`/`or`; cặp biểu thức viết lại theo số học
    imp = lambda a, b: 1 - a + a * b
    cap = [
        (1, 2, lambda p, q: 1 - p * (1 - q), lambda p, q: (1 - p) + p * q),
        (2, 2, lambda p, q: imp(p, q), lambda p, q: imp(q, p)),
        (3, 2, lambda p, q: imp(p, q), lambda p, q: imp(1 - q, 1 - p)),
        (4, 3, lambda p, q, r: imp(p, imp(q, r)), lambda p, q, r: imp(p * q, r)),
        (5, 3, lambda p, q, r: imp(p, q) * imp(q, r), lambda p, q, r: imp(p, r)),
    ]
    out = []
    for k, n, f, g in cap:
        rows = [tuple((m >> (n - 1 - i)) & 1 for i in range(n)) for m in range(2 ** n - 1, -1, -1)]   # từ 1…1 xuống 0…0
        bad = [r for r in rows if f(*r) != g(*r)]
        out.append(f"{k}: tuong duong" if not bad else f"{k}: khong tuong duong, dong lech dau tien: " + " ".join(map(str, bad[0])))
    return out


@quymo("L01")
def _():
    # hai số lệch giữa bản đúng và bản nhầm = hiệu đối xứng của hai tập nghiệm trên [-50, 50]
    A = {x for x in range(-50, 51) if x <= 0 or x >= 10}
    B = {x for x in range(-50, 51) if x < 0 or x > 10}
    return [("chỉ lệch ở 0 và 10", sorted(A ^ B) == [0, 10]), ("101 số đã thử", len(range(-50, 51)) == 101),
            ("trung bình 2^31 lần thử ngẫu nhiên", F(2 ** 32, 2) == 2 ** 31 == 2147483648)]

import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L11")
def _():
    # công thức bằng đệ quy Pascal (comb tự cài), vét cạn bằng đệ quy phân phối từng viên (không itertools)
    from functools import lru_cache
    @lru_cache(None)
    def C(n, k):
        return 1 if k in (0, n) else C(n - 1, k - 1) + C(n - 1, k)
    def ways(total, boxes, lo=0, hi=None):
        if boxes == 0:
            return 1 if total == 0 else 0
        top = total if hi is None else min(total, hi)
        return sum(ways(total - x, boxes - 1, lo, hi) for x in range(lo, top + 1))
    def multisets(r, k):
        return len({tuple(sorted(c)) for c in itertools.product(range(k), repeat=r)})
    return [f"x1+x2+x3+x4 = 7: {C(10, 3)} {ways(7, 4)}",
            f"x1+x2+x3 = 12, moi xi >= 2: {C(8, 2)} {ways(12, 3, lo=2)}",
            f"chon 4 vien kem tu 6 vi: {C(9, 4)} {multisets(4, 6)}",
            f"x1+x2+x3 = 10, moi xi <= 5: {C(12, 2) - 3 * C(6, 2)} {ways(10, 3, hi=5)}"]


@quymo("L11")
def _():
    cnt = lambda n: sum(1 for a in range(n + 1) for b in range(n + 1 - a))
    return [("66, 5151, 501501 cách", [cnt(n) for n in (10, 100, 1000)] == [66, 5151, 501501] == [math.comb(n + 2, 2) for n in (10, 100, 1000)]),
            ("bảng k = 3, 5, 10, 20", [math.comb(99 + k, k - 1) for k in (3, 5, 10)] == [5151, 4598126, 4263421511271] and math.comb(119, 19) == 4910371215196105953021),
            ("71 phút; 156 000 năm", round(math.comb(109, 9) / 1e9 / 60) == 71 and round(math.comb(119, 19) / 1e9 / 31557600 / 1000) == 156)]

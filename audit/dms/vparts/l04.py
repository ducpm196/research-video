import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L04")
def _():
    # Σk² bằng Fraction và công thức đóng; quy nạp bằng hiệu S(n+1) − S(n)
    S = lambda n: sum(F(k) ** 2 for k in range(1, n + 1))
    C = lambda n: F(n * (n + 1) * (2 * n + 1), 6)
    W = lambda n: F(n * (n + 1) * (n + 2), 6)
    out = [f"co so: {int(S(1))} {int(C(1))}"]
    for n in range(1, 5):
        out.append(f"quy nap {n}->{n + 1}: {int(S(n))} + {(n + 1) ** 2} = {int(S(n) + (n + 1) ** 2)}, cong thuc {int(C(n + 1))}")
    out.append("kiem 1..1000: " + ("dung" if all(S(n) == C(n) for n in range(1, 1001)) else "sai"))
    n = next(n for n in itertools.count(1) if S(n) != W(n))
    out.append(f"cong thuc sai: co so dung, sai dau tien o n={n}")
    return out


@quymo("L04")
def _():
    import sys
    return [("tổng n số lẻ = n²", all(sum(2 * k - 1 for k in range(1, n + 1)) == n * n for n in (10, 1000))),
            ("n = 1 000 000 → 10^12", sum(2 * k - 1 for k in range(1, 10 ** 6 + 1)) == 10 ** 12),
            ("10^9 phép ≈ 1 giây; 10^18 phép ≈ 32 năm", 10 ** 9 / 1e9 == 1 and 31 < 10 ** 18 / 1e9 / 31557600 < 33)]

# RLN L11 — tính lại bằng tổng cấp số nhân dạng đóng (phân số chính xác) và đếm thẳng bằng range, khác `checks` (alg.rln_race mô phỏng
# từng bước với số thực).
from fractions import Fraction as F


def loop_closed(g, every=5, T=1000, rep=F(1)):  # số hạng đầu ở bước `every` (nhân g^(every−1)), công bội g^every, n = T // every số hạng
    n = T // every
    g = F(g)
    if g == 1:
        return 1 + (n - 1) * rep
    first = g ** (every - 1)
    return first + rep * first * g ** every * (1 - g ** (every * (n - 1))) / (1 - g ** every)


def finish(g, at=100, R=100):
    return F(g) ** (at - 1) * R


rec("L11a", finish(1) == 100 and loop_closed(1) == 200 == len(range(5, 1001, 5)) and alg.rln_boat("vong") == 200,
    "γ = 1: về đích 100, quay vòng 200 (đếm 5, 10, …, 1000)")
g99 = F(99, 100)
rec("L11b", round(float(finish(g99)), 2) == 36.97 and round(float(loop_closed(g99)), 2) == 19.6
    and abs(float(loop_closed(g99)) - alg.rln_race("vong", 0.99)) < 1e-9 and finish(g99) > loop_closed(g99),
    "γ = 0,99: về đích ≈ 36,97 > quay vòng ≈ 19,60 (dạng đóng, phân số)")
g9 = F(9, 10)
rec("L11c", round(float(finish(g9)), 4) == 0.003 and round(float(loop_closed(g9)), 2) == 1.6 and loop_closed(g9) > finish(g9),
    "γ = 0,9: về đích ≈ 0,003 < quay vòng ≈ 1,60")
rec("L11d", loop_closed(1, rep=F(7, 10)) == F(1403, 10) and loop_closed(1, rep=F(99, 199)) == 100
    and loop_closed(1, rep=F(2, 5)) < 100 < loop_closed(1, rep=F(1, 2)),
    "lỗi 2: phạt 0,3 → 140,3; ngưỡng hoà đúng 99/199 ≈ 0,4975")
rec("L11e", loop_closed(1, every=4) == 250 and loop_closed(1, every=4, rep=F(2, 5)) == F(1006, 10)
    and loop_closed(1, every=4, rep=F(0)) == 1,
    "câu đố: 250; vá 0,4 → 100,6 (vẫn hơn 100); chỉ thưởng lần đầu → 1")
rec("L11f", round(0.99 ** 4, 3) == 0.961 and round(1 - 0.99 ** 1000, 5) == 0.99996 and round(1 - 0.99 ** 5, 3) == 0.049
    and round(0.99 ** 99, 2) == 0.37 and 0.9 ** 99 < 0.00004,
    "tự kiểm: 0,961 · 0,99996 / 0,049; ôn nền: 0,99⁹⁹ ≈ 0,37, 0,9⁹⁹ ≈ 0,00003")

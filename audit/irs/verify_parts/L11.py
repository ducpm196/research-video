# IRS L11 — đa dạng (MMR), mức được nhìn thấy, vòng phản hồi: tính lại bằng CÁCH KHÁC checks (Fraction cho mọi điểm, cài lại phép chọn
# tham lam bằng vòng lặp riêng theo tên, sympy giải ngưỡng lambda, mô phỏng vòng phản hồi bằng lượt bấm ngẫu nhiên từng người).
import math
import random
from fractions import Fraction as F
import sympy as sp

rel = {"A": F(95, 100), "X": F(9, 10), "Y": F(7, 10), "Z": F(6, 10)}
sim = {frozenset("AX"): F(8, 10), frozenset("AY"): F(1, 10), frozenset("AZ"): F(2, 10),
       frozenset("XY"): F(1, 10), frozenset("XZ"): F(2, 10), frozenset("YZ"): F(3, 10)}


def pick(lam, k):
    chosen, trace = [], []
    while len(chosen) < k:
        sc = {d: lam * rel[d] - (1 - lam) * max([sim[frozenset(d + e)] for e in chosen], default=F(0)) for d in rel if d not in chosen}
        best = max(sc, key=lambda d: sc[d])
        trace.append(sc)
        chosen.append(best)
    return chosen, trace


L7 = F(7, 10)
ch, tr = pick(L7, 3)
names = "AXYZ"
S = [[1, .8, .1, .2], [.8, 1, .1, .2], [.1, .1, 1, .3], [.2, .2, .3, 1]]
R = [0.95, 0.9, 0.7, 0.6]
rec("L11a", ch == ["A", "Y", "X"] and [names[i] for i in alg.irs_mmr_select(R, S, 0.7, 3)] == ch
    and tr[0]["A"] == F(665, 1000) and tr[0]["X"] == F(63, 100)
    and (tr[1]["X"], tr[1]["Y"], tr[1]["Z"]) == (F(39, 100), F(46, 100), F(36, 100)) and (tr[2]["X"], tr[2]["Z"]) == (F(39, 100), F(33, 100)),
    "λ = 0,7: ô1 A 0,665; ô2 X 0,39 / Y 0,46 / Z 0,36; ô3 X 0,39 / Z 0,33 → A, Y, X")
rec("L11b", pick(F(1), 2)[0] == ["A", "X"] and pick(F(3, 10), 3)[0] == ["A", "Y", "Z"] and pick(F(8, 10), 3)[0] == ["A", "X", "Y"]
    and pick(F(3, 10), 3)[1][2]["X"] == F(-29, 100) and pick(F(3, 10), 3)[1][2]["Z"] == F(-3, 100)
    and rel["A"] + rel["X"] == F(185, 100) and rel["A"] + rel["Y"] == F(165, 100),
    "λ = 1 → A, X; λ = 0,3 → A, Y, Z (X −0,29, Z −0,03); λ = 0,8 → A, X, Y; tổng liên quan 1,85 / 1,65")
lam = sp.symbols("lam")
root = sp.solve(sp.Eq(sp.Rational(9, 10) * lam - sp.Rational(8, 10) * (1 - lam), sp.Rational(7, 10) * lam - sp.Rational(1, 10) * (1 - lam)), lam)
q8 = pick(F(8, 10), 2)[1][1]
rec("L11c", root == [sp.Rational(7, 9)] and round(7 / 9, 3) == 0.778 and (q8["X"], q8["Y"], q8["Z"]) == (F(56, 100), F(54, 100), F(44, 100))
    and pick(F(3, 4), 2)[1][1]["X"] == F(475, 1000) and pick(F(3, 4), 2)[1][1]["Y"] == F(1, 2),
    "ngưỡng λ = 7/9 ≈ 0,778 (sympy); λ = 0,8: 0,56 / 0,54 / 0,44; λ = 0,75: 0,475 / 0,5")
disc = [1 / math.log(i + 1, 2) for i in range(1, 5)]
rec("L11d", [round(d, 3) for d in disc] == [1.0, 0.631, 0.5, 0.431] and round(sum(disc), 3) == 2.562
    and round((disc[2] + disc[3]) / sum(disc) * 100, 1) == 36.3 == round(alg.irs_exposure([3, 4]) / alg.irs_exposure([1, 2, 3, 4]) * 100, 1)
    and round((disc[1] + disc[3]) / sum(disc) * 100, 1) == 41.4 and round(disc[1] + disc[3], 3) == 1.062,
    "mức được nhìn thấy vị trí 3, 4: 0,931 / 2,562 ≈ 36,3%; vị trí 2, 4: 41,4% (2 trên 4 ô = 50%)")


def loop(rates, day1, days, by, explore, seed):
    """Mô phỏng ngẫu nhiên từng lần hiện (lượt bấm thật tung đồng xu), cùng luật dồn lượt hiện như bài."""
    r = random.Random(seed)
    shows, hist, tot = list(day1), [tuple(day1)], [0, 0, 0, 0]
    for _ in range(days - 1):
        ca = sum(r.random() < rates[0] for _ in range(int(shows[0])))
        cb = sum(r.random() < rates[1] for _ in range(int(shows[1])))
        tot = [tot[0] + shows[0], tot[1] + ca, tot[2] + shows[1], tot[3] + cb]
        a_wins = ((tot[1] / tot[0] if tot[0] else 0) >= (tot[3] / tot[2] if tot[2] else 0)) if by == "rate" else ca >= cb
        win, ex = 1000 * (1 - explore), 1000 * explore / 2
        shows = [win + ex, ex] if a_wins else [ex, win + ex]
        hist.append(tuple(shows))
    return hist


h1 = loop((0.10, 0.12), (600, 400), 4, "clicks", 0, 1)
h2 = loop((0.10, 0.12), (1000, 0), 4, "rate", 0, 2)
h3 = [loop((0.10, 0.12), (1000, 0), 4, "rate", 0.1, s)[2] for s in range(200)]
rec("L11e", h1[1:] == [(1000, 0)] * 3 and h2[1:] == [(1000, 0)] * 3 and sum(x == (50, 950) for x in h3) > 120
    and alg.irs_feedback_loop((0.10, 0.12), (1000, 0), 4, 1000, explore=0.1, by="rate")[2] == (50.0, 950.0)
    and round(600 * 0.10) == 60 and round(400 * 0.12) == 48,
    f"vòng phản hồi (mô phỏng ngẫu nhiên): theo lượt bấm B mất mãi; theo tỉ lệ khi B chưa hiện: kẹt; cộng 10% khám phá: "
    f"{sum(x == (50, 950) for x in h3)}/200 lần chạy B thắng ngày 3 (kỳ vọng tất định của alg: thắng)")
rec("L11f", F(7, 10) * F(9, 10) == F(63, 100) and F(3, 10) * F(8, 10) == F(24, 100) and max(F(8, 10), F(1, 10)) == F(8, 10),
    "ôn: 0,63; 0,24; max 0,8")
# Thêm 2026-11-09 (đợt C): phần ôn nay giảng lôgarit cơ số 2 bằng ví dụ log₂ 4 = 2 → chiết khấu vị trí 3 = 1/2 (đếm số lần chia đôi).
halvings = 0
v = 4
while v > 1:
    v //= 2
    halvings += 1
rec("L11g", halvings == 2 and F(1, halvings) == F(1, 2) and round(1 / math.log2(3 + 1), 3) == 0.5,
    "ôn: log₂ 4 = 2 (chia đôi 2 lần) → chiết khấu vị trí 3 = 0,5")

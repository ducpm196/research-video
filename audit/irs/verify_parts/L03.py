# IRS L03 — tìm láng giềng theo cụm: tính lại bằng cách KHÁC `checks` (đếm phép so bằng cách THẬT SỰ đếm từng lần gọi hàm khoảng cách
# trên kho 12 điểm; dò mọi L nguyên để tìm cực tiểu; chạy lại mô phỏng 5000 điểm bằng mã viết khác — vòng theo tâm, heapq cho k láng
# giềng — với cùng hạt giống, rồi so với alg.irs_ivf_sim).
import heapq
import math
from fractions import Fraction as F

import numpy as np

P = [(0, 1), (1, 0), (2, 1), (1, 2), (3.5, 1), (6, 0), (8.5, 1), (6, 2), (2, 5), (3, 4), (4, 5), (3, 6)]
lab = [0] * 4 + [1] * 4 + [2] * 4
cent = [tuple(np.mean([P[i] for i in range(12) if lab[i] == c], axis=0)) for c in range(3)]
q = (3, 1)
calls = [0]


def dist(a, b):
    calls[0] += 1
    return (F(a[0]) - F(b[0])) ** 2 + (F(a[1]) - F(b[1])) ** 2


def ivf(m):
    calls[0] = 0
    dc = sorted(range(3), key=lambda c: dist(q, cent[c]))[:m]
    best = min((i for i in range(12) if lab[i] in dc), key=lambda i: dist(q, P[i]))
    return P[best], calls[0]


rec("L03a", cent == [(1, 1), (6, 1), (3, 5)] and [dist(q, c) for c in cent] == [4, 9, 16], "tâm (1,1), (6,1), (3,5); khoảng cách bình phương 4, 9, 16")
rec("L03b", ivf(1) == ((2, 1), 7) and ivf(2) == ((3.5, 1), 11) and min(P, key=lambda p: dist(q, p)) == (3.5, 1)
    and dist(q, (3.5, 1)) == F(1, 4), "m = 1: trả (2,1) sau 7 phép so — sót; m = 2: đúng sau 11; chính xác: (3,5; 1), 0,25")
rec("L03c", [dist(q, p) for p in P[:4]] == [9, 5, 1, 5] and [dist(q, p) for p in P[4:8]] == [F(1, 4), 10, F(121, 4), 10], "bảng cụm A và B")
cost = lambda n, L, m: L + m * n / L
rec("L03d", cost(10 ** 6, 1000, 10) == 11000 and round(10 ** 6 / 11000, 1) == 90.9 and cost(10 ** 6, 100, 10) == 100100
    and cost(10 ** 6, 10000, 10) == 11000, "11 000; ≈ 90,9 lần; L = 100 → 100 100; L = 10 000 → 11 000")
Lbest = min(range(1, 100001), key=lambda L: cost(10 ** 6, L, 10))
rec("L03e", Lbest in (3162, 3163) and round(cost(10 ** 6, 3162, 10)) == 6325 and min(range(1, 10001), key=lambda L: cost(10 ** 6, L, 1)) == 1000
    and cost(10 ** 6, 1000, 1) == 2000, "dò mọi L: cực tiểu ở L ≈ 3162 (m = 10) và L = 1000 (m = 1)")
rec("L03f", 10 ** 6 * 256 == 256 * 10 ** 6 and 256e6 / 1e9 == 0.256, "256 triệu phép nhân → 256 ms ở 1 tỉ phép/s")


def sim2(n=5000, d=8, L=70, probes=(1, 2, 4, 8), k=10, nq=50, seed=0, blobs=40, iters=15):
    rng = np.random.default_rng(seed)  # cùng thứ tự gọi bộ sinh như alg.irs_ivf_sim, mã tính khác
    C = rng.normal(0, 3, (blobs, d))
    X = C[rng.integers(0, blobs, n)] + rng.normal(0, 1, (n, d))
    Q = C[rng.integers(0, blobs, nq)] + rng.normal(0, 1, (nq, d))
    ce = X[rng.choice(n, L, replace=False)].copy()

    def assign():
        D = np.stack([((X - ce[j]) ** 2).sum(1) for j in range(L)], axis=1)
        return D.argmin(1)
    for _ in range(iters):
        a = assign()
        for j in range(L):
            mem = X[a == j]
            if len(mem):
                ce[j] = mem.mean(0)
    a = assign()
    lists = {j: [i for i in range(n) if a[i] == j] for j in range(L)}
    res = []
    for m in probes:
        tot_r = tot_c = 0
        for qq in Q:
            dall = ((X - qq) ** 2).sum(1)
            true = {i for _, i in heapq.nsmallest(k, ((dall[i], i) for i in range(n)))}
            dc = ((ce - qq) ** 2).sum(1)
            near = [j for _, j in heapq.nsmallest(m, ((dc[j], j) for j in range(L)))]
            cand = [i for j in near for i in lists[j]]
            found = {i for _, i in heapq.nsmallest(k, ((dall[i], i) for i in cand))}
            tot_r += len(true & found) / k
            tot_c += L + len(cand)
        res.append((m, round(tot_r / nq, 3), round(tot_c / nq)))
    return res


s2 = sim2()
rec("L03g", s2 == alg.irs_ivf_sim() == [(1, 0.804, 159), (2, 0.948, 231), (4, 1.0, 402), (8, 1.0, 776)],
    "mô phỏng viết lại cho cùng bảng: độ phủ 0,804; 0,948; 1; 1 — phép so 159, 231, 402, 776")
rec("L03h", round(70 + 5000 / 70) == 141 and round(5000 / 159) == 31 and round(math.sqrt(5000)) == 71,
    "công thức đều cụm 141; nhanh ≈ 31 lần; 70 ≈ căn 5000")
rec("L03i", 1000 + 9 * 1000 + 201000 == 211000 and round(211000 / 11000) == 19, "cụm phình: 211 000, chậm ≈ 19 lần")
rec("L03j", cost(4 * 10 ** 6, 2000, 1) == 4000 and cost(4 * 10 ** 6, 2000, 20) == 42000 and round(4e6 / 42000) == 95
    and min(m for m, r, c in s2 if r >= 0.95) == 4, "quiz: 4000; 42 000; ≈ 95 lần; m = 4")
rec("L03k", math.log2(10 ** 6) < 20 < math.log2(10 ** 6) + 0.1 and 2 ** 19 < 10 ** 6 < 2 ** 20, "lôgarit cơ số 2 của 1 triệu ≈ 20 (chia đôi ~20 lần còn 1)")


# Phần nền (sửa 2026-11-09, đợt C — bài tự đứng được): vector nhúng 2 chiều minh hoạ và K trung bình 1 chiều làm từng vòng.
# Tính lại bằng phân số chính xác (cosin bình phương để khỏi căn) và vòng K trung bình viết đầy đủ (gán → cập nhật → dừng khi không đổi).
def cos2(a, b):  # bình phương cosin, chính xác
    dot = sum(F(x) * y for x, y in zip(a, b))
    return dot * dot / (sum(F(x) ** 2 for x in a) * sum(F(y) ** 2 for y in b)), dot


q2, d1, d2 = (4, 3), (3, 4), (0, 5)
rec("L03l", cos2(q2, d1) == (F(24, 25) ** 2, 24) and cos2(q2, d2) == (F(3, 5) ** 2, 15) and dist(q2, d1) == 2 and dist(q2, d2) == 20,
    "nền: cosin(q, d1) = 24/25 = 0,96, cosin(q, d2) = 15/25 = 0,6; bình phương khoảng cách 2 và 20")


def kmeans1d(pts, cs):
    hist, lab_prev = [], None
    while True:
        lab1 = [min(range(len(cs)), key=lambda j: abs(F(p) - cs[j])) for p in pts]
        if lab1 == lab_prev:
            return hist
        hist.append((lab1, cs))
        cs = [sum(F(p) for p, l in zip(pts, lab1) if l == j) / lab1.count(j) for j in range(len(cs))]
        lab_prev = lab1


H = kmeans1d([1, 2, 4, 8, 9], [F(1), F(4)])
rec("L03m", len(H) == 2 and H[0][0] == [0, 0, 1, 1, 1] and H[1][1] == [F(3, 2), 7] and H[1][0] == [0, 0, 0, 1, 1]
    and round(float(F(7, 3)), 2) == 2.33, "nền K trung bình: vòng 1 gán {1,2}/{4,8,9} → tâm 1,5 và 7; vòng 2 điểm 4 đổi cụm → 7/3 ≈ 2,33 và 8,5; vòng 3 dừng")

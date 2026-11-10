# IRS L01 — nDCG: tính lại bằng cách KHÁC `checks` (sympy chính xác rồi mới đổi số thực; liệt kê MỌI hoán vị để xác nhận thứ tự lý
# tưởng là lớn nhất; numpy tích vô hướng giữa vector mức và vector chiết khấu), đối chiếu alg.irs_dcg / irs_ndcg / irs_dcg_jk.
import itertools
import numpy as np
import sympy as sp

disc = lambda n: np.array([1 / np.log2(i + 1) for i in range(1, n + 1)])
dcg_np = lambda g: float(np.dot(np.array(g, float), disc(len(g))))
dcg_sym = lambda g: sum(sp.Integer(y) / sp.log(i + 1, 2) for i, y in enumerate(g, 1))

X, ideal = [3, 2, 0, 1], [3, 2, 1, 0]
dX, dI = dcg_sym(X), dcg_sym(ideal)
rec("L01a", [round(float(x), 3) for x in disc(4)] == [1.0, 0.631, 0.5, 0.431]
    and round(float(dX), 4) == 4.6925 and round(float(dI), 4) == 4.7619 and abs(dcg_np(X) - alg.irs_dcg(X)) < 1e-12,
    "chiết khấu 1; 0,631; 0,5; 0,431 — DCG 4,6925, lý tưởng 4,7619")
nd = sp.N(dX / dI, 30)
rec("L01b", round(float(nd), 5) == 0.98544 and round(float(nd), 3) == 0.985 and round(4.693 / 4.762, 3) == 0.986,
    "nDCG = 0,98544 → 0,985; làm tròn trước khi chia cho 0,986 (lỗi đã gặp)")
best = max(itertools.permutations(X), key=dcg_np)
rec("L01c", list(best) == ideal and all(dcg_np(p) <= dcg_np(ideal) + 1e-12 for p in itertools.permutations(X)),
    "liệt kê 24 hoán vị: thứ tự giảm dần 3, 2, 1, 0 cho DCG lớn nhất")
rec("L01d", abs((dI - dX) - (1 / sp.log(4, 2) - 1 / sp.log(5, 2))) < 1e-15 and round(float(dI - dX), 4) == 0.0693,
    "đổi chỗ vị trí 3–4: chênh đúng bằng 0,5 − 0,4307 = 0,0693")
Y = [1, 0, 2, 3]
rec("L01e", round(dcg_np(Y), 3) == 3.292 and round(dcg_np(Y) / dcg_np(ideal), 3) == 0.691 and alg.irs_prec_at_k([1, 0, 1, 1], 4) == 0.75,
    "hệ Y: DCG 3,292, nDCG 0,691, cùng P@4 = 0,75")
# ví dụ của bài báo 2002 (dạng gốc b = 2) — dò từng bước theo định nghĩa đệ quy của bài báo
G = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
cg, dcg_rec = [], []
for i, g in enumerate(G, 1):
    cg.append((cg[-1] if cg else 0) + g)
    dcg_rec.append(cg[-1] if i < 2 else dcg_rec[-1] + g / np.log2(i))
rec("L01f", cg[:3] == [3, 5, 8] and [round(x, 2) for x in dcg_rec] == [3, 5, 6.89, 6.89, 6.89, 7.28, 7.99, 8.66, 9.61, 9.61]
    and abs(alg.irs_dcg_jk(G) - dcg_rec[-1]) < 1e-12, "bài báo 2002: CG 3, 5, 8; DCG 3, 5, 6,89, …, 9,61")
rec("L01g", round(1 / np.log2(1024), 3) == 0.1 and round(1 / 1024, 3) == 0.001, "vị trí 1024: chia lôgarit còn 0,1; chia vị trí còn 0,001")
# văn bản mức 3 hệ không trả: lý tưởng 3, 3, 2, 1
rec("L01h", round(dcg_np([3, 3, 2, 1]), 3) == 6.323 and round(dcg_np(X) / dcg_np([3, 3, 2, 1]), 3) == 0.742
    and round(alg.irs_ndcg(X, judged=[3, 3, 2, 1, 0]), 3) == 0.742, "thứ tự lý tưởng từ mọi văn bản đã chấm: 0,742")
jk = lambda g: g[0] + sum(y / np.log2(i) for i, y in enumerate(g[1:], 2))
expg = lambda g: dcg_np([2 ** y - 1 for y in g])
rec("L01i", jk(X) == 5.5 and round(jk(X) / jk(ideal), 3) == 0.977 and round(expg(X) / expg(ideal), 3) == 0.993,
    "ba công thức: 0,985; 0,977; 0,993")
rec("L01j", round((0.985 + 0.691) / 2, 3) == 0.838 and round((0.985 + 0.691 + 0) / 3, 3) == 0.559, "câu hỏi không có văn bản đúng: 0,838 hay 0,559")
Z = [2, 3, 0, 0]
rec("L01k", round(dcg_np(Z), 3) == 3.893 and round(dcg_np(Z) / dcg_np(ideal), 3) == 0.817
    and round(dcg_np(Z[:2]) / dcg_np(ideal[:2]), 3) == 0.913 and dcg_np(X[:2]) == dcg_np(ideal[:2]) and round(dcg_np([3, 2]), 3) == 4.262,
    "quiz: Z 3,893 → 0,817; ở 2 dòng X = 1, Z 0,913")
# sửa 2026-11-09: số hiện 5 chữ số (sympy chính xác) để phép cộng/trừ trên màn hình khớp tới chữ số cuối
r5 = lambda e: round(float(sp.N(e, 30)), 5)
rec("L01l", [r5(2 / sp.log(3, 2)), r5(1 / sp.log(5, 2)), r5(dX), r5(dI), r5(dI - dX)] == [1.26186, 0.43068, 4.69254, 4.76186, 0.06932]
    and round(1.26186 + 0.43068 + 3, 5) == 4.69254 and round(4.76186 - 4.69254, 5) == 0.06932,
    "1,26186; 0,43068; DCG 4,69254; lý tưởng 4,76186; chênh 0,06932")
dZ = dcg_sym(Z)
rec("L01m", r5(dZ) == 3.89279 and round(float(dZ / dI), 3) == 0.817 and round(3.893 / 4.762, 3) == 0.818,
    "quiz: 3,89279 / 4,76186 → 0,817; chia số đã làm tròn 3,893 / 4,762 → 0,818 (lệch)")
# ôn lôgarit cơ số 2 (sửa 2026-11-09): đếm số lần nhân đôi từ 1
doublings = lambda x: next(n for n in range(64) if 2 ** n == x)
rec("L01n", doublings(8) == 3 and doublings(1) == 0 and doublings(1024) == 10 and round(2 ** 1.585, 3) == 3.0
    and round(float(sp.N(sp.log(5, 2) - 2)), 3) == 0.322, "log₂ 8 = 3, log₂ 1 = 0, log₂ 1024 = 10; 2^1,585 ≈ 3; 4 → 5 thêm 0,322")

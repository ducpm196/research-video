# IRS L04 — hợp nhất thứ hạng nghịch đảo: tính lại bằng cách KHÁC `checks` (phân số chính xác Fraction, dò hạng bằng list.index thay vì
# vòng enumerate của alg.irs_rrf, so sánh đại số triệt tiêu số hạng chung), đối chiếu alg.irs_rrf / alg.irs_ndcg.
from fractions import Fraction as F
import math

kw, vec = list("ABCD"), list("BEAC")


def rrf_exact(lists, k=60):
    docs = sorted({d for l in lists for d in l})
    return {d: sum((F(1, k + l.index(d) + 1) for l in lists if d in l), F(0)) for d in docs}


S = rrf_exact([kw, vec])
order = sorted(S, key=lambda d: -S[d])
alg_s = alg.irs_rrf([kw, vec])
rec("L04a", order == ["B", "A", "C", "E", "D"] and all(abs(float(S[d]) - alg_s[d]) < 1e-15 for d in S),
    "thứ tự B, A, C, E, D; khớp alg.irs_rrf")
rec("L04b", S["A"] == F(1, 61) + F(1, 63) and round(float(S["A"]), 5) == 0.03227 and round(float(S["B"]), 5) == 0.03252
    and round(float(S["C"]), 5) == 0.0315 and S["E"] == F(1, 62) and S["D"] == F(1, 64) and float(S["D"]) == 0.015625,
    "A 0,03227; B 0,03252; C 0,03150; E 1/62; D = 0,015625")
rec("L04c", S["B"] - S["A"] == F(1, 62) - F(1, 63) == F(1, 3906) and round(float(F(1, 3906)), 6) == 0.000256,
    "B − A = 1/62 − 1/63 = 1/3906 ≈ 0,000256 > 0")
rec("L04d", F(1, 61) / F(1, 62) == F(62, 61) and round(62 / 61, 4) == 1.0164 and F(1, 1) / F(1, 2) == 2,
    "k = 60: hạng 1 nặng hơn hạng 2 khoảng 1,6%; k = 0: gấp đôi")
raw = {"A": 12.4 + 0.79, "B": 11.9 + 0.83, "C": 6.0 + 0.70, "D": 5.5, "E": 0.81}
rec("L04e", sorted(raw, key=lambda d: -raw[d]) == kw + ["E"] and round(raw["A"], 2) == 13.19,
    "cộng thẳng: thứ tự trùng hẳn danh sách từ khoá, E cuối")
S0, S60 = rrf_exact([["X", "Y"], ["Z", "Y"]], k=0), rrf_exact([["X", "Y"], ["Z", "Y"]])
rec("L04f", S0 == {"X": 1, "Y": 1, "Z": 1} and S60["Y"] == F(2, 62) and round(float(S60["Y"]), 4) == 0.0323 and round(float(S60["X"]), 4) == 0.0164,
    "k = 0: X, Y, Z hoà 1; k = 60: Y 0,0323, X 0,0164")
rel = {"A": 2, "B": 3, "C": 1, "D": 0, "E": 2}
ideal = sorted(rel.values(), reverse=True)[:4]
dcg = lambda g: sum(y / math.log2(i + 1) for i, y in enumerate(g, 1))
nd = lambda L: dcg([rel[d] for d in L]) / dcg(ideal)
rec("L04g", round(nd(kw), 3) == 0.772 and abs(nd(vec) - 1) < 1e-12 and round(nd(order[:4]), 3) == 0.988
    and round(alg.irs_ndcg([rel[d] for d in order[:4]], k=4, judged=list(rel.values())), 3) == 0.988, "nDCG@4: từ khoá 0,772; vector 1; bản ghép 0,988")
rec("L04h", round(float(F(2, 65)), 4) == 0.0308 and F(2, 65) > S["E"] > S["D"], "hạng 5 ở cả hai danh sách: 2/65 ≈ 0,0308 > E > D")
Q = rrf_exact([list("PQR"), list("RSQ")])
rec("L04i", sorted(Q, key=lambda d: -Q[d]) == ["R", "Q", "P", "S"] and round(float(Q["R"]), 5) == 0.03227 and round(float(Q["Q"]), 5) == 0.032
    and round(float(Q["P"]), 5) == 0.01639 and round(float(Q["S"]), 5) == 0.01613, "quiz: R 0,03227 > Q 0,03200 > P 0,01639 > S 0,01613")
rawq = {"P": 14, "Q": 9 + 0.8, "R": 8 + 0.9, "S": 0.85}
rec("L04j", max(rawq, key=rawq.get) == "P" and round(rawq["Q"], 1) == 9.8 and round(rawq["R"], 1) == 8.9, "quiz: cộng thẳng đưa P lên đầu")
# Phần nền (sửa 2026-11-09, đợt C — bài tự đứng được): công thức xếp hạng có bão hoà làm từng bước theo Robertson & Zaragoza 2009
# (độ hiếm dạng cộng 1 trong lôgarit cho luôn dương, như alg.bm25_idf), tính lại bằng tay từng phần rồi so alg.bm25; cosin bằng sympy.
import sympy as sp
docs = [["mèo", "đen", "mèo"], ["chó", "đen"], ["mèo", "trắng", "chó", "con"]]
avg = sp.Rational(sum(map(len, docs)), len(docs))
idf = math.log(1 + (3 - 2 + 0.5) / (2 + 0.5))
Kh = [sp.Rational(12, 10) * (1 - sp.Rational(3, 4) + sp.Rational(3, 4) * len(d) / avg) for d in docs]
tfp = [sp.Rational(d.count("mèo")) * sp.Rational(22, 10) / (d.count("mèo") + Kh[i]) for i, d in enumerate(docs)]
sc = [idf * float(t) for t in tfp]
rec("L04k", avg == 3 and Kh[0] == sp.Rational(6, 5) and Kh[2] == sp.Rational(3, 2) and tfp[0] == sp.Rational(11, 8) and tfp[2] == sp.Rational(22, 25)
    and round(idf, 3) == 0.47 and [round(x, 3) for x in sc] == [0.646, 0.0, 0.414]
    and all(abs(a - b) < 1e-12 for a, b in zip(sc, alg.bm25(["mèo"], docs))),
    "nền: độ hiếm ln 1,6 ≈ 0,470; K = 1,2 / 1,5; phần tần suất 11/8 = 1,375 và 22/25 = 0,88; điểm 0,646 / 0 / 0,414 (khớp alg.bm25)")
sat = [sp.Rational(f) * sp.Rational(22, 10) / (f + sp.Rational(6, 5)) for f in (1, 2, 10)]
rec("L04l", sat[0] == 1 and sat[1] == sp.Rational(11, 8) and round(float(sat[2]), 3) == 1.964
    and sp.limit(sp.Symbol("f") * sp.Rational(22, 10) / (sp.Symbol("f") + sp.Rational(6, 5)), sp.Symbol("f"), sp.oo) == sp.Rational(11, 5),
    "bão hoà: f = 1, 2, 10 → 1; 1,375; 1,964; giới hạn k1 + 1 = 2,2")
cz = sp.Rational(8) / (sp.sqrt(5) * sp.sqrt(14))
rec("L04m", round(float(cz), 3) == 0.956 and round(float(sp.sqrt(5)), 3) == 2.236 and round(float(sp.sqrt(14)), 3) == 3.742,
    "nền cosin: 8 / (√5 · √14) ≈ 0,956")

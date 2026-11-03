# IRS L00 — độ chuẩn xác, độ phủ, hạng nghịch đảo: tính lại bằng cách KHÁC `checks` (tập hợp mã văn bản thay vì danh sách 0/1,
# phân số chính xác, mô phỏng người dùng đọc từ trên xuống), rồi đối chiếu hàm alg.irs_*.
from fractions import Fraction as F

# Hệ A đúng ở 1, 3, 6; hệ B ở 4, 5, 6; kho có 5 văn bản đúng (2 văn bản hệ không trả về). Mã văn bản: d1…d10 là kết quả, g1…g5 là văn bản đúng.
gold = {"g1", "g2", "g3", "g4", "g5"}
A = ["g1", "x2", "g2", "x4", "x5", "g3", "x7", "x8", "x9", "x10"]
B = ["x1", "x2", "x3", "g1", "g2", "g3", "x7", "x8", "x9", "x10"]


def p_at(ranked, k):
    return F(len(set(ranked[:k]) & gold), k)


def r_at(ranked, k, T=gold):
    return F(len(set(ranked[:k]) & T), len(T))


def rr_read(ranked):  # người dùng đọc từng dòng tới khi gặp văn bản đúng
    for pos in range(1, len(ranked) + 1):
        if ranked[pos - 1] in gold:
            return F(1, pos)
    return F(0)


bin_of = lambda ranked: [1 if d in gold else 0 for d in ranked]
rec("L00a", p_at(A, 10) == p_at(B, 10) == F(3, 10) and p_at(A, 5) == p_at(B, 5) == F(2, 5)
    and alg.irs_prec_at_k(bin_of(A), 5) == float(p_at(A, 5)), "P@10 = 0,3 cả hai; P@5 = 0,4 cả hai")
rec("L00b", p_at(A, 3) == F(2, 3) and p_at(B, 3) == 0 and round(float(F(2, 3)), 3) == 0.667, "P@3: A 0,667, B 0")
rec("L00c", r_at(A, 5) == r_at(B, 5) == F(2, 5) and r_at(A, 10) == r_at(B, 10) == F(3, 5)
    and alg.irs_recall_at_k(bin_of(A), 10, 5) == 0.6, "R@5 0,4; R@10 0,6 (T = 5)")
rec("L00d", rr_read(A) == 1 and rr_read(B) == F(1, 4) and alg.irs_rr(bin_of(B)) == 0.25, "RR: A 1, B 0,25")
mrr = (F(1) + F(1, 3) + F(0)) / 3
rec("L00e", mrr == F(4, 9) and round(float(mrr), 3) == 0.444 and abs(alg.irs_mrr([[1], [0, 0, 1], [0] * 10]) - 4 / 9) < 1e-12,
    "MRR = 4/9 ≈ 0,444")
# bảng dò mọi k: độ phủ không giảm, độ chuẩn xác lên xuống
Ps = [p_at(A, k) for k in range(1, 11)]
Rs = [r_at(A, k) for k in range(1, 11)]
rec("L00f", [round(float(x), 2) for x in Ps] == [1.0, 0.5, 0.67, 0.5, 0.4, 0.5, 0.43, 0.38, 0.33, 0.3]
    and [float(x) for x in Rs] == [0.2, 0.2, 0.4, 0.4, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6]
    and all(Rs[i] <= Rs[i + 1] for i in range(9)) and any(Ps[i] < Ps[i + 1] for i in range(9)),
    "bảng P@k, R@k của hệ A; R@k không giảm, P@k có lúc tăng")
rec("L00g", p_at(A, 5) * 5 == r_at(A, 5) * 5 == 2 and p_at(A, 10) * 10 == r_at(A, 10) * 5 == 3, "nhân ngược về số đúng 2 và 3")
# TREC-7 (CITED JK02): 50 câu hỏi, 528 000 văn bản, 1000 kết quả mỗi câu
rec("L00h", 50 * 528000 == 26400000 and 50 * 1000 == 50000 and 26400000 // 50000 == 528, "26,4 triệu cặp, gấp 528 lần 50 000")
# lỗi 3: bỏ câu hỏi RR = 0; lỗi 4: T = số đúng chính hệ tìm được
rec("L00i", (F(1) + F(1, 3)) / 2 == F(2, 3) and round(2 / 3, 3) == 0.667 and r_at(A, 10, T={"g1", "g2", "g3"}) == 1,
    "bỏ câu hỏng: 0,667; T = 3 → độ phủ giả 1")
# quiz: hệ C đúng ở 2 và 7, kho 4 văn bản đúng
gold_C = {"g1", "g2", "g3", "g4"}
C = ["x1", "g1", "x3", "x4", "x5", "x6", "g2", "x8", "x9", "x10"]
pC5 = F(len(set(C[:5]) & gold_C), 5)
rC5 = F(len(set(C[:5]) & gold_C), 4)
rrC = next(F(1, i + 1) for i, d in enumerate(C) if d in gold_C)
rec("L00j", pC5 == F(1, 5) and rC5 == F(1, 4) and rrC == F(1, 2) and F(len(set(C[:3]) & gold_C), 3) == F(1, 3) and p_at(A, 3) == F(2, 3),
    "quiz: P@5 0,2; R@5 0,25; RR 0,5; P@3 A 0,667 > C 0,333")

# IRS L13 — hành trình gợi ý video: con số CITED đối chiếu với câu trích trong audit/irs/sources_L13.md (đọc tệp, tìm chuỗi), con số
# tính lại bằng cách KHÁC `checks` (Fraction, chuỗi lôgarit, đếm từng phút, đếm lượt mô phỏng), đối chiếu alg.* khi có.
from fractions import Fraction as F
import math
from pathlib import Path

src = (Path(alg.__file__).resolve().parents[1] / "audit" / "irs" / "sources_L13.md").read_text(encoding="utf-8")
cited = ["over 45,000,000 videos", "seven hours of video being uploaded every minute", "approximately 1.1 million users and 1.3 million videos, with approximately 12.5 million watches",
         "approximately 5.4 million users", "nearly 29 million total views", "first 46 days", "roughly 8.4% precision at 3.2% recall",
         "more than a billion users", "several thousand negatives are sampled, corresponding to more than 100 times speedup",
         "1M videos and 1M search tokens were embedded with 256 floats", "dramatic 4.1%", "34.6%", "1.9 billion monthly active users",
         "Input Feature −0.07%", "Shallow Tower +0.24%", "10% feature drop-out", "MMoE (8 Experts): +0.45% / +3.07%", "6.1M", "3.7M",
         "90%, 5%, 5%", "ViewTime by 0.07%", "drop of 0.52%", "cap c = 3", "0.85%", "every 50 steps, then we have p = 0.02",
         "approximately 10M videos", "more than 90% of training examples", "+0.37%", "+0.20%", "tens of millions of videos", "tens of milliseconds",
         # thêm 2026-11-09 (đợt C): so sánh 4,1% với 0,2% (bớt lũy thừa đặc trưng); lọc người có mặt ở cả hai giai đoạn
         "increased loss by 0.2%", "nearly 29 million total views"]
miss = [c for c in cited if c not in src]
rec("L13a", not miss, "mọi con số CITED dạy trong bài có trong câu trích nguyên văn" + (f" — THIẾU: {miss}" if miss else ""))
minutes_per_day = sum(1 for _ in range(24 * 60))
rec("L13b", 7 * minutes_per_day == 10080 and 7 * 1440 == 10080, "7 giờ mỗi phút × 1440 phút = 10 080 giờ mỗi ngày")
rec("L13c", round(float(F(125, 11)), 1) == 11.4 and round(float(F(290, 54)), 1) == 5.4 and round(1.1e6 * 0.084) == 92400,
    "12,5/1,1 ≈ 11,4; 29/5,4 ≈ 5,4; 8,4% của 1,1 triệu = 92 400")
rec("L13d", sum(256 * 4 for _ in range(1000)) * 1000 == 1024000000 and 10 ** 6 // 5000 == 200,
    "bảng vector 1 024 000 000 byte; 5000 mẫu âm → 200 lần ít số hạng")
# Sửa 2026-11-08 (đọc kiểm đợt B): [CO16] chỉ ghi “increased the watch time-weighted loss by a dramatic 4.1%” (và “increased loss by 0.2%”
#   ngay trước đó), không nói là tương đối hay điểm phần trăm → bỏ phép tính 34,6 · 1,041 ≈ 36,0 (không có nguồn); chỉ kiểm rằng 4,1 lớn hơn
#   hẳn mức chênh giữa các cấu hình mạng ở Bảng 1 (34,7% − 34,6% = 0,1).
# Sửa 2026-11-09 (đợt C): bài từng nói “đổi cỡ mạng chỉ làm mất mát chênh nhau cỡ vài phần mười” — SAI với Bảng 1 [CO16]
#   (41,6% không lớp ẩn → 34,6%, chênh 7 điểm; đọc lại PDF bằng pdftotext 2026-11-09). Bài nay so 4,1% với 0,2% (bớt lũy thừa của đặc
#   trưng số, cùng cấu hình 1024→512→256, cùng đoạn của bài báo): 4,1 / 0,2 = 20,5 → “khoảng 20 lần”.
table1 = [F(416, 10), F(369, 10), F(367, 10), F(358, 10), F(352, 10), F(347, 10), F(346, 10)]
rec("L13e", table1[0] - table1[-1] == 7 and min(table1) == F(346, 10) and round(float(F(41, 10) / F(2, 10))) == 20
    and F(24, 100) - F(-7, 100) == F(31, 100) and round(6.1 / 3.7, 2) == 1.65,
    "Bảng 1 CO16: 41,6 → 34,6 (chênh 7 điểm, không phải ‘vài phần mười’); 4,1% / 0,2% ≈ 20; 0,24 − (−0,07) = 0,31; 6,1/3,7 ≈ 1,65")
# Thêm 2026-11-09 (đợt C, bài tự đứng): thử nghiệm hai nhóm (minh hoạ) — chia ngẫu nhiên làm tỉ lệ người xem nhiều như nhau ở hai nhóm;
#   thay đổi tương đối (50,12 − 50) / 50 = 0,24%; tích vô hướng (3, 2)·(1, 4) = 11; 1414 ≈ √(2 triệu).
import random
rg = random.Random(11)
heavy = [rg.random() < 0.3 for _ in range(200000)]
grp = [rg.random() < 0.5 for _ in range(200000)]
share = [sum(h for h, g in zip(heavy, grp) if g == side) / sum(1 for g in grp if g == side) for side in (True, False)]
rec("L13k", all(abs(s - 0.3) < 0.005 for s in share) and (F(5012, 100) - 50) / 50 == F(24, 10000)
    and sum(a * b for a, b in zip((3, 2), (1, 4))) == 11 and math.isqrt(2 * 10 ** 6) == 1414 and F(51, 1002) == F(50 + 1, 1000 + 2),
    f"chia ngẫu nhiên: người xem nhiều {share[0]:.3f} / {share[1]:.3f} ở hai nhóm; +0,24% tương đối; tích vô hướng 11; √2e6 ≈ 1414")
rec("L13f", 90 + 5 == 95 and F(5, 100) * 1000 == 50 and min(F(5, 100) / F(1, 100), 3) == 3 and min(F(5, 100) / F(1, 100), 5) == 5,
    "nhóm 90/5/5: hai mô hình cùng 95% dữ liệu; trọng số 5 cắt ở 3")
ln = lambda x: 2 * sum((((x - 1) / (x + 1)) ** (2 * k + 1)) / (2 * k + 1) for k in range(3000))  # chuỗi artanh
rec("L13g", round(ln(50), 3) == 3.912 and abs(ln(50) + math.log(0.02)) < 1e-9 and round(2 + ln(50), 3) == 5.912 and round(2 + ln(2), 3) == 2.693,
    "−ln 0,02 = ln 50 ≈ 3,912 (chuỗi); 5,912 và 2,693")
rec("L13h", round(math.log(2) + 2 * math.log(5), 3) == 3.912 and 1000 * 10 // 100 == 100, "ln 2 + 2 ln 5 = 3,912; ẩn vị trí 10% → 100 trên 1000")
rec("L13i", 20000 * 64 == 1280000 and 1280000 / 1e9 * 1000 == 1.28 and 2 * 10 ** 6 * 64 / 1e9 * 1000 == 128
    and round(alg.irs_ivf_cost(2 * 10 ** 6, 1414, 10)) == round(1414 + 10 * 2e6 / 1414) == 15558,
    "quiz: 1,28 ms; 128 ms; chia cụm 1414 cụm, xét 10 → ≈ 15 558 phép so")
rec("L13j", round(51 / 1002, 4) == 0.0509 and round(100 ** 0.75, 1) == 31.6 and 10 + 1000 * 0.05 + 20 == 80, "ôn: 0,0509; 31,6; 80 ms")

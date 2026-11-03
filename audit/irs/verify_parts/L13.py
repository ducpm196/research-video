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
         "approximately 10M videos", "more than 90% of training examples", "+0.37%", "+0.20%", "tens of millions of videos", "tens of milliseconds"]
miss = [c for c in cited if c not in src]
rec("L13a", not miss, "mọi con số CITED dạy trong bài có trong câu trích nguyên văn" + (f" — THIẾU: {miss}" if miss else ""))
minutes_per_day = sum(1 for _ in range(24 * 60))
rec("L13b", 7 * minutes_per_day == 10080 and 7 * 1440 == 10080, "7 giờ mỗi phút × 1440 phút = 10 080 giờ mỗi ngày")
rec("L13c", round(float(F(125, 11)), 1) == 11.4 and round(float(F(290, 54)), 1) == 5.4 and round(1.1e6 * 0.084) == 92400,
    "12,5/1,1 ≈ 11,4; 29/5,4 ≈ 5,4; 8,4% của 1,1 triệu = 92 400")
rec("L13d", sum(256 * 4 for _ in range(1000)) * 1000 == 1024000000 and 10 ** 6 // 5000 == 200,
    "bảng vector 1 024 000 000 byte; 5000 mẫu âm → 200 lần ít số hạng")
rec("L13e", round(34.6 * (1 + 0.041), 1) == 36.0 and F(24, 100) - F(-7, 100) == F(31, 100) and round(6.1 / 3.7, 2) == 1.65,
    "34,6% → ≈ 36,0%; 0,24 − (−0,07) = 0,31; 6,1/3,7 ≈ 1,65")
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

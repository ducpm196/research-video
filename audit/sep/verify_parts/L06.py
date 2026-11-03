# SEP L06 — tính lại bằng phân số chính xác và cộng dồn từng giờ (khác `checks`: nhân số thực trực tiếp).
from fractions import Fraction as F

dev = sum(F(4, 10) for _ in range(8))              # cộng công suất từng thiết bị
hourly = sum(dev for _ in range(720))              # cộng dồn từng giờ
total = hourly * F(12, 10)
rec("L06a", dev == F(16, 5) and hourly == 2304 and total == F(27648, 10) and total * F(1, 2) == F(13824, 10),
    "8 × 0,4 = 3,2 kW; 720 giờ cộng dồn = 2304 kWh; × 1,2 = 2764,8; × 0,5 = 1382,4 kg")
rec("L06b", F(2304) / total == F(5, 6) and round(float(F(2304) / total) * 100) == 83 and total - 2304 == F(4608, 10)
    and round(float((total - 2304) / total) * 100) == 17, "tách phần: 2304/2764,8 = 5/6 ≈ 83%; 460,8 kWh ≈ 17%")
rec("L06c", sum(dev * 24 for _ in range(30)) == 2304 and [round(float(total * F(c, 1000))) for c in (429, 201, 545)] == [1186, 556, 1507]
    and round(float(F(545, 201)), 1) == 2.7, "theo ngày 76,8 × 30; khí thải 1186 / 556 / 1507 kg; 0,545/0,201 ≈ 2,7")
rec("L06d", round(float(F(2304) * F(158, 100)), 1) == 3640.3 and total / 10 == F(27648, 100) and 10 * 365 == 3650
    and min(d for d in range(1, 1000) if 10 * d >= total) == 277, "PUE 1,58 → 3640,3; phục vụ 10 kWh/ngày bằng huấn luyện sau 276,48 ngày (ngày thứ 277 vượt)")
q = sum(F(3, 10) for _ in range(16)) * 240 * F(15, 10)
rec("L06e", q == 1728 and q * F(4, 10) == F(6912, 10) and sum(F(3, 10) for _ in range(16)) * 240 * F(11, 10) == F(12672, 10)
    and q - F(12672, 10) == F(4608, 10) and F(4608, 10) * F(4, 10) == F(18432, 100), "quiz: 1728 kWh; 691,2 kg; PUE 1,1 → 1267,2; tiết kiệm 460,8 kWh ≈ 184,32 kg")
rec("L06f", F(1) * F(5, 10) * 2 * F(15, 10) == F(3, 2) and F(3, 2) * F(4, 10) == F(6, 10) and F(100) * F(12, 10) == 120,
    "làm thử: 1 × 0,5 × 2 × 1,5 = 1,5 kWh → 0,6 kg; 100 × 1,2 = 120")

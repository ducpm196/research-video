# CAS L01 — Patriot. Tính lại bằng đường KHÁC `checks`: Fraction chính xác + chuỗi bit sinh bằng phép nhân đôi, thay số thực.
from fractions import Fraction as F

tenth = F(1, 10)
bits, x = [], tenth                     # nhân đôi phần lẻ — đúng cách bài dạy
for _ in range(23):
    x *= 2
    bits.append(int(x))
    x -= int(x)
kept = sum(F(b, 2 ** (i + 1)) for i, b in enumerate(bits))
err = tenth - kept
rec("L01a", "".join(map(str, bits)) == "00011001100110011001100" and kept == F(838860, 2 ** 23), "23 bit phần lẻ của 0,1 = 0,00011001100110011001100 = 838 860 / 2^23")
rec("L01b", err == F(4, 5 * 2 ** 23) and abs(float(err) - 9.5367e-8) < 1e-12, "sai mỗi nhịp = 0,8 / 2^23 ≈ 9,54e-8 s")
gao = {1: "0.0034", 8: "0.0275", 20: "0.0687", 48: "0.1648", 72: "0.2472", 100: "0.3433"}   # Phụ lục II, cột Inaccuracy
rec("L01c", all(f"{float(err * 36000 * h):.4f}" == v for h, v in gao.items()), "mô hình 23 bit khớp cả 6 hàng cột sai số")
err24 = tenth - F(int(tenth * 2 ** 24), 2 ** 24)
rec("L01d", f"{float(err24 * 3_600_000):.4f}" == "0.1287", "mô hình 24 bit: 100 h chỉ 0,1287 s — không khớp (bị loại)")
calc = {1: "3599.9966", 8: "28799.9725", 20: "71999.9313", 48: "172799.8352", 72: "259199.7528", 100: "359999.6667"}  # cột Calculated Time
ok5 = all(f"{3600 * h - float(F(gao[h])):.4f}" == calc[h] for h in (1, 8, 20, 48, 72))
rec("L01e", ok5 and f"{360000 - 0.3433:.4f}" == "359999.6567" != calc[100], "cột thời gian tính ra: 5 hàng khớp, hàng 100 h bảng in lệch một chữ số")
meters = {8: 55, 20: 137, 48: 330, 72: 494, 100: 687}
rec("L01f", all(1990 < m / float(F(gao[h])) < 2010 for h, m in meters.items()), "mét / giây ≈ 2000 ở mọi hàng ≥ 8 h: tỉ lệ thuận")
rec("L01g", F(8) * 50 / 20 == 20 and F(100, 20) == 5, "lệch 20% sau 8 h, ngưỡng 50% → 20 h; 100 h gấp 5")
q = F(1, 100) - F(655, 2 ** 16)
rec("L01h", int(F(1, 100) * 2 ** 16) == 655 and round(float(q) * 1e6, 2) == 5.49 and round(float(q * 360000), 2) == 1.98
    and round(float(1 / q) / 6000) == 30 and round(2 ** 32 / 8_640_000) == 497, "quiz: 5,49 µs mỗi nhịp; 1 h → 1,98 s; ≈ 30 phút; 2^32 nhịp ≈ 497 ngày")

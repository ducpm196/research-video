# CAS L02 — Ariane 501. Tính lại bằng đường KHÁC `checks`: bù 2 dựng tay từ các bit (không dùng numpy), liệt kê phạm vi, phép cộng mốc giờ.


def to_int16_wrap(v):                     # giữ 16 bit cuối rồi đọc bit dấu, làm tay từng bit
    bits = [(v >> k) & 1 for k in range(16)]
    return sum(b << k for k, b in enumerate(bits[:15])) - bits[15] * (1 << 15)


rng = [to_int16_wrap(u) for u in range(1 << 16)]
rec("L02a", (min(rng), max(rng), len(set(rng))) == (-32768, 32767, 65536), "16 bit có dấu: −32 768 … 32 767, đủ 65 536 giá trị")
rec("L02b", to_int16_wrap(32768) == -32768 and to_int16_wrap(40000) == -25536 and to_int16_wrap(50000) == -15536,
    "quay vòng: 32 768 → −32 768; 40 000 → −25 536; 50 000 → −15 536 (số minh hoạ)")
sat = lambda v: -32768 if v < -32768 else 32767 if v > 32767 else v
rec("L02c", sat(40000) == 32767 and sat(-50000) == -32768 and sat(20000) == 20000, "bão hoà kẹp về biên; 20 000 giữ nguyên")
flight_mode, window, liftoff, fail = -3, 50, 36.7 - 30, 36.7      # [IB96]: chế độ bay H0−3 s, căn chỉnh 50 s; hỏng H0+36,7 ≈ 30 s sau cất cánh
rec("L02d", flight_mode + window == 47 and round(47 - liftoff) == 40 and round(fail - liftoff, 1) == 30.0,
    "căn chỉnh dừng ở H0+47 s; ≈ 40 s sau cất cánh (cất cánh ≈ H0+7 s); hỏng ≈ 30 s sau cất cánh")
rec("L02e", 7 - 4 == 3 and round(100 * 3 / 7) == 43, "7 biến có rủi ro, 4 được bảo vệ → 3 không bảo vệ ≈ 43%")
rec("L02f", "{:016b}".format(40000) == "1001110001000000" and "{:016b}".format(32767) == "0" + "1" * 15, "mẫu bit 40 000 bắt đầu bằng 1; 32 767 = 0 rồi 15 chữ 1")
p = 0.1
rec("L02g", abs(p * p - 0.01) < 1e-12, "hai bộ độc lập 10% → 1%; cùng phần mềm → cùng hỏng")

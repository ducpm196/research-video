# PAR L11 — huấn luyện phân tán: mô phỏng sự kiện theo từng tầng (gradient tầng cuối có trước, đường mạng gửi lần lượt), đếm số ví dụ
# xử lý trong 13 giây, chạy SGD thật cho quy tắc nhân (khác `checks`: công thức C / (C + G − O) của alg.par_step_efficiency).
from fractions import Fraction as F


def step_time(fwd, bwd_layers, comm_layers, overlap=True):
    """fwd: ms lan truyền xuôi; bwd_layers: ms ngược của từng tầng (theo thứ tự tầng CUỐI trước); comm_layers: ms gộp gradient từng tầng.
    overlap: gradient tầng nào xong thì gửi ngay (đường bận thì xếp hàng); không overlap: chờ hết lan truyền ngược."""
    t, link, ends = fwd, 0.0, []
    ready = []
    for b in bwd_layers:
        t += b; ready.append(t)
    compute_end = t
    for r, c in zip(ready, comm_layers):
        start = max(link, r if overlap else compute_end)
        link = start + c
    return max(compute_end, link)


# 100 ms tính (xuôi 33,3; ngược 66,7 chia 3 tầng), 30 ms gộp chia 3 tầng; chỉ gradient của 2 tầng cuối gửi sớm được 20 ms
no = step_time(100 / 3, [200 / 9] * 3, [10, 10, 10], overlap=False)
yes = step_time(100 / 3, [200 / 9] * 3, [10, 10, 10], overlap=True)
rec("L11a", abs(no - 130) < 1e-9 and round(100 / no * 100, 1) == 76.9 and round(8 * 100 / no, 2) == 6.15,
    f"mô phỏng sự kiện, không chồng: bước {no:.1f} ms → 76,9%, gấp 6,15")
# trường hợp chồng: tầng cuối xong lúc 55,6 ms; gộp 3 tầng nối nhau trên đường mạng
rec("L11b", round(yes, 1) == 110.0 and round(100 / yes * 100, 1) == 90.9 and round(8 * 100 / yes, 2) == 7.27,
    f"mô phỏng sự kiện, gửi ngay khi có: bước {yes:.1f} ms (20 ms gộp giấu trong lúc tính) → 90,9%, gấp 7,27")
ex1 = sum(32 for _ in range(int(14300 // 100)))           # 1 thẻ trong 14,3 s (bội chung của 100, 130, 110 ms)
ex8 = sum(8 * 32 for _ in range(int(14300 // 130)))       # 8 thẻ không chồng
ex8o = sum(8 * 32 for _ in range(int(14300 // 110)))      # 8 thẻ chồng
rec("L11c", ex1 == 4576 and ex8 == 28160 and round(ex8 / ex1, 2) == 6.15 and round(ex8o / ex1, 2) == 7.27 and round(256 / 0.11) == 2327 and round(256 / 0.13) == 1969,
    f"đếm ví dụ trong 14,3 s (bội chung của 100, 130, 110 ms): {ex1}, {ex8}, {ex8o} → 6,15 và 7,27; 1969 và 2327 ví dụ/giây")
D = F(150 * 10 ** 6 * 4, 10 ** 9)
rec("L11d", D == F(3, 5) and 2 * F(7, 8) * D == F(21, 20) and F(21, 20) / 35 * 1000 == 30,
    "150 triệu × 4 byte = 0,6 GB; vòng 8 thẻ 1,05 GB; chia 35 GB/s = 30 ms (phân số chính xác)")
w_small = F(1)
for _ in range(4):
    w_small -= F(1, 10) * 2
w_big = F(1) - F(4, 10) * 2
rec("L11e", w_small == w_big == F(1, 5) and F(1) - F(1, 10) * 2 == F(4, 5) and F(1, 10) * F(1024, 256) == F(2, 5) and F(1, 10) * F(512, 256) == F(1, 5),
    "SGD thật: 4 bước nhỏ η = 0,1 và 1 bước η = 0,4 cùng ra 0,2; ôn nền 0,8; η = 0,4 (lô 1024), 0,2 (lô 512)")
rec("L11f", round(24.84 - 23.60, 2) == 1.24 and round(23.74 - 23.60, 2) == 0.14 and round(100 / 130 * 8 / 1.1, 2) == 5.59 and F(256, 32) == 8,
    "lỗi 2: số của [GO17] 24,84 / 23,60 / 23,74; lỗi 3: 5,59; lỗi 4: gấp 8")
G16 = 2 * F(15, 16) * F(3, 5) / 35 * 1000
rec("L11g", round(float(G16), 1) == 32.1 and round(120 / (120 + float(G16)) * 100, 1) == 78.9 and max(G16 - 40, 0) == 0
    and 2 * F(15, 16) * F(3, 5) / 10 * 1000 == F(225, 2) and round(120 / (120 + 112.5 - 40) * 100, 1) == 62.3,
    "quiz: G ≈ 32,1 ms, 78,9% không chồng, giấu hết khi chồng 40; mạng 10 GB/s: 112,5 ms, 62,3%")

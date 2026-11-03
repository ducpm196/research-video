# CAS L08 — GitLab 31/1/2017. Đường KHÁC `checks`: datetime qua nửa đêm; Fraction cho tỉ số; đổi đơn vị bằng bit → byte từng bước;
# mô phỏng chép theo từng giây (đếm số giây cần) thay phép chia.
import datetime as dt
from fractions import Fraction as F

D = lambda d, hm: dt.datetime(2017, *d, *map(int, hm.split(":")))
mins = lambda a, b: int((b - a).total_seconds() // 60)
wipe = D((1, 31), "23:30")
rec("L08a", mins(D((1, 31), "17:20"), wipe) == 370 and divmod(370, 60) == (6, 10), "mất dữ liệu 17:20 → 23:30 = 6 giờ 10 phút")
rec("L08b", mins(D((1, 31), "01:00"), wipe) == 1350 and divmod(1350, 60) == (22, 30), "bản tự động 01:00 → 22 giờ 30 phút (“gần 24 giờ”)")
rec("L08c", round(float(F(1350, 370)), 1) == 3.6, "bản chụp tay: mất ít hơn ≈ 3,6 lần")
rec("L08d", divmod(mins(wipe, D((2, 1), "18:00")), 60) == (18, 30), "ngừng 23:30 → 18:00 hôm sau = 18 giờ 30 phút")
bytes_per_s = 60 * 10 ** 6 // 8
rec("L08e", bytes_per_s == 7_500_000 and bytes_per_s * 18 * 3600 == 486 * 10 ** 9, "60 Mbit/s × 18 giờ = 486 GB (ước lượng của bài)")
rec("L08f", 4 - 3 == 1 and 5000 + 5000 + 700 == 10700, "4 cách, 3 không dùng được; 5000 / 5000 / 700")


def secs(size_bytes, rate_bytes):              # mô phỏng thô: đếm số giây (bước 1 triệu byte) — chỉ để đối chiếu phép chia
    t, left = 0, size_bytes
    while left > 0:
        left -= rate_bytes
        t += 1
    return t


rec("L08g", round(secs(200 * 10 ** 9, 7_500_000) / 3600, 1) == 7.4, "quiz: 200 GB ở 60 Mbit/s ≈ 7,4 giờ")
rec("L08h", secs(200 * 10 ** 9, 125 * 10 ** 6) == 1600 and round(1600 / 60, 1) == 26.7, "quiz: 200 GB ở 1 Gbit/s = 1600 s ≈ 26,7 phút")

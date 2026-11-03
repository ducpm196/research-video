# CAS L11 — năm 2038. Tính lại bằng đường KHÁC `checks`: numpy ép kiểu int32/uint32 thật, đếm từng ngày bằng lịch datetime.date
# (không qua phép chia giây), và đối chiếu với ngày giờ nguồn ghi ([MDB] 2038-01-19 03:14:07 / 2106-02-07 06:28:15, [EXT4] 1901-12-13, May 2446).
import datetime as dt

import numpy as np

E = dt.datetime(1970, 1, 1)
top = int(np.iinfo(np.int32).max)
wrap = int((np.array([top], dtype=np.int64) + 1).astype(np.int32)[0])       # ép thô về 32 bit có dấu: quay vòng
rec("L11a", top == 2147483647 and E + dt.timedelta(seconds=top) == dt.datetime(2038, 1, 19, 3, 14, 7), "int32 lớn nhất → 2038-01-19 03:14:07 (khớp MariaDB trước 11.5)")
rec("L11b", wrap == -2 ** 31 and E + dt.timedelta(seconds=wrap) == dt.datetime(1901, 12, 13, 20, 45, 52), "cộng 1 → −2³¹ → 1901-12-13 20:45:52 (khớp ext4 “1901-12-13”)")
u = int(np.iinfo(np.uint32).max)
rec("L11c", E + dt.timedelta(seconds=u) == dt.datetime(2106, 2, 7, 6, 28, 15), "uint32 lớn nhất → 2106-02-07 06:28:15 (khớp MariaDB 11.5, glibc 2.40 “2106”)")
rec("L11d", (E + dt.timedelta(seconds=2 ** 34 - 2 ** 31 - 1)).date() == dt.date(2446, 5, 10), "34 bit gốc có dấu → 2446-05-10 (khớp ext4 “May 2446”)")
# đếm ngày bằng cách bước từng năm của lịch (không dùng công thức chia hết cho 4)
days = 0
y = 1970
while y < 2038:
    days += (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
    y += 1
rec("L11e", days == 24837 and top // 86400 - days == 18 and top % 86400 == 3 * 3600 + 14 * 60 + 7, "1970–2037 = 24 837 ngày; còn 18 ngày → 19/1; dư 11 647 s = 03:14:07")
rec("L11f", sum((dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days for y in range(1902, 1970)) + (dt.date(1902, 1, 1) - dt.date(1901, 12, 13)).days == 24856,
    "24 856 ngày trước 1970 = 1902–1969 (24 837) + 19 ngày cuối 1901")
rec("L11g", (dt.date(2000, 1, 1) - dt.date(1970, 1, 1)).days == 10957 and (dt.date(2038, 1, 1) - dt.date(2000, 1, 1)).days == 13880, "kiểm hai đoạn: 10 957 + 13 880")
rec("L11h", abs(2 ** 31 / 100 / 86400 - 248.55) < 0.01, "giả thuyết 1/100 giây: 248,55 ngày (FAA chỉ ghi “248 days” — không khẳng định đơn vị)")
rec("L11i", round((2 ** 63 - 1) / (365.2425 * 86400) / 1e9) == 292 and round(top / (365.25 * 86400), 2) == 68.05, "64 bit ≈ 292 tỉ năm; 2³¹ − 1 s ≈ 68,05 năm")
rec("L11j", (E + dt.timedelta(seconds=top) + dt.timedelta(hours=7)).time() == dt.time(10, 14, 7), "giờ Việt Nam (UTC+7): 10:14:07")
rec("L11k", (2038 - 10, 2026 + 15, 2106 - 2026) == (2028, 2041, 80) and dt.date(2028, 1, 19).replace(year=2038) == dt.date(2038, 1, 19),
    "quiz: thẻ 10 năm → hạn sớm nhất 2028; thiết bị 15 năm → 2041 vượt 2038; 2106 còn 80 năm")

# Lab SEP L07 — Hạn công bố lỗ hổng theo lịch

Đọc `YYYY-MM-DD patch_day` từ stdin (ví dụ `2024-02-01 45`). Tính ngày hạn `90` ngày, ngày công bố sau vá theo chính sách 90+30 (`v + 30` ngày nếu `v <= 90`, ngược lại `90` ngày), và hạn khẩn `7` ngày (gợi ý Python: `datetime.date` và `datetime.timedelta`).
In đúng 1 dòng `d90=<date> d_patched=<date> exploit_7d=<date>`.

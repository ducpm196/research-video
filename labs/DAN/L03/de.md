# Lab DAN L03 — Hàm cửa sổ SQLite: SUM lũy kế, LAG và RANK

Đọc `stdin` `days=<d1:rev1,d2:rev2,...>`. Chạy hàm cửa sổ SQLite tính tổng lũy kế, chênh lệch hôm trước và thứ hạng giảm dần cho từng ngày.

In mỗi ngày 1 dòng: `d=<d> cum=<c> diff=<diff> rk=<r>`.
Chấm tự động: `bash labs/cham.sh DAN L03 duong_dan/bai_cua_ban.py`

> Gợi ý `sqlite3` (`PYT:L04` + stdlib): nạp bảng vào `sqlite3.connect(":memory:")`, dùng `SUM(...) OVER (ORDER BY ...)`, `LAG(...) OVER (...)`, `RANK() OVER (...)`.

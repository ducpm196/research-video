# Lab DAN L02 — Nối bảng 1-N làm nhân dòng tổng đơn hàng trong SQLite

Đọc `stdin` `orders=<id:amt,...> items=<oid1,oid2,...>`. Nạp hai bảng vào SQLite, tính tổng sai khi JOIN bảng chi tiết so với tổng đúng trước khi nối.

In 1 dòng: `joined_wrong=<d> true_sum=<d>`.
Chấm tự động: `bash labs/cham.sh DAN L02 duong_dan/bai_cua_ban.py`

> Gợi ý `sqlite3` (`PYT:L04` + stdlib): `c = sqlite3.connect(":memory:")` tạo bảng tạm trên RAM, `c.executemany(...)` rồi `c.execute("SELECT ...").fetchone()[0]`.

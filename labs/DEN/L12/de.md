# Lab DEN L12 — Truy vấn lịch sử SCD Type 2 trong SQLite

Đọc `stdin` `rows=<city:from:to,...> d1=<YYYY-MM-DD> d2=<YYYY-MM-DD>`. Trong Python `sqlite3`, tạo kết nối `c = sqlite3.connect(':memory:')`, tạo bảng `scd(city TEXT, f TEXT, t TEXT)`, tách từng phần tử theo `,` rồi `:` để nạp bằng `c.executemany('INSERT INTO scd VALUES(?,?,?)', rows)`. Vì các khoảng hiệu lực trong dữ liệu không chồng lấn ngày biên, truy vấn thành phố hiệu lực tại `d1`, `d2` bằng `SELECT city FROM scd WHERE ? BETWEEN f AND t` (đoạn đóng `[f, t]`) và đếm tổng dòng bằng `SELECT COUNT(*) FROM scd`.

In 3 dòng: `scd_rows=<d>`, `city_mar20=<str>`, `city_may01=<str>`.
Chấm tự động: `bash labs/cham.sh DEN L12 duong_dan/bai_cua_ban.py`

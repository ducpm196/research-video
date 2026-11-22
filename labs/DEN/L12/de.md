# Lab DEN L12 — Truy vấn lịch sử trên bảng chiều thay đổi chậm trong SQLite

Dùng `sqlite3` dựng bảng `scd(city TEXT, f TEXT, t TEXT)` lưu hai giai đoạn cho một khách hàng chuyển từ `'HCM'` sang `'HN'` ngày `'2026-04-15'` (`'2026-01-01'..'2026-04-14'` và `'2026-04-15'..'9999-12-31'`). Truy vấn thành phố hiệu lực tại `'2026-03-20'` và `'2026-05-01'`.

Định dạng đầu ra (3 dòng):
`scd_rows=<số nguyên>`
`city_mar20=<tên>`
`city_may01=<tên>`

Chấm tự động:
```bash
bash labs/cham.sh DEN L12 duong_dan/bai_cua_ban.py
```

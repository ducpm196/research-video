# Lab SEC L06 — Phòng thủ XSS (chèn mã HTML) bằng html.escape và chèn SQL (SQLi) bằng ?

Viết chương trình Python thoát ký tự đặc biệt HTML của chuỗi `<script>alert(1)</script>` bằng `html.escape` và kiểm tra truy vấn SQLite tham số hoá `?` chặn chuỗi tấn công (payload) `' OR '1'='1`, in đúng 3 dòng:
1. `raw_lt_present=0`
2. `escaped_len=37`
3. `sqli_rows=0`

Chấm tự động:
```bash
bash labs/cham.sh SEC L06 duong_dan/bai_cua_ban.py
```

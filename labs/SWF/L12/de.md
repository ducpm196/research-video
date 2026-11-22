# Lab SWF L12 — Đối chiếu ghép chuỗi vs truy vấn tham số hoá thật trên SQLite (ngôn ngữ SQL)

Viết chương trình Python dùng `sqlite3` thật tạo bảng `users(name TEXT, role TEXT)` có 2 dòng `('an','user'),('root','admin')`, thử payload `' OR '1'='1` vào ghép chuỗi so với `?` tham số hoá, in đúng 3 dòng:
1. `unsafe_rows_leaked=2`
2. `param_rows_returned=0`
3. `sqli_blocked=1`

Chấm tự động:
```bash
bash labs/cham.sh SWF L12 duong_dan/bai_cua_ban.py
```

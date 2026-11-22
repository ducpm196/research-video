# Lab PRJ L02 (100đ theo labs/PRJ/SPEC.md) — Cổng JWT, khử trùng và phân trang con trỏ

Viết chương trình Python cài kiểm chữ ký HMAC-SHA256, khử trùng 5 yêu cầu `(k1,400),(k2,500),(k1,400),(k3,300),(k2,500)` trong SQLite, và phân trang con trỏ trang sau `last_id=990` trên bảng 1 000 dòng, in đúng 3 dòng:
1. `jwt_valid=1`
2. `executed=3 total_amount=1200`
3. `cursor_page=991,992,993`

Chấm tự động:
```bash
bash labs/cham.sh PRJ L02 duong_dan/bai_cua_ban.py
```

# Lab DBS L10 — SQLite thật: tối ưu JOIN giữa hai bảng bằng chỉ mục trên khoá nối

Viết tập lệnh SQLite dựng hai bảng `R(id INT, k INT)` (`200` dòng) và `S(k INT, v INT)` (`50` dòng) có chỉ mục `idx_sk ON S(k)`, thực hiện `JOIN` lấy tổng giá trị khớp và số cặp nối, in đúng 3 dòng:
1. `joined_rows=200`
2. `idx_sk_ok=1`
3. `sum_v=5100`

Chấm tự động:
```bash
bash labs/cham.sh DBS L10 duong_dan/bai_cua_ban.sql
```

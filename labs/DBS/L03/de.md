# Lab DBS L03 — SQLite thật: logic ba trị NULL và hàm tổng hợp

Viết tập lệnh SQLite kiểm chứng `COUNT(*)` vs `COUNT(lop)`, so sánh `WHERE lop = NULL` vs `WHERE lop IS NULL`, và `GROUP BY lop HAVING COUNT(*) >= 2`, in đúng 3 dòng:
1. `cnt_all=4 cnt_col=3`
2. `eq_null=0 is_null=1`
3. `having_ge2_groups=1`

Chấm tự động:
```bash
bash labs/cham.sh DBS L03 duong_dan/bai_cua_ban.sql
```

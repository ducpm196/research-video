# Lab DBS L02 — SQLite thật: LEFT JOIN và bẫy lọc ở WHERE vs ON

Viết tập lệnh SQLite trên bảng `SV(4 dòng)` và `Lop(2 dòng)`: so sánh `LEFT JOIN` thuần, `LEFT JOIN ... WHERE Lop.ten='CS'` (biến thành inner join mất dòng NULL), và sắp tên điểm `>= 7`, in đúng 3 dòng:
1. `left_all=4`
2. `left_where_drops_null=2`
3. `top_names=An,Chi,Dung`

Chấm tự động:
```bash
bash labs/cham.sh DBS L02 duong_dan/bai_cua_ban.sql
```

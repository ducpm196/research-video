# Lab DBS L09 — SQLite thật: chỉ mục ghép cột (lop, diem) và quy tắc tiền tố trái

Viết tập lệnh SQLite tạo bảng `Diem(id INT, lop TEXT, diem INT)` cùng `INDEX idx_ld ON Diem(lop, diem)`, kiểm tra chỉ mục ghép và lọc cả điều kiện `(lop='K1' AND diem >= 8)` vs lọc khoảng điểm từ 7 đến 9 (`diem BETWEEN 7 AND 9`), in đúng 3 dòng:
1. `composite_idx_ok=1`
2. `k1_ge8=2`
3. `between_7_9=4`

Chấm tự động:
```bash
bash labs/cham.sh DBS L09 duong_dan/bai_cua_ban.sql
```

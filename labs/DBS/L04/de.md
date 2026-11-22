# Lab DBS L04 — SQLite thật: kiểm tra tính duy nhất của khoá hợp thành AD

Viết tập lệnh SQLite kiểm bảng `R(A,B,C,D)` thoả phụ thuộc `A->B, B->C` và khoá `(A,D)`: xác nhận mọi dòng có `(A,D)` duy nhất (`UNIQUE(A,D)`), `A` riêng lẻ thì không duy nhất, và không tồn tại cặp mâu thuẫn `A->B`, in đúng 3 dòng:
1. `rows=3 distinct_ad=3`
2. `a_not_unique=1`
3. `fd_a_to_b_holds=1`

Chấm tự động:
```bash
bash labs/cham.sh DBS L04 duong_dan/bai_cua_ban.sql
```

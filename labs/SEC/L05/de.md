# Lab SEC L05 — Kiểm tra chính sách cookie SameSite trước POST chéo trang

Viết hàm `cookie_sent(same_site, method, cross_site)` mô phỏng quy tắc trình duyệt: `None` vẫn gửi khi `POST` chéo trang; `Lax` và `Strict` không gửi cookie khi `POST` từ trang lạ, in đúng 3 dòng:
1. `none_cross_post=1`
2. `lax_cross_post=0`
3. `strict_cross_post=0`

Chấm tự động:
```bash
bash labs/cham.sh SEC L05 duong_dan/bai_cua_ban.py
```

# Lab BCH L01 — Dựng chuỗi băm SHA-256 4 khối và phát hiện sửa đổi dữ liệu

Dùng `hashlib.sha256` tạo chuỗi `4` khối nối đuôi từ danh sách `['khối 0', 'A->B 10', 'B->C 4', 'C->A 3']` (bắt đầu bằng `prev = '0'*10`, mỗi khối băm `prev + '|' + data`, lấy 10 ký tự hex đầu). Thử sửa khối chỉ số `2` thành `'B->C 40'` và tính lại phần đuôi để xem có bao nhiêu khối đổi mã.
In đúng 1 dòng `orig_b2=... tampered_b2=... broken_blocks=...`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L01 duong_dan/bai_cua_ban.py
```

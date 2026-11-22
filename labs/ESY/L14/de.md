# Lab ESY L14 — Kiểm toàn vẹn SHA-256, chữ ký và tự quay lui cập nhật A/B

Cho hai phân vùng phần sụn: bản `A` hợp lệ (`sha_ok=True, sig_ok=True, boot_ok=True`) và bản `B` vừa tải có nội dung `b'fw-v2'` nhưng mã kiểm định mong đợi là SHA-256 của `b'fw-v2-clean'` (`sig_ok=True, boot_ok=True`). Viết bộ chọn khởi động so khớp `hashlib.sha256` thực tế để quyết định chọn `'A'` hay `'B'`.
In đúng 1 dòng `b_hash_ok=0/1 boot_slot=...`.

Chấm tự động:
```bash
bash labs/cham.sh ESY L14 duong_dan/bai_cua_ban.py
```

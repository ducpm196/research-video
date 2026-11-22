# Lab DVO L04 — Kiểm chứng SHA-256 sản phẩm dựng bất biến và tái lập

Viết chương trình Python băm SHA-256 hai bản dựng nhị phân giống nhau `b'app-v1.4.2'` so với bản thay 1 byte `b'app-v1.4.3'`, kiểm tra toàn bộ `64` ký tự hệ 16 trùng khớp khi không đổi và đổi khác khi sửa 1 byte, in đúng 3 dòng:
1. `same_artifact_same_hash=1`
2. `changed_byte_different_hash=1`
3. `sha256_len_hex=64`

Chấm tự động:
```bash
bash labs/cham.sh DVO L04 duong_dan/bai_cua_ban.py
```

# Lab SEC L00 — Ánh xạ mô hình đe doạ STRIDE sang thuộc tính an toàn

Viết chương trình Python cài bảng ánh xạ STRIDE và kiểm tra 6 cặp 1-1 không trùng lặp, truy vấn tính chất bị vi phạm của `Information Disclosure` (lộ thông tin → `Confidentiality` bí mật), `Tampering` (sửa lén → `Integrity` toàn vẹn) và `Spoofing` (giả mạo → `Authentication` xác thực), in đúng 3 dòng:
1. `stride_unique_props=6`
2. `info_disclosure=Confidentiality`
3. `tampering=Integrity spoofing=Authentication`

Chấm tự động:
```bash
bash labs/cham.sh SEC L00 duong_dan/bai_cua_ban.py
```

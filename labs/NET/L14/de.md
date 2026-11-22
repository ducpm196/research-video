# Lab NET L14 (Mô phỏng chữ ký số) — RSA (hệ khoá công khai) ký/kiểm chữ ký đồ chơi + băm SHA-256

Viết chương trình Python dùng RSA (hệ khoá công khai đồ chơi) ký giá trị `m = 4` bằng cặp `(n=33, d=7, e=3)` (`sig = m^d mod n`), kiểm chữ ký bằng `sig^e mod n == m` và kiểm tra độ dài chuẩn `64` ký tự hệ 16 (`hex`) của SHA-256 trên `'TLS'`, in đúng 3 dòng:
1. `sig=16 verify=4`
2. `valid=1`
3. `sha256_hex_len=64`

Chấm tự động:
```bash
bash labs/cham.sh NET L14 duong_dan/bai_cua_ban.py
```

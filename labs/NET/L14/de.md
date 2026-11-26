# Lab NET L14 — Chữ ký số RSA đồ chơi và độ dài băm SHA-256

Đọc `stdin` `n=<int> d=<int> e=<int> m=<int> tag=<str>`. Ký và xác minh RSA `sig = m^d mod n`, `chk = sig^e mod n`, đồng thời đo độ dài hex SHA-256 của `tag`.

In đúng 3 dòng: `sig=<d> verify=<d>`, `valid=<0|1>`, `sha256_hex_len=<d>`.
Chấm tự động: `bash labs/cham.sh NET L14 duong_dan/bai_cua_ban.py`

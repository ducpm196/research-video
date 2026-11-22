# Lab NET L13 (Mô phỏng trao đổi khoá) — Diffie–Hellman trên tham số nhỏ

Viết chương trình Python tính các thông điệp công khai `A = g^a mod p`, `B = g^b mod p` và khoá bí mật chung cho `p = 23, g = 5, a = 6, b = 15`, kiểm chứng hai bên thu cùng một giá trị, in đúng 3 dòng:
1. `A=8 B=19`
2. `shared_alice=2 shared_bob=2`
3. `keys_match=1`

Chấm tự động:
```bash
bash labs/cham.sh NET L13 duong_dan/bai_cua_ban.py
```

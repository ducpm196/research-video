# Lab BCH L03 — Ký SHA-256 và kiểm chứng chữ ký số trên mô hình RSA đồ chơi

Với cặp khoá hệ mật mã bất đối xứng RSA (Rivest–Shamir–Adleman) đồ chơi `(n = 3233, e = 17, d = 2753)`, lấy mã băm `m = int(hashlib.sha256('A trả B 15'.encode()).hexdigest(), 16) % n` rồi ký `sig = pow(m, d, n)`. Kiểm định chữ ký cho tin gốc (`m`) và cho tin bị sửa (`'A trả B 150'`).
In đúng 1 dòng `sig_valid=0/1 tampered_valid=0/1`.

Chấm tự động:
```bash
bash labs/cham.sh BCH L03 duong_dan/bai_cua_ban.py
```

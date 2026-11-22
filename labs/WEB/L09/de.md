# Lab WEB L09 — Node.js thật: tính chuỗi thử thách PKCE từ chuẩn RFC 7636 bằng module crypto

Viết tập lệnh Node.js dùng module `crypto` tính `code_challenge = BASE64URL(SHA256(verifier))` (mã hoá Base64 an toàn cho URL) cho vector chuẩn RFC 7636 `'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'`, in đúng 3 dòng:
1. `challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM`
2. `len=43`
3. `no_padding=1`

Chấm tự động:
```bash
bash labs/cham.sh WEB L09 duong_dan/bai_cua_ban.js
```

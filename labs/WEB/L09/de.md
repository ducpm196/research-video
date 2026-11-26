# Lab WEB L09 — Node.js: tính chuỗi thử thách PKCE chuẩn RFC 7636

Đọc `stdin` `verifier=<str>`. Dùng mô-đun `crypto` tính `code_challenge = BASE64URL(SHA256(verifier))`, kiểm độ dài và kiểm tra không có dấu đệm `=`.

In đúng 3 dòng: `challenge=<str>`, `len=<d>`, `no_padding=<0|1>`.
Chấm tự động: `bash labs/cham.sh WEB L09 duong_dan/bai_cua_ban.js`

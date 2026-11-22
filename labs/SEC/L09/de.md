# Lab SEC L09 — Chuỗi tin cậy TLS: tổ chức cấp chứng chỉ (CA) ký và phát hiện sửa tên miền

Viết chương trình Python băm tên miền `b'bank.vn'` và `b'evil.vn'` modulo `n = 33` (`e = 3, d = 7`), tổ chức cấp chứng chỉ (CA) ký chứng chỉ thật rồi máy khách kiểm chứng bằng khoá công khai của CA, in đúng 3 dòng:
1. `legit_cert_valid=1`
2. `forged_domain_valid=0`
3. `chain_verified=1`

Chấm tự động:
```bash
bash labs/cham.sh SEC L09 duong_dan/bai_cua_ban.py
```

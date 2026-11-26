# Lab SEC L08 — Tính và xác minh thẻ HMAC theo thuật toán băm RFC 2104

Đọc `stdin` 4 dòng `alg=<hash>`, `key=<str>`, `msg=<str>`, `tampered=<str>`. Tính thẻ HMAC theo thuật toán động `alg` bằng `hmac.new(key.encode(), ..., alg).hexdigest()` cho bản gốc và bản sửa đổi, rồi so sánh hằng thời gian bằng `hmac.compare_digest`.

In đúng 3 dòng: `mac_len_hex=<d>`, `orig_valid=<0|1>`, `tampered_valid=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L08 duong_dan/bai_cua_ban.py`

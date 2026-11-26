# Lab DVO L04 — Kiểm chứng SHA-256 sản phẩm dựng bất biến và tái lập

Đọc `stdin` `b1=<str> b2=<str> b3=<str>`. Băm SHA-256 ba chuỗi bản dựng, kiểm trùng khớp giữa `b1`, `b2`, khác biệt với `b3` và chiều dài chuỗi hex.

In đúng 3 dòng: `same_artifact_same_hash=<0|1>`, `changed_byte_different_hash=<0|1>`, `sha256_len_hex=<d>`.
Chấm tự động: `bash labs/cham.sh DVO L04 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.

# Lab ESY L14 — Kiểm toàn vẹn SHA-256 và chữ ký phân vùng A/B

Đọc `expected_str|got_str|sig_ok` từ stdin (ví dụ `fw-v2-clean|fw-v2|1`). So khớp SHA-256 và chữ ký `sig_ok=1` để chọn `'B'` hoặc quay lui `'A'`.
In đúng 1 dòng `b_hash_ok=0/1 boot_slot=A/B`.

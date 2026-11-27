# Lab BCH L01 — Chuỗi băm SHA-256 và hiệu ứng dây chuyền khi sửa

Đọc `idx|b0;b1;...|new_txt` từ stdin (ví dụ `2|khối 0;A->B 10;B->C 4;C->A 3|B->C 40`), trong đó `idx` đánh số từ `0` (`0..len(blocks)-1`). Khởi tạo mã trước khối đầu bằng `"0" * 10`, băm mỗi khối bằng `hashlib.sha256(f"{prev_10}|{data}".encode("utf-8")).hexdigest()[:10]` (lấy 10 hex đầu nối sang khối sau bằng `|`), sửa khối `idx` thành `new_txt` và đếm số khối đổi mã. Lưu ý: mọi ca (kể cả khi `idx` khác `2`) luôn giữ nguyên tên khoá đầu ra `orig_b2=` và `tampered_b2=` để in mã của khối `idx` (`chain[idx]` và `tampered[idx]`).
In đúng 1 dòng `orig_b2=<hex> tampered_b2=<hex> broken_blocks=<int>`.
Gợi ý Python: `import sys, hashlib; sys.stdin.reconfigure(encoding="utf-8"); idx_s, blocks_s, new_txt = sys.stdin.read().strip().split('|', 2); idx = int(idx_s); blocks = blocks_s.split(';')`, dùng `hashlib.sha256(t.encode("utf-8")).hexdigest()[:10]`.

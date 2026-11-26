# Lab BCH L01 — Chuỗi băm SHA-256 và hiệu ứng dây chuyền khi sửa

Đọc `idx|b0;b1;...|new_txt` từ stdin (ví dụ `2|khối 0;A->B 10;B->C 4;C->A 3|B->C 40`). Khởi tạo mã trước khối đầu bằng 10 số `0` (`"0" * 10`), băm mỗi khối bằng `sha256(f"{prev_10}|{data}".encode()).hexdigest()[:10]` (lấy 10 hex đầu rồi nối sang khối sau bằng dấu `|`), sửa khối `idx` thành `new_txt` và đếm số khối đổi mã.
In đúng 1 dòng `orig_b2=<hex> tampered_b2=<hex> broken_blocks=<int>`.

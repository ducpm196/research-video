# Lab PAR L03 — Điều kiện tranh chấp mất cập nhật

Đọc số lượt tăng mỗi luồng `k` từ stdin (ví dụ `3`).
Mô phỏng đúng kiểu xen kẽ đồng bộ 2 luồng trong `k` lượt: ở mỗi lượt, cả hai luồng cùng đọc biến dùng chung `c` (`r1 = c; r2 = c`) trước khi luồng 1 ghi `c = r1 + 1` rồi luồng 2 ghi `c = r2 + 1` (so với phép nguyên tử cho `2*k`).
In đúng 1 dòng `racy_final=<int> expected_atomic=<int>`.

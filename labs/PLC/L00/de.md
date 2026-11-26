# Lab PLC L00 — Lỗi cú pháp và lỗi ngữ nghĩa

Đọc `k:v,...|var|tk0,tk1,...` từ `stdin` (ví dụ `x:1|y|(,1,+,2`).
- `syn_err`: bằng `1` nếu dãy từ tố không cân bằng ngoặc tròn `(` `)` (số ngoặc mở và đóng không khớp, hoặc có ngoặc đóng `)` đứng trước ngoặc mở tương ứng), bằng `0` nếu hợp lệ.
- `sem_err`: bằng `1` nếu tên biến `var` chưa có trong bảng khai báo môi trường `k:v,...`, bằng `0` nếu đã khai báo.

In đúng 1 dòng `syn_err=<0|1> sem_err=<0|1>`.
Chấm tự động: `bash labs/cham.sh PLC L00 duong_dan/bai_cua_ban.py`

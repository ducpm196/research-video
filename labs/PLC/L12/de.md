# Lab PLC L12 — Bảo toàn bất biến bằng cấu trúc dữ liệu không đổi (tuple)

Đọc `x0,x1,...|them` từ `stdin` (ví dụ `5,15,25|35`). Chuyển dãy đầu vào thành `tuple` `xs1`, rồi tạo phiên bản mới `xs2 = xs1 + (int(them),)` mà giữ nguyên không đổi `xs1`.

In đúng 1 dòng `xs1=(...) xs2=(...) unchanged=<0|1>`.
Chấm tự động: `bash labs/cham.sh PLC L12 duong_dan/bai_cua_ban.py`

# Lab SDP L06 — SOLID 2: Phát hiện sai lệch hậu điều kiện Liskov trên cặp cạnh (w, h)

Đọc `stdin` `w=<int> h=<int>`. Đặt chiều rộng `w` rồi chiều cao `h` cho lớp `Rectangle` và lớp con `Square` (ép `w = h`). Đặt `lsp_violated=1` nếu trên đúng cặp `(w, h)` này diện tích trả về của `Square` khác với `Rectangle` (ngược lại `0`; lưu ý về tổng quát hợp đồng của `Square` luôn sai nếu có thao tác gán từng cạnh).

In đúng 3 dòng: `rect_area=<d>`, `square_area=<d>`, `lsp_violated=<0|1>`.
Chấm tự động: `bash labs/cham.sh SDP L06 duong_dan/bai_cua_ban.py`

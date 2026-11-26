# Lab HCI L05 — Mô hình thao tác KLM chuột vs phím tắt

Đọc `K P H M BB` từ stdin (ví dụ `0.20 1.10 0.40 1.35 0.20`). Tính thời gian đổi tên một tệp sang tên mới dài đúng 3 ký tự theo hai chuỗi thao tác KLM:
- Chuột: `H + M + P + BB + P + BB + 3*K` (chuyển tay sang chuột, nghĩ, trỏ biểu tượng, nhấp đúp mở sửa tên, trỏ nút xác nhận, nhấp, gõ tên mới 3 ký tự).
- Phím tắt: `H + 2*K + M + 3*K + K` (đặt tay lên bàn phím, nhấn tổ hợp 2 phím mở đổi tên, nghĩ, gõ tên mới 3 ký tự, nhấn phím Enter xác nhận).
In đúng 1 dòng `mouse_s=<2 chữ số> keyboard_s=<2 chữ số>`.

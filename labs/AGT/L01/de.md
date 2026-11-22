# Lab AGT L01 — Gọi công cụ và kiểm tra lược đồ tham số

Kiểm tra danh sách 5 lời gọi chuyển khoản giả lập `calls = [(750_000, '9876543210'), (True, '9876543210'), (-100, '9876543210'), (250_000, '12345'), (15_000_000, '9876543210')]`. Quy tắc hợp lệ: số tiền `amt` phải là `int` thực sự (loại `bool`) trong khoảng `0 < amt <= 10_000_000` và tài khoản `acc` là chuỗi đúng `10` chữ số.

Định dạng đầu ra (1 dòng):
`total_calls=<số> valid_count=<số> idx=<danh sách chỉ số>`

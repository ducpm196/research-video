# Lab ACB L06 — Ngưỡng sinh trắc học cộng dồn trong ngày và kiểm vé một lần

Số liệu (số minh hoạ, khác ví dụ trong bài; đơn vị triệu đồng):
- Các giao dịch trong ngày, theo thứ tự: `6, 7, 9, 15, 3`. Quy tắc: phải quét mặt khi số tiền **trên 10** hoặc khi **tổng cộng dồn cộng số tiền này vượt 20**; sau khi quét mặt, tổng cộng dồn về **0**; nếu không quét thì tổng cộng dồn tăng thêm số tiền.
- Vé `id = x7`, số tiền `30`, hạn dùng đến giây `240`, chữ ký là HMAC-SHA256 của chuỗi `id|tien|het_han` (ví dụ `x7|30|240`) với khoá bí mật bạn tự chọn (lấy 8 ký tự hệ mười sáu đầu). Bốn lần kiểm theo thứ tự `(tiền, giây hiện tại)`: `(30, 100)`, `(30, 150)`, `(35, 100)`, `(30, 250)`. Mỗi lần kiểm theo đúng thứ tự cổng: chữ ký, hết hạn, đã dùng; vé qua cả ba cổng thì ghi là đã dùng.

Viết `mau.py` (Python 3, dùng `hmac` và `hashlib` có sẵn) in đúng chín dòng:

1. Năm dòng `<tiền> <quet mat|thuong> tong: <tổng sau giao dịch>`.
2. Bốn dòng kết quả kiểm vé, mỗi dòng là một trong `cho phep`, `tu choi: ky sai hoac tien bi sua`, `tu choi: het han`, `tu choi: da dung`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L06 mau.py`.

# Hàm tham chiếu cho `checks:` của khoá BNX

Mỗi bài một tệp `lNN.py` (ví dụ `l03.py`). Mọi hàm công khai đặt tên `bnx_…` (ví dụ `bnx_jwt_sign`). `tools/checklib.py` nạp mọi tệp ở đây
vào không gian `alg`, nên trong `checks:` gọi `alg.bnx_jwt_sign(...)`. Chỉ dùng thư viện chuẩn của Python. Không đọc mạng, không gọi Docker
(phép chạy thật đặt ở `audit/bnx/ver/lNN.py`, không ở đây).

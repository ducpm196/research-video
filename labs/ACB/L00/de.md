# Lab ACB L00 — Tải, độ trễ, thời gian sống khoá và bồi hoàn SAGA

Số liệu (số minh hoạ, khác ví dụ trong bài): tải **4 000** giao dịch mỗi giây; mạng **90** mi li giây, hạch toán **40** mi li giây, ngưỡng là dưới **200** mi li giây (tổng ước lượng, không phải P99); đối tác có thể gửi lại bản tin tối đa **45** giây, khoá khử trùng lặp đặt thời gian sống **gấp đôi** khoảng đó; số dư **3 000 000** đồng, hệ thống đã trừ **1 200 000** nhưng đối tác báo chưa nhận được tiền nên phải bồi hoàn.

Viết `mau.py` (Python 3, chỉ dùng `print`) in đúng năm dòng theo mẫu:

1. `moi phut: <số giao dịch>`
2. `moi gio: <số giao dịch>`
3. `toan trinh: <tổng> ms, duoi 200` (hoặc `toan trinh: <tổng> ms, vuot 200` nếu không dưới 200)
4. `ttl: <giây> giay = <mi li giây> ms`
5. `so du sau boi hoan: <số>`

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L00 mau.py`.

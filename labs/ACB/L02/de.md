# Lab ACB L02 — Bản đồ bit ISO 8583 và khoá khử trùng lặp có hạn

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Bản tin A có các trường **3, 4, 11, 37, 41**.
- Bản tin B có các trường **3, 4, 11, 37, 128**: trường 128 nằm ở bản đồ bit thứ hai, nên bản đồ bit chính phải có thêm **trường 1** (bit báo "có bản đồ thứ hai"); bản đồ bit thứ hai đánh số trường 65–128 thành vị trí 1–64 (trường 128 là vị trí 64).
- Giải mã bản đồ bit chính `5030000000000000`.
- Khoá khử trùng lặp `654321:000000000007`; đối tác gửi lại tối đa **40** giây, thời gian sống đặt **gấp đôi**; lệnh đến lúc giây **0**, **30**, **95**. Tải **2 400** lệnh mỗi giây, độ trễ **150** mi li giây.

Viết `mau.py` (Python 3) in đúng các dòng:

1. `bitmap A: <16 chữ số hệ mười sáu, chữ in hoa>` — trường n ứng với số 1 dịch sang trái `64 - n` vị trí (`1 << (64 - n)`), rồi cộng các bit lại.
2. `bitmap B: <chính> <phụ>`.
3. `giai ma: <danh sách số trường tăng dần>` (dạng `[2, 4, 11, 12]`).
4. Ba dòng `t=<giây> <nhãn>: <True|False>`, nhãn lần lượt `khoa moi`, `khoa trung`, `het han`; `True` nghĩa là khoá được đặt (khoá chưa có hoặc đã hết hạn).
5. `dang cho: <số>` — tải nhân độ trễ (mi li giây) chia nguyên cho 1000.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L02 mau.py`.

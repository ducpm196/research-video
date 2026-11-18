# Lab ACB L08 — Hạn mức và lãi thấu chi, phong tỏa hai pha, nhóm nợ CIC và giải ngân lũy đẳng

Số liệu (số minh hoạ, khác ví dụ trong bài):
- Sổ tiết kiệm **240 000 000** đồng, tỉ lệ cấp vốn **80%**, lãi gửi **4,8%** một năm, biên độ **2,7%**; khách rút **120 000 000** đồng trong **45** ngày; một năm tính **365** ngày.
- Quy trình hai pha với `khoa_ok = True`, `cap_ok = False`: khoá sổ thành công, cấp hạn mức lỗi thì nhả khoá sổ.
- Quy tắc duyệt: nhóm nợ cao nhất tra được ở CIC **dưới 2** thì `duyet tu dong`, từ **2 trở lên** thì `chuyen tham dinh`. Thử nhóm 1 và nhóm 2.
- Giải ngân: khoá `K7`, số tiền `120000000`, gửi hai lần; mỗi khoá chỉ được chi một lần.

Viết `mau.py` (Python 3, dùng `sqlite3` có sẵn nếu muốn) in đúng tám dòng:

1. `han muc: <số>`; `lai suat: <số>` (lãi gửi cộng biên độ); `lai 45 ngay: <số>` (làm tròn `rut × lãi suất / 100 × ngày / 365`).
2. `hai pha: <các bước nối bằng dấu phẩy, không cách>` — bước đã làm theo đúng thứ tự: `khoa so`, rồi `cap han muc loi: nha khoa so`.
3. `quyet dinh nhom 1: …` và `quyet dinh nhom 2: …`.
4. `giai ngan lan 1 chi tien` và `giai ngan lan 2 trung khoa, bo qua` (không có dấu hai chấm sau số lần).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh ACB L08 mau.py`.

# Lab BNX L15 — Ước lượng tải, ngân sách độ trễ và bể kết nối cho một bộ số liệu mới

Số liệu là số minh hoạ (không phải của ngân hàng nào). Viết `mau.py` (chỉ dùng Python có sẵn):

- **5 000 000** giao dịch mỗi ngày; cao điểm gấp **6** lần trung bình;
- ngân sách độ trễ **400 ms** cho một lệnh; các chặng nối tiếp (ms): cổng 12, xác thực 6, dịch vụ 25, Oracle 120, đọc Redis 3;
- mỗi lệnh ở lại Oracle **120 ms**; bể kết nối tới Oracle có **30** kết nối.

Tính và in đúng năm dòng (dùng `round(x, 1)` cho số có một chữ số thập phân, `round(x)` cho số nguyên, `math.ceil` làm tròn lên):

1. `trung binh <tải trung bình> giao dich/giay` — một chữ số thập phân (một ngày có 24·60·60 giây);
2. `cao diem <tải cao điểm> giao dich/giay` — làm tròn tới số nguyên;
3. `con du <số> ms` — ngân sách trừ tổng các chặng;
4. `cung luc o Oracle <số>` — số lệnh trung bình chạy cùng lúc ở Oracle ở cao điểm (tải cao điểm × thời gian mỗi lệnh, tính bằng giây, định luật Little), một chữ số thập phân; **nhân bằng tải cao điểm chưa làm tròn** (347 × 0,120 = 41,64 cho 41,6, còn số chưa làm tròn cho 41,7: làm tròn chỉ để in);
5. `be 30 ket noi: <du hoặc khong du> - can it nhat <số kết nối>` — bể đủ nếu số lệnh cùng lúc không vượt 30; số kết nối cần ít nhất là số lệnh cùng lúc làm tròn lên.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L15 mau.py`. Đầu ra viết không dấu.

# Lab BNX L34 — Bậc duyệt theo tổng dư nợ, máy trạng thái và tra cứu có đồng ý

Số liệu (số minh hoạ, đơn vị triệu đồng; khác ví dụ trong bài):
- Bậc duyệt: tổng ≤ 50 → `chuyen vien`; ≤ 200 → `truong phong`; trên 200 → `hoi dong`.
- Hồ sơ A: dư nợ hiện có 120, xin thêm 100. Hồ sơ B: dư nợ 0, xin 40.
- Các cạnh được phép: `KHOI_TAO → THAM_DINH`, `THAM_DINH → DUYET`, `THAM_DINH → TU_CHOI`.
- Bảng `dong_y` có một dòng: khách `K9`, mục đích `tham dinh`, hết hạn `2026-06-30`, chưa thu hồi.

Viết `mau.py` in năm dòng:
1. `ho so A: tong <tổng> -> <vai trò>` và dòng tương tự cho hồ sơ B (tính theo TỔNG dư nợ cộng khoản mới).
2. `THAM_DINH -> KHOI_TAO: <cho phep | tu choi>` (quay lui có được phép không).
3. Hàm tra cứu: `K9 tham dinh <ngày>: cho phep` khi đồng ý còn hạn; ngược lại `tu choi (het han)` (ngày dạng `2026-05-31`, so sánh chuỗi). In cho hai ngày `2026-05-31` và `2026-07-01`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L34 mau.py`.

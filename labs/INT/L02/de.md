# Lab INT L02 — Trả lời một câu phỏng vấn có số: bể kết nối và REQUIRES_NEW (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ): cơ sở dữ liệu **16 nhân**, **2 ổ đĩa**; mỗi giao dịch giữ kết nối chính **20 mili giây**; ghi nhật ký bằng REQUIRES_NEW giữ thêm một kết nối khác **5 mili giây** cho mỗi giao dịch.

Viết ba dòng:
1. `be ket noi: <số>` — nhân × 2 + số đĩa (công thức kinh nghiệm, điểm khởi đầu).
2. `toi da khong nhat ky: <số> giao dich/giay` — số kết nối chia cho 0,020 giây, lấy phần nguyên.
3. `toi da co nhat ky REQUIRES_NEW: <số> giao dich/giay` — số kết nối chia cho (0,020 + 0,005) giây, lấy phần nguyên.

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "print(16*2+2, 34/0.02, 34/0.025)"` rồi so ba số với ba dòng (lấy phần nguyên).

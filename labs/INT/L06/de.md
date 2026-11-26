# Lab INT L06 — Trả lời một câu phỏng vấn có số: thiết kế cổng thanh toán và ngưỡng sinh trắc học (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, có thể tự so với `loi_giai.md` hoặc chấm định dạng bằng `bash labs/cham.sh INT L06 bai_lam.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây.

Số liệu (số minh hoạ, đề bài giả định, không phải số của ngân hàng nào): cổng nhận **2 000** giao dịch mỗi giây; độ trễ trung bình **200 mili giây**; mỗi máy giữ **150** yêu cầu cùng lúc; mục tiêu sẵn sàng **99,95%**, một năm có 525 600 phút; chuỗi **3** tầng nối tiếp, mỗi tầng 99,95%. Quy định sinh trắc học: bắt buộc xác thực khuôn mặt khi một lần chuyển **trên 10 triệu** hoặc tổng chuyển trong ngày **trên 20 triệu** (theo Thông tư 50/2024/TT-NHNN, sửa đổi bởi Thông tư 77/2025/TT-NHNN; Quyết định 2345/QĐ-NHNN chưa đọc nguyên văn, chưa rõ còn áp dụng nên không dùng làm căn cứ; bài không nêu số điều, khi làm thật hãy mở văn bản hiện hành).

Viết sáu dòng:
1. `yeu cau do cung luc: <số>` — giao dịch mỗi giây × số giây ở lại.
2. `so may (moi may 150, +1 du phong): <số>` — làm tròn lên (yêu cầu dở chia 150), cộng 1.
3. `ngan sach 99.95%: <số> phut/nam` — 525 600 × (1 − 0,9995).
4. `chuoi 3 tang 99.95%: <x>%, ngung <y> phut/nam` — x = tích ba tỉ lệ (2 chữ số sau dấu phẩy, tính theo phần trăm), y = 525 600 × (1 − tích), 1 chữ số sau dấu phẩy; dùng tích chưa làm tròn (0,9995³), không dùng x đã làm tròn.
5. `sinh trac hoc 12 trieu mot lan: <can hoặc chua can>`
6. `tong ngay 8 + 7 = 15 trieu: <can hoặc chua can>` — mỗi lần ≤ 10 triệu và tổng ngày ≤ 20 triệu.

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "import math; d=2000*0.2; print(d, math.ceil(d/150)+1, 525600*0.0005, round(525600*(1-0.9995**3),1))"` rồi so bốn số với các dòng 1 đến 4.

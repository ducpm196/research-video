# Lab INT L05 — Trả lời một câu phỏng vấn có số: nhân xử lý, điểm Z, UCB1, cosine (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, và `cham.sh` không chấm tệp `.md`. Tính tay (máy tính bỏ túi được dùng cho căn và logarit tự nhiên), ghi từng dòng đúng định dạng dưới đây, rồi tự so với `loi_giai.md`.

Số liệu (số minh hoạ, chưa đo trên mô hình thật):
- **12 000** giao dịch mỗi giây; mô hình nhẹ **3 mili giây**, mô hình nặng **40 mili giây** mỗi giao dịch (một nhân xử lý một giao dịch tại một thời điểm);
- giao dịch **45 triệu**, trung bình 30 ngày **5 triệu**, độ lệch chuẩn **4 triệu**;
- hai kênh, hệ số khám phá c = √2, tổng đã thử N = **210**: kênh A thành công **180 / 200**, kênh B thành công **9 / 10**; điểm = tỉ lệ thành công + √(2 · ln N / số lần thử của kênh);
- hai véc tơ u = **(2, 1)** và v = **(1, 3)**.

Viết bảy dòng:
1. `so nhan mo hinh nhe 3 ms: <số>`
2. `so nhan mo hinh nang 40 ms: <số>`
3. `diem Z: <số>`
4. `diem A: <số, 2 chữ số sau dấu phẩy>`
5. `diem B: <số, 2 chữ số sau dấu phẩy>`
6. `chon kenh: <A hoặc B>` — kênh có điểm cao hơn.
7. `cosine: <số, 3 chữ số sau dấu phẩy>`

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "import math; u=lambda m,k,n: m+math.sqrt(2*math.log(n)/k); print(12000*0.003, 12000*0.04, (45-5)/4, round(u(0.9,200,210),2), round(u(0.9,10,210),2), round(5/math.sqrt(5*10),3))"` rồi so sáu số với các dòng 1, 2, 3, 4, 5 và 7.

# Lab INT L08 — Trả lời một câu phỏng vấn có số: LTV, DTI, trích nợ từng phần và đối soát cuối ngày (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, có thể tự so với `loi_giai.md` hoặc chấm định dạng bằng `bash labs/cham.sh INT L08 bai_lam.md`. Tính tay, ghi từng dòng đúng định dạng dưới đây.

Số liệu (số minh hoạ, không phải số của ngân hàng nào):
- sổ tiết kiệm **240 triệu**, tỉ lệ cho vay LTV **70%**;
- trả nợ **9 triệu** mỗi tháng, thu nhập **36 triệu** mỗi tháng;
- đến hạn phải trả **12 triệu**, số dư khả dụng **7,5 triệu**;
- đối soát ba danh sách, mỗi danh sách **2 000 000** giao dịch, tốc độ **10^9** (một tỉ) phép so sánh mỗi giây. Hai vòng lặp lồng nhau: N × N phép so sánh với N = 2 000 000 (đổi ra giờ, làm tròn một chữ số thập phân). Sắp xếp cộng hai con trỏ: 3 × N × ⌈log₂ N⌉ + 2 × (N + N) phép so sánh (đổi ra giây, làm tròn hai chữ số thập phân); trong đó 3 lần sắp xếp ứng với ba danh sách, mỗi lần N × ⌈log₂ N⌉, còn 2 lượt hai con trỏ ứng với hai cặp danh sách, mỗi lượt đi qua N + N bản ghi.

Viết năm dòng:
1. `han muc LTV 70%: <số> trieu` — giá trị sổ × LTV.
2. `DTI: <số>%` — tiền trả nợ mỗi tháng chia thu nhập mỗi tháng.
3. `thu tung phan: <số> trieu, con thieu <số> trieu` — thu bằng số dư khả dụng, phần còn thiếu vẫn tính ngày quá hạn.
4. `doi soat long nhau: <số> gio`
5. `doi soat sap xep: <số> giay`

Tự kiểm bằng Python (không bắt buộc, sau khi đã tính tay): chạy `python -c "import math; N=2000000; print(240*0.7, 9/36, 7.5, 12-7.5, round(N*N/1e9/3600,1), round((3*N*math.ceil(math.log2(N))+2*(N+N))/1e9,2))"` rồi so sáu số với các dòng 1 đến 5.

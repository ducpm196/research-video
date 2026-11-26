# Lab BNX L35 — Ngân sách SLA và khung tài liệu thiết kế (giấy bút, `loi_giai.md`)

Bài giấy bút: không chạy mã, có thể tự so với `loi_giai.md` (đáp án và cách tính) hoặc chấm 4 dòng đáp án bằng `bash labs/cham.sh BNX L35 bai_lam.md`.

Số liệu (số minh hoạ): tháng **31 ngày**; SLA **99,8%**; hai dịch vụ nối tiếp **99,9%** và **99,5%**; trong tháng có **hai sự cố 20 phút và 75 phút**.

Viết bốn dòng:
1. `ngan sach 99.8% thang 31 ngay: <số> phut` — số phút ngừng tối đa trong tháng.
2. `chuoi 99.9% va 99.5%: <số>%` — độ sẵn sàng chung khi hai dịch vụ nối tiếp (nhân hai tỉ lệ), 4 chữ số sau dấu phẩy.
3. `su co 20 + 75 = <tổng> phut: vuot ngan sach <số> phut` (hoặc `con trong ngan sach` nếu không vượt).
4. Viết khung tài liệu thiết kế một trang cho quyết định "tách truy vấn báo cáo sang bản sao đọc": ba mục **Bối cảnh, Quyết định, Hệ quả**; câu quyết định bắt đầu bằng "Chúng tôi sẽ"; hệ quả nêu cả mặt tiêu cực. **Danh mục kiểm** (tự chấm, có ngay ở đây): (a) có đủ ba mục Bối cảnh, Quyết định, Hệ quả; (b) câu quyết định bắt đầu bằng "Chúng tôi sẽ"; (c) hệ quả nêu cả mặt tiêu cực. Đạt cả ba thì ghi dòng `tai lieu thiet ke: du 3 muc, quyet dinh chu dong, he qua co mat tieu cuc`. Khung mẫu nằm ở cuối `loi_giai.md`.

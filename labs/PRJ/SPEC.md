# Quy chuẩn Bài tập Dự án theo Chặng (`PRJ L00–L10`)

Mỗi chặng học (`S01..S11`) kết thúc bằng một bài dự án tổng hợp (`PRJ L00..L10`) nhằm ghép toàn bộ kỹ năng rời rạc trong chặng thành sản phẩm chạy thật và kiểm thử tự động được.

## 1. Cấu trúc bắt buộc của mỗi bài dự án (`labs/PRJ/Lxx/`)

| Tệp | Vai trò | Yêu cầu |
|---|---|---|
| `de.md` | Đề bài, đầu vào mẫu, ràng buộc hiệu năng/bộ nhớ, thang chấm | Đọc đủ là làm được không cần đoán định dạng |
| `mong_doi.txt` | Kết quả chuẩn hóa từng dòng từ đầu ra thật của lời giải mẫu | Khớp 100% qua `bash labs/cham.sh PRJ Lxx <tep>` |
| `loi_giai.*` | Lời giải mẫu tham chiếu (`.py`, `.sh`, `.java`, `.c`, `.sql`) | Tự đứng được, chạy tất định không phụ thuộc mạng ngoài |

## 2. Thang chấm 100 điểm áp dụng thống nhất cho mọi bài dự án

1. **Tính đúng chức năng & bất biến (50 điểm):** Đầu ra khớp từng dòng `mong_doi.txt`, các bất biến miền nghiệp vụ (như cân bằng bút toán kép, khử trùng giao dịch, tính bảo toàn đồ thị) giữ đúng 100%.
2. **Xử lý biên & lỗi đầu vào (20 điểm):** Không sập khi dòng rỗng, bản ghi lỗi định dạng, số dư không đủ, chia 0 hoặc trùng khóa; mã thoát khác 0 hoặc báo lỗi rõ ràng theo quy ước đề.
3. **Đo quy mô & độ phức tạp (20 điểm):** Thực thi sạch ở ba cỡ dữ liệu (nhỏ, vừa, lớn); thuật toán và cấu trúc dữ liệu đạt đúng bậc độ phức tạp đã học trong chặng.
4. **Tính sạch & tái lập (10 điểm):** Không lộ bí mật cứng trong mã, không rò rỉ tài nguyên/tệp mở, chạy lại nhiều lần cho cùng kết quả tất định.

## 3. Phân bổ 11 bài theo Chặng (`WP-AF4-2` dựng trước `L00–L04`)

- `PRJ:L00` (Chặng 1): Sổ giao dịch CLI đa công cụ (Bash + Python + SQLite) — kiểm lọc lỗi CSV và số dư.
- `PRJ:L01` (Chặng 2): Lõi chuyển khoản bút toán kép + Outbox bất biến — `Σ nợ = Σ có` ở mọi ca thử.
- `PRJ:L02` (Chặng 3): Cổng tích hợp ngân hàng bảo mật: xác thực khung JWT chuẩn, lũy đẳng `Idempotency-Key`, phân trang ổn định.
- `PRJ:L03` (Chặng 4): Đối soát ba bên (Ngân hàng – NAPAS – Đối tác) + đánh đổi kiến trúc cho hội đồng phỏng vấn.
- `PRJ:L04` (Chặng 5): Đường đi chi phí thấp nhất trên đồ thị giao dịch & hồi quy tìm tham số bằng Gradient Descent.
- `PRJ:L05–L07` (Chặng 6–8, bổ sung ở `WP-AF4-3`) và `PRJ:L08–L10` (Chặng 9–11, bổ sung ở `WP-AF4-4`).

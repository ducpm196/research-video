# Quy chuẩn Bài tập Dự án theo Chặng (`PRJ L00–L10`)

Mỗi chặng học (`S01..S11`) kết thúc bằng một bài dự án tổng hợp (`PRJ L00..L10`) nhằm ghép toàn bộ kỹ năng rời rạc trong chặng thành sản phẩm chạy thật và kiểm thử tự động được theo chuẩn **Đạt / Chưa đạt** (không dùng thang điểm phần trăm hay thang điểm giả).

## 1. Cấu trúc bắt buộc của mỗi bài dự án (`labs/PRJ/Lxx/`)

| Tệp | Vai trò | Yêu cầu |
|---|---|---|
| `de.md` | Đề bài, khuôn dữ liệu `stdin`, khuôn đầu ra, ràng buộc và yêu cầu biên | Đọc đủ là tự cài được; không chép đáp án tĩnh của `mong_doi.txt` |
| `du_lieu.txt` | Dữ liệu mẫu công khai truyền qua `stdin` | Dữ liệu kiểm thử tách riêng khỏi ví dụ trên video |
| `mong_doi.txt` | Kết quả chuẩn hoá từng dòng cho `du_lieu.txt` | Khớp 100% qua `bash labs/cham.sh PRJ Lxx <tep>` |
| `ca_an/*.in`, `*.out` | Các ca kiểm thử ẩn bắt buộc (biên lỗi, dữ liệu lớn, chống in cứng) | Mọi bài `PRJ` đều có `ca_an/` theo `labs/CONTRACT.yaml` |
| `loi_giai.*` | Lời giải mẫu tham chiếu (`.py`, `.sh`, `.java`, `.c`, `.sql`) | Đọc từ `stdin`, tự đứng được, chạy tất định không phụ thuộc mạng ngoài |

## 2. Bốn nhóm kiểm thử nghiệm thu (Đạt / Chưa đạt)

1. **Đúng chức năng & bất biến:** Đầu ra khớp từng dòng `mong_doi.txt` và mọi ca ẩn; giữ đúng bất biến miền nghiệp vụ (cân bằng bút toán kép `Σ = 0`, khử trùng khoá lũy đẳng, bảo toàn sổ chính khi đối soát).
2. **Xử lý biên & lỗi đầu vào:** Không sập khi gặp dòng rỗng, bản ghi thiếu cột, số tiền âm hoặc `0`, số dư không đủ, tự chuyển cho chính mình, hoặc mã lệch chiều.
3. **Quy mô dữ liệu:** Chạy sạch ở cả ca nhỏ (`du_lieu.txt`) lẫn ca vừa/lớn trong `ca_an/` (hàng nghìn bản ghi) với thuật toán đúng bậc độ phức tạp đã học (`O(n)` đọc một lượt hoặc `O(n log n)` sắp xếp trộn).
4. **Sạch & tất định:** Không in cứng đáp án tĩnh, không lộ bí mật trong mã nguồn, chạy lặp lại nhiều lần cho kết quả giống nhau từng byte.

## 3. Phân bổ 11 bài theo Chặng

- `PRJ:L00` (Chặng 1): Sổ giao dịch CLI đa công cụ (Python + SQLite) — đọc CSV từ `stdin`, lọc dòng lỗi, đối chiếu số dư từng tài khoản giữa Python và SQLite.
- `PRJ:L01` (Chặng 2): Lõi chuyển khoản bút toán kép — khoá thứ tự tăng dần, từ chối thiếu số dư/biên lỗi, giữ bất biến `ledger_sum=0` và tổng tiền.
- `PRJ:L02` (Chặng 3): Cổng tích hợp ngân hàng bảo mật: xác thực khung JWT, lũy đẳng `Idempotency-Key`, phân trang con trỏ.
- `PRJ:L03` (Chặng 4): Đối soát ba bên (Ngân hàng – NAPAS – Đối tác) — tách khớp, lệch trạng thái và thiếu một chiều vào hàng đợi tra soát.
- `PRJ:L04` (Chặng 5): Đường đi chi phí thấp nhất trên đồ thị giao dịch & hồi quy công thức đóng.
- `PRJ:L05–L07` (Chặng 6–8) và `PRJ:L08–L10` (Chặng 9–11).

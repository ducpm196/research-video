# R7 BNK (vòng 7, đọc độc lập bản dựng sau lần sửa thứ ba, P1 chặt): 15/15 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a634b002b4928aa94)

## 1. Tóm tắt (vòng 4: 3/15 → 5: 7 → 6: 11 → 7: 10 chắc+vừa; ±1–4 là độ nhiễu giữa reader)
MUST 0 (15/15). P1=2: 10/15 chắc+vừa (P1=1: L01, L05, L07, L08, L13; P1=0: không bài nào); tính cả yếu 2/15 (L12, L14; P1=1: L04, L09, L11; 10 bài P1=0). Tổng 55 mục: 0 chắc, 7 vừa, 48 yếu (A 20, B 31, M 4). P8=2 15/15; P9=2 15/15; spec khớp 15/15 (L12 dựng sớm hơn, digest khớp); SRT khớp 15/15; lab ĐÚNG 15/15; 20/20 chương trình Java/Python và 9 tệp SQL khớp (L04 "2|0|216|SCAN tx" ra "2|0|0|…" trên sqlite 3.45.1 — cột số thứ ba phụ thuộc phiên bản, bài đã nói "ta chỉ đọc cột cuối"); 40/40 số khớp. SHOULD 5 (L02, L06, L10, L12, L13). Bảng cách đọc vừa sửa (L00: Runtime.getRuntime, totalMemory/freeMemory, static, ==, null, <>, x++; L01: try/catch InterruptedException, synchronized, for, return; L03: PRIMARY KEY, INSERT OR IGNORE, COUNT(*), WHERE; L08: BEGIN/COMMIT/ROLLBACK, UPDATE, INSERT outbox, DEFAULT) phủ đúng điều hứa; khung L00 74, L01 53/54/69, L03 55/80, L08 62/65/67 không tràn/đè/cắt/gãy dòng.
Nhận định: 4 mục vừa của vòng 6 ĐÃ ĐƯỢC SỬA (reader không còn nêu); 7 mục vừa mới là mục khác (reader khác xếp 'vừa' khác) → đo lường nhiễu (CB-P1-CODE); mục chắc = 0 liên tiếp ở R5, R6, R7.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L02 | quy_mo.0 (cột "hộp mặc định 10 kết nối") | "thiếu: kẹt" | công thức T·(C−1)+1 là ngưỡng bảo đảm không kẹt; thiếu hộp chỉ kẹt khi mọi kết nối bị giao dịch ngoài giữ; "có thể kẹt" (HikariCP báo hết thời gian chờ sau 30 giây) | thêm "có thể" | PLAUSIBLE |
| L06 | phụ đề intuition.1 và chay_that.4 (SRT dòng 139, 287) | "bị tạm dừng, ." và "ba mili giây, ." | phụ đề hiện dấu ", ." thừa do `say` có ", ." | xoá dấu thừa trong `say` | CONFIRMED |
| L10 | intuition.0 (khung 26) | nhãn "tương quan = M7" | nhãn đè cạnh dưới hộp "hàng đợi phản hồi" sát dòng chú thích; vẫn đọc được | dời nhãn | CONFIRMED |
| L12 | chay_that.1 (khung 78) | khung nhấn mạnh bọc tiêu đề | phải bọc dòng kết quả "3 1 1 1 / 150" | chỉnh `focus` | CONFIRMED |
| L13 | chay_that.4 (khung 81) | khung nhấn mạnh bọc dòng "Kết quả chạy thật" | như L12 | chỉnh `focus` | CONFIRMED |
Chưa kiểm được nguồn (giữ): L10 "T24 nay là Temenos Transact"; L11 PCI DSS 3.4.1, 3.5.1 và các trường ISO 8583 (khớp hiểu biết); L12 mô tả NAPAS (bài ghi chi tiết ở đặc tả chính thức); L13 TT 77/2025 (mốc 01/03/2026, 01/07/2026, VBHN 25), "kết hợp thêm một yếu tố nữa như mã dùng một lần" — giữ CHƯA KIỂM; TT 50/2024 khớp hiểu biết; L05 PL/SQL Oracle chỉ đọc (số học khối kiểm tay khớp: 1 500 000, 700 000 và 800 000); L06 Redis chỉ mô phỏng; ASR còn 12 câu chưa xem xét (L00, L01, L03, L04, L06, L08, L09, L13; lỗi nhận dạng thường: "bản tra" thay "bảng tra"...).

## 3. Mục chưa giảng — 7 mục VỪA (SỬA BẮT BUỘC) + yếu theo nhóm
Vừa:
1. L01 chay_that.10–11 `System.nanoTime()`, `/ 1_000_000` (A; không nói nano giây; manh mối: biến `ms`, `ms < 2000`).
2. L05 chay_that.7 `t1.join()` (B; L01 ⑥ dạy; manh mối lời đọc "chạy hai luồng").
3. L07 chay_that.1–2 `new StringBuilder(...)`, `sb.append(...)` (A; hàng ví dụ chỉ nói "nối chữ P và số p vào dòng"; không nói StringBuilder là gì; bảng một phần).
4. L08 chay_that.3 `for (int loi = 0; loi < 3; loi++)` (B; không có hàng cho `for` ở L08; manh mối: ví dụ hàng `j--`).
5. L08 chay_that.6 và .9 `PRIMARY KEY` (B; L03/L04 dạy; hàng ví dụ có mà không giảng).
6. L13 pitfalls.2 "API" (B; L03 dạy; manh mối: "gọi thẳng").
7. L13 formula.0 "TDES", "AES" (A; chỉ gọi "thuật toán chuẩn").
Yếu (48; xử lý được tới đâu hay tới đó, ưu tiên một hàng bảng 'nhắc lại cú pháp Java nền' ở L05, L06, L07, L08, L10: `System.out.println`, `return`, `//`, `import`, `+` nối chuỗi — mỗi cái là 1 mục B, đẩy L05 lên 9 mục và L08 lên 7): L00 `Object tk = new byte[1_000_000];`, `new HashMap<>()`, `BO_DEM.clear()`, `BigDecimal.ZERO`/`b.add(...)`, "(G1)"; L01 `"so du = " + soDu` (M; giảng ở chay_that.9), `//` (M; chay_that.8), `System.out.println` (B); L02 `System.out.println`, `//` (M; chay_that.2), `m.getName()`, "CGLIB", `rollbackFor`; L03 `ex.close()`, `sv.start()`, `new HashMap<>()`; L04 `AND` trong WHERE; L05 `t1.start()`, `System.out.println`, `+`, `//`, `PRIMARY KEY`, `WHERE id = 2`, `ORDER BY id`, `return duoc;`; L06 `new HashMap<>()`, `return v;`, `//`, `System.out.println`; L07 `m == 2 && !daSap` (M; giảng bằng lời ở chay_that.7, không có trên màn hình), `import java.util.Arrays;`, `System.out.println`, `return dem;`; L08 `CREATE TABLE`/`SELECT … FROM`, `import java.util.*;`, `System.out.println`, `//`, `nhatKy.add(...)`; L09 `AND`, `WHERE gd = 1`; L10 `import java.util.*;`, `System.out.println`, `//`, `return n;`, `HashMap`; L11 thụt lề và dấu `:` của `for so in truong:` (A; hàng ⑥ giảng `for k in d:` nhưng không nói thụt lề); L13 `==` Python (B; L12), `#` (B; L11). L12, L14: không có mục nào.

## 4. Người học kẹt ở đâu
L00 không kẹt (chậm nhẹ chay_that.2 `Object tk = new byte[1_000_000];`); L01 chay_that.10–11 `(System.nanoTime() - t0) / 1_000_000` không giải thích nano giây; L05 chay_that.7 `t1.start(); t2.start(); t1.join(); t2.join();` không có hàng đọc; L07 chay_that.1–2 `new StringBuilder("bo doc " + b + ":")`, `sb.append(" P").append(p++)`; L08 chay_that.3 `for (int loi = 0; loi < 3; loi++)`, sau đó `PRIMARY KEY` ở chay_that.9; L11 dễ vấp thụt lề ở chay_that.1; L13 formula.0 "TDES với khối định dạng 0, AES đi với định dạng 4"; các bài còn lại không kẹt.

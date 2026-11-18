# R6 INT (vòng 6, đọc độc lập bản dựng sau sửa, P1 chặt): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a201c2a52975f13a6)

## 1. Tóm tắt
MUST 0 (9/9). P1=2: 6/9 chắc+vừa (L00, L02, L05, L06, L07, L08; L01, L03, L04 = 1); tính cả yếu 1/9 (L07). 4 mục vừa, 0 chắc, 15 yếu. P8=2 9/9 (cả 9 lab là giấy-bút; `cham.sh` không chấm .md; reader tính lại 43/43 dòng đáp án khớp mong_doi.txt; chỉ L01 hướng dẫn cách tự chạy mã — theo ADDENDUM vẫn P8=2, nhưng ghi nhận: L00, L02–L08 không có lệnh để người học gõ chạy); P9=2 9/9; spec khớp 9/9; SRT khớp 9/9; `checks` 214/214; 12/12 khối Python và 2/2 Java (L01 `LuongAo`, L02 `TuGoi` 6 dòng) khớp. Không có mục chắc. Mất gốc ĐỦ 9/9 (cả yếu: ĐỦ 5, GẦN 4: L01–L04). 55 khung hình đã xem: không tràn/đè/cắt; gãy dòng nhẹ ở bảng L03 quymo.2, ô mã L05/L07/L08. Tiêu đề L06 mới (khung 5) không bị cắt. SVG L03 Outbox/CDC (khung 24) và lưới bản đồ bit L04 (khung 17) đạt.
Chưa kiểm được nguồn (bài đã tự ghi): TT 50/2024, TT 77/2025, QĐ 2345 (ngưỡng 10/20 triệu) L05, L06; TT 31/2024, TT 37/2025 L08; luật lao động thử việc L07; tin tuyển dụng ACB "đọc 2026-11" L00, L07; danh sách học phần Cử nhân AI UIT L05; đặc tả OFS Temenos, NAPAS 247, mã 68 theo NAPAS L04; `server.tomcat.threads.max` không còn tác dụng khi bật luồng ảo L01.

## 2. SHOULD
| Bài | Cảnh | Trích | Vấn đề | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L01 | quiz.1 | "StringBuilder gấp đôi mảng đệm mỗi khi đầy: các lần cấp lại chép 16 + 32 + 64 + 128 + 256 + 512 = 1 008 ký tự" | JDK `AbstractStringBuilder.newCapacity`: dung lượng mới = cũ×2 + 2, không đúng gấp đôi (cùng bậc, chưa mở mã nguồn JDK) | "khoảng gấp đôi" | PLAUSIBLE |
| L02 | chaythat.3–5 | mã `TuGoi.java` | chương trình Java cắt thành 3 màn hình xoá nền, không khung nào thấy trọn mã để gõ lại (L01 có một màn hình trọn) | thêm một khung hiện đủ chương trình | CONFIRMED |
| L03 | quymo.2 (khung 67) | cột "SAGA": "40 / giây" | cột hẹp, "40 giây" gãy 2 dòng ở cả 3 hàng | nới cột | CONFIRMED |
| L04 | prereq.4 | "Làm đủ 16 cặp ta được khối PIN rõ" (lời đọc "mười sáu cặp") | ví dụ ngay trên dùng "cặp 34 và 19 cho 2D" (cặp 2 chữ số) → chỉ 16/2 = 8 cặp; nếu "cặp" = một chữ số hệ 16 thì ví dụ sai | "8 cặp hai chữ số" hoặc "16 chữ số" | CONFIRMED (tự mâu thuẫn) |
| L04 | `asr_report` | "câu: 99", checked_at 2026-11-16T01:26Z | bản dựng L04 có 98 câu, built_at 13:04Z → báo cáo ASR cũ hơn bản dựng | chạy lại ASR L04 | CONFIRMED |
| L05, L07, L08 | L05 chaythat.0 (khung 36); L07 quymo.0 (50); L08 quymo.0 (66) | ví dụ L07: "chenh = 4 * (13 + / 2) # ..." | cột "viết trong mã" của bảng Đọc trước gãy dòng giữa biểu thức | nới cột mã hoặc `white-space: nowrap` | CONFIRMED |
| L06 | concept.1 (khung 22) | "Kiến trúc 4 Tầng Payment Hub" (lời "ta vẽ sơ đồ bốn tầng") | hình chỉ là 4 thanh xếp chồng, không mũi tên luồng yêu cầu | vẽ luồng yêu cầu qua 4 tầng | CONFIRMED |
| L06 | hook.1 | hàng 3 của bảng | thiếu `</td>` ô giữa (trình duyệt tự đóng; khung 5 đúng) | thêm thẻ đóng | CONFIRMED |
| L08 | example.0 (khung 43) | "O(N^2)" | hiện chữ `^`, dòng sau dùng mũ thật | dùng mũ thật | CONFIRMED |
| L08 | quymo.1, lab (P2) | `xep = 3 * n * math.ceil(math.log2(n)) + 2 * (n + n)` | vì sao nhân 3 và 2×(n+n) chỉ có trong chú thích mã; lab bảo "công thức như trong bài" | thêm một dòng giải thích: 3 lần sắp xếp, 2 lượt hai con trỏ trên hai danh sách | CONFIRMED |
Đường học: L08 khai `requires: [L07]` + `requires_ext` PYT dù bài dùng NAPAS/T24/Redis học ở L00–L04 (bài tự giải nghĩa phần lớn; riêng "NAPAS" thì không).

## 3. Mục chưa giảng (4 vừa, 0 chắc, 15 yếu)
Vừa (SỬA BẮT BUỘC):
1. L01 concept.0 "Bể kết nối, Đệm tĩnh" (ô Old Gen) (A; ô "Chứa đối tượng sống lâu năm" gợi "tồn tại lâu" nhưng không đoán được "đệm tĩnh" là gì; L00 giảng "bể kết nối", chưa bao giờ giảng "đệm tĩnh").
2. L03 quymo.0 `doi_tac = [('nhanh 20 ms', 0.020), ...]` (M; tên biến, chú thích, kết quả in gợi "danh sách các cặp (tên, giây)"; bảng cách đọc ở quymo.1, SAU).
3. L03 quymo.0 `for ten, rtt in doi_tac:` (M; lấy từng cặp ra hai biến — bảng ở quymo.1, sau).
4. L04 prereq.1–2 "bit thứ k", "byte 1 (bit 1–8) bật bit 3, 4 → 0011 0000 = 30" (A; ví dụ "0011 → 3, 1111 → F" gợi bit là chữ số 0/1, "dịch trái" ở chaythat có giải nghĩa; không có câu định nghĩa bit/nhị phân ở bài nào trong khoá).
Yếu: L00 example.4 "MySQL InnoDB còn khoá cả khoảng trống giữa các giá trị" (chỉ chữ, không đọc), concept.0 "kho dữ liệu nằm trong RAM" (M; "RAM (bộ nhớ chính)" ở concept.2); L01 "Bộ nhớ native ngoài heap", "JDK" ("cần cài JDK 21", example.2 và .6); L02 quiz.0–1 "AOP Aspect", "Servlet Filter" ("Servlet" không giải), symbol.0 "tổng kết nối của mọi instance ứng dụng"; L03 quymo.0 `toc, xong = round(1 / giu, 2), round(tong * giu)` (B+M; L01 giảng `cao, suc = 0, 1`; bảng ở quymo.1), prereq.0 "Không phải tỉ lệ uptime" (B), quiz.1 "địa chỉ dòng bị khoá"; L04 symbol.2 "khoá khử trùng" (M; định nghĩa pitfall.1), prereq.4 "bỏ chữ số kiểm tra cuối"; L05 prereq.0 "độ tương đồng cosine" (M; giảng symbol.0–2), concept.2 "hiệu chỉnh trên dữ liệu thật"; L06 concept.2 "cơ chế gọi lại bất đồng bộ"; L08 example.0 "NAPAS" (B; L00 và L04 giảng).
Bảng cách đọc có phủ: L00 (Python `w =`, `#`, `for … in (…)`, `print`, `**`, `round`; Redis `SET … NX EX`; SQL `INSERT INTO … VALUES`, `UNIQUE`, `SELECT … FOR UPDATE`), L01 (Java `double`, `new BigDecimal`, `.add`, `import`, `class`, `main`, `throws`, `try (var …)`, `for`, `ex.submit(() ->`, `println`; `log_m`, `ceil`; Python `while`, `*=`; dòng cấu hình `spring.threads.virtual.enabled=true` chỉ chú thích), L02, L03 (Python: bảng đến sau mã, ở quymo.1), L04, L05, L06, L07, L08.
Cần biết trước (dùng mà không giảng tại chỗ): L01 "Đệm tĩnh", "native", "JDK"; L02 AOP, Servlet; L03 cú pháp ghép cặp `for ten, rtt in …`; L04 nhị phân/bit, "chữ số kiểm tra"; L08 "NAPAS".

## 4. Người học kẹt ở đâu
L00 không kẹt (gần nhất: example.4 "MySQL InnoDB … khoảng trống"); L01 concept.0 (khung 22) "Bể kết nối, Đệm tĩnh" (nhỏ); L02 quiz.1 "Servlet Filter … AOP Aspect" (nhỏ); L03 quymo.0 mã `doi_tac = [...]` rồi `for ten, rtt in doi_tac:` hiện trước bảng "Cách đọc" (bảng ở quymo.1); L04 prereq.2 "byte 1 (bit 1–8) bật bit 3, 4 → 0011 0000 = 30" (người chưa biết nhị phân không hiểu bit và 0011); L05 prereq.0 "độ tương đồng cosine" (nhỏ); L08 quymo.1 và lab "3 * n * math.ceil(math.log2(n)) + 2 * (n + n)" (không ai giải thích vì sao 3 và 2×(n+n), lab đòi tự tính theo công thức này); L06, L07 không kẹt.

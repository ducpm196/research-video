# R4 INT L00–L08 (vòng 4, đọc độc lập): 9/9 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a44ea59fc80efb2df)

## 1. Tóm tắt
MUST 0 (9/9). P1=2 (chỉ mục "chắc"): 7/9 (L00, L03–L08); L01=1, L02=1. Nếu tính cả mục "yếu": 0/9 (≥ 5 mục yếu mỗi bài). P8=2 9/9; P9=2 9/9. spec khớp 9/9; SRT khớp 9/9. Lab: cả 9 là giấy-bút (loi_giai.md; cham.sh không chấm .md) — 0/9 chạy bằng lệnh; 9/9 giải lại độc lập bằng Python khớp mong_doi.txt (L06 dòng 4 mơ hồ, xem SHOULD-3). Mã Python 12/12 khớp; Java 2/2 (L01 LuongAo; L02 TuGoi 6 dòng); SQL sqlite 2/2. Không chạy được: PL/SQL (L03), Redis/Spring (L02), ONNX Java (L05). ~100 số tính lại khớp.
Điểm khác: L02 P2=1 (REQUIRES_NEW và Bloom không có ví dụ số/vết), P5=1 (quiz Filter/Interceptor in sẵn vị trí từng thành phần → lộ đáp án A); L03 P3=1 (Outbox/CDC, 2PC, replica Kafka chỉ là chữ, chỉ SAGA có hình), P5=1 (quiz toàn đáp án rõ sai); L06 P5=1 (quiz 90 ngày không tính toán, phương án sai quá lộ), P7=1 (tiêu đề/recap hứa "100 câu"); L00 scene `check` cột "đánh giá" lộ đáp án trước khi dừng; L04 bản đồ bit không có lưới hình.

## 2. SHOULD
| Mã | Bài | Vị trí | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| 1 | L02 | `curriculum/int.yaml` mục L02 trường `fix` | "tách service hoặc inject qua ApplicationContext" | bài không dạy ApplicationContext (0 lần trong YAML) | sửa `fix` hoặc thêm 1 câu | CONFIRMED |
| 2 | L06 | tiêu đề, hook, recap | "Bộ 100 Câu hỏi Phỏng vấn Thực chiến"; recap "Làm chủ 100 Câu hỏi Thực chiến theo Phương pháp 5 Tầng" | hook nói bộ 100 câu chỉ là bộ luyện thêm; bài có 5 tình huống | đổi tiêu đề/recap | CONFIRMED |
| 3 | L06 | practice `de.md` dòng 4 | "y = 525 600 × (1 − tích), 1 chữ số" | 788.0 chỉ đúng với tích chưa làm tròn (0,99850075); dùng x đã làm tròn 99,85% ra 788,4 | ghi rõ "dùng tích chưa làm tròn" | PLAUSIBLE |
| 4 | L04, L05 | L04 hook bước 0; L05 prereq bước 1, check bước 0 | "bạn đã tích hợp với T24 ở OCB…" (chỉ trên màn hình) | lời đọc bỏ chi tiết OCB; lệch màn hình/lời đọc; chưa kiểm nguồn hồ sơ | đọc ra hoặc bỏ khỏi màn hình | CONFIRMED (lệch chữ) |
| 5 | L04 | symbol bước 0 | "gồm năm phần cách nhau bằng dấu phẩy" | các cặp trường=giá trị cũng cách nhau bằng dấu phẩy | nói "năm nhóm" | PLAUSIBLE |
Chưa kiểm được nguồn (không phải lỗi; GIỮ nhãn, không bịa số): TT 50/2024/TT-NHNN, TT 77/2025/TT-NHNN, QĐ 2345/QĐ-NHNN, ngưỡng 10 triệu/20 triệu và biên "trên"/"từ" (L05, L06, de.md L06); TT 31/2024, TT 37/2025, "quá hạn 10–90 ngày là nhóm 2, nhóm 3–5 là nợ xấu" (L08; văn bản gốc có thể là TT 11/2021); mã phản hồi 68 (NAPAS vs ISO 8583 gốc "phản hồi quá muộn"), đảo 0400/0420 luồng 247, mã xử lý 40xxxx, OFS ACTP/I/PROCESS//0, "AZ là phân hệ tiền gửi của T24" (L04, L08); "tin tuyển dụng ACB đã lưu", danh sách học phần Cử nhân AI UIT (L00, L05, L07). Đối chiếu công khai khớp: RFC 9457 thay RFC 7807, JEP 444/491, HikariCP, UCB1 (Auer 2002), payShield CA/CC/JE/JC, khối PIN định dạng 0, MTI/bản đồ bit, Kafka 3−2=1, khoá hàng Oracle. Khoá INT không có `audit/int/sources*.md`.

## 3. Mục chưa giảng (P1) — chỉ mục "chắc" (điểm P1) + mục "yếu" (để fixer xử lý hết)
Chắc: L01 quiz/1 "Chi phí tuyến tính (khấu hao)" (A); L02 chaythat/1 `Class<?>[] gt = { Dv.class };` (A) và `Proxy.newProxyInstance(Dv.class.getClassLoader(), gt, vv)` (A; lời đọc chỉ nói "bọc bằng lớp vỏ").
Yếu (xử lý hết):
- L00: example/1 `SET lock:transfer:TXN_998822 1 NX EX 60` (SET, tên khoá, giá trị 1); example/3 `SELECT … FOR UPDATE`; "Oracle và PostgreSQL", "MySQL InnoDB … khoá khoảng"; "UIT", "ACB"; quymo/0 `print(...)`, `#`, `(500, 50000, 5000000)`; Kafka/SAGA/Outbox dùng trước khi giải nghĩa; "đối soát" dùng ở quymo/2, giảng ở check/1.
- L01: prereq/2 `double d = …`, `new BigDecimal("0.1").add(new BigDecimal("0.2"))`; symbol/1 `log_m(N)`, `log_1000(10^7) = 7/3`; JEP 444, G1/ZGC, `@Contended`, `-XX:-RestrictContended`, "lập lịch", XML; example/3 `System.out.println`, `var`, `int i`, `i++`, `static`; mã Java/Python hiện trước, bảng ngay sau (M).
- L02: `public static void main(String[] args)`, `import java.lang.reflect.*;` (B); `moGD++`, `InvocationHandler`, ép kiểu `(Dv)`; "Hàm Transactional", "gọi qua this"; `redis.getOperations().delete`, `serialize`, `rollbackFor = Exception.class`, RFC/IETF, "Spring MVC", "bắt tay TLS"; "Controller" dùng ở prereq/1 giảng ở quiz (M).
- L03: `ORDER BY`; `OPEN … LOOP … END LOOP … CLOSE`, `GREATEST`, `l_accounts(i).amount`; "TLS client-broker", `socket_fd`/`file_fd`; "SQL", "trích nợ", "hạch toán", "đám mây".
- L04: `bit = [3, 4, 11, 37, 52]`, `print(...)`, `pin`/`pan`; "POS", "PIN", ISO 4217, ISO 9564, "thụ hưởng", `TRANSACTION.TYPE=AC`, `ACTP/I/PROCESS//0`; mã Python trước, bảng sau (M).
- L05: `import math`; "if-else", "p95", "API", "chống rửa tiền", "ĐHQG-HCM", "Inbound", `env`, tên học phần ML/DL/CV; công thức `\ln N` giảng ở bước sau (M).
- L06: `if (domainComplexity == LOW && teamSize < 10)` (`&&`, `==`, `LOW`); "thủ tục lưu trữ", "Site Reliability Engineering", "5 Whys", `import math`; `UPDATE … SET … WHERE` hiện trước, bảng sau (M).
- L07: "neo mức đề xuất", "HR"; quymo/0 `tong, tang = 0, 1.0`, `# comment`.
- L08: "giải ngân" (không định nghĩa), "NHNN", "bội số lương", "thẻ ảo", "rút tiền mặt trả góp", "thu hộ"; `if / else if / else`, tên hàm `matchOrFlagAmount…`, `import math`; `&&`, `.size()`, `.rrn`, `==` ở step 4, bảng step 5 (M).
Bảng "cách đọc" đã có ngay sau mọi đoạn mã; chỗ chưa phủ chủ yếu là token lẻ.

## 4. Người học kẹt ở đâu
L00 example/1 `SET lock:… NX EX 60` (nhẹ); L01 quiz/1 "khấu hao" (kẹt thật); L02 chaythat/1 `Class<?>[]… Proxy.newProxyInstance(…)`; L03 example/4 `OPEN cur_payroll; LOOP … CLOSE` (chùng); L04–L05 không kẹt; L06 symbol/1 `&&` `==` (chùng); L07 không kẹt; L08 "giải ngân" (chùng).

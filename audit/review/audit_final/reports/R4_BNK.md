# R4 BNK (vòng 4, đọc độc lập, P1 chặt): 15/15 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a54a92520f3aa1a7e)

## 1. Tóm tắt
MUST 0 (15/15). P1=2: 3/15 (L09, L12, L14); P1=1: 11 bài; P1=0: L00. P8=2: 15/15; P9=2: 15/15. spec khớp 15/15; SRT khớp 15/15; lab ĐÚNG 15/15 (L05 PL/SQL Oracle chỉ đọc, không chạy Docker). ~36 đoạn mã chạy khớp (Java 21, sqlite 3.49.1, Python). ~120 số tính lại, 0 sai. SHOULD 7. Mất gốc: ĐỦ 14, GẦN 1 (L00 = 12, có một mục 0).
Gốc P1: cú pháp Java không có bảng cách đọc — chữ ký hàm (kiểu trả về, tham số, public/static/void), chỉ số mảng, `p++` làm đối số, ép kiểu, `.length`. Python (L11–L13) và SQL (L03/L04/L09/L12/L14) đã có bảng cách đọc ở bài đầu tiên dùng.

## 2. SHOULD
| Bài | Cảnh | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L08 | chay_that step 5–7 | "Ghi kép: lưu số dư rồi sập…" (1500000 / 0); "Cùng giao dịch đó nhưng bị huỷ…" (2000000 / 0) | Màn hình không nói đặt lại bảng; chạy nối tiếp từ step 3 cho 1000000 / 1 vì outbox đã có 1 dòng; chạy trên bảng mới thì đúng | thêm "chạy trên bảng mới" hoặc dựng lại bảng mỗi kịch bản | CONFIRMED |
| L10 | chay_that step 0, khung 00061 | `// mỗi phản hồi: mã tương quan, việc đã làm` | chú thích tràn ngoài khung mã (x≈1893 vs viền ≈1840) | rút ngắn/xuống dòng | CONFIRMED |
| L10 | sym step 0 | "Temenos T24 / phần mềm lõi ngân hàng" | sản phẩm nay thường gọi Temenos Transact (chưa tra nguồn) | ghi chú "nay là Transact" nếu có nguồn | PLAUSIBLE |
| L13 | formula step 2 | "chuyển tiền … phải xác thực sinh trắc học (Phụ lục 01)" | nguồn thứ cấp ghi ngưỡng 10 triệu/20 triệu ở Phụ lục 02; chưa mở bản gốc; bài tự ghi CHƯA KIỂM | kiểm bản gốc rồi sửa số phụ lục (giữ CHƯA KIỂM đến khi có văn bản gốc, không bịa số) | PLAUSIBLE |
| L05 | chay_that step 1–2 | "Chạy thật trên Oracle 26ai Free (Docker)", `DBMS_OUTPUT.PUT_LINE` | màn hình không nhắc `SET SERVEROUTPUT ON` | ghi lệnh bật in đầu ra | PLAUSIBLE |
| L09 | check step 0–1 | "Ta cố ý sửa một dòng của giao dịch 1", bảng `1 (đã sửa lén) \| −100, +90` | câu UPDATE không hiện; số đổi sang bộ khác không báo | hiện lệnh sửa hoặc nói rõ bảng thử khác | PLAUSIBLE |
| L08 | quy_mo | "bộ chuyển tiếp = sự kiện mỗi giây ÷ 1 000, làm tròn lên (11 574 thành 12)" | tính theo tải trung bình, không tính đỉnh tải | thêm "chưa tính đỉnh tải" | PLAUSIBLE |
Nguồn pháp lý nhắc tới (thứ cấp, không dùng làm nguồn chốt): hoatieu.vn, luatvietnam.vn (TT 50/2024, TT 77/2025). Ngày hiệu lực TT 50 = 01/01/2025, TT 77/2025 = 01/3/2026 khớp nhưng chỉ số phụ lục cần bản gốc.

## 3. Mục chưa giảng (P1 chặt)
| Bài | Cảnh/step | Trích | Bảng cách đọc phủ |
|---|---|---|---|
| L00 | chay_that 2 | `static long dungMB() {` | không (sym chỉ đọc nguyên khối main) |
| L00 | practice 0 | `javac PhiLech.java && java PhiLech` | không (`&&` không giải thích) |
| L00 | sym 1, check 1 | "số thực nhị phân" | không (chưa định nghĩa nhị phân; L11 mới dạy) |
| L01 | chay_that 0 | `static void nap(int tien, int cho) {` | không |
| L01 | chay_that 3 | `static final Object KHOA = new Object();` | có (final ở L00) nhưng L01 không nhắc lại |
| L02 | chay_that 0 | `public void chuyenTien() { ghiVet(); }`; `interface Dich { void chuyenTien(); … }` | không (void/public) |
| L02 | chay_that 1 | `Dich proxy = (Dich) Proxy.newProxyInstance(…)` | không (ép kiểu `(Dich)`) |
| L03 | chay_that 0 | `static void tra(HttpExchange ex, String s) throws IOException {` | không (danh sách tham số) |
| L03 | chay_that 0–1 | `ex.sendResponseHeaders(200, s.length());`; `HttpServer.create(new InetSocketAddress(8099), 0)` | không (`s.length()`, đối số `0`) |
| L04 | chay_that 3 | `2\|0\|56\|SEARCH tx USING COVERING INDEX i_tk (tk=?)` | không (`(tk=?)`) |
| L05 | chay_that 4–5 | `static boolean lam(Lock dau, Lock sau) {`; `static String thu(Lock x1, Lock y1, Lock x2, Lock y2) throws Exception {` | không |
| L05 | practice 2 (gợi ý) | `int[][] lenh = {…}`, `for (int[] l : lenh)`, `l[0]`, `l[1]` | không |
| L06 | chay_that 0, 2 | `static long soDu(int tk) {`; `static boolean ghi(long ma, String v) {` | không |
| L06 | chay_that 1 | `"…" + tong / 100.0 + " ms"` | không (vì sao `.0`) |
| L07 | chay_that 2 | `static int[] chay(boolean ghiNhoTruoc) {` | không |
| L07 | chay_that 0 | `for (int k = 0; k < so; k++) sb.append(" P").append(p++);` | không (`p++` làm đối số) |
| L08 | chay_that 3 | `da_gui INTEGER DEFAULT 0` | không |
| L08 | chay_that 5–7 | `SELECT COUNT(*) FROM outbox;` | có (L03/L04) nhưng L08 không nhắc lại |
| L10 | chay_that 3 | `static int soLanGhiNo(boolean daHachToan, boolean hoiTruoc) {` | không |
| L10 | chay_that 1 | `for (int k = 0; k < ve.length; k++)` | không (`.length` mảng) |
| L11 | practice 2 (gợi ý) | `"".join(truong[k] for k in sorted(truong))` | không (`sorted`) |
| L13 | chay_that 2 | `hmac.new(b"k", nd.encode(), hashlib.sha256)` | không (`.encode()`) |
| L13 | chay_that 2 | `pan[:6] + "*" * 6 + pan[-4:]` | không (nhân chuỗi `"*" * 6`) |
Không có mục ở L09, L12, L14.
Đếm theo bài (xấp xỉ từ danh sách): L00 3, L01 2, L02 2, L03 2(-3), L04 1, L05 2–3, L06 2, L07 2, L08 2, L10 2, L11 1, L13 2.
Đề xuất của reader: bảng "cách đọc" cho chữ ký hàm Java (kiểu trả về, tham số, public/static/void), chỉ số mảng, `p++`, ép kiểu, `.length`, ở bài Java đầu tiên dùng chúng — và nhắc lại một dòng ở mỗi bài dùng lại (BNK tự đứng được).
